import streamlit as st

from components.pages.home.visualization_interface import set_visualization_interface
from components.pages.home.helpers import set_contents_table_buttons
from components.pages.home.query_interface import set_query_interface

from utils.database_helper.connection import get_connection
from utils.page_helper.BasePage import BasePage

from config import HOME_PAGE


class Home(BasePage):
    def content(self):
        db_conn = get_connection()

        self.set_sub_title("Table of contents")

        set_contents_table_buttons()

        st.divider()

        if db_conn:
            tab1, tab2 = st.tabs(["🔍 Queries", "📊 Graphs"])
            with tab1:
                set_query_interface(db_conn)
            with tab2:
                set_visualization_interface()


def main():
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
    home_page.render(home=True)
