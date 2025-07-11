import streamlit as st

from utils.commons.BasePage import BasePage

from components.commons.get_seasons import get_all_seasons
from components.connection import get_connection
from components.pages.monitoring.plot.upper import plot_upper
from components.pages.monitoring.plot.by_season import plot_by_season
from components.pages.monitoring.table.upper import get_upper_tables
from components.pages.monitoring.table.by_season import get_by_season_tables

from config import MONITORING_PAGE


class MonitoringPage(BasePage):
    def content(self):
        db_conn = get_connection()

        inserted_at = "inserted_at"
        updated_at = "updated_at"

        plot_upper(db_conn, inserted_at)
        plot_upper(db_conn, updated_at)

        st.divider()

        all_seasons = get_all_seasons(db_conn)
        chosen_season = st.selectbox("Choose a season:", all_seasons)
        plot_by_season(db_conn, chosen_season, inserted_at)
        plot_by_season(db_conn, chosen_season, updated_at)

        st.divider()

        st.write(inserted_at)
        upper, by_season = st.columns(2, gap="medium")

        with upper:
            get_upper_tables(db_conn, inserted_at)
        with by_season:
            get_by_season_tables(db_conn, chosen_season, inserted_at)

        st.write(updated_at)
        upper, by_season = st.columns(2, gap="medium")

        with upper:
            get_upper_tables(db_conn, updated_at)
        with by_season:
            get_by_season_tables(db_conn, chosen_season, updated_at)




if __name__ == "__main__" or True:
    page = MonitoringPage(MONITORING_PAGE)
    page.render()