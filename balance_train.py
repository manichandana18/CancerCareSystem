import os
import random
import shutil

SRC = "dataset_clean/train"
DST = "dataset_balanced/train"

os.makedirs(f"{DST}/cancer", exist_ok=True)
os.makedirs(f"{DST}/normal", exist_ok=True)

cancer_imgs = os.listdir(f"{SRC}/cancer")
normal_imgs = os.listdir(f"{SRC}/normal")

# Keep all cancer images
for img in cancer_imgs:
    shutil.copy(f"{SRC}/cancer/{img}", f"{DST}/cancer/{img}")

# Randomly select normal images equal to cancer count
selected_normal = random.sample(normal_imgs, len(cancer_imgs))

for img in selected_normal:
    shutil.copy(f"{SRC}/normal/{img}", f"{DST}/normal/{img}")

print("✅ Training data balanced successfully.")
print("Cancer:", len(cancer_imgs))
print("Normal:", len(selected_normal))
