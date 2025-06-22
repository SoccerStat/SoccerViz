import streamlit as st

from components.charts import visualization_interface
from components.commons.ensure_connection_or_warning import set_connection_or_warning
from components.connection import get_connection
from components.pages.home.navigation_buttons import set_navigation_buttons
from components.queries.home.query_interface import query_interface
from components.sidebar import sidebar_connection
from config import HOME_PAGE
from utils.page_helper.page_config import set_page_config


def main():
    """Fonction principale de l'application"""
    set_page_config(HOME_PAGE)

    st.markdown('<h1 class="main-title">SoccerStat-II</h1>', unsafe_allow_html=True)

    st.markdown('<h3 class="nav-title">Navigation</h3>', unsafe_allow_html=True)

    set_navigation_buttons()

    st.divider()

    sidebar_connection()

    set_connection_or_warning(home_content)

    st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #1f77b4;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        }
        .nav-section {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .nav-title {
            text-align: center;
            color: #333;
            margin-bottom: 1rem;
        }
        .stButton > button {
            width: 100%;
            margin: 0.25rem;
        }
    </style>
    """, unsafe_allow_html=True)


def home_content():
    """Corps principal de l'application après connexion"""

    db_conn = get_connection()
    if db_conn:
        tab1, tab2 = st.tabs(["🔍 Requêtes", "📊 Graphiques"])
        with tab1:
            query_interface(db_conn)
        with tab2:
            visualization_interface()


if __name__ == "__main__":
    main()