"""
Cancer Staging Assessment Routes for CancerCare AI
Provides symptom-based cancer staging estimates and actionable recommendations.

DISCLAIMER: This tool provides AI-estimated staging for educational purposes only.
Actual staging requires clinical examination, imaging, biopsy, and pathological review.
Always consult an oncologist for accurate diagnosis and treatment planning.
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from secure_database import SecureDatabase

router = APIRouter(prefix="/api/staging", tags=["Cancer Staging"])

db = SecureDatabase()


# --- Request models ---

class StagingAssessmentRequest(BaseModel):
    cancer_type: str  # bone, lung, blood, brain, skin, breast
    age: Optional[int] = None
    gender: Optional[str] = None
    # Symptom inputs
    tumor_size: Optional[str] = None       # small (<2cm), medium (2-5cm), large (>5cm)
    lymph_nodes: Optional[str] = None      # none, nearby, distant
    metastasis: Optional[str] = None       # no, suspected, confirmed
    pain_level: Optional[int] = None       # 0-10
    weight_loss: Optional[bool] = None
    fatigue_level: Optional[str] = None    # none, mild, moderate, severe
    duration_months: Optional[int] = None  # how long symptoms present
    # Additional symptoms (varies by cancer type)
    breathing_difficulty: Optional[bool] = None   # lung
    coughing_blood: Optional[bool] = None         # lung
    skin_changes: Optional[str] = None            # skin: color_change, irregular_border, growing, bleeding
    lump_detected: Optional[bool] = None          # breast
    bone_pain: Optional[bool] = None              # bone
    night_sweats: Optional[bool] = None           # blood
    swollen_lymph: Optional[bool] = None          # blood
    headaches: Optional[bool] = None              # brain
    vision_changes: Optional[bool] = None         # brain
    seizures: Optional[bool] = None               # brain
    family_history: Optional[bool] = None
    previous_treatment: Optional[str] = None      # none, surgery, chemo, radiation, combination


# --- Staging logic ---

STAGE_INFO = {
    "Stage 0": {
        "description": "Carcinoma in situ — abnormal cells present but not spread to nearby tissue.",
        "severity": "Very Early",
        "color": "#22c55e",
        "survival_note": "Highly treatable with excellent outcomes in most cases.",
    },
    "Stage I": {
        "description": "Cancer is small and localized to one area. No lymph node involvement.",
        "severity": "Early",
        "color": "#84cc16",
        "survival_note": "Very good prognosis. Often curable with surgery or localized treatment.",
    },
    "Stage II": {
        "description": "Cancer is larger but still localized. May have limited lymph node involvement.",
        "severity": "Moderate",
        "color": "#eab308",
        "survival_note": "Good prognosis with appropriate treatment. Early intervention is key.",
    },
    "Stage III": {
        "description": "Cancer has spread to nearby lymph nodes or surrounding tissues. Locally advanced.",
        "severity": "Advanced",
        "color": "#f97316",
        "survival_note": "Treatable but requires aggressive therapy. Multi-modal treatment recommended.",
    },
    "Stage IV": {
        "description": "Cancer has metastasized (spread) to distant organs or parts of the body.",
        "severity": "Metastatic",
        "color": "#ef4444",
        "survival_note": "Focus shifts to managing disease, quality of life, and targeted therapies.",
    },
}


def estimate_stage(data: StagingAssessmentRequest) -> dict:
    """
    Estimate cancer stage based on reported symptoms.
    Uses a weighted scoring system inspired by TNM staging.
    """
    score = 0  # 0-100 scale → maps to stages

    # --- Tumor size (T component) ---
    if data.tumor_size == "small":
        score += 5
    elif data.tumor_size == "medium":
        score += 20
    elif data.tumor_size == "large":
        score += 40

    # --- Lymph node involvement (N component) ---
    if data.lymph_nodes == "nearby":
        score += 20
    elif data.lymph_nodes == "distant":
        score += 35

    # --- Metastasis (M component) ---
    if data.metastasis == "suspected":
        score += 25
    elif data.metastasis == "confirmed":
        score += 45

    # --- Symptom severity modifiers ---
    if data.pain_level is not None:
        score += min(data.pain_level, 10)

    if data.weight_loss:
        score += 8

    fatigue_map = {"mild": 3, "moderate": 6, "severe": 10}
    score += fatigue_map.get(data.fatigue_level or "", 0)

    if data.duration_months is not None:
        if data.duration_months > 12:
            score += 10
        elif data.duration_months > 6:
            score += 5

    # --- Cancer-type-specific symptoms ---
    if data.cancer_type == "lung":
        if data.breathing_difficulty:
            score += 8
        if data.coughing_blood:
            score += 12

    elif data.cancer_type == "skin":
        skin_map = {"color_change": 3, "irregular_border": 6, "growing": 10, "bleeding": 15}
        score += skin_map.get(data.skin_changes or "", 0)

    elif data.cancer_type == "breast":
        if data.lump_detected:
            score += 10

    elif data.cancer_type == "bone":
        if data.bone_pain:
            score += 8

    elif data.cancer_type == "blood":
        if data.night_sweats:
            score += 7
        if data.swollen_lymph:
            score += 10

    elif data.cancer_type == "brain":
        if data.headaches:
            score += 5
        if data.vision_changes:
            score += 8
        if data.seizures:
            score += 12

    # Family history
    if data.family_history:
        score += 5

    # Cap score
    score = min(score, 100)

    # Map score to stage
    if score <= 10:
        stage = "Stage 0"
    elif score <= 25:
        stage = "Stage I"
    elif score <= 50:
        stage = "Stage II"
    elif score <= 75:
        stage = "Stage III"
    else:
        stage = "Stage IV"

    return {
        "stage": stage,
        "score": score,
        "info": STAGE_INFO[stage],
    }


def get_recommendations(stage: str, cancer_type: str, data: StagingAssessmentRequest) -> List[dict]:
    """Generate personalized recommendations based on staging."""

    recs = []

    # Universal recommendations
    recs.append({
        "category": "🏥 Medical",
        "priority": "Critical",
        "title": "Consult an Oncologist",
        "description": "This assessment is AI-estimated. Schedule an appointment with a certified oncologist for proper clinical staging.",
    })

    if stage in ("Stage 0", "Stage I"):
        recs.extend([
            {
                "category": "🔬 Screening",
                "priority": "High",
                "title": "Get Comprehensive Imaging",
                "description": "Request a full imaging workup (CT/MRI/PET scan) to confirm the extent of the disease.",
            },
            {
                "category": "💪 Lifestyle",
                "priority": "Medium",
                "title": "Adopt an Anti-Inflammatory Diet",
                "description": "Focus on fruits, vegetables, whole grains, and lean proteins. Reduce processed foods and sugar.",
            },
            {
                "category": "🧘 Wellness",
                "priority": "Medium",
                "title": "Start Gentle Exercise",
                "description": "30 minutes of light walking, yoga, or stretching daily can improve energy and mood.",
            },
        ])

    elif stage in ("Stage II", "Stage III"):
        recs.extend([
            {
                "category": "💊 Treatment",
                "priority": "Critical",
                "title": "Discuss Treatment Options",
                "description": "Based on staging, discuss surgery, chemotherapy, radiation, or combination therapy with your oncology team.",
            },
            {
                "category": "🧬 Testing",
                "priority": "High",
                "title": "Request Genetic & Biomarker Testing",
                "description": "Genetic profiling can identify targeted therapy options specific to your cancer type.",
            },
            {
                "category": "🤝 Support",
                "priority": "High",
                "title": "Join a Support Group",
                "description": "Connecting with others going through similar experiences can significantly improve mental health.",
            },
            {
                "category": "🧘 Wellness",
                "priority": "Medium",
                "title": "Practice Mindfulness & Stress Reduction",
                "description": "Use our app's breathing exercises and yoga sessions to manage treatment-related anxiety.",
            },
        ])

    else:  # Stage IV
        recs.extend([
            {
                "category": "💊 Treatment",
                "priority": "Critical",
                "title": "Explore Advanced Treatment Options",
                "description": "Discuss immunotherapy, targeted therapy, and clinical trials with your care team.",
            },
            {
                "category": "🏠 Palliative Care",
                "priority": "High",
                "title": "Consider Palliative Care",
                "description": "Palliative care focuses on quality of life and symptom management alongside treatment.",
            },
            {
                "category": "📋 Planning",
                "priority": "High",
                "title": "Create a Care Team",
                "description": "Assemble a multi-disciplinary team: oncologist, nutritionist, counselor, and palliative care specialist.",
            },
            {
                "category": "💕 Emotional",
                "priority": "High",
                "title": "Connect with Loved Ones",
                "description": "Open communication with family and friends is vital. Consider professional counseling for emotional support.",
            },
        ])

    # Cancer-type specific recommendations
    type_specific = {
        "lung": {
            "category": "🫁 Lung-Specific",
            "priority": "High",
            "title": "Pulmonary Function Assessment",
            "description": "Get a pulmonary function test to assess breathing capacity and guide treatment decisions.",
        },
        "breast": {
            "category": "🎀 Breast-Specific",
            "priority": "High",
            "title": "Hormone Receptor Testing",
            "description": "Request ER/PR/HER2 testing to determine if hormone therapy or targeted drugs are applicable.",
        },
        "skin": {
            "category": "🧴 Skin-Specific",
            "priority": "High",
            "title": "Dermatological Mapping",
            "description": "Get a full-body skin examination and mole mapping to monitor for additional lesions.",
        },
        "brain": {
            "category": "🧠 Brain-Specific",
            "priority": "High",
            "title": "Neurological Evaluation",
            "description": "Schedule a comprehensive neurological exam and consider MRI with contrast for detailed brain imaging.",
        },
        "blood": {
            "category": "🩸 Blood-Specific",
            "priority": "High",
            "title": "Complete Blood Panel & Bone Marrow Biopsy",
            "description": "A complete blood count and bone marrow biopsy are essential for blood cancer staging.",
        },
        "bone": {
            "category": "🦴 Bone-Specific",
            "priority": "High",
            "title": "Bone Scan & Biopsy",
            "description": "A full-body bone scan and tissue biopsy will confirm diagnosis and extent of involvement.",
        },
    }

    if cancer_type in type_specific:
        recs.append(type_specific[cancer_type])

    return recs


# --- Endpoints ---

@router.post("/assess")
async def assess_staging(
    data: StagingAssessmentRequest,
    authorization: Optional[str] = Header(None),
):
    """
    Perform a cancer staging assessment based on patient-reported symptoms.
    Returns estimated stage, explanation, and personalized recommendations.
    """
    valid_types = ["bone", "lung", "blood", "brain", "skin", "breast"]
    if data.cancer_type.lower() not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid cancer type. Must be one of: {', '.join(valid_types)}"
        )

    staging = estimate_stage(data)
    recommendations = get_recommendations(staging["stage"], data.cancer_type, data)

    # Save assessment if user is authenticated
    user_id = _extract_user_id(authorization)
    if user_id:
        _save_assessment(user_id, data, staging)

    return {
        "success": True,
        "assessment": {
            "cancer_type": data.cancer_type,
            "estimated_stage": staging["stage"],
            "confidence_score": staging["score"],
            "stage_info": staging["info"],
            "recommendations": recommendations,
            "disclaimer": (
                "⚠️ This is an AI-estimated staging based on self-reported symptoms. "
                "It is NOT a medical diagnosis. Please consult an oncologist for "
                "proper clinical staging using imaging, biopsy, and laboratory tests."
            ),
        },
    }


@router.get("/history")
async def staging_history(
    authorization: Optional[str] = Header(None),
):
    """Get past staging assessments for the user."""
    user_id = _extract_user_id(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    _ensure_staging_table()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, cancer_type, estimated_stage, score, created_at
                FROM staging_assessments
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT 20
            """, (user_id,))
            rows = cursor.fetchall()

        results = [{
            "id": r[0], "cancer_type": r[1], "stage": r[2],
            "score": r[3], "date": r[4],
        } for r in rows]

        return {"success": True, "assessments": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


def _ensure_staging_table():
    with db._get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS staging_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                cancer_type TEXT,
                estimated_stage TEXT,
                score INTEGER,
                input_data TEXT,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        conn.commit()


def _save_assessment(user_id: str, data: StagingAssessmentRequest, staging: dict):
    import json
    _ensure_staging_table()
    try:
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO staging_assessments 
                (user_id, cancer_type, estimated_stage, score, input_data, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id, data.cancer_type, staging["stage"], staging["score"],
                json.dumps(data.dict()), datetime.now().isoformat()
            ))
            conn.commit()
    except Exception as e:
        print(f"Warning: failed to save staging assessment: {e}")
