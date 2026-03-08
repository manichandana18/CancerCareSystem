#!/usr/bin/env python3
"""
Test Vision Transformer Lung Cancer Detection
"""

import requests
import json

def test_vit_lung():
    """Test if Vision Transformer is working"""
    
    # Test image
    image_path = "organ_dataset\\lung\\Malignant case (13).jpg"
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post("http://127.0.0.1:8000/predict/auto", files=files, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        
        print("Lung Cancer Detection Results:")
        print(f"   Organ: {result.get('organ', 'Unknown')}")
        print(f"   Diagnosis: {result.get('diagnosis', 'Unknown')}")
        print(f"   Confidence: {result.get('diagnosis_confidence_pct', 0)}%")
        print(f"   Method: {result.get('method', 'Unknown')}")
        
        # Check explainability
        explain = result.get('explainability', {})
        print(f"   Explainability Method: {explain.get('method', 'Unknown')}")
        
        if 'attention_maps' in explain:
            print("   Vision Transformer Attention Maps Available!")
        elif 'grad_cam' in explain:
            print("   Grad-CAM Heatmap Available!")
        
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    print("Testing Vision Transformer Lung Cancer Detection...")
    print("=" * 60)
    
    result = test_vit_lung()
    
    if result:
        print("\nTest Complete!")
        print("Check if Vision Transformer is being used:")
        if result.get('method') == 'Vision Transformer':
            print("   SUCCESS: Using Vision Transformer!")
        else:
            print(f"   Using: {result.get('method')} (fallback)")
    else:
        print("Test Failed!")
