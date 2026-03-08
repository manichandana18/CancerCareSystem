"""
Test lung detection issue - lung showing as bone
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_lung_detection():
    """Test lung detection showing as bone"""
    
    print("🫁 TESTING LUNG DETECTION ISSUE")
    print("=" * 50)
    print("Testing: Lung images showing as bone")
    print("=" * 50)
    
    # Test with the image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Test Case 1: Lung cancer image
        print("--- LUNG CANCER TEST ---")
        result1 = auto_predict(image_bytes, filename_hint="lung_cancer.jpg")
        
        print(f"Expected: LUNG - CANCER")
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
        
        # Test Case 2: Normal lung image
        print("--- NORMAL LUNG TEST ---")
        result2 = auto_predict(image_bytes, filename_hint="normal_lung.jpg")
        
        print(f"Expected: LUNG - NORMAL")
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
        print("🎯 LUNG DETECTION ANALYSIS:")
        
        organ1 = result1.get('organ', '').lower()
        organ2 = result2.get('organ', '').lower()
        
        if organ1 == 'lung' and organ2 == 'lung':
            print("✅ SUCCESS: Lung detection working correctly")
        elif organ1 == 'bone' or organ2 == 'bone':
            print("❌ PROBLEM: Lung images detected as bone")
            print("🔧 Need to fix lung vs bone detection logic")
        else:
            print(f"⚠️ UNEXPECTED: Detected as {organ1} and {organ2}")
        
        print("\n📋 IMAGE ANALYSIS:")
        print("If lung is detected as bone:")
        print("1. Bone detection is too aggressive")
        print("2. Lung detection logic needs improvement")
        print("3. Need to differentiate lung vs bone better")
        
        print("\n🔧 CURRENT ISSUE:")
        print("Your image characteristics:")
        print("- Aspect Ratio: 1.775 (wide - typical for lung)")
        print("- Brightness: 145.5 (moderate - could be lung)")
        print("- Edge Density: 0.033 (medium - could be lung)")
        print("- Gradient: 32.1 (high - could be lung)")
        print("But system is detecting as bone due to bone priority logic")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_lung_detection()
