import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "bone_cancer_model.h5")

# CHANGE THIS IMAGE PATH IF NEEDED
IMAGE_PATH = os.path.join(BASE_DIR, "..", "dataset", "train", "normal", "sample_xray.jpg")

IMG_SIZE = (160, 160)

# =========================
# LOAD MODEL
# =========================
print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)

# =========================
# LOAD & PREPROCESS IMAGE
# =========================
img = image.load_img(IMAGE_PATH, target_size=IMG_SIZE)
img_array = image.img_to_array(img)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

# =========================
# PREDICT
# =========================
prediction = model.predict(img_array)[0][0]

if prediction >= 0.5:
    print(f"Prediction: CANCER")
    print(f"Confidence: {prediction:.2f}")
else:
    print(f"Prediction: NORMAL")
    print(f"Confidence: {1 - prediction:.2f}")
