"""
Test the lung cancer case that failed
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_lung_cancer_case():
    """Test the lung cancer case that failed"""
    
    print("🚨 TESTING FAILED LUNG CANCER CASE")
    print("=" * 50)
    print("This should detect LUNG CANCER, not something else")
    print("=" * 50)
    
    # Test with the lung cancer image you uploaded
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print("This is actually a LUNG CANCER image")
        print()
        
        # Test the detection
        print("--- LUNG CANCER DETECTION TEST ---")
        result = auto_predict(image_bytes, filename_hint="lung_cancer.jpg")
        
        detected_organ = result.get('organ', '').lower()
        diagnosis = result.get('diagnosis', '').lower()
        confidence = result.get('diagnosis_confidence_pct', 0)
        method = result.get('method', '')
        
        print(f"Detected Organ: {detected_organ}")
        print(f"Diagnosis: {diagnosis}")
        print(f"Confidence: {confidence}%")
        print(f"Method: {method}")
        
        if result.get('emergency_override'):
            print(f"⚠️ EMERGENCY OVERRIDE: {result.get('override_reason')}")
        
        # Check debug info
        debug_info = result.get('debug', {})
        if debug_info:
            print(f"\n🔍 DEBUG INFO:")
            print(f"Decision: {debug_info.get('decision', 'No decision')}")
            
            confidence_breakdown = debug_info.get('confidence_breakdown', {})
            print(f"Image Confidence: {confidence_breakdown.get('image_confidence', 0)}")
            print(f"Filename Confidence: {confidence_breakdown.get('filename_confidence', 0)}")
            
            if 'all_scores' in debug_info:
                all_scores = debug_info['all_scores']
                print("All Organ Scores:")
                for organ, score in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {organ}: {score:.3f}")
        
        print()
        print("=" * 50)
        print("🎯 ANALYSIS:")
        
        # Check if it's detecting correctly
        if detected_organ == 'lung' and diagnosis in ['cancer', 'malignant', 'suspicious']:
            print("✅ CORRECT: Detected as LUNG CANCER")
        elif detected_organ == 'lung':
            print("⚠️ PARTIAL: Detected as LUNG but diagnosis is wrong")
            print(f"   Should be cancer, got: {diagnosis}")
        else:
            print(f"❌ INCORRECT: Should detect LUNG CANCER")
            print(f"   Got: {detected_organ} - {diagnosis}")
        
        print("\n🔧 NEED TO FIX:")
        if detected_organ != 'lung':
            print(f"1. Lung detection is not working (got {detected_organ})")
        if diagnosis not in ['cancer', 'malignant', 'suspicious']:
            print(f"2. Cancer detection is not working (got {diagnosis})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_lung_cancer_case()
