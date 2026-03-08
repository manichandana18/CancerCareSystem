"""
Real-World Simulation Test for CancerCare AI
Simulates actual medical workflow scenarios
"""

import os
import sys
import time
import random
import requests
from datetime import datetime, timedelta
from pathlib import Path
import json

# Add backend to path
sys.path.append(str(Path(__file__).parent))

class RealWorldTester:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.test_images = [
            "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
            "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg", 
            "C:\\Users\\Balaiah goud\\Downloads\\normalbone1.jpg",
            "C:\\Users\\Balaiah goud\\Downloads\\cancer3.jpg",
            "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg"
        ]
        
    def simulate_doctor_workflow(self, num_patients=20):
        """Simulate a doctor analyzing patient images throughout the day"""
        
        print(f"🏥 Simulating Doctor Workflow - {num_patients} patients")
        print("=" * 60)
        
        results = []
        start_time = time.time()
        
        for patient_id in range(1, num_patients + 1):
            # Random patient scenario
            patient_name = f"Patient_{patient_id:03d}"
            image_path = random.choice([img for img in self.test_images if os.path.exists(img)])
            
            if not os.path.exists(image_path):
                continue
            
            # Simulate doctor uploading image
            print(f"📸 Dr. Smith analyzing {patient_name}...")
            
            try:
                upload_time = time.time()
                with open(image_path, 'rb') as f:
                    files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
                    response = requests.post(f"{self.backend_url}/predict/auto", files=files, timeout=30)
                analysis_time = time.time() - upload_time
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Simulate doctor reviewing results
                    time.sleep(0.5)  # Doctor review time
                    
                    results.append({
                        "patient_id": patient_id,
                        "patient_name": patient_name,
                        "image": os.path.basename(image_path),
                        "organ": result.get('organ'),
                        "diagnosis": result.get('diagnosis'),
                        "confidence": result.get('diagnosis_confidence_pct'),
                        "analysis_time": analysis_time,
                        "status": "✅ SUCCESS"
                    })
                    
                    print(f"  ✅ Analysis complete: {result.get('organ')} - {result.get('diagnosis')}")
                else:
                    results.append({
                        "patient_id": patient_id,
                        "patient_name": patient_name,
                        "status": f"❌ ERROR: {response.status_code}"
                    })
                    print(f"  ❌ Analysis failed")
                    
            except Exception as e:
                results.append({
                    "patient_id": patient_id,
                    "patient_name": patient_name,
                    "status": f"❌ ERROR: {str(e)}"
                })
                print(f"  ❌ Analysis error: {e}")
            
            # Simulate time between patients
            time.sleep(random.uniform(0.2, 0.8))
        
        total_time = time.time() - start_time
        
        # Analyze workflow results
        successful = sum(1 for r in results if "SUCCESS" in r['status'])
        avg_analysis_time = sum(r.get('analysis_time', 0) for r in results) / len(results) if results else 0
        
        print(f"\n📊 Doctor Workflow Results:")
        print(f"  Total Patients: {num_patients}")
        print(f"  Successful Analyses: {successful}")
        print(f"  Success Rate: {successful/num_patients*100:.1f}%")
        print(f"  Average Analysis Time: {avg_analysis_time:.2f}s")
        print(f"  Total Workflow Time: {total_time:.1f}s")
        print(f"  Patients per Hour: {num_patients/total_time*3600:.1f}")
        
        return results
    
    def simulate_emergency_room(self, num_cases=15):
        """Simulate emergency room rapid analysis scenarios"""
        
        print(f"\n🚑 Simulating Emergency Room - {num_cases} urgent cases")
        print("=" * 60)
        
        results = []
        start_time = time.time()
        
        for case_id in range(1, num_cases + 1):
            case_name = f"ER_Case_{case_id:03d}"
            
            # Emergency cases are more likely to be cancer
            if random.random() < 0.6:  # 60% chance of suspected cancer
                image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
                expected_diagnosis = "cancer"
            else:
                image_path = "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg"
                expected_diagnosis = "malignant"
            
            if not os.path.exists(image_path):
                continue
            
            print(f"🏥 ER Case {case_id}: Urgent analysis needed...")
            
            try:
                # Emergency requests should be fast
                emergency_start = time.time()
                with open(image_path, 'rb') as f:
                    files = {'file': (f'ER_{case_id}.jpg', f, 'image/jpeg')}
                    response = requests.post(f"{self.backend_url}/predict/auto", files=files, timeout=15)
                emergency_time = time.time() - emergency_start
                
                if response.status_code == 200:
                    result = response.json()
                    
                    results.append({
                        "case_id": case_id,
                        "case_name": case_name,
                        "organ": result.get('organ'),
                        "diagnosis": result.get('diagnosis'),
                        "confidence": result.get('diagnosis_confidence_pct'),
                        "response_time": emergency_time,
                        "status": "✅ SUCCESS"
                    })
                    
                    print(f"  ⚡ Emergency result: {result.get('organ')} - {result.get('diagnosis')} ({emergency_time:.2f}s)")
                else:
                    results.append({
                        "case_id": case_id,
                        "case_name": case_name,
                        "status": f"❌ ERROR: {response.status_code}"
                    })
                    print(f"  ❌ Emergency analysis failed")
                    
            except Exception as e:
                results.append({
                    "case_id": case_id,
                    "case_name": case_name,
                    "status": f"❌ ERROR: {str(e)}"
                })
                print(f"  ❌ Emergency error: {e}")
            
            # Emergency cases come in quickly
            time.sleep(random.uniform(0.1, 0.3))
        
        total_time = time.time() - start_time
        
        # Analyze ER results
        successful = sum(1 for r in results if "SUCCESS" in r['status'])
        avg_response_time = sum(r.get('response_time', 0) for r in results) / len(results) if results else 0
        
        print(f"\n📊 Emergency Room Results:")
        print(f"  Total Cases: {num_cases}")
        print(f"  Successful Analyses: {successful}")
        print(f"  Success Rate: {successful/num_cases*100:.1f}%")
        print(f"  Average Response Time: {avg_response_time:.2f}s")
        print(f"  Total ER Time: {total_time:.1f}s")
        
        return results
    
    def simulate_research_study(self, num_samples=50):
        """Simulate research study with batch analysis"""
        
        print(f"\n🔬 Simulating Research Study - {num_samples} samples")
        print("=" * 60)
        
        results = []
        start_time = time.time()
        
        # Simulate batch processing
        batch_size = 5
        for batch_start in range(0, num_samples, batch_size):
            batch_end = min(batch_start + batch_size, num_samples)
            batch_results = []
            
            print(f"📊 Processing batch {batch_start//batch_size + 1}: samples {batch_start+1}-{batch_end}")
            
            for sample_id in range(batch_start + 1, batch_end + 1):
                sample_name = f"Research_Sample_{sample_id:04d}"
                image_path = random.choice([img for img in self.test_images if os.path.exists(img)])
                
                if not os.path.exists(image_path):
                    continue
                
                try:
                    with open(image_path, 'rb') as f:
                        files = {'file': (f'{sample_name}.jpg', f, 'image/jpeg')}
                        response = requests.post(f"{self.backend_url}/predict/auto", files=files, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        batch_results.append({
                            "sample_id": sample_id,
                            "sample_name": sample_name,
                            "organ": result.get('organ'),
                            "diagnosis": result.get('diagnosis'),
                            "confidence": result.get('diagnosis_confidence_pct'),
                            "status": "✅ SUCCESS"
                        })
                    else:
                        batch_results.append({
                            "sample_id": sample_id,
                            "sample_name": sample_name,
                            "status": f"❌ ERROR: {response.status_code}"
                        })
                        
                except Exception as e:
                    batch_results.append({
                        "sample_id": sample_id,
                        "sample_name": sample_name,
                        "status": f"❌ ERROR: {str(e)}"
                    })
            
            results.extend(batch_results)
            
            # Brief pause between batches
            time.sleep(0.5)
        
        total_time = time.time() - start_time
        
        # Analyze research results
        successful = sum(1 for r in results if "SUCCESS" in r['status'])
        
        # Count diagnoses
        organ_counts = {}
        diagnosis_counts = {}
        for result in results:
            if "SUCCESS" in result['status']:
                organ = result.get('organ', 'unknown')
                diagnosis = result.get('diagnosis', 'unknown')
                organ_counts[organ] = organ_counts.get(organ, 0) + 1
                diagnosis_counts[diagnosis] = diagnosis_counts.get(diagnosis, 0) + 1
        
        print(f"\n📊 Research Study Results:")
        print(f"  Total Samples: {num_samples}")
        print(f"  Successful Analyses: {successful}")
        print(f"  Success Rate: {successful/num_samples*100:.1f}%")
        print(f"  Total Study Time: {total_time:.1f}s")
        print(f"  Samples per Hour: {num_samples/total_time*3600:.1f}")
        
        print(f"\n  Organ Distribution:")
        for organ, count in organ_counts.items():
            print(f"    {organ}: {count} samples")
        
        print(f"\n  Diagnosis Distribution:")
        for diagnosis, count in diagnosis_counts.items():
            print(f"    {diagnosis}: {count} samples")
        
        return results
    
    def run_real_world_tests(self):
        """Run all real-world simulation tests"""
        
        print("🌍 REAL-WORLD SIMULATION TESTING")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check backend
        try:
            response = requests.get(f"{self.backend_url}/", timeout=5)
            if response.status_code != 200:
                print("❌ Backend is not responding correctly")
                return
        except Exception as e:
            print(f"❌ Cannot connect to backend: {e}")
            return
        
        # Run simulations
        doctor_results = self.simulate_doctor_workflow(15)
        er_results = self.simulate_emergency_room(10)
        research_results = self.simulate_research_study(25)
        
        # Overall summary
        print("\n" + "=" * 60)
        print("🎯 REAL-WORLD SIMULATION SUMMARY")
        print("=" * 60)
        
        total_tests = len(doctor_results) + len(er_results) + len(research_results)
        total_success = sum(1 for r in doctor_results + er_results + research_results if "SUCCESS" in r['status'])
        
        print(f"Total Simulations: {total_tests}")
        print(f"Total Successful: {total_success}")
        print(f"Overall Success Rate: {total_success/total_tests*100:.1f}%")
        
        print(f"\n📈 Performance Metrics:")
        print(f"  Doctor Workflow: {len(doctor_results)} cases")
        print(f"  Emergency Room: {len(er_results)} cases")
        print(f"  Research Study: {len(research_results)} samples")
        
        if total_success/total_tests >= 0.95:
            print(f"\n🎉 EXCELLENT! System is ready for real-world deployment!")
        elif total_success/total_tests >= 0.85:
            print(f"\n🟡 GOOD! System is mostly ready for deployment")
        else:
            print(f"\n🔴 NEEDS IMPROVEMENT! System needs more work before deployment")
        
        print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main real-world testing function"""
    tester = RealWorldTester()
    tester.run_real_world_tests()

if __name__ == "__main__":
    main()
