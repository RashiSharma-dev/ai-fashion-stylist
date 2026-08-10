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


def get_filtered_outfits(recommender, skin_tone, occasion, season, gender, style):
    recommended_names = [c["name"] for c in recommender.color_rules[skin_tone]["best_colors"]]
    df = recommender.df

    base = df[df["top_color"].isin(recommended_names)]

    if gender != "Any":
        base = base[(base["gender"] == gender) | (base["gender"] == "Unisex")]
    if style != "Any":
        base = base[base["style_type"] == style]

    exact = base[(base["occasion"] == occasion) & (base["season"] == season)]
    if len(exact) > 0:
        exact = exact.copy()
        exact["match_level"] = "exact"
        pool = exact
    else:
        relaxed = base[base["occasion"] == occasion]
        if len(relaxed) > 0:
            relaxed = relaxed.copy()
            relaxed["match_level"] = "season_relaxed"
            pool = relaxed
        else:
            fallback = base.copy()
            fallback["match_level"] = "color_only"
            pool = fallback

    pool = pool.copy()
    pool["match_score"] = pool["match_level"].map(MATCH_SCORES)
    pool = pool.sort_values("match_score", ascending=False)

    outfits = pool.to_dict("records")
    for outfit in outfits:
        outfit["skin_tone"] = skin_tone

    return outfits


st.title("👗 Your Outfit Recommendations")

with st.sidebar:
    st.header("Filters")
    skin_tone = st.selectbox("Skin Tone", ["warm", "cool", "neutral"])
    occasion = st.selectbox("Occasion", ["Formal", "Casual", "Party"])
    season = st.selectbox("Season", ["Summer", "Winter"])
    gender = st.selectbox("Gender", ["Any", "Male", "Female", "Unisex"])
    style = st.selectbox("Style", ["Any", "Ethnic", "Western", "Fusion", "Minimalist", "Bohemian"])

recommender = OutfitRecommender()
all_outfits = get_filtered_outfits(recommender, skin_tone, occasion, season, gender, style)

total_found = len(all_outfits)
display_outfits = all_outfits[:5]

st.subheader(f"Showing {len(display_outfits)} of {total_found} matching outfits")

for row_start in range(0, len(display_outfits), 3):
    row_outfits = display_outfits[row_start:row_start + 3]
    cols = st.columns(3)

    for col, outfit in zip(cols, row_outfits):
        with col:
            top_hex = get_color_hex(outfit["top_color"])
            bottom_hex = get_color_hex(outfit["bottom_color"])
            score = outfit["match_score"]

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