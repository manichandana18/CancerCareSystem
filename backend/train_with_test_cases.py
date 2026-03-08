"""
Train the adaptive organ classifier with our test cases
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from adaptive_organ_classifier import train_organ_classifier

def train_with_known_cases():
    """Train the classifier with our known test cases"""
    
    print("🎓 TRAINING ADAPTIVE ORGAN CLASSIFIER")
    print("=" * 50)
    
    # Known training cases
    training_cases = [
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bone3.jpg",
            "organ": "bone",
            "name": "Normal Bone X-ray"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\bonecancer.jpg", 
            "organ": "bone",
            "name": "Cancerous Bone X-ray"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\normalbone1.jpg",
            "organ": "lung",
            "name": "Normal Lung X-ray"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\cancer3.jpg",
            "organ": "lung", 
            "name": "Cancerous Lung X-ray"
        },
        {
            "path": "C:\\Users\\Balaiah goud\\Downloads\\lungcancer1.jpg",
            "organ": "lung",
            "name": "Your Lung Cancer Image"
        }
    ]
    
    trained_count = 0
    
    for case in training_cases:
        print(f"\n📚 Training with: {case['name']}")
        print(f"   Expected organ: {case['organ']}")
        
        if not os.path.exists(case['path']):
            print("   ⏭️  Skipped - File not found")
            continue
            
        try:
            with open(case['path'], 'rb') as f:
                image_bytes = f.read()
            
            filename = os.path.basename(case['path'])
            success = train_organ_classifier(image_bytes, case['organ'], filename)
            
            if success:
                trained_count += 1
                print(f"   ✅ Trained successfully")
            else:
                print(f"   ❌ Training failed")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎯 TRAINING COMPLETE!")
    print(f"✅ Trained with {trained_count}/{len(training_cases)} cases")
    print(f"📁 Training data saved to: organ_classifier_training.json")
    print(f"🚀 Classifier is now ready for testing!")

if __name__ == "__main__":
    train_with_known_cases()
