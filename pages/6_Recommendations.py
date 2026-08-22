import streamlit as st
import sys
import os
import datetime
import numpy as np
import cv2
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from recommender import OutfitRecommender
from user_profile import save_profile, load_profile
from torso_overlay import apply_torso_overlay
from report_generator import generate_style_report

st.title("👗 Your Outfit Recommendations")

with st.sidebar:
    st.header("Your Profile")

    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    name_input = st.text_input("Enter your name", value=st.session_state.user_name)

    if name_input:
        st.session_state.user_name = name_input
        profile = load_profile(name_input)

        if profile:
            st.success(f"Welcome back, {name_input}! 👋")
            st.caption(f"Last search: {profile['skin_tone'].title()} skin, {profile['occasion']}, {profile['season']}")
            st.caption(f"Top match last time: Outfit #{profile['top_outfit_id']} ({profile['top_score']}%)")
            st.caption(f"Last visit: {profile['last_updated']}")
        else:
            st.info("New profile! Your preferences will be saved after your first search below.")

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


st.subheader("Step 1: Upload a photo for try-on previews (optional)")
tryon_photo = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"], key="tryon_upload")

if tryon_photo is not None:
    tryon_image = Image.open(tryon_photo).convert("RGB")
    st.session_state.tryon_image_np = np.array(tryon_image)

if "preview_outfit_id" not in st.session_state:
    st.session_state.preview_outfit_id = None

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

            preview_disabled = "tryon_image_np" not in st.session_state
            if st.button("👕 Preview on My Photo", key=f"preview_{outfit['outfit_id']}", disabled=preview_disabled):
                st.session_state.preview_outfit_id = outfit["outfit_id"]

if "tryon_image_np" not in st.session_state and st.session_state.preview_outfit_id is None:
    st.info("👆 Upload a photo above to enable 'Preview on My Photo' buttons.")

if st.session_state.preview_outfit_id is not None and "tryon_image_np" in st.session_state:
    preview_outfit = next((o for o in display_outfits if o["outfit_id"] == st.session_state.preview_outfit_id), None)

    if preview_outfit:
        st.divider()
        st.subheader(f"Preview: How you'd look in {preview_outfit['top_color'].upper()}")

        top_hex = recommender.get_color_hex(preview_outfit["top_color"])
        top_rgb = tuple(int(top_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        top_bgr = (top_rgb[2], top_rgb[1], top_rgb[0])

        image_bgr = cv2.cvtColor(st.session_state.tryon_image_np, cv2.COLOR_RGB2BGR)
        result_bgr, error = apply_torso_overlay(image_bgr, top_bgr, strength=50)

        if error:
            st.error("No face detected in your uploaded photo. Please upload a clearer photo.")
        else:
            result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)

            preview_col1, preview_col2 = st.columns(2)
            with preview_col1:
                st.image(st.session_state.tryon_image_np, caption="Original", width="stretch")
            with preview_col2:
                st.image(result_rgb, caption=f"Outfit #{preview_outfit['outfit_id']} Preview", width="stretch")

if st.session_state.user_name and display_outfits:
    save_profile(st.session_state.user_name, {
        "skin_tone": skin_tone,
        "occasion": occasion,
        "season": season,
        "gender": gender,
        "style": style,
        "top_outfit_id": display_outfits[0]["outfit_id"],
        "top_score": display_outfits[0]["scores"]["total"],
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    })

st.divider()
st.subheader("📄 Download Your Style Report")

report_name = st.session_state.user_name if st.session_state.user_name else "Guest"

if display_outfits:
    html_report = generate_style_report(
        name=report_name,
        skin_tone=skin_tone,
        top_outfits=display_outfits[:3],
        preview_image_np=None
    )

    st.download_button(
        label="⬇️ Download Your Style Report",
        data=html_report,
        file_name=f"{report_name.lower().replace(' ', '_')}_style_report.html",
        mime="text/html"
    )

    st.caption("Downloads as an HTML file — open it in any browser, or use your browser's Print → Save as PDF to convert it.")