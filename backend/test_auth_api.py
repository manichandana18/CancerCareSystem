"""
Test script for authentication API endpoints
Tests user registration, login, session verification, and logout
"""

import requests
import json

API_BASE_URL = "http://127.0.0.1:8000"

def test_authentication_flow():
    print("=" * 60)
    print("TESTING AUTHENTICATION SYSTEM")
    print("=" * 60)
    
    # Test 1: User Registration
    print("\n1. Testing User Registration...")
    register_data = {
        "name": "Test User",
        "email": "testuser@cancercare.ai",
        "phone": "+1234567890",
        "password": "SecurePassword123!"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/auth/register", json=register_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Registration successful!")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Session Token: {data.get('session_token')[:20]}...")
            session_token = data.get('session_token')
        else:
            print(f"❌ Registration failed: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test 2: Session Verification
    print("\n2. Testing Session Verification...")
    try:
        headers = {"Authorization": f"Bearer {session_token}"}
        response = requests.get(f"{API_BASE_URL}/api/auth/verify", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Session verified!")
            print(f"   User: {data.get('user_info', {}).get('name')}")
            print(f"   Email: {data.get('user_info', {}).get('email')}")
        else:
            print(f"❌ Session verification failed: {response.json()}")
    except Exception as e:
        print(f"❌ Verification error: {e}")
    
    # Test 3: Logout
    print("\n3. Testing Logout...")
    try:
        logout_data = {"session_token": session_token}
        response = requests.post(f"{API_BASE_URL}/api/auth/logout", json=logout_data)
        if response.status_code == 200:
            print(f"✅ Logout successful!")
        else:
            print(f"❌ Logout failed: {response.json()}")
    except Exception as e:
        print(f"❌ Logout error: {e}")
    
    # Test 4: Login with same credentials
    print("\n4. Testing Login...")
    login_data = {
        "email": "testuser@cancercare.ai",
        "password": "SecurePassword123!"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login successful!")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Session Token: {data.get('session_token')[:20]}...")
            new_session_token = data.get('session_token')
        else:
            print(f"❌ Login failed: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test 5: Get User Profile
    print("\n5. Testing Get Profile...")
    try:
        headers = {"Authorization": f"Bearer {new_session_token}"}
        response = requests.get(f"{API_BASE_URL}/api/auth/profile", headers=headers)
        if response.status_code == 200:
            data = response.json()
            user_info = data.get('user_info', {})
            print(f"✅ Profile retrieved!")
            print(f"   Name: {user_info.get('name')}")
            print(f"   Email: {user_info.get('email')}")
            print(f"   Phone: {user_info.get('phone')}")
            print(f"   Security Level: {user_info.get('security_level')}")
        else:
            print(f"❌ Profile retrieval failed: {response.json()}")
    except Exception as e:
        print(f"❌ Profile error: {e}")
    
    # Test 6: Invalid Login
    print("\n6. Testing Invalid Login...")
    invalid_login_data = {
        "email": "testuser@cancercare.ai",
        "password": "WrongPassword123!"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/auth/login", json=invalid_login_data)
        if response.status_code == 401:
            print(f"✅ Invalid login correctly rejected!")
        else:
            print(f"❌ Invalid login should have been rejected")
    except Exception as e:
        print(f"❌ Invalid login test error: {e}")
    
    print("\n" + "=" * 60)
    print("AUTHENTICATION TESTS COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    print("\n⚠️  Make sure the backend server is running:")
    print("   cd backend")
    print("   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000\n")
    
    input("Press Enter to start tests...")
    test_authentication_flow()
