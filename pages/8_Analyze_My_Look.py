import streamlit as st
from PIL import Image
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from color_recommender import analyze_and_recommend
from recommender import OutfitRecommender
from chatbot import set_analysis_context
from occasion_advisor import get_occasion_guidance, map_to_recommender_occasion

st.title("✨ Analyze My Look")
st.write("Take a photo, pick your occasion and season, then click one button to get your full personalized style analysis.")

# --- Occasion selector: styled icon buttons instead of a plain dropdown ---
st.subheader("Choose Your Occasion")

OCCASIONS = [
    ("Casual", "👕"),
    ("Office/Formal", "👔"),
    ("Wedding Guest", "💍"),
    ("Party", "🎉"),
    ("Date Night", "❤️"),
    ("Outdoor", "🌳"),
]

if "selected_occasion" not in st.session_state:
    st.session_state.selected_occasion = "Casual"

occasion_cols = st.columns(3)
for index, (name, icon) in enumerate(OCCASIONS):
    col = occasion_cols[index % 3]
    is_selected = st.session_state.selected_occasion == name
    with col:
        button_type = "primary" if is_selected else "secondary"
        if st.button(f"{icon} {name}", key=f"occasion_{name}", width="stretch", type=button_type):
            st.session_state.selected_occasion = name

occasion = st.session_state.selected_occasion

# Show DO / DON'T color tips for the chosen occasion
guidance_result = get_occasion_guidance(occasion)
if guidance_result["error"] is None:
    with st.expander(f"💡 Color tips for {occasion}"):
        do_list = ", ".join(guidance_result["guidance"]["do_colors"])
        dont_list = ", ".join(guidance_result["guidance"]["dont_colors"])
        st.markdown(f"**Do wear:** {do_list}")
        st.markdown(f"**Avoid:** {dont_list}")

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

    if result.get("error"):
        st.error(result["error"])
    else:
        skin_tone = result["skin_tone"]

        # Map the specific occasion (e.g. "Wedding Guest") down to the
        # broad category ("Formal") that the scoring engine understands
        recommender_occasion = map_to_recommender_occasion(occasion)

        with st.spinner("Finding outfits that match your style..."):
            recommender = OutfitRecommender()
            outfits = recommender.recommend(skin_tone, recommender_occasion, season, top_n=5)
            for outfit in outfits:
                outfit["scores"] = recommender.calculate_match_score(outfit)
            time.sleep(0.5)

        # Let the AI Stylist chatbot know about this analysis, using the
        # SPECIFIC occasion (not the mapped broad category) so it can give
        # hyper-specific advice like "for a wedding guest look..."
        set_analysis_context(
            skin_tone=skin_tone,
            occasion=occasion,
            image_path=save_path
        )

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

        st.divider()
        st.page_link("pages/10_AI_Stylist_Chat.py", label="💬 Discuss my results with the AI Stylist", icon="🎨")