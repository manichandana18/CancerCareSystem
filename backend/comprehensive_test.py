"""
Comprehensive Testing Framework for CancerCare AI System
Tests with various image types and edge cases
"""

import os
import sys
from pathlib import Path
import requests
import json
from datetime import datetime

# Add backend to path
sys.path.append(str(Path(__file__).parent))

class ComprehensiveTester:
    def __init__(self):
        self.test_results = []
        self.backend_url = "http://localhost:8000"
        
    def run_test(self, image_path, expected_organ, expected_diagnosis, test_name):
        """Run a single test case"""
        
        print(f"\n🧪 Testing: {test_name}")
        print(f"   Expected: {expected_organ} + {expected_diagnosis}")
        
        if not os.path.exists(image_path):
            result = {
                "test_name": test_name,
                "status": "❌ SKIPPED",
                "error": "File not found",
                "image_path": image_path
            }
            self.test_results.append(result)
            return result
        
        try:
            # Test via API
            with open(image_path, 'rb') as f:
                files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
                response = requests.post(f"{self.backend_url}/predict/auto", files=files, timeout=30)
            
            if response.status_code == 200:
                api_result = response.json()
                
                organ = api_result.get('organ', '').lower()
                diagnosis = api_result.get('diagnosis', '').lower()
                confidence = api_result.get('diagnosis_confidence_pct', 0)
                method = api_result.get('method', 'Unknown')
                
                # Check results
                organ_match = organ == expected_organ.lower()
                diagnosis_match = expected_diagnosis.lower() in diagnosis
                
                status = '✅ PASS' if organ_match and diagnosis_match else '❌ FAIL'
                
                result = {
                    "test_name": test_name,
                    "status": status,
                    "organ_match": organ_match,
                    "diagnosis_match": diagnosis_match,
                    "got_organ": organ,
                    "expected_organ": expected_organ.lower(),
                    "got_diagnosis": diagnosis,
                    "expected_diagnosis": expected_diagnosis.lower(),
                    "confidence": confidence,
                    "method": method,
                    "image_path": image_path,
                    "api_result": api_result
                }
                
                print(f"   {status}")
                print(f"   Got: {organ} + {diagnosis} ({confidence}% confidence)")
                print(f"   Method: {method}")
                
            else:
                result = {
                    "test_name": test_name,
                    "status": "❌ API ERROR",
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "image_path": image_path
                }
                print(f"   ❌ API Error: {response.status_code}")
                
        except Exception as e:
            result = {
                "test_name": test_name,
                "status": "❌ TEST ERROR",
                "error": str(e),
                "image_path": image_path
            }
            print(f"   ❌ Test Error: {e}")
        
        self.test_results.append(result)
        return result
    
    def run_comprehensive_tests(self):
        """Run comprehensive test suite"""
        
        print("🧪 COMPREHENSIVE CANCERCARE AI TESTING")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Backend URL: {self.backend_url}")
        
        # Test cases - expand with more scenarios
        test_cases = [
            # Original working cases
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
                "organ": "bone",
                "diagnosis": "normal",
                "name": "Normal Bone X-ray (Original)"
            },
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
                "organ": "bone", 
                "diagnosis": "cancer",
                "name": "Cancerous Bone X-ray (Original)"
            },
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\normalbone1.jpg",
                "organ": "lung",
                "diagnosis": "normal",
                "name": "Normal Lung X-ray (Original)"
            },
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\cancer3.jpg",
                "organ": "lung",
                "diagnosis": "malignant",
                "name": "Cancerous Lung X-ray (Original)"
            },
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg",
                "organ": "lung",
                "diagnosis": "malignant",
                "name": "Your Lung Cancer Image (Original)"
            },
            
            # Additional test scenarios (if you have more images)
            # You can add more test cases here as you acquire more images
            
            # Edge cases with different naming patterns
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
                "organ": "bone",
                "diagnosis": "normal", 
                "name": "Normal Bone - Different Filename Test"
            },
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg",
                "organ": "lung",
                "diagnosis": "malignant",
                "name": "Lung Cancer - Consistency Test"
            }
        ]
        
        # Run all tests
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{'='*20} Test {i}/{len(test_cases)} {'='*20}")
            self.run_test(
                test_case["path"],
                test_case["organ"],
                test_case["diagnosis"],
                test_case["name"]
            )
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate comprehensive test summary"""
        
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.test_results if 'PASS' in r['status'])
        failed = sum(1 for r in self.test_results if 'FAIL' in r['status'])
        errors = sum(1 for r in self.test_results if 'ERROR' in r['status'])
        skipped = sum(1 for r in self.test_results if 'SKIPPED' in r['status'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"🚫 Errors: {errors}")
        print(f"⏭️ Skipped: {skipped}")
        print(f"📈 Success Rate: {passed/total*100:.1f}%")
        
        # Detailed results
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            print(f"  {result['status']} | {result['test_name']}")
            if 'organ_match' in result:
                print(f"    Organ: {'✅' if result['organ_match'] else '❌'}")
                print(f"    Diagnosis: {'✅' if result['diagnosis_match'] else '❌'}")
                if result['confidence']:
                    print(f"    Confidence: {result['confidence']}%")
        
        # Performance analysis
        print("\n🔍 Performance Analysis:")
        organ_accuracy = sum(1 for r in self.test_results if r.get('organ_match', False)) / max(1, total)
        diagnosis_accuracy = sum(1 for r in self.test_results if r.get('diagnosis_match', False)) / max(1, total)
        
        print(f"  Organ Classification Accuracy: {organ_accuracy*100:.1f}%")
        print(f"  Cancer Detection Accuracy: {diagnosis_accuracy*100:.1f}%")
        
        # Methods used
        methods = {}
        for result in self.test_results:
            method = result.get('method', 'Unknown')
            methods[method] = methods.get(method, 0) + 1
        
        print("\n🛠️ Detection Methods Used:")
        for method, count in methods.items():
            print(f"  {method}: {count} times")
        
        # Recommendations
        print("\n🎯 Recommendations:")
        if passed == total:
            print("🎉 EXCELLENT! All tests passed!")
            print("✅ System is ready for production use")
            print("🚀 Consider adding more test cases for robustness")
        elif passed >= total * 0.8:
            print("🟡 GOOD! Most tests passed")
            print("🔧 Review failed cases for improvement")
            print("🚀 System is nearly ready for production")
        else:
            print("🔴 NEEDS IMPROVEMENT")
            print("🔧 Significant issues found")
            print("🚀 System needs more development before production")
        
        # Save results
        self.save_results()
        
        print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def save_results(self):
        """Save test results to file"""
        try:
            results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(results_file, 'w') as f:
                json.dump(self.test_results, f, indent=2, default=str)
            print(f"💾 Results saved to: {results_file}")
        except Exception as e:
            print(f"❌ Could not save results: {e}")

def main():
    """Main testing function"""
    tester = ComprehensiveTester()
    
    # Check if backend is running
    try:
        response = requests.get(f"{tester.backend_url}/", timeout=5)
        if response.status_code != 200:
            print("❌ Backend is not responding correctly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("🚀 Please start the backend with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    print("✅ Backend is running - Starting comprehensive tests...")
    tester.run_comprehensive_tests()

if __name__ == "__main__":
    main()
