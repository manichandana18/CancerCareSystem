"""
Test all organ detections to find the issue
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_all_organ_detections():
    """Test all organ detections to find the issue"""
    
    print("🚨 TESTING ALL ORGAN DETECTIONS")
    print("=" * 60)
    print("Checking: bone, skin, blood - all showing as LUNG?")
    print("=" * 60)
    
    # Test with the image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Test different filename hints
        test_cases = [
            {
                "filename": "normal_bone.jpg",
                "expected_organ": "bone",
                "name": "Normal Bone Case"
            },
            {
                "filename": "skin_lesion.jpg",
                "expected_organ": "skin", 
                "name": "Skin Lesion Case"
            },
            {
                "filename": "blood_sample.jpg",
                "expected_organ": "blood",
                "name": "Blood Sample Case"
            },
            {
                "filename": "brain_mri.jpg",
                "expected_organ": "brain",
                "name": "Brain MRI Case"
            },
            {
                "filename": "breast_mammogram.jpg",
                "expected_organ": "breast",
                "name": "Breast Mammogram Case"
            }
        ]
        
        all_results = []
        
        for test in test_cases:
            print(f"--- {test['name']} ---")
            print(f"Filename: {test['filename']}")
            print(f"Expected Organ: {test['expected_organ']}")
            
            result = auto_predict(image_bytes, filename_hint=test['filename'])
            
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
            if debug_info and 'all_scores' in debug_info:
                all_scores = debug_info['all_scores']
                print("All Organ Scores:")
                for organ, score in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {organ}: {score:.3f}")
            
            # Store result
            all_results.append({
                'name': test['name'],
                'expected': test['expected_organ'],
                'detected': detected_organ,
                'diagnosis': diagnosis,
                'correct': detected_organ == test['expected_organ']
            })
            
            if detected_organ == test['expected_organ']:
                print("✅ CORRECT")
            else:
                print("❌ INCORRECT")
            
            print()
        
        # Summary
        print("=" * 60)
        print("📊 SUMMARY:")
        
        correct_count = sum(1 for r in all_results if r['correct'])
        total_count = len(all_results)
        
        print(f"Correct detections: {correct_count}/{total_count}")
        
        # Check what's being detected most
        detected_organs = [r['detected'] for r in all_results]
        from collections import Counter
        organ_counts = Counter(detected_organs)
        
        print("Detection distribution:")
        for organ, count in organ_counts.most_common():
            print(f"  {organ}: {count} times")
        
        # Identify the problem
        if organ_counts.get('lung', 0) >= 3:
            print("\n🚨 PROBLEM IDENTIFIED:")
            print("System is detecting too many images as LUNG")
            print("Need to fix lung detection boost logic")
        
        print("\n🔧 DETAILED ANALYSIS:")
        for result in all_results:
            if not result['correct']:
                print(f"❌ {result['name']}: Expected {result['expected']}, got {result['detected']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_all_organ_detections()
