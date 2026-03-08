"""
Test bone detection issue - bone showing as blood
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_bone_detection():
    """Test bone detection showing as blood"""
    
    print("🦴 TESTING BONE DETECTION ISSUE")
    print("=" * 50)
    print("Testing: Bone images showing as blood")
    print("=" * 50)
    
    # Test with the image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Test Case 1: Bone cancer image
        print("--- BONE CANCER TEST ---")
        result1 = auto_predict(image_bytes, filename_hint="bone_cancer.jpg")
        
        print(f"Expected: BONE - CANCER")
        print(f"Detected: {result1.get('organ')} - {result1.get('diagnosis')}")
        print(f"Confidence: {result1.get('diagnosis_confidence_pct', 0)}%")
        print(f"Method: {result1.get('method')}")
        
        # Check debug info
        debug_info = result1.get('debug', {})
        if debug_info and 'all_scores' in debug_info:
            all_scores = debug_info['all_scores']
            print("All Organ Scores:")
            for organ, score in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
                print(f"  {organ}: {score:.3f}")
        
        print()
        
        # Test Case 2: Normal bone image
        print("--- NORMAL BONE TEST ---")
        result2 = auto_predict(image_bytes, filename_hint="normal_bone.jpg")
        
        print(f"Expected: BONE - NORMAL")
        print(f"Detected: {result2.get('organ')} - {result2.get('diagnosis')}")
        print(f"Confidence: {result2.get('diagnosis_confidence_pct', 0)}%")
        print(f"Method: {result2.get('method')}")
        
        print()
        
        # Check what the advanced analyzer says
        print("--- ADVANCED ANALYZER CHECK ---")
        try:
            from advanced_image_analyzer import analyze_medical_image_content
            analyzer_result = analyze_medical_image_content(image_bytes)
            
            print(f"Advanced Analyzer Result:")
            print(f"  Organ: {analyzer_result.get('organ')}")
            print(f"  Confidence: {analyzer_result.get('confidence'):.3f}")
            print(f"  All Scores: {analyzer_result.get('all_scores', {})}")
            
        except Exception as e:
            print(f"Error in advanced analyzer: {e}")
        
        print()
        print("=" * 50)
        print("🎯 BONE DETECTION ANALYSIS:")
        
        organ1 = result1.get('organ', '').lower()
        organ2 = result2.get('organ', '').lower()
        
        if organ1 == 'bone' and organ2 == 'bone':
            print("✅ SUCCESS: Bone detection working correctly")
        elif organ1 == 'blood' or organ2 == 'blood':
            print("❌ PROBLEM: Bone images detected as blood")
            print("🔧 Need to fix bone vs blood detection logic")
        else:
            print(f"⚠️ UNEXPECTED: Detected as {organ1} and {organ2}")
        
        print("\n📋 IMAGE ANALYSIS:")
        print("If bone is detected as blood:")
        print("1. Image characteristics match blood pattern")
        print("2. Bone detection logic needs improvement")
        print("3. Need to differentiate bone vs blood better")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bone_detection()
