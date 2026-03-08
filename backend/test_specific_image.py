"""
Test organ classifier with a specific image file
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.organ_classifier import predict_organ

def test_specific_image(image_path):
    """Test organ classifier with a specific image file"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return
    
    print(f"🔍 Testing image: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        result = predict_organ(image_bytes)
        print(f"🎯 Result: {result}")
        
        # Check if debug info is available
        if 'debug' in result:
            print(f"📊 Bone prob: {result['debug']['bone_prob']}%")
            print(f"🫁 Lung prob: {result['debug']['lung_prob']}%")
        
    except Exception as e:
        print(f"❌ Error processing image: {e}")

if __name__ == "__main__":
    # Test with a sample image - replace with your actual image path
    image_path = input("Enter the path to your lung X-ray image: ").strip().strip('"')
    test_specific_image(image_path)
