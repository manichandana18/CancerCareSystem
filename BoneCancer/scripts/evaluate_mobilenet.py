import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# ================= CONFIG =================
MODEL_PATH = "mobilenet_bone_cancer.h5"
TEST_DIR = "dataset_balanced/train"   # temporary test on train
IMG_SIZE = 224
BATCH_SIZE = 16

# ================= LOAD MODEL =================
model = tf.keras.models.load_model(MODEL_PATH)

# ================= DATA =================
test_gen = ImageDataGenerator(rescale=1./255)

test_data = test_gen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=False
)

# ================= EVALUATION =================
pred_probs = model.predict(test_data)
preds = (pred_probs > 0.5).astype(int).flatten()
true = test_data.classes

# Accuracy
accuracy = np.mean(preds == true) * 100
print(f"\n✅ MobileNetV2 Accuracy: {accuracy:.2f} %\n")

# Classification report
print("📊 Classification Report:")
print(classification_report(true, preds, target_names=["Cancer", "Normal"]))

# Confusion matrix
cm = confusion_matrix(true, preds)

plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Cancer", "Normal"],
            yticklabels=["Cancer", "Normal"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix – MobileNetV2")
plt.tight_layout()
plt.savefig("mobilenet_confusion_matrix.png")
plt.show()

print("📁 Confusion matrix saved as mobilenet_confusion_matrix.png")
