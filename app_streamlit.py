import streamlit as st
import tensorflow as tf
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import hashlib

# ================= CONFIG =================
MODEL_PATH = "bone_cancer_final_model.h5"
IMG_SIZE = 224
CANCER_THRESHOLD = 0.40
BORDERLINE_THRESHOLD = 0.55

st.set_page_config(
    page_title="Bone Cancer Detection",
    page_icon="🦴",
    layout="centered"
)

# ================= SIDEBAR =================
with st.sidebar:
    st.title("🦴 Bone Cancer AI")
    st.write("AI-assisted screening of bone X-ray images.")
    st.warning(
        "Educational & research purposes only.\n\n"
        "Not a medical diagnosis system."
    )

# ================= LOAD MODEL =================
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model(MODEL_PATH)
    dummy = np.zeros((1, IMG_SIZE, IMG_SIZE, 1), dtype=np.float32)
    model(dummy)  # force build
    return model

model = load_model()

# ================= UTILITIES =================
def preprocess_image(image):
    img = np.array(image.convert("L"))
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = img.reshape(1, IMG_SIZE, IMG_SIZE, 1)
    return img

def is_likely_xray(image):
    img = np.array(image)

    if len(img.shape) == 3:
        r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        color_diff = (
            np.mean(np.abs(r - g)) +
            np.mean(np.abs(r - b)) +
            np.mean(np.abs(g - b))
        )
        if color_diff > 15:
            return False
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img

    return gray.std() > 25

def file_hash(file):
    return hashlib.md5(file.getvalue()).hexdigest()

def result_label(pred):
    if pred < CANCER_THRESHOLD:
        return "Likely Bone Cancer"
    elif pred < BORDERLINE_THRESHOLD:
        return "Borderline"
    else:
        return "Normal Bone"

# ================= HEADER =================
st.title("🦴 Bone Cancer Detection System")
st.caption("AI-assisted screening of bone X-ray images")
st.divider()

# ================= SINGLE IMAGE =================
st.subheader("🔍 Single Image Analysis")

single_file = st.file_uploader(
    "Upload a single bone X-ray image",
    type=["png", "jpg", "jpeg"]
)

if single_file is not None:
    image = Image.open(single_file)
    st.image(image, width=300)

    if st.button("Analyze Image"):
        if not is_likely_xray(image):
            st.error("❌ Invalid image. Please upload a bone X-ray.")
        else:
            img = preprocess_image(image)
            pred = model.predict(img)[0][0]
            confidence = ((1 - pred) if pred < 0.5 else pred) * 100

            st.progress(int(confidence))
            st.write(f"Confidence: {confidence:.2f}%")
            st.success(result_label(pred))

st.divider()

# ================= BATCH ANALYSIS =================
st.subheader("📂 Batch Analysis (Multiple Images)")

files = st.file_uploader(
    "Upload multiple bone X-ray images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if files:
    unique_files = {}
    for f in files:
        h = file_hash(f)
        if h not in unique_files:
            unique_files[h] = f
        else:
            st.warning(f"Duplicate skipped: {f.name}")

    st.info(f"{len(unique_files)} unique images will be analyzed")

    if st.button("Analyze All Images"):
        results = []

        for idx, f in enumerate(unique_files.values(), start=1):
            try:
                image = Image.open(f)

                if not is_likely_xray(image):
                    st.warning(f"{f.name} skipped (not an X-ray)")
                    continue

                img = preprocess_image(image)
                pred = model.predict(img)[0][0]
                confidence = ((1 - pred) if pred < 0.5 else pred) * 100
                label = result_label(pred)

                st.markdown(f"### 🖼 Image {idx}: {f.name}")
                st.image(image, width=250)
                st.progress(int(confidence))
                st.write(f"Confidence: {confidence:.2f}%")
                st.success(label)

                results.append({
                    "Image Name": f.name,
                    "Raw Score": round(float(pred), 4),
                    "Confidence (%)": round(confidence, 2),
                    "Result": label
                })

                st.divider()

            except Exception as e:
                st.error(f"❌ Error processing {f.name}: {str(e)}")

        if results:
            df = pd.DataFrame(results)
            st.subheader("📥 Download Report")
            st.download_button(
                label="Download CSV Report",
                data=df.to_csv(index=False),
                file_name="bone_cancer_batch_results.csv",
                mime="text/csv"
            )
