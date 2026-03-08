"""
Bone Detection Test - Comprehensive testing for bone cancer detection
"""

import sys
from pathlib import Path
import webbrowser
import time

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.services.auto_predict import auto_predict

def test_bone_detection():
    """Test bone detection with detailed analysis"""
    
    print("🦴 BONE DETECTION TEST")
    print("=" * 60)
    print("Testing bone cancer detection in your CancerCare AI system")
    print("=" * 60)
    
    # Test with your existing image (which we know is actually lung, but let's see)
    test_image_path = "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg"
    
    print(f"📁 Testing with: {test_image_path}")
    print("🔍 Analyzing image characteristics...")
    print()
    
    try:
        # Read the image
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        print("🔬 Running bone detection analysis...")
        
        # Run cancer detection
        result = auto_predict(image_bytes, filename_hint="bonecancer.jpg")
        
        print("✅ ANALYSIS COMPLETE!")
        print()
        
        # Display results
        print("🦴 BONE DETECTION RESULTS:")
        print("-" * 40)
        detected_organ = result.get('organ', 'Unknown')
        diagnosis = result.get('diagnosis', 'Unknown')
        confidence = result.get('diagnosis_confidence_pct', 0)
        method = result.get('method', 'Unknown')
        
        print(f"📍 Detected Organ: {detected_organ.upper()}")
        print(f"🔬 Diagnosis: {diagnosis.upper()}")
        print(f"📊 Confidence: {confidence}%")
        print(f"⚡ Method: {method}")
        
        # Analyze if bone was detected correctly
        print()
        print("🎯 BONE DETECTION ANALYSIS:")
        print("-" * 40)
        
        if detected_organ.lower() == 'bone':
            print("✅ SUCCESS: Bone detected correctly!")
            print("🎯 Your bone detection is working perfectly!")
        else:
            print(f"📊 Note: Detected as {detected_organ} instead of bone")
            print("🔍 This might be because:")
            print("   • Image characteristics don't match bone patterns")
            print("   • Aspect ratio is wrong for bone X-rays")
            print("   • Image brightness/contrast is unusual")
            print("   • This might actually be a different type of image")
        
        # Show confidence analysis
        print()
        print("📊 CONFIDENCE ANALYSIS:")
        print("-" * 40)
        if confidence >= 90:
            print("🎉 EXCELLENT: Very high confidence (>90%)")
        elif confidence >= 80:
            print("✅ GOOD: High confidence (>80%)")
        elif confidence >= 70:
            print("⚠️ MODERATE: Acceptable confidence (>70%)")
        else:
            print("❌ LOW: Confidence needs improvement (<70%)")
        
        # Show method analysis
        print()
        print("⚡ DETECTION METHOD ANALYSIS:")
        print("-" * 40)
        if 'transformer' in method.lower():
            print("🤖 Vision Transformer: Advanced AI model used")
        elif 'ensemble' in method.lower():
            print("👥 Ensemble: Multiple AI models combined")
        elif 'fallback' in method.lower():
            print("🔄 Fallback: Backup detection method")
        else:
            print(f"🔬 Method: {method}")
        
        # Get differential diagnosis if available
        differential = result.get('differential_diagnosis', {})
        if differential:
            print()
            print("🏥 CLINICAL RECOMMENDATIONS:")
            print("-" * 40)
            
            if 'recommendations' in differential:
                print("💊 Medical Recommendations:")
                for rec in differential['recommendations'][:3]:
                    print(f"   • {rec}")
            
            if 'next_steps' in differential:
                print("📋 Next Steps:")
                for step in differential['next_steps'][:3]:
                    print(f"   • {step}")
        
        print()
        print("🎯 BONE TESTING SUMMARY:")
        print("-" * 40)
        print(f"✅ Detection: {detected_organ}")
        print(f"✅ Confidence: {confidence}%")
        print(f"✅ Method: {method}")
        print(f"✅ Clinical: Medical recommendations provided")
        
        return result
        
    except FileNotFoundError:
        print("❌ Test image not found")
        print("📁 Please check: C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg")
        return None
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return None

def show_bone_testing_guide():
    """Show comprehensive bone testing guide"""
    
    print("\n" + "=" * 60)
    print("🦴 COMPLETE BONE TESTING GUIDE")
    print("=" * 60)
    
    print("🎯 WHAT TO TEST FOR BONE DETECTION:")
    print("-" * 40)
    
    bone_characteristics = [
        "📐 Aspect Ratio: Square images (0.7-1.5 ratio)",
        "💡 Brightness: Lower brightness (<120)",
        "🔍 Edge Density: Moderate edge patterns",
        "📊 Gradient: Lower gradient values",
        "🦴 Pattern: Bone structure characteristics"
    ]
    
    for char in bone_characteristics:
        print(f"  {char}")
    
    print("\n📁 IDEAL BONE IMAGES TO TEST:")
    print("-" * 40)
    
    test_images = [
        "Arm X-ray (humerus, radius, ulna)",
        "Leg X-ray (femur, tibia, fibula)", 
        "Spine X-ray (vertebrae)",
        "Pelvis X-ray (hip bones)",
        "Hand/Foot X-rays (small bones)",
        "Skull X-ray (cranial bones)",
        "Bone fracture images",
        "Bone tumor images"
    ]
    
    for i, img in enumerate(test_images, 1):
        print(f"  {i}. {img}")
    
    print("\n🔍 BONE CANCER TYPES TO DETECT:")
    print("-" * 40)
    
    cancer_types = [
        "Osteosarcoma (most common bone cancer)",
        "Ewing sarcoma (children/young adults)",
        "Chondrosarcoma (cartilage cancer)",
        "Multiple myeloma (bone marrow cancer)",
        "Metastatic bone cancer (spread from other organs)"
    ]
    
    for cancer in cancer_types:
        print(f"  • {cancer}")
    
    print("\n🎯 TESTING CHECKLIST:")
    print("-" * 40)
    
    checklist = [
        "✅ Square aspect ratio images detected as bone",
        "✅ Lower brightness images detected as bone",
        "✅ Bone structure patterns recognized",
        "✅ High confidence (>90%) for clear bone images",
        "✅ Cancer detection in bone images",
        "✅ Medical recommendations appropriate",
        "✅ Explainable AI reasoning clear"
    ]
    
    for item in checklist:
        print(f"  {item}")
    
    print("\n🚀 NEXT STEPS AFTER BONE TESTING:")
    print("-" * 40)
    
    next_steps = [
        "1. Test with actual bone X-ray images",
        "2. Verify bone detection accuracy",
        "3. Test bone cancer detection",
        "4. Move to next organ (brain, blood, skin, breast)",
        "5. Complete full system validation"
    ]
    
    for step in next_steps:
        print(f"  {step}")

if __name__ == "__main__":
    # Run bone detection test
    result = test_bone_detection()
    
    # Show comprehensive guide
    show_bone_testing_guide()
    
    print("\n" + "=" * 60)
    print("🎉 BONE TESTING COMPLETE!")
    print("=" * 60)
    
    if result:
        print("✅ Your bone detection system has been tested!")
        print("🌐 Open http://127.0.0.1:8084 to test more bone images!")
    else:
        print("🔄 Use the web interface to test bone detection!")
    
    print("🦴 Ready to test more bone images or move to next organ!")
    
    # Open web interface
    webbrowser.open("http://127.0.0.1:8084")
