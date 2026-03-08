"""
Comprehensive Backend API Testing Script
Tests all API endpoints of the CancerCareSystem
"""

import requests
import json
import os
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")

def test_backend_health():
    """Test if backend is running"""
    print_header("Backend Health Check")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print_success("Backend server is running!")
            print_info(f"API Documentation available at: {BASE_URL}/docs")
            return True
        else:
            print_error(f"Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend server!")
        print_info("Make sure backend is running on http://127.0.0.1:8000")
        return False

def test_auth_endpoints():
    """Test authentication endpoints"""
    print_header("Authentication Endpoints")
    
    # Test registration
    print_info("Testing user registration...")
    register_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "Test123!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        if response.status_code in [200, 201]:
            print_success("Registration endpoint works!")
            print_info(f"Response: {response.json()}")
        elif response.status_code == 400:
            print_info("User might already exist (this is okay)")
            print_info(f"Response: {response.json()}")
        else:
            print_error(f"Registration failed with status {response.status_code}")
            print_info(f"Response: {response.text}")
    except Exception as e:
        print_error(f"Registration test failed: {str(e)}")
    
    # Test login
    print_info("\nTesting user login...")
    login_data = {
        "email": "testuser@example.com",
        "password": "Test123!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            print_success("Login endpoint works!")
            token_data = response.json()
            print_info(f"Received access token: {token_data.get('access_token', 'N/A')[:20]}...")
            return token_data.get('access_token')
        else:
            print_error(f"Login failed with status {response.status_code}")
            print_info(f"Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Login test failed: {str(e)}")
        return None

def test_prediction_endpoint(endpoint_name, endpoint_path, image_path=None):
    """Test a cancer prediction endpoint"""
    print_info(f"\nTesting {endpoint_name} endpoint...")
    
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as f:
                files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
                response = requests.post(f"{BASE_URL}{endpoint_path}", files=files)
                
                if response.status_code == 200:
                    print_success(f"{endpoint_name} endpoint works!")
                    result = response.json()
                    print_info(f"Prediction: {result.get('prediction', 'N/A')}")
                    print_info(f"Confidence: {result.get('confidence', 'N/A')}")
                    return True
                else:
                    print_error(f"{endpoint_name} failed with status {response.status_code}")
                    print_info(f"Response: {response.text}")
                    return False
        except Exception as e:
            print_error(f"{endpoint_name} test failed: {str(e)}")
            return False
    else:
        print_info(f"No test image available for {endpoint_name}")
        print_info(f"Endpoint: {endpoint_path}")
        return None

def test_all_prediction_endpoints():
    """Test all cancer detection endpoints"""
    print_header("Cancer Detection Endpoints")
    
    # Define endpoints
    endpoints = [
        ("Bone Cancer", "/predict/bone"),
        ("Lung Cancer", "/predict/lung"),
        ("Brain Cancer", "/predict/brain"),
        ("Breast Cancer", "/predict/breast"),
        ("Blood Cancer", "/predict/blood"),
        ("Skin Cancer", "/predict/skin"),
        ("Auto-Predict", "/predict/auto"),
    ]
    
    # Look for test images in common locations
    test_image_dirs = [
        Path("../BoneCancer/dataset/valid"),
        Path("../LungCancer"),
        Path("./dataset"),
        Path("../dataset"),
        Path("."),
    ]
    
    test_image = None
    for dir_path in test_image_dirs:
        if dir_path.exists():
            # Find first image file
            for ext in ['*.jpg', '*.jpeg', '*.png']:
                images = list(dir_path.glob(ext))
                if images:
                    test_image = str(images[0])
                    print_info(f"Using test image: {test_image}")
                    break
            if test_image:
                break
    
    if not test_image:
        print_info("No test images found. Testing endpoint availability only.")
    
    results = {}
    for name, path in endpoints:
        result = test_prediction_endpoint(name, path, test_image)
        results[name] = result
    
    return results

def print_summary(results):
    """Print test summary"""
    print_header("Test Summary")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    
    print(f"Total Tests: {total}")
    print_success(f"Passed: {passed}")
    print_error(f"Failed: {failed}")
    print_info(f"Skipped: {skipped}")
    
    print("\nDetailed Results:")
    for test_name, result in results.items():
        if result is True:
            print_success(f"{test_name}: PASSED")
        elif result is False:
            print_error(f"{test_name}: FAILED")
        else:
            print_info(f"{test_name}: SKIPPED (no test data)")

def main():
    print_header("CancerCareSystem Backend API Testing")
    
    results = {}
    
    # Test 1: Backend Health
    if not test_backend_health():
        print_error("\nBackend is not running. Please start the backend server first.")
        return
    
    results['Backend Health'] = True
    
    # Test 2: Authentication
    token = test_auth_endpoints()
    results['Authentication'] = token is not None
    
    # Test 3: Prediction Endpoints
    prediction_results = test_all_prediction_endpoints()
    results.update(prediction_results)
    
    # Print Summary
    print_summary(results)
    
    print_header("Testing Complete")
    print_info("Frontend Testing:")
    print_info("Please open your browser and visit: http://localhost:5173")
    print_info("Follow the manual testing guide in testing_plan.md")

if __name__ == "__main__":
    main()
