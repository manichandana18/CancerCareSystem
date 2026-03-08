import requests
import time

API_BASE_URL = "http://127.0.0.1:8000"

def test_otp_flow():
    email = f"otp_test_{int(time.time())}@example.com"
    reg_data = {
        "name": "OTP Tester",
        "email": email,
        "phone": "+1234567890",
        "password": "Password123!"
    }
    
    # 1. Register
    print(f"\n[1] Registering {email}...")
    reg_res = requests.post(f"{API_BASE_URL}/api/auth/register", json=reg_data)
    print(f"Status: {reg_res.status_code}")
    print(f"Response: {reg_res.text}")
    
    if reg_res.status_code != 200:
        print("❌ Registration failed")
        return

    # In a real scenario, we'd get the OTP from email. 
    # Here we might need to check the backend console/logs if we were running it.
    # But since I know the backend prints it, and I want to verify the endpoint:
    # I'll try to verify with 'invalid' first.
    
    print(f"\n[2] Verifying with INVALID OTP...")
    verify_data = {"email": email, "otp": "000000"}
    v_res = requests.post(f"{API_BASE_URL}/api/auth/verify-otp", json=verify_data)
    print(f"Status: {v_res.status_code}")
    print(f"Response: {v_res.text}")
    
    if v_res.status_code == 401:
        print("✅ Correctly rejected invalid OTP")
    else:
        print("❌ Error: Should have rejected invalid OTP")

if __name__ == "__main__":
    test_otp_flow()
