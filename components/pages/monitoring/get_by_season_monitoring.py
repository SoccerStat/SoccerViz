import streamlit as st

from components.commons.set_titles import set_sub_sub_title
from components.pages.monitoring.plot.by_season import plot_by_season
from components.pages.monitoring.table.by_season import get_by_season_tables
from components.commons.get_seasons import get_all_seasons


def get_by_season_monitoring(db_conn, col_inserted_at, col_updated_at):
    all_seasons = get_all_seasons(db_conn)
    chosen_season = st.selectbox("Choose a season:", [season[7:] for season in all_seasons])
    plot_by_season(db_conn, chosen_season, col_inserted_at)
    plot_by_season(db_conn, chosen_season, col_updated_at)

    set_sub_sub_title(f"{col_inserted_at} 7 previous days")
    by_season, _ = st.columns(2, gap="medium")

    with by_season:
        get_by_season_tables(db_conn, chosen_season, col_inserted_at)

    set_sub_sub_title(f"{col_updated_at} 7 previous days")
    by_season, _ = st.columns(2, gap="medium")

    with by_season:
        get_by_season_tables(db_conn, chosen_season, col_updated_at)