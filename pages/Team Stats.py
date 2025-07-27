import streamlit as st

from components.connection import get_connection

from components.pages.team_stats.get_home_away_outcomes import get_home_away_outcomes
from components.pages.team_stats.get_combined_ranking_one_season import get_combined_ranking_one_season
from components.pages.team_stats.get_dual_history import get_dual_history
from components.pages.team_stats.get_global_ranking_one_season import get_global_ranking_one_season
from components.pages.team_stats.get_global_ranking_many_seasons import get_global_ranking_many_seasons
from components.pages.team_stats.get_global_ranking_by_season import get_global_ranking_by_season
from components.pages.team_stats.get_single_ranking_one_season import get_single_ranking_one_season
from components.pages.team_stats.get_stats_one_team import get_stats_one_team
from components.pages.team_stats.get_team_performance_against_top_and_bottom import get_team_performance_against_top_and_bottom

from config import TEAM_STATS_PAGE
from utils.commons.BasePage import BasePage


class TeamStatsPage(BasePage):
    def content(self):
        db_conn = get_connection()

        self.set_sub_title("By Competition by season")

        self.set_sub_sub_title("Basic Stats of one team")
        get_stats_one_team(db_conn)

        st.divider()

        self.set_sub_sub_title("Single Stat ranking")
        get_single_ranking_one_season(db_conn)

        st.divider()

        self.set_sub_sub_title("Combined Stat ranking")
        get_combined_ranking_one_season(db_conn)

        st.divider()

        self.set_sub_sub_title("Moving Ranking") # Moyennes mobiles

        st.divider()

        self.set_sub_sub_title("Global ranking over the season")
        get_global_ranking_one_season(db_conn)

        st.divider()
        
        self.set_sub_sub_title("Global ranking over the completed seasons")
        get_global_ranking_many_seasons(db_conn)

        st.divider()

        self.set_sub_sub_title("Global ranking over each season")
        get_global_ranking_by_season(db_conn)

        st.divider()

        self.set_sub_sub_title("Teams Performance against Top/Bottom teams")
        get_team_performance_against_top_and_bottom(db_conn)

        st.divider()

        self.set_sub_title("All competitions and seasons included")

        self.set_sub_sub_title("Dual history")
        get_dual_history(db_conn)

        st.divider()

        self.set_sub_sub_title("Home / Away Balance")
        get_home_away_outcomes(db_conn)

if __name__ == "__main__" or True:
    page = TeamStatsPage(TEAM_STATS_PAGE)
    page.render()