import requests
import time

API_BASE_URL = "http://127.0.0.1:8000"

def test_registration():
    email = f"bug_test_{int(time.time())}@example.com"
    data = {
        "name": "Bug Tester",
        "email": email,
        "phone": "+1234567890",
        "password": "Password123!"
    }
    
    print(f"Testing registration with {email}...")
    try:
        response = requests.post(f"{API_BASE_URL}/api/auth/register", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_registration()
