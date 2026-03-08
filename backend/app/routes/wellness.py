"""
Wellness Routes for CancerCare AI
Provides endpoints for wellness exercises, breathing, yoga sessions, and progress tracking
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List
import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from secure_database import SecureDatabase

router = APIRouter(prefix="/api/wellness", tags=["Wellness"])

db = SecureDatabase()

# --- Seed data (served from backend, not hardcoded in frontend) ---

EXERCISES = [
    {
        "id": 1,
        "title": "Deep Breathing",
        "type": "breathing",
        "duration": 120,
        "difficulty": "Beginner",
        "description": "Controlled deep breathing to reduce anxiety and promote relaxation. Focus on slow, steady breaths.",
        "imageUrl": "https://picsum.photos/seed/breathing/800/600",
        "steps": [
            "Find a comfortable seated position",
            "Breathe In (4s)",
            "Hold Breath (4s)",
            "Breathe Out (4s)",
            "Repeat cycle"
        ],
        "benefits": ["Reduces stress", "Lowers blood pressure", "Improves focus"]
    },
    {
        "id": 2,
        "title": "Gentle Yoga Flow",
        "type": "yoga",
        "duration": 900,
        "difficulty": "Beginner",
        "description": "A gentle yoga sequence designed for cancer patients. Low-impact poses to improve flexibility and mood.",
        "imageUrl": "https://picsum.photos/seed/yoga1/800/600",
        "steps": [
            "Start in Mountain Pose (Tadasana)",
            "Move to Cat-Cow stretches",
            "Transition to Warrior I with gentle hold",
            "Tree Pose for balance",
            "Seated forward fold",
            "End in Savasana for relaxation"
        ],
        "benefits": ["Improves flexibility", "Reduces fatigue", "Enhances mood"]
    },
    {
        "id": 3,
        "title": "Body Scan Meditation",
        "type": "meditation",
        "duration": 600,
        "difficulty": "Beginner",
        "description": "A guided body scan meditation to release tension and promote healing awareness throughout the body.",
        "imageUrl": "https://picsum.photos/seed/meditation/800/600",
        "steps": [
            "Lie down in a comfortable position",
            "Begin by focusing on your feet",
            "Slowly move attention up through each body part",
            "Notice any areas of tension without judgment",
            "Send healing breath to those areas",
            "Complete the scan at the crown of your head"
        ],
        "benefits": ["Pain management", "Better sleep", "Body awareness"]
    },
    {
        "id": 4,
        "title": "Progressive Muscle Relaxation",
        "type": "relaxation",
        "duration": 480,
        "difficulty": "Beginner",
        "description": "Systematically tense and release muscle groups to reduce physical stress and promote relaxation.",
        "imageUrl": "https://picsum.photos/seed/relax/800/600",
        "steps": [
            "Start by tensing the muscles in your toes for 5 seconds",
            "Release and notice the difference",
            "Move up to calves, thighs, abdomen",
            "Tense fists, arms, shoulders",
            "Scrunch face muscles then release",
            "Feel the wave of relaxation"
        ],
        "benefits": ["Muscle tension relief", "Stress reduction", "Sleep improvement"]
    },
    {
        "id": 5,
        "title": "Gratitude Journaling",
        "type": "mindfulness",
        "duration": 600,
        "difficulty": "Beginner",
        "description": "Write down things you are grateful for to shift focus toward positivity and emotional resilience.",
        "imageUrl": "https://picsum.photos/seed/journal/800/600",
        "steps": [
            "Find a quiet space with paper or device",
            "Write 3 things you are grateful for today",
            "For each, explain why it matters to you",
            "Reflect on a challenge you overcame recently",
            "Write a kind message to yourself",
            "Read your entries aloud"
        ],
        "benefits": ["Emotional resilience", "Positive outlook", "Mental clarity"]
    },
    {
        "id": 6,
        "title": "Chair Yoga for Recovery",
        "type": "yoga",
        "duration": 720,
        "difficulty": "Beginner",
        "description": "Accessible yoga poses done while seated in a chair. Perfect for patients with limited mobility.",
        "imageUrl": "https://picsum.photos/seed/chair/800/600",
        "steps": [
            "Sit tall in a sturdy chair",
            "Neck rolls: 5 circles each direction",
            "Seated cat-cow: arch and round spine",
            "Seated twist: gentle rotation each side",
            "Ankle circles and toe lifts",
            "Seated forward fold with breathing"
        ],
        "benefits": ["Accessible for all", "Joint mobility", "Gentle strengthening"]
    },
    {
        "id": 7,
        "title": "Hold & Breathe Cycle",
        "type": "breathing",
        "duration": 120,
        "difficulty": "Beginner",
        "description": "A structured breathing cycle involving holds to improve lung capacity and focus. Perfect for minimal exertion.",
        "imageUrl": "https://picsum.photos/seed/breath/800/600",
        "steps": [
            "Prepare your posture",
            "Breathe In (4s)",
            "Hold Breath (4s)",
            "Breathe Out (4s)",
            "Repeat cycle"
        ],
        "benefits": ["Improved lung capacity", "Mental clarity", "Nervous system calming"]
    },
    {
        "id": 8,
        "title": "Bedside Stretch & Relax",
        "type": "yoga",
        "duration": 480,
        "difficulty": "Beginner",
        "description": "Simple stretches you can do while lying down or sitting on the edge of the bed. Very low exertion.",
        "imageUrl": "https://picsum.photos/seed/bedside/800/600",
        "steps": [
            "Lie on your back, legs extended",
            "Bring one knee to your chest, holding it gently",
            "Rotate your ankle slowly in both directions",
            "Switch legs and repeat",
            "Finish by stretching arms overhead"
        ],
        "benefits": ["Improves circulation", "Releases muscle tension", "Accessible from bed"]
    },
]


# --- Endpoints ---

@router.get("/exercises")
async def list_exercises(type: Optional[str] = None, difficulty: Optional[str] = None):
    """List all available wellness exercises, optionally filtered."""
    result = EXERCISES
    if type:
        result = [e for e in result if e["type"] == type]
    if difficulty:
        result = [e for e in result if e["difficulty"].lower() == difficulty.lower()]
    return {"success": True, "exercises": result, "total": len(result)}


@router.get("/exercises/{exercise_id}")
async def get_exercise(exercise_id: int):
    """Get a specific exercise by ID."""
    exercise = next((e for e in EXERCISES if e["id"] == exercise_id), None)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return {"success": True, "exercise": exercise}


class SessionCompleteRequest(BaseModel):
    exercise_id: int
    duration_completed: int  # seconds
    notes: Optional[str] = None


@router.post("/sessions/complete")
async def complete_session(
    data: SessionCompleteRequest,
    authorization: Optional[str] = Header(None),
):
    """Record a completed wellness session for the user."""
    # Extract user
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    exercise = next((e for e in EXERCISES if e["id"] == data.exercise_id), None)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    try:
        _ensure_wellness_table()
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO wellness_sessions 
                (user_id, exercise_id, exercise_title, exercise_type, duration_completed, notes, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, data.exercise_id, exercise["title"], exercise["type"],
                data.duration_completed, data.notes, datetime.now().isoformat()
            ))
            conn.commit()

        return {"success": True, "message": "Session recorded! Great work! 🌟"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save session: {str(e)}")


@router.get("/sessions/history")
async def session_history(
    authorization: Optional[str] = Header(None),
    limit: int = 20,
):
    """Get wellness session history for the user."""
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        _ensure_wellness_table()
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, exercise_id, exercise_title, exercise_type, 
                       duration_completed, notes, completed_at
                FROM wellness_sessions
                WHERE user_id = ?
                ORDER BY completed_at DESC
                LIMIT ?
            """, (user_id, limit))
            rows = cursor.fetchall()

        sessions = [{
            "id": r[0], "exercise_id": r[1], "title": r[2],
            "type": r[3], "duration": r[4], "notes": r[5], "completed_at": r[6],
        } for r in rows]

        return {"success": True, "sessions": sessions, "total": len(sessions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sessions: {str(e)}")


@router.get("/sessions/stats")
async def session_stats(
    authorization: Optional[str] = Header(None),
):
    """Get wellness stats: total sessions, total minutes, streak."""
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        _ensure_wellness_table()
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*), COALESCE(SUM(duration_completed), 0)
                FROM wellness_sessions WHERE user_id = ?
            """, (user_id,))
            row = cursor.fetchone()

        return {
            "success": True,
            "stats": {
                "total_sessions": row[0],
                "total_minutes": round(row[1] / 60),
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


def _ensure_wellness_table():
    """Create wellness_sessions table if it doesn't exist."""
    with db._get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wellness_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                exercise_id INTEGER NOT NULL,
                exercise_title TEXT,
                exercise_type TEXT,
                duration_completed INTEGER DEFAULT 0,
                notes TEXT,
                completed_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        conn.commit()
