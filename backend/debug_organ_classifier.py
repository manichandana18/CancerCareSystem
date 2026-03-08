"""
Debug script to test organ classifier performance
"""

import os
import numpy as np
from PIL import Image
import io
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.organ_classifier import predict_organ, preprocess_image, _get_organ_model

def test_organ_classifier():
    """Test the organ classifier with sample predictions"""
    
    print("🔍 Testing Organ Classifier...")
    
    # Load the model
    try:
        model = _get_organ_model()
        print(f"✅ Model loaded successfully")
        print(f"📊 Model input shape: {model.input_shape}")
        print(f"🎯 Model output shape: {model.output_shape}")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return
    
    # Test with a dummy image to see raw predictions
    print("\n🧪 Testing with dummy image...")
    
    # Create a dummy RGB image (224x224)
    dummy_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    dummy_pil = Image.fromarray(dummy_image)
    dummy_bytes = io.BytesIO()
    dummy_pil.save(dummy_bytes, format='JPEG')
    dummy_bytes = dummy_bytes.getvalue()
    
    # Test prediction
    result = predict_organ(dummy_bytes)
    print(f"🎯 Prediction result: {result}")
    
    # Get raw model output
    try:
        processed_img = preprocess_image(dummy_bytes)
        raw_pred = model.predict(processed_img)[0]
        print(f"📊 Raw model output: {raw_pred}")
        print(f"📊 Raw output shape: {raw_pred.shape}")
        print(f"📊 Raw output type: {type(raw_pred)}")
        
        if len(raw_pred) == 2:
            print(f"🦴 Bone probability: {raw_pred[0]:.4f}")
            print(f"🫁 Lung probability: {raw_pred[1]:.4f}")
        elif len(raw_pred) == 1:
            print(f"🫁 Lung probability (sigmoid): {raw_pred[0]:.4f}")
            print(f"🦴 Bone probability (1-lung): {1-raw_pred[0]:.4f}")
        
    except Exception as e:
        print(f"❌ Error getting raw prediction: {e}")
    
    # Test multiple random images
    print("\n🎲 Testing multiple random images...")
    for i in range(5):
        dummy_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        dummy_pil = Image.fromarray(dummy_image)
        dummy_bytes = io.BytesIO()
        dummy_pil.save(dummy_bytes, format='JPEG')
        dummy_bytes = dummy_bytes.getvalue()
        
        result = predict_organ(dummy_bytes)
        print(f"Test {i+1}: {result['organ']} ({result['confidence']}%)")

if __name__ == "__main__":
    test_organ_classifier()
