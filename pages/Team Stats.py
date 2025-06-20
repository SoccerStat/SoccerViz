from utils.commons.common_page_config import BasePage
from config import TEAM_STATS_PAGE


class TeamStatsPage(BasePage):
    def render(self):
        self.set_page_config()
        self.set_page_title()
        self.set_back_home_button()

if __name__ == "__main__" or True:
    page = TeamStatsPage(TEAM_STATS_PAGE)
    page.render()