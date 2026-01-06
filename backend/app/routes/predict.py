from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io

from app.services.predictor import predict_bone_cancer

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        result = predict_bone_cancer(image)
        return result

    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid image file"}
        )
