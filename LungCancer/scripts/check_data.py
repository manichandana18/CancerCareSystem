import os

BASE_PATH = "data/raw"
SPLITS = ["train", "test", "valid"]
CLASSES = ["Normal", "Cancer"]

for split in SPLITS:
    print(f"\n{split.upper()} DATA")
    for cls in CLASSES:
        path = os.path.join(BASE_PATH, split, cls)
        if os.path.exists(path):
            count = len([
                f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))
            ])
            print(f"{cls}: {count}")
        else:
            print(f"{cls}: folder not found")
