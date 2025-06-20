import streamlit as st

from config import APP_CONFIG

def set_page_config(page_title):
    st.set_page_config(
        page_title=page_title,
        page_icon=APP_CONFIG['icon'],
        layout=APP_CONFIG['layout']
    )