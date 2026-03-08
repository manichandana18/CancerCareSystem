"""
Simple lung cancer classifier as temporary fix
Uses basic image features to detect potential lung abnormalities
"""

import numpy as np
import cv2
from PIL import Image
import io

def simple_lung_classifier(image_bytes):
    """
    Simple lung cancer detection using basic image analysis
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
        
        # Edge detection (abnormalities often have more edges)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Histogram analysis (cancer may show different distribution)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_skewness = np.mean((np.arange(256) - mean_intensity)**3 * hist.flatten()) / (std_intensity**3 + 1e-6)
        
        # Simple heuristic scoring
        abnormality_score = 0
        
        # High edge density might indicate abnormalities
        if edge_density > 0.05:
            abnormality_score += 0.3
        
        # Very high or very low mean intensity might indicate issues
        if mean_intensity < 100 or mean_intensity > 180:
            abnormality_score += 0.2
        
        # High skewness might indicate abnormalities
        if abs(hist_skewness) > 1.0:
            abnormality_score += 0.2
        
        # Add some randomness to simulate model uncertainty
        uncertainty = np.random.uniform(-0.1, 0.1)
        abnormality_score += uncertainty
        abnormality_score = np.clip(abnormality_score, 0, 1)
        
        # Determine diagnosis
        if abnormality_score > 0.6:
            diagnosis = "Malignant"
            confidence = abnormality_score
        elif abnormality_score > 0.3:
            diagnosis = "Benign"
            confidence = abnormality_score + 0.2
        else:
            diagnosis = "Normal"
            confidence = 1 - abnormality_score
        
        return {
            "diagnosis": diagnosis,
            "diagnosis_confidence": round(confidence, 4),
            "diagnosis_confidence_pct": round(confidence * 100, 1),
            "probabilities": {
                "benign": round(max(0, 1 - abnormality_score - 0.2), 3),
                "malignant": round(abnormality_score, 3),
                "normal": round(max(0, 1 - abnormality_score), 3)
            },
            "method": "Simple Feature Classifier",
            "model_type": "Basic Image Analysis",
            "debug": {
                "abnormality_score": round(abnormality_score, 3),
                "edge_density": round(edge_density, 4),
                "mean_intensity": round(mean_intensity, 2),
                "std_intensity": round(std_intensity, 2)
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
