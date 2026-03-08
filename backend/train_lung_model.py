"""
Train a lightweight CNN for lung cancer classification using the existing lung dataset.
Saves the model to backend/lung_cancer_model.h5 for use in the organ-aware pipeline.
"""

import os
import shutil
from pathlib import Path
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Enable symlink creation on Windows
if os.name == 'nt':
    import ctypes
    ctypes.windll.kernel32.SetErrorMode(1)

# -----------------------------
# CONFIGURATION
# -----------------------------
DATA_DIR = Path("organ_dataset/lung")
MODEL_PATH = "lung_cancer_model.h5"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 12
SEED = 42

# -----------------------------
# PREPARE DATASET
# -----------------------------
def prepare_dataset():
    """Organize images into class folders for Keras flow_from_directory."""
    # Target folders
    train_dir = Path("lung_train")
    val_dir = Path("lung_val")
    for d in [train_dir, val_dir]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir()

    # Class mapping from filenames
    class_map = {
        "Normal": "normal",
        "Bengin": "benign",
        "Malignant": "malignant"
    }

    # Collect files by class
    files_by_class = {k: [] for k in class_map.values()}
    for file_path in DATA_DIR.glob("*.jpg"):
        fname = file_path.name
        for label, folder in class_map.items():
            if label in fname:
                files_by_class[folder].append(file_path)
                break

    # Split each class into train/val (80/20)
    for cls, files in files_by_class.items():
        train_files, val_files = train_test_split(files, test_size=0.2, random_state=SEED)
        for f in train_files:
            (train_dir / cls).mkdir(parents=True, exist_ok=True)
            os.symlink(f.resolve(), train_dir / cls / f.name)
        for f in val_files:
            (val_dir / cls).mkdir(parents=True, exist_ok=True)
            os.symlink(f.resolve(), val_dir / cls / f.name)

    print(f"Dataset prepared: {len(train_files)} train, {len(val_files)} val per class")
    return train_dir, val_dir

# -----------------------------
# BUILD MODEL
# -----------------------------
def build_model(num_classes=3):
    """Lightweight CNN for lung classification."""
    inputs = layers.Input(shape=(*IMG_SIZE, 3))
    x = layers.Rescaling(1./255)(inputs)

    x = layers.Conv2D(32, 3, activation='relu')(x)
    x = layers.MaxPooling2D()(x)

    x = layers.Conv2D(64, 3, activation='relu')(x)
    x = layers.MaxPooling2D()(x)

    x = layers.Conv2D(128, 3, activation='relu')(x)
    x = layers.MaxPooling2D()(x)

    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = models.Model(inputs, outputs, name="LungCancerCNN")
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

# -----------------------------
# TRAIN & EVALUATE
# -----------------------------
def train_and_evaluate():
    train_dir, val_dir = prepare_dataset()

    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        label_mode='int',
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True,
        seed=SEED
    ).cache().prefetch(buffer_size=tf.data.AUTOTUNE)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        label_mode='int',
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False,
        seed=SEED
    ).cache().prefetch(buffer_size=tf.data.AUTOTUNE)

    model = build_model(num_classes=3)
    model.summary()

    # Get class names from the directory structure
    class_names = sorted([d.name for d in train_dir.iterdir() if d.is_dir()])

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)
        ]
    )

    # Save model
    model.save(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    # Evaluation
    y_true = np.concatenate([y for _, y in val_ds], axis=0)
    y_pred_probs = model.predict(val_ds)
    y_pred = np.argmax(y_pred_probs, axis=1)

    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names))

    # Confusion matrix plot
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names,
                yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Lung Cancer Classification Confusion Matrix')
    plt.tight_layout()
    plt.savefig('lung_confusion_matrix.png')
    plt.show()

    # Cleanup temporary dirs
    shutil.rmtree(train_dir, ignore_errors=True)
    shutil.rmtree(val_dir, ignore_errors=True)

    return model, train_ds.class_names

if __name__ == "__main__":
    model, class_names = train_and_evaluate()
    print(f"Training complete. Model saved to {MODEL_PATH}")
    print("Class order:", class_names)
