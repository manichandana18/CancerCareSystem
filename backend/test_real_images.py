"""
Test with real image content detection
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_real_images():
    """Test with actual medical images"""
    
    print("🔍 TESTING REAL IMAGE CONTENT DETECTION")
    print("=" * 60)
    print("This test shows what the image ACTUALLY contains")
    print("Not what the filename says")
    print("=" * 60)
    
    # Test with the bone image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Test with different filenames to show image content wins
        test_cases = [
            {
                "filename": "bonecancer.jpg",
                "name": "Correct filename (bonecancer.jpg)"
            },
            {
                "filename": "bloodcancer.jpg", 
                "name": "Wrong filename (bloodcancer.jpg) - but image is bone"
            },
            {
                "filename": "lungcancer.jpg",
                "name": "Wrong filename (lungcancer.jpg) - but image is bone"
            },
            {
                "filename": "braincancer.jpg",
                "name": "Wrong filename (braincancer.jpg) - but image is bone"
            },
            {
                "filename": "skincancer.jpg",
                "name": "Wrong filename (skincancer.jpg) - but image is bone"
            },
            {
                "filename": "breastcancer.jpg",
                "name": "Wrong filename (breastcancer.jpg) - but image is bone"
            }
        ]
        
        for test in test_cases:
            print(f"--- {test['name']} ---")
            print(f"Filename: {test['filename']}")
            
            result = auto_predict(image_bytes, filename_hint=test['filename'])
            
            detected_organ = result.get('organ', 'Unknown')
            diagnosis = result.get('diagnosis', 'Unknown')
            confidence = result.get('diagnosis_confidence_pct', 0)
            method = result.get('method', 'Unknown')
            
            print(f"Detected Organ: {detected_organ}")
            print(f"Diagnosis: {diagnosis}")
            print(f"Confidence: {confidence}%")
            print(f"Method: {method}")
            
            if detected_organ.lower() == 'bone':
                print("✅ CORRECT: Image content is bone, detected as bone")
            else:
                print("❌ INCORRECT: Should detect as bone")
            
            print()
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_real_images()
