import streamlit as st

from components.charts import visualization_interface
from components.commons.ensure_connection_or_warning import set_connection_or_warning
from components.connection import get_connection
from components.pages.home.navigation_buttons import set_navigation_buttons
from components.queries.home.query_interface import query_interface
from components.sidebar import sidebar_connection
from config import HOME_PAGE
from utils.commons.BasePage import BasePage


class Home(BasePage):
    def render(self):
        self.set_page_config(home=True)
        self.set_page_title()
        sidebar_connection()
        set_connection_or_warning(self.content)

    def content(self):
        db_conn = get_connection()

        self.set_sub_title("Navigation")

        set_navigation_buttons()

        st.divider()

        if db_conn:
            tab1, tab2 = st.tabs(["🔍 Queries", "📊 Graphs"])
            with tab1:
                query_interface(db_conn)
            with tab2:
                visualization_interface()

def main():
    """Fonction principale de l'application"""

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


if __name__ == "__main__":
    home_page = Home(HOME_PAGE)
    home_page.render()