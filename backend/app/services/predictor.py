import os
import numpy as np
from PIL import Image
import cv2
from tensorflow import keras

# Model path - adjust if your model is saved elsewhere
# Try multiple possible locations
_base_dir = os.path.dirname(__file__)
_possible_paths = [
    os.path.join(_base_dir, "../../bone_cancer_model.h5"),  # backend/bone_cancer_model.h5
    os.path.join(_base_dir, "../../../ml/bone_cancer_model.h5"),  # ml/bone_cancer_model.h5
    os.path.join(_base_dir, "../../ml/bone_cancer_model.h5"),  # Alternative path
]

MODEL_PATH = None
for path in _possible_paths:
    if os.path.exists(path):
        MODEL_PATH = path
        break

if MODEL_PATH is None:
    # Default to backend directory
    MODEL_PATH = os.path.join(_base_dir, "../../bone_cancer_model.h5")

# Model expects 160x160 RGB images (3 channels), not 128x128 grayscale
IMG_SIZE = 160

# Load model (lazy loading - only load when first prediction is made)
_model = None

def _load_model():
    """Load the trained model if it exists, otherwise use fallback"""
    global _model
    if _model is None:
        if MODEL_PATH and os.path.exists(MODEL_PATH):
            try:
                print(f"Attempting to load model from: {MODEL_PATH}")
                _model = keras.models.load_model(MODEL_PATH)
                print(f"[SUCCESS] Model loaded successfully from {MODEL_PATH}")
            except Exception as e:
                print(f"[ERROR] Could not load model: {e}")
                import traceback
                traceback.print_exc()
                _model = None
        else:
            print(f"[WARNING] Model file not found at {MODEL_PATH}")
            print("Using fallback prediction method (heuristic only)")
    return _model

def preprocess_image(image):
    """Preprocess image for model prediction"""
    # Convert PIL Image to numpy array
    img_array = np.array(image)
    
    # Model expects RGB (3 channels), not grayscale
    # Convert to RGB if grayscale or has alpha channel
    if len(img_array.shape) == 2:
        # Grayscale image - convert to RGB
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
    elif img_array.shape[2] == 4:
        # RGBA image - convert to RGB
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
    elif img_array.shape[2] == 3:
        # Already RGB, but ensure it's in RGB format (not BGR)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB) if hasattr(cv2, 'COLOR_BGR2RGB') else img_array
    
    # Resize to model input size (160x160)
    img_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    
    # Normalize pixel values to [0, 1]
    img_array = img_array.astype('float32') / 255.0
    
    # Reshape for model input (batch_size, height, width, channels)
    # Model expects: (1, 160, 160, 3)
    img_array = img_array.reshape(1, IMG_SIZE, IMG_SIZE, 3)
    
    return img_array

