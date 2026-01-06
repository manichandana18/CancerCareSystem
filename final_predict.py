import tensorflow as tf
import cv2
import numpy as np
import os

MODEL_PATH = "bone_cancer_final_model.h5"

# Medical thresholds
CANCER_THRESHOLD = 0.40
BORDERLINE_THRESHOLD = 0.55

model = tf.keras.models.load_model(MODEL_PATH)

def predict_image(img_path):
    img = cv2.imread(img_path, 0)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = img.reshape(1, 224, 224, 1)

    prediction = model.predict(img)[0][0]
    print("RAW PREDICTION:", prediction)

    if prediction < CANCER_THRESHOLD:
        return "⚠️ Likely Bone Cancer"
    elif prediction < BORDERLINE_THRESHOLD:
        return "⚠️ Borderline Case – Needs Medical Review"
    else:
        return "Normal Bone"

# TEST WITH ONE IMAGE
test_image_path = os.path.join(
    "dataset_clean", "test", "cancer",
    os.listdir("dataset_clean/test/cancer")[0]
)

print("RESULT:", predict_image(test_image_path))
