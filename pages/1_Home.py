import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from trending_colors import get_trending_colors, get_pantone_color_of_year, check_color_compatibility
from theme import apply_theme

apply_theme()

st.title("🏠 Home")
st.write("Welcome to AI Fashion Color Fit Matcher!")
st.write("Use the sidebar to navigate to Upload your photo.")

# Initialize session state if it doesn't exist yet
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

name = st.text_input("What's your name?", value=st.session_state.user_name)

if st.button("Save Name"):
    st.session_state.user_name = name
    st.success(f"Saved! Welcome, {name}")

# ---------------------------------------------------------------
# Trending Colors section
# ---------------------------------------------------------------
st.divider()
st.subheader("🔥 Trending This Season")

# --- Pantone Color of the Year highlight ---
pantone_result = get_pantone_color_of_year()
if pantone_result["error"] is None:
    pantone = pantone_result["pantone"]
    st.markdown(f"""
    <div style="border:2px solid var(--color-primary); border-radius:12px; padding:16px; margin-bottom:16px; background-color:var(--color-secondary);">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="background-color:{pantone['hex']}; width:60px; height:60px; border-radius:8px; border:1px solid var(--color-primary);"></div>
            <div>
                <b>⭐ Pantone Color of the Year: {pantone['name']}</b><br>
                <span style="color:var(--color-text);">{pantone['description']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Trending color swatches ---
trending_result = get_trending_colors()
if trending_result["error"] is None:
    swatch_cols = st.columns(len(trending_result["colors"]))
    for col, color in zip(swatch_cols, trending_result["colors"]):
        with col:
            st.markdown(f"""
            <div style="text-align:center;">
                <div style="background-color:{color['hex']}; width:100%; height:60px; border-radius:8px; border:1px solid var(--color-primary); margin-bottom:6px;"></div>
                <span>{color['name']}</span>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info(trending_result["error"])

# --- Instant skin tone compatibility check ---
st.write("")
st.write("**Is a trending color good for your skin tone?**")

if trending_result["error"] is None:
    color_names = [c["name"] for c in trending_result["colors"]]
    selected_color_name = st.selectbox("Pick a trending color", color_names)

    if st.button("Check compatibility"):
        selected_color = next(c for c in trending_result["colors"] if c["name"] == selected_color_name)
        user_skin_tone = st.session_state.get("stylist_context", {}).get("skin_tone")

        check_result = check_color_compatibility(selected_color["undertone"], user_skin_tone)

        if check_result["error"]:
            st.warning(check_result["error"])
        elif check_result["compatible"]:
            st.success(check_result["message"])
        else:
            st.warning(check_result["message"])
