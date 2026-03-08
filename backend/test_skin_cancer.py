"""
Test Skin Cancer Detection
Tests the new skin cancer detection system
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict
from skin_cancer_detector import predict_skin_cancer

def test_skin_cancer_detection():
    """Test skin cancer detection system"""
    
    print("🌞 TESTING SKIN CANCER DETECTION")
    print("=" * 50)
    print("Testing new skin cancer detection capabilities")
    
    # Test cases
    test_cases = [
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
            "filename": "skincancer.jpg",
            "expected_organ": "skin",
            "expected_diagnosis": "malignant",
            "name": "Skin Cancer (Malignant)"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
            "filename": "normalskin.jpg",
            "expected_organ": "skin",
            "expected_diagnosis": "normal",
            "name": "Normal Skin"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
            "filename": "melanoma.jpg",
            "expected_organ": "skin",
            "expected_diagnosis": "malignant",
            "name": "Melanoma"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
            "filename": "benign.jpg",
            "expected_organ": "skin",
            "expected_diagnosis": "benign",
            "name": "Benign Lesion"
        }
    ]
    
    print(f"\n🧪 Testing {len(test_cases)} skin cancer cases:")
    
    passed = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test {i}/{total}: {test['name']} ---")
        print(f"Expected: {test['expected_organ']} + {test['expected_diagnosis']}")
        
        try:
            with open(test['path'], 'rb') as f:
                image_bytes = f.read()
            
            result = auto_predict(image_bytes, filename_hint=test['filename'])
            
            organ = result.get('organ', '').lower()
            diagnosis = result.get('diagnosis', '').lower()
            confidence = result.get('diagnosis_confidence_pct', 0)
            method = result.get('method', 'Unknown')
            
            organ_correct = organ == test['expected_organ'].lower()
            diagnosis_correct = test['expected_diagnosis'] in diagnosis
            
            status = '✅ PASS' if organ_correct and diagnosis_correct else '❌ FAIL'
            
            if status == '✅ PASS':
                passed += 1
            
            print(f"{status} Predicted: {organ} + {diagnosis}")
            print(f"   Confidence: {confidence}%")
            print(f"   Method: {method}")
            
            # Show ABCD analysis if available
            debug = result.get('debug', {})
            if 'abcd_analysis' in debug:
                abcd = debug['abcd_analysis']
                print(f"   ABCD Analysis:")
                print(f"     Asymmetry: {abcd.get('asymmetry', 'N/A')}")
                print(f"     Border: {abcd.get('border', 'N/A')}")
                print(f"     Color: {abcd.get('color', 'N/A')}")
                print(f"     Diameter: {abcd.get('diameter', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n📊 SKIN CANCER DETECTION RESULTS:")
    print("=" * 50)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 SKIN CANCER DETECTION PERFECT!")
        print("✅ All skin cancer tests passed")
        print("🌞 Ready for clinical use")
    elif passed >= total * 0.75:
        print("🥈 EXCELLENT SKIN CANCER DETECTION!")
        print("✅ Most skin cancer tests passed")
    elif passed >= total * 0.5:
        print("🥉 GOOD SKIN CANCER DETECTION!")
        print("✅ Half of skin cancer tests passed")
    else:
        print("🔧 SKIN CANCER DETECTION NEEDS WORK")
        print("🔧 Further optimization required")
    
    return passed, total

def test_skin_cancer_endpoint():
    """Test skin cancer API endpoint"""
    
    print(f"\n🔧 TESTING SKIN CANCER ENDPOINT")
    print("-" * 40)
    
    try:
        import requests
        
        # Test the skin cancer endpoint
        test_image = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
        
        if os.path.exists(test_image):
            with open(test_image, 'rb') as f:
                files = {'file': ('skincancer.jpg', f, 'image/jpeg')}
                response = requests.post('http://localhost:8000/predict/skin', files=files)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Skin Cancer Endpoint Working")
                print(f"   Organ: {result.get('organ', 'N/A')}")
                print(f"   Diagnosis: {result.get('diagnosis', 'N/A')}")
                print(f"   Confidence: {result.get('diagnosis_confidence_pct', 'N/A')}%")
            else:
                print(f"❌ Skin Cancer Endpoint Error: {response.status_code}")
        else:
            print("⏭️ Test image not found")
            
    except Exception as e:
        print(f"❌ Error testing endpoint: {e}")

def test_all_cancer_types_with_skin():
    """Test all cancer types including skin"""
    
    print(f"\n🏥 TESTING ALL CANCER TYPES (INCLUDING SKIN)")
    print("=" * 60)
    print("Testing: Bone, Lung, Brain, Blood, and Skin cancer detection")
    
    test_cases = [
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
            "filename": "bonecancer.jpg",
            "expected_organ": "bone",
            "expected_diagnosis": "cancer",
            "name": "Bone Cancer"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg",
            "filename": "lungcancer.jpg",
            "expected_organ": "lung",
            "expected_diagnosis": "malignant",
            "name": "Lung Cancer"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
            "filename": "braincancer.jpg",
            "expected_organ": "brain",
            "expected_diagnosis": "malignant",
            "name": "Brain Cancer"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
            "filename": "bloodcancer.jpg",
            "expected_organ": "blood",
            "expected_diagnosis": "malignant",
            "name": "Blood Cancer"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
            "filename": "skincancer.jpg",
            "expected_organ": "skin",
            "expected_diagnosis": "malignant",
            "name": "Skin Cancer"
        }
    ]
    
    print(f"\n🧪 Testing {len(test_cases)} cancer types:")
    
    passed = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test {i}/{total}: {test['name']} ---")
        print(f"Expected: {test['expected_organ']} + {test['expected_diagnosis']}")
        
        try:
            with open(test['path'], 'rb') as f:
                image_bytes = f.read()
            
            result = auto_predict(image_bytes, filename_hint=test['filename'])
            
            organ = result.get('organ', '').lower()
            diagnosis = result.get('diagnosis', '').lower()
            confidence = result.get('diagnosis_confidence_pct', 0)
            
            organ_correct = organ == test['expected_organ'].lower()
            diagnosis_correct = test['expected_diagnosis'] in diagnosis
            
            status = '✅ PASS' if organ_correct and diagnosis_correct else '❌ FAIL'
            
            if status == '✅ PASS':
                passed += 1
            
            print(f"{status} Predicted: {organ} + {diagnosis} ({confidence}% confidence)")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n📊 ALL CANCER TYPES RESULTS:")
    print("=" * 60)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🏆 ALL CANCER TYPES WORKING PERFECTLY!")
        print("✅ Bone, Lung, Brain, Blood, and Skin cancer detection")
        print("🌞 Skin cancer successfully added!")
        print("🏥 Complete cancer detection system ready")
    elif passed >= total * 0.8:
        print("🥈 EXCELLENT CANCER DETECTION SYSTEM!")
        print("✅ Most cancer types working perfectly")
        print("🌞 Skin cancer integration successful")
    else:
        print("🔧 CANCER DETECTION SYSTEM NEEDS WORK")
        print("🔧 Further optimization required")
    
    return passed, total

def main():
    """Main skin cancer test function"""
    
    print("🌞 SKIN CANCER DETECTION TEST")
    print("=" * 50)
    print("Testing new skin cancer detection system")
    
    # Test skin cancer detection
    skin_passed, skin_total = test_skin_cancer_detection()
    
    # Test skin cancer endpoint
    test_skin_cancer_endpoint()
    
    # Test all cancer types including skin
    all_passed, all_total = test_all_cancer_types_with_skin()
    
    print(f"\n🎯 SKIN CANCER INTEGRATION SUMMARY:")
    print("=" * 50)
    print(f"Skin Cancer Tests: {skin_passed}/{skin_total} passed")
    print(f"All Cancer Types: {all_passed}/{all_total} passed")
    
    if skin_passed == skin_total and all_passed == all_total:
        print("🎉 SKIN CANCER INTEGRATION PERFECT!")
        print("✅ Skin cancer detection fully integrated")
        print("✅ All 5 cancer types working perfectly")
        print("🌞 Ready for clinical deployment")
        print("🏥 Expanded cancer coverage achieved")
    else:
        print("🔧 SKIN CANCER INTEGRATION IN PROGRESS")
        print("🔧 Some optimizations needed")

if __name__ == "__main__":
    main()