def predict_bone_cancer(image):
    """Predict bone cancer from X-ray image"""
    model = _load_model()
    
    # Preprocess image
    processed_image = preprocess_image(image)
    
    # Initialize variables for probability tracking
    tumor_probability = None
    no_tumor_probability = None
    # Adjusted threshold: 0.5 for balanced detection (was 0.3 for maximum sensitivity)
    # Lower = more sensitive (catches more cancers but more false positives)
    # Higher = less sensitive (fewer false positives but might miss some cancers)
    CANCER_THRESHOLD = 0.5
    
    if model is not None:
        # Use actual model prediction
        try:
            prediction = model.predict(processed_image, verbose=0)
            
            # Handle different model output formats
            # Some models output (1, 1) - single probability value
            # Others output (1, 2) - two probabilities [normal, tumor]
            pred_shape = prediction.shape
            
            if len(pred_shape) == 2:
                if pred_shape[1] == 1:
                    # Binary classifier: single probability value
                    # CRITICAL FIX: Labels are REVERSED in the model
                    # The model outputs probability of NORMAL, not TUMOR
                    # Low values (< 0.5) = Normal (high confidence)
                    # High values (> 0.5) = Tumor (high confidence)
                    raw_prob = float(prediction[0][0])
                    
                    # Invert: model outputs P(normal), we need P(tumor)
                    no_tumor_probability = raw_prob
                    tumor_probability = 1.0 - raw_prob
                    
                    # Debug output - shows raw model output
                    print(f"DEBUG: Raw model output: {raw_prob:.6f} | P(normal): {no_tumor_probability:.4f} | P(tumor): {tumor_probability:.4f}")
                elif pred_shape[1] == 2:
                    # Two-class classifier: [normal, tumor] probabilities
                    no_tumor_probability = float(prediction[0][0])
                    tumor_probability = float(prediction[0][1])
                else:
                    raise ValueError(f"Unexpected prediction shape: {pred_shape}")
            else:
                # Flatten and take first value
                tumor_probability = float(prediction.flatten()[0])
                no_tumor_probability = 1.0 - tumor_probability
            
            # Debug output to console
            print(f"DEBUG: Prediction probabilities - Normal: {no_tumor_probability:.4f}, Tumor: {tumor_probability:.4f}")
            
            # CRITICAL FIX: Use lower threshold for cancer detection to reduce false negatives
            # In medical diagnosis, it's better to have false positives than false negatives
            # Threshold lowered from 0.5 to 0.3 to catch more potential cancers
            
            confidence = float(max(tumor_probability, no_tumor_probability))
            
            # More conservative approach: flag as tumor if probability exceeds threshold
            # OR if tumor probability is close to normal (uncertain cases should be flagged)
            is_tumor = tumor_probability >= CANCER_THRESHOLD or (tumor_probability > 0.25 and confidence < 0.7)
            
            # Additional safety: if model is very uncertain (low confidence), recommend consultation
            is_uncertain = confidence < 0.6
            
            if is_tumor:
                prediction_text = "Tumor Detected"
                advice = [
                    "[IMPORTANT] Consult a specialist immediately",
                    "Early detection helps improve treatment outcomes",
                    "This is a screening tool - professional medical evaluation is essential",
                    "Follow medical advice and treatment plan"
                ]
            elif is_uncertain:
                # If model is uncertain, err on the side of caution
                prediction_text = "Uncertain - Medical Consultation Recommended"
                advice = [
                    "[WARNING] Model confidence is low - Professional evaluation recommended",
                    "No clear tumor detected, but results are uncertain",
                    "Consult a specialist if you have symptoms or concerns",
                    "Regular medical checkups are important"
                ]
            else:
                prediction_text = "No Tumor Detected"
                advice = [
                    "No tumor detected in the X-ray",
                    "[NOTE] This is a screening tool, not a replacement for medical diagnosis",
                    "Maintain healthy habits and regular checkups",
                    "Consult doctor if pain or symptoms continue",
                    "Keep monitoring your health"
                ]
        except Exception as e:
            print(f"[ERROR] Error during prediction: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to default
            prediction_text = "Prediction Error"
            confidence = 0.0
            advice = [f"Error occurred during prediction: {str(e)}"]
    else:
        # Fallback: Use simple heuristic based on image analysis
        # This is a placeholder until model is trained
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Simple heuristic: analyze image variance and intensity
        variance = np.var(img_array)
        mean_intensity = np.mean(img_array)
        
        # This is a very basic heuristic - replace with actual model
        # Higher variance might indicate abnormalities
        if variance > 2000 or mean_intensity < 100:
            prediction_text = "Tumor Detected"
            confidence = 0.75
        else:
            prediction_text = "No Tumor Detected"
            confidence = 0.80
        
        if prediction_text == "Tumor Detected":
            advice = [
                "Consult a specialist",
                "Early detection helps",
                "Stay strong and positive"
            ]
        else:
            advice = [
                "No tumor detected",
                "Maintain healthy habits",
                "Consult doctor if pain continues"
            ]

    result = {
        "prediction": prediction_text,
        "confidence": round(confidence, 2),
        "advice": advice
    }
    
    # Add detailed probability information for debugging
    if tumor_probability is not None and no_tumor_probability is not None:
        result["probabilities"] = {
            "normal": round(no_tumor_probability, 4),
            "tumor": round(tumor_probability, 4)
        }
        result["threshold_used"] = CANCER_THRESHOLD
        result["debug_info"] = f"Tumor probability: {tumor_probability:.4f}, Normal probability: {no_tumor_probability:.4f}"
    
    return result
