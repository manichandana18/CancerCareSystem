"""
Test the web interface with a simple API call
"""

import requests
import json

def test_web_interface():
    """Test the web interface API"""
    
    print("🌐 TESTING WEB INTERFACE API")
    print("=" * 40)
    
    # Test server connection
    try:
        response = requests.get("http://127.0.0.1:8080/")
        if response.status_code == 200:
            print("✅ Server connection successful")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Server connection failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Server connection error: {e}")
        print("Make sure the server is running on http://127.0.0.1:8080")
        return
    
    # Test with an image
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://127.0.0.1:8080/auto-predict", files=files)
            
        if response.status_code == 200:
            result = response.json()
            print("✅ API test successful")
            print(f"Organ: {result.get('organ')}")
            print(f"Diagnosis: {result.get('diagnosis')}")
            print(f"Confidence: {result.get('diagnosis_confidence_pct')}%")
            
            # Check for differential diagnosis
            if 'differential_diagnosis' in result:
                diff = result['differential_diagnosis']
                print("✅ Differential diagnosis present")
                
                if 'primary_diagnosis' in diff:
                    primary = diff['primary_diagnosis']
                    print(f"Primary: {primary.get('cancer_type')} - Risk: {primary.get('risk_level')}")
                
                if 'clinical_recommendations' in diff:
                    recs = diff['clinical_recommendations']
                    print(f"Recommendations: {len(recs)} items")
                    for rec in recs[:2]:
                        print(f"  • {rec}")
                
                if 'next_steps' in diff:
                    steps = diff['next_steps']
                    print(f"Next steps: {len(steps)} items")
                    for step in steps[:2]:
                        print(f"  • {step}")
            else:
                print("❌ Differential diagnosis missing")
        else:
            print(f"❌ API test failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ API test error: {e}")

if __name__ == "__main__":
    test_web_interface()
