import streamlit as st

from components.connection import get_connection
from components.queries.basic_stats.comp_query import comp_query
from components.sidebar import sidebar_connection
from config import COMPETITION_AND_COLORS


def main():

    sidebar_connection()

    st.markdown('<h1 class="main-title">SoccerStat-II - Basic Stats</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="nav-title">Navigation</h3>', unsafe_allow_html=True)

    conn = get_connection()

    with st.container():
        if conn:
            comp_query(conn)

    def button_style(color, key):
        st.markdown(f"""
            <style>
            div[data-testid="stButton"][data-key="{key}"] button {{
                background-color: {color};
                color: white;
                border-radius: 8px;
                padding: 0.5em 1em;
                font-weight: bold;
                border: none;
            }}
            </style>
        """, unsafe_allow_html=True)

    competitions = list(COMPETITION_AND_COLORS.keys())

    with st.container():
        col_all_button, col_buttons = st.columns([1, 5], gap="large")

        # Colonne "All"
        with col_all_button:
            button_style(COMPETITION_AND_COLORS["All"], "All")
            if st.button("All", key="All"):
                st.write("All")

        # Ligne 1 : 5 boutons centrés
        with col_buttons:
            st.markdown("### ")
            row1 = st.columns(5)
            for i, comp in enumerate(competitions[1:6]):
                with row1[i]:
                    key = f"nav_{comp}"
                    button_style(COMPETITION_AND_COLORS[comp], key)
                    if st.button(comp, key=key):
                        st.write(comp)

            st.markdown("### ")
            spacer, col1, col2, col3, spacer2 = st.columns([1, 2, 2, 2, 1])
            for i, comp in enumerate(competitions[6:]):
                col = [col1, col2, col3][i]
                with col:
                    key = f"btn_{comp}"
                    button_style(COMPETITION_AND_COLORS[comp], key)
                    if st.button(comp, key=key):
                        st.write(comp)

    if st.button("← Return to Home"):
        st.switch_page("Home.py")

if __name__ == "__main__":
    main()