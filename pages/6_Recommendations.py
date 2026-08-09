import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from recommender import OutfitRecommender
from color_recommender import load_color_rules

BOTTOM_COLOR_HEX = {
    "Black": "#000000",
    "White": "#FFFFFF",
    "Navy": "#000080",
    "Grey": "#808080",
    "Beige": "#F5F5DC",
    "Denim Blue": "#1560BD",
}

MATCH_SCORES = {
    "exact": 100,
    "season_relaxed": 75,
    "color_only": 50,
}


def get_color_hex(color_name):
    if color_name in BOTTOM_COLOR_HEX:
        return BOTTOM_COLOR_HEX[color_name]

    rules = load_color_rules()
    for skin_tone_data in rules.values():
        for c in skin_tone_data["best_colors"]:
            if c["name"] == color_name:
                return c["hex"]

    return "#CCCCCC"


st.title("👗 Your Outfit Recommendations")

col1, col2, col3 = st.columns(3)
with col1:
    skin_tone = st.selectbox("Skin Tone", ["warm", "cool", "neutral"])
with col2:
    occasion = st.selectbox("Occasion", ["Formal", "Casual", "Party"])
with col3:
    season = st.selectbox("Season", ["Summer", "Winter"])

if st.button("Get Recommendations"):
    recommender = OutfitRecommender()
    outfits = recommender.recommend(skin_tone, occasion, season, top_n=5)

    st.subheader(f"Top {len(outfits)} Outfits For You")

    for row_start in range(0, len(outfits), 3):
        row_outfits = outfits[row_start:row_start + 3]
        cols = st.columns(3)

        for col, outfit in zip(cols, row_outfits):
            with col:
                top_hex = get_color_hex(outfit["top_color"])
                bottom_hex = get_color_hex(outfit["bottom_color"])
                score = MATCH_SCORES[outfit["match_level"]]

                st.markdown(f"""
                <div style="border:1px solid #444; border-radius:10px; padding:12px; margin-bottom:10px;">
                    <div style="display:flex; gap:5px; margin-bottom:8px;">
                        <div style="background-color:{top_hex}; width:50%; height:40px; border-radius:5px;"></div>
                        <div style="background-color:{bottom_hex}; width:50%; height:40px; border-radius:5px;"></div>
                    </div>
                    <b>Outfit #{outfit['outfit_id']}</b><br>
                    {outfit['top_color']} + {outfit['bottom_color']}<br>
                    <span style="background-color:#D96C8C; padding:2px 8px; border-radius:8px; font-size:12px;">{outfit['occasion']}</span>
                </div>
                """, unsafe_allow_html=True)

                st.progress(score / 100)
                st.caption(f"Match Score: {score}%")

                with st.expander("Why this outfit?"):
                    st.write(recommender.explain(outfit))
