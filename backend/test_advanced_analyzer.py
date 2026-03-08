"""
Test the advanced medical image analyzer
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from advanced_image_analyzer import analyze_medical_image_content

def test_advanced_analyzer():
    """Test the advanced medical image analyzer"""
    
    print("🔬 TESTING ADVANCED MEDICAL IMAGE ANALYZER")
    print("=" * 60)
    print("This system analyzes ACTUAL medical image content")
    print("=" * 60)
    
    # Test with the image you have
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    try:
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"Testing image: {test_image_path}")
        print()
        
        # Analyze the image
        result = analyze_medical_image_content(image_bytes)
        
        print("🎯 ANALYSIS RESULTS:")
        print(f"Detected Organ: {result.get('organ', 'Unknown')}")
        print(f"Confidence: {result.get('confidence', 0):.3f} ({result.get('confidence', 0)*100:.1f}%)")
        print(f"Analysis Method: {result.get('analysis_method', 'Unknown')}")
        
        # Show all organ scores
        all_scores = result.get('all_scores', {})
        if all_scores:
            print("\n📊 ALL ORGAN SCORES:")
            for organ, score in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
                print(f"  {organ}: {score:.3f} ({score*100:.1f}%)")
        
        # Show features
        features = result.get('features', {})
        if features:
            print("\n🔍 IMAGE FEATURES:")
            print(f"  Aspect Ratio: {features.get('aspect_ratio', 0):.3f}")
            print(f"  Dimensions: {features.get('width', 0)} x {features.get('height', 0)}")
            print(f"  Brightness: {features.get('mean_brightness', 0):.1f}")
            print(f"  Edge Density: {features.get('edge_density', 0):.4f}")
            print(f"  Gradient: {features.get('mean_gradient', 0):.1f}")
            print(f"  Contour Ratio: {features.get('contour_ratio', 0):.3f}")
        
        print("\n" + "="*60)
        
        # Determine if this looks correct
        detected_organ = result.get('organ', '').lower()
        confidence = result.get('confidence', 0)
        
        if confidence > 0.6:
            print(f"✅ HIGH CONFIDENCE: {detected_organ.upper()} detected with {confidence*100:.1f}% confidence")
            print("🎉 Advanced analysis is working!")
        elif confidence > 0.4:
            print(f"⚠️ MEDIUM CONFIDENCE: {detected_organ.upper()} detected with {confidence*100:.1f}% confidence")
            print("🔧 Analysis is working but could be improved")
        else:
            print(f"❌ LOW CONFIDENCE: {detected_organ.upper()} detected with {confidence*100:.1f}% confidence")
            print("🚨 Analysis needs improvement")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_advanced_analyzer()
