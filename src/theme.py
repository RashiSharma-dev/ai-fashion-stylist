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
    """Inject our fonts, CSS variables, animations, and mobile rules. Call once near the top of every page."""
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

    /* ---------- Fonts and text colors ---------- */
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

    hr {{
        border-color: var(--color-primary);
        opacity: 0.4;
    }}

    /* Images and videos never grow wider than their container */
    img, video {{
        max-width: 100%;
        height: auto;
    }}

    /* Long words (like color codes) wrap instead of pushing the page sideways */
    .stMarkdown {{
        overflow-wrap: anywhere;
    }}

    /* ---------- Animation keyframes ---------- */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(16px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to   {{ opacity: 1; }}
    }}
    @keyframes shimmer {{
        0%   {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}

    /* ---------- 1. Cards fade in one by one ---------- */
    .fade-in-card {{
        opacity: 0;
        animation: fadeInUp 0.6s ease forwards;
    }}

    /* ---------- 2. Loading progress bar ---------- */
    .loading-label {{
        font-size: 0.9rem;
        margin-bottom: 6px;
    }}
    .loading-track {{
        background-color: var(--color-secondary);
        border: 1px solid var(--color-primary);
        border-radius: 10px;
        height: 14px;
        overflow: hidden;
        margin-bottom: 12px;
    }}
    .loading-fill {{
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, var(--color-primary), var(--color-accent), var(--color-primary));
        background-size: 200% 100%;
        animation: shimmer 1.2s linear infinite;
        transition: width 0.4s ease;
    }}

    /* ---------- 3. Button hover effects ---------- */
    .stButton > button,
    .stDownloadButton > button {{
        transition: transform 0.2s ease, box-shadow 0.2s ease,
                    background-color 0.25s ease, border-color 0.25s ease, color 0.25s ease;
    }}
    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        transform: translateY(-2px);
        border-color: var(--color-primary);
        color: var(--color-accent);
        box-shadow: 0 4px 16px color-mix(in srgb, var(--color-primary) 35%, transparent);
    }}
    .stButton > button:active,
    .stDownloadButton > button:active {{
        transform: translateY(0) scale(0.98);
    }}
    button[kind="primary"]:hover,
    button[data-testid="stBaseButton-primary"]:hover {{
        background-color: var(--color-accent);
        color: var(--color-background);
    }}

    /* ---------- 4. Smooth tab transitions ---------- */
    [data-baseweb="tab-panel"] {{
        animation: fadeIn 0.45s ease;
    }}
    button[data-baseweb="tab"] {{
        transition: color 0.25s ease, background-color 0.25s ease;
    }}

    /* ---------- Day 75: tablet screens ---------- */
    @media (max-width: 900px) {{
        .block-container {{
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }}
    }}

    /* ---------- Day 75: phone screens ---------- */
    @media (max-width: 640px) {{
        /* Less side padding so content uses the whole screen */
        .block-container {{
            padding: 1rem 0.9rem 5rem 0.9rem !important;
        }}

        /* Smaller headings so they don't take over a small screen */
        h1, [data-testid="stHeading"] h1 {{ font-size: 1.7rem !important; }}
        h2, [data-testid="stHeading"] h2 {{ font-size: 1.4rem !important; }}
        h3, [data-testid="stHeading"] h3 {{ font-size: 1.15rem !important; }}
        [data-testid="stMetricValue"] {{ font-size: 1.6rem !important; }}

        /* Thumb-friendly buttons: at least 48px tall, full width */
        .stButton > button,
        .stDownloadButton > button {{
            min-height: 48px;
            font-size: 1rem;
            width: 100%;
        }}

        /* Tabs get a bigger tap area */
        button[data-baseweb="tab"] {{
            min-height: 44px;
            padding-left: 12px;
            padding-right: 12px;
        }}

        /* Hover lift makes no sense on touch screens */
        .stButton > button:hover,
        .stDownloadButton > button:hover {{
            transform: none;
        }}

        /* Camera frame and Mirror Mode cards: tighter spacing */
        [data-testid="stCameraInput"] {{
            padding: 6px !important;
            border-radius: 20px !important;
        }}
        .mirror-card {{
            padding: 10px 12px !important;
            gap: 10px !important;
        }}
        .mirror-tone {{
            font-size: 1.3rem !important;
        }}

        /* Progress bar label */
        .loading-label {{
            font-size: 0.8rem;
        }}
    }}

    /* ---------- Respect "reduce motion" system settings ---------- */
    @media (prefers-reduced-motion: reduce) {{
        .fade-in-card {{ opacity: 1; animation: none; }}
        .loading-fill {{ animation: none; }}
        [data-baseweb="tab-panel"] {{ animation: none; }}
        .stButton > button:hover,
        .stDownloadButton > button:hover {{ transform: none; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def show_loading(placeholder, percent, label):
    """
    Draw (or update) our animated progress bar inside a st.empty() placeholder.
    Usage:
        loader = st.empty()
        show_loading(loader, 40, "Reading your skin tone...")
        ...
        loader.empty()   # remove the bar when finished
    """
    placeholder.markdown(
        f'<div class="loading-label">{label}</div>'
        f'<div class="loading-track"><div class="loading-fill" style="width:{percent}%;"></div></div>',
        unsafe_allow_html=True,
    )
