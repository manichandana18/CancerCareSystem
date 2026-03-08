"""
Test with simulated real medical image characteristics
"""

import sys
from pathlib import Path
import numpy as np
from PIL import Image
import io

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def create_simulated_bone_xray():
    """Create a simulated bone X-ray image"""
    # Create a grayscale image with bone-like characteristics
    width, height = 400, 400  # Square aspect ratio for bone
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Fill with moderate brightness (typical for bone X-rays)
    img_array[:, :, :] = 80  # Gray background
    
    # Add some bone-like structures (brighter areas)
    img_array[100:300, 150:250] = 150  # Bone shaft
    img_array[50:100, 140:160] = 120  # Upper bone
    img_array[300:350, 140:160] = 120  # Lower bone
    
    # Add some noise/texture
    noise = np.random.normal(0, 20, (height, width, 3))
    img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(img_array)

def create_simulated_lung_xray():
    """Create a simulated lung X-ray image"""
    # Create a grayscale image with lung-like characteristics
    width, height = 500, 400  # Wide aspect ratio for lung
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Fill with moderate brightness
    img_array[:, :, :] = 70  # Darker background for lung
    
    # Add lung fields (darker areas)
    img_array[50:350, 50:200] = 50  # Left lung
    img_array[50:350, 300:450] = 50  # Right lung
    
    # Add heart shadow (brighter area in center)
    img_array[150:250, 200:300] = 100
    
    # Add ribs (horizontal lines)
    for i in range(50, 350, 30):
        img_array[i:i+2, :] = 90
    
    # Add some noise
    noise = np.random.normal(0, 15, (height, width, 3))
    img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(img_array)

def create_simulated_brain_mri():
    """Create a simulated brain MRI image"""
    # Create a grayscale image with brain-like characteristics
    width, height = 350, 350  # Square aspect ratio for brain
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Fill with moderate brightness
    img_array[:, :, :] = 90  # Gray background
    
    # Add brain-like structures
    # Outer brain matter
    img_array[50:300, 50:300] = 100
    
    # Ventricles (darker center)
    img_array[150:200, 150:200] = 70
    
    # Add some texture
    noise = np.random.normal(0, 10, (height, width, 3))
    img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(img_array)

def test_simulated_medical_images():
    """Test with simulated medical images"""
    
    print("🏥 TESTING SIMULATED MEDICAL IMAGES")
    print("=" * 60)
    print("Testing with created medical image simulations")
    print("=" * 60)
    
    # Test simulated bone X-ray
    print("--- TEST 1: Simulated Bone X-ray ---")
    bone_image = create_simulated_bone_xray()
    bone_bytes = io.BytesIO()
    bone_image.save(bone_bytes, format='JPEG')
    bone_bytes.seek(0)
    
    result1 = auto_predict(bone_bytes.getvalue(), filename_hint="bone_xray.jpg")
    print(f"Expected: BONE - NORMAL")
    print(f"Detected: {result1.get('organ')} - {result1.get('diagnosis')}")
    print(f"Confidence: {result1.get('diagnosis_confidence_pct', 0)}%")
    
    if result1.get('organ', '').lower() == 'bone':
        print("✅ CORRECT: Detected as BONE")
    else:
        print(f"❌ INCORRECT: Should detect BONE, got {result1.get('organ')}")
    
    print()
    
    # Test simulated lung X-ray
    print("--- TEST 2: Simulated Lung X-ray ---")
    lung_image = create_simulated_lung_xray()
    lung_bytes = io.BytesIO()
    lung_image.save(lung_bytes, format='JPEG')
    lung_bytes.seek(0)
    
    result2 = auto_predict(lung_bytes.getvalue(), filename_hint="lung_xray.jpg")
    print(f"Expected: LUNG - NORMAL")
    print(f"Detected: {result2.get('organ')} - {result2.get('diagnosis')}")
    print(f"Confidence: {result2.get('diagnosis_confidence_pct', 0)}%")
    
    if result2.get('organ', '').lower() == 'lung':
        print("✅ CORRECT: Detected as LUNG")
    else:
        print(f"❌ INCORRECT: Should detect LUNG, got {result2.get('organ')}")
    
    print()
    
    # Test simulated brain MRI
    print("--- TEST 3: Simulated Brain MRI ---")
    brain_image = create_simulated_brain_mri()
    brain_bytes = io.BytesIO()
    brain_image.save(brain_bytes, format='JPEG')
    brain_bytes.seek(0)
    
    result3 = auto_predict(brain_bytes.getvalue(), filename_hint="brain_mri.jpg")
    print(f"Expected: BRAIN - NORMAL")
    print(f"Detected: {result3.get('organ')} - {result3.get('diagnosis')}")
    print(f"Confidence: {result3.get('diagnosis_confidence_pct', 0)}%")
    
    if result3.get('organ', '').lower() == 'brain':
        print("✅ CORRECT: Detected as BRAIN")
    else:
        print(f"❌ INCORRECT: Should detect BRAIN, got {result3.get('organ')}")
    
    print()
    print("=" * 60)
    print("🎯 SIMULATED IMAGE ANALYSIS:")
    
    correct_count = sum(1 for r in [result1, result2, result3] 
                      if r.get('organ', '').lower() in ['bone', 'lung', 'brain'])
    total_count = 3
    
    print(f"Correct detections: {correct_count}/{total_count}")
    
    if correct_count == total_count:
        print("✅ SUCCESS: Organ detection working correctly!")
    elif correct_count >= 2:
        print("⚠️ PARTIAL: Most organ detection working")
    else:
        print("❌ PROBLEM: Organ detection needs improvement")

if __name__ == "__main__":
    test_simulated_medical_images()
