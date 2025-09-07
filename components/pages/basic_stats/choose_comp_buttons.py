import streamlit as st

from components.commons.set_button_style import set_button_with_style
from config import COMPETITIONS, ALL_BUTTON_CONFIG


def choose_comp_buttons():
    competitions = list(COMPETITIONS.keys())

    key_all_comps = f"{ALL_BUTTON_CONFIG["id"]}_comps"

    st.session_state.setdefault("basic_stats__id_comp_selected", key_all_comps)

    st.session_state.setdefault("basic_stats__name_comp_selected", None)

    col_all, col_comps = st.columns([1, 8], gap="large")

    st.session_state.setdefault("basic_stats__comp_clicked", False)

    with col_all:
        all_comps = ALL_BUTTON_CONFIG["label_comps"]
        with set_button_with_style(key_all_comps, width='140%'):
            if st.button(all_comps, key=key_all_comps, use_container_width=True):
                id_comp = ALL_BUTTON_CONFIG["id"]
                st.session_state.basic_stats__comp_clicked = id_comp
                st.session_state.basic_stats__id_comp_selected = key_all_comps
                st.session_state.basic_stats__name_comp_selected = all_comps

    with col_comps:
        cols = st.columns(len(competitions))

        for i, comp in enumerate(competitions):
            comp_config = COMPETITIONS[comp]

            with cols[i]:
                key = f"btn_{comp}"
                bg_color = comp_config["style"]["bg_color"]
                font_color = comp_config["style"]["font_color"]
                border_color = comp_config["style"]["border_color"]

                with set_button_with_style(key, bg_color, font_color, border_color):
                    if st.button(comp_config["diminutive"], key=key, use_container_width=True):
                        st.session_state.basic_stats__id_comp_selected = comp
                        st.session_state.basic_stats__name_comp_selected = comp_config["label"]

    return st.session_state.basic_stats__id_comp_selected, st.session_state.basic_stats__name_comp_selected
