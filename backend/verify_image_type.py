"""
Verify what type of medical image this actually is
"""

import sys
from pathlib import Path
from PIL import Image
import numpy as np

# Add backend to path
sys.path.append(str(Path(__file__).parent))

def verify_image_type():
    """Verify the actual type of medical image"""
    
    print("🔍 VERIFYING ACTUAL IMAGE TYPE")
    print("=" * 50)
    
    # Test with the image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Analyzing image: {test_image_path}")
        print()
        
        # Open and analyze the image
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image_array = np.array(image)
        
        print("📊 IMAGE CHARACTERISTICS:")
        print(f"Dimensions: {image_array.shape}")
        print(f"Aspect Ratio: {image_array.shape[1] / image_array.shape[0]:.3f}")
        
        # Color analysis
        print(f"\n🎨 COLOR ANALYSIS:")
        print(f"Red mean: {np.mean(image_array[:,:,0]):.1f}")
        print(f"Green mean: {np.mean(image_array[:,:,1]):.1f}")
        print(f"Blue mean: {np.mean(image_array[:,:,2]):.1f}")
        print(f"Overall brightness: {np.mean(image_array):.1f}")
        
        # Check if it looks like different medical image types
        aspect_ratio = image_array.shape[1] / image_array.shape[0]
        brightness = np.mean(image_array)
        
        print(f"\n🔍 MEDICAL IMAGE TYPE ANALYSIS:")
        
        # Lung X-ray characteristics
        if aspect_ratio > 1.5 and brightness < 120:
            print("✅ Characteristics match LUNG X-ray:")
            print(f"   - Wide aspect ratio ({aspect_ratio:.2f})")
            print(f"   - Lower brightness ({brightness:.1f})")
            print("   - Typical chest X-ray proportions")
        elif aspect_ratio < 1.3 and brightness > 100:
            print("✅ Characteristics match BONE X-ray:")
            print(f"   - More square aspect ratio ({aspect_ratio:.2f})")
            print(f"   - Higher brightness ({brightness:.1f})")
            print("   - Typical bone X-ray proportions")
        elif brightness > 130:
            print("✅ Characteristics match SKIN image:")
            print(f"   - High brightness ({brightness:.1f})")
            print(f"   - Color-rich appearance")
            print("   - Typical skin lesion characteristics")
        elif aspect_ratio < 1.2:
            print("✅ Characteristics match BRAIN MRI:")
            print(f"   - Square aspect ratio ({aspect_ratio:.2f})")
            print(f"   - Medium brightness ({brightness:.1f})")
            print("   - Typical brain scan proportions")
        else:
            print("❓ Unclear image type - mixed characteristics")
            print(f"   - Aspect ratio: {aspect_ratio:.2f}")
            print(f"   - Brightness: {brightness:.1f}")
        
        print(f"\n🎯 CONCLUSION:")
        print(f"Based on the image characteristics:")
        print(f"- Aspect Ratio: {aspect_ratio:.3f}")
        print(f"- Brightness: {brightness:.1f}")
        print(f"- Color richness: {np.std(image_array):.1f}")
        
        if brightness > 130:
            print("🔴 This appears to be a SKIN CANCER image")
            print("   (high brightness, color-rich, not typical X-ray)")
        elif aspect_ratio > 1.5:
            print("🔵 This appears to be a LUNG X-ray image")
            print("   (wide aspect ratio, typical chest X-ray)")
        else:
            print("🟡 This appears to be a BONE X-ray image")
            print("   (more square, typical bone X-ray)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import io
    verify_image_type()
