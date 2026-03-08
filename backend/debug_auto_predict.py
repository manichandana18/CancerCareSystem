"""
Debug script to test auto-predict with specific images
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict
from app.services.organ_classifier import predict_organ

def debug_auto_predict(image_path):
    """Debug auto-predict with a specific image file"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return
    
    print(f"🔍 Testing image: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        print("\n=== STEP 1: Organ Classification ===")
        organ_result = predict_organ(image_bytes)
        print(f"🎯 Organ Result: {organ_result}")
        
        print("\n=== STEP 2: Auto Prediction ===")
        auto_result = auto_predict(image_bytes)
        print(f"🎯 Auto Result: {auto_result}")
        
        print("\n=== ANALYSIS ===")
        print(f"Detected Organ: {auto_result.get('organ')}")
        print(f"Organ Confidence: {auto_result.get('organ_confidence_pct')}%")
        print(f"Diagnosis: {auto_result.get('diagnosis')}")
        print(f"Diagnosis Confidence: {auto_result.get('diagnosis_confidence_pct')}%")
        print(f"Method: {auto_result.get('method')}")
        
        if 'error' in auto_result:
            print(f"❌ Error: {auto_result['error']}")
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test with a specific image
    image_path = input("Enter the full path to your lung cancer image: ").strip().strip('"')
    debug_auto_predict(image_path)
