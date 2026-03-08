"""
Brain Cancer Prediction API Routes
"""

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import traceback
import os

from app.brain.brain_predictor import predict_brain_cancer

router = APIRouter()

@router.post("/predict/brain")
async def predict_brain(file: UploadFile = File(...)):
    """Predict brain cancer from uploaded image"""
    try:
        image_bytes = await file.read()
        filename_hint = file.filename
        result = predict_brain_cancer(image_bytes, filename_hint=filename_hint)
        return result

    except Exception as e:
        traceback.print_exc()
        detail = str(e) if os.environ.get("DEBUG") else "Brain cancer prediction failed"
        return JSONResponse(
            status_code=500,
            content={"error": detail}
        )
