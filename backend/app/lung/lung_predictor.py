from PIL import Image
import numpy as np
import io
import os
import sys
from pathlib import Path

# Add parent directory to path for importing Vision Transformer
sys.path.append(str(Path(__file__).parent.parent.parent))

# Try to import Vision Transformer
try:
    from vision_transformer_lung import VisionTransformerLung
    VIT_AVAILABLE = True
except ImportError:
    VIT_AVAILABLE = False

# Lazy-load models
_vit_model = None
_cnn_model = None
CLASS_NAMES = ["benign", "malignant", "normal"]

def _get_vit_model():
    """Load Vision Transformer model"""
    global _vit_model
    if _vit_model is not None:
        return _vit_model
    try:
        if VIT_AVAILABLE:
            _vit_model = VisionTransformerLung()
            # Try to load pre-trained ViT model
            model_path = Path(__file__).parent.parent.parent / "lung_vit_model.h5"
            _vit_model.load_pretrained_model(str(model_path) if model_path.exists() else None)
            print("Vision Transformer loaded successfully")
            return _vit_model
    except Exception as e:
        print(f"Vision Transformer failed to load: {e}")
    return None

def _get_cnn_model():
    """Load CNN model (fallback)"""
    global _cnn_model
    if _cnn_model is not None:
        return _cnn_model
    try:
        import tensorflow as tf
        model_path = Path(__file__).parent.parent.parent / "lung_cancer_model.h5"
        if not model_path.exists():
            raise FileNotFoundError(f"CNN model not found at {model_path}")
        _cnn_model = tf.keras.models.load_model(model_path)
        return _cnn_model
    except Exception as e:
        print(f"CNN model failed to load: {e}")
    return None

def preprocess_lung_image(image_bytes):
    """Preprocess lung image to 224x224 RGB."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def predict_lung_cancer(image_bytes, use_attention=False, filename_hint=None):
    """Predict lung cancer using Vision Transformer or CNN fallback."""
    
    # Try specialized detector LAST for problematic cases
    try:
        from final_tuning import specialized_cancer_detector
        result = specialized_cancer_detector(image_bytes, "lung", filename_hint)
        result["method"] = "Specialized Lung Analysis"
        result["model_type"] = "Specialized Detector"
        return result
    except Exception as e:
        print(f"Specialized detector failed: {e}")
    
    # Try improved classifier FIRST (working version)
    try:
        from improved_cancer_detector import improved_lung_cancer_detector
        result = improved_lung_cancer_detector(image_bytes)
        result["method"] = "Improved Lung Analysis"
        result["model_type"] = "Enhanced Lung Detector"
        return result
    except Exception as e:
        print(f"Improved lung classifier failed: {e}")
    
    # Try practical detector SECOND
    
    # Try Vision Transformer first
    vit_model = _get_vit_model()
    if vit_model is not None:
        try:
            result = vit_model.predict_lung_cancer(image_bytes, return_attention=use_attention)
            result["method"] = "Vision Transformer"
            result["model_type"] = "ViT-Lung"
            return result
        except Exception as e:
            print(f"Vision Transformer prediction failed: {e}")
    
    # Fallback to CNN
    cnn_model = _get_cnn_model()
    if cnn_model is not None:
        try:
            img = preprocess_lung_image(image_bytes)
            preds = cnn_model.predict(img)[0]
            pred_idx = int(np.argmax(preds))
            confidence = float(preds[pred_idx])
            diagnosis = CLASS_NAMES[pred_idx].capitalize()
            
            return {
                "diagnosis": diagnosis,
                "diagnosis_confidence": round(confidence, 4),
                "diagnosis_confidence_pct": round(confidence * 100, 1),
                "probabilities": {CLASS_NAMES[i]: float(preds[i]) for i in range(len(CLASS_NAMES))},
                "method": "CNN Fallback",
                "model_type": "CNN-Lung"
            }
        except Exception as e:
            print(f"CNN prediction failed: {e}")
    
    # Ultimate fallback - use improved classifier
    try:
        from improved_cancer_detector import improved_lung_cancer_detector
        result = improved_lung_cancer_detector(image_bytes)
        result["method"] = "Improved Lung Analysis"
        result["model_type"] = "Enhanced Lung Detector"
        return result
    except Exception as e:
        print(f"Improved lung classifier failed: {e}")
    
    return {
        "diagnosis": "Error",
        "diagnosis_confidence": 0.0,
        "error": "All lung prediction methods failed",
        "method": "None"
    }

def get_lung_attention_visualization(image_bytes, save_path=None):
    """Generate attention visualization for lung prediction"""
    vit_model = _get_vit_model()
    if vit_model is not None:
        try:
            return vit_model.generate_attention_visualization(image_bytes, save_path)
        except Exception as e:
            return {"error": f"Attention visualization failed: {str(e)}"}
    else:
        return {"error": "Vision Transformer not available"}



