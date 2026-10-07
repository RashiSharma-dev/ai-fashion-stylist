import streamlit as st
import matplotlib.pyplot as plt

from src.analytics import load_analytics, get_top_colors, get_occasion_breakdown
from src.theme import apply_theme, PALETTE
from src.ui_states import empty_state

st.set_page_config(page_title="Your Dashboard", page_icon="📊", layout="wide")
apply_theme()

# Chart colors come from the central palette, so charts match the app
BG = PALETTE["secondary"]
PINK = PALETTE["primary"]
TEXT = PALETTE["text"]
PIE_COLORS = [PALETTE["primary"], PALETTE["accent"], PALETTE["text"], "#B8547A", "#8E3B5C", "#F2A0B5"]


def style_axes(fig, ax):
    """Make a matplotlib chart use our dark/pink theme."""
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.tick_params(colors=TEXT)
    for spine in ax.spines.values():
        spine.set_color(TEXT)


st.title("📊 Your Style Dashboard")
st.caption("A snapshot of your activity in the AI Fashion Stylist.")

result = load_analytics()
if result["error"]:
    st.warning(result["error"])
stats = result["data"]

# --- Brand-new user: nothing recorded yet ---
total_activity = stats["photos_analyzed"] + stats["outfits_viewed"] + stats["chat_messages_sent"]
if total_activity == 0:
    empty_state(
        "📊",
        "Your dashboard is empty for now",
        "Analyze a photo, browse outfits, or chat with your stylist, and your stats will appear here."
    )
    st.page_link("pages/8_Analyze_My_Look.py", label="Start with Analyze My Look", icon="✨")

# --- Row 1: three big numbers ---
col1, col2, col3 = st.columns(3)
col1.metric("📸 Photos analyzed", stats["photos_analyzed"])
col2.metric("👗 Outfits viewed", stats["outfits_viewed"])
col3.metric("💬 Chatbot messages sent", stats["chat_messages_sent"])

st.divider()

# --- Row 2: the two charts as tabs that fade in smoothly ---
tab_colors, tab_occasions = st.tabs(["🎨 Most Recommended Colors", "🎉 Occasions Styled"])

with tab_colors:
    st.subheader("Your Most Recommended Colors")
    top = get_top_colors(5)
    if not top["colors"]:
        empty_state(
            "🎨",
            "No color history yet",
            "Run 'Analyze My Look' and your most recommended colors will show up here."
        )
    else:
        names = [c[0] for c in top["colors"]]
        counts = [c[1] for c in top["colors"]]
        fig, ax = plt.subplots(figsize=(8, 4))
        style_axes(fig, ax)
        ax.barh(names, counts, color=PINK)
        ax.invert_yaxis()  # biggest bar on top
        ax.set_xlabel("Times recommended", color=TEXT)
        st.pyplot(fig)
        plt.close(fig)

with tab_occasions:
    st.subheader("Occasions You've Styled For")
    occ = get_occasion_breakdown()
    if not occ["occasions"]:
        empty_state(
            "🎉",
            "No occasion history yet",
            "Pick an occasion on Analyze My Look or Recommendations to fill this chart."
        )
    else:
        labels = [o[0] for o in occ["occasions"]]
        sizes = [o[1] for o in occ["occasions"]]
        colors = [PIE_COLORS[i % len(PIE_COLORS)] for i in range(len(labels))]
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor(BG)
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.0f%%",
            textprops={"color": TEXT},
            wedgeprops={"edgecolor": BG},
        )
        # Percentage labels sit ON the slices, so make them dark for contrast
        for t in autotexts:
            t.set_color(PALETTE["background"])
            t.set_fontweight("bold")
        st.pyplot(fig)
        plt.close(fig)

if stats["last_updated"]:
    st.caption(f"Last activity: {stats['last_updated']}")
