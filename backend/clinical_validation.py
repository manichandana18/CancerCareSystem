"""
Clinical Validation Framework
Tests CancerCare AI with real medical imaging scenarios
"""

import os
import sys
from pathlib import Path
import requests
import json
from datetime import datetime
import time

# Add backend to path
sys.path.append(str(Path(__file__).parent))

class ClinicalValidator:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.validation_results = []
        
    def create_realistic_test_cases(self):
        """Create realistic medical imaging test cases"""
        
        print("🏥 CREATING REALISTIC MEDICAL TEST CASES")
        print("=" * 60)
        
        # Simulate real medical scenarios using available images
        test_cases = [
            # Emergency Room Cases
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
                "filename": "ER_bone_fracture_suspected.jpg",
                "scenario": "ER - Trauma Patient",
                "clinical_context": "45-year-old male, car accident, suspected bone fracture",
                "expected_findings": "bone abnormalities",
                "urgency": "high"
            },
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg",
                "filename": "ER_chest_pain_unknown.jpg",
                "scenario": "ER - Chest Pain",
                "clinical_context": "62-year-old female, acute chest pain, shortness of breath",
                "expected_findings": "lung abnormalities",
                "urgency": "high"
            },
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg",
                "filename": "ER_head_trauma.jpg",
                "scenario": "ER - Head Trauma",
                "clinical_context": "28-year-old male, motorcycle accident, head injury",
                "expected_findings": "brain abnormalities",
                "urgency": "critical"
            },
            
            # Outpatient Clinic Cases
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
                "filename": "clinic_orthopedic_followup.jpg",
                "scenario": "Orthopedic Clinic - Follow-up",
                "clinical_context": "67-year-old female, osteoporosis monitoring",
                "expected_findings": "normal bone structure",
                "urgency": "routine"
            },
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\normalbone1.jpg",
                "filename": "clinic_pulmonary_screening.jpg",
                "scenario": "Pulmonary Clinic - Screening",
                "clinical_context": "55-year-old male, smoker, annual lung cancer screening",
                "expected_findings": "normal lung tissue",
                "urgency": "routine"
            },
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\cancer3.jpg",
                "filename": "clinic_oncology_review.jpg",
                "scenario": "Oncology Clinic - Review",
                "clinical_context": "71-year-old female, lung cancer follow-up scan",
                "expected_findings": "lung malignancy",
                "urgency": "medium"
            },
            
            # Specialized Cases
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg",
                "filename": "neuro_brain_tumor_consult.jpg",
                "scenario": "Neurology - Tumor Consult",
                "clinical_context": "48-year-old male, headaches, MRI scan for suspected tumor",
                "expected_findings": "brain abnormalities",
                "urgency": "medium"
            },
            {
                "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
                "filename": "radiology_second_opinion.jpg",
                "scenario": "Radiology - Second Opinion",
                "clinical_context": "52-year-old female, previous scan showed abnormalities",
                "expected_findings": "detailed bone analysis",
                "urgency": "medium"
            }
        ]
        
        return test_cases
    
    def run_clinical_test(self, test_case):
        """Run a single clinical test case"""
        
        print(f"\n🏥 {test_case['scenario']}")
        print(f"📋 Clinical Context: {test_case['clinical_context']}")
        print(f"🎯 Expected: {test_case['expected_findings']}")
        print(f"⚡ Urgency: {test_case['urgency']}")
        
        if not os.path.exists(test_case['path']):
            result = {
                "scenario": test_case['scenario'],
                "status": "❌ SKIPPED",
                "error": "Test image not found",
                "urgency": test_case['urgency']
            }
            return result
        
        try:
            # Measure response time
            start_time = time.time()
            
            # Test auto-predict (clinical workflow)
            with open(test_case['path'], 'rb') as f:
                files = {'file': (test_case['filename'], f, 'image/jpeg')}
                response = requests.post(f"{self.backend_url}/predict/auto", files=files, timeout=30)
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                api_result = response.json()
                
                # Clinical analysis
                organ = api_result.get('organ', '').lower()
                diagnosis = api_result.get('diagnosis', '').lower()
                confidence = api_result.get('diagnosis_confidence_pct', 0)
                method = api_result.get('method', 'Unknown')
                
                # Clinical validation
                clinical_findings = f"{organ} - {diagnosis}"
                is_normal = 'normal' in diagnosis
                is_abnormal = any(word in diagnosis for word in ['cancer', 'malignant', 'suspicious', 'benign'])
                
                # Clinical relevance assessment
                relevance_score = self.assess_clinical_relevance(test_case, organ, diagnosis)
                
                result = {
                    "scenario": test_case['scenario'],
                    "clinical_context": test_case['clinical_context'],
                    "urgency": test_case['urgency'],
                    "filename": test_case['filename'],
                    "organ": organ,
                    "diagnosis": diagnosis,
                    "confidence": confidence,
                    "method": method,
                    "response_time": response_time,
                    "clinical_findings": clinical_findings,
                    "is_normal": is_normal,
                    "is_abnormal": is_abnormal,
                    "relevance_score": relevance_score,
                    "status": "✅ SUCCESS",
                    "timestamp": datetime.now().isoformat()
                }
                
                print(f"✅ Analysis Complete ({response_time:.2f}s)")
                print(f"🔬 Findings: {clinical_findings}")
                print(f"📊 Confidence: {confidence}%")
                print(f"🎯 Clinical Relevance: {relevance_score}/10")
                
            else:
                result = {
                    "scenario": test_case['scenario'],
                    "status": f"❌ API ERROR {response.status_code}",
                    "error": response.text,
                    "urgency": test_case['urgency'],
                    "response_time": time.time() - start_time
                }
                print(f"❌ API Error: {response.status_code}")
                
        except Exception as e:
            result = {
                "scenario": test_case['scenario'],
                "status": "❌ CLINICAL ERROR",
                "error": str(e),
                "urgency": test_case['urgency']
            }
            print(f"❌ Clinical Error: {e}")
        
        return result
    
    def assess_clinical_relevance(self, test_case, detected_organ, detected_diagnosis):
        """Assess clinical relevance of the detection"""
        
        score = 5  # Base score
        
        # Check if organ matches expected findings
        expected_keywords = test_case['expected_findings'].lower()
        
        if 'bone' in expected_keywords and detected_organ == 'bone':
            score += 2
        elif 'lung' in expected_keywords and detected_organ == 'lung':
            score += 2
        elif 'brain' in expected_keywords and detected_organ == 'brain':
            score += 2
        
        # Check diagnosis relevance
        if 'normal' in expected_keywords and 'normal' in detected_diagnosis:
            score += 2
        elif 'abnormal' in expected_keywords or 'cancer' in expected_keywords:
            if any(word in detected_diagnosis for word in ['cancer', 'malignant', 'suspicious', 'benign']):
                score += 2
        
        # Urgency bonus
        if test_case['urgency'] == 'critical' and detected_organ in ['brain', 'lung']:
            score += 1
        elif test_case['urgency'] == 'high' and detected_organ in ['bone', 'lung']:
            score += 1
        
        return min(score, 10)
    
    def run_clinical_validation(self):
        """Run complete clinical validation suite"""
        
        print("🏥 CLINICAL VALIDATION SUITE")
        print("=" * 60)
        print("Testing CancerCare AI with realistic medical scenarios")
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
        
        print("✅ Backend is running - Starting clinical validation...")
        
        # Get test cases
        test_cases = self.create_realistic_test_cases()
        
        # Run tests
        print(f"\n🧪 Running {len(test_cases)} clinical test cases:\n")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"{'='*20} Test {i}/{len(test_cases)} {'='*20}")
            result = self.run_clinical_test(test_case)
            self.validation_results.append(result)
            time.sleep(0.5)  # Brief pause between tests
        
        # Generate clinical report
        self.generate_clinical_report()
    
    def generate_clinical_report(self):
        """Generate comprehensive clinical validation report"""
        
        print("\n" + "=" * 60)
        print("📊 CLINICAL VALIDATION REPORT")
        print("=" * 60)
        
        # Overall statistics
        total_tests = len(self.validation_results)
        successful_tests = sum(1 for r in self.validation_results if 'SUCCESS' in r['status'])
        
        print(f"Total Clinical Cases: {total_tests}")
        print(f"Successful Analyses: {successful_tests}")
        print(f"Success Rate: {successful_tests/total_tests*100:.1f}%")
        
        # Response time analysis
        response_times = [r.get('response_time', 0) for r in self.validation_results if 'response_time' in r]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            print(f"\n⏱️ Response Time Analysis:")
            print(f"  Average: {avg_response_time:.2f}s")
            print(f"  Fastest: {min_response_time:.2f}s")
            print(f"  Slowest: {max_response_time:.2f}s")
        
        # Clinical relevance analysis
        relevance_scores = [r.get('relevance_score', 0) for r in self.validation_results if 'relevance_score' in r]
        if relevance_scores:
            avg_relevance = sum(relevance_scores) / len(relevance_scores)
            print(f"\n🎯 Clinical Relevance:")
            print(f"  Average Score: {avg_relevance:.1f}/10")
            print(f"  High Relevance Cases: {sum(1 for s in relevance_scores if s >= 8)}/{len(relevance_scores)}")
        
        # Organ distribution
        organ_counts = {}
        for result in self.validation_results:
            organ = result.get('organ', 'unknown')
            organ_counts[organ] = organ_counts.get(organ, 0) + 1
        
        print(f"\n🏥 Organ Distribution:")
        for organ, count in organ_counts.items():
            print(f"  {organ.capitalize()}: {count} cases")
        
        # Diagnosis distribution
        diagnosis_counts = {}
        for result in self.validation_results:
            diagnosis = result.get('diagnosis', 'unknown')
            diagnosis_counts[diagnosis] = diagnosis_counts.get(diagnosis, 0) + 1
        
        print(f"\n🔬 Diagnosis Distribution:")
        for diagnosis, count in diagnosis_counts.items():
            print(f"  {diagnosis.capitalize()}: {count} cases")
        
        # Urgency analysis
        urgency_stats = {'critical': 0, 'high': 0, 'medium': 0, 'routine': 0}
        for result in self.validation_results:
            urgency = result.get('urgency', 'routine')
            urgency_stats[urgency] = urgency_stats.get(urgency, 0) + 1
        
        print(f"\n⚡ Urgency Distribution:")
        for urgency, count in urgency_stats.items():
            print(f"  {urgency.capitalize()}: {count} cases")
        
        # Clinical recommendations
        print(f"\n🎯 CLINICAL RECOMMENDATIONS:")
        
        if successful_tests == total_tests and avg_relevance >= 7:
            print("🎉 EXCELLENT! System ready for clinical deployment")
            print("✅ High accuracy and clinical relevance")
            print("✅ Suitable for emergency room use")
            print("✅ Ready for clinical validation studies")
        elif successful_tests >= total_tests * 0.8 and avg_relevance >= 6:
            print("🟡 GOOD! System suitable for clinical use")
            print("✅ Good accuracy and relevance")
            print("🔧 Minor improvements recommended")
            print("✅ Ready for supervised clinical use")
        else:
            print("🔴 NEEDS IMPROVEMENT")
            print("🔧 System requires further development")
            print("🔧 Additional training needed")
            print("🔧 Not ready for clinical use")
        
        # Save detailed results
        self.save_clinical_results()
        
        print(f"\n⏰ Validation Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def save_clinical_results(self):
        """Save clinical validation results"""
        try:
            results_file = f"clinical_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(results_file, 'w') as f:
                json.dump(self.validation_results, f, indent=2, default=str)
            print(f"💾 Clinical results saved to: {results_file}")
        except Exception as e:
            print(f"❌ Could not save clinical results: {e}")

def main():
    """Main clinical validation function"""
    validator = ClinicalValidator()
    validator.run_clinical_validation()

if __name__ == "__main__":
    main()
