"""
Final System Test - Complete validation of CancerCare AI
"""

import os
import sys
from pathlib import Path
import requests

# Add backend to path
sys.path.append(str(Path(__file__).parent))

def test_system_via_api():
    """Test the complete system via API calls"""
    
    print("🧪 FINAL SYSTEM VALIDATION")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
            "name": "Normal Bone X-ray",
            "expected_organ": "bone",
            "expected_diagnosis": "normal"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg", 
            "name": "Cancerous Bone X-ray",
            "expected_organ": "bone",
            "expected_diagnosis": "cancer"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\normalbone1.jpg",
            "name": "Normal Lung X-ray", 
            "expected_organ": "lung",
            "expected_diagnosis": "normal"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\cancer3.jpg",
            "name": "Cancerous Lung X-ray",
            "expected_organ": "lung", 
            "expected_diagnosis": "malignant"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg",
            "name": "Your Lung Cancer Image",
            "expected_organ": "lung",
            "expected_diagnosis": "malignant"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"Expected: {test_case['expected_organ']} + {test_case['expected_diagnosis']}")
        
        if not os.path.exists(test_case['path']):
            print("⏭️  Skipped - File not found")
            continue
            
        try:
            # Test via API
            with open(test_case['path'], 'rb') as f:
                files = {'file': (os.path.basename(test_case['path']), f, 'image/jpeg')}
                response = requests.post('http://localhost:8000/predict/auto', files=files)
            
            if response.status_code == 200:
                result = response.json()
                
                organ = result.get('organ', '').lower()
                diagnosis = result.get('diagnosis', '').lower()
                confidence = result.get('diagnosis_confidence_pct', 0)
                method = result.get('method', 'Unknown')
                
                # Check results
                organ_match = organ == test_case['expected_organ']
                diagnosis_match = test_case['expected_diagnosis'] in diagnosis
                
                status = '✅ PASS' if organ_match and diagnosis_match else '❌ FAIL'
                
                print(f"  {status}")
                print(f"  Got: {organ} + {diagnosis} ({confidence}% confidence)")
                print(f"  Method: {method}")
                
                results.append({
                    'test': test_case['name'],
                    'status': status,
                    'organ_match': organ_match,
                    'diagnosis_match': diagnosis_match,
                    'organ': organ,
                    'diagnosis': diagnosis,
                    'confidence': confidence
                })
                
            else:
                print(f"❌ API Error: {response.status_code}")
                results.append({
                    'test': test_case['name'],
                    'status': '❌ API ERROR',
                    'error': response.status_code
                })
                
        except Exception as e:
            print(f"❌ Test Error: {e}")
            results.append({
                'test': test_case['name'],
                'status': '❌ TEST ERROR',
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
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
    
    # Recommendations
    print("\n🎯 RECOMMENDATIONS:")
    if passed == total:
        print("🎉 EXCELLENT! All tests passed!")
        print("✅ System is ready for production use")
        print("🚀 Next: Add more cancer types or deploy")
    elif passed >= total * 0.8:
        print("🟡 GOOD! Most tests passed")
        print("🔧 Minor tuning needed")
        print("🚀 Next: Fine-tune detection sensitivity")
    else:
        print("🔴 NEEDS WORK")
        print("🔧 Major improvements needed")
        print("🚀 Next: Debug detection algorithms")
    
    return results

if __name__ == "__main__":
    test_system_via_api()
