import streamlit as st

st.title("About the Project")
# st.write("This app classifies brain tumors using MRI scans.")
col1, col2, col3 = st.columns([1, 0.05, 0.6])
with col3:
    # st.markdown("<h3 style='text-align: center;'>Brain Tumor Types</h3>", unsafe_allow_html=True)
    st.image(
        "https://www.mdpi.com/applsci/applsci-10-01999/article_deploy/html/images/applsci-10-01999-g001.png", 
        caption="Brain Tumor MRI (Reference)", 
        use_container_width=True
    )
with col1:
  st.markdown(
              """
              This project uses a Convolutional Neural Network (CNN) to classify brain tumors from MRI scans.
              The model is trained on a dataset of brain MRI images and can identify four types of tumors:
              - Glioma Tumor
              - Meningioma Tumor
              - No Tumor
              - Pituitary Tumor
              """
          )
  st.markdown(
      """
      ### How to Use
      1. Upload an MRI image using the file uploader.
      2. The model will process the image and provide a prediction along with confidence level.
      3. Optionally, enter your email to receive the result via email.
      """
    )
  
st.markdown("<hr style='border-top: 1px solid #bbb;'>", unsafe_allow_html=True)
st.markdown(
    """
    ##### Disclaimer
    This tool is for educational and research purposes only. It is not FDA-approved or clinically certified. Always consult a licensed medical professional for diagnosis and treatment.
    """
  )