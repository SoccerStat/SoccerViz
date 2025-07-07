from components.connection import get_connection
from components.pages.team_stats.get_one_ranking import get_one_ranking
from config import TEAM_STATS_PAGE
from utils.commons.BasePage import BasePage


class TeamStatsPage(BasePage):
    def content(self):
        db_conn = get_connection()

        get_one_ranking(db_conn)

if __name__ == "__main__" or True:
    page = TeamStatsPage(TEAM_STATS_PAGE)
    page.render()