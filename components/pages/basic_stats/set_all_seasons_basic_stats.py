import streamlit as st

from components.commons.get_seasons import get_all_season_schemas
from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def set_count_matches(_db_conn, all_season_schemas):
    union_query = " UNION ALL ".join(
        [
            f"SELECT COUNT(*) AS c FROM {schema}.match"
            for schema in all_season_schemas
        ]
    )
    final_query = f"SELECT SUM(c) AS total_matches FROM ({union_query}) AS all_counts;"
    return execute_query(_db_conn, final_query)


def set_all_seasons_basic_stats(db_conn):
    if db_conn:
        with st.container():
            players, matches, clubs, seasons = st.columns([1, 1, 1, 1])

            all_season_schemas = get_all_season_schemas(db_conn)

            with players:
                query = read_sql_file("components/queries/basic_stats/upper/count_players.sql")
                resu = execute_query(db_conn, query)
                if resu is not None:
                    st.markdown(
                        f"""
                        <h3 style='text-align: center; font-weight: normal'>
                            <strong>{int(resu.iloc[0, 0])}</strong> Players
                        </h3>
                        """,
                        unsafe_allow_html=True
                    )

            with matches:
                resu = set_count_matches(db_conn, all_season_schemas)
                if resu is not None:
                    st.markdown(
                        f"""
                        <h3 style='text-align: center; font-weight: normal'>
                            <strong>{int(resu.iloc[0, 0])}</strong> Matches
                        </h3>
                        """,
                        unsafe_allow_html=True
                    )

            with clubs:
                query = read_sql_file("components/queries/basic_stats/upper/count_clubs.sql")
                resu = execute_query(db_conn, query)
                if resu is not None:
                    st.markdown(
                        f"""
                        <h3 style='text-align: center; font-weight: normal'>
                            <strong>{int(resu.iloc[0, 0])}</strong> Clubs
                        </h3>
                        """,
                        unsafe_allow_html=True
                    )

            with seasons:
                st.markdown(
                    f"""
                    <h3 style='text-align: center; font-weight: normal'>
                        <strong>{len(all_season_schemas)}</strong> Seasons
                    </h3>
                    """,
                    unsafe_allow_html=True
                )
