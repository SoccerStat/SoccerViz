import streamlit as st

from components.connection import get_connection
from components.pages.basic_stats.choose_comp_buttons import choose_comp_buttons
from components.pages.basic_stats.choose_season_button import choose_season_button
from components.pages.basic_stats.set_all_seasons_basic_stats import set_all_seasons_basic_stats
from components.pages.basic_stats.by_season_by_comp.set_basic_stats import set_basic_stats_by_season_by_comp
from config import PLAYER_X_TEAM_STATS

from utils.commons.BasePage import BasePage


class PlayerTeamStats(BasePage):
    def content(self):
        pass

if __name__ == "__main__" or True:
    page = PlayerTeamStats(PLAYER_X_TEAM_STATS)
    page.render()