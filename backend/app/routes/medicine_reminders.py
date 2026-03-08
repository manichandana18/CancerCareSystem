"""
Medicine Reminders Routes for CancerCare AI
Provides endpoints for managing medicine reminders with photo upload and scheduling.
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from pathlib import Path
import json
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from secure_database import SecureDatabase

router = APIRouter(prefix="/api/medicines", tags=["Medicine Reminders"])

db = SecureDatabase()


# --- Pydantic Models ---

class MedicineCreate(BaseModel):
    name: str  # Can be a primary name or a comma-separated list
    dosage: str
    category: Optional[str] = "medicine"  # medicine, exercise, vitals, water, other
    reminder_time: str  # HH:MM format
    days: List[str] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    photo_base64: Optional[str] = None
    notes: Optional[str] = None
    caretaker_name: Optional[str] = None  # name of the person whose voice to mimic
    medications: Optional[List[dict]] = None  # [{name, dosage}, ...]


class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    category: Optional[str] = None
    reminder_time: Optional[str] = None
    days: Optional[List[str]] = None
    photo_base64: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None
    caretaker_name: Optional[str] = None
    medications: Optional[List[dict]] = None


# --- Endpoints ---

@router.get("")
async def list_medicines(authorization: Optional[str] = Header(None)):
    """List all medicines for the authenticated user."""
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    _ensure_medicines_table()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, dosage, reminder_time, days, photo_base64,
                       notes, is_active, caretaker_name, created_at, category, medications_json
                FROM medicine_reminders
                WHERE user_id = ?
                ORDER BY reminder_time ASC
            """, (user_id,))
            rows = cursor.fetchall()

        medicines = [{
            "id": r[0], "name": r[1], "dosage": r[2], "reminder_time": r[3],
            "days": json.loads(r[4]) if r[4] else [],
            "photo_base64": r[5], "notes": r[6], "is_active": bool(r[7]),
            "caretaker_name": r[8], "created_at": r[9],
            "category": r[10] if len(r) > 10 else "medicine",
            "medications": json.loads(r[11]) if len(r) > 11 and r[11] else []
        } for r in rows]

        return {"success": True, "medicines": medicines, "total": len(medicines)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch medicines: {str(e)}")


@router.post("")
async def add_medicine(data: MedicineCreate, authorization: Optional[str] = Header(None)):
    """Add a new medicine reminder."""
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    _ensure_medicines_table()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO medicine_reminders
                (user_id, name, dosage, reminder_time, days, photo_base64, notes, is_active, caretaker_name, created_at, category, medications_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?)
            """, (
                user_id, data.name, data.dosage, data.reminder_time,
                json.dumps(data.days), data.photo_base64, data.notes,
                data.caretaker_name, datetime.now().isoformat(),
                data.category, json.dumps(data.medications) if data.medications else None
            ))
            conn.commit()
            medicine_id = cursor.lastrowid

        return {"success": True, "message": "Medicine reminder added! 💊", "id": medicine_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add medicine: {str(e)}")


@router.put("/{medicine_id}")
async def update_medicine(
    medicine_id: int,
    data: MedicineUpdate,
    authorization: Optional[str] = Header(None),
):
    """Update an existing medicine reminder."""
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    _ensure_medicines_table()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            # Check ownership
            cursor.execute("SELECT id FROM medicine_reminders WHERE id = ? AND user_id = ?", (medicine_id, user_id))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Medicine not found")

            # Build dynamic update
            updates = []
            values = []
            for field in ["name", "dosage", "reminder_time", "photo_base64", "notes", "caretaker_name", "category"]:
                val = getattr(data, field, None)
                if val is not None:
                    updates.append(f"{field} = ?")
                    values.append(val)
            if data.days is not None:
                updates.append("days = ?")
                values.append(json.dumps(data.days))
            if data.medications is not None:
                updates.append("medications_json = ?")
                values.append(json.dumps(data.medications))
            if data.is_active is not None:
                updates.append("is_active = ?")
                values.append(1 if data.is_active else 0)

            if updates:
                values.append(medicine_id)
                values.append(user_id)
                cursor.execute(
                    f"UPDATE medicine_reminders SET {', '.join(updates)} WHERE id = ? AND user_id = ?",
                    values
                )
                conn.commit()

        return {"success": True, "message": "Medicine updated! ✅"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update medicine: {str(e)}")


@router.delete("/{medicine_id}")
async def delete_medicine(medicine_id: int, authorization: Optional[str] = Header(None)):
    """Delete a medicine reminder."""
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    _ensure_medicines_table()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM medicine_reminders WHERE id = ? AND user_id = ?", (medicine_id, user_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Medicine not found")

        return {"success": True, "message": "Medicine deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete medicine: {str(e)}")


@router.get("/stats")
async def platform_stats(authorization: Optional[str] = Header(None)):
    """Get platform-wide user count and user's medicine stats."""
    user_id = _extract_user_id(authorization)

    _ensure_medicines_table()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()

            # Total registered users on platform
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]

            user_medicine_count = 0
            active_reminders = 0
            if user_id:
                cursor.execute("SELECT COUNT(*) FROM medicine_reminders WHERE user_id = ?", (user_id,))
                user_medicine_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM medicine_reminders WHERE user_id = ? AND is_active = 1", (user_id,))
                active_reminders = cursor.fetchone()[0]

        return {
            "success": True,
            "stats": {
                "total_platform_users": total_users,
                "user_medicine_count": user_medicine_count,
                "active_reminders": active_reminders,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")


# --- Helpers ---

def _extract_user_id(authorization: Optional[str]) -> Optional[str]:
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


def _ensure_medicines_table():
    """Create medicine_reminders table if it doesn't exist."""
    with db._get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS medicine_reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                dosage TEXT,
                reminder_time TEXT NOT NULL,
                days TEXT DEFAULT '["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]',
                photo_base64 TEXT,
                notes TEXT,
                is_active INTEGER DEFAULT 1,
                caretaker_name TEXT,
                created_at TEXT,
                category TEXT DEFAULT 'medicine',
                medications_json TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Migrations: check for missing columns if table exists
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(medicine_reminders)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'category' not in columns:
            cursor.execute("ALTER TABLE medicine_reminders ADD COLUMN category TEXT DEFAULT 'medicine'")
        if 'medications_json' not in columns:
            cursor.execute("ALTER TABLE medicine_reminders ADD COLUMN medications_json TEXT")
            
        conn.commit()
