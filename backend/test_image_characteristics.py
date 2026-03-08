"""
Test image characteristics to understand bone vs lung X-ray differences
"""

import os
import sys
import numpy as np
from pathlib import Path
from PIL import Image
import io

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.organ_classifier import preprocess_image

def analyze_image_characteristics(image_path):
    """Analyze image characteristics to distinguish bone vs lung"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return
    
    print(f"🔍 Analyzing image: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        # Preprocess image
        img = preprocess_image(image_bytes)
        img_array = img[0]  # Remove batch dimension
        
        # Calculate characteristics
        mean_intensity = np.mean(img_array)
        std_intensity = np.std(img_array)
        contrast_ratio = std_intensity / (mean_intensity + 1e-6)
        
        # Channel analysis
        mean_r = np.mean(img_array[:, :, 0])
        mean_g = np.mean(img_array[:, :, 1])
        mean_b = np.mean(img_array[:, :, 2])
        
        print(f"📊 Image Characteristics:")
        print(f"   Mean Intensity: {mean_intensity:.2f}")
        print(f"   Std Intensity: {std_intensity:.2f}")
        print(f"   Contrast Ratio: {contrast_ratio:.4f}")
        print(f"   RGB Means: R={mean_r:.2f}, G={mean_g:.2f}, B={mean_b:.2f}")
        
        # Heuristic classification
        is_likely_lung = (
            mean_intensity > 100 and 
            mean_intensity < 180 and 
            contrast_ratio < 0.4
        )
        
        is_likely_bone = (
            mean_intensity < 100 or 
            mean_intensity > 180 or 
            contrast_ratio > 0.5
        )
        
        print(f"\n🎯 Heuristic Analysis:")
        print(f"   Likely Lung: {is_likely_lung}")
        print(f"   Likely Bone: {is_likely_bone}")
        
        if is_likely_lung:
            print(f"   ✅ Image appears to be a LUNG X-ray")
        elif is_likely_bone:
            print(f"   ✅ Image appears to be a BONE X-ray")
        else:
            print(f"   ❓ Image characteristics are unclear")
        
    except Exception as e:
        print(f"❌ Error analyzing image: {e}")

if __name__ == "__main__":
    # Test with lung image
    lung_path = input("Enter the full path to your LUNG X-ray image: ").strip().strip('"')
    analyze_image_characteristics(lung_path)
    
    print("\n" + "="*50 + "\n")
    
    # Test with bone image
    bone_path = input("Enter the full path to your BONE X-ray image: ").strip().strip('"')
    analyze_image_characteristics(bone_path)
