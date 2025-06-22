from utils.commons.BasePage import BasePage
from config import TEAM_STATS_PAGE


class TeamStatsPage(BasePage):
    def content(self):
        pass

if __name__ == "__main__" or True:
    page = TeamStatsPage(TEAM_STATS_PAGE)
    page.render()