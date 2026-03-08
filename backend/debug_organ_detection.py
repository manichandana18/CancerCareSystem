"""
Debug organ detection to understand what's happening
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from smart_organ_detector import smart_organ_detector

def debug_organ_detection():
    """Debug organ detection with detailed analysis"""
    
    print("🔍 DEBUGGING ORGAN DETECTION")
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
            
            result = smart_organ_detector(image_bytes, filename_hint=test['filename'])
            
            predicted_organ = result.get('organ', '').lower()
            confidence = result.get('confidence', 0)
            method = result.get('method', 'Unknown')
            debug_info = result.get('debug', {})
            
            print(f"Predicted Organ: {predicted_organ}")
            print(f"Confidence: {confidence}")
            print(f"Method: {method}")
            
            if 'confidence_breakdown' in debug_info:
                breakdown = debug_info['confidence_breakdown']
                print(f"Image Confidence: {breakdown.get('image_confidence', 0)}")
                print(f"Filename Confidence: {breakdown.get('filename_confidence', 0)}")
            
            if predicted_organ == test['expected_organ'].lower():
                print("✅ SUCCESS")
            else:
                print("❌ FAILED")
            
            print()
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_organ_detection()
