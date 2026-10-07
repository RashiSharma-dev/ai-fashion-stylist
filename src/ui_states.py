import streamlit as st


def empty_state(icon, title, hint=""):
    """
    Show a friendly, styled placeholder where content would normally appear.

    icon:  an emoji, like "📸"
    title: the main message, like "Upload your photo to begin analysis ↑"
    hint:  optional smaller line underneath with extra help
    """
    hint_html = ""
    if hint:
        hint_html = f'<div style="font-size:0.9rem; opacity:0.85; margin-top:6px;">{hint}</div>'

    st.markdown(f"""
    <div style="border:2px dashed var(--color-primary); border-radius:14px; padding:22px 16px; text-align:center; background-color:var(--color-secondary); margin:8px 0 16px 0;">
        <div style="font-size:2rem;">{icon}</div>
        <div style="font-family:var(--font-heading); font-size:1.15rem;">{title}</div>
        {hint_html}
    </div>
    """, unsafe_allow_html=True)
