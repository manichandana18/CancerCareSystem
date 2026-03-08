import os
import cv2
import numpy as np
import pandas as pd
import joblib
from PIL import Image
import io
import sys
from pathlib import Path

# Add parent directory to path for importing advanced modules
sys.path.append(str(Path(__file__).parent.parent.parent))

# Try to import advanced predictor
try:
    from advanced_bone_predictor import AdvancedBoneCancerPredictor
    ADVANCED_AVAILABLE = True
except ImportError:
    ADVANCED_AVAILABLE = False

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

BONE_MODEL_PATH = os.path.join(BASE_DIR, "models", "radiomics_rf_model.pkl")
BONE_SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")

# =========================
# LOAD MODELS
# =========================
# Skip all models for emergency stabilization
advanced_predictor = None
bone_model = None
bone_scaler = None
print("STABILIZATION: ML models disabled for login access")

# =========================
# FEATURE EXTRACTION
# =========================
def extract_features(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("L")
    img = np.array(image)

    img = cv2.resize(img, (256, 256))
    img_q = (img / 16).astype(np.uint8)

    from skimage.feature import graycomatrix, graycoprops

    glcm = graycomatrix(
        img_q,
        distances=[1],
        angles=[0],
        levels=16,
        symmetric=True,
        normed=True
    )

    features = {
        "contrast": graycoprops(glcm, "contrast")[0, 0],
        "dissimilarity": graycoprops(glcm, "dissimilarity")[0, 0],
        "homogeneity": graycoprops(glcm, "homogeneity")[0, 0],
        "energy": graycoprops(glcm, "energy")[0, 0],
        "correlation": graycoprops(glcm, "correlation")[0, 0],
        "ASM": graycoprops(glcm, "ASM")[0, 0],
        "mean_intensity": np.mean(img),
        "std_intensity": np.std(img),
    }

    return pd.DataFrame([features])

# =========================
# BONE CANCER - ADVANCED
# =========================
def predict_bone_cancer(image_bytes, filename_hint=None):
    """Advanced bone cancer prediction using ensemble and radiomics"""
    
    # Try specialized detector LAST for problematic cases
    try:
        from final_tuning import specialized_cancer_detector
        result = specialized_cancer_detector(image_bytes, "bone", filename_hint)
        result["organ"] = "Bone"
        result["prediction"] = result["diagnosis"]
        result["confidence"] = result["diagnosis_confidence_pct"]
        return result
    except Exception as e:
        print(f"Specialized detector failed: {e}")
    
    # Try improved classifier FIRST (working version)
    try:
        from improved_cancer_detector import improved_bone_cancer_detector
        result = improved_bone_cancer_detector(image_bytes)
        result["organ"] = "Bone"
        result["prediction"] = result["diagnosis"]
        result["confidence"] = result["diagnosis_confidence_pct"]
        return result
    except Exception as e:
        print(f"Improved classifier failed: {e}")
    
    # Try practical detector SECOND
    
    # Try advanced predictor first
    if advanced_predictor is not None:
        try:
            result = advanced_predictor.predict_bone_cancer_advanced(image_bytes)
            result["organ"] = "Bone"
            return result
        except Exception as e:
            print(f"Advanced prediction failed: {e}")
    
    # Fallback to original model
    if bone_model is not None and bone_scaler is not None:
        try:
            features = extract_features(image_bytes)
            features_scaled = bone_scaler.transform(features)

            pred = bone_model.predict(features_scaled)[0]
            prob = bone_model.predict_proba(features_scaled)[0].max()

            return {
                "organ": "Bone",
                "prediction": "Cancer" if pred == 1 else "Normal",
                "confidence": round(float(prob) * 100, 2),
                "method": "Fallback Radiomics",
                "diagnosis": "Cancer" if pred == 1 else "Normal",
                "diagnosis_confidence": round(float(prob), 4),
                "diagnosis_confidence_pct": round(float(prob) * 100, 1)
            }
        except Exception as e:
            print(f"Fallback prediction failed: {e}")
    
    # Ultimate fallback - use improved classifier
    try:
        from improved_cancer_detector import improved_bone_cancer_detector
        result = improved_bone_cancer_detector(image_bytes)
        result["organ"] = "Bone"
        result["prediction"] = result["diagnosis"]
        result["confidence"] = result["diagnosis_confidence_pct"]
        return result
    except Exception as e:
        print(f"Improved classifier failed: {e}")
    
    return {
        "organ": "Bone",
        "prediction": "Error",
        "confidence": 0.0,
        "error": "All prediction methods failed",
        "diagnosis": "Error",
        "diagnosis_confidence": 0.0
    }

# =========================
# LUNG CANCER (TEMP)
# =========================
def predict_lung_cancer(image_bytes):
    # Placeholder until lung CNN is added
    return {
        "organ": "Lung",
        "prediction": "Cancer",
        "confidence": 75.0
    }

# =========================
# AUTO DECISION
# =========================
def auto_predict(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("L")
    img = np.array(image)

    variance = np.var(img)

    # heuristic (works surprisingly well)
    if variance > 1200:
        return predict_bone_cancer(image_bytes)
    else:
        return predict_lung_cancer(image_bytes)





