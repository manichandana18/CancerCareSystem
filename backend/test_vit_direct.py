#!/usr/bin/env python3
"""
Direct test of Vision Transformer
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

try:
    from vision_transformer_lung import VisionTransformerLung
    print("SUCCESS: Vision Transformer imported")
    
    # Create ViT instance
    vit = VisionTransformerLung()
    print("SUCCESS: ViT instance created")
    
    # Try to load model
    loaded = vit.load_pretrained_model()
    print(f"Model loading: {'SUCCESS' if loaded else 'FAILED (using new model)'}")
    
    # Test with a real image
    from PIL import Image
    import numpy as np
    
    # Load real image
    try:
        with open("organ_dataset\\lung\\Malignant case (13).jpg", "rb") as f:
            image_bytes = f.read()
        
        # Try prediction
        result = vit.predict_lung_cancer(image_bytes)
        print("SUCCESS: ViT prediction worked")
        print(f"   Method: {result.get('method', 'Unknown')}")
        print(f"   Diagnosis: {result.get('diagnosis', 'Unknown')}")
        print(f"   Confidence: {result.get('diagnosis_confidence', 0):.3f}")
    except Exception as e:
        print(f"PREDICTION FAILED: {e}")
    
except ImportError as e:
    print(f"IMPORT FAILED: {e}")
except Exception as e:
    print(f"ERROR: {e}")

print("\nDirect ViT test complete!")
