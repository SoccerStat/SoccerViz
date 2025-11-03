import streamlit as st

from components.commons.get_seasons import get_all_season_schemas
from components.commons.set_titles import set_sub_sub_title
from components.queries.execute_query import execute_query
from config import COMPETITIONS

from utils.file_helper.reader import read_sql_file


# @st.cache_data(show_spinner=False)
def get_top_scorers(_db_conn, in_ranking, chosen_comp, chosen_season, chosen_side):
    sql_file = read_sql_file(
        file_name="components/queries/player_stats/top_players.sql",
        ranking=in_ranking,
        comp=chosen_comp,
        season=chosen_season,
        side=chosen_side.lower(),
    )
    st.write(sql_file)

    return execute_query(_db_conn, sql_file)


def get_top_players(db_conn):
    col, _ = st.columns(2)

    with col:
        chosen_comp = st.selectbox(
            key="top_players__comp",
            label="Choose one competition...",
            options=[""] + ["All"] + [comp["label"] for _, comp in COMPETITIONS.items()]
        )

        if chosen_comp:
            all_seasons = [season_schema[7:] for season_schema in get_all_season_schemas(db_conn)]

            chosen_season = st.selectbox(
                key="top_players__season",
                label="Choose one season...",
                options=[""] + all_seasons
            )

            if chosen_season:

                # chosen_ranking = st.selectbox(
                #     key="top_players__ranking",
                #     label="Choose a ranking...",
                #     options=[""] + PLAYER_RANKING
                # )

                # if chosen_ranking:
                chosen_side = st.radio(
                    key="top_players__side",
                    label="Side",
                    options=["Home", "Both", "Away"],
                    horizontal=True,
                    label_visibility="collapsed",
                    index=1
                )

    if chosen_comp and chosen_season:
        goals, assists = st.columns(2)

        with goals:
            set_sub_sub_title("Goals")
            st.write(get_top_scorers(db_conn, 'Goals', chosen_comp, chosen_season, chosen_side))

        with assists:
            set_sub_sub_title("Assists")
            st.write(get_top_scorers(db_conn, 'Assists', chosen_comp, chosen_season, chosen_side))