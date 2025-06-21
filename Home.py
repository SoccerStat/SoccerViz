import streamlit as st

from components.charts import visualization_interface
from components.connection import ensure_connection, get_connection
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

    if ensure_connection():
        st.success("✅ Database connected and ready to use!")
        home_content()
    else:
        st.warning("⚠️ Please connect to the database via the sidebar.")

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

    conn = get_connection()
    if conn:
        tab1, tab2 = st.tabs(["🔍 Requêtes", "📊 Graphiques"])
        with tab1:
            query_interface(conn)
        with tab2:
            visualization_interface()


if __name__ == "__main__":
    main()