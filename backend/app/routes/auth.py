"""
Authentication Routes for CancerCare AI
Provides user registration, login, logout, and session management
"""

from fastapi import APIRouter, HTTPException, Header, Request
from pydantic import BaseModel, EmailStr
from typing import Optional
import os

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from secure_database import SecureDatabase

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Initialize secure database
db = SecureDatabase()

# Request/Response Models
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    age: Optional[int] = None
    gender: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[str] = None
    session_token: Optional[str] = None
    user_info: Optional[dict] = None
    otp: Optional[str] = None

class LogoutRequest(BaseModel):
    session_token: str

class VerifyOTPRequest(BaseModel):
    email: str
    otp: str

# Helper function to get client info
def get_client_info(request: Request):
    """Extract client IP and user agent from request"""
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", None)
    return ip_address, user_agent

@router.post("/register", response_model=AuthResponse)
async def register(data: RegisterRequest, request: Request):
    """
    Register a new user
    
    - **name**: User's full name
    - **email**: User's email address
    - **phone**: User's phone number (optional)
    - **password**: User's password (will be hashed)
    
    Returns user_id and session_token on success
    """
    try:
        # Get client info
        ip_address, user_agent = get_client_info(request)
        
        # Create user
        user_id = db.create_user(
            name=data.name,
            email=data.email,
            phone=data.phone,
            password=data.password,
            age=data.age,
            gender=data.gender,
            security_level="standard"
        )
        
        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="User registration failed. Email may already exist."
            )
        
        # Create session for the new user
        session_token = db.create_session(user_id, ip_address, user_agent)
        
        if not session_token:
            raise HTTPException(
                status_code=500,
                detail="Session creation failed"
            )
        
        # Get user info
        user_info = db.get_user_info(user_id)
        
        # Create OTP for verification
        otp = db.create_otp(data.email, "email", user_id)
        # Log OTP to server console only (never send to client in production)
        if os.environ.get("DEBUG", "false").lower() == "true":
            print(f"DEBUG: OTP for {data.email} is {otp}")
        
        return {
            "success": True,
            "message": "Registration successful. Please check your email for the verification code.",
            "user_id": user_id,
            "session_token": session_token,
            "user_info": user_info,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration error: {str(e)}"
        )

@router.post("/verify-otp", response_model=AuthResponse)
async def verify_otp(data: VerifyOTPRequest, request: Request):
    """
    Verify OTP for a user
    """
    try:
        ip_address, user_agent = get_client_info(request)
        
        # Verify OTP
        is_valid = db.verify_otp(data.email, data.otp, "email")
        
        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired OTP"
            )
        
        return AuthResponse(
            success=True,
            message="OTP verified successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OTP verification error: {str(e)}"
        )

@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest, request: Request):
    """
    Login user with email and password
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns user_id and session_token on success
    """
    try:
        # Get client info
        ip_address, user_agent = get_client_info(request)
        
        # Authenticate user
        user_id = db.authenticate_user(
            email=data.email,
            password=data.password,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        if not user_id:
            # Check if user exists but is locked
            conn = db._get_connection()
            users = conn.cursor().execute("SELECT user_id, email_encrypted, account_locked FROM users").fetchall()
            
            is_locked = False
            for u in users:
                if db._decrypt_data(u[1]).lower() == data.email.lower() and u[2]:
                    is_locked = True
                    break
                    
            if is_locked:
                raise HTTPException(
                    status_code=401,
                    detail="Account is locked due to multiple failed attempts. Please contact support."
                )
            else:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid email or password."
                )
        
        # Create new session
        session_token = db.create_session(user_id, ip_address, user_agent)
        
        if not session_token:
            raise HTTPException(
                status_code=500,
                detail="Session creation failed"
            )
        
        # Get user info
        user_info = db.get_user_info(user_id)
        
        return AuthResponse(
            success=True,
            message="Login successful",
            user_id=user_id,
            session_token=session_token,
            user_info=user_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Login error: {str(e)}"
        )

@router.post("/logout", response_model=AuthResponse)
async def logout(data: LogoutRequest, request: Request):
    """
    Logout user by invalidating session
    
    - **session_token**: User's session token
    """
    try:
        # Get client info
        ip_address, user_agent = get_client_info(request)
        
        # Verify session exists
        session_result = db.verify_session(data.session_token, ip_address, user_agent)
        
        if not session_result:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired session"
            )
        user_id = session_result.get('user_id') if isinstance(session_result, dict) else session_result
        
        # Invalidate session
        try:
            conn = db._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE user_sessions SET is_active = 0 WHERE session_token = ?",
                (data.session_token,)
            )
            conn.commit()
        except Exception:
            pass  # Session invalidation is best-effort
        
        # Log logout event
        db._log_security_event(
            user_id, "LOGOUT", True, 
            "User logged out successfully", 
            ip_address, user_agent
        )
        
        return AuthResponse(
            success=True,
            message="Logout successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Logout error: {str(e)}"
        )

@router.get("/verify", response_model=AuthResponse)
async def verify_session(
    request: Request,
    authorization: Optional[str] = Header(None)
):
    """
    Verify session token and return user info
    
    Expects Authorization header with format: "Bearer <session_token>"
    """
    try:
        if not authorization:
            raise HTTPException(
                status_code=401,
                detail="No authorization header provided"
            )
        
        # Extract token from "Bearer <token>" format
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authorization header format. Use: Bearer <token>"
            )
        
        session_token = parts[1]
        
        # Get client info
        ip_address, user_agent = get_client_info(request)
        
        # Verify session
        session_result = db.verify_session(session_token, ip_address, user_agent)
        
        if not session_result:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired session"
            )
        user_id = session_result.get('user_id') if isinstance(session_result, dict) else session_result
        
        # Get user info
        user_info = db.get_user_info(user_id)
        
        if not user_info:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        return AuthResponse(
            success=True,
            message="Session valid",
            user_id=user_id,
            user_info=user_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Verification error: {str(e)}"
        )

@router.get("/profile", response_model=AuthResponse)
async def get_profile(
    request: Request,
    authorization: Optional[str] = Header(None)
):
    """
    Get user profile information
    
    Expects Authorization header with format: "Bearer <session_token>"
    """
    try:
        if not authorization:
            raise HTTPException(
                status_code=401,
                detail="No authorization header provided"
            )
        
        # Extract token
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authorization header format"
            )
        
        session_token = parts[1]
        
        # Get client info
        ip_address, user_agent = get_client_info(request)
        
        # Verify session
        session_result = db.verify_session(session_token, ip_address, user_agent)
        
        if not session_result:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired session"
            )
        user_id = session_result.get('user_id') if isinstance(session_result, dict) else session_result
        
        # Get user info
        user_info = db.get_user_info(user_id)
        
        if not user_info:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        return AuthResponse(
            success=True,
            message="Profile retrieved successfully",
            user_id=user_id,
            user_info=user_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Profile retrieval error: {str(e)}"
        )
