import streamlit as st
from components.connection import ensure_connection, get_connection
from components.sidebar import sidebar_connection
from components.queries.home.query_interface import query_interface
from components.charts import visualization_interface
from config import PAGES_CONFIG, HOME_PAGE
from utils.page_helper.page_config import set_page_config


def main():
    """Fonction principale de l'application"""
    set_page_config(HOME_PAGE)

    # Titre centré
    st.markdown('<h1 class="main-title">SoccerStat-II</h1>', unsafe_allow_html=True)

    # Section Navigation avec boutons horizontaux
    st.markdown('<h3 class="nav-title">Navigation</h3>', unsafe_allow_html=True)

    with st.container():
        cols = st.columns(len(PAGES_CONFIG))
        for i, page in enumerate(PAGES_CONFIG):
            with cols[i]:
                if st.button(page, key=f"nav_{page}"):
                    st.switch_page(f"pages/{page}.py")


    st.divider()

    sidebar_connection()

    if ensure_connection():
        st.success("✅ Database connected and ready to use!")
        main_content()
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


def main_content():
    """Corps principal de l'application après connexion"""

    conn = get_connection()
    if conn:
        tab1, tab2 = st.tabs(["🔍 Requêtes", "📊 Graphiques"])
        with tab1:
            query_interface(conn)
        with tab2:
            visualization_interface()

    st.divider()
    st.markdown("---")
    st.markdown("*Application créée avec Streamlit 🎈*", unsafe_allow_html=True)


if __name__ == "__main__":
    main()