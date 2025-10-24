import pandas as pd
import streamlit as st

from components.commons.get_seasons import get_all_season_schemas
from components.commons.set_titles import set_sub_sub_sub_title

from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_promoted_teams_by_season(_db_conn, current_season, previous_season):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/given_competition/history/get_promoted_teams.sql",
        current_season=current_season,
        previous_season=previous_season
    )

    return execute_query(_db_conn, sql_file)


def get_promoted_teams(db_conn):
    all_seasons = [season[7:] for season in get_all_season_schemas(db_conn)]

    chosen_season = st.selectbox(
        key="promoted_teams__season",
        label="Choose season...",
        options=[""] + all_seasons[:-1]
    )

    if chosen_season:
        previous_season_schema = all_seasons[all_seasons.index(chosen_season)+1]

        set_sub_sub_sub_title(f"Promoted teams in {chosen_season.replace('_', '-')}")

        df_promoted_teams = get_promoted_teams_by_season(db_conn, chosen_season, previous_season_schema)

        clubs_by_competition = df_promoted_teams.groupby('Competition')['Club'].apply(list)

        for competition, clubs in clubs_by_competition.items():
            st.write(f"**{competition}**")
            st.dataframe(pd.DataFrame({'Club': clubs}), hide_index=True)
