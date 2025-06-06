import streamlit as st

# ✅ Set page config at the top
st.set_page_config(
    page_title="Brain Tumor Classification", 
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import gdown
import os
import time
import streamlit_shadcn_ui as ui
# Import your email service module
import email_service

# Load model if not cached
MODEL_DIR = "./model"
MODEL_PATH = os.path.join(MODEL_DIR, "brain_tumor_classification.keras")
GOOGLE_DRIVE_FILE_ID = "10nlJfTiDtu4Gokx5HndDQPAwDU2FwgXf"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_DIR, exist_ok=True)
        gdown.download(f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}", MODEL_PATH, quiet=False)
    return tf.keras.models.load_model(MODEL_PATH)

model = load_model()
CLASS_LABELS = ["Glioma Tumor", "Meningioma Tumor", "No Tumor", "Pituitary Tumor"]

# Set layout
col1, _, col3 = st.columns([1, 0.2, 2])

# File uploader in col3
with col3:
    st.title("🧠 Brain Tumor Classification")
    st.write("Upload an MRI scan to classify the type of tumor.")
    uploaded_file = st.file_uploader("Choose an MRI image...", type=["jpg", "png", "jpeg"])

    if not uploaded_file or "last_uploaded_filename" not in st.session_state or uploaded_file.name != st.session_state["last_uploaded_filename"]:
        st.session_state.clear()
        st.session_state["last_uploaded_filename"] = uploaded_file.name if uploaded_file else None

# 🧠 Always show reference image and uploaded image (if present)
with col1:
    if uploaded_file:
        st.markdown("<h4 style='text-align: center;'>Uploaded MRI Image</h4>", unsafe_allow_html=True)
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
    else:
      st.image("./assets/doctor-looking-at-MRI.jpg", use_container_width=True)

with col3:
    if not uploaded_file:
        st.markdown(
            """
            <div style="background-color: #fcf7fa; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                <h3>🤖 How the Model Works</h3>
                <p>This ML model uses a Convolutional Neural Network (CNN) trained on thousands of labeled MRI images. It extracts features from the uploaded image and classifies it into one of four categories:</p>
                <ul>
                    <li>Glioma Tumor</li>
                    <li>Meningioma Tumor</li>
                    <li>Pituitary Tumor</li>
                    <li>No Tumor</li>
                </ul>
                <p>A probability score is also provided to indicate the model’s confidence in its prediction.</p>
                <p styles="margin: 0px;">To learn more about the project, <a href="/About" target="_self" style="text-decoration: none; color: blue;">click here </a></p>
                
            </div>
            
            """,
            unsafe_allow_html=True
        )
    # st.markdown("<h3 style='text-align: center;'>Brain Tumor Types</h3>", unsafe_allow_html=True)
    # st.image(
    #     "https://www.mdpi.com/applsci/applsci-10-01999/article_deploy/html/images/applsci-10-01999-g001.png", 
    #     caption="Brain Tumor MRI (Reference)", 
    #     use_container_width=True
    # )

# 🔄 Only run prediction if file is uploaded and no prediction exists in session
if uploaded_file and "predicted_class" not in st.session_state:
    with col3:
        image = Image.open(uploaded_file)

        # Progress bar
        progress_bar = st.progress(0, text="Initializing...")

        for i in range(61):
            time.sleep(0.05)
            if i < 20:
                progress_bar.progress(i, text="Preprocessing Image...")
            elif i < 40:
                progress_bar.progress(i, text="Loading Model...")
            elif i < 60:
                progress_bar.progress(i, text="Making Prediction...")
            else:
                progress_bar.progress(i, text="Finalizing...")

        def preprocess_image(image):
            img = np.array(image)
            img = cv2.resize(img, (224, 224))
            img = img / 255.0
            img = np.expand_dims(img, axis=0)
            return img

        processed_image = preprocess_image(image)
        prediction = model.predict(processed_image)
        predicted_index = np.argmax(prediction)
        predicted_class = CLASS_LABELS[predicted_index]
        confidence = prediction[0][predicted_index] * 100

        progress_bar.progress(100, text="Processing complete!")
        time.sleep(1)
        progress_bar.empty()

        # Store in session
        st.session_state["predicted_class"] = predicted_class
        st.session_state["confidence"] = confidence

