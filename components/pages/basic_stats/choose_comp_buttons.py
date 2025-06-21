import streamlit as st

from config import COMPETITION_AND_COLORS, ALL_BUTTON_CONFIG


def choose_comp_buttons():
    competitions = list(COMPETITION_AND_COLORS.keys())

    id_comp = None

    with st.container():
        col_all, col_comps = st.columns([1, 8], gap="large")

        if "clicked" not in st.session_state:
            st.session_state.clicked = False

        with col_all:
            key = f"{ALL_BUTTON_CONFIG["id"]}_comps"
            if st.button(ALL_BUTTON_CONFIG["label"], key=key):
                id_comp = ALL_BUTTON_CONFIG["id"]

        with col_comps:
            cols = st.columns(len(competitions))

            for i, comp in enumerate(competitions):
                comp_config = COMPETITION_AND_COLORS[comp]

                with cols[i]:
                    key = f"btn_{comp}"
                    if st.button(comp_config["diminutive"], key=key, use_container_width=True):
                        st.session_state.clicked = comp_config["label"]
                        id_comp = comp

        # if st.session_state.clicked:
        #     st.write(st.session_state.clicked)

    return id_comp