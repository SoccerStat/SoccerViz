import streamlit as st

from components.pages.monitoring.get_upper_schema_monitoring import get_upper_schema_monitoring
from components.pages.monitoring.get_by_season_monitoring import get_by_season_monitoring
from components.connection import get_connection

from utils.commons.BasePage import BasePage
from config import MONITORING_PAGE


class MonitoringPage(BasePage):
    def content(self):
        db_conn = get_connection()

        inserted_at = "inserted_at"
        updated_at = "updated_at"

        self.set_sub_title("Upper Schema Monitoring")
        get_upper_schema_monitoring(db_conn, inserted_at, updated_at)

        st.divider()

        self.set_sub_title("By Season Monitoring")
        get_by_season_monitoring(db_conn, inserted_at, updated_at)


if __name__ == "__main__" or True:
    page = MonitoringPage(MONITORING_PAGE)
    page.render()
