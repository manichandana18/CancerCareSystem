import tensorflow as tf
import numpy as np
import cv2
import os

MODEL_PATH = "bone_cancer_final_model.h5"
TEST_DIR = "dataset_clean/test"

model = tf.keras.models.load_model(MODEL_PATH)

def predict_image(img_path):
    img = cv2.imread(img_path, 0)
    img = cv2.resize(img, (224,224))
    img = img / 255.0
    img = img.reshape(1,224,224,1)
    pred = model.predict(img)[0][0]
    return pred

for cls in ["cancer", "normal"]:
    folder = os.path.join(TEST_DIR, cls)
    img = os.listdir(folder)[0]
    path = os.path.join(folder, img)
    pred = predict_image(path)
    print(f"{cls.upper()} → RAW PREDICTION:", pred)
