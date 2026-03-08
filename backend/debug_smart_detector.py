"""
Debug the smart detector directly
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from smart_organ_detector import smart_organ_detector

def debug_smart_detector():
    """Debug smart detector directly"""
    
    print("🔍 DEBUGGING SMART DETECTOR DIRECTLY")
    print("=" * 50)
    
    # Test with the bone image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Test with wrong filename
        print("--- Testing with filename 'bloodcancer.jpg' ---")
        result = smart_organ_detector(image_bytes, filename_hint="bloodcancer.jpg")
        
        print(f"Detected Organ: {result.get('organ')}")
        print(f"Confidence: {result.get('confidence')}")
        print(f"Method: {result.get('method')}")
        
        debug_info = result.get('debug', {})
        print(f"Decision: {debug_info.get('decision', 'No decision info')}")
        
        if 'confidence_breakdown' in debug_info:
            breakdown = debug_info['confidence_breakdown']
            print(f"Image Confidence: {breakdown.get('image_confidence', 0)}")
            print(f"Filename Confidence: {breakdown.get('filename_confidence', 0)}")
        
        print()
        
        # Test with no filename
        print("--- Testing with NO filename ---")
        result2 = smart_organ_detector(image_bytes, filename_hint=None)
        
        print(f"Detected Organ: {result2.get('organ')}")
        print(f"Confidence: {result2.get('confidence')}")
        print(f"Method: {result2.get('method')}")
        
        debug_info2 = result2.get('debug', {})
        print(f"Decision: {debug_info2.get('decision', 'No decision info')}")
        
        if 'confidence_breakdown' in debug_info2:
            breakdown2 = debug_info2['confidence_breakdown']
            print(f"Image Confidence: {breakdown2.get('image_confidence', 0)}")
            print(f"Filename Confidence: {breakdown2.get('filename_confidence', 0)}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_smart_detector()
