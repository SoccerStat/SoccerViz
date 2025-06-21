import streamlit as st
from components.queries.execute_query import execute_query
from config import START_SEASON, END_SEASON


def set_all_seasons_basic_stats(db_conn):
    if db_conn:
        with st.container():
            players, matches, clubs, seasons = st.columns([1,1,1,1])

            all_seasons = [f"season_{y}_{y+1}" for y in range(START_SEASON, END_SEASON)]

            with players:
                query = "SELECT count(*) from upper.player"
                resu = execute_query(db_conn, query)
                if resu is not None:
                    st.write(f"{int(resu.iloc[0, 0])} Players")

            with matches:
                union_query = " UNION ALL ".join([f"SELECT COUNT(*) AS c FROM {schema}.match" for schema in all_seasons])
                final_query = f"SELECT SUM(c) AS total_matches FROM ({union_query}) AS all_counts;"
                resu = execute_query(db_conn, final_query)
                if resu is not None:
                    st.write(f"{int(resu.iloc[0, 0])} Matches")

            with clubs:
                query = "SELECT count(*) from upper.club"
                resu = execute_query(db_conn, query)
                if resu is not None:
                    st.write(f"{int(resu.iloc[0, 0])} Clubs")

            with seasons:
                st.write(f"{len(all_seasons)} Seasons")