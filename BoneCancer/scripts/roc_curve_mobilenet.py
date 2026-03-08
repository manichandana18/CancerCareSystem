import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from tensorflow.keras.preprocessing.image import ImageDataGenerator

MODEL_PATH = "dataset/mobilenet_bone_cancer.h5"
TEST_DIR = "dataset_balanced/test"
IMG_SIZE = 224
BATCH_SIZE = 16

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# Test data loader
test_gen = ImageDataGenerator(rescale=1./255)

test_data = test_gen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=False
)

# Predictions
y_true = test_data.classes
y_probs = model.predict(test_data).ravel()

# ROC
fpr, tpr, _ = roc_curve(y_true, y_probs)
roc_auc = auc(fpr, tpr)

# Plot
plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve – MobileNetV2 Bone Cancer Detection")
plt.legend()
plt.savefig("roc_curve_mobilenet.png")
plt.show()

print(f"✅ ROC AUC Score: {roc_auc:.4f}")
