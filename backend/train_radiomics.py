import os
import cv2
import numpy as np
import pandas as pd
import joblib

from skimage.feature import graycomatrix, graycoprops
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = r"C:\Users\Balaiah goud\Desktop\CancerCareSystem\BoneCancer\data\balanced\train"

MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)

def extract_features(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    img = cv2.resize(img, (256, 256))
    img_q = (img / 16).astype(np.uint8)

    glcm = graycomatrix(
        img_q,
        distances=[1],
        angles=[0],
        levels=16,
        symmetric=True,
        normed=True
    )

    features = [
        graycoprops(glcm, "contrast")[0, 0],
        graycoprops(glcm, "dissimilarity")[0, 0],
        graycoprops(glcm, "homogeneity")[0, 0],
        graycoprops(glcm, "energy")[0, 0],
        graycoprops(glcm, "correlation")[0, 0],
        graycoprops(glcm, "ASM")[0, 0],
        np.mean(img),
        np.std(img)
    ]

    return features

X = []
y = []

for label, class_name in enumerate(["normal", "cancer"]):
    class_dir = os.path.join(DATASET_DIR, class_name)
    for file in os.listdir(class_dir):
        img_path = os.path.join(class_dir, file)
        features = extract_features(img_path)
        if features is not None:
            X.append(features)
            y.append(label)

X = np.array(X)
y = np.array(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\nMODEL REPORT\n")
print(classification_report(y_test, y_pred))

joblib.dump(model, os.path.join(MODEL_DIR, "radiomics_rf_model.pkl"))
joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))

print("\n✅ Model and scaler saved in /models folder")
