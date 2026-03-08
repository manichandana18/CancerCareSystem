import requests
import json
import time

API_BASE_URL = "http://127.0.0.1:8000"

def register_and_login_user(i):
    user_data = {
        "name": f"User {i}",
        "email": f"user{i}_{int(time.time()) + i}@cancercare.ai",
        "phone": f"+123456789{i}",
        "password": f"Password123!{i}"
    }
    
    print(f"[User {i}] Registering {user_data['email']}...")
    reg_response = requests.post(f"{API_BASE_URL}/api/auth/register", json=user_data)
    if reg_response.status_code != 200:
        return f"User {i} Registration Failed: {reg_response.text}"
    
    print(f"[User {i}] Logging in...")
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    login_response = requests.post(f"{API_BASE_URL}/api/auth/login", json=login_data)
    if login_response.status_code != 200:
        return f"User {i} Login Failed: {login_response.text}"
    
    login_data = login_response.json()
    token = login_data.get("session_token")
    
    # Verify session
    headers = {"Authorization": f"Bearer {token}"}
    verify_response = requests.get(f"{API_BASE_URL}/api/auth/verify", headers=headers)
    
    if verify_response.status_code == 200:
        return f"User {i} Success: Name={user_data['name']}"
    else:
        return f"User {i} Verification Failed: {verify_response.text}"

def run_multi_user_test_seq(num_users=5):
    print(f"🚀 Starting Sequential Multi-User Test for {num_users} users...")
    results = []
    for i in range(1, num_users + 1):
        results.append(register_and_login_user(i))
        time.sleep(0.5) # Small pause
    
    print("\n--- TEST RESULTS ---")
    for res in results:
        print(res)
    
    success_count = sum(1 for res in results if "Success" in res)
    print(f"\n✅ Total Successes: {success_count}/{num_users}")

if __name__ == "__main__":
    run_multi_user_test_seq(5)
