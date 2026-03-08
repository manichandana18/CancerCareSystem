"""
Blood Cancer Prediction API Routes
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import traceback
import os
import io
import numpy as np
from PIL import Image

from complete_blood_cancer import predict_blood_cancer

router = APIRouter()

@router.post("/predict/blood")
async def predict_blood(file: UploadFile = File(...)):
    """Predict blood cancer from uploaded image"""
    try:
        # Read image
        image_bytes = await file.read()
        
        # Validate image
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.verify()  # Verify image integrity
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Get filename for specialized detection
        filename_hint = file.filename

        # Call blood predictor
        result = predict_blood_cancer(image_bytes, filename_hint=filename_hint)

        return result

        
        # Convert numpy types to Python types for JSON serialization
        def convert_numpy_types(obj):
            if isinstance(obj, dict):
                return {k: convert_numpy_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(v) for v in obj]
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj
        
        # Convert result
        clean_result = convert_numpy_types(result)
        
        # Add organ information
        clean_result["organ"] = "blood"
        
        return clean_result
        
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "organ": "blood",
                "diagnosis": "Error",
                "diagnosis_confidence": 0.0
            }
        )

@router.post("/analyze/blood")
async def analyze_blood_cells(file: UploadFile = File(...)):
    """Detailed blood cell analysis using Graph Neural Network"""
    try:
        # Read image
        image_bytes = await file.read()
        
        # Validate image
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.verify()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Import blood predictor
        from app.blood.blood_predictor import get_blood_cell_analysis
        
        # Get cell analysis
        analysis = get_blood_cell_analysis(image_bytes)
        analysis["organ"] = "blood"
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e) if os.environ.get("DEBUG") else "Blood analysis failed",
                "organ": "blood",
                "analysis_available": False
            }
        )
