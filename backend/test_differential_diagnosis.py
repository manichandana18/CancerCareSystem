"""
Test the revolutionary differential diagnosis system
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_differential_diagnosis():
    """Test the differential diagnosis system"""
    
    print("🔬 TESTING REVOLUTIONARY DIFFERENTIAL DIAGNOSIS")
    print("=" * 60)
    print("This system provides multiple diagnosis possibilities like medical professionals")
    print("=" * 60)
    
    # Test with the bone image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Test cases
        test_cases = [
            {
                "filename": "bonecancer.jpg",
                "name": "Primary Bone Cancer Case"
            },
            {
                "filename": "unknown_mass.jpg",
                "name": "Unknown Mass - Differential Diagnosis Critical"
            },
            {
                "filename": "suspicious_lesion.jpg",
                "name": "Suspicious Lesion - Multiple Possibilities"
            }
        ]
        
        for test in test_cases:
            print(f"--- {test['name']} ---")
            print(f"Filename: {test['filename']}")
            
            result = auto_predict(image_bytes, filename_hint=test['filename'])
            
            # Primary diagnosis
            primary = result.get('organ', 'Unknown')
            diagnosis = result.get('diagnosis', 'Unknown')
            confidence = result.get('diagnosis_confidence_pct', 0)
            
            print(f"Primary Diagnosis: {primary} - {diagnosis}")
            print(f"Confidence: {confidence}%")
            
            # Differential diagnosis
            differential = result.get('differential_diagnosis', {})
            if differential:
                print(f"\n🔬 DIFFERENTIAL DIAGNOSIS:")
                
                # Primary diagnosis details
                primary_diag = differential.get('primary_diagnosis', {})
                if primary_diag:
                    print(f"1️⃣ PRIMARY: {primary_diag.get('cancer_type', 'Unknown')} (Confidence: {primary_diag.get('confidence', 0):.1%})")
                    print(f"   Risk Level: {primary_diag.get('risk_level', 'Unknown')}")
                    print(f"   Reasoning: {primary_diag.get('reasoning', 'No reasoning available')}")
                    
                    recommendations = primary_diag.get('recommendations', [])
                    if recommendations:
                        print(f"   Recommendations: {', '.join(recommendations[:2])}")
                
                # Alternative diagnoses
                alternatives = differential.get('differential_diagnoses', [])
                for i, alt in enumerate(alternatives[:3], 2):
                    print(f"{i}️⃣ ALTERNATIVE: {alt.get('cancer_type', 'Unknown')} (Confidence: {alt.get('confidence', 0):.1%})")
                    print(f"   Risk Level: {alt.get('risk_level', 'Unknown')}")
                    print(f"   Reasoning: {alt.get('reasoning', 'No reasoning available')}")
                
                # Clinical recommendations
                clinical_recs = differential.get('clinical_recommendations', [])
                if clinical_recs:
                    print(f"\n🏥 CLINICAL RECOMMENDATIONS:")
                    for rec in clinical_recs[:3]:
                        print(f"   • {rec}")
                
                # Next steps
                next_steps = differential.get('next_steps', [])
                if next_steps:
                    print(f"\n🚀 NEXT STEPS:")
                    for step in next_steps[:3]:
                        print(f"   • {step}")
                
                # Confidence analysis
                conf_dist = differential.get('confidence_distribution', {})
                if conf_dist:
                    print(f"\n📊 CONFIDENCE ANALYSIS:")
                    print(f"   Primary Confidence: {conf_dist.get('primary_confidence', 0):.1%}")
                    print(f"   Overall Certainty: {conf_dist.get('overall_certainty', 'Unknown')}")
                    if conf_dist.get('confidence_gap', 0) > 0:
                        print(f"   Confidence Gap: {conf_dist.get('confidence_gap', 0):.1%}")
            
            print("\n" + "="*60 + "\n")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_differential_diagnosis()
