import os
import cv2
import pandas as pd
import numpy as np
from skimage.feature import graycomatrix, graycoprops

DATA_DIR = "data/raw/train"
OUTPUT_CSV = "data/features.csv"

CLASSES = {
    "Normal": 0,
    "Cancer": 1
}

rows = []

for class_name, label in CLASSES.items():
    class_path = os.path.join(DATA_DIR, class_name)

    for img_name in os.listdir(class_path):
        img_path = os.path.join(class_path, img_name)

        if not os.path.isfile(img_path):
            continue

        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            continue

        image = cv2.resize(image, (256, 256))

        # Quantize image
        image_q = (image / 16).astype(np.uint8)

        # GLCM texture features
        glcm = graycomatrix(
            image_q,
            distances=[1],
            angles=[0],
            levels=16,
            symmetric=True,
            normed=True
        )

        row = {
            "contrast": graycoprops(glcm, "contrast")[0, 0],
            "dissimilarity": graycoprops(glcm, "dissimilarity")[0, 0],
            "homogeneity": graycoprops(glcm, "homogeneity")[0, 0],
            "energy": graycoprops(glcm, "energy")[0, 0],
            "correlation": graycoprops(glcm, "correlation")[0, 0],
            "ASM": graycoprops(glcm, "ASM")[0, 0],
            "mean_intensity": np.mean(image),
            "std_intensity": np.std(image),
            "label": label
        }

        rows.append(row)

print("Extracted features from", len(rows), "images")

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False)

print("Features saved to:", OUTPUT_CSV)
