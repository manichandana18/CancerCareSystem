"""
Debug the lung image detection issue
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from smart_organ_detector import smart_organ_detector

def debug_lung_detection():
    """Debug why lung image is detected as bone"""
    
    print("🔍 DEBUGGING LUNG IMAGE DETECTION")
    print("=" * 50)
    
    # Test with the lung image you have (named as bonecancer.jpg)
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print("This is actually a LUNG cancer image")
        print()
        
        # Test with correct filename
        print("--- Test 1: With correct filename 'lungcancer.jpg' ---")
        result1 = smart_organ_detector(image_bytes, filename_hint="lungcancer.jpg")
        
        print(f"Detected Organ: {result1.get('organ')}")
        print(f"Confidence: {result1.get('confidence')}")
        print(f"Method: {result1.get('method')}")
        
        debug1 = result1.get('debug', {})
        if 'confidence_breakdown' in debug1:
            breakdown1 = debug1['confidence_breakdown']
            print(f"Image Confidence: {breakdown1.get('image_confidence', 0)}")
            print(f"Filename Confidence: {breakdown1.get('filename_confidence', 0)}")
        print()
        
        # Test with wrong filename
        print("--- Test 2: With wrong filename 'bonecancer.jpg' ---")
        result2 = smart_organ_detector(image_bytes, filename_hint="bonecancer.jpg")
        
        print(f"Detected Organ: {result2.get('organ')}")
        print(f"Confidence: {result2.get('confidence')}")
        print(f"Method: {result2.get('method')}")
        
        debug2 = result2.get('debug', {})
        if 'confidence_breakdown' in debug2:
            breakdown2 = debug2['confidence_breakdown']
            print(f"Image Confidence: {breakdown2.get('image_confidence', 0)}")
            print(f"Filename Confidence: {breakdown2.get('filename_confidence', 0)}")
        print()
        
        # Test with no filename
        print("--- Test 3: With NO filename ---")
        result3 = smart_organ_detector(image_bytes, filename_hint=None)
        
        print(f"Detected Organ: {result3.get('organ')}")
        print(f"Confidence: {result3.get('confidence')}")
        print(f"Method: {result3.get('method')}")
        
        debug3 = result3.get('debug', {})
        if 'confidence_breakdown' in debug3:
            breakdown3 = debug3['confidence_breakdown']
            print(f"Image Confidence: {breakdown3.get('image_confidence', 0)}")
            print(f"Filename Confidence: {breakdown3.get('filename_confidence', 0)}")
        
        print()
        print("=" * 50)
        print("ANALYSIS:")
        
        # Determine what the image actually is
        image_organ_no_filename = result3.get('organ', 'unknown')
        image_confidence_no_filename = result3.get('confidence', 0)
        
        print(f"The image content analysis detects: {image_organ_no_filename}")
        print(f"Image analysis confidence: {image_confidence_no_filename}")
        
        if image_organ_no_filename.lower() == 'lung':
            print("✅ Image content is correctly detected as LUNG")
            if result2.get('organ').lower() == 'bone':
                print("❌ But filename 'bonecancer.jpg' is overriding the correct detection!")
                print("🔧 Need to fix the smart detector logic")
        elif image_organ_no_filename.lower() == 'bone':
            print("❌ Image content is being detected as BONE (incorrect)")
            print("🔧 Need to improve image analysis for lung detection")
        else:
            print(f"❓ Image content detected as {image_organ_no_filename} (need investigation)")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_lung_detection()
