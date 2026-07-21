import streamlit as st
import sys
import os

# Allow importing from src folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from color_recommender import analyze_and_recommend
from color_swatches import make_swatch

st.title("📤 Upload Photo")

if "user_name" in st.session_state and st.session_state.user_name:
    st.write(f"Hi {st.session_state.user_name}! Upload your photo below.")
else:
    st.write("Please upload your photo below.")

uploaded = st.file_uploader("Upload photo", type=['jpg', 'jpeg', 'png'])

if uploaded is not None:
    st.session_state.uploaded_photo = uploaded
    st.image(uploaded, caption="Uploaded photo", width=300)

    # Save uploaded file temporarily so OpenCV can read it
    temp_path = "data/temp_upload.jpg"
    with open(temp_path, "wb") as f:
        f.write(uploaded.getbuffer())

    if st.button("Analyze My Skin Tone"):
        result = analyze_and_recommend(temp_path)

        if result:
            st.session_state.skin_tone_result = result
            st.success(f"Your skin tone is: **{result['skin_tone'].upper()}**")

            st.write("### Recommended Colors For You:")
            cols = st.columns(len(result['recommended_colors']))

            for i, color in enumerate(result['recommended_colors']):
                swatch = make_swatch(color['name'], color['hex'])
                with cols[i]:
                    st.image(swatch)
                    st.caption(color['name'])
        else:
            st.error("No face detected. Please try a clearer photo.")
