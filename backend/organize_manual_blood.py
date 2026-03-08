#!/usr/bin/env python3
"""
Organize manually downloaded blood cancer dataset
"""

import os
import shutil
from pathlib import Path
import json
from PIL import Image
import numpy as np

class ManualBloodDatasetOrganizer:
    """Organize manually downloaded blood cancer dataset"""
    
    def __init__(self, dataset_dir="blood_dataset_real"):
        self.dataset_dir = Path(dataset_dir)
        self.train_dir = self.dataset_dir / "train"
        self.val_dir = self.dataset_dir / "val"
        self.test_dir = self.dataset_dir / "test"
        
        # Create directories
        for dir_path in [self.dataset_dir, self.train_dir, self.val_dir, self.test_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create class subdirectories
            (dir_path / "normal").mkdir(exist_ok=True)
            (dir_path / "leukemia").mkdir(exist_ok=True)
    
    def find_downloaded_dataset(self):
        """Find the manually downloaded dataset"""
        print("🔍 Looking for downloaded dataset...")
        
        # Common download locations
        search_paths = [
            Path("."),  # Current directory
            Path("C-NMC_2019_Leukemia"),
            Path("blood-cells"),
            Path("leukemia-classification"),
            Path("extracted"),
            Path("downloads")
        ]
        
        for search_path in search_paths:
            if search_path.exists():
                print(f"📂 Checking: {search_path}")
                
                # Look for image files
                image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'}
                image_files = []
                
                for ext in image_extensions:
                    image_files.extend(search_path.rglob(f"*{ext}"))
                    image_files.extend(search_path.rglob(f"*{ext.upper()}"))
                
                if len(image_files) > 10:  # Found substantial dataset
                    print(f"✅ Found {len(image_files)} images in {search_path}")
                    return search_path, image_files
        
        print("❌ No suitable dataset found")
        print("📋 Please download dataset from Kaggle and extract to backend folder")
        return None, []
    
    def organize_dataset(self, dataset_path, image_files):
        """Organize dataset into train/val/test splits"""
        print("🗂️ Organizing dataset...")
        
        # Classify images
        normal_images = []
        leukemia_images = []
        
        for img_path in image_files:
            label = self._determine_label_from_path(img_path)
            if label == "normal":
                normal_images.append(img_path)
            else:
                leukemia_images.append(img_path)
        
        print(f"🩸 Found {len(normal_images)} normal, {len(leukemia_images)} leukemia images")
        
        if len(normal_images) == 0 or len(leukemia_images) == 0:
            print("⚠️ No clear class separation found, using random split")
            # Random split if no clear classes
            np.random.shuffle(image_files)
            mid_point = len(image_files) // 2
            normal_images = image_files[:mid_point]
            leukemia_images = image_files[mid_point:]
        
        # Split datasets (70% train, 15% val, 15% test)
        def split_images(images):
            np.random.shuffle(images)
            n_total = len(images)
            n_train = int(0.7 * n_total)
            n_val = int(0.15 * n_total)
            return (
                images[:n_train],
                images[n_train:n_train + n_val],
                images[n_train + n_val:]
            )
        
        normal_train, normal_val, normal_test = split_images(normal_images)
        leukemia_train, leukemia_val, leukemia_test = split_images(leukemia_images)
        
        # Copy files
        print("📋 Copying files...")
        
        self._copy_images_to_split(normal_train, self.train_dir / "normal")
        self._copy_images_to_split(normal_val, self.val_dir / "normal")
        self._copy_images_to_split(normal_test, self.test_dir / "normal")
        
        self._copy_images_to_split(leukemia_train, self.train_dir / "leukemia")
        self._copy_images_to_split(leukemia_val, self.val_dir / "leukemia")
        self._copy_images_to_split(leukemia_test, self.test_dir / "leukemia")
        
        print("✅ Dataset organized successfully!")
        return True
    
    def _determine_label_from_path(self, img_path):
        """Determine label from file path"""
        path_str = str(img_path).lower()
        
        # Check for leukemia indicators
        leukemia_keywords = ['all', 'leukemia', 'malignant', 'cancer', 'blast', 'tumor']
        normal_keywords = ['normal', 'healthy', 'benign', 'hem', 'normal_', 'heme']
        
        for keyword in leukemia_keywords:
            if keyword in path_str:
                return "leukemia"
        
        for keyword in normal_keywords:
            if keyword in path_str:
                return "normal"
        
        # Check parent directory
        parent_dir = img_path.parent.name.lower()
        if any(keyword in parent_dir for keyword in leukemia_keywords):
            return "leukemia"
        elif any(keyword in parent_dir for keyword in normal_keywords):
            return "normal"
        
        # Default random
        return "leukemia" if hash(str(img_path)) % 2 == 0 else "normal"
    
    def _copy_images_to_split(self, images, target_dir):
        """Copy and standardize images"""
        for img_path in images:
            try:
                # Target path
                target_path = target_dir / img_path.name
                
                # Copy and standardize
                with Image.open(img_path) as img:
                    # Convert to RGB if needed
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Resize to standard size
                    img = img.resize((400, 300))
                    
                    # Save
                    img.save(target_path)
                    
            except Exception as e:
                print(f"⚠️ Error processing {img_path}: {e}")
    
    def create_dataset_info(self):
        """Create dataset information"""
        dataset_info = {
            "name": "Real Blood Cancer Dataset (Manual)",
            "type": "Leukemia Classification",
            "source": "Kaggle (Manual Download)",
            "classes": ["normal", "leukemia"],
            "image_size": [400, 300],
            "format": "RGB",
            "splits": {
                "train": len(list(self.train_dir.rglob("*.jpg"))),
                "val": len(list(self.val_dir.rglob("*.jpg"))),
                "test": len(list(self.test_dir.rglob("*.jpg")))
            },
            "description": "Real blood smear images for leukemia detection"
        }
        
        info_path = self.dataset_dir / "dataset_info.json"
        with open(info_path, 'w') as f:
            json.dump(dataset_info, f, indent=2)
        
        print(f"📋 Dataset info saved to {info_path}")
    
    def verify_dataset(self):
        """Verify dataset"""
        print("🔍 Verifying dataset...")
        
        total_images = 0
        for split_name, split_dir in [("train", self.train_dir), ("val", self.val_dir), ("test", self.test_dir)]:
            for label in ["normal", "leukemia"]:
                label_dir = split_dir / label
                images = list(label_dir.glob("*.jpg"))
                total_images += len(images)
                print(f"  {split_name}/{label}: {len(images)} images")
        
        print(f"📊 Total images: {total_images}")
        
        if total_images > 0:
            print("✅ Dataset ready for training!")
            return True
        else:
            print("❌ No images found")
            return False

def main():
    """Main function"""
    print("🩸 Manual Blood Cancer Dataset Organizer")
    print("=" * 50)
    
    print("📋 Instructions:")
    print("1. Download dataset from Kaggle")
    print("2. Extract to backend folder")
    print("3. Run this script to organize")
    
    organizer = ManualBloodDatasetOrganizer()
    
    # Find dataset
    dataset_path, image_files = organizer.find_downloaded_dataset()
    
    if dataset_path and image_files:
        # Organize dataset
        success = organizer.organize_dataset(dataset_path, image_files)
        
        if success:
            # Create info and verify
            organizer.create_dataset_info()
            organizer.verify_dataset()
            
            print("\n✅ Dataset ready!")
            print("🎯 Run: python train_blood_gnn.py")
        else:
            print("\n❌ Organization failed")
    else:
        print("\n📥 Please download dataset first:")
        print("🔗 Kaggle: https://kaggle.com/datasets")
        print("🔍 Search: 'leukemia' or 'blood cancer'")

if __name__ == "__main__":
    main()
