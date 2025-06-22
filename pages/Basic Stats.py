import streamlit as st

from components.commons.ensure_connection_or_warning import set_connection_or_warning
from components.connection import get_connection
from components.pages.basic_stats.choose_comp_buttons import choose_comp_buttons
from components.pages.basic_stats.choose_season_button import choose_season_button
from components.pages.basic_stats.set_all_seasons_basic_stats import set_all_seasons_basic_stats
from components.sidebar import sidebar_connection
from config import BASIC_STATS_PAGE

from utils.commons.common_page_config import BasePage


class BasicStats(BasePage):
    def render(self):
        self.set_page_config()
        self.set_page_title()

        sidebar_connection()

        set_connection_or_warning(self.content)



    def content(self):
        db_conn = get_connection()
        set_all_seasons_basic_stats(db_conn)

        st.divider()

        id_comp = choose_comp_buttons()
        st.write(id_comp)

        st.divider()

        seasons_ids = choose_season_button(db_conn, id_comp)
        st.write(seasons_ids)

        st.divider()

        self.set_back_home_button()

if __name__ == "__main__" or True:
    page = BasicStats(BASIC_STATS_PAGE)
    page.render()