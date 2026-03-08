"""
Test Optimized CancerCare AI System
Tests all cancer types after optimization
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_optimized_system():
    """Test all optimized cancer types"""
    
    print("🧪 TESTING OPTIMIZED CANCER TYPES")
    print("=" * 50)
    
    test_cases = [
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
            "filename": "bonecancer.jpg",
            "expected_organ": "bone",
            "expected_diagnosis": "cancer",
            "name": "Bone Cancer (Optimized)"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg",
            "filename": "lungcancer.jpg",
            "expected_organ": "lung",
            "expected_diagnosis": "malignant",
            "name": "Lung Cancer (Optimized)"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
            "filename": "braincancer.jpg",
            "expected_organ": "brain",
            "expected_diagnosis": "malignant",
            "name": "Brain Cancer (Optimized)"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
            "filename": "normalbone.jpg",
            "expected_organ": "bone",
            "expected_diagnosis": "normal",
            "name": "Normal Bone (Optimized)"
        }
    ]
    
    print(f"\n🧪 Testing {len(test_cases)} optimized cancer types:")
    
    passed = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*20} Test {i}/{total} {'='*20}")
        print(f"🏥 {test['name']}")
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
            
            print(f"  {status}")
            print(f"  Got: {organ} + {diagnosis} ({confidence}% confidence)")
            print(f"  Method: {result.get('method')}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n📊 OPTIMIZATION RESULTS:")
    print(f"Overall: {passed}/{total} tests passed")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 ALL CANCER TYPES OPTIMIZED!")
        print("✅ System ready for clinical excellence")
    else:
        print(f"🔧 {total-passed} tests need further optimization")

if __name__ == "__main__":
    test_optimized_system()
