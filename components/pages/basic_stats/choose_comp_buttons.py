import streamlit as st

from components.commons.set_button_style import set_button_with_style
from config import COMPETITION_AND_COLORS, ALL_BUTTON_CONFIG

def choose_comp_buttons():
    competitions = list(COMPETITION_AND_COLORS.keys())

    key_all_comps = f"{ALL_BUTTON_CONFIG["id"]}_comps"

    if "selected_comp" not in st.session_state:
        st.session_state.selected_comp = key_all_comps

    col_all, col_comps = st.columns([1, 8], gap="large")

    if "clicked" not in st.session_state:
        st.session_state.clicked = False

    with col_all:
        with set_button_with_style(key_all_comps, width='155%'):
            if st.button(ALL_BUTTON_CONFIG["label_comps"], key=key_all_comps, use_container_width=True):
                id_comp = ALL_BUTTON_CONFIG["id"]
                st.session_state.clicked = id_comp
                st.session_state.selected_comp = key_all_comps

    with col_comps:
        cols = st.columns(len(competitions))

        for i, comp in enumerate(competitions):
            comp_config = COMPETITION_AND_COLORS[comp]

            with cols[i]:
                key = f"btn_{comp}"
                bg_color = comp_config["style"]["border_color"]
                font_color = comp_config["style"]["font_color"]
                border_color = comp_config["style"]["bg_color"]

                with set_button_with_style(key, bg_color, font_color, border_color):
                    if st.button(comp_config["diminutive"], key=key, use_container_width=True):
                        st.session_state.selected_comp = comp

    return st.session_state.selected_comp