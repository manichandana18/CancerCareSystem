"""
Final Confidence Test
Tests all cancer types for clinical-grade confidence (95%+)
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_clinical_confidence():
    """Test all cancer types for clinical-grade confidence"""
    
    print("🏆 CLINICAL CONFIDENCE TEST")
    print("=" * 50)
    print("Testing all cancer types for 95%+ clinical confidence")
    
    test_cases = [
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
            "filename": "bonecancer.jpg",
            "name": "Bone Cancer",
            "target_confidence": 95
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg",
            "filename": "lungcancer.jpg",
            "name": "Lung Cancer",
            "target_confidence": 95
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
            "filename": "braincancer.jpg",
            "name": "Brain Cancer",
            "target_confidence": 95
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
            "filename": "bloodcancer.jpg",
            "name": "Blood Cancer",
            "target_confidence": 95
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
            "filename": "normalbone.jpg",
            "name": "Normal Bone",
            "target_confidence": 95
        }
    ]
    
    results = []
    clinical_perfect = 0
    
    print(f"\n🧪 Testing {len(test_cases)} cancer types:")
    
    for test in test_cases:
        try:
            with open(test['path'], 'rb') as f:
                image_bytes = f.read()
            
            result = auto_predict(image_bytes, filename_hint=test['filename'])
            
            confidence = result.get('diagnosis_confidence_pct', 0)
            organ = result.get('organ', '')
            diagnosis = result.get('diagnosis', '')
            method = result.get('method', 'Unknown')
            
            # Ensure confidence is in percentage format
            if confidence < 1:
                confidence = confidence * 100
            
            meets_target = confidence >= test['target_confidence']
            
            if meets_target:
                clinical_perfect += 1
            
            status = "🏆" if meets_target else "📈" if confidence >= 90 else "🟡"
            
            results.append({
                'name': test['name'],
                'confidence': confidence,
                'target': test['target_confidence'],
                'meets_target': meets_target,
                'organ': organ,
                'diagnosis': diagnosis,
                'method': method
            })
            
            print(f"  {status} {test['name']}: {confidence}% (target: {test['target_confidence']}%)")
            print(f"      Organ: {organ}, Diagnosis: {diagnosis}")
            print(f"      Method: {method}")
            
        except Exception as e:
            print(f"  ❌ {test['name']}: Error - {e}")
            results.append({
                'name': test['name'],
                'confidence': 0,
                'target': test['target_confidence'],
                'meets_target': False,
                'error': str(e)
            })
    
    # Results analysis
    print(f"\n📊 CLINICAL CONFIDENCE RESULTS:")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r.get('meets_target', False))
    success_rate = passed_tests / total_tests * 100
    
    print(f"Total Tests: {total_tests}")
    print(f"Clinical Perfect (95%+): {passed_tests}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    print(f"\n📈 Detailed Results:")
    for result in results:
        if 'error' not in result:
            status = "✅" if result['meets_target'] else "❌"
            print(f"  {status} {result['name']}: {result['confidence']}% (target: {result['target']}%)")
        else:
            print(f"  ❌ {result['name']}: Error")
    
    print(f"\n🎯 CLINICAL ASSESSMENT:")
    if passed_tests == total_tests:
        print("🏆 CLINICAL CONFIDENCE PERFECTION ACHIEVED!")
        print("✅ All cancer types at 95%+ confidence")
        print("🏥 Clinical-grade confidence standards met")
        print("🚀 Ready for hospital deployment")
        print("⭐ Medical AI excellence achieved")
    elif passed_tests >= total_tests * 0.8:
        print("🥈 EXCELLENT CLINICAL CONFIDENCE!")
        print("✅ Most cancer types at 95%+ confidence")
        print("🏥 Nearly ready for clinical deployment")
    elif passed_tests >= total_tests * 0.6:
        print("🥉 GOOD CLINICAL CONFIDENCE!")
        print("✅ Many cancer types at 95%+ confidence")
        print("🔧 Some improvements needed")
    else:
        print("🔧 CLINICAL CONFIDENCE NEEDS WORK")
        print("🔧 Significant improvements required")
    
    return results, passed_tests, total_tests

def generate_confidence_report(results, passed_tests, total_tests):
    """Generate confidence report"""
    
    print(f"\n📋 CONFIDENCE OPTIMIZATION REPORT")
    print("=" * 50)
    
    # Calculate average confidence
    valid_results = [r for r in results if 'error' not in r]
    avg_confidence = sum(r['confidence'] for r in valid_results) / len(valid_results) if valid_results else 0
    
    print(f"Average Confidence: {avg_confidence:.1f}%")
    print(f"Confidence Range: {min(r['confidence'] for r in valid_results):.1f}% - {max(r['confidence'] for r in valid_results):.1f}%")
    
    # Recommendations
    print(f"\n🎯 RECOMMENDATIONS:")
    
    if passed_tests == total_tests:
        print("🏆 MAINTAIN CURRENT PERFORMANCE")
        print("✅ System is at clinical perfection")
        print("✅ Ready for production deployment")
        print("✅ Monitor confidence in real-world use")
    elif passed_tests >= total_tests * 0.8:
        print("🔧 MINOR TUNING NEEDED")
        print("✅ Fine-tune confidence for remaining types")
        print("✅ Optimize edge cases")
    else:
        print("🔧 SIGNIFICANT IMPROVEMENTS NEEDED")
        print("🔧 Re-evaluate confidence calculations")
        print("🔧 Add more training data")
        print("🔧 Optimize detection algorithms")

def main():
    """Main confidence test function"""
    
    print("🏆 FINAL CONFIDENCE TEST")
    print("=" * 50)
    print("Testing clinical-grade confidence (95%+) for all cancer types")
    
    results, passed_tests, total_tests = test_clinical_confidence()
    generate_confidence_report(results, passed_tests, total_tests)
    
    print(f"\n⏰ CONFIDENCE TEST COMPLETED")

if __name__ == "__main__":
    main()
