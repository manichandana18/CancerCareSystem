"""
Test the bone detection fix
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_bone_detection_fix():
    """Test bone detection fix"""
    
    print("🔧 TESTING BONE DETECTION FIX")
    print("=" * 50)
    print("Testing: Bone images should detect as BONE")
    print("=" * 50)
    
    # Test with the bone image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Test Case 1: Normal bone image
        print("--- TEST 1: Normal bone image ---")
        result1 = auto_predict(image_bytes, filename_hint="normal_bone.jpg")
        
        detected_organ1 = result1.get('organ', '').lower()
        diagnosis1 = result1.get('diagnosis', '').lower()
        confidence1 = result1.get('diagnosis_confidence_pct', 0)
        
        print(f"Detected Organ: {detected_organ1}")
        print(f"Diagnosis: {diagnosis1}")
        print(f"Confidence: {confidence1}%")
        
        if detected_organ1 == 'bone':
            print("✅ CORRECT: Detected as BONE")
        else:
            print(f"❌ INCORRECT: Should detect BONE, got {detected_organ1}")
        
        print()
        
        # Test Case 2: Bone cancer image
        print("--- TEST 2: Bone cancer image ---")
        result2 = auto_predict(image_bytes, filename_hint="bone_cancer.jpg")
        
        detected_organ2 = result2.get('organ', '').lower()
        diagnosis2 = result2.get('diagnosis', '').lower()
        confidence2 = result2.get('diagnosis_confidence_pct', 0)
        
        print(f"Detected Organ: {detected_organ2}")
        print(f"Diagnosis: {diagnosis2}")
        print(f"Confidence: {confidence2}%")
        
        if detected_organ2 == 'bone':
            print("✅ CORRECT: Detected as BONE")
        else:
            print(f"❌ INCORRECT: Should detect BONE, got {detected_organ2}")
        
        print()
        
        # Test Case 3: Skin image (should NOT detect as bone)
        print("--- TEST 3: Skin image ---")
        result3 = auto_predict(image_bytes, filename_hint="skin_lesion.jpg")
        
        detected_organ3 = result3.get('organ', '').lower()
        diagnosis3 = result3.get('diagnosis', '').lower()
        confidence3 = result3.get('diagnosis_confidence_pct', 0)
        
        print(f"Detected Organ: {detected_organ3}")
        print(f"Diagnosis: {diagnosis3}")
        print(f"Confidence: {confidence3}%")
        
        # Check debug info
        debug_info = result3.get('debug', {})
        if debug_info and 'all_scores' in debug_info:
            all_scores = debug_info['all_scores']
            print("All Organ Scores:")
            for organ, score in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
                print(f"  {organ}: {score:.3f}")
        
        print()
        print("=" * 50)
        print("🎯 BONE DETECTION ANALYSIS:")
        
        bone_count = sum(1 for r in [result1, result2] if r.get('organ', '').lower() == 'bone')
        total_bone_tests = 2
        
        print(f"Bone detection: {bone_count}/{total_bone_tests}")
        
        if bone_count == total_bone_tests:
            print("✅ SUCCESS: Bone detection is working!")
        elif bone_count >= 1:
            print("⚠️ PARTIAL: Some bone detection working")
        else:
            print("❌ PROBLEM: Bone detection not working")
        
        print("\n🔧 NEXT STEPS:")
        if detected_organ3 == 'bone':
            print("❌ Still detecting skin as bone - need more refinement")
        else:
            print("✅ Skin correctly not detected as bone")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bone_detection_fix()
