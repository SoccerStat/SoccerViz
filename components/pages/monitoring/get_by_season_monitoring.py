import streamlit as st

from components.commons.set_titles import set_sub_sub_title
from components.pages.monitoring.plot.by_season import plot_by_season
from components.pages.monitoring.tables.by_season import get_by_season_tables
from components.commons.get_seasons import get_all_season_schemas


def get_by_season_monitoring(db_conn, col_inserted_at, col_updated_at):
    all_season_schemas = get_all_season_schemas(db_conn)
    chosen_season = st.selectbox("Choose a season:", [season[7:] for season in all_season_schemas])
    plot_by_season(db_conn, chosen_season, col_inserted_at)
    plot_by_season(db_conn, chosen_season, col_updated_at)

    set_sub_sub_title(col_inserted_at)
    by_season, _ = st.columns(2, gap="medium")

    with by_season:
        get_by_season_tables(db_conn, chosen_season, col_inserted_at)

    set_sub_sub_title(col_updated_at)
    by_season, _ = st.columns(2, gap="medium")

    with by_season:
        get_by_season_tables(db_conn, chosen_season, col_updated_at)
