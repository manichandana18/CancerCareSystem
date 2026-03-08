"""
Quick test script to verify the prediction fix
Run this after starting the FastAPI backend server
"""
import requests
import sys

def test_prediction(image_path):
    """Test the prediction API with an image"""
    url = "http://127.0.0.1:8000/predict"
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (image_path, f, 'image/jpeg')}
            response = requests.post(url, files=files)
            
        if response.status_code == 200:
            result = response.json()
            print("\n" + "="*60)
            print("PREDICTION RESULTS")
            print("="*60)
            print(f"Prediction: {result.get('prediction', 'N/A')}")
            print(f"Confidence: {result.get('confidence', 'N/A')}")
            
            if 'probabilities' in result:
                probs = result['probabilities']
                print(f"\nDetailed Probabilities:")
                print(f"  Normal (No Tumor): {probs.get('normal', 'N/A')}")
                print(f"  Tumor: {probs.get('tumor', 'N/A')}")
                print(f"  Threshold Used: {result.get('threshold_used', 'N/A')}")
            
            print(f"\nAdvice:")
            for advice_item in result.get('advice', []):
                print(f"  • {advice_item}")
            
            print("="*60)
            
            # Check if it's detecting cancer correctly
            if 'Tumor' in result.get('prediction', '') or 'Uncertain' in result.get('prediction', ''):
                print("\n[OK] Model is flagging potential cancer (good for safety)")
            else:
                tumor_prob = result.get('probabilities', {}).get('tumor', 0)
                if tumor_prob > 0.3:
                    print(f"\n[WARNING] Tumor probability is {tumor_prob:.4f} but classified as normal!")
                    print("   This might indicate a label reversal issue or model needs retraining.")
                else:
                    print(f"\n[OK] Model classified as normal (tumor prob: {tumor_prob:.4f})")
            
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except FileNotFoundError:
        print(f"Error: Image file not found: {image_path}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the backend server is running:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_prediction.py <image_path>")
        print("Example: python test_prediction.py test_xray.jpg")
        sys.exit(1)
    
    test_prediction(sys.argv[1])

