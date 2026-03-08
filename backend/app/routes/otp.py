"""
OTP Routes for CancerCare System
Handles OTP request, verification, and resend functionality
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Literal
import re
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.services.otp_service import OTPService

router = APIRouter(prefix="/api/otp", tags=["OTP"])

# Initialize OTP service
otp_service = OTPService()

# Request/Response Models
class SendOTPRequest(BaseModel):
    contact: str  # Email or phone number
    method: Literal["email", "phone"]
    user_id: Optional[str] = None
    
    @validator('contact')
    def validate_contact(cls, v, values):
        """Validate email or phone format"""
        method = values.get('method', 'email')
        if method == 'email':
            # Basic email validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, v):
                raise ValueError('Invalid email format')
        elif method == 'phone':
            # Basic phone validation (digits only, 10-15 digits)
            phone_pattern = r'^\+?[1-9]\d{9,14}$'
            cleaned_phone = re.sub(r'[\s\-\(\)]', '', v)
            if not re.match(phone_pattern, cleaned_phone):
                raise ValueError('Invalid phone number format')
        return v

class VerifyOTPRequest(BaseModel):
    contact: str
    otp: str
    method: Literal["email", "phone"]
    
    @validator('otp')
    def validate_otp(cls, v):
        """Validate OTP format (6 digits)"""
        if not re.match(r'^\d{6}$', v):
            raise ValueError('OTP must be 6 digits')
        return v

class ResendOTPRequest(BaseModel):
    contact: str
    method: Literal["email", "phone"]
    user_id: Optional[str] = None

class OTPResponse(BaseModel):
    success: bool
    message: str
    otp: Optional[str] = None  # Only for testing, remove in production
    expires_in_minutes: int = 10

@router.post("/send", response_model=OTPResponse)
async def send_otp(data: SendOTPRequest, request: Request):
    """
    Send OTP to user's email or phone
    
    - **contact**: Email address or phone number
    - **method**: 'email' or 'phone'
    - **user_id**: Optional user ID if OTP is for existing user
    
    Returns success status and OTP (for testing)
    """
    try:
        # Create and send OTP
        otp = otp_service.create_and_send_otp(
            contact=data.contact,
            method=data.method,
            user_id=data.user_id
        )
        
        if not otp:
            raise HTTPException(
                status_code=500,
                detail="Failed to create or send OTP. Please try again."
            )
        
        return OTPResponse(
            success=True,
            message=f"OTP sent successfully to your {data.method}",
            otp=otp,  # Include for testing - remove in production
            expires_in_minutes=otp_service.otp_expiry_minutes
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error sending OTP: {str(e)}"
        )

@router.post("/verify", response_model=OTPResponse)
async def verify_otp(data: VerifyOTPRequest, request: Request):
    """
    Verify OTP entered by user
    
    - **contact**: Email address or phone number
    - **otp**: 6-digit OTP code
    - **method**: 'email' or 'phone'
    
    Returns success status if OTP is valid
    """
    try:
        # Verify OTP
        is_valid = otp_service.verify_otp(
            contact=data.contact,
            otp=data.otp,
            method=data.method
        )
        
        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired OTP. Please check and try again."
            )
        
        return OTPResponse(
            success=True,
            message="OTP verified successfully",
            expires_in_minutes=0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error verifying OTP: {str(e)}"
        )

@router.post("/resend", response_model=OTPResponse)
async def resend_otp(data: ResendOTPRequest, request: Request):
    """
    Resend OTP to user
    
    - **contact**: Email address or phone number
    - **method**: 'email' or 'phone'
    - **user_id**: Optional user ID
    
    Returns success status and new OTP (for testing)
    """
    try:
        # Resend OTP
        otp = otp_service.resend_otp(
            contact=data.contact,
            method=data.method,
            user_id=data.user_id
        )
        
        if not otp:
            raise HTTPException(
                status_code=500,
                detail="Failed to resend OTP. Please try again."
            )
        
        return OTPResponse(
            success=True,
            message=f"OTP resent successfully to your {data.method}",
            otp=otp,  # Include for testing - remove in production
            expires_in_minutes=otp_service.otp_expiry_minutes
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error resending OTP: {str(e)}"
        )
