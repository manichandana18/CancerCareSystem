from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import traceback
import os

from app.services.auto_predict import auto_predict

router = APIRouter()

@router.post("/auto-predict")
async def predict_auto(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        filename_hint = file.filename
        result = auto_predict(image_bytes, filename_hint=filename_hint)
        return result

    except Exception as e:
        traceback.print_exc()
        detail = str(e) if os.environ.get("DEBUG") else "Auto-prediction failed"
        return JSONResponse(
            status_code=500,
            content={"error": detail}
        )
