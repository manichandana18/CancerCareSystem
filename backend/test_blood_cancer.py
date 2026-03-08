#!/usr/bin/env python3
"""
Test Graph Neural Network Blood Cancer Detection
"""

import requests
import json
import sys
import io
from pathlib import Path

def test_blood_cancer_direct():
    """Test GNN blood cancer detection directly"""
    try:
        from graph_neural_network_blood import BloodCancerGNN
        
        # Create GNN instance
        gnn = BloodCancerGNN()
        gnn.load_pretrained_model()
        print("SUCCESS: Graph Neural Network loaded")
        
        # Test with dummy image (since we don't have blood smear images)
        from PIL import Image
        import numpy as np
        
        # Create a synthetic blood smear image
        img = Image.new('RGB', (400, 300), color='white')
        
        # Add some red spots to simulate cells
        import random
        for _ in range(20):
            x = random.randint(0, 350)
            y = random.randint(0, 250)
            radius = random.randint(5, 15)
            
            # Draw red circles
            for dx in range(-radius, radius):
                for dy in range(-radius, radius):
                    if dx*dx + dy*dy <= radius*radius:
                        if 0 <= x+dx < 400 and 0 <= y+dy < 300:
                            img.putpixel((x+dx, y+dy), (200, 50, 50))
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        image_bytes = img_bytes.getvalue()
        
        # Test prediction
        result = gnn.predict_blood_cancer(image_bytes)
        
        print("BLOOD CANCER DETECTION RESULTS:")
        print("=" * 40)
        print(f"Diagnosis: {result.get('diagnosis', 'Unknown')}")
        print(f"Confidence: {result.get('diagnosis_confidence_pct', 0)}%")
        print(f"Method: {result.get('method', 'Unknown')}")
        print(f"Cell Count: {result.get('cell_count', 0)}")
        
        # Check explainability
        explain = result.get('explainability', {})
        print(f"Explainability Method: {explain.get('method', 'Unknown')}")
        print(f"Graph Nodes: {explain.get('graph_nodes', 0)}")
        print(f"Graph Edges: {explain.get('graph_edges', 0)}")
        
        return result
        
    except ImportError as e:
        print(f"IMPORT FAILED: {e}")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def test_blood_cancer_api():
    """Test blood cancer detection through API"""
    
    # Create synthetic blood smear image
    from PIL import Image
    import random
    import io
    
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
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    image_bytes = img_bytes.getvalue()
    
    # Test API
    files = {"file": ("blood_smear.jpg", image_bytes, "image/jpeg")}
    
    try:
        response = requests.post("http://127.0.0.1:8000/predict/blood", files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            print("API BLOOD CANCER RESULTS:")
            print("=" * 30)
            print(f"Organ: {result.get('organ', 'Unknown')}")
            print(f"Diagnosis: {result.get('diagnosis', 'Unknown')}")
            print(f"Confidence: {result.get('diagnosis_confidence_pct', 0)}%")
            print(f"Method: {result.get('method', 'Unknown')}")
            print(f"Cell Count: {result.get('cell_count', 0)}")
            
            return result
        else:
            print(f"API ERROR: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"API TEST FAILED: {e}")
        return None

def test_blood_cell_analysis():
    """Test blood cell analysis endpoint"""
    
    # Create synthetic blood smear image
    from PIL import Image
    import random
    import io
    
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
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    image_bytes = img_bytes.getvalue()
    
    # Test API
    files = {"file": ("blood_smear.jpg", image_bytes, "image/jpeg")}
    
    try:
        response = requests.post("http://127.0.0.1:8000/analyze/blood", files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            print("BLOOD CELL ANALYSIS RESULTS:")
            print("=" * 35)
            print(f"Cell Count: {result.get('cell_count', 0)}")
            print(f"Graph Nodes: {result.get('graph_nodes', 0)}")
            print(f"Graph Edges: {result.get('graph_edges', 0)}")
            print(f"Analysis Available: {result.get('analysis_available', False)}")
            
            return result
        else:
            print(f"ANALYSIS API ERROR: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"ANALYSIS API TEST FAILED: {e}")
        return None

if __name__ == "__main__":
    print("Testing Graph Neural Network Blood Cancer Detection...")
    print("=" * 60)
    
    # Test 1: Direct GNN test
    print("\n1. DIRECT GNN TEST:")
    direct_result = test_blood_cancer_direct()
    
    # Test 2: API test
    print("\n2. API PREDICTION TEST:")
    api_result = test_blood_cancer_api()
    
    # Test 3: Cell analysis test
    print("\n3. CELL ANALYSIS TEST:")
    analysis_result = test_blood_cell_analysis()
    
    print("\n" + "=" * 60)
    print("BLOOD CANCER DETECTION TEST COMPLETE!")
    
    if direct_result and api_result:
        print("SUCCESS: Graph Neural Network blood cancer detection is working!")
    else:
        print("ISSUES: Some tests failed - check implementation")
