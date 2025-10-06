import streamlit as st

from components.connection import get_connection
from components.pages.consistency_checks.set_match_consistency import set_match_consistency_section
from components.pages.consistency_checks.set_substitutions_checks import set_substitutions_checks_section
from components.pages.consistency_checks.set_teams_by_competition_section import set_teams_by_competition_section
from components.pages.consistency_checks.set_unknown_players_section import set_unknown_players_section

from utils.commons.BasePage import BasePage
from config import CONSISTENCY_PAGE


class ConsistencyPage(BasePage):
    def content(self):
        db_conn = get_connection()

        set_unknown_players_section(db_conn)

        st.divider()

        set_teams_by_competition_section(db_conn)

        st.divider()

        set_substitutions_checks_section(db_conn)

        st.divider()

        set_match_consistency_section(db_conn)


if __name__ == "__main__" or True:
    page = ConsistencyPage(CONSISTENCY_PAGE)
    page.render()
