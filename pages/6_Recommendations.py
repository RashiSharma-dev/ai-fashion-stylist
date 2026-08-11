import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from recommender import OutfitRecommender

st.title("👗 Your Outfit Recommendations")

with st.sidebar:
    st.header("Filters")
    skin_tone = st.selectbox("Skin Tone", ["warm", "cool", "neutral"])
    occasion = st.selectbox("Occasion", ["Formal", "Casual", "Party"])
    season = st.selectbox("Season", ["Summer", "Winter"])
    gender = st.selectbox("Gender", ["Any", "Male", "Female", "Unisex"])
    style = st.selectbox("Style", ["Any", "Ethnic", "Western", "Fusion", "Minimalist", "Bohemian"])


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

    outfits = pool.to_dict("records")
    for outfit in outfits:
        outfit["skin_tone"] = skin_tone

    for outfit in outfits:
        outfit["scores"] = recommender.calculate_match_score(outfit)

    outfits.sort(key=lambda o: o["scores"]["total"], reverse=True)

    return outfits


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
            top_hex = recommender.get_color_hex(outfit["top_color"])
            bottom_hex = recommender.get_color_hex(outfit["bottom_color"])
            scores = outfit["scores"]
            total = scores["total"]

            if total >= 80:
                bar_color = "#4CAF50"
            elif total >= 50:
                bar_color = "#FFC107"
            else:
                bar_color = "#F44336"

            st.markdown(f"""
            <div style="border:1px solid #444; border-radius:10px; padding:12px; margin-bottom:10px;">
                <div style="display:flex; gap:5px; margin-bottom:8px;">
                    <div style="background-color:{top_hex}; width:50%; height:40px; border-radius:5px;"></div>
                    <div style="background-color:{bottom_hex}; width:50%; height:40px; border-radius:5px;"></div>
                </div>
                <b>Outfit #{outfit['outfit_id']}</b><br>
                {outfit['top_color']} + {outfit['bottom_color']}<br>
                <span style="background-color:#D96C8C; padding:2px 8px; border-radius:8px; font-size:12px;">{outfit['occasion']}</span>
                <div style="background-color:#333; border-radius:5px; height:12px; width:100%; margin-top:10px;">
                    <div style="background-color:{bar_color}; width:{total}%; height:12px; border-radius:5px;"></div>
                </div>
                <p style="font-size:13px; margin-top:5px; margin-bottom:0;"><b>{total}% Match</b></p>
            </div>
            """, unsafe_allow_html=True)

            st.caption(f"Skin Match: {scores['skin_match']}% | Color Harmony: {scores['color_harmony']}% ({scores['harmony_label']}) | Occasion: {scores['occasion_fit']}%")

            with st.expander("Why this outfit?"):
                st.write(recommender.explain(outfit))