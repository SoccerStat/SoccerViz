import streamlit as st

from components.connection import get_connection
from components.pages.basic_stats.choose_comp_buttons import choose_comp_buttons
from components.pages.basic_stats.choose_season_button import choose_season_button
from components.pages.basic_stats.set_all_seasons_basic_stats import set_all_seasons_basic_stats
from config import BASIC_STATS_PAGE

from utils.commons.BasePage import BasePage


class BasicStats(BasePage):
    def content(self):
        db_conn = get_connection()
        set_all_seasons_basic_stats(db_conn)

        st.divider()

        self.set_sub_title("Competitions")

        id_comp = choose_comp_buttons()
        st.write(id_comp)

        st.divider()

        self.set_sub_title("Seasons")

        seasons_ids = choose_season_button(db_conn, id_comp)
        st.write(seasons_ids)

        st.divider()

if __name__ == "__main__" or True:
    page = BasicStats(BASIC_STATS_PAGE)
    page.render()