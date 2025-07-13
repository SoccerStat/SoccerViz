import streamlit as st

from components.connection import get_connection
from components.pages.team_stats.get_global_ranking_one_season import get_global_ranking_one_season
from components.pages.team_stats.get_global_ranking_many_seasons import get_global_ranking_many_seasons
from components.pages.team_stats.get_global_ranking_by_season import get_global_ranking_by_season
from components.pages.team_stats.get_one_ranking import get_one_ranking
from config import TEAM_STATS_PAGE
from utils.commons.BasePage import BasePage


class TeamStatsPage(BasePage):
    def content(self):
        db_conn = get_connection()

        self.set_sub_title("Stat ranking by competition by season")
        get_one_ranking(db_conn)

        st.divider()

        self.set_sub_title("Global ranking over the season")
        get_global_ranking_one_season(db_conn)

        st.divider()
        
        self.set_sub_title("Global ranking over the seasons")
        get_global_ranking_many_seasons(db_conn)

        st.divider()

        self.set_sub_title("Global ranking by season")
        get_global_ranking_by_season(db_conn)

if __name__ == "__main__" or True:
    page = TeamStatsPage(TEAM_STATS_PAGE)
    page.render()