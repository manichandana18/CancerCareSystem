"""
Test that the system correctly ignores misleading filenames
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_filename_override():
    """Test that system analyzes image content, not filename"""
    
    print("🔍 TESTING FILENAME OVERRIDE PREVENTION")
    print("=" * 50)
    print("This test proves your system analyzes ACTUAL image content")
    print("=" * 50)
    
    # Test with the bone image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print("This is actually a BONE image")
        print()
        
        # Test cases with misleading filenames
        test_cases = [
            {
                "filename": "blood_sample.jpg",
                "name": "Bone image named as blood sample",
                "expected": "bone"
            },
            {
                "filename": "lung_xray.jpg", 
                "name": "Bone image named as lung xray",
                "expected": "bone"
            },
            {
                "filename": "brain_mri.jpg",
                "name": "Bone image named as brain MRI", 
                "expected": "bone"
            },
            {
                "filename": "skin_lesion.jpg",
                "name": "Bone image named as skin lesion",
                "expected": "bone"
            },
            {
                "filename": "breast_mammogram.jpg",
                "name": "Bone image named as breast mammogram",
                "expected": "bone"
            }
        ]
        
        all_correct = True
        
        for test in test_cases:
            print(f"--- {test['name']} ---")
            print(f"Filename: {test['filename']}")
            print(f"Expected: {test['expected']}")
            
            result = auto_predict(image_bytes, filename_hint=test['filename'])
            
            detected_organ = result.get('organ', '').lower()
            diagnosis = result.get('diagnosis', 'Unknown')
            confidence = result.get('diagnosis_confidence_pct', 0)
            
            print(f"Detected: {detected_organ}")
            print(f"Diagnosis: {diagnosis}")
            print(f"Confidence: {confidence}%")
            
            if detected_organ == test['expected']:
                print("✅ CORRECT: System analyzed image content, not filename!")
            else:
                print("❌ INCORRECT: System was fooled by filename")
                all_correct = False
            
            print()
        
        print("=" * 50)
        if all_correct:
            print("🎉 SUCCESS! Your system correctly analyzes image content!")
            print("🏆 It's NOT fooled by misleading filenames!")
            print("🚀 This is exactly what we wanted!")
        else:
            print("❌ Some tests failed - system needs improvement")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_filename_override()
