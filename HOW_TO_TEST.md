# How to Test Your Bone Cancer Detection Model

## 📁 Where to Put Your Test Images

You can place test images **anywhere** on your computer! Here are the recommended locations:

### Option 1: Root Directory (Easiest)
Place your images in the main project folder:
```
BONE CANCER/
├── sample_xray.jpg          ← Already exists
├── test_xray.jpg            ← Already exists  
├── your_cancer_image.jpg    ← Put your test images here
└── your_normal_image.jpg
```

### Option 2: Create a Test Folder
Create a `test_images` folder in the root:
```
BONE CANCER/
└── test_images/
    ├── cancer_test1.jpg
    ├── cancer_test2.jpg
    └── normal_test1.jpg
```

### Option 3: Use Existing Dataset Images
You already have many test images in:
```
BONE CANCER/
└── dataset/
    └── valid/
        ├── [cancer images with names like: osteosarcoma, ewing, chondrosarcoma, metastasis]
        └── [normal images with names like: image-no91-normal]
```

## 🧪 How to Test

### Method 1: Using Python Test Script (Recommended)

1. **Make sure backend server is running** (in one terminal):
   ```bash
   cd backend
   venv\Scripts\activate
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **In a NEW terminal**, test with an image:
   ```bash
   # Test with image in root folder
   python test_prediction.py sample_xray.jpg
   python test_prediction.py test_xray.jpg
   
   # Test with your own image
   python test_prediction.py your_image.jpg
   
   # Test with image in subfolder
   python test_prediction.py test_images\cancer_test1.jpg
   
   # Test with dataset image
   python test_prediction.py dataset\valid\tibia_osteosarcoma_18_PNG.rf.8356edeaa98cc538f5512fe6e4e7f61d.jpg
   ```

### Method 1B: Test the Organ-Aware Multi-Stage Pipeline (/predict/auto)

This endpoint performs:

Stage 1: Organ Classification (Bone vs Lung)

Stage 2: Organ-specific prediction

Stage 3: Organ-aware explainability

1. **Make sure backend server is running** (same as above)

2. **In a NEW terminal**, call the organ-aware test client:
   ```bash
   cd backend
   venv\Scripts\activate
   python test_auto_predict.py sample_xray.jpg
   ```

3. **Expected output fields** include:

   - `organ`, `organ_confidence`
   - `diagnosis`, `diagnosis_confidence`
   - `explainability`

4. **Grad-CAM setup note (Lung)**

   Grad-CAM requires a lung CNN model file. Configure one of these:

   - Set env var `LUNG_CNN_MODEL_PATH` to a `.h5` model file path
   - Or place a model at `backend\models\lung_cnn_model.h5`

   If the lung model is not configured, the API will still work, but `explainability` for lung will return an `error` explaining what is missing.

### Method 2: Using Java Frontend

1. **Make sure backend server is running** (same as above)

2. **Compile Java code** (if not already compiled):
   ```bash
   cd src
   javac -d .. Main.java
   ```

3. **Run with your image**:
   ```bash
   cd ..
   
   # Test with default image
   java Main
   
   # Test with specific image
   java Main sample_xray.jpg
   java Main test_xray.jpg
   java Main your_image.jpg
   java Main test_images\cancer_test1.jpg
   ```

## 🔍 Finding Cancer Images in Your Dataset

Your dataset has many cancer images! Here are some examples:

**Cancer images** (should be detected as "Tumor"):
- `dataset\valid\tibia_osteosarcoma_*.jpg` - Osteosarcoma (bone cancer)
- `dataset\valid\pelvis_osteosarcoma_*.jpg` - Pelvis osteosarcoma
- `dataset\valid\tibia_ewing_*.jpg` - Ewing's sarcoma
- `dataset\valid\tibia_chondrosarcoma_*.jpg` - Chondrosarcoma
- `dataset\valid\tibia_metastasis_*.jpg` - Metastatic cancer
- `dataset\valid\ulna_osteosarcoma_*.jpg` - Ulna osteosarcoma

**Normal images** (should be detected as "No Tumor"):
- `dataset\valid\image-no*-normal-*.jpg` - Normal bone X-rays
- `dataset\valid\pelvis_female_*.jpg` - Normal pelvis
- `dataset\valid\pelvis_chield_*.jpg` - Normal child pelvis

## 📊 What to Look For in Results

When you test, check:

1. **Prediction**: Should say "Tumor Detected" for cancer images
2. **Probabilities**: 
   - `tumor` probability should be > 0.3 for cancer images
   - `normal` probability should be > 0.7 for normal images
3. **Confidence**: Higher is better (> 0.6 is good)

## 🐛 Troubleshooting

**Image not found?**
- Use full path: `python test_prediction.py "C:\Users\Balaiah goud\Desktop\BONE CANCER\your_image.jpg"`
- Or copy image to project root folder

**Server not running?**
- Check terminal shows: `Uvicorn running on http://127.0.0.1:8000`
- Make sure port 8000 is not used by another program

**Want to test multiple images?**
Create a batch script or test them one by one!

