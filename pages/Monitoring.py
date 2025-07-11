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

        self.set_sub_title("Upper Schema Monitoring")
        plot_upper(db_conn, inserted_at)
        plot_upper(db_conn, updated_at)

        self.set_sub_sub_title(f"{inserted_at} 7 previous days")
        upper, _ = st.columns(2, gap="medium")

        with upper:
            get_upper_tables(db_conn, inserted_at)

        self.set_sub_sub_title(f"{updated_at} 7 previous days")
        upper, _ = st.columns(2, gap="medium")

        with upper:
            get_upper_tables(db_conn, updated_at)

        st.divider()

        self.set_sub_title("Upper Schema Monitoring")
        all_seasons = get_all_seasons(db_conn)
        chosen_season = st.selectbox("Choose a season:", [season[7:] for season in all_seasons])
        plot_by_season(db_conn, chosen_season, inserted_at)
        plot_by_season(db_conn, chosen_season, updated_at)

        self.set_sub_sub_title(f"{inserted_at} 7 previous days")
        by_season, _ = st.columns(2, gap="medium")

        with by_season:
            get_by_season_tables(db_conn, chosen_season, inserted_at)

        self.set_sub_sub_title(f"{updated_at} 7 previous days")
        by_season, _ = st.columns(2, gap="medium")

        with by_season:
            get_by_season_tables(db_conn, chosen_season, updated_at)


if __name__ == "__main__" or True:
    page = MonitoringPage(MONITORING_PAGE)
    page.render()