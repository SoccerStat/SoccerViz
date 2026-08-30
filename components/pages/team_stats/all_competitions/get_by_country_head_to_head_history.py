import numpy as np
import pandas as pd
import streamlit as st
from streamlit_searchbox import st_searchbox

from components.commons.clubs import get_all_clubs
from components.commons.clubs import get_club_logo, get_all_club_countries
from components.commons.search_for_item import search_for_team, search_for_country
from components.commons.seasons import get_all_season_schemas
from components.commons.streamlit.titles import set_sub_sub_sub_title, set_sub_sub_title
from components.commons.streamlit.widgets import radio__select_side, download_button, check__group_by_competition, \
    check__group_by_season
from components.queries.execute_query import execute_query
from config import COMPETITIONS
from utils.file_helper.reader import read_sql_file


# @st.cache_data(show_spinner=False)
def get_history_stats(_db_conn, team, country, all_comps, all_season_schemas, side) -> pd.DataFrame:
    sql_file = read_sql_file(
        "components/queries/team_stats/all_competitions/by_country_head_to_head_history/get_head_to_head_history_stats.sql",
        team=team,
        country=country,
        comps=', '.join([f"'{comp}'" for comp in all_comps]),
        seasons=', '.join([f"'{season_schema[7:]}'" for season_schema in all_season_schemas]),
        side=side
    )

    return execute_query(_db_conn, sql_file)


# @st.cache_data(show_spinner=False)
def get_history_matches(_db_conn, team, country, all_comps, all_season_schemas, side) -> pd.DataFrame:
    sql_file = read_sql_file(
        "components/queries/team_stats/all_competitions/by_country_head_to_head_history/get_head_to_head_history_matches.sql",
        team=team,
        country=country,
        comps=', '.join([f"'{comp}'" for comp in all_comps]),
        seasons=', '.join([f"'{season_schema[7:]}'" for season_schema in all_season_schemas]),
        side=side
    )
    return execute_query(_db_conn, sql_file)


def get_by_country_head_to_head_history(db_conn):
    prefix = "by_country_head_to_head_history"
    all_comps = [comp["label"] for comp in COMPETITIONS.values()]
    all_season_schemas = get_all_season_schemas(db_conn)
    all_teams = list(get_all_clubs(db_conn))
    all_countries = list(get_all_club_countries(db_conn))

    search_function = search_for_team(all_teams)

    team = st_searchbox(
        search_function=search_function,
        key=f"{prefix}__teamA",
        placeholder="Choose Team A",
    )

    search_function = search_for_country(all_countries)

    country = st_searchbox(
        search_function=search_function,
        key=f"{prefix}__country",
        placeholder="Choose Country",
    )

    team_logo = get_club_logo(db_conn, team)

    if team and country:

        side = radio__select_side(
            prefix=prefix,
            custom_options=[f"{team} home", "Both", f"{team} away", "Neutral", "All"],
            default_index=4
        )

        st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center;">
            <img src="{team_logo['logo']}" width="150" style="margin-right: 10px;">
        </div>
        """, unsafe_allow_html=True)

        set_sub_sub_title("Basic Stats")

        granularity_competition = check__group_by_competition(prefix=prefix)
        granularity_season = check__group_by_season(prefix=prefix)

        df_stats = get_history_stats(db_conn, team, country, all_comps, all_season_schemas, side)

        set_sub_sub_sub_title("Overall")
        df_agg = df_stats[(df_stats["Opponent"] == "ALL")]
        if not granularity_competition:
            df_agg = df_agg[df_agg["Competition"] == "ALL"].drop("Competition", axis=1)
        else:
            df_agg = df_agg[df_agg["Competition"] != "ALL"]
        if not granularity_season:
            df_agg = df_agg[df_agg["Season"] == "ALL"].drop("Season", axis=1)
        else:
            df_agg = df_agg[df_agg["Season"] != "ALL"]
        st.dataframe(df_agg.drop("Opponent", axis=1), hide_index=True)

        set_sub_sub_sub_title("By opponent")
        df_by_opponent = df_stats[df_stats["Opponent"] != "ALL"]
        if not granularity_competition:
            df_by_opponent = df_by_opponent[df_by_opponent["Competition"] == "ALL"].drop("Competition", axis=1)
        else:
            df_by_opponent = df_by_opponent[df_by_opponent["Competition"] != "ALL"]
        if not granularity_season:
            df_by_opponent = df_by_opponent[df_by_opponent["Season"] == "ALL"].drop("Season", axis=1)
        else:
            df_by_opponent = df_by_opponent[df_by_opponent["Season"] != "ALL"]
        df_by_opponent = df_by_opponent.reset_index(drop=True)
        df_by_opponent.index = df_by_opponent.index + 1
        st.dataframe(df_by_opponent, hide_index=False)

        csv_stats = df_stats.to_csv(index=False, sep='|')
        download_button(
            prefix=f"{prefix}_stats",
            data=csv_stats,
            file_name=f"{prefix}_stats__{team}__{side.lower()}.csv",
            mime="text/csv"
        )

        set_sub_sub_title("Selected matches")

        df_matches = get_history_matches(db_conn, team, country, all_comps, all_season_schemas, side)
        df_matches.index = np.arange(1, len(df_matches) + 1)
        st.dataframe(df_matches)

        csv_matches = df_matches.to_csv(index=False, sep='|')
        download_button(
            prefix=f"{prefix}_matches",
            data=csv_matches,
            file_name=f"{prefix}_matches__{team}__{side.lower()}.csv",
            mime="text/csv"
        )
