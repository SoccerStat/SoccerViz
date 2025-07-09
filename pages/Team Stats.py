import streamlit as st

from components.connection import get_connection
from components.pages.team_stats.get_moving_ranking import get_moving_ranking
from components.pages.team_stats.get_one_ranking import get_one_ranking
from config import TEAM_STATS_PAGE
from utils.commons.BasePage import BasePage


class TeamStatsPage(BasePage):
    def content(self):
        db_conn = get_connection()

        with st.container():
            get_one_ranking(db_conn)

        st.divider()

        with st.container():
            get_moving_ranking(db_conn)

if __name__ == "__main__" or True:
    page = TeamStatsPage(TEAM_STATS_PAGE)
    page.render()