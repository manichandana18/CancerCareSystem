"""
Smart Organ Classifier - Uses image analysis to properly detect bone vs lung
"""

import numpy as np
import cv2
from PIL import Image
import io

def smart_organ_classifier(image_bytes):
    """
    Smart organ classification using image analysis
    """
    
    try:
        # Convert bytes to image
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image = np.array(image)
        
        # Resize to standard size
        image = cv2.resize(image, (224, 224))
        
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Calculate image characteristics
        mean_intensity = np.mean(gray)
        std_intensity = np.std(gray)
        
        # Edge density analysis
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Texture analysis using Local Binary Pattern
        from skimage.feature import local_binary_pattern
        lbp = local_binary_pattern(gray, 8, 1, method='uniform')
        lbp_hist, _ = np.histogram(lbp.ravel(), bins=10)
        lbp_hist = lbp_hist.astype(float)
        lbp_hist /= (lbp_hist.sum() + 1e-6)
        
        # Shape and structure analysis
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        num_contours = len(contours)
        
        # Decision logic based on medical imaging characteristics
        lung_score = 0
        bone_score = 0
        
        # Lung X-rays typically have:
        # - Moderate intensity (not too dark, not too bright)
        # - Lower edge density (softer tissue)
        # - More uniform texture
        # - Larger, rounded structures (lung fields)
        
        if 100 <= mean_intensity <= 160:
            lung_score += 2
        else:
            bone_score += 1
            
        if edge_density < 0.08:
            lung_score += 2
        else:
            bone_score += 1
            
        if std_intensity < 50:
            lung_score += 1
        else:
            bone_score += 1
            
        # Texture analysis - lungs have more uniform texture
        if lbp_hist[0] > 0.3:  # High uniform texture
            lung_score += 1
        else:
            bone_score += 1
            
        # Contour analysis - lungs have fewer, larger contours
        if num_contours < 100:
            lung_score += 1
        else:
            bone_score += 1
        
        # Decision logic with better tie-breaking and more features
        if lung_score > bone_score:
            organ = "lung"
            confidence = min(0.9, 0.6 + (lung_score - bone_score) * 0.1)
        elif bone_score > lung_score:
            organ = "bone"
            confidence = min(0.9, 0.6 + (bone_score - lung_score) * 0.1)
        else:
            # Enhanced tie-breaking with more sophisticated logic
            print(f"🔀 TIE DETECTED: lung={lung_score}, bone={bone_score}")
            
            # Factor 1: Intensity analysis with better ranges
            intensity_score = 0
            if mean_intensity < 70:
                intensity_score = 2  # Very dark = likely bone
            elif mean_intensity < 100:
                intensity_score = 1  # Dark = likely bone
            elif mean_intensity <= 140:
                intensity_score = -1  # Medium = likely lung
            elif mean_intensity <= 180:
                intensity_score = -2  # Light-medium = likely lung
            else:
                intensity_score = 1  # Very light = likely bone
            
            # Factor 2: Edge density analysis
            edge_score = 0
            if edge_density > 0.08:
                edge_score = 2  # High edge = bone
            elif edge_density > 0.05:
                edge_score = 1  # Medium edge = bone
            elif edge_density > 0.03:
                edge_score = -1  # Low edge = lung
            else:
                edge_score = -2  # Very low edge = lung
            
            # Factor 3: Contour analysis
            contour_score = 0
            if num_contours > 40:
                contour_score = 2  # Many contours = bone
            elif num_contours > 25:
                contour_score = 1  # Medium contours = bone
            elif num_contours > 15:
                contour_score = -1  # Few contours = lung
            else:
                contour_score = -2  # Very few contours = lung
            
            # Factor 4: Texture analysis (std intensity)
            texture_score = 0
            if std_intensity > 70:
                texture_score = 1  # High texture variation = bone
            elif std_intensity > 50:
                texture_score = 0  # Medium = neutral
            else:
                texture_score = -1  # Low texture variation = lung
            
            # Calculate total score
            total_score = intensity_score + edge_score + contour_score + texture_score
            
            print(f"   → Scores: Intensity={intensity_score}, Edge={edge_score}, Contour={contour_score}, Texture={texture_score}")
            print(f"   → Total Score: {total_score}")
            
            if total_score > 0:
                organ = "bone"
                confidence = min(0.85, 0.6 + abs(total_score) * 0.05)
                print(f"   → Final: BONE (score={total_score})")
            else:
                organ = "lung"
                confidence = min(0.85, 0.6 + abs(total_score) * 0.05)
                print(f"   → Final: LUNG (score={total_score})")
        
        return {
            "organ": organ,
            "confidence": round(confidence * 100, 2),
            "method": "Smart Image Analysis",
            "debug": {
                "lung_score": lung_score,
                "bone_score": bone_score,
                "mean_intensity": round(mean_intensity, 2),
                "edge_density": round(edge_density, 4),
                "std_intensity": round(std_intensity, 2),
                "num_contours": num_contours
            }
        }
        
    except Exception as e:
        # Fallback to basic analysis
        return {
            "organ": "uncertain",
            "confidence": 50.0,
            "method": "Error Fallback",
            "error": str(e)
        }
