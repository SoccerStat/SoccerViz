from components.connection import get_connection
from components.pages.coaches_stats.get_coaches_stats import get_all_coaches_stats

from utils.commons.BasePage import BasePage
from config import COACHES_STATS_PAGE


class PlayerTeamStats(BasePage):
    def content(self):
        db_conn = get_connection()

        with self.set_expander("Coaches Stats"):
            self.set_sub_title("Main Stats")
            get_all_coaches_stats(db_conn)

            self.set_sub_title("One Stat")
            # get_one_coaches_stat(db_conn)


if __name__ == "__main__" or True:
    page = PlayerTeamStats(COACHES_STATS_PAGE)
    page.render()
