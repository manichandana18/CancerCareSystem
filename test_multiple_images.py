"""
Test script to validate the model with multiple images
Tests both cancer and normal images to verify the fix
"""
import requests
import sys
import os

def test_image(image_path, expected_type="unknown"):
    """Test a single image and return results"""
    url = "http://127.0.0.1:8000/predict"
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(url, files=files)
            
        if response.status_code == 200:
            result = response.json()
            prediction = result.get('prediction', 'N/A')
            confidence = result.get('confidence', 0)
            tumor_prob = result.get('probabilities', {}).get('tumor', 0)
            
            # Determine if prediction matches expectation
            is_correct = "unknown"
            if expected_type == "cancer":
                is_correct = "Tumor" in prediction or tumor_prob > 0.5
            elif expected_type == "normal":
                is_correct = "No Tumor" in prediction and tumor_prob < 0.5
            
            status = "[CORRECT]" if is_correct else "[WRONG]" if expected_type != "unknown" else "[?]"
            
            return {
                'path': os.path.basename(image_path),
                'expected': expected_type,
                'prediction': prediction,
                'tumor_prob': tumor_prob,
                'confidence': confidence,
                'correct': is_correct,
                'status': status
            }
        else:
            return {'error': f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {'error': str(e)}

def main():
    """Test multiple images"""
    print("="*70)
    print("BONE CANCER MODEL VALIDATION TEST")
    print("="*70)
    
    # Test images - add paths to your test images
    test_images = [
        # Cancer images (should detect as tumor)
        ("dataset/valid/tibia_osteosarcoma_18_PNG.rf.8356edeaa98cc538f5512fe6e4e7f61d.jpg", "cancer"),
        ("dataset/valid/pelvis_osteosarcoma_5_png.rf.7ed6d01bf41dbbd3d31357b3d3db0566.jpg", "cancer"),
        ("dataset/valid/bone-cancer_test_11_png.rf.6e0c97c1ff11d2ad679ba4e23903d337.jpg", "cancer"),
        
        # Normal images (should detect as no tumor)
        ("dataset/valid/image-no91-normal-_png.rf.7952cc8ecf509042a95503cd2cda8ede.jpg", "normal"),
        ("dataset/valid/image-no82-normal-_png.rf.2d7bd7371f4a666a938db042fc1cc503.jpg", "normal"),
        
        # Unknown (for testing)
        ("sample_xray.jpg", "unknown"),
    ]
    
    results = []
    for img_path, expected in test_images:
        if os.path.exists(img_path):
            print(f"\nTesting: {os.path.basename(img_path)} (Expected: {expected})")
            result = test_image(img_path, expected)
            results.append(result)
            
            if 'error' in result:
                print(f"  ERROR: {result['error']}")
            else:
                print(f"  Prediction: {result['prediction']}")
                print(f"  Tumor Probability: {result['tumor_prob']:.4f}")
                print(f"  Confidence: {result['confidence']:.2f}")
                print(f"  {result['status']}")
        else:
            print(f"\nSkipping (not found): {img_path}")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    cancer_tests = [r for r in results if r.get('expected') == 'cancer' and 'error' not in r]
    normal_tests = [r for r in results if r.get('expected') == 'normal' and 'error' not in r]
    
    if cancer_tests:
        cancer_correct = sum(1 for r in cancer_tests if r.get('correct'))
        print(f"Cancer Detection: {cancer_correct}/{len(cancer_tests)} correct")
        for r in cancer_tests:
            print(f"  - {r['path']}: Tumor prob={r['tumor_prob']:.4f} {r['status']}")
    
    if normal_tests:
        normal_correct = sum(1 for r in normal_tests if r.get('correct'))
        print(f"Normal Detection: {normal_correct}/{len(normal_tests)} correct")
        for r in normal_tests:
            print(f"  - {r['path']}: Tumor prob={r['tumor_prob']:.4f} {r['status']}")
    
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("ERROR: Backend server not running!")
        print("Start it with: cd backend && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
        sys.exit(1)

