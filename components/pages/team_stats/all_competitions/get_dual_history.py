import streamlit as st
from streamlit_searchbox import st_searchbox
import numpy as np

from components.commons.get_seasons import get_all_season_schemas
from components.commons.search_for_item import make_search_function
from components.commons.set_titles import set_sub_sub_sub_title
from components.commons.get_all_teams import get_all_clubs
from components.commons.streamlit_widgets import radio__select_side
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file
from config import COMPETITIONS


@st.cache_data(show_spinner=False)
def get_history(_db_conn, teamA, teamB, all_comps, all_season_schemas, side):
    sql_file = read_sql_file(
        "components/queries/team_stats/all_competitions/dual/get_dual_history_stats.sql",
        teamA=teamA,
        teamB=teamB,
        comps=', '.join([f"'{comp}'" for comp in all_comps]),
        seasons=', '.join([f"'{season_schema[7:]}'" for season_schema in all_season_schemas]),
        side=side
    )

    return execute_query(_db_conn, sql_file)


@st.cache_data(show_spinner=False)
def get_history_matches(_db_conn, teamA, teamB, all_comps, all_season_schemas, side):
    sql_file = read_sql_file(
        "components/queries/team_stats/all_competitions/dual/get_dual_history_matches.sql",
        teamA=teamA,
        teamB=teamB,
        comps=', '.join([f"'{comp}'" for comp in all_comps]),
        seasons=', '.join([f"'{season_schema[7:]}'" for season_schema in all_season_schemas]),
        side=side
    )
    return execute_query(_db_conn, sql_file)


def get_dual_history(db_conn):
    prefix = "dual_history"
    all_comps = [comp["label"] for comp in COMPETITIONS.values()]
    all_season_schemas = get_all_season_schemas(db_conn)
    all_teams = list(get_all_clubs(db_conn))

    search_function = make_search_function(all_teams)

    teamA = st_searchbox(
        search_function=search_function,
        key="dual_history__teamA",
        placeholder="Choose Team A",
    )

    search_function = make_search_function(all_teams, teamA)

    teamB = st_searchbox(
        search_function=search_function,
        key="dual_history__teamB",
        placeholder="Choose Team B",
    )

    if teamA and teamB and teamA != teamB:

        side = radio__select_side(
            prefix=prefix,
            custom_options=[f"{teamA} home", "Both", f"{teamB} home", "Neutral", "All"]
        )

        set_sub_sub_sub_title("Basic Stats")

        df = get_history(db_conn, teamA, teamB, all_comps, all_season_schemas, side)

        if side in ["Both", "Neutral", "All"]:
            df.rename(columns={
                "Wins_A": f"Wins {teamA}",
                "Wins_B": f"Wins {teamB}",
                "Goals_A": f"Goals {teamA}",
                "Goals_B": f"Goals {teamB}"
            }, inplace=True)

        st.dataframe(df, hide_index=True)

        set_sub_sub_sub_title("Selected matches")

        df_matches = get_history_matches(db_conn, teamA, teamB, all_comps, all_season_schemas, side)
        df_matches.index = np.arange(1, len(df_matches) + 1)
        st.dataframe(df_matches)
