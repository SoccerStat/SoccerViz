import streamlit as st

from config import PAGES_CONFIG

def set_navigation_buttons():
    with st.container():
        cols = st.columns(len(PAGES_CONFIG))
        for i, page in enumerate(PAGES_CONFIG):
            with cols[i]:
                if st.button(page, key=f"nav_{page}"):
                    st.switch_page(f"pages/{page}.py")