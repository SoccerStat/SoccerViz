import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from config import COMPETITION_AND_COLORS, ALL_BUTTON_CONFIG

def set_button_with_style(key, bg_color="white", font_color="black", border_color="black"):
    return stylable_container(
        key=key,
        css_styles=f"""
            .stButton > button {{
                background: {bg_color};
                color: {font_color};
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 0.4em 1em;
                font-weight: 600;
                font-size: 0.9rem;
                transition: all 0.2s ease-in-out;
                cursor: pointer;
                outline: none;
            }}
            .stButton > button:hover {{
                transform: scale(1.05);
                box-shadow: 0 4px 12px rgba(0,0,0,0);
            }}
            .stButton > button:focus,
            .stButton > button:active {{
                background: #FAFAFA !important;
                color: #212121 !important;
                border: 2px solid #607D8B !important;
                box-shadow: none !important;
                outline: none !important;
                transform: scale(0.96);
            }}
        """
    )


def choose_comp_buttons():
    competitions = list(COMPETITION_AND_COLORS.keys())

    id_comp = None

    col_all, col_comps = st.columns([1, 8], gap="large")

    if "clicked" not in st.session_state:
        st.session_state.clicked = False

    with col_all:
        key = f"{ALL_BUTTON_CONFIG["id"]}_comps"
        with set_button_with_style(key, ):
            if st.button(ALL_BUTTON_CONFIG["label"], key=key, use_container_width=True):
                id_comp = ALL_BUTTON_CONFIG["id"]
                st.session_state.clicked = id_comp

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
                        st.session_state.clicked = comp
                        id_comp = comp

    if st.session_state.clicked:
        st.write(st.session_state.clicked)

    return id_comp