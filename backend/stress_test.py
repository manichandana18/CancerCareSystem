"""
Stress Testing for CancerCare AI System
Tests system under various conditions and edge cases
"""

import os
import sys
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json

# Add backend to path
sys.path.append(str(Path(__file__).parent))

class StressTester:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.test_image = "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg"
        
    def test_single_request(self, test_id):
        """Test a single API request"""
        try:
            start_time = time.time()
            with open(self.test_image, 'rb') as f:
                files = {'file': ('lungcancer1.jpg', f, 'image/jpeg')}
                response = requests.post(f"{self.backend_url}/predict/auto", files=files, timeout=30)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "test_id": test_id,
                    "status": "✅ SUCCESS",
                    "response_time": end_time - start_time,
                    "organ": result.get('organ'),
                    "diagnosis": result.get('diagnosis'),
                    "confidence": result.get('diagnosis_confidence_pct')
                }
            else:
                return {
                    "test_id": test_id,
                    "status": f"❌ HTTP {response.status_code}",
                    "response_time": end_time - start_time,
                    "error": response.text
                }
        except Exception as e:
            return {
                "test_id": test_id,
                "status": "❌ ERROR",
                "error": str(e)
            }
    
    def test_concurrent_requests(self, num_requests=10):
        """Test multiple concurrent requests"""
        print(f"🔄 Testing {num_requests} concurrent requests...")
        
        start_time = time.time()
        results = []
        
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(self.test_single_request, i) for i in range(num_requests)]
            
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                print(f"  Request {result['test_id']}: {result['status']}")
        
        end_time = time.time()
        
        # Analyze results
        successful = sum(1 for r in results if "SUCCESS" in r['status'])
        failed = len(results) - successful
        
        response_times = [r['response_time'] for r in results if 'response_time' in r]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        print(f"\n📊 Concurrent Test Results:")
        print(f"  Total Requests: {num_requests}")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        print(f"  Success Rate: {successful/num_requests*100:.1f}%")
        print(f"  Average Response Time: {avg_response_time:.2f}s")
        print(f"  Total Time: {end_time - start_time:.2f}s")
        
        return results
    
    def test_sequential_requests(self, num_requests=20):
        """Test sequential requests"""
        print(f"🔄 Testing {num_requests} sequential requests...")
        
        results = []
        start_time = time.time()
        
        for i in range(num_requests):
            result = self.test_single_request(i)
            results.append(result)
            print(f"  Request {i+1}/{num_requests}: {result['status']}")
            time.sleep(0.1)  # Small delay between requests
        
        end_time = time.time()
        
        # Analyze results
        successful = sum(1 for r in results if "SUCCESS" in r['status'])
        failed = len(results) - successful
        
        response_times = [r['response_time'] for r in results if 'response_time' in r]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        print(f"\n📊 Sequential Test Results:")
        print(f"  Total Requests: {num_requests}")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        print(f"  Success Rate: {successful/num_requests*100:.1f}%")
        print(f"  Average Response Time: {avg_response_time:.2f}s")
        print(f"  Total Time: {end_time - start_time:.2f}s")
        
        return results
    
    def test_different_images(self):
        """Test with different image types"""
        print("🔄 Testing with different image types...")
        
        test_images = [
            ("C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg", "bone", "normal"),
            ("C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg", "bone", "cancer"),
            ("C:\\Users\\Balaiah goud\\Downloads\\normalbone1.jpg", "lung", "normal"),
            ("C:\\Users\\Balaiah goud\\Downloads\\cancer3.jpg", "lung", "malignant"),
            ("C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg", "lung", "malignant")
        ]
        
        results = []
        
        for image_path, expected_organ, expected_diagnosis in test_images:
            if not os.path.exists(image_path):
                print(f"  ⏭️ Skipping {os.path.basename(image_path)} - file not found")
                continue
            
            try:
                start_time = time.time()
                with open(image_path, 'rb') as f:
                    files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
                    response = requests.post(f"{self.backend_url}/predict/auto", files=files, timeout=30)
                end_time = time.time()
                
                if response.status_code == 200:
                    result = response.json()
                    organ = result.get('organ', '').lower()
                    diagnosis = result.get('diagnosis', '').lower()
                    
                    organ_match = organ == expected_organ.lower()
                    diagnosis_match = expected_diagnosis.lower() in diagnosis
                    
                    status = "✅ PASS" if organ_match and diagnosis_match else "❌ FAIL"
                    
                    results.append({
                        "image": os.path.basename(image_path),
                        "status": status,
                        "expected": f"{expected_organ} + {expected_diagnosis}",
                        "got": f"{organ} + {diagnosis}",
                        "response_time": end_time - start_time
                    })
                    
                    print(f"  {os.path.basename(image_path)}: {status}")
                else:
                    print(f"  {os.path.basename(image_path)}: ❌ HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  {os.path.basename(image_path)}: ❌ ERROR - {e}")
        
        return results
    
    def run_stress_tests(self):
        """Run all stress tests"""
        print("🔥 STRESS TESTING FOR CANCERCARE AI")
        print("=" * 50)
        
        if not os.path.exists(self.test_image):
            print(f"❌ Test image not found: {self.test_image}")
            return
        
        # Test 1: Sequential requests
        print("\n" + "="*30 + " TEST 1: SEQUENTIAL " + "="*30)
        sequential_results = self.test_sequential_requests(10)
        
        # Test 2: Concurrent requests
        print("\n" + "="*30 + " TEST 2: CONCURRENT " + "="*30)
        concurrent_results = self.test_concurrent_requests(5)
        
        # Test 3: Different images
        print("\n" + "="*30 + " TEST 3: DIFFERENT IMAGES " + "="*30)
        image_results = self.test_different_images()
        
        # Summary
        print("\n" + "="*50)
        print("📊 STRESS TEST SUMMARY")
        print("="*50)
        
        sequential_success = sum(1 for r in sequential_results if "SUCCESS" in r['status'])
        concurrent_success = sum(1 for r in concurrent_results if "SUCCESS" in r['status'])
        image_success = sum(1 for r in image_results if "PASS" in r['status'])
        
        print(f"Sequential Requests: {sequential_success}/{len(sequential_results)} successful")
        print(f"Concurrent Requests: {concurrent_success}/{len(concurrent_results)} successful")
        print(f"Different Images: {image_success}/{len(image_results)} successful")
        
        overall_score = (sequential_success + concurrent_success + image_success) / (len(sequential_results) + len(concurrent_results) + len(image_results)) * 100
        
        print(f"\n🎯 Overall Stress Test Score: {overall_score:.1f}%")
        
        if overall_score >= 90:
            print("🎉 EXCELLENT! System handles stress very well")
        elif overall_score >= 75:
            print("🟡 GOOD! System handles stress reasonably well")
        else:
            print("🔴 NEEDS IMPROVEMENT! System struggles under stress")

def main():
    """Main stress testing function"""
    tester = StressTester()
    
    # Check if backend is running
    try:
        response = requests.get(f"{tester.backend_url}/", timeout=5)
        if response.status_code != 200:
            print("❌ Backend is not responding correctly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("🚀 Please start the backend first")
        return
    
    print("✅ Backend is running - Starting stress tests...")
    tester.run_stress_tests()

if __name__ == "__main__":
    main()
