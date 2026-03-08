"""
Blood Cancer Prediction API Routes
"""

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import traceback
import os

from complete_blood_cancer import predict_blood_cancer

router = APIRouter()

@router.post("/predict/blood")
async def predict_blood(file: UploadFile = File(...)):
    """Predict blood cancer from uploaded image"""
    try:
        image_bytes = await file.read()
        filename_hint = file.filename
        result = predict_blood_cancer(image_bytes, filename_hint=filename_hint)
        return result

    except Exception as e:
        traceback.print_exc()
        detail = str(e) if os.environ.get("DEBUG") else "Blood cancer prediction failed"
        return JSONResponse(
            status_code=500,
            content={"error": detail}
        )
