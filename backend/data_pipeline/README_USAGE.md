# 🚀 CancerCare AI Data Pipeline - Usage Guide

## 🎯 **Sequential Cancer Type Expansion**

This pipeline allows you to systematically add new cancer types to your CancerCare AI system.

## 📋 **Quick Start - Adding Your First New Cancer Type**

### **Step 1: Run the Setup Script**
```bash
cd backend
python data_pipeline/setup_new_cancer.py
```

### **Step 2: Choose Your Cancer Type**
The script will show you options like:
```
1. brain_cancer: Brain tumor detection using MRI and CT scans
2. liver_cancer: Liver cancer detection using CT and ultrasound images
3. skin_cancer: Skin cancer detection using dermatology images
4. prostate_cancer: Prostate cancer detection using MRI and ultrasound
5. kidney_cancer: Kidney cancer detection using CT and MRI scans
6. custom: Custom cancer type
```

### **Step 3: Follow Generated Instructions**
The script creates:
- ✅ Directory structure
- ✅ Preprocessor template
- ✅ Metadata files
- ✅ Setup instructions

## 🏗️ **Pipeline Architecture**

### **Directory Structure Created Automatically:**
```
data_pipeline/
├── datasets/
│   ├── brain_cancer/          # New cancer type
│   │   ├── train/
│   │   │   ├── normal/        # Healthy cases
│   │   │   └── cancer/        # Cancer cases
│   │   ├── val/
│   │   ├── test/
│   │   ├── metadata.json      # Dataset info
│   │   └── data_collection.json
│   ├── liver_cancer/          # Next cancer type
│   └── skin_cancer/           # And so on...
├── preprocessors/
│   ├── brain_cancer_preprocessor.py
│   ├── liver_cancer_preprocessor.py
│   └── skin_cancer_preprocessor.py
└── validators/
    └── data_validator.py
```

## 🔄 **Workflow for Each Cancer Type**

### **Phase 1: Data Collection**
1. **Collect medical images** for the cancer type
2. **Organize into train/val/test splits**
3. **Maintain balance** between normal and cancer cases

### **Phase 2: Data Validation**
```bash
# Validate your dataset
python data_pipeline/validators/data_validator.py
```

### **Phase 3: Preprocessing Customization**
Edit the generated preprocessor:
```python
# data_pipeline/preprocessors/brain_cancer_preprocessor.py
class BrainCancerPreprocessor:
    def preprocess_image(self, image_path):
        # Customize for brain MRI/CT scans
        pass
```

### **Phase 4: Model Development**
1. **Choose AI architecture** (CNN, ViT, GNN, etc.)
2. **Train on your dataset**
3. **Validate performance**

### **Phase 5: Integration**
1. **Add API endpoints**
2. **Update frontend**
3. **Test end-to-end**

## 📊 **Data Quality Standards**

### **Image Requirements:**
- ✅ **Formats**: JPG, PNG, BMP, TIFF
- ✅ **Size**: 64x64 to 4096x4096 pixels
- ✅ **Quality**: Clear medical images
- ✅ **Consistency**: Similar imaging protocols

### **Dataset Balance:**
- 🎯 **Target**: 70-80% training, 10-15% validation, 10-15% test
- 🎯 **Balance**: Equal normal vs cancer cases (or realistic medical distribution)
- 🎯 **Diversity**: Multiple patient demographics

## 🛠️ **Advanced Usage**

### **Manual Pipeline Management:**
```python
from data_pipeline.pipeline_manager import CancerDataPipeline

# Initialize pipeline
pipeline = CancerDataPipeline()

# Add new cancer type
pipeline.add_cancer_type("pancreatic_cancer", "Pancreatic cancer detection")

# Check status
status = pipeline.get_pipeline_status()
print(status)

# Update metadata
pipeline.update_metadata("pancreatic_cancer", {
    "status": "data_collection",
    "samples_collected": 500
})
```

### **Data Validation:**
```python
from data_pipeline.validators.data_validator import DataValidator

validator = DataValidator()

# Validate dataset structure
structure_report = validator.validate_dataset_structure("datasets/brain_cancer")

# Validate image quality
quality_report = validator.generate_quality_report("datasets/brain_cancer")
print(quality_report)
```

## 📈 **Expansion Roadmap**

### **Recommended Sequence:**
1. **brain_cancer** - MRI/CT analysis
2. **liver_cancer** - CT/ultrasound analysis  
3. **skin_cancer** - Dermatology images
4. **prostate_cancer** - MRI/ultrasound analysis
5. **kidney_cancer** - CT/MRI analysis
6. **lung_cancer** (already done)
7. **blood_cancer** (already done)
8. **bone_cancer** (already done)

### **Each New Cancer Type Gets:**
- ✅ **Standardized data pipeline**
- ✅ **Automated preprocessing**
- ✅ **Quality validation**
- ✅ **Performance tracking**
- ✅ **Easy integration**

## 🎯 **Success Metrics**

### **Data Quality:**
- 🎯 **95%+ image validation pass rate**
- 🎯 **Consistent image formats**
- 🎯 **Proper train/val/test splits**

### **Model Performance:**
- 🎯 **85%+ accuracy target**
- 🎯 **Proper explainability**
- 🎯 **Cross-validation results**

### **Integration:**
- 🎯 **API endpoints working**
- 🎯 **Frontend integration**
- 🎯 **End-to-end testing**

## 🚨 **Important Notes**

### **Medical Ethics:**
- ⚠️ **Patient privacy** - Maintain confidentiality
- ⚠️ **Data regulations** - Follow HIPAA/GDPR
- ⚠️ **Informed consent** - Proper data usage permissions
- ⚠️ **Clinical validation** - Medical expert review

### **Technical Best Practices:**
- ⚠️ **Version control** - Track data and model versions
- ⚠️ **Backup data** - Prevent data loss
- ⚠️ **Documentation** - Maintain clear records
- ⚠️ **Testing** - Validate at each step

## 📞 **Support**

For each cancer type:
1. **Run setup script** - Automated initialization
2. **Follow instructions** - Step-by-step guidance
3. **Validate data** - Quality assurance
4. **Customize preprocessor** - Adapt to specific needs
5. **Train and integrate** - Complete the pipeline

**Your CancerCare AI system is now ready for unlimited expansion!** 🏥✨
