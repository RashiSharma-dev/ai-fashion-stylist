import streamlit as st
from PIL import Image
import numpy as np
import cv2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from color_overlay import apply_color_overlay

st.title("🎨 Virtual Try-On: Color Overlay")
st.write("Upload a photo and preview how a color overlay looks, with adjustable strength.")

uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    strength = st.slider("Overlay Strength", 0, 100, 40)

    test_color_bgr = (30, 30, 220)

    result_bgr = apply_color_overlay(image_bgr, test_color_bgr, strength)
    result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)

    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Original", width="stretch")
    with col2:
        st.image(result_rgb, caption=f"With {strength}% Red Overlay", width="stretch")
