import os
import cv2
import shutil
import numpy as np

SRC = "dataset"
DST = "dataset_clean"

CANCER_KEYWORDS = [
    "chondrosarcoma",
    "osteosarcoma",
    "metastasis",
    "ewing"
]

NORMAL_KEYWORDS = [
    "other",
    "normal"
]

IMG_EXTENSIONS = (".png", ".jpg", ".jpeg")

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
    src_split = os.path.join(SRC, split)

    for item in os.listdir(src_split):
        item_path = os.path.join(src_split, item)

        # ✅ Ignore folders
        if not os.path.isfile(item_path):
            continue

        # ✅ Ignore non-image files
        if not item.lower().endswith(IMG_EXTENSIONS):
            continue

        if not is_good_xray(item_path):
            continue

        name = item.lower()
        target = None

        if any(k in name for k in CANCER_KEYWORDS):
            target = "cancer"
        elif any(k in name for k in NORMAL_KEYWORDS):
            target = "normal"

        if target:
            dst_path = os.path.join(DST, split, target, item)
            shutil.copy(item_path, dst_path)

print("✅ Dataset organized and cleaned successfully (no folder warnings).")

