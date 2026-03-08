"""
Diagnose why model is not predicting perfectly
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def diagnose_model_issues():
    """Diagnose model prediction issues"""
    
    print("🔍 DIAGNOSING MODEL PREDICTION ISSUES")
    print("=" * 60)
    print("Finding why model is not predicting perfectly")
    print("=" * 60)
    
    # Test with your image
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Test 1: Deep analysis of current detection
        print("--- DEEP DETECTION ANALYSIS ---")
        result = auto_predict(image_bytes, filename_hint="test.jpg")
        
        detected_organ = result.get('organ', '').lower()
        diagnosis = result.get('diagnosis', '').lower()
        confidence = result.get('diagnosis_confidence_pct', 0)
        method = result.get('method', '')
        
        print(f"Current Detection:")
        print(f"  Organ: {detected_organ}")
        print(f"  Diagnosis: {diagnosis}")
        print(f"  Confidence: {confidence}%")
        print(f"  Method: {method}")
        
        # Check debug info
        debug_info = result.get('debug', {})
        if debug_info:
            print(f"  Decision: {debug_info.get('decision', 'No decision')}")
            
            if 'all_scores' in debug_info:
                all_scores = debug_info['all_scores']
                print("  All Organ Scores:")
                for organ, score in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
                    print(f"    {organ}: {score:.3f}")
        
        print()
        
        # Test 2: Analyze what should be detected
        print("--- WHAT SHOULD BE DETECTED ---")
        
        # Get image characteristics
        try:
            from advanced_image_analyzer import analyze_medical_image_content
            analyzer_result = analyze_medical_image_content(image_bytes)
            
            features = analyzer_result.get('features', {})
            aspect_ratio = features.get('aspect_ratio', 0)
            brightness = features.get('mean_brightness', 0)
            edge_density = features.get('edge_density', 0)
            mean_gradient = features.get('mean_gradient', 0)
            
            print("Image Characteristics:")
            print(f"  Aspect Ratio: {aspect_ratio:.3f}")
            print(f"  Brightness: {brightness:.1f}")
            print(f"  Edge Density: {edge_density:.3f}")
            print(f"  Mean Gradient: {mean_gradient:.1f}")
            
            print()
            print("Expected Organ Based on Characteristics:")
            
            # Analyze characteristics
            if aspect_ratio > 1.5:
                print("  ✅ Wide image → Likely LUNG (chest X-ray)")
                expected_organ = "lung"
            elif aspect_ratio < 1.2:
                print("  ✅ Square image → Likely BONE (limb X-ray)")
                expected_organ = "bone"
            elif brightness > 140:
                print("  ✅ Bright image → Likely SKIN (color-rich)")
                expected_organ = "skin"
            elif edge_density > 0.1:
                print("  ✅ High edge density → Likely BLOOD (cell boundaries)")
                expected_organ = "blood"
            else:
                print("  ✅ Moderate characteristics → Could be BRAIN/BREAST")
                expected_organ = "brain"
            
            print(f"  Expected: {expected_organ.upper()}")
            print(f"  Detected: {detected_organ.upper()}")
            
            if detected_organ == expected_organ:
                print("  ✅ CORRECT ORGAN DETECTION")
            else:
                print("  ❌ INCORRECT ORGAN DETECTION")
                print("  🔧 This is why model is not perfect!")
            
        except Exception as e:
            print(f"Error in analysis: {e}")
        
        print()
        
        # Test 3: Check for common issues
        print("--- COMMON MODEL ISSUES ---")
        
        issues = []
        
        # Issue 1: Low confidence
        if confidence < 80:
            issues.append("Low confidence in predictions")
        
        # Issue 2: Inconsistent detection
        test_filenames = [
            "bone_cancer.jpg",
            "lung_cancer.jpg", 
            "skin_cancer.jpg",
            "blood_cancer.jpg"
        ]
        
        detections = []
        for filename in test_filenames:
            result = auto_predict(image_bytes, filename_hint=filename)
            organ = result.get('organ', '').lower()
            detections.append(organ)
        
        if len(set(detections)) > 1:
            issues.append("Inconsistent detection across filenames")
        
        # Issue 3: Wrong diagnosis
        if diagnosis == 'normal' and 'cancer' in test_image_path.lower():
            issues.append("Cancer image detected as normal")
        
        # Issue 4: Method issues
        if 'fallback' in method.lower():
            issues.append("Using fallback detection method")
        
        if 'error' in method.lower():
            issues.append("Detection method has errors")
        
        print("Identified Issues:")
        if issues:
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
        else:
            print("  ✅ No major issues detected")
        
        print()
        
        # Test 4: Performance check
        print("--- PERFORMANCE CHECK ---")
        
        import time
        start_time = time.time()
        
        for _ in range(3):
            result = auto_predict(image_bytes, filename_hint="perf_test.jpg")
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 3
        
        print(f"Average Response Time: {avg_time:.2f} seconds")
        
        if avg_time > 5:
            issues.append("Slow response time")
        elif avg_time > 2:
            issues.append("Moderate response time")
        else:
            print("  ✅ Good response time")
        
        print()
        print("=" * 60)
        print("🎯 DIAGNOSIS SUMMARY:")
        
        if issues:
            print("❌ MODEL ISSUES FOUND:")
            for issue in issues:
                print(f"  • {issue}")
            
            print("\n🔧 RECOMMENDED FIXES:")
            if "Inconsistent" in str(issues):
                print("  1. Fix filename override logic")
            if "Low confidence" in str(issues):
                print("  2. Improve model confidence calibration")
            if "Cancer image detected as normal" in str(issues):
                print("  3. Fix cancer detection sensitivity")
            if "fallback" in str(issues):
                print("  4. Improve primary detection methods")
            if "Slow" in str(issues):
                print("  5. Optimize model performance")
        else:
            print("✅ MODEL IS WORKING WELL")
            print("  Minor tuning may improve performance")
        
        print("\n🚀 NEXT STEPS:")
        print("1. Address identified issues")
        print("2. Retest with improvements")
        print("3. Validate with real medical images")
        print("4. Optimize for production deployment")
        
    except Exception as e:
        print(f"❌ Diagnosis error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_model_issues()
