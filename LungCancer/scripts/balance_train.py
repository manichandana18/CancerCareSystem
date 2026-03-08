import os
import shutil

RAW_DIR = "data/raw/train"
BALANCED_DIR = "data/balanced/train"

CLASSES = ["Normal", "Cancer"]

os.makedirs(BALANCED_DIR, exist_ok=True)

# Count images
counts = {}
for cls in CLASSES:
    cls_path = os.path.join(RAW_DIR, cls)
    counts[cls] = len([
        f for f in os.listdir(cls_path)
        if os.path.isfile(os.path.join(cls_path, f))
    ])

min_count = min(counts.values())

for cls in CLASSES:
    src = os.path.join(RAW_DIR, cls)
    dst = os.path.join(BALANCED_DIR, cls)
    os.makedirs(dst, exist_ok=True)

    images = [
        f for f in os.listdir(src)
        if os.path.isfile(os.path.join(src, f))
    ][:min_count]

    for img in images:
        shutil.copy(
            os.path.join(src, img),
            os.path.join(dst, img)
        )

print("✅ LungCancer training data balanced successfully")
print(f"Normal: {min_count}")
print(f"Cancer: {min_count}")
