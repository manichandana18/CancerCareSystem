"""
Debug the current detection issue
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def debug_current_issue():
    """Debug what's actually happening with detection"""
    
    print("🚨 DEBUGGING CURRENT DETECTION ISSUE")
    print("=" * 60)
    print("Checking: What is the system actually detecting?")
    print("=" * 60)
    
    # Test with the image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Test multiple scenarios
        test_cases = [
            {
                "filename": "pic1_bone_normal.jpg",
                "name": "Pic 1: Bone Normal (showing brain normal)"
            },
            {
                "filename": "pic2_bone_cancer.jpg", 
                "name": "Pic 2: Bone Cancer (showing brain cancer)"
            },
            {
                "filename": "skin_lesion.jpg",
                "name": "Skin Lesion (showing bone)"
            },
            {
                "filename": "blood_sample.jpg",
                "name": "Blood Sample (showing bone)"
            }
        ]
        
        for test in test_cases:
            print(f"--- {test['name']} ---")
            print(f"Filename: {test['filename']}")
            
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
            if debug_info:
                print(f"Decision: {debug_info.get('decision', 'No decision')}")
                
                if 'all_scores' in debug_info:
                    all_scores = debug_info['all_scores']
                    print("All Organ Scores:")
                    for organ, score in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
                        print(f"  {organ}: {score:.3f}")
            
            print()
        
        print("=" * 60)
        print("🎯 ISSUE ANALYSIS:")
        
        # Check what's being detected most
        print("The system appears to be stuck on detecting one organ type.")
        print("This suggests the advanced analyzer is not working properly.")
        
        print("\n🔧 IMMEDIATE FIX NEEDED:")
        print("1. Check if advanced analyzer is being called")
        print("2. Check if organ detection logic is working")
        print("3. Check if there's a fallback to basic detection")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_current_issue()
