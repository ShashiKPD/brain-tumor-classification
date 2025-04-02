import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image

import streamlit as st
import tensorflow as tf
import gdown
import os

MODEL_PATH = "brain_tumor_classification.keras"
GOOGLE_DRIVE_FILE_ID = "10nlJfTiDtu4Gokx5HndDQPAwDU2FwgXf"  # Replace with your actual file ID

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):  
        # st.write("Downloading model (may take a few minutes)...")
        gdown.download(f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}", MODEL_PATH, quiet=False)
    return tf.keras.models.load_model(MODEL_PATH)

model = load_model()

# @st.cache_resource
# def load_model():
#     return tf.keras.models.load_model("brain_tumor_classification.keras")

# model = load_model()

CLASS_LABELS = ["Glioma Tumor", "Meningioma Tumor", "No Tumor", "Pituitary Tumor"]

st.title("🧠 Brain Tumor Classification")
st.write("Upload an MRI scan to classify the type of tumor.")

uploaded_file = st.file_uploader("Choose an MRI image...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)

def preprocess_image(image):
    img = np.array(image)  # Convert to NumPy array
    img = cv2.resize(img, (224, 224))  # Resize for model
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

if uploaded_file:
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image)
    predicted_class = CLASS_LABELS[np.argmax(prediction)]  # Get the highest probability class

    st.write(f"### 🏥 Prediction: **{predicted_class}**")

if uploaded_file:
    st.image(image, caption="Uploaded MRI Image", use_container_width=True)