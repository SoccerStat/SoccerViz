import streamlit as st

from components.commons.set_button_style import set_button_with_style
from config import PAGES_CONFIG


def set_navigation_buttons():
    with st.container():
        cols = st.columns(len(PAGES_CONFIG))
        for i, page in enumerate(sorted(PAGES_CONFIG)):
            with cols[i]:
                key = f"nav_{page}"
                with set_button_with_style(key):
                    if st.button(page, key=key):
                        st.switch_page(f"pages/{page}.py")
