import streamlit as st
from PIL import Image
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from color_recommender import analyze_and_recommend
from recommender import OutfitRecommender

st.title("✨ Analyze My Look")
st.write("Take a photo, pick your occasion and season, then click one button to get your full personalized style analysis.")

col1, col2 = st.columns(2)
with col1:
    occasion = st.selectbox("Occasion", ["Formal", "Casual", "Party"])
with col2:
    season = st.selectbox("Season", ["Summer", "Winter"])

camera_photo = st.camera_input("Take a photo")

analyze_clicked = st.button("✨ Analyze My Look", disabled=(camera_photo is None))

if camera_photo is None:
    st.info("Take a photo above to enable the Analyze button.")

if analyze_clicked:
    with st.spinner("Analyzing your skin tone..."):
        image = Image.open(camera_photo).convert("RGB")
        save_path = "data/temp_analyze_capture.jpg"
        image.save(save_path)

        result = analyze_and_recommend(save_path)
        time.sleep(0.5)

    if result is None:
        st.error("No face detected. Please retake the photo with better lighting, facing the camera directly.")
    else:
        skin_tone = result["skin_tone"]

        with st.spinner("Finding outfits that match your style..."):
            recommender = OutfitRecommender()
            outfits = recommender.recommend(skin_tone, occasion, season, top_n=5)
            for outfit in outfits:
                outfit["scores"] = recommender.calculate_match_score(outfit)
            time.sleep(0.5)

        st.balloons()

        st.subheader(f"Detected Skin Tone: {skin_tone.upper()}")
        st.subheader(f"Top {len(outfits)} Outfits For You")

        for row_start in range(0, len(outfits), 3):
            row_outfits = outfits[row_start:row_start + 3]
            cols = st.columns(3)

            for col, outfit in zip(cols, row_outfits):
                with col:
                    top_hex = recommender.get_color_hex(outfit["top_color"])
                    bottom_hex = recommender.get_color_hex(outfit["bottom_color"])
                    score = outfit["scores"]["total"]

                    st.markdown(f"""
                    <div style="border:1px solid #444; border-radius:10px; padding:12px; margin-bottom:10px;">
                        <div style="display:flex; gap:5px; margin-bottom:8px;">
                            <div style="background-color:{top_hex}; width:50%; height:40px; border-radius:5px;"></div>
                            <div style="background-color:{bottom_hex}; width:50%; height:40px; border-radius:5px;"></div>
                        </div>
                        <b>Outfit #{outfit['outfit_id']}</b><br>
                        {outfit['top_color']} + {outfit['bottom_color']}
                    </div>
                    """, unsafe_allow_html=True)

                    st.caption(f"Match Score: {score}%")
                    with st.expander("Why this outfit?"):
                        st.write(recommender.explain(outfit))
