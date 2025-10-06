import streamlit as st

from components.commons.get_seasons import get_all_season_schemas
from components.commons.set_titles import set_sub_title, set_sub_sub_title
from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_unknown_players(_db_conn):
    sql_file = read_sql_file(file_name="components/queries/consistency_checks/unknown_players/unknown_players.sql")
    return execute_query(_db_conn, sql_file)


@st.cache_data(show_spinner=False)
def get_players_in_match_but_not_in_team(_db_conn):
    all_season_schemas = get_all_season_schemas(_db_conn)
    union_query = " UNION ALL ".join(
        [
            f"""
            SELECT '{season_schema[7:]}' as "Season", match as "Match", player as "Player"
            FROM {season_schema}.compo
            WHERE length(split_part(player, '_', 1)) != 8
              OR CASE
                  WHEN split_part(player, '_', 2) = 'uefa'
                  THEN array_length(string_to_array(player, '_'), 1) != 5
                  ELSE array_length(string_to_array(player, '_'), 1) != 4
            END
            """
            for season_schema in all_season_schemas
        ]
    )
    final_query = f"""
            SELECT *
            FROM ({union_query}) AS all_seasons
            ORDER BY "Season" desc;
        """
    return execute_query(_db_conn, final_query)


def set_unknown_players_section(db_conn):
    with st.container():
        set_sub_title("Basic consistency enforced by foreign keys")

        cols = st.columns([2, 3])
        with cols[0]:
            set_sub_sub_title("Unknown players")
            st.write(get_unknown_players(db_conn))

        with cols[1]:
            set_sub_sub_title("Non team players who still played a game")
            st.write(get_players_in_match_but_not_in_team(db_conn))
