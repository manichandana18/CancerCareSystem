"""
Test the organ detection fix
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_organ_detection():
    """Test organ detection with filename hints"""
    
    print("🔧 TESTING ORGAN DETECTION FIX")
    print("=" * 50)
    
    test_cases = [
        {
            "filename": "bonecancer.jpg",
            "expected_organ": "bone",
            "name": "Bone Cancer Test"
        },
        {
            "filename": "lungcancer.jpg", 
            "expected_organ": "lung",
            "name": "Lung Cancer Test"
        },
        {
            "filename": "braincancer.jpg",
            "expected_organ": "brain", 
            "name": "Brain Cancer Test"
        },
        {
            "filename": "bloodcancer.jpg",
            "expected_organ": "blood",
            "name": "Blood Cancer Test"
        },
        {
            "filename": "skincancer.jpg",
            "expected_organ": "skin",
            "name": "Skin Cancer Test"
        },
        {
            "filename": "breastcancer.jpg",
            "expected_organ": "breast",
            "name": "Breast Cancer Test"
        }
    ]
    
    # Use a test image
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Using test image: {test_image_path}")
        print()
        
        for test in test_cases:
            print(f"--- {test['name']} ---")
            print(f"Filename: {test['filename']}")
            print(f"Expected Organ: {test['expected_organ']}")
            
            result = auto_predict(image_bytes, filename_hint=test['filename'])
            
            predicted_organ = result.get('organ', '').lower()
            confidence = result.get('diagnosis_confidence_pct', 0)
            method = result.get('method', 'Unknown')
            
            if predicted_organ == test['expected_organ'].lower():
                print(f"✅ SUCCESS: {predicted_organ} (confidence: {confidence}%)")
            else:
                print(f"❌ FAILED: Expected {test['expected_organ']}, got {predicted_organ}")
            
            print(f"Method: {method}")
            print()
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_organ_detection()
