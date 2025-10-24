from config import PLAYER_X_TEAM_STATS_PAGE

from utils.commons.BasePage import BasePage


class PlayerTeamStats(BasePage):
    def content(self):
        pass


if __name__ == "__main__" or True:
    page = PlayerTeamStats(PLAYER_X_TEAM_STATS_PAGE)
    page.render()
