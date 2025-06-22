from utils.commons.BasePage import BasePage
from config import PLAYER_STATS_PAGE


class PlayerStatsPage(BasePage):
    def content(self):
        pass

if __name__ == "__main__" or True:
    page = PlayerStatsPage(PLAYER_STATS_PAGE)
    page.render()