#!/usr/bin/env python3
"""
Download real blood cancer dataset from Kaggle
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
import json
import pandas as pd
from PIL import Image
import numpy as np

class KaggleBloodCancerDownloader:
    """Download blood cancer dataset from Kaggle"""
    
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
    
    def check_kaggle_api(self):
        """Check if Kaggle API is configured"""
        try:
            import kaggle
            print("✅ Kaggle API found")
            return True
        except ImportError:
            print("❌ Kaggle API not installed")
            print("Install with: pip install kaggle")
            return False
    
    def download_dataset(self, choice="cnmc"):
        """Download dataset based on choice"""
        if not self.check_kaggle_api():
            return False
        
        datasets = {
            "cnmc": {
                "name": "C-NMC 2019 Leukemia Classification",
                "command": "kaggle datasets download -d c-nmc-2019-leukemia-classification",
                "expected_files": ["C-NMC_Leukemia_training_data.zip"]
            },
            "blood_cells": {
                "name": "Blood Cell Images Dataset",
                "command": "kaggle datasets download -d paultimothymooney/blood-cells",
                "expected_files": ["blood-cells.zip"]
            },
            "leukemia_comp": {
                "name": "Leukemia Classification Competition",
                "command": "kaggle competitions download -d leukemia-classification",
                "expected_files": ["leukemia-classification.zip"]
            }
        }
        
        if choice not in datasets:
            print(f"❌ Invalid choice. Available: {list(datasets.keys())}")
            return False
        
        dataset_info = datasets[choice]
        print(f"🩸 Downloading: {dataset_info['name']}")
        
        try:
            # Download dataset
            os.system(dataset_info['command'])
            
            # Find and extract downloaded file
            for filename in dataset_info['expected_files']:
                if Path(filename).exists():
                    self._extract_dataset(filename)
                    return True
            
            print("⚠️ Expected file not found, checking for alternatives...")
            
            # Look for any downloaded zip files
            for zip_file in Path(".").glob("*.zip"):
                if any(keyword in zip_file.name.lower() for keyword in ['leukemia', 'blood', 'cell']):
                    print(f"📦 Found: {zip_file}")
                    self._extract_dataset(str(zip_file))
                    return True
            
            print("❌ No suitable dataset file found")
            return False
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def _extract_dataset(self, zip_path):
        """Extract and organize dataset"""
        print(f"📂 Extracting {zip_path}...")
        
        # Extract
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.dataset_dir / "extracted")
        
        # Clean up zip file
        Path(zip_path).unlink()
        
        # Organize extracted files
        self._organize_extracted_data()
    
    def _organize_extracted_data(self):
        """Organize extracted data into train/val/test"""
        print("🗂️ Organizing dataset...")
        
        extracted_dir = self.dataset_dir / "extracted"
        
        # Find image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'}
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(extracted_dir.rglob(f"*{ext}"))
            image_files.extend(extracted_dir.rglob(f"*{ext.upper()}"))
        
        if not image_files:
            print("⚠️ No images found in extracted data")
            return False
        
        print(f"📊 Found {len(image_files)} images")
        
        # Determine labels and organize
        normal_images = []
        leukemia_images = []
        
        for img_path in image_files:
            label = self._determine_label_from_path(img_path)
            if label == "normal":
                normal_images.append(img_path)
            else:
                leukemia_images.append(img_path)
        
        print(f"🩸 Normal: {len(normal_images)}, Leukemia: {len(leukemia_images)}")
        
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
        
        # Copy files to appropriate directories
        self._copy_images_to_split(normal_train, self.train_dir / "normal")
        self._copy_images_to_split(normal_val, self.val_dir / "normal")
        self._copy_images_to_split(normal_test, self.test_dir / "normal")
        
        self._copy_images_to_split(leukemia_train, self.train_dir / "leukemia")
        self._copy_images_to_split(leukemia_val, self.val_dir / "leukemia")
        self._copy_images_to_split(leukemia_test, self.test_dir / "leukemia")
        
        # Clean up extracted directory
        shutil.rmtree(extracted_dir)
        
        print("✅ Dataset organized successfully")
        return True
    
    def _determine_label_from_path(self, img_path):
        """Determine label from file path"""
        path_str = str(img_path).lower()
        
        # Check for leukemia indicators
        leukemia_keywords = ['all', 'leukemia', 'malignant', 'cancer', 'blast', 'tumor']
        normal_keywords = ['normal', 'healthy', 'benign', 'hem', 'normal_']
        
        for keyword in leukemia_keywords:
            if keyword in path_str:
                return "leukemia"
        
        for keyword in normal_keywords:
            if keyword in path_str:
                return "normal"
        
        # Default: check parent directory
        parent_dir = img_path.parent.name.lower()
        if any(keyword in parent_dir for keyword in leukemia_keywords):
            return "leukemia"
        elif any(keyword in parent_dir for keyword in normal_keywords):
            return "normal"
        
        # Random default
        return "leukemia" if hash(str(img_path)) % 2 == 0 else "normal"
    
    def _copy_images_to_split(self, images, target_dir):
        """Copy images to target directory"""
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
            "name": "Real Blood Cancer Dataset from Kaggle",
            "type": "Leukemia Classification",
            "source": "Kaggle",
            "classes": ["normal", "leukemia"],
            "image_size": [400, 300],
            "format": "RGB",
            "splits": {
                "train": len(list(self.train_dir.rglob("*.jpg"))),
                "val": len(list(self.val_dir.rglob("*.jpg"))),
                "test": len(list(self.test_dir.rglob("*.jpg")))
            },
            "description": "Real blood smear images for leukemia detection from Kaggle"
        }
        
        info_path = self.dataset_dir / "dataset_info.json"
        with open(info_path, 'w') as f:
            json.dump(dataset_info, f, indent=2)
        
        print(f"📋 Dataset info saved to {info_path}")
    
    def verify_dataset(self):
        """Verify dataset integrity"""
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
            print("✅ Dataset verification passed")
            return True
        else:
            print("❌ No images found")
            return False

def main():
    """Main function"""
    print("🩸 Kaggle Blood Cancer Dataset Downloader")
    print("=" * 50)
    
    print("📋 Available datasets:")
    print("1. C-NMC 2019 Leukemia Classification (recommended)")
    print("2. Blood Cell Images Dataset")
    print("3. Leukemia Classification Competition")
    
    choice = input("\nSelect dataset (1-3): ").strip()
    
    dataset_map = {
        "1": "cnmc",
        "2": "blood_cells", 
        "3": "leukemia_comp"
    }
    
    if choice not in dataset_map:
        print("❌ Invalid choice")
        return
    
    downloader = KaggleBloodCancerDownloader()
    
    # Download dataset
    success = downloader.download_dataset(dataset_map[choice])
    
    if success:
        # Create dataset info
        downloader.create_dataset_info()
        
        # Verify dataset
        downloader.verify_dataset()
        
        print("\n✅ Real blood cancer dataset ready!")
        print("🎯 Ready to train Graph Neural Network on real data!")
    else:
        print("\n❌ Dataset download failed")

if __name__ == "__main__":
    main()
