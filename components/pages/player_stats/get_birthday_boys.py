import streamlit as st
import pandas as pd

from components.commons.get_seasons import get_all_seasons
from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file


def format_dict(d):
    return ", ".join(f"{club}: [{', '.join(seasons)}]" for club, seasons in d.items())

# @st.cache_data(show_spinner=False)
def get_birthday_boys_by_season(_db_conn, season_schema):
    sql_file = read_sql_file(
        file_name=f"components/queries/player_stats/birthday_boys.sql",
        season=season_schema[7:]
    )
    return execute_query(_db_conn, sql_file)

def get_birthday_boys(db_conn):
    n_seasons = 5
    all_seasons_schema = get_all_seasons(db_conn)

    df = pd.DataFrame()

    for season_schema in all_seasons_schema[:n_seasons]:
        df_season = get_birthday_boys_by_season(db_conn, season_schema)
        df = pd.concat([df, df_season], ignore_index=True)

    df = df
    season_club_dict = (
        df.groupby(["Id", "Player", "Age"])
        .apply(lambda x: x.groupby("Club")["Season"].apply(list).to_dict())
    )

    df["Season x Club"] = (df
                           .set_index(["Id", "Player", "Age"])
                           .index.map(season_club_dict)
    )
    df["Season x Club"] = df["Season x Club"].apply(format_dict)

    df = df.drop(columns=["Season", "Club"])
    df = df.drop_duplicates(subset=["Id", "Player"])

    st.dataframe(df.sort_values(["Age", "Player"]), hide_index=True, use_container_width=True)
    # st.markdown(render_html_table(df), unsafe_allow_html=True)