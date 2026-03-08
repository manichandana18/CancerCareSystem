import os
import shutil

RAW_DIR = "data/raw"
BALANCED_DIR = "data/balanced"

CLASSES = ["Cancer", "Normal"]


def count_images(base_path):
    counts = {}
    for cls in CLASSES:
        cls_path = os.path.join(base_path, "train", cls)
        if os.path.exists(cls_path):
            counts[cls] = len([
                f for f in os.listdir(cls_path)
                if os.path.isfile(os.path.join(cls_path, f))
            ])
        else:
            counts[cls] = 0
    return counts


def balance_data():
    raw_train = os.path.join(RAW_DIR, "train")
    balanced_train = os.path.join(BALANCED_DIR, "train")

    os.makedirs(balanced_train, exist_ok=True)

    counts = count_images(RAW_DIR)
    min_count = min(counts.values())

    for cls in CLASSES:
        src = os.path.join(raw_train, cls)
        dst = os.path.join(balanced_train, cls)

        os.makedirs(dst, exist_ok=True)

        images = [
            img for img in os.listdir(src)
            if os.path.isfile(os.path.join(src, img))
        ][:min_count]

        for img in images:
            shutil.copy(
                os.path.join(src, img),
                os.path.join(dst, img)
            )

    print("✅ Training data balanced successfully.")
    print(f"Cancer: {min_count}")
    print(f"Normal: {min_count}")


if __name__ == "__main__":
    balance_data()
