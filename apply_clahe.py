import cv2
import os

DATASET = "dataset_balanced/train"

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

for cls in ["cancer", "normal"]:
    folder = f"{DATASET}/{cls}"
    for img_name in os.listdir(folder):
        path = f"{folder}/{img_name}"
        img = cv2.imread(path, 0)
        if img is None:
            continue
        enhanced = clahe.apply(img)
        cv2.imwrite(path, enhanced)

print("✅ CLAHE applied successfully.")
