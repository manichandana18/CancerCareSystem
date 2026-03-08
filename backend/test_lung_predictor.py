#!/usr/bin/env python3
"""
Direct test of lung predictor
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

try:
    from app.lung.lung_predictor import predict_lung_cancer
    
    # Load real image
    with open("organ_dataset\\lung\\Malignant case (13).jpg", "rb") as f:
        image_bytes = f.read()
    
    # Test prediction
    result = predict_lung_cancer(image_bytes)
    
    print("DIRECT LUNG PREDICTOR TEST:")
    print("=" * 40)
    print(f"Diagnosis: {result.get('diagnosis', 'Unknown')}")
    print(f"Confidence: {result.get('diagnosis_confidence', 0):.3f}")
    print(f"Method: {result.get('method', 'Unknown')}")
    print(f"Model Type: {result.get('model_type', 'Unknown')}")
    
    if 'probabilities' in result:
        print("Probabilities:")
        for cls, prob in result['probabilities'].items():
            print(f"  {cls}: {prob:.3f}")
    
    print("\nSUCCESS: Direct lung predictor working!")
    
except ImportError as e:
    print(f"IMPORT FAILED: {e}")
except Exception as e:
    print(f"ERROR: {e}")

print("\nDirect lung predictor test complete!")
