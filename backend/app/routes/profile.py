"""
Profile Management Routes for CancerCare AI
Provides endpoints for updating user profile info and changing password.
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from secure_database import SecureDatabase

router = APIRouter(prefix="/api/profile", tags=["Profile"])

db = SecureDatabase()


class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str


# --- Helpers ---

def _get_user_from_token(authorization: Optional[str]) -> Optional[str]:
    """Extract and validate user_id from Bearer token."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.replace("Bearer ", "")
    try:
        session = db.verify_session(token)
        if session and session.get("valid"):
            return session.get("user_id")
    except Exception:
        pass
    return None


# --- Endpoints ---

@router.put("/update")
async def update_profile(
    data: ProfileUpdateRequest,
    authorization: Optional[str] = Header(None),
):
    """Update user profile fields (name, phone, age, gender)."""
    user_id = _get_user_from_token(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()

            # Build dynamic update query based on provided fields
            updates = []
            params = []

            if data.name is not None:
                encrypted_name = db._encrypt_data(data.name)
                updates.append("name_encrypted = ?")
                params.append(encrypted_name)

            if data.phone is not None:
                encrypted_phone = db._encrypt_data(data.phone)
                updates.append("phone_encrypted = ?")
                params.append(encrypted_phone)

            if data.age is not None:
                updates.append("age = ?")
                params.append(data.age)

            if data.gender is not None:
                updates.append("gender = ?")
                params.append(data.gender)

            if not updates:
                return {"success": False, "error": "No fields to update"}

            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(user_id)

            query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
            cursor.execute(query, params)
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")

        # Fetch updated user info to return
        updated_user = _get_user_info(user_id)

        return {
            "success": True,
            "message": "Profile updated successfully! ✅",
            "user": updated_user,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")


@router.put("/change-password")
async def change_password(
    data: PasswordChangeRequest,
    authorization: Optional[str] = Header(None),
):
    """Change user password after verifying current password."""
    user_id = _get_user_from_token(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    if len(data.new_password) < 6:
        raise HTTPException(status_code=400, detail="New password must be at least 6 characters")

    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()

            # Get current password hash
            cursor.execute("SELECT password_hash FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="User not found")

            # Verify current password
            import bcrypt
            current_hash = row[0]
            if not bcrypt.checkpw(data.current_password.encode('utf-8'), current_hash.encode('utf-8')):
                raise HTTPException(status_code=403, detail="Current password is incorrect")

            # Hash new password
            new_hash = bcrypt.hashpw(data.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            cursor.execute(
                "UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
                (new_hash, user_id)
            )
            conn.commit()

        return {"success": True, "message": "Password changed successfully! 🔐"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to change password: {str(e)}")


@router.get("/me")
async def get_profile(
    authorization: Optional[str] = Header(None),
):
    """Get current user's full profile info."""
    user_id = _get_user_from_token(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    user = _get_user_info(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"success": True, "user": user}


def _get_user_info(user_id: str) -> Optional[dict]:
    """Fetch and decrypt user information."""
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, email_encrypted, phone_encrypted, name_encrypted,
                       age, gender, created_at, last_login, security_level
                FROM users WHERE user_id = ?
            """, (user_id,))
            row = cursor.fetchone()

        if not row:
            return None

        return {
            "user_id": row[0],
            "email": db._decrypt_data(row[1]),
            "phone": db._decrypt_data(row[2]) if row[2] else None,
            "name": db._decrypt_data(row[3]),
            "age": row[4],
            "gender": row[5],
            "created_at": row[6],
            "last_login": row[7],
            "security_level": row[8] or "standard",
        }
    except Exception as e:
        print(f"Error fetching user info: {e}")
        return None
