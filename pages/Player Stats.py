from components.connection import get_connection
from components.pages.player_stats.get_birthday_boys import get_birthday_boys
from components.pages.player_stats.get_player_info import get_player_info
from components.pages.player_stats.get_top_players import get_top_players
from utils.commons.BasePage import BasePage
from config import PLAYER_STATS_PAGE


class PlayerStatsPage(BasePage):
    def content(self):
        db_conn = get_connection()

        with self.set_expander("Birthday boys"):
            self.set_sub_title("Birthday boys")
            get_birthday_boys(db_conn)

        with self.set_expander("Top players"):
            self.set_sub_title("Top players")
            get_top_players(db_conn)

        with self.set_expander("Player info"):
            self.set_sub_title("Player info")
            get_player_info(db_conn)


if __name__ == "__main__" or True:
    page = PlayerStatsPage(PLAYER_STATS_PAGE)
    page.render()
