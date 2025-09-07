import streamlit as st

from components.commons.set_titles import set_sub_sub_title
from components.pages.monitoring.plot.upper import plot_upper
from components.pages.monitoring.tables.upper import get_upper_tables


def get_upper_schema_monitoring(db_conn, col_inserted_at, col_updated_at):
    plot_upper(db_conn, col_inserted_at)
    plot_upper(db_conn, col_updated_at)

    set_sub_sub_title(col_inserted_at)
    upper, _ = st.columns(2, gap="medium")

    with upper:
        get_upper_tables(db_conn, col_inserted_at)

    set_sub_sub_title(col_updated_at)
    upper, _ = st.columns(2, gap="medium")

    with upper:
        get_upper_tables(db_conn, col_updated_at)
