"""
Setup script for adding new cancer types to CancerCare AI
Automates the entire setup process for new cancer detection models
"""

import os
import sys
import json
from pathlib import Path

# Add the parent directory to the path to import pipeline_manager
sys.path.append(str(Path(__file__).parent.parent))
from data_pipeline.pipeline_manager import CancerDataPipeline
from data_pipeline.validators.data_validator import DataValidator

class CancerTypeSetup:
    """Complete setup automation for new cancer types"""
    
    def __init__(self):
        self.pipeline = CancerDataPipeline()
        self.validator = DataValidator()
        
    def setup_cancer_type(self, cancer_type: str, description: str, data_source: str = None) -> dict:
        """
        Complete setup for a new cancer type
        
        Args:
            cancer_type: Name of cancer type (e.g., "brain_cancer")
            description: Description of the cancer type
            data_source: Source of dataset (optional)
            
        Returns:
            Setup report
        """
        report = {
            "cancer_type": cancer_type,
            "success": False,
            "steps_completed": [],
            "errors": [],
            "next_steps": []
        }
        
        try:
            # Step 1: Add cancer type to pipeline
            print(f"🔧 Step 1: Adding {cancer_type} to pipeline...")
            if self.pipeline.add_cancer_type(cancer_type, description):
                report["steps_completed"].append("✅ Added to pipeline")
                print("✅ Successfully added to pipeline")
            else:
                report["errors"].append("❌ Failed to add to pipeline")
                return report
            
            # Step 2: Create directory structure
            print(f"📁 Step 2: Creating directory structure...")
            dataset_path = Path(f"data_pipeline/datasets/{cancer_type}")
            if dataset_path.exists():
                report["steps_completed"].append("✅ Directory structure created")
                print("✅ Directory structure ready")
            else:
                report["errors"].append("❌ Failed to create directory structure")
                return report
            
            # Step 3: Initialize metadata
            print(f"📝 Step 3: Initializing metadata...")
            metadata_updates = {
                "data_source": data_source,
                "status": "setup_complete",
                "setup_date": str(Path.cwd()),
                "next_steps": [
                    "1. Collect and organize dataset",
                    "2. Validate data quality",
                    "3. Customize preprocessor",
                    "4. Train model",
                    "5. Evaluate performance"
                ]
            }
            
            if self.pipeline.update_metadata(cancer_type, metadata_updates):
                report["steps_completed"].append("✅ Metadata initialized")
                print("✅ Metadata initialized")
            else:
                report["errors"].append("❌ Failed to initialize metadata")
            
            # Step 4: Generate setup instructions
            print(f"📋 Step 4: Generating setup instructions...")
            instructions = self._generate_setup_instructions(cancer_type, description)
            report["setup_instructions"] = instructions
            report["steps_completed"].append("✅ Setup instructions generated")
            
            # Step 5: Create data collection template
            print(f"📊 Step 5: Creating data collection template...")
            self._create_data_collection_template(cancer_type)
            report["steps_completed"].append("✅ Data collection template created")
            
            report["success"] = True
            report["next_steps"] = [
                f"1. Collect dataset for {cancer_type}",
                f"2. Place images in data_pipeline/datasets/{cancer_type}/train/",
                f"3. Run: python data_pipeline/validators/data_validator.py",
                f"4. Customize data_pipeline/preprocessors/{cancer_type}_preprocessor.py",
                f"5. Train model using the standardized pipeline"
            ]
            
            print(f"\n🎉 Setup complete for {cancer_type}!")
            print(f"📁 Dataset location: data_pipeline/datasets/{cancer_type}/")
            print(f"🔧 Preprocessor: data_pipeline/preprocessors/{cancer_type}_preprocessor.py")
            
        except Exception as e:
            report["errors"].append(f"❌ Setup failed: {str(e)}")
            print(f"❌ Setup failed: {str(e)}")
        
        return report
    
    def _generate_setup_instructions(self, cancer_type: str, description: str) -> str:
        """Generate detailed setup instructions"""
        instructions = f"""
# {cancer_type.title().replace('_', ' ')} Setup Instructions

## Overview
{description}

## Directory Structure Created
```
data_pipeline/datasets/{cancer_type}/
├── train/          # Training images
├── val/            # Validation images  
├── test/           # Test images
└── metadata.json   # Dataset information

data_pipeline/preprocessors/
└── {cancer_type}_preprocessor.py  # Custom preprocessing logic
```

## Data Collection Guidelines

### Image Requirements:
- **Format**: JPG, PNG, BMP, TIFF
- **Size**: Minimum 64x64, Maximum 4096x4096
- **Quality**: Clear, high-resolution medical images
- **Consistency**: Similar imaging protocols across dataset

### Directory Organization:
```
train/
├── normal/         # Normal/healthy cases
├── cancer/         # Cancer/malignant cases
└── subcategories/  # If applicable (e.g., cancer subtypes)

val/
├── normal/
└── cancer/

test/
├── normal/
└── cancer/
```

## Next Steps

1. **Data Collection**:
   - Collect {cancer_type.replace('_', ' ')} medical images
   - Ensure balanced dataset (normal vs cancer cases)
   - Maintain patient privacy and ethical guidelines

2. **Data Validation**:
   ```bash
   python data_pipeline/validators/data_validator.py
   ```

3. **Preprocessing Customization**:
   - Edit `data_pipeline/preprocessors/{cancer_type}_preprocessor.py`
   - Adjust preprocessing parameters for {cancer_type.replace('_', ' ')} images
   - Add specific feature extraction methods

4. **Model Development**:
   - Choose appropriate AI architecture
   - Train on collected dataset
   - Validate performance metrics

5. **Integration**:
   - Add API endpoints
   - Update frontend UI
   - Test end-to-end functionality

## Important Notes
- Ensure ethical data collection practices
- Maintain patient confidentiality
- Follow medical data regulations (HIPAA, GDPR, etc.)
- Validate model performance before clinical use
- Include diverse patient demographics

## Support
For questions or issues, refer to the main documentation or create an issue.
"""
        return instructions
    
    def _create_data_collection_template(self, cancer_type: str):
        """Create a template for data collection tracking"""
        template = {
            "cancer_type": cancer_type,
            "collection_status": "not_started",
            "target_samples": {
                "train": 1000,
                "val": 200,
                "test": 200
            },
            "current_samples": {
                "train": 0,
                "val": 0,
                "test": 0
            },
            "data_sources": [],
            "quality_checks": {
                "validation_passed": False,
                "issues_found": [],
                "quality_score": 0.0
            },
            "preprocessing_config": {
                "target_size": [224, 224],
                "normalization": "standard",
                "augmentation": "basic"
            }
        }
        
        collection_file = Path(f"data_pipeline/datasets/{cancer_type}/data_collection.json")
        with open(collection_file, "w") as f:
            json.dump(template, f, indent=2)

