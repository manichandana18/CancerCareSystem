"""
Skin Cancer Prediction API Routes
"""

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import traceback
import os

from app.skin.skin_predictor import predict_skin_cancer

router = APIRouter()

@router.post("/predict/skin")
async def predict_skin(file: UploadFile = File(...)):
    """Predict skin cancer from uploaded image"""
    try:
        image_bytes = await file.read()
        filename_hint = file.filename
        result = predict_skin_cancer(image_bytes, filename_hint=filename_hint)
        return result

    except Exception as e:
        traceback.print_exc()
        detail = str(e) if os.environ.get("DEBUG") else "Skin cancer prediction failed"
        return JSONResponse(
            status_code=500,
            content={"error": detail}
        )
