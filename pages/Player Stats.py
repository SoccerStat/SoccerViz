from components.connection import get_connection
from components.pages.player_stats.get_birthday_boys import get_birthday_boys
from utils.commons.BasePage import BasePage
from config import PLAYER_STATS_PAGE


class PlayerStatsPage(BasePage):
    def content(self):
        db_conn = get_connection()

        self.set_sub_title("Birthday boys")
        get_birthday_boys(db_conn)

if __name__ == "__main__" or True:
    page = PlayerStatsPage(PLAYER_STATS_PAGE)
    page.render()