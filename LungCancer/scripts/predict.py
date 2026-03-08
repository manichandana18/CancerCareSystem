import cv2
import numpy as np
import pandas as pd
import joblib
from skimage.feature import graycomatrix, graycoprops
import sys
import os

MODEL_PATH = "models/radiomics_rf_model.pkl"
SCALER_PATH = "models/scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def extract_features(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Invalid image path")

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

    features = {
        "contrast": graycoprops(glcm, "contrast")[0, 0],
        "dissimilarity": graycoprops(glcm, "dissimilarity")[0, 0],
        "homogeneity": graycoprops(glcm, "homogeneity")[0, 0],
        "energy": graycoprops(glcm, "energy")[0, 0],
        "correlation": graycoprops(glcm, "correlation")[0, 0],
        "ASM": graycoprops(glcm, "ASM")[0, 0],
        "mean_intensity": np.mean(img),
        "std_intensity": np.std(img),
    }

    return pd.DataFrame([features])

def predict(image_path):
    features = extract_features(image_path)
    features_scaled = scaler.transform(features)

    pred = model.predict(features_scaled)[0]
    prob = model.predict_proba(features_scaled)[0].max()

    return {
        "prediction": "Cancer" if pred == 1 else "Normal",
        "confidence": round(float(prob), 3)
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python predict.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    result = predict(image_path)

    print("\nLUNG CANCER PREDICTION")
    print("----------------------")
    print(f"Prediction : {result['prediction']}")
    print(f"Confidence : {result['confidence']}")
