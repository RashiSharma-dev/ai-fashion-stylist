import streamlit as st
import matplotlib.pyplot as plt

from src.analytics import load_analytics, get_top_colors, get_occasion_breakdown

st.set_page_config(page_title="Your Dashboard", page_icon="📊", layout="wide")

# Our theme colors, reused inside the charts so they match the app
BG = "#1C1F26"
PINK = "#D96C8C"
TEXT = "#FFB6C1"
PIE_COLORS = ["#D96C8C", "#FFB6C1", "#B8547A", "#F2A0B5", "#8E3B5C", "#FFD1DC"]


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

# --- Row 1: three big numbers ---
col1, col2, col3 = st.columns(3)
col1.metric("📸 Photos analyzed", stats["photos_analyzed"])
col2.metric("👗 Outfits viewed", stats["outfits_viewed"])
col3.metric("💬 Chatbot messages sent", stats["chat_messages_sent"])

st.divider()

# --- Row 2: two charts side by side ---
left, right = st.columns(2)

with left:
    st.subheader("Your Most Recommended Colors")
    top = get_top_colors(5)
    if not top["colors"]:
        st.info("No color history yet. Run 'Analyze My Look' to get started!")
    else:
        names = [c[0] for c in top["colors"]]
        counts = [c[1] for c in top["colors"]]
        fig, ax = plt.subplots(figsize=(6, 4))
        style_axes(fig, ax)
        ax.barh(names, counts, color=PINK)
        ax.invert_yaxis()  # biggest bar on top
        ax.set_xlabel("Times recommended", color=TEXT)
        st.pyplot(fig)
        plt.close(fig)

with right:
    st.subheader("Occasions You've Styled For")
    occ = get_occasion_breakdown()
    if not occ["occasions"]:
        st.info("No occasion history yet. Pick an occasion to see this chart!")
    else:
        labels = [o[0] for o in occ["occasions"]]
        sizes = [o[1] for o in occ["occasions"]]
        colors = [PIE_COLORS[i % len(PIE_COLORS)] for i in range(len(labels))]
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor(BG)
        ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.0f%%",
            textprops={"color": TEXT},
            wedgeprops={"edgecolor": BG},
        )
        st.pyplot(fig)
        plt.close(fig)

if stats["last_updated"]:
    st.caption(f"Last activity: {stats['last_updated']}")