# ✅ If prediction exists, show it and email input
if "predicted_class" in st.session_state and uploaded_file:
    with col3:
        left_card, middle_card, right_card = st.columns([1, 0.7, 0.5])

        with left_card:
            with ui.card(
                title=" Prediction",
                content=st.session_state.predicted_class,
                # description=st.session_state.predicted_class,
                key="prediction_card"
            ):
                st.markdown("")

        with middle_card:
            with ui.card(
                title="Confidence",
                content=f"{st.session_state.confidence:.2f}%",
                key="confidence_card"
            ):
              st.markdown("")


        # HTML and CSS for circular progress bar
        progress_bar = f"""
        <div style="position: relative; width: 150px; height: 150px;">
          <svg viewBox="0 0 36 36" width="150" height="150" style="transform: rotate(-90deg);">
            <path
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke="#eee"
              stroke-width="3.8"
            />
            <path
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke="#ed76c2"
              stroke-width="3.8"
              stroke-dasharray="{st.session_state.confidence}, 100"
              stroke-linecap="round"
            />
          </svg>
          <div style="position: absolute; top: 0; left: 0; width: 150px; height: 150px;
                      display: flex; align-items: center; justify-content: center;
                      font-size: 24px;">
            {st.session_state.confidence:.2f}%
          </div>
        </div>
        """

        with right_card:
          st.markdown(progress_bar, unsafe_allow_html=True)


        # Initialize session state keys
        if "sending_email" not in st.session_state:
            st.session_state["sending_email"] = False
        if "email_sent" not in st.session_state:
            st.session_state["email_sent"] = False
        if "email" not in st.session_state:
            st.session_state["email"] = ""

        # st.divider()
        st.markdown("<hr style='border-top: 1px solid #bbb;'>", unsafe_allow_html=True)

        # Email input
        st.markdown("##### Enter your email to receive the result")
        email = st.text_input("Enter your email to receive the result:", placeholder="Email", label_visibility="collapsed", key="email")



        # Define button label dynamically
        button_label = "📤 Sending Email..." if st.session_state["sending_email"] else "Send Result via Email"
        if st.session_state["email_sent"]:
            button_label = "📩 Email Sent!"
        
        def handle_email_button():
          if email:
            st.session_state["sending_email"] = True
            st.session_state["email_sent"] = False

        def handle_reset_email():
            st.session_state["sending_email"] = False
            st.session_state["email_sent"] = False
            st.session_state["email"] = ""
              
        # Handle button click
        if st.button(button_label, on_click=handle_email_button, disabled=st.session_state["sending_email"]):
          if not email:
            st.error("❌ Please enter a valid email address.")

        # Perform email sending if triggered
        if st.session_state["sending_email"] and not st.session_state["email_sent"]:
            with st.spinner("📤 Sending Email..."):
                try:
                    email_service.send_email(email, st.session_state["predicted_class"])  # Simulated email sending
                    st.session_state["email_sent"] = True
                    st.success("📩 Result sent successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to send email: {e}")

            # **Update button state after email is sent**
            st.session_state["sending_email"] = False
        
        if st.session_state["email_sent"]:
          st.button("Send another mail", on_click=handle_reset_email)

if uploaded_file:
  with col3:
      st.write("### Predicted Result Information")
      about_section_col1, about_section_col2 = st.columns([0.4, 1])
      with about_section_col1:
          st.image("./assets/Understanding-Brain-Tumors.jpg", use_container_width=True, width=150)
      with about_section_col2:
          st.markdown("""
          Based on the uploaded MRI scan, the model has analyzed the image and predicted the type of brain condition. Below are details related to the predicted result.

          """)

          # Example: Replace `predicted_class` with your actual prediction variable
          if st.session_state.predicted_class == "Glioma Tumor":
              st.markdown("""
              #### 🧠 Glioma Tumor
              **Description:**  
              Gliomas are tumors that originate in the glial cells of the brain or spine. These are typically malignant and can grow rapidly.

              **Common Symptoms:**  
              - Headaches
              - Seizures
              - Nausea or vomiting
              - Memory loss
              - Personality changes

              **Note:** Early diagnosis and medical consultation are crucial for treatment planning.
              """)

          elif st.session_state.predicted_class == "Meningioma Tumor":
              st.markdown("""
              #### 🧠 Meningioma Tumor
              **Description:**  
              Meningiomas are usually benign tumors that form in the meninges (the layers of tissue covering the brain and spinal cord).

              **Common Symptoms:**  
              - Headaches
              - Vision problems
              - Hearing loss
              - Weakness in limbs
              - Trouble with memory or speech

              **Note:** They grow slowly and are often found incidentally during scans for other conditions.
              """)

          elif st.session_state.predicted_class == "Pituitary Tumor":
              st.markdown("""
              #### 🧠 Pituitary Tumor
              **Description:**  
              Pituitary tumors grow in the pituitary gland and can affect hormone production, leading to various systemic symptoms.

              **Common Symptoms:**  
              - Vision problems
              - Hormonal imbalances
              - Unexplained fatigue
              - Irregular menstruation or sexual dysfunction
              - Growth issues

              **Note:** Treatment may involve surgery, radiation, or medications depending on the size and activity.
              """)

          elif st.session_state.predicted_class == "No Tumor":
              st.markdown("""
              #### ✅ No Tumor Detected
              The scan does not show signs of a brain tumor.

              **Recommendation:**  
              If you're experiencing symptoms, it's important to consult a medical professional for further evaluation.
              """)

          # Optional: Add a horizontal line or divider
          st.divider()

  with col1:
      st.markdown(
        """
        <div style="background-color: #fcf7fa; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
            <h3>What Should You Do After Prediction?</h3>
            <h5>If a tumor is detected:</h5>
            <ol>
                <li>Do not panic — the model is a support tool, not a definitive diagnosis.</li>
                <li>Consult a neurologist or oncologist with your MRI scan and symptoms.</li>
                <li>Request additional tests, such as contrast-enhanced MRIs or biopsies.</li>
                <li>Follow up regularly to monitor any changes.</li>
            </ol>
            <h6>If no tumor is detected but symptoms persist, consider a medical consultation for further investigation.</h6>
        </div>
        """,
        unsafe_allow_html=True
    )
