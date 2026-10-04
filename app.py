import streamlit as st
import cv2
import numpy as np
from PIL import Image

from src.theme import apply_theme

# Must be the FIRST Streamlit command in the file
st.set_page_config(page_title="AI Fashion Color Fit Matcher", page_icon="✨")

apply_theme()

# Page-specific style: rounded buttons with a primary-colored border
st.markdown("""
    <style>
    .stButton>button {
        border-radius: 8px;
        border: 1px solid var(--color-primary);
    }
    </style>
""", unsafe_allow_html=True)

st.title("AI Fashion Color Fit Matcher")
st.subheader("Upload Your Photo")

uploaded = st.file_uploader("Upload photo", type=["jpg", "jpeg", "png"])

if uploaded is not None:
    # Show the uploaded image
    st.image(uploaded, caption="Your uploaded photo")

    # Convert to RGB first (PNGs can have a hidden transparency channel),
    # then to OpenCV's BGR format
    image = Image.open(uploaded).convert("RGB")
    image_array = np.array(image)
    opencv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

    # Show image metadata
    st.write("**Image size and shape:**")
    st.write(f"Shape: {opencv_image.shape}")
    st.write(f"Width: {image.width}px, Height: {image.height}px")
else:
    st.write("Please upload a photo to see it here.")