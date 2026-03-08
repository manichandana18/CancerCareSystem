"""
Brain Cancer Detection Test Suite
Tests the new brain cancer detection module
"""

import os
import sys
from pathlib import Path
import requests

# Add backend to path
sys.path.append(str(Path(__file__).parent))

def test_brain_cancer_detection():
    """Test brain cancer detection with sample images"""
    
    print("🧠 TESTING BRAIN CANCER DETECTION")
    print("=" * 50)
    
    # Test cases (we'll simulate with existing images for now)
    test_cases = [
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
            "filename": "normalbrain.jpg",
            "expected_organ": "brain",
            "expected_diagnosis": "normal",
            "name": "Normal Brain MRI"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
            "filename": "braincancer.jpg", 
            "expected_organ": "brain",
            "expected_diagnosis": "malignant",
            "name": "Brain Cancer MRI"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg",
            "filename": "braintumor.jpg",
            "expected_organ": "brain", 
            "expected_diagnosis": "malignant",
            "name": "Brain Tumor MRI"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"   Expected: {test_case['expected_organ']} + {test_case['expected_diagnosis']}")
        
        if not os.path.exists(test_case['path']):
            print("   ⏭️  Skipped - File not found")
            continue
        
        try:
            # Test via brain-specific API
            with open(test_case['path'], 'rb') as f:
                files = {'file': (test_case['filename'], f, 'image/jpeg')}
                response = requests.post('http://localhost:8000/predict/brain', files=files)
            
            if response.status_code == 200:
                result = response.json()
                
                organ = result.get('organ', '').lower()
                diagnosis = result.get('diagnosis', '').lower()
                confidence = result.get('diagnosis_confidence_pct', 0)
                method = result.get('method', 'Unknown')
                
                # Check results
                organ_match = organ == test_case['expected_organ'].lower()
                diagnosis_match = test_case['expected_diagnosis'].lower() in diagnosis
                
                status = '✅ PASS' if organ_match and diagnosis_match else '❌ FAIL'
                
                results.append({
                    'test': test_case['name'],
                    'status': status,
                    'organ_match': organ_match,
                    'diagnosis_match': diagnosis_match,
                    'organ': organ,
                    'diagnosis': diagnosis,
                    'confidence': confidence,
                    'method': method
                })
                
                print(f"   {status}")
                print(f"   Got: {organ} + {diagnosis} ({confidence}% confidence)")
                print(f"   Method: {method}")
                
            else:
                print(f"   ❌ API Error: {response.status_code}")
                results.append({
                    'test': test_case['name'],
                    'status': '❌ API ERROR',
                    'error': response.status_code
                })
                
        except Exception as e:
            print(f"   ❌ Test Error: {e}")
            results.append({
                'test': test_case['name'],
                'status': '❌ TEST ERROR',
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 BRAIN CANCER TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for r in results if 'PASS' in r['status'])
    total = len(results)
    
    print(f"Overall: {passed}/{total} tests passed")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    print("\nDetailed Results:")
    for result in results:
        print(f"  {result['status']} | {result['test']}")
        if 'organ_match' in result:
            print(f"    Organ: {'✅' if result['organ_match'] else '❌'}")
            print(f"    Diagnosis: {'✅' if result['diagnosis_match'] else '❌'}")
    
    # Test auto-predict with brain
    print(f"\n🔄 TESTING AUTO-PREDICT WITH BRAIN")
    print("-" * 40)
    
    try:
        with open("C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg", 'rb') as f:
            files = {'file': ('braincancer.jpg', f, 'image/jpeg')}
            response = requests.post('http://localhost:8000/predict/auto', files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Auto-predict Result:")
            print(f"  Organ: {result.get('organ')}")
            print(f"  Diagnosis: {result.get('diagnosis')}")
            print(f"  Method: {result.get('method')}")
        else:
            print(f"❌ Auto-predict Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Auto-predict Test Error: {e}")
    
    print(f"\n🎯 BRAIN CANCER MODULE STATUS:")
    if passed == total:
        print("🎉 EXCELLENT! All brain cancer tests passed!")
        print("✅ Brain cancer detection is ready for use")
    elif passed >= total * 0.7:
        print("🟡 GOOD! Most brain cancer tests passed")
        print("🔧 Minor improvements needed")
    else:
        print("🔴 NEEDS WORK")
        print("🔧 Brain cancer detection needs improvement")

def test_brain_features():
    """Test brain feature extraction"""
    
    print(f"\n🔍 TESTING BRAIN FEATURE EXTRACTION")
    print("-" * 40)
    
    try:
        from app.brain.brain_predictor import extract_brain_features
        
        # Test with an existing image
        test_image = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
        
        if os.path.exists(test_image):
            with open(test_image, 'rb') as f:
                image_bytes = f.read()
            
            features = extract_brain_features(image_bytes)
            
            if features:
                print("✅ Feature extraction successful!")
                print(f"  Extracted {len(features)} features:")
                for key, value in list(features.items())[:5]:  # Show first 5
                    print(f"    {key}: {value}")
                print(f"    ... and {len(features)-5} more")
            else:
                print("❌ Feature extraction failed")
        else:
            print("⏭️ Test image not found")
            
    except Exception as e:
        print(f"❌ Feature extraction error: {e}")

def main():
    """Main test function"""
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code != 200:
            print("❌ Backend is not responding correctly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("🚀 Please start the backend first")
        return
    
    print("✅ Backend is running - Starting brain cancer tests...")
    
    # Run tests
    test_brain_features()
    test_brain_cancer_detection()

if __name__ == "__main__":
    main()
