import streamlit as st

from config import ALL_BUTTON_CONFIG

def choose_season_button(id_comp):
    seasons_ids = None

    with st.container():
        col_all, col_range, col_compare = st.columns([1, 1, 1], gap="large")

        with col_all:
            key = f"{ALL_BUTTON_CONFIG["id"]}_seasons"
            if st.button(ALL_BUTTON_CONFIG["label"], key=key):
                seasons_ids = []

        with col_range:
            None

        with col_compare:
            None

    return seasons_ids