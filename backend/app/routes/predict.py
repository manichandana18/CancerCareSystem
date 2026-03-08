from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import traceback
import os

from app.services.predictor import predict_bone_cancer

router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        return predict_bone_cancer(image_bytes)
    except Exception as e:
        traceback.print_exc()
        detail = str(e) if os.environ.get("DEBUG") else "Prediction failed"
        return JSONResponse(
            status_code=500,
            content={"error": detail}
        )
