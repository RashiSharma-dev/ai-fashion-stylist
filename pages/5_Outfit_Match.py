import streamlit as st
from PIL import Image
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from outfit_compatibility import check_outfit_compatibility

st.title("✨ Outfit + Skin Tone Compatibility Checker")
st.write("Upload a selfie and an outfit photo to see if the color works for you.")

col1, col2 = st.columns(2)

with col1:
    selfie_file = st.file_uploader("Upload your selfie", type=["jpg", "jpeg", "png"], key="selfie")
with col2:
    outfit_file = st.file_uploader("Upload outfit photo", type=["jpg", "jpeg", "png"], key="outfit")

if selfie_file is not None and outfit_file is not None:
    selfie_image = Image.open(selfie_file).convert("RGB")
    outfit_image = Image.open(outfit_file).convert("RGB")

    selfie_path = "data/temp_selfie.jpg"
    outfit_path = "data/temp_outfit.jpg"
    selfie_image.save(selfie_path)
    outfit_image.save(outfit_path)

    col1.image(selfie_image, caption="Your Selfie", use_column_width=True)
    col2.image(outfit_image, caption="Your Outfit", use_column_width=True)

    result = check_outfit_compatibility(selfie_path, outfit_path)

    if result is None:
        st.error("No face detected in your selfie. Please try a clearer photo.")
    else:
        st.subheader("Result")
        if result["is_recommended"]:
            st.success(result["message"])
        else:
            st.warning(result["message"])

        st.write(f"Detected skin tone: **{result['skin_tone'].upper()}**")
        st.color_picker("Outfit's dominant color", result["outfit_hex"], disabled=True)
