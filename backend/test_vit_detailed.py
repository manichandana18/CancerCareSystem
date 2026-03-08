#!/usr/bin/env python3
"""
Detailed test of Vision Transformer through API
"""

import requests
import json

def test_vit_detailed():
    """Test Vision Transformer with detailed output"""
    
    # Test image
    image_path = "organ_dataset\\lung\\Malignant case (13).jpg"
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post("http://127.0.0.1:8000/predict/auto", files=files, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        
        print("DETAILED LUNG CANCER RESULTS:")
        print("=" * 50)
        print(f"Organ: {result.get('organ', 'Unknown')}")
        print(f"Diagnosis: {result.get('diagnosis', 'Unknown')}")
        print(f"Confidence: {result.get('diagnosis_confidence_pct', 0)}%")
        print(f"Method: {result.get('method', 'Unknown')}")
        
        # Check all result fields
        print("\nALL RESULT FIELDS:")
        for key, value in result.items():
            if key != 'explainability':
                print(f"  {key}: {value}")
        
        # Check explainability in detail
        explain = result.get('explainability', {})
        print("\nEXPLAINABILITY DETAILS:")
        for key, value in explain.items():
            if key not in ['grad_cam', 'attention_maps']:
                print(f"  {key}: {value}")
        
        # Check if ViT features are present
        if 'attention_maps' in explain:
            print("\nVISION TRANSFORMER FEATURES:")
            attention = explain['attention_maps']
            if isinstance(attention, dict):
                for key, value in attention.items():
                    print(f"  {key}: {value}")
        
        return result
    else:
        print(f"ERROR: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    print("Detailed Vision Transformer Test...")
    print("=" * 60)
    
    result = test_vit_detailed()
    
    if result:
        print("\nANALYSIS:")
        method = result.get('method', 'Unknown')
        if method == 'Vision Transformer':
            print("SUCCESS: Vision Transformer is being used!")
        elif method == 'CNN Fallback':
            print("INFO: CNN fallback is being used")
        else:
            print(f"INFO: Method is '{method}'")
        
        # Check if ViT is available in explainability
        explain = result.get('explainability', {})
        if explain.get('method') == 'Vision Transformer Attention':
            print("SUCCESS: ViT attention is available in explainability!")
    else:
        print("Test failed!")
