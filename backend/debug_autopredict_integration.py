"""
Debug auto-predict integration to see if smart classifier is being used
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

def test_autopredict_integration():
    """Test if smart classifier is being used in auto-predict"""
    
    print("🔍 Debugging Auto-Predict Integration")
    print("=" * 50)
    
    # Test with lung image
    lung_path = input("Enter path to LUNG X-ray image: ").strip().strip('"')
    
    if not os.path.exists(lung_path):
        print(f"❌ File not found: {lung_path}")
        return
    
    try:
        # Test organ classifier directly
        print("\n📋 Step 1: Testing Organ Classifier Directly")
        from app.services.organ_classifier import predict_organ
        
        with open(lung_path, 'rb') as f:
            image_bytes = f.read()
        
        organ_result = predict_organ(image_bytes)
        print(f"🎯 Organ Classifier Result: {organ_result}")
        
        # Test auto-predict
        print("\n📋 Step 2: Testing Auto-Predict")
        from app.services.auto_predict import auto_predict
        
        auto_result = auto_predict(image_bytes)
        print(f"🎯 Auto-Predict Result: {auto_result}")
        
        # Compare results
        print("\n📊 Comparison:")
        print(f"Organ from classifier: {organ_result.get('organ')}")
        print(f"Organ from auto-predict: {auto_result.get('organ')}")
        
        if organ_result.get('organ') == auto_result.get('organ'):
            print("✅ Organ classification is consistent")
        else:
            print("❌ Organ classification is inconsistent!")
        
        # Check method used
        method = organ_result.get('debug', {}).get('method', 'Unknown')
        print(f"Method used: {method}")
        
        if 'Smart' in method:
            print("✅ Smart classifier is being used")
        else:
            print("❌ Smart classifier is NOT being used")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_autopredict_integration()
