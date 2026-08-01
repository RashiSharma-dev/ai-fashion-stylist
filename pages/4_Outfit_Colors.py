import streamlit as st
from PIL import Image
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from dominant_color_extractor import extract_dominant_colors
from palette_generator import create_palette_image, rgb_to_hex

st.title("👕 Outfit Color Extractor")
st.write("Upload a photo of a clothing item to see its dominant colors.")

uploaded_file = st.file_uploader("Upload a clothing image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Clothing Item", use_column_width=True)

    save_path = "data/temp_clothing.jpg"
    image.convert("RGB").save(save_path)

    colors = extract_dominant_colors(save_path)
    palette_image = create_palette_image(colors)

    st.subheader("Dominant Colors")
    st.image(palette_image, use_column_width=False)

    hex_codes = [rgb_to_hex(color) for color in colors]
    st.write(", ".join(hex_codes))
