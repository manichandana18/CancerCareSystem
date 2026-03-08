"""
Donation Routes for CancerCare AI
Backend for monetary and wig donations with tracking
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from secure_database import SecureDatabase

router = APIRouter(prefix="/api/donations", tags=["Donations"])

db = SecureDatabase()


class DonationRequest(BaseModel):
    amount: float
    currency: str = "USD"
    donor_name: Optional[str] = None
    message: Optional[str] = None
    anonymous: bool = False
    type: str = "monetary"  # monetary | wig


class WigDonationRequest(BaseModel):
    wig_type: str  # synthetic | human_hair
    color: str
    length: str  # short | medium | long
    condition: str  # new | gently_used
    donor_name: Optional[str] = None
    message: Optional[str] = None


# --- Endpoints ---

@router.post("/monetary")
async def donate_money(
    data: DonationRequest,
    authorization: Optional[str] = Header(None),
):
    """Record a monetary donation."""
    user_id = _extract_user_id(authorization)

    _ensure_donation_tables()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO donations 
                (user_id, type, amount, currency, donor_name, message, anonymous, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, "monetary", data.amount, data.currency,
                data.donor_name if not data.anonymous else "Anonymous",
                data.message, data.anonymous, datetime.now().isoformat()
            ))
            conn.commit()

        return {
            "success": True,
            "message": "Thank you for your generous donation! 💕",
            "donation_id": cursor.lastrowid,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process donation: {str(e)}")


@router.post("/wig")
async def donate_wig(
    data: WigDonationRequest,
    authorization: Optional[str] = Header(None),
):
    """Record a wig donation."""
    user_id = _extract_user_id(authorization)

    _ensure_donation_tables()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO wig_donations 
                (user_id, wig_type, color, length, condition, donor_name, message, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, data.wig_type, data.color, data.length, data.condition,
                data.donor_name, data.message, "pending", datetime.now().isoformat()
            ))
            conn.commit()

        return {
            "success": True,
            "message": "Thank you for donating a wig! It will make someone's day! 🌟",
            "donation_id": cursor.lastrowid,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process wig donation: {str(e)}")


@router.get("/stats")
async def donation_stats():
    """Get public donation stats (total donations, wigs donated, etc.)."""
    _ensure_donation_tables()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM donations")
            money = cursor.fetchone()

            cursor.execute("SELECT COUNT(*) FROM wig_donations")
            wigs = cursor.fetchone()

        return {
            "success": True,
            "stats": {
                "total_monetary_donations": money[0],
                "total_amount_raised": round(money[1], 2),
                "total_wigs_donated": wigs[0],
                "patients_helped": money[0] + wigs[0],
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")


@router.get("/recent")
async def recent_donations(limit: int = 10):
    """Get recent public (non-anonymous) donations."""
    _ensure_donation_tables()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT donor_name, amount, currency, message, created_at 
                FROM donations 
                WHERE anonymous = 0 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()

        donations = [{
            "donor": r[0] or "Kind Soul",
            "amount": r[1],
            "currency": r[2],
            "message": r[3],
            "date": r[4],
        } for r in rows]

        return {"success": True, "donations": donations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch donations: {str(e)}")


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


def _ensure_donation_tables():
    with db._get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                type TEXT DEFAULT 'monetary',
                amount REAL,
                currency TEXT DEFAULT 'USD',
                donor_name TEXT,
                message TEXT,
                anonymous BOOLEAN DEFAULT 0,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wig_donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                wig_type TEXT,
                color TEXT,
                length TEXT,
                condition TEXT,
                donor_name TEXT,
                message TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT
            )
        """)
        conn.commit()
