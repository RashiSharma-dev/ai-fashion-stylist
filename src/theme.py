import streamlit as st

# The ONE place where our 5-color palette is defined.
# Python code (like matplotlib charts) can import this too.
PALETTE = {
    "primary": "#D96C8C",
    "secondary": "#1C1F26",
    "accent": "#FFD1DC",
    "background": "#0E1117",
    "text": "#FFB6C1",
}

HEADING_FONT = "Playfair Display"
BODY_FONT = "Inter"


def apply_theme():
    """Inject our fonts + CSS variables. Call once near the top of every page."""
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@600;700&display=swap');

    :root {{
        --color-primary: {PALETTE['primary']};
        --color-secondary: {PALETTE['secondary']};
        --color-accent: {PALETTE['accent']};
        --color-background: {PALETTE['background']};
        --color-text: {PALETTE['text']};
        --font-heading: '{HEADING_FONT}', Georgia, serif;
        --font-body: '{BODY_FONT}', 'Segoe UI', sans-serif;
    }}

    /* Body text: font and text color */
    .stApp,
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown li,
    label,
    input,
    textarea,
    [data-testid="stCaptionContainer"],
    [data-testid="stMetricLabel"] {{
        font-family: var(--font-body);
        color: var(--color-text);
    }}

    /* Buttons: font only (their text color is handled below) */
    button {{
        font-family: var(--font-body);
    }}

    /* Primary (pink) buttons: dark text so it stays readable */
    button[kind="primary"],
    button[data-testid="stBaseButton-primary"],
    button[kind="primary"] p,
    button[data-testid="stBaseButton-primary"] p {{
        color: var(--color-background);
    }}

    /* Headings: the second font */
    h1, h2, h3, h4,
    [data-testid="stHeading"],
    [data-testid="stMetricValue"] {{
        font-family: var(--font-heading);
        color: var(--color-text);
        letter-spacing: 0.3px;
    }}

    /* Keep Streamlit's built-in icons working (arrows, etc.) */
    [data-testid="stIconMaterial"] {{
        font-family: "Material Symbols Rounded" !important;
    }}

    /* Soft pink hover on buttons */
    .stButton > button:hover {{
        border-color: var(--color-primary);
        color: var(--color-accent);
    }}

    /* Divider lines in the primary color */
    hr {{
        border-color: var(--color-primary);
        opacity: 0.4;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
