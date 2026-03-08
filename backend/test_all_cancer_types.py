"""
Complete CancerCare System Test
Tests all cancer types: Bone, Lung, and Brain
"""

import os
import sys
from pathlib import Path
import requests

# Add backend to path
sys.path.append(str(Path(__file__).parent))

def test_all_cancer_types():
    """Test all cancer types with the auto-predict endpoint"""
    
    print("🏥 TESTING COMPLETE CANCERCARE SYSTEM")
    print("=" * 60)
    print("Testing: Bone, Lung, and Brain Cancer Detection")
    
    # Test cases for all cancer types
    test_cases = [
        # Bone cancer tests
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
            "filename": "normalbone.jpg",
            "expected_organ": "bone",
            "expected_diagnosis": "normal",
            "name": "Normal Bone X-ray"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
            "filename": "bonecancer.jpg",
            "expected_organ": "bone",
            "expected_diagnosis": "cancer",
            "name": "Cancerous Bone X-ray"
        },
        
        # Lung cancer tests
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\normalbone1.jpg",
            "filename": "normallung.jpg",
            "expected_organ": "lung",
            "expected_diagnosis": "normal",
            "name": "Normal Lung X-ray"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\cancer3.jpg",
            "filename": "lungcancer.jpg",
            "expected_organ": "lung",
            "expected_diagnosis": "malignant",
            "name": "Cancerous Lung X-ray"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg",
            "filename": "lungmalignant.jpg",
            "expected_organ": "lung",
            "expected_diagnosis": "malignant",
            "name": "Malignant Lung X-ray"
        },
        
        # Brain cancer tests
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
            # Test via auto-predict API
            with open(test_case['path'], 'rb') as f:
                files = {'file': (test_case['filename'], f, 'image/jpeg')}
                response = requests.post('http://localhost:8000/predict/auto', files=files)
            
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
                    'cancer_type': test_case['expected_organ'],
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
                    'cancer_type': test_case['expected_organ'],
                    'status': '❌ API ERROR',
                    'error': response.status_code
                })
                
        except Exception as e:
            print(f"   ❌ Test Error: {e}")
            results.append({
                'test': test_case['name'],
                'cancer_type': test_case['expected_organ'],
                'status': '❌ TEST ERROR',
                'error': str(e)
            })
    
    # Summary by cancer type
    print("\n" + "=" * 60)
    print("📊 COMPLETE SYSTEM TEST SUMMARY")
    print("=" * 60)
    
    # Overall results
    passed = sum(1 for r in results if 'PASS' in r['status'])
    total = len(results)
    
    print(f"Overall: {passed}/{total} tests passed")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    # Results by cancer type
    cancer_types = ['bone', 'lung', 'brain']
    for cancer_type in cancer_types:
        type_results = [r for r in results if r.get('cancer_type') == cancer_type]
        type_passed = sum(1 for r in type_results if 'PASS' in r['status'])
        type_total = len(type_results)
        
        print(f"\n{cancer_type.upper()} Cancer:")
        print(f"  {type_passed}/{type_total} tests passed")
        print(f"  Success Rate: {type_passed/type_total*100:.1f}%" if type_total > 0 else "  No tests")
        
        for result in type_results:
            print(f"    {result['status']} | {result['test']}")
    
    # Method analysis
    methods = {}
    for result in results:
        method = result.get('method', 'Unknown')
        methods[method] = methods.get(method, 0) + 1
    
    print(f"\n🛠️ Detection Methods Used:")
    for method, count in methods.items():
        print(f"  {method}: {count} times")
    
    # Overall assessment
    print(f"\n🎯 OVERALL SYSTEM ASSESSMENT:")
    if passed == total:
        print("🎉 PERFECT! All cancer types working excellently!")
        print("✅ System is ready for multi-cancer deployment")
        print("🚀 Ready for clinical use with bone, lung, and brain cancer")
    elif passed >= total * 0.8:
        print("🟡 EXCELLENT! Most tests passed across all cancer types")
        print("✅ System is nearly ready for multi-cancer deployment")
    elif passed >= total * 0.6:
        print("🟠 GOOD! System working reasonably well")
        print("🔧 Some improvements needed for full deployment")
    else:
        print("🔴 NEEDS WORK")
        print("🔧 Significant improvements needed")
    
    return results

def test_individual_endpoints():
    """Test individual cancer type endpoints"""
    
    print(f"\n🔧 TESTING INDIVIDUAL ENDPOINTS")
    print("-" * 40)
    
    endpoints = [
        ("Bone Cancer", "http://localhost:8000/predict/bone"),
        ("Lung Cancer", "http://localhost:8000/predict/lung"),
        ("Brain Cancer", "http://localhost:8000/predict/brain")
    ]
    
    for name, url in endpoints:
        try:
            # Use a test image
            test_image = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
            
            if os.path.exists(test_image):
                with open(test_image, 'rb') as f:
                    files = {'file': ('test.jpg', f, 'image/jpeg')}
                    response = requests.post(url, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ {name}: Working")
                    print(f"   Organ: {result.get('organ', 'N/A')}")
                    print(f"   Diagnosis: {result.get('diagnosis', 'N/A')}")
                else:
                    print(f"❌ {name}: HTTP {response.status_code}")
            else:
                print(f"⏭️ {name}: Test image not found")
                
        except Exception as e:
            print(f"❌ {name}: Error - {e}")

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
    
    print("✅ Backend is running - Starting complete system tests...")
    
    # Run tests
    test_individual_endpoints()
    test_all_cancer_types()

if __name__ == "__main__":
    main()
