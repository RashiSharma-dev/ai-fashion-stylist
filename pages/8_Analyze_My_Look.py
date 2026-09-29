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
from style_advisor import get_combined_style_advice

st.title("✨ Analyze My Look")
st.write("Take a photo, pick your occasion, season, and body shape, then click one button to get your full personalized style analysis.")

# --- Occasion selector: styled icon buttons ---
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

guidance_result = get_occasion_guidance(occasion)
if guidance_result["error"] is None:
    with st.expander(f"💡 Color tips for {occasion}"):
        do_list = ", ".join(guidance_result["guidance"]["do_colors"])
        dont_list = ", ".join(guidance_result["guidance"]["dont_colors"])
        st.markdown(f"**Do wear:** {do_list}")
        st.markdown(f"**Avoid:** {dont_list}")

season = st.selectbox("Season", ["Summer", "Winter"])

# --- Body shape selector: SELF-SELECTED, not auto-detected ---
st.subheader("Your Body Shape")
st.caption(
    "We ask you to self-select for now, since reliable automated detection "
    "requires full-body pose estimation — see the README's Future Scope "
    "section for more on that."
)

BODY_SHAPES = ["Hourglass", "Pear", "Apple", "Rectangle", "Inverted Triangle"]
body_shape = st.selectbox("Select your body shape", BODY_SHAPES)

from body_shape_advisor import get_body_shape_guidance
shape_guidance_result = get_body_shape_guidance(body_shape)
if shape_guidance_result["error"] is None:
    with st.expander(f"💡 Fit tips for {body_shape}"):
        st.write(shape_guidance_result["guidance"]["description"])
        fits = ", ".join(shape_guidance_result["guidance"]["recommended_fits"])
        avoid = ", ".join(shape_guidance_result["guidance"]["avoid_fits"])
        st.markdown(f"**Look for:** {fits}")
        st.markdown(f"**Avoid:** {avoid}")

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
        recommender_occasion = map_to_recommender_occasion(occasion)

        with st.spinner("Finding outfits that match your style..."):
            recommender = OutfitRecommender()
            outfits = recommender.recommend(skin_tone, recommender_occasion, season, top_n=5)
            for outfit in outfits:
                outfit["scores"] = recommender.calculate_match_score(outfit)
            time.sleep(0.5)

            set_analysis_context(
            skin_tone=skin_tone,
            occasion=occasion,
            image_path=save_path,
            body_shape=body_shape,
            style_personality=style_personality
        )

        st.balloons()

        st.subheader(f"Detected Skin Tone: {skin_tone.upper()}")

        # --- Combined style advice: skin tone + occasion + body shape ---
        style_personality = st.session_state.get("style_personality")
        combined_result = get_combined_style_advice(skin_tone, occasion, body_shape, style_personality)
        if combined_result["error"] is None:
            st.info(combined_result["advice"])

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