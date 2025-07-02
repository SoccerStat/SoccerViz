import streamlit as st

from components.connection import get_connection
from components.pages.basic_stats.choose_comp_buttons import choose_comp_buttons
from components.pages.basic_stats.choose_season_button import choose_season_button
from components.pages.basic_stats.set_all_seasons_basic_stats import set_all_seasons_basic_stats
from components.pages.basic_stats.by_season_by_comp.set_basic_stats import set_basic_stats_by_season_by_comp
from config import BASIC_STATS_PAGE

from utils.commons.BasePage import BasePage


class BasicStats(BasePage):
    def content(self):
        db_conn = get_connection()
        set_all_seasons_basic_stats(db_conn)

        st.divider()

        self.set_sub_title("Competitions")

        id_comp, name_comp = choose_comp_buttons()

        st.divider()

        self.set_sub_title("Seasons")

        seasons_mode, seasons_ids = choose_season_button(db_conn, name_comp)

        st.divider()

        if seasons_ids:
            set_basic_stats_by_season_by_comp(db_conn, name_comp, seasons_mode, seasons_ids)

if __name__ == "__main__" or True:
    page = BasicStats(BASIC_STATS_PAGE)
    page.render()