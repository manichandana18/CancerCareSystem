import cv2
import os
import numpy as np
import shutil

SRC = "dataset"
DST = "dataset_clean"

def is_good_xray(path):
    img = cv2.imread(path, 0)
    if img is None:
        return False
    mean = np.mean(img)
    h, w = img.shape
    if mean < 40 or mean > 220:
        return False
    if h < 200 or w < 200:
        return False
    return True

for split in ["train", "valid", "test"]:
    for cls in ["cancer", "normal"]:
        src_dir = os.path.join(SRC, split, cls)
        dst_dir = os.path.join(DST, split, cls)

        for img_name in os.listdir(src_dir):
            src_path = os.path.join(src_dir, img_name)
            if is_good_xray(src_path):
                shutil.copy(src_path, dst_dir)

print("Automatic dataset cleaning completed successfully.")
