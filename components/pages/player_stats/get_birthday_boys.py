import streamlit as st
import pandas as pd
from datetime import datetime

from components.commons.get_seasons import get_all_seasons
from components.commons.set_titles import set_sub_sub_title
from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file


def format_dict(d):
    return ", ".join(f"{club}: [{', '.join(seasons)}]" for club, seasons in d.items())

@st.cache_data(show_spinner=False)
def get_birthday_boys_by_season(_db_conn, season_schema, date):
    sql_file = read_sql_file(
        file_name=f"components/queries/player_stats/birthday_boys.sql",
        season=season_schema[7:],
        date=date
    )
    return execute_query(_db_conn, sql_file)

def get_birthday_boys(db_conn):
    n_seasons = 5
    all_seasons_schema = get_all_seasons(db_conn)

    date_input, actual_date = st.columns([2,2])

    with date_input:
        chosen_date = st.date_input(
            key="birthday_boy__date",
            label="Choose a date...",
            value="today",
            format="YYYY-MM-DD"
        )

    with actual_date:
        set_sub_sub_title(chosen_date.strftime("%A %d %B %Y"))

    df = pd.DataFrame()

    for season_schema in all_seasons_schema[:n_seasons]:
        df_season = get_birthday_boys_by_season(db_conn, season_schema, chosen_date)
        df = pd.concat([df, df_season], ignore_index=True)

    df = df
    season_club_dict = (
        df.groupby(["Id", "Player", "Age"])
        .apply(
            lambda x: x.groupby("Club")["Season"].apply(list).to_dict(),
            include_groups=False
        )
    )

    df["Season x Club"] = (df
                           .set_index(["Id", "Player", "Age"])
                           .index.map(season_club_dict)
    )
    df["Season x Club"] = df["Season x Club"].apply(format_dict)

    df = df.drop(columns=["Season", "Club"])
    df = df.drop_duplicates(subset=["Id", "Player"])

    st.dataframe(df.sort_values(["Age", "Player"]), hide_index=True, use_container_width=True)
