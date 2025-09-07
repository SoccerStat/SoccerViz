import streamlit as st

from components.commons.get_seasons import get_all_seasons
from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file


def set_all_seasons_basic_stats(db_conn):
    if db_conn:
        with st.container():
            players, matches, clubs, seasons = st.columns([1, 1, 1, 1])

            all_seasons = get_all_seasons(db_conn)

            with players:
                query = read_sql_file("components/queries/basic_stats/n_players.sql")
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
                union_query = " UNION ALL ".join([f"SELECT COUNT(*) AS c FROM {schema}.match" for schema in all_seasons])
                final_query = f"SELECT SUM(c) AS total_matches FROM ({union_query}) AS all_counts;"
                resu = execute_query(db_conn, final_query)
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
                query = read_sql_file("components/queries/basic_stats/n_clubs.sql")
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
                        <strong>{len(all_seasons)}</strong> Seasons
                    </h3>
                    """,
                    unsafe_allow_html=True
                )
