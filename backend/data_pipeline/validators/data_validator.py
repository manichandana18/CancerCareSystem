"""
Data validation utilities for CancerCare AI pipeline
Ensures data quality and consistency across cancer types
"""

import os
import json
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

class DataValidator:
    """Validates medical imaging data for cancer detection"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Supported image formats
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
        
        # Minimum image requirements
        self.min_image_size = (64, 64)
        self.max_image_size = (4096, 4096)
        self.max_file_size_mb = 50
        
    def validate_dataset_structure(self, dataset_path: str) -> Dict:
        """
        Validate the structure of a dataset
        
        Args:
            dataset_path: Path to the dataset directory
            
        Returns:
            Validation report
        """
        dataset_path = Path(dataset_path)
        report = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "statistics": {}
        }
        
        # Check required directories
        required_dirs = ["train", "val", "test"]
        for dir_name in required_dirs:
            dir_path = dataset_path / dir_name
            if not dir_path.exists():
                report["valid"] = False
                report["errors"].append(f"Missing required directory: {dir_name}")
            else:
                file_count = len([f for f in dir_path.iterdir() if f.is_file()])
                report["statistics"][f"{dir_name}_files"] = file_count
                
                if file_count == 0:
                    report["warnings"].append(f"Directory {dir_name} is empty")
        
        # Check metadata file
        metadata_file = dataset_path / "metadata.json"
        if not metadata_file.exists():
            report["valid"] = False
            report["errors"].append("Missing metadata.json file")
        
        return report
    
    def validate_image_file(self, image_path: str) -> Dict:
        """
        Validate a single image file
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Validation report
        """
        image_path = Path(image_path)
        report = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "file_info": {}
        }
        
        # Check file extension
        if image_path.suffix.lower() not in self.supported_formats:
            report["valid"] = False
            report["errors"].append(f"Unsupported file format: {image_path.suffix}")
            return report
        
        # Check file size
        file_size_mb = image_path.stat().st_size / (1024 * 1024)
        report["file_info"]["size_mb"] = round(file_size_mb, 2)
        
        if file_size_mb > self.max_file_size_mb:
            report["valid"] = False
            report["errors"].append(f"File too large: {file_size_mb:.2f}MB (max: {self.max_file_size_mb}MB)")
        
        # Try to load and validate image
        try:
            image = cv2.imread(str(image_path))
            if image is None:
                report["valid"] = False
                report["errors"].append("Cannot read image file (corrupted or invalid)")
                return report
            
            # Check image dimensions
            height, width = image.shape[:2]
            report["file_info"]["dimensions"] = f"{width}x{height}"
            report["file_info"]["channels"] = image.shape[2] if len(image.shape) > 2 else 1
            
            if width < self.min_image_size[0] or height < self.min_image_size[1]:
                report["valid"] = False
                report["errors"].append(f"Image too small: {width}x{height} (min: {self.min_image_size[0]}x{self.min_image_size[1]})")
            
            if width > self.max_image_size[0] or height > self.max_image_size[1]:
                report["warnings"].append(f"Large image: {width}x{height} (may slow processing)")
            
            # Check for corrupted data
            if np.isnan(image).any():
                report["valid"] = False
                report["errors"].append("Image contains NaN values")
            
            if np.isinf(image).any():
                report["valid"] = False
                report["errors"].append("Image contains infinite values")
            
        except Exception as e:
            report["valid"] = False
            report["errors"].append(f"Error processing image: {str(e)}")
        
        return report
    
    def validate_dataset_batch(self, dataset_path: str, sample_size: int = 50) -> Dict:
        """
        Validate a sample of images from a dataset
        
        Args:
            dataset_path: Path to the dataset directory
            sample_size: Number of images to sample from each directory
            
        Returns:
            Batch validation report
        """
        dataset_path = Path(dataset_path)
        report = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "statistics": {
                "total_files_checked": 0,
                "valid_files": 0,
                "invalid_files": 0,
                "file_issues": {}
            }
        }
        
        # Check each split directory
        for split_dir in ["train", "val", "test"]:
            split_path = dataset_path / split_dir
            if not split_path.exists():
                continue
            
            # Get image files
            image_files = []
            for ext in self.supported_formats:
                image_files.extend(split_path.glob(f"*{ext}"))
                image_files.extend(split_path.glob(f"*{ext.upper()}"))
            
            # Sample files
            sample_files = image_files[:sample_size] if len(image_files) > sample_size else image_files
            
            split_report = {
                "total_files": len(image_files),
                "checked_files": len(sample_files),
                "valid_files": 0,
                "invalid_files": 0,
                "issues": []
            }
            
            for image_file in sample_files:
                file_report = self.validate_image_file(str(image_file))
                report["statistics"]["total_files_checked"] += 1
                
                if file_report["valid"]:
                    split_report["valid_files"] += 1
                    report["statistics"]["valid_files"] += 1
                else:
                    split_report["invalid_files"] += 1
                    report["statistics"]["invalid_files"] += 1
                    split_report["issues"].extend(file_report["errors"])
                    report["errors"].extend([f"{split_dir}/{image_file.name}: {error}" for error in file_report["errors"]])
                
                if file_report["warnings"]:
                    report["warnings"].extend([f"{split_dir}/{image_file.name}: {warning}" for warning in file_report["warnings"]])
            
            report["statistics"]["file_issues"][split_dir] = split_report
        
        # Overall validity
        if report["statistics"]["invalid_files"] > 0:
            report["valid"] = False
        
        return report
    
    def generate_quality_report(self, dataset_path: str) -> str:
        """
        Generate a comprehensive quality report for a dataset
        
        Args:
            dataset_path: Path to the dataset directory
            
        Returns:
            Formatted quality report string
        """
        # Validate structure
        structure_report = self.validate_dataset_structure(dataset_path)
        
        # Validate sample of images
        batch_report = self.validate_dataset_batch(dataset_path)
        
        # Generate report
        report_lines = [
            "=" * 60,
            "CANCERCARE AI DATASET QUALITY REPORT",
            "=" * 60,
            f"Dataset: {dataset_path}",
            f"Overall Valid: {'✅ YES' if batch_report['valid'] else '❌ NO'}",
            "",
            "STRUCTURE VALIDATION:",
            f"Valid Structure: {'✅ YES' if structure_report['valid'] else '❌ NO'}"
        ]
        
        if structure_report["errors"]:
            report_lines.extend(["❌ Structure Errors:"] + structure_report["errors"])
        
        if structure_report["warnings"]:
            report_lines.extend(["⚠️ Structure Warnings:"] + structure_report["warnings"])
        
        report_lines.extend([
            "",
            "STATISTICS:",
            f"Total Files Checked: {batch_report['statistics']['total_files_checked']}",
            f"Valid Files: {batch_report['statistics']['valid_files']}",
            f"Invalid Files: {batch_report['statistics']['invalid_files']}",
            ""
        ])
        
        for split, stats in batch_report["statistics"]["file_issues"].items():
            report_lines.extend([
                f"{split.upper()} DIRECTORY:",
                f"  Total Files: {stats['total_files']}",
                f"  Files Checked: {stats['checked_files']}",
                f"  Valid Files: {stats['valid_files']}",
                f"  Invalid Files: {stats['invalid_files']}",
                ""
            ])
        
        if batch_report["errors"]:
            report_lines.extend(["❌ FILE ERRORS:"] + batch_report["errors"][:10])
            if len(batch_report["errors"]) > 10:
                report_lines.append(f"... and {len(batch_report['errors']) - 10} more errors")
        
        if batch_report["warnings"]:
            report_lines.extend(["⚠️ FILE WARNINGS:"] + batch_report["warnings"][:10])
            if len(batch_report["warnings"]) > 10:
                report_lines.append(f"... and {len(batch_report['warnings']) - 10} more warnings")
        
        report_lines.extend([
            "",
            "=" * 60,
            "END OF REPORT",
            "=" * 60
        ])
        
        return "\n".join(report_lines)

# Example usage
if __name__ == "__main__":
    validator = DataValidator()
    
    # Validate a dataset
    dataset_path = "data_pipeline/datasets/bone_cancer"
    quality_report = validator.generate_quality_report(dataset_path)
    print(quality_report)
