"""
Test the brain override issue
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_brain_override():
    """Test the brain override issue"""
    
    print("🚨 TESTING BRAIN OVERRIDE ISSUE")
    print("=" * 50)
    print("Testing: Normal bone image showing as brain normal")
    print("=" * 50)
    
    # Test with the bone image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Test normal bone case
        print("--- NORMAL BONE CASE ---")
        result = auto_predict(image_bytes, filename_hint="normal_bone.jpg")
        
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
        print("🎯 ANALYSIS:")
        
        if detected_organ == 'brain':
            print("❌ PROBLEM: Detected as BRAIN instead of BONE")
            print("🔧 Need to fix brain detection logic")
        elif detected_organ == 'bone':
            print("✅ CORRECT: Detected as BONE")
        else:
            print(f"⚠️ UNEXPECTED: Detected as {detected_organ}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_brain_override()
