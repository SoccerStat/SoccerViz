import streamlit as st

from pathlib import Path
from config import FALLBACK_CSS


def load_css(file_name):
    """Charge le CSS depuis un fichier externe"""
    try:
        css_file_path = Path(__file__).parent / "assets" / "styles" / file_name
        with open(css_file_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # CSS de fallback
        st.markdown(FALLBACK_CSS, unsafe_allow_html=True)