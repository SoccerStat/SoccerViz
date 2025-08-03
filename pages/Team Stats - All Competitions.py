import streamlit as st

from components.connection import get_connection
from components.pages.team_stats.get_dual_history import get_dual_history
from components.pages.team_stats.get_home_away_outcomes import get_home_away_outcomes_plotly
from config import TEAM_STATS_PAGES
from utils.commons.BasePage import BasePage


class TeamStatsPage(BasePage):
    def content(self):
        db_conn = get_connection()

        self.set_sub_title("All competitions and seasons")

        self.set_sub_sub_title("Dual history")
        get_dual_history(db_conn)

        st.divider()

        self.set_sub_sub_title("Home / Away Balance")
        get_home_away_outcomes_plotly(db_conn)

if __name__ == "__main__" or True:
    page = TeamStatsPage(TEAM_STATS_PAGES)
    page.render()