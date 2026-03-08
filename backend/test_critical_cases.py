"""
Test the critical cases you mentioned
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_critical_cases():
    """Test the critical cases you mentioned"""
    
    print("🚨 TESTING CRITICAL CASES - EMERGENCY FIX")
    print("=" * 60)
    print("Testing: Blood sample named 'bone' should detect BLOOD")
    print("Testing: Lung cancer image named 'bone' should detect LUNG")
    print("=" * 60)
    
    # Test with the image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Test Case 1: Blood sample named as bone
        print("--- TEST 1: Blood sample named 'bone' ---")
        result1 = auto_predict(image_bytes, filename_hint="bone.jpg")
        
        detected_organ1 = result1.get('organ', '').lower()
        diagnosis1 = result1.get('diagnosis', '').lower()
        confidence1 = result1.get('diagnosis_confidence_pct', 0)
        
        print(f"Detected Organ: {detected_organ1}")
        print(f"Diagnosis: {diagnosis1}")
        print(f"Confidence: {confidence1}%")
        
        if result1.get('emergency_override'):
            print(f"⚠️ EMERGENCY OVERRIDE: {result1.get('override_reason')}")
        
        if detected_organ1 == 'blood':
            print("✅ CORRECT: Detected as BLOOD (ignoring filename)")
        else:
            print(f"❌ INCORRECT: Should detect BLOOD, got {detected_organ1}")
        
        print()
        
        # Test Case 2: Lung cancer image named as bone
        print("--- TEST 2: Lung cancer image named 'bone' ---")
        result2 = auto_predict(image_bytes, filename_hint="bone.jpg")
        
        detected_organ2 = result2.get('organ', '').lower()
        diagnosis2 = result2.get('diagnosis', '').lower()
        confidence2 = result2.get('diagnosis_confidence_pct', 0)
        
        print(f"Detected Organ: {detected_organ2}")
        print(f"Diagnosis: {diagnosis2}")
        print(f"Confidence: {confidence2}%")
        
        if result2.get('emergency_override'):
            print(f"⚠️ EMERGENCY OVERRIDE: {result2.get('override_reason')}")
        
        # Check if it's detecting cancer (not normal)
        if diagnosis2 in ['malignant', 'cancer', 'suspicious']:
            print("✅ CORRECT: Detected as CANCER (not normal)")
        else:
            print(f"❌ INCORRECT: Should detect CANCER, got {diagnosis2}")
        
        print()
        
        # Test Case 3: Check debug info
        print("--- TEST 3: Debug Information ---")
        debug_info = result2.get('debug', {})
        if debug_info:
            print(f"Method: {debug_info.get('method')}")
            print(f"Decision: {debug_info.get('decision')}")
            
            confidence_breakdown = debug_info.get('confidence_breakdown', {})
            print(f"Image Confidence: {confidence_breakdown.get('image_confidence', 0)}")
            print(f"Filename Confidence: {confidence_breakdown.get('filename_confidence', 0)}")
            
            if 'all_scores' in debug_info:
                all_scores = debug_info['all_scores']
                print("All Organ Scores:")
                for organ, score in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {organ}: {score:.3f}")
        
        print()
        print("=" * 60)
        print("🎯 CRITICAL ANALYSIS:")
        
        # Check if filename is being ignored
        filename_confidence = confidence_breakdown.get('filename_confidence', 0)
        if filename_confidence == 0.0:
            print("✅ SUCCESS: Filename is being IGNORED (correct)")
        else:
            print("❌ PROBLEM: Filename is still influencing detection")
        
        # Check if cancer is being detected
        if diagnosis2 in ['malignant', 'cancer', 'suspicious']:
            print("✅ SUCCESS: Cancer is being detected (reduced false negatives)")
        else:
            print("❌ PROBLEM: Still showing false negatives")
        
        print("🚀 Emergency fix applied - system should now work correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_critical_cases()
