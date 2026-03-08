"""
Breast Cancer Prediction API Routes
"""

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import traceback
import os

from app.breast.breast_predictor import predict_breast_cancer

router = APIRouter()

@router.post("/predict/breast")
async def predict_breast(file: UploadFile = File(...)):
    """Predict breast cancer from uploaded image"""
    try:
        image_bytes = await file.read()
        filename_hint = file.filename
        result = predict_breast_cancer(image_bytes, filename_hint=filename_hint)
        return result

    except Exception as e:
        traceback.print_exc()
        detail = str(e) if os.environ.get("DEBUG") else "Breast cancer prediction failed"
        return JSONResponse(
            status_code=500,
            content={"error": detail}
        )
