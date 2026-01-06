import tensorflow as tf
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# ================= CONFIG =================
MODEL_PATH = "bone_cancer_final_model.h5"
IMG_SIZE = 224
TEST_DIR = "dataset_clean/test"
CLASSES = ["cancer", "normal"]

# ================= LOAD MODEL =================
model = tf.keras.models.load_model(MODEL_PATH)

# ================= LOAD TEST DATA =================
X_test = []
y_test = []

for label, class_name in enumerate(CLASSES):
    class_path = os.path.join(TEST_DIR, class_name)

    for img_name in os.listdir(class_path):
        img_path = os.path.join(class_path, img_name)

        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = img / 255.0
        img = img.reshape(IMG_SIZE, IMG_SIZE, 1)

        X_test.append(img)
        y_test.append(label)

X_test = np.array(X_test)
y_test = np.array(y_test)

print("Total test samples:", len(X_test))

# ================= PREDICTION =================
y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype(int).reshape(-1)

# ================= METRICS =================
accuracy = accuracy_score(y_test, y_pred)
print("\n✅ Model Accuracy:", round(accuracy * 100, 2), "%")

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=CLASSES))

# ================= CONFUSION MATRIX =================
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Predicted Cancer", "Predicted Normal"],
    yticklabels=["Actual Cancer", "Actual Normal"]
)

plt.title("Confusion Matrix – Bone Cancer Detection")
plt.ylabel("Actual Label")
plt.xlabel("Predicted Label")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()

print("📁 Confusion matrix saved as confusion_matrix.png")
