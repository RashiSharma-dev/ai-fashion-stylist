import streamlit as st
from PIL import Image
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from color_recommender import analyze_and_recommend

st.title("📸 Webcam Skin Tone Capture")
st.write("Take a live photo with your webcam to instantly check your skin tone.")

camera_photo = st.camera_input("Take a photo")

if camera_photo is not None:
    image = Image.open(camera_photo).convert("RGB")

    save_path = "data/temp_webcam_capture.jpg"
    image.save(save_path)

    st.image(image, caption="Your Captured Photo", width="stretch")

    result = analyze_and_recommend(save_path)

    if result.get("error"):
        st.error(result["error"])
    else:
        skin_tone = result["skin_tone"]
        recommended_colors = result["recommended_colors"]

        st.subheader(f"Detected Skin Tone: {skin_tone.upper()}")

        st.write("**Recommended colors for you:**")
        swatch_cols = st.columns(len(recommended_colors))
        for col, color in zip(swatch_cols, recommended_colors):
            with col:
                st.markdown(
                    f"""<div style="background-color:{color['hex']}; height:50px; border-radius:5px; border:1px solid #444;"></div>""",
                    unsafe_allow_html=True
                )
                st.caption(color["name"])