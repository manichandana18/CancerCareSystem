"""
Advanced Clinical Stress Test
Tests system under high-volume clinical scenarios
"""

import os
import sys
from pathlib import Path
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import random

# Add backend to path
sys.path.append(str(Path(__file__).parent))

class ClinicalStressTester:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.test_images = [
            "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
            "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
            "C:\\Users\\Balaiah goud\\Downloads\\normalbone1.jpg",
            "C:\\Users\\Balaiah goud\\Downloads\\cancer3.jpg",
            "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg"
        ]
        
    def simulate_emergency_room_load(self, num_patients=20):
        """Simulate high-volume emergency room scenario"""
        
        print(f"🚑 SIMULATING EMERGENCY ROOM LOAD")
        print(f"Processing {num_patients} emergency patients...")
        
        results = []
        start_time = time.time()
        
        def process_er_patient(patient_id):
            """Process a single ER patient"""
            try:
                # Simulate different emergency cases
                case_types = [
                    ("ER_trauma", "bonecancer.jpg", "high"),
                    ("ER_chest_pain", "lungcancer1.jpg", "high"),
                    ("ER_head_injury", "bone3.jpg", "critical"),
                    ("ER_abdominal_pain", "normalbone1.jpg", "medium"),
                    ("ER_neuro_emergency", "cancer3.jpg", "critical")
                ]
                
                case_type, filename, urgency = random.choice(case_types)
                
                process_start = time.time()
                with open(random.choice([img for img in self.test_images if os.path.exists(img)]), 'rb') as f:
                    files = {'file': (f'ER_{patient_id}_{filename}', f, 'image/jpeg')}
                    response = requests.post(f"{self.backend_url}/predict/auto", files=files, timeout=15)
                process_time = time.time() - process_start
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "patient_id": patient_id,
                        "case_type": case_type,
                        "urgency": urgency,
                        "organ": result.get('organ'),
                        "diagnosis": result.get('diagnosis'),
                        "confidence": result.get('diagnosis_confidence_pct'),
                        "process_time": process_time,
                        "status": "✅ SUCCESS"
                    }
                else:
                    return {
                        "patient_id": patient_id,
                        "case_type": case_type,
                        "urgency": urgency,
                        "status": f"❌ ERROR {response.status_code}",
                        "process_time": process_time
                    }
                    
            except Exception as e:
                return {
                    "patient_id": patient_id,
                    "status": f"❌ EXCEPTION {str(e)}",
                    "process_time": 0
                }
        
        # Process patients concurrently (simulating real ER)
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_er_patient, i) for i in range(1, num_patients + 1)]
            
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                urgency = result.get('urgency', 'unknown')
                print(f"  Patient {result['patient_id']}: {result['status']} ({urgency} urgency)")
        
        total_time = time.time() - start_time
        
        # Analyze ER performance
        successful = sum(1 for r in results if "SUCCESS" in r['status'])
        avg_process_time = sum(r.get('process_time', 0) for r in results) / len(results) if results else 0
        
        print(f"\n📊 EMERGENCY ROOM PERFORMANCE:")
        print(f"  Total Patients: {num_patients}")
        print(f"  Successful: {successful}")
        print(f"  Success Rate: {successful/num_patients*100:.1f}%")
        print(f"  Average Process Time: {avg_process_time:.2f}s")
        print(f"  Total ER Time: {total_time:.1f}s")
        print(f"  Patients per Hour: {num_patients/total_time*3600:.1f}")
        
        # Urgency analysis
        urgency_stats = {}
        for result in results:
            urgency = result.get('urgency', 'unknown')
            if urgency not in urgency_stats:
                urgency_stats[urgency] = {'total': 0, 'success': 0}
            urgency_stats[urgency]['total'] += 1
            if "SUCCESS" in result['status']:
                urgency_stats[urgency]['success'] += 1
        
        print(f"\n⚡ URGENCY PERFORMANCE:")
        for urgency, stats in urgency_stats.items():
            success_rate = stats['success'] / stats['total'] * 100 if stats['total'] > 0 else 0
            print(f"  {urgency.capitalize()}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        return results
    
    def simulate_clinical_workflow(self, num_cases=30):
        """Simulate normal clinical workflow over time"""
        
        print(f"\n🏥 SIMULATING CLINICAL WORKFLOW")
        print(f"Processing {num_cases} routine clinical cases...")
        
        results = []
        start_time = time.time()
        
        for i in range(1, num_cases + 1):
            # Simulate different clinical scenarios
            scenarios = [
                ("routine_checkup", "bone3.jpg", "routine"),
                ("screening_test", "normalbone1.jpg", "routine"),
                ("follow_up", "cancer3.jpg", "medium"),
                ("second_opinion", "bonecancer.jpg", "medium"),
                ("specialist_referral", "lungcancer1.jpg", "medium")
            ]
            
            scenario, filename, priority = random.choice(scenarios)
            
            try:
                case_start = time.time()
                with open(random.choice([img for img in self.test_images if os.path.exists(img)]), 'rb') as f:
                    files = {'file': (f'clinic_{i}_{filename}', f, 'image/jpeg')}
                    response = requests.post(f"{self.backend_url}/predict/auto", files=files, timeout=30)
                case_time = time.time() - case_start
                
                if response.status_code == 200:
                    result = response.json()
                    results.append({
                        "case_id": i,
                        "scenario": scenario,
                        "priority": priority,
                        "organ": result.get('organ'),
                        "diagnosis": result.get('diagnosis'),
                        "confidence": result.get('diagnosis_confidence_pct'),
                        "case_time": case_time,
                        "status": "✅ SUCCESS"
                    })
                    print(f"  Case {i}: {scenario} - {result.get('organ')} ({result.get('diagnosis')})")
                else:
                    print(f"  Case {i}: ❌ API Error {response.status_code}")
                    
            except Exception as e:
                print(f"  Case {i}: ❌ Error - {e}")
            
            # Simulate time between cases (clinic workflow)
            time.sleep(random.uniform(0.1, 0.3))
        
        total_time = time.time() - start_time
        
        # Analyze workflow performance
        successful = sum(1 for r in results if "SUCCESS" in r['status'])
        avg_case_time = sum(r.get('case_time', 0) for r in results) / len(results) if results else 0
        
        print(f"\n📊 CLINICAL WORKFLOW PERFORMANCE:")
        print(f"  Total Cases: {num_cases}")
        print(f"  Successful: {successful}")
        print(f"  Success Rate: {successful/num_cases*100:.1f}%")
        print(f"  Average Case Time: {avg_case_time:.2f}s")
        print(f"  Total Workflow Time: {total_time:.1f}s")
        print(f"  Cases per Hour: {num_cases/total_time*3600:.1f}")
        
        return results
    
    def simulate_peak_load(self, duration_seconds=60):
        """Simulate peak load scenario for specified duration"""
        
        print(f"\n🔥 SIMULATING PEAK LOAD TEST")
        print(f"High-volume requests for {duration_seconds} seconds...")
        
        results = []
        start_time = time.time()
        request_count = 0
        
        def send_request():
            nonlocal request_count
            request_count += 1
            
            try:
                with open(random.choice([img for img in self.test_images if os.path.exists(img)]), 'rb') as f:
                    files = {'file': (f'peak_{request_count}.jpg', f, 'image/jpeg')}
                    response = requests.post(f"{self.backend_url}/predict/auto", files=files, timeout=10)
                
                return {
                    "request_id": request_count,
                    "status": "✅ SUCCESS" if response.status_code == 200 else f"❌ ERROR {response.status_code}",
                    "timestamp": time.time() - start_time
                }
            except Exception as e:
                return {
                    "request_id": request_count,
                    "status": f"❌ EXCEPTION {str(e)}",
                    "timestamp": time.time() - start_time
                }
        
        # Send requests continuously for the duration
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = []
            
            while time.time() - start_time < duration_seconds:
                # Submit new requests
                future = executor.submit(send_request)
                futures.append(future)
                
                # Brief pause to control rate
                time.sleep(0.1)
                
                # Clean up completed futures
                completed = [f for f in futures if f.done()]
                for f in completed:
                    try:
                        result = f.result()
                        results.append(result)
                    except:
                        pass
                    futures.remove(f)
            
            # Wait for remaining requests
            for future in futures:
                try:
                    result = future.result()
                    results.append(result)
                except:
                    pass
        
        total_time = time.time() - start_time
        successful = sum(1 for r in results if "SUCCESS" in r['status'])
        
        print(f"\n📊 PEAK LOAD PERFORMANCE:")
        print(f"  Duration: {total_time:.1f}s")
        print(f"  Total Requests: {len(results)}")
        print(f"  Successful: {successful}")
        print(f"  Success Rate: {successful/len(results)*100:.1f}%")
        print(f"  Requests per Second: {len(results)/total_time:.1f}")
        print(f"  Average Response Time: {sum(r.get('timestamp', 0) for r in results)/len(results):.2f}s")
        
        return results
    
    def run_clinical_stress_tests(self):
        """Run all clinical stress tests"""
        
        print("🏥 CLINICAL STRESS TESTING SUITE")
        print("=" * 60)
        print("Testing CancerCare AI under high-volume clinical scenarios")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check backend
        try:
            response = requests.get(f"{self.backend_url}/", timeout=5)
            if response.status_code != 200:
                print("❌ Backend is not responding correctly")
                return
        except Exception as e:
            print(f"❌ Cannot connect to backend: {e}")
            return
        
        print("✅ Backend is running - Starting clinical stress tests...")
        
        # Run stress tests
        er_results = self.simulate_emergency_room_load(15)
        workflow_results = self.simulate_clinical_workflow(20)
        peak_results = self.simulate_peak_load(30)
        
        # Overall analysis
        print(f"\n" + "=" * 60)
        print("🎯 CLINICAL STRESS TEST SUMMARY")
        print("=" * 60)
        
        total_requests = len(er_results) + len(workflow_results) + len(peak_results)
        total_successful = (
            sum(1 for r in er_results if "SUCCESS" in r['status']) +
            sum(1 for r in workflow_results if "SUCCESS" in r['status']) +
            sum(1 for r in peak_results if "SUCCESS" in r['status'])
        )
        
        print(f"Total Requests Processed: {total_requests}")
        print(f"Total Successful: {total_successful}")
        print(f"Overall Success Rate: {total_successful/total_requests*100:.1f}%")
        
        print(f"\n📈 PERFORMANCE SUMMARY:")
        print(f"  Emergency Room: {len(er_results)} requests")
        print(f"  Clinical Workflow: {len(workflow_results)} requests")
        print(f"  Peak Load: {len(peak_results)} requests")
        
        # Clinical readiness assessment
        if total_successful/total_requests >= 0.95:
            print(f"\n🎉 EXCELLENT! System handles clinical stress perfectly")
            print(f"✅ Ready for high-volume clinical deployment")
            print(f"✅ Suitable for hospital-wide implementation")
        elif total_successful/total_requests >= 0.85:
            print(f"\n🟡 GOOD! System handles clinical stress well")
            print(f"✅ Ready for moderate clinical deployment")
            print(f"🔧 Minor optimizations recommended")
        else:
            print(f"\n🔴 NEEDS IMPROVEMENT")
            print(f"🔧 System struggles under clinical stress")
            print(f"🔧 Performance optimization required")
        
        print(f"\n⏰ Stress Testing Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main stress testing function"""
    tester = ClinicalStressTester()
    tester.run_clinical_stress_tests()

if __name__ == "__main__":
    main()
