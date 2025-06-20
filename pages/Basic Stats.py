import streamlit as st

from components.connection import get_connection
from components.pages.choose_comp_buttons import choose_comp_buttons
from components.pages.choose_season_button import choose_season_button
from components.pages.set_all_seasons_basic_stats import set_all_seasons_basic_stats
from components.sidebar import sidebar_connection
from config import COMPETITION_AND_COLORS, BASIC_STATS_PAGE, BASIC_STATS_PAGE

from utils.commons.common_page_config import BasePage


class BasicStats(BasePage):
    def render(self):
        self.set_page_config()
        self.set_page_title()

        sidebar_connection()
        conn = get_connection()

        set_all_seasons_basic_stats(conn)

        st.divider()

        id_comp = choose_comp_buttons()
        print("coucou", id_comp)

        st.divider()

        seasons_ids = choose_season_button(id_comp)

        st.divider()

        self.set_back_home_button()

if __name__ == "__main__" or True:
    page = BasicStats(BASIC_STATS_PAGE)
    page.render()