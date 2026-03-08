# Bone Cancer Detection Module

## 🔒 STATUS: FINALIZED (BASELINE MODULE)

This module implements a machine learning–based bone cancer detection
system using X-ray images. It is designed as a **standalone ML module**
within the larger **CancerCareSystem** project.

This module is **complete, validated, and locked**. It will be used as
a baseline reference for other cancer detection modules.

---

## Project Structure
BoneCancer/
├── data/
│ ├── raw/ # Original dataset (train / test / valid)
│ ├── clean/ # Cleaned dataset
│ └── balanced/ # Balanced dataset used for training
│
├── scripts/ # All ML-related Python scripts
│ ├── mobilenet_train.py
│ ├── final_train.py
│ ├── balance_train.py
│ ├── evaluate_model.py
│ ├── evaluate_mobilenet.py
│ ├── test_prediction.py
│ ├── test_multiple_images.py
│ ├── final_predict.py
│ ├── count_data.py
│ └── organize_and_clean.py
│
├── models/ # Trained models
│ └── mobilenet_bone_cancer.h5
│
├── results/ # Output results
│ ├── confusion_matrix.png
│ ├── roc_curve_mobilenet.png
│ └── sample_xray_predictions
│
└── docs/ # Documentation
└── README.md

---

## Dataset Details

- Imaging Type: **X-ray**
- Classes:
  - **Normal**
  - **Cancer**
- Dataset Versions:
  - **Raw**: Original dataset
  - **Clean**: Noise-removed and standardized images
  - **Balanced**: Equal number of Normal and Cancer samples

Balanced dataset was used for final training to avoid class bias.

---

## Model Architecture

- Model: **MobileNet (Transfer Learning)**
- Framework: **TensorFlow / Keras**
- Input Size: 224 × 224
- Loss Function: Binary Crossentropy
- Optimizer: Adam

---

## Training

Model training was performed using the balanced dataset.

```bash
python scripts/final_train.py
models/mobilenet_bone_cancer.h5
Evaluation

Evaluation scripts include:

python scripts/evaluate_model.py
python scripts/test_prediction.py


Generated outputs:

Confusion Matrix

ROC Curve

Sample predictions

All outputs are stored in:

results/

Usage

This module is intended for:

Research

Academic projects

Baseline comparison with other cancer detection modules

It can later be integrated with:

REST APIs

Web applications

Desktop applications
Disclaimer

This system is for educational and research purposes only.
It is NOT a medical diagnostic tool.
Always consult qualified healthcare professionals for medical advice


