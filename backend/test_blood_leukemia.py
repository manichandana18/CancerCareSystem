#!/usr/bin/env python3
"""
Test blood cancer detection with leukemia sample
"""

import requests
import io
from PIL import Image
import random

def create_leukemia_image():
    """Create a synthetic leukemia blood smear image"""
    img = Image.new('RGB', (400, 300), color='white')
    
    # Add many abnormal cells (leukemia characteristic)
    for _ in range(30):  # More cells than normal
        x = random.randint(0, 350)
        y = random.randint(0, 250)
        radius = random.randint(8, 18)  # Larger cells (leukemia blasts)
        
        # Leukemia cells: darker, irregular
        color = (180, 60, 60)  # Darker red
        
        # Draw irregular cell (simulate blast cells)
        for dx in range(-radius, radius):
            for dy in range(-radius, radius):
                if dx*dx + dy*dy <= radius*radius:
                    if 0 <= x+dx < 400 and 0 <= y+dy < 300:
                        # Add some irregularity
                        if random.random() > 0.1:  # 90% fill
                            img.putpixel((x+dx, y+dy), color)
    
    return img

def test_leukemia_prediction():
    """Test leukemia prediction"""
    img = create_leukemia_image()
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    image_bytes = img_bytes.getvalue()
    
    # Test API
    files = {"file": ("leukemia_smear.jpg", image_bytes, "image/jpeg")}
    
    try:
        response = requests.post("http://127.0.0.1:8000/predict/blood", files=files, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("🩸 LEUKEMIA TEST RESULTS:")
            print("=" * 30)
            print(f"Diagnosis: {result.get('diagnosis', 'Unknown')}")
            print(f"Confidence: {result.get('diagnosis_confidence_pct', 0)}%")
            print(f"Method: {result.get('method', 'Unknown')}")
            print(f"Cell Count: {result.get('cell_count', 0)}")
            
            # Check explainability
            explain = result.get('explainability', {})
            print(f"Graph Nodes: {explain.get('graph_nodes', 0)}")
            print(f"Graph Edges: {explain.get('graph_edges', 0)}")
            
            return True
        else:
            print("ERROR:")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return False

if __name__ == "__main__":
    print("Testing Leukemia Detection...")
    test_leukemia_prediction()
