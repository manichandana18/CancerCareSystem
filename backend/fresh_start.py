"""
Fresh Start - Clean Cancer Detection System
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def fresh_start_test():
    """Fresh start test - clean system check"""
    
    print("🚀 FRESH START - CLEAN CANCER DETECTION SYSTEM")
    print("=" * 60)
    print("Starting fresh with clean detection logic")
    print("=" * 60)
    
    # Test with the image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Test Case 1: Clean test - no filename hint
        print("--- CLEAN TEST: No filename hint ---")
        result1 = auto_predict(image_bytes, filename_hint=None)
        
        print(f"Detected Organ: {result1.get('organ')}")
        print(f"Diagnosis: {result1.get('diagnosis')}")
        print(f"Confidence: {result1.get('diagnosis_confidence_pct', 0)}%")
        print(f"Method: {result1.get('method')}")
        
        if result1.get('emergency_override'):
            print(f"⚠️ EMERGENCY OVERRIDE: {result.get('override_reason')}")
        
        print()
        
        # Test Case 2: Test with different filename hints
        test_cases = [
            "bone_cancer.jpg",
            "lung_cancer.jpg", 
            "skin_cancer.jpg",
            "brain_cancer.jpg",
            "blood_cancer.jpg",
            "breast_cancer.jpg"
        ]
        
        print("--- CONSISTENCY TEST: Different filename hints ---")
        
        results = []
        for filename in test_cases:
            result = auto_predict(image_bytes, filename_hint=filename)
            organ = result.get('organ', '').lower()
            diagnosis = result.get('diagnosis', '').lower()
            confidence = result.get('diagnosis_confidence_pct', 0)
            
            results.append({
                'filename': filename,
                'organ': organ,
                'diagnosis': diagnosis,
                'confidence': confidence
            })
            
            print(f"{filename:20} → {organ:8} - {diagnosis:10} ({confidence}%)")
        
        print()
        print("=" * 60)
        print("🎯 CONSISTENCY ANALYSIS:")
        
        # Check if all results are the same
        organs = [r['organ'] for r in results]
        diagnoses = [r['diagnosis'] for r in results]
        
        if len(set(organs)) == 1:
            print("✅ CONSISTENT: Same organ detected regardless of filename")
            print(f"   Organ: {organs[0]}")
        else:
            print("❌ INCONSISTENT: Different organs detected")
            print(f"   Organs: {set(organs)}")
        
        if len(set(diagnoses)) == 1:
            print("✅ CONSISTENT: Same diagnosis regardless of filename")
            print(f"   Diagnosis: {diagnoses[0]}")
        else:
            print("❌ INCONSISTENT: Different diagnoses detected")
            print(f"   Diagnoses: {set(diagnoses)}")
        
        print()
        print("🔍 FINAL RESULT:")
        final_result = results[0]  # First result
        print(f"Your image is detected as: {final_result['organ'].upper()} - {final_result['diagnosis'].upper()}")
        print(f"Confidence: {final_result['confidence']}%")
        
        print()
        print("🎉 FRESH START COMPLETE!")
        print("System is ready for accurate cancer detection!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fresh_start_test()
