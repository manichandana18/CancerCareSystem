"""
Analysis History Routes for CancerCare AI
Provides endpoints to save, retrieve, and manage cancer detection history
"""

from fastapi import APIRouter, HTTPException, Header, Request
from pydantic import BaseModel
from typing import Optional, List
import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from secure_database import SecureDatabase

router = APIRouter(prefix="/api/history", tags=["Analysis History"])

db = SecureDatabase()


# --- Request / Response models ---

class SaveAnalysisRequest(BaseModel):
    organ: str
    diagnosis: str
    confidence: float
    confidence_pct: float
    method: str
    model_type: Optional[str] = None
    explainability: Optional[dict] = None
    cell_count: Optional[int] = None
    debug: Optional[dict] = None


class AnalysisRecord(BaseModel):
    id: int
    organ: str
    diagnosis: str
    confidence: float
    confidence_pct: float
    method: str
    model_type: Optional[str] = None
    timestamp: str
    doctor_verified: bool = False


# --- Helpers ---

def _extract_user_id(authorization: Optional[str]) -> Optional[str]:
    """Extract user_id from session token, returns None for anonymous."""
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

@router.post("/save")
async def save_analysis(
    data: SaveAnalysisRequest,
    request: Request,
    authorization: Optional[str] = Header(None),
):
    """Save a completed analysis to persistent history."""
    user_id = _extract_user_id(authorization)

    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required to save history")

    notes = json.dumps({
        "method": data.method,
        "model_type": data.model_type,
        "confidence_pct": data.confidence_pct,
        "explainability": data.explainability,
        "cell_count": data.cell_count,
        "debug": data.debug,
    })

    success = db.save_cancer_detection(
        patient_id=user_id,
        organ=data.organ,
        diagnosis=data.diagnosis,
        confidence=data.confidence,
        notes=notes,
    )

    if not success:
        raise HTTPException(status_code=500, detail="Failed to save analysis")

    return {"success": True, "message": "Analysis saved to history"}


@router.get("/list")
async def list_history(
    authorization: Optional[str] = Header(None),
    limit: int = 50,
    offset: int = 0,
):
    """Retrieve analysis history for the authenticated user."""
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, organ_detected, diagnosis, confidence_score,
                       ai_model_version, detection_date, doctor_verified, notes_encrypted
                FROM cancer_detections
                WHERE patient_id = ?
                ORDER BY detection_date DESC
                LIMIT ? OFFSET ?
            """, (user_id, limit, offset))

            rows = cursor.fetchall()

            # Get total count
            cursor.execute(
                "SELECT COUNT(*) FROM cancer_detections WHERE patient_id = ?",
                (user_id,),
            )
            total = cursor.fetchone()[0]

        results = []
        for row in rows:
            record = {
                "id": row[0],
                "organ": row[1] or "unknown",
                "diagnosis": row[2] or "unknown",
                "confidence": row[3] or 0.0,
                "confidence_pct": round((row[3] or 0.0) * 100, 1),
                "method": "",
                "model_type": row[4] or "",
                "timestamp": row[5] or "",
                "doctor_verified": bool(row[6]),
            }

            # Extract extra info from encrypted notes
            if row[7]:
                try:
                    notes_decrypted = db._decrypt_data(row[7])
                    notes_data = json.loads(notes_decrypted)
                    record["method"] = notes_data.get("method", "")
                    record["model_type"] = notes_data.get("model_type", record["model_type"])
                    record["confidence_pct"] = notes_data.get("confidence_pct", record["confidence_pct"])
                except Exception:
                    pass

            results.append(record)

        return {
            "success": True,
            "history": results,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")


@router.get("/stats")
async def get_stats(
    authorization: Optional[str] = Header(None),
):
    """Get analysis statistics for the dashboard."""
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()

            # Total scans
            cursor.execute(
                "SELECT COUNT(*) FROM cancer_detections WHERE patient_id = ?",
                (user_id,),
            )
            total = cursor.fetchone()[0]

            # By organ
            cursor.execute("""
                SELECT organ_detected, COUNT(*) 
                FROM cancer_detections 
                WHERE patient_id = ? 
                GROUP BY organ_detected
            """, (user_id,))
            organ_counts = {r[0] or "unknown": r[1] for r in cursor.fetchall()}

            # Cancer vs normal
            cursor.execute("""
                SELECT diagnosis, COUNT(*)
                FROM cancer_detections
                WHERE patient_id = ?
                GROUP BY diagnosis
            """, (user_id,))
            diagnosis_counts = {r[0] or "unknown": r[1] for r in cursor.fetchall()}

            cancer_count = sum(
                v for k, v in diagnosis_counts.items()
                if any(w in k.lower() for w in ["cancer", "malignant", "tumor", "suspicious"])
            )
            normal_count = sum(
                v for k, v in diagnosis_counts.items()
                if any(w in k.lower() for w in ["normal", "benign", "healthy"])
            )

        return {
            "success": True,
            "stats": {
                "total": total,
                "bone": organ_counts.get("bone", organ_counts.get("Bone", 0)),
                "lung": organ_counts.get("lung", organ_counts.get("Lung", 0)),
                "blood": organ_counts.get("blood", organ_counts.get("Blood", 0)),
                "brain": organ_counts.get("brain", organ_counts.get("Brain", 0)),
                "skin": organ_counts.get("skin", organ_counts.get("Skin", 0)),
                "breast": organ_counts.get("breast", organ_counts.get("Breast", 0)),
                "cancer": cancer_count,
                "normal": normal_count,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")


@router.delete("/{record_id}")
async def delete_record(
    record_id: int,
    authorization: Optional[str] = Header(None),
):
    """Delete a specific analysis record."""
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM cancer_detections WHERE id = ? AND patient_id = ?",
                (record_id, user_id),
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Record not found")

        return {"success": True, "message": "Record deleted"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete record: {str(e)}")
