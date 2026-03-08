"""
Wig Marketplace Routes for CancerCare AI
Backend for listing, browsing, and requesting wigs for cancer patients
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from secure_database import SecureDatabase

router = APIRouter(prefix="/api/wigs", tags=["Wig Marketplace"])

db = SecureDatabase()

# --- Seed listings ---
SEED_WIGS = [
    {
        "id": 1, "name": "Natural Wave Bob", "type": "Human Hair", "color": "Dark Brown",
        "length": "Short", "price": 0, "free": True, "condition": "New",
        "description": "Beautiful natural wave bob wig, donated for patients undergoing chemotherapy.",
        "image": "💇‍♀️", "available": True,
    },
    {
        "id": 2, "name": "Long Straight Classic", "type": "Synthetic", "color": "Black",
        "length": "Long", "price": 0, "free": True, "condition": "New",
        "description": "Comfortable long straight wig, lightweight and breathable for everyday wear.",
        "image": "💇", "available": True,
    },
    {
        "id": 3, "name": "Curly Confidence", "type": "Human Hair", "color": "Auburn",
        "length": "Medium", "price": 25, "free": False, "condition": "New",
        "description": "Gorgeous curly wig that adds volume and confidence. Subsidized pricing for patients.",
        "image": "👩‍🦱", "available": True,
    },
    {
        "id": 4, "name": "Pixie Power", "type": "Synthetic", "color": "Blonde",
        "length": "Short", "price": 0, "free": True, "condition": "Gently Used",
        "description": "Chic pixie cut wig, professionally cleaned and ready to wear.",
        "image": "✨", "available": True,
    },
    {
        "id": 5, "name": "Silver Grace", "type": "Synthetic", "color": "Silver/Grey",
        "length": "Medium", "price": 15, "free": False, "condition": "New",
        "description": "Elegant silver wig for a sophisticated, natural look.",
        "image": "🤍", "available": True,
    },
    {
        "id": 6, "name": "Headscarf Collection", "type": "Headwear", "color": "Assorted",
        "length": "N/A", "price": 0, "free": True, "condition": "New",
        "description": "Set of 5 beautiful headscarves in assorted colors and patterns.",
        "image": "🧕", "available": True,
    },
]


class WigRequestModel(BaseModel):
    wig_id: int
    patient_name: str
    reason: Optional[str] = None
    shipping_address: Optional[str] = None


# --- Endpoints ---

@router.get("/listings")
async def list_wigs(
    type: Optional[str] = None,
    color: Optional[str] = None,
    free_only: bool = False,
):
    """Browse available wigs with optional filters."""
    _ensure_wig_tables()

    # Start with seed data + any user-added listings
    result = list(SEED_WIGS)
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wig_listings ORDER BY created_at DESC")
            db_wigs = cursor.fetchall()
            for row in db_wigs:
                result.append({
                    "id": row[0] + 1000,  # offset to avoid seed ID collision
                    "name": row[2], "type": row[3], "color": row[4],
                    "length": row[5], "price": row[6], "free": row[6] == 0,
                    "condition": row[7], "description": row[8],
                    "image": "🎁", "available": bool(row[9]),
                })
    except Exception:
        pass  # Seed data still works if DB fails

    if type:
        result = [w for w in result if type.lower() in w["type"].lower()]
    if color:
        result = [w for w in result if color.lower() in w["color"].lower()]
    if free_only:
        result = [w for w in result if w["free"]]

    return {"success": True, "wigs": result, "total": len(result)}


@router.get("/listings/{wig_id}")
async def get_wig(wig_id: int):
    """Get a specific wig listing."""
    wig = next((w for w in SEED_WIGS if w["id"] == wig_id), None)
    if not wig:
        raise HTTPException(status_code=404, detail="Wig not found")
    return {"success": True, "wig": wig}


@router.post("/request")
async def request_wig(
    data: WigRequestModel,
    authorization: Optional[str] = Header(None),
):
    """Request a wig as a patient."""
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    _ensure_wig_tables()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO wig_requests 
                (user_id, wig_id, patient_name, reason, shipping_address, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, data.wig_id, data.patient_name, data.reason,
                data.shipping_address, "pending", datetime.now().isoformat()
            ))
            conn.commit()

        return {
            "success": True,
            "message": "Your wig request has been submitted! We'll be in touch soon. 💕",
            "request_id": cursor.lastrowid,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit request: {str(e)}")


@router.get("/requests")
async def my_requests(
    authorization: Optional[str] = Header(None),
):
    """Get the user's wig requests."""
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    _ensure_wig_tables()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, wig_id, patient_name, reason, status, created_at
                FROM wig_requests WHERE user_id = ?
                ORDER BY created_at DESC
            """, (user_id,))
            rows = cursor.fetchall()

        requests = [{
            "id": r[0], "wig_id": r[1], "patient_name": r[2],
            "reason": r[3], "status": r[4], "date": r[5],
        } for r in rows]

        return {"success": True, "requests": requests}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch requests: {str(e)}")


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


def _ensure_wig_tables():
    with db._get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wig_listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                donor_id TEXT,
                name TEXT,
                type TEXT,
                color TEXT,
                length TEXT,
                price REAL DEFAULT 0,
                condition TEXT,
                description TEXT,
                available BOOLEAN DEFAULT 1,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wig_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                wig_id INTEGER,
                patient_name TEXT,
                reason TEXT,
                shipping_address TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        conn.commit()
