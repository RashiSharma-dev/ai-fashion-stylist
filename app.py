import streamlit as st
st.markdown("""
    <style>
    .stButton>button {
        border-radius: 8px;
        border: 1px solid #D96C8C;
    }
    </style>
""", unsafe_allow_html=True)
import cv2
import numpy as np
from PIL import Image

st.title("AI Fashion Color Fit Matcher")
st.button("Test Button")
st.write("### Upload Your Photo")

uploaded = st.file_uploader("Upload photo", type=['jpg', 'jpeg', 'png'])

if uploaded is not None:
    # Show the uploaded image
    st.image(uploaded, caption="Your uploaded photo")

    # Convert the uploaded file to an OpenCV-compatible format
    image = Image.open(uploaded)
    image_array = np.array(image)
    opencv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

    # Show image metadata
    st.write("**Image size and shape:**")
    st.write(f"Shape: {opencv_image.shape}")
    st.write(f"Width: {image.width}px, Height: {image.height}px")
else:
    st.write("Please upload a photo to see it here.")
