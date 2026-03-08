
import requests
import json
import secrets

def test_auth_with_age():
    base_url = "http://127.0.0.1:8000"
    email = f"test_{secrets.token_hex(4)}@example.com"
    password = "SecurePassword123!"
    name = "Test Age User"
    age = 25

    print(f"🧪 TESTING AUTH WITH AGE: {email}")
    print("-" * 50)

    # 1. Register
    reg_data = {
        "name": name,
        "email": email,
        "phone": "+1234567890",
        "password": password,
        "age": age
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/register", json=reg_data)
        print(f"Register Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Registration Successful")
            data = response.json()
            otp = data.get("otp")
            print(f"Received OTP: {otp}")
            
            # 2. Verify OTP
            verify_data = {"email": email, "otp": otp}
            v_res = requests.post(f"{base_url}/api/auth/verify-otp", json=verify_data)
            print(f"Verify OTP Status: {v_res.status_code}")
            
            # 3. Login
            login_data = {"email": email, "password": password}
            l_res = requests.post(f"{base_url}/api/auth/login", json=login_data)
            print(f"Login Status: {l_res.status_code}")
            if l_res.status_code == 200:
                l_data = l_res.json()
                print("✅ Login Successful")
                user_info = l_data.get('user_info', {})
                print(f"User Info: {json.dumps(user_info, indent=2)}")
                if user_info.get('age') == age:
                    print("✅ Age verified in user info")
                else:
                    print(f"❌ Age mismatch: Expected {age}, got {user_info.get('age')}")
            else:
                print(f"❌ Login failed: {l_res.text}")
        else:
            print(f"❌ Registration failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_auth_with_age()
