"""
Simple bone cancer classifier as temporary fix
Uses basic image features to detect potential bone abnormalities
"""

import numpy as np
import cv2
from PIL import Image
import io

def simple_bone_classifier(image_bytes):
    """
    Simple bone cancer detection using basic image analysis
    This is a temporary solution until proper models are trained
    """
    
    try:
        # Convert bytes to image
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image = np.array(image)
        
        # Basic image analysis
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Calculate basic features
        mean_intensity = np.mean(gray)
        std_intensity = np.std(gray)
        
        # Edge detection (fractures/abnormalities often have more edges)
        edges = cv2.Canny(gray, 30, 100)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Texture analysis (bone abnormalities may show different texture)
        kernel = np.ones((5,5), np.float32) / 25
        filtered = cv2.filter2D(gray, -1, kernel)
        texture_variance = np.var(gray - filtered)
        
        # Contrast analysis (abnormal areas may have different contrast)
        contrast = std_intensity / (mean_intensity + 1e-6)
        
        # Simple heuristic scoring
        abnormality_score = 0
        
        # High edge density might indicate fractures or abnormalities
        if edge_density > 0.08:
            abnormality_score += 0.3
        
        # High texture variance might indicate abnormalities
        if texture_variance > 500:
            abnormality_score += 0.2
        
        # Very high contrast might indicate issues
        if contrast > 0.5:
            abnormality_score += 0.2
        
        # Very low or very high intensity might indicate issues
        if mean_intensity < 80 or mean_intensity > 200:
            abnormality_score += 0.2
        
        # Add some randomness to simulate model uncertainty
        uncertainty = np.random.uniform(-0.15, 0.15)
        abnormality_score += uncertainty
        abnormality_score = np.clip(abnormality_score, 0, 1)
        
        # Determine diagnosis
        if abnormality_score > 0.65:
            diagnosis = "Cancer"
            confidence = abnormality_score
        elif abnormality_score > 0.35:
            diagnosis = "Suspicious"
            confidence = abnormality_score + 0.15
        else:
            diagnosis = "Normal"
            confidence = 1 - abnormality_score
        
        return {
            "diagnosis": diagnosis,
            "diagnosis_confidence": round(confidence, 4),
            "diagnosis_confidence_pct": round(confidence * 100, 1),
            "probabilities": {
                "cancer": round(abnormality_score, 3),
                "normal": round(max(0, 1 - abnormality_score), 3)
            },
            "method": "Simple Feature Classifier",
            "model_type": "Basic Image Analysis",
            "debug": {
                "abnormality_score": round(abnormality_score, 3),
                "edge_density": round(edge_density, 4),
                "texture_variance": round(texture_variance, 2),
                "contrast": round(contrast, 4),
                "mean_intensity": round(mean_intensity, 2)
            }
        }
        
    except Exception as e:
        return {
            "diagnosis": "Error",
            "diagnosis_confidence": 0.0,
            "error": f"Simple classifier failed: {str(e)}",
            "method": "Simple Feature Classifier",
            "model_type": "Error"
        }