def main():
    """Interactive setup for new cancer types"""
    setup = CancerTypeSetup()
    
    print("🏥 CancerCare AI - New Cancer Type Setup")
    print("=" * 50)
    
    # Predefined cancer types for easy setup
    cancer_options = {
        "1": ("brain_cancer", "Brain tumor detection using MRI and CT scans"),
        "2": ("liver_cancer", "Liver cancer detection using CT and ultrasound images"),
        "3": ("skin_cancer", "Skin cancer detection using dermatology images"),
        "4": ("prostate_cancer", "Prostate cancer detection using MRI and ultrasound"),
        "5": ("kidney_cancer", "Kidney cancer detection using CT and MRI scans"),
        "6": ("custom", "Custom cancer type")
    }
    
    print("\nAvailable cancer types:")
    for key, (cancer_type, description) in cancer_options.items():
        print(f"{key}. {cancer_type.replace('_', ' ').title()}: {description}")
    
    choice = input("\nSelect cancer type (1-6): ").strip()
    
    if choice in cancer_options:
        cancer_type, description = cancer_options[choice]
        
        if choice == "6":  # Custom
            cancer_type = input("Enter cancer type name (e.g., 'pancreatic_cancer'): ").strip().lower().replace(" ", "_")
            description = input("Enter description: ").strip()
        
        print(f"\n🚀 Setting up {cancer_type}...")
        report = setup.setup_cancer_type(cancer_type, description)
        
        if report["success"]:
            print("\n✅ Setup completed successfully!")
            print("\n📋 Next Steps:")
            for i, step in enumerate(report["next_steps"], 1):
                print(f"  {i}. {step}")
            
            save_instructions = input("\nSave setup instructions to file? (y/n): ").strip().lower()
            if save_instructions == 'y':
                filename = f"{cancer_type}_setup_instructions.md"
                # Remove emojis to avoid Unicode encoding issues
                clean_instructions = report["setup_instructions"].replace('🏥', '').replace('🗂️', '').replace('📊', '').replace('🔄', '').replace('⚠️', '').replace('📞', '').replace('✅', '').replace('❌', '').replace('🎯', '').replace('📋', '').replace('🔧', '').replace('📁', '').replace('🚀', '').replace('🎉', '').replace('📝', '').replace('📈', '').replace('🛠️', '')
                with open(filename, "w", encoding='utf-8') as f:
                    f.write(clean_instructions)
                print(f"✅ Instructions saved to {filename}")
        else:
            print("\n❌ Setup failed!")
            print("Errors:")
            for error in report["errors"]:
                print(f"  - {error}")
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
