import streamlit as st

from config import COMPETITION_AND_COLORS, ALL_BUTTON_CONFIG


def choose_comp_buttons():
    competitions = list(COMPETITION_AND_COLORS.keys())

    id_comp = None

    with st.container():
        col_all, col_comps = st.columns([1, 5], gap="large")

        with col_all:
            key = f"{ALL_BUTTON_CONFIG["id"]}_comps"
            if st.button(ALL_BUTTON_CONFIG["label"], key=key):
                id_comp = ALL_BUTTON_CONFIG["id"]

        with col_comps:
            row1 = st.columns(5)
            for i, comp in enumerate(competitions[0:5]):
                comp_config = COMPETITION_AND_COLORS[comp]
                with row1[i]:
                    key = f"btn_{comp}"
                    if st.button(comp_config['label'], key=key):
                        id_comp = comp

            spacer, col1, col2, col3, spacer2 = st.columns([1, 2, 2, 2, 1])
            for i, comp in enumerate(competitions[5:]):
                comp_config = COMPETITION_AND_COLORS[comp]
                col = [col1, col2, col3][i]
                with col:
                    key = f"btn_{comp}"
                    if st.button(comp_config['label'], key=key):
                        id_comp = comp

    return id_comp