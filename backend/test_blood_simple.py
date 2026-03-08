#!/usr/bin/env python3
"""
Simple test of blood cancer prediction
"""

import requests
import io
from PIL import Image
import random

def create_blood_image():
    """Create a synthetic blood smear image"""
    img = Image.new('RGB', (400, 300), color='white')
    
    # Add red spots to simulate cells
    for _ in range(20):
        x = random.randint(0, 350)
        y = random.randint(0, 250)
        radius = random.randint(5, 15)
        
        for dx in range(-radius, radius):
            for dy in range(-radius, radius):
                if dx*dx + dy*dy <= radius*radius:
                    if 0 <= x+dx < 400 and 0 <= y+dy < 300:
                        img.putpixel((x+dx, y+dy), (200, 50, 50))
    
    return img

def test_blood_prediction():
    """Test blood cancer prediction API"""
    img = create_blood_image()
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    image_bytes = img_bytes.getvalue()
    
    # Test API
    files = {"file": ("blood_smear.jpg", image_bytes, "image/jpeg")}
    
    try:
        response = requests.post("http://127.0.0.1:8000/predict/blood", files=files, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("SUCCESS: Blood cancer prediction worked!")
            print(f"Diagnosis: {result.get('diagnosis', 'Unknown')}")
            print(f"Confidence: {result.get('diagnosis_confidence_pct', 0)}%")
            print(f"Method: {result.get('method', 'Unknown')}")
            return True
        else:
            print("ERROR:")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return False

if __name__ == "__main__":
    print("Testing Blood Cancer Prediction...")
    test_blood_prediction()
