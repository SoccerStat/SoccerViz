import pandas as pd
import streamlit as st

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.commons.set_titles import set_sub_sub_title
from components.commons.streamlit_widgets import select__get_one_comp, select__get_one_season, radio__select_side
from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_top_teams(_db_conn, chosen_comp, chosen_season):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/given_competition/top_bottom/get_top_teams.sql",
        name_comp=chosen_comp,
        season=chosen_season
    )

    return execute_query(_db_conn, sql_file)["Club"].tolist()


@st.cache_data(show_spinner=False)
def get_bottom_teams(_db_conn, chosen_comp, chosen_season):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/given_competition/top_bottom/get_bottom_teams.sql",
        name_comp=chosen_comp,
        season=chosen_season
    )

    return execute_query(_db_conn, sql_file)["Club"].tolist()


@st.cache_data(show_spinner=False)
def get_teams_performance_against_teams(_db_conn, chosen_comp, chosen_season, opponents, side):
    df = pd.DataFrame()

    teams = get_teams_by_comp_by_season(_db_conn, chosen_comp, [chosen_season])

    for team in teams:
        sql_file = read_sql_file(
            file_name="components/queries/team_stats/given_competition/top_bottom/get_ranking_against_teams.sql",
            name_comp=chosen_comp,
            season=chosen_season,
            name_team=team,
            opponents=opponents,
            side=side.lower()
        )
        df_team = execute_query(_db_conn, sql_file)
        df = pd.concat([df, df_team], ignore_index=True)

    return df


def get_team_performance_against_top_and_bottom(db_conn):
    prefix = "teams_performance_top_bottom_teams"

    chosen_comp = select__get_one_comp(prefix=prefix)

    if chosen_comp:
        seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

        chosen_season = select__get_one_season(
            prefix=prefix,
            custom_options=seasons_by_comp
        )

        if chosen_season:

            side = radio__select_side(prefix=prefix)

            top_teams = get_top_teams(db_conn, chosen_comp, chosen_season)
            bottom_teams = get_bottom_teams(db_conn, chosen_comp, chosen_season)

            set_sub_sub_title("Against Top 6 Teams")
            df_against_top_teams = get_teams_performance_against_teams(
                db_conn,
                chosen_comp,
                chosen_season,
                top_teams,
                side
            )
            st.dataframe(df_against_top_teams)

            set_sub_sub_title("Against Bottom 3 Teams")
            df_against_bottom_teams = get_teams_performance_against_teams(
                db_conn,
                chosen_comp,
                chosen_season,
                bottom_teams,
                side
            )
            st.dataframe(df_against_bottom_teams)
