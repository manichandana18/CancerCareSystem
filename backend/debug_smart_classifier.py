"""
Debug the smart organ classifier
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

def test_smart_classifier():
    """Test the smart organ classifier directly"""
    
    print("🧪 Testing Smart Organ Classifier")
    print("=" * 40)
    
    # Test with a lung image
    lung_path = input("Enter path to LUNG X-ray image: ").strip().strip('"')
    
    if not os.path.exists(lung_path):
        print(f"❌ File not found: {lung_path}")
        return
    
    try:
        # Test smart classifier directly
        from smart_organ_classifier import smart_organ_classifier
        
        with open(lung_path, 'rb') as f:
            image_bytes = f.read()
        
        result = smart_organ_classifier(image_bytes)
        print(f"🎯 Smart Classifier Result: {result}")
        
    except Exception as e:
        print(f"❌ Smart classifier failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "-" * 40)
    
    # Test with bone image
    bone_path = input("Enter path to BONE X-ray image: ").strip().strip('"')
    
    if not os.path.exists(bone_path):
        print(f"❌ File not found: {bone_path}")
        return
    
    try:
        with open(bone_path, 'rb') as f:
            image_bytes = f.read()
        
        result = smart_organ_classifier(image_bytes)
        print(f"🎯 Smart Classifier Result: {result}")
        
    except Exception as e:
        print(f"❌ Smart classifier failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_smart_classifier()
