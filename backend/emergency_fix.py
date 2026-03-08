"""
Emergency fix for any model issues
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

def emergency_diagnostic():
    """Emergency diagnostic to find the issue"""
    
    print("🚨 EMERGENCY DIAGNOSTIC")
    print("=" * 40)
    
    # Test the basic components
    try:
        print("1. Testing smart organ detector...")
        from smart_organ_detector import smart_organ_detector
        
        test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        result = smart_organ_detector(image_bytes, filename_hint="test.jpg")
        print(f"✅ Smart detector: {result.get('organ')} - {result.get('confidence')}")
        
    except Exception as e:
        print(f"❌ Smart detector error: {e}")
    
    try:
        print("\n2. Testing auto predict...")
        from app.services.auto_predict import auto_predict
        
        result = auto_predict(image_bytes, filename_hint="test.jpg")
        print(f"✅ Auto predict: {result.get('organ')} - {result.get('diagnosis')}")
        
    except Exception as e:
        print(f"❌ Auto predict error: {e}")
    
    try:
        print("\n3. Testing differential diagnosis...")
        from differential_diagnosis import get_differential_diagnosis
        
        result = get_differential_diagnosis(image_bytes, {"organ": "skin", "diagnosis": "Malignant"})
        print(f"✅ Differential diagnosis: {result.get('primary_diagnosis', {}).get('cancer_type')}")
        
    except Exception as e:
        print(f"❌ Differential diagnosis error: {e}")
    
    try:
        print("\n4. Testing advanced analyzer...")
        from advanced_image_analyzer import analyze_medical_image_content
        
        result = analyze_medical_image_content(image_bytes)
        print(f"✅ Advanced analyzer: {result.get('organ')} - {result.get('confidence')}")
        
    except Exception as e:
        print(f"❌ Advanced analyzer error: {e}")
    
    print("\n" + "="*40)
    print("🔍 If you're seeing errors above, that's the issue!")
    print("📋 Please tell me what specific error you're seeing!")

if __name__ == "__main__":
    emergency_diagnostic()
