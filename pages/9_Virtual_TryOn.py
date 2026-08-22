import streamlit as st
from PIL import Image
import numpy as np
import cv2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from torso_overlay import apply_torso_overlay
from outfit_compatibility import get_all_known_colors, identify_color_name

st.title("🎨 Virtual Try-On: Color Overlay")
st.write("Upload a photo, pick a color, and preview how it would look on you.")

uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    col_picker, col_slider = st.columns(2)
    with col_picker:
        chosen_hex = st.color_picker("Choose outfit color", "#4169E1")
    with col_slider:
        strength = st.slider("Overlay Strength", 0, 100, 50)

    chosen_rgb = tuple(int(chosen_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    chosen_bgr = (chosen_rgb[2], chosen_rgb[1], chosen_rgb[0])

    known_colors = get_all_known_colors()
    color_name, distance = identify_color_name(chosen_hex, known_colors)

    if color_name is None:
        color_name = "your chosen color"

    result_bgr, error = apply_torso_overlay(image_bgr, chosen_bgr, strength)

    if error:
        st.error("No face detected. Please try a clearer photo, facing the camera directly.")
    else:
        result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)

        st.subheader(f"Preview: How you'd look in {color_name.upper()}")

        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Original", width="stretch")
        with col2:
            st.image(result_rgb, caption=f"Try-On Preview ({strength}% strength)", width="stretch")