import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# ===============================
# FIXED PATH HANDLING (IMPORTANT)
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TRAIN_DIR = os.path.join(BASE_DIR, "..", "dataset", "train")

print("✅ Train directory:", TRAIN_DIR)

# ===============================
# PARAMETERS (SAFE FOR LAPTOP)
# ===============================

IMG_SIZE = (160, 160)
BATCH_SIZE = 8
EPOCHS = 5

# ===============================
# DATA GENERATOR WITH VALIDATION SPLIT
# ===============================

train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2   # 80% training, 20% validation
)

train_data = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="training"
)

val_data = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="validation"
)

# ===============================
# MODEL (TRANSFER LEARNING)
# ===============================

base_model = EfficientNetB0(
    weights="imagenet",
    include_top=False,
    input_shape=(160, 160, 3)
)

base_model.trainable = False  # freeze base model

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation="relu")(x)
x = Dropout(0.5)(x)
output = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ===============================
# TRAIN MODEL
# ===============================

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# ===============================
# SAVE MODEL
# ===============================

model.save("bone_cancer_model.h5")
print("✅ Model saved as bone_cancer_model.h5")
