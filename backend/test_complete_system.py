"""
Complete System Test - Test all scenarios
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_complete_system():
    """Test the complete system with different scenarios"""
    
    print("🧪 COMPLETE SYSTEM TEST")
    print("=" * 50)
    
    # Test scenarios
    test_cases = [
        {
            "name": "Normal Bone X-ray",
            "expected_organ": "bone",
            "expected_diagnosis": "normal"
        },
        {
            "name": "Cancerous Bone X-ray", 
            "expected_organ": "bone",
            "expected_diagnosis": "cancer"
        },
        {
            "name": "Normal Lung X-ray",
            "expected_organ": "lung", 
            "expected_diagnosis": "normal"
        },
        {
            "name": "Cancerous Lung X-ray",
            "expected_organ": "lung",
            "expected_diagnosis": "malignant"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"Expected: Organ={test_case['expected_organ']}, Diagnosis={test_case['expected_diagnosis']}")
        
        image_path = input(f"Enter path to {test_case['name']} image (or press Enter to skip): ").strip().strip('"')
        
        if not image_path:
            print("⏭️  Skipped")
            continue
            
        if not os.path.exists(image_path):
            print(f"❌ File not found: {image_path}")
            continue
            
        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            
            result = auto_predict(image_bytes)
            
            print(f"🎯 Results:")
            print(f"   Organ: {result.get('organ')} (confidence: {result.get('organ_confidence_pct')}%)")
            print(f"   Diagnosis: {result.get('diagnosis')} (confidence: {result.get('diagnosis_confidence_pct')}%)")
            print(f"   Method: {result.get('method')}")
            
            # Check if results match expectations
            organ_match = result.get('organ', '').lower() == test_case['expected_organ']
            diagnosis_match = test_case['expected_diagnosis'] in result.get('diagnosis', '').lower()
            
            if organ_match and diagnosis_match:
                print("   ✅ PASS - Results match expectations!")
            else:
                print("   ❌ FAIL - Results don't match expectations")
                if not organ_match:
                    print(f"      Organ mismatch: expected {test_case['expected_organ']}, got {result.get('organ')}")
                if not diagnosis_match:
                    print(f"      Diagnosis mismatch: expected {test_case['expected_diagnosis']}, got {result.get('diagnosis')}")
            
            # Show debug info if available
            if 'debug' in result:
                print(f"   🔍 Debug: {result['debug']}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 TEST COMPLETE!")
    print("\n📊 Summary:")
    print("- Smart Organ Classifier should properly detect bone vs lung")
    print("- Improved Cancer Detectors should be more sensitive to cancer")
    print("- No more forced corrections - everything is based on actual image analysis")

if __name__ == "__main__":
    test_complete_system()
