import os

for split in ["train", "valid", "test"]:
    print("\n" + split.upper())
    for cls in ["cancer", "normal"]:
        path = f"dataset_clean/{split}/{cls}"
        print(cls, "=", len(os.listdir(path)))
