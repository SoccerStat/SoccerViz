import streamlit as st
import pandas as pd
import altair as alt

from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file

@st.cache_data(show_spinner=False)
def get_counts_by_item(_db_conn, column, item):
    sql_file = read_sql_file(
        file_name=f"components/queries/monitoring/plot/upper.sql",
        date_column=column,
        in_tab=item
    )
    return execute_query(_db_conn, sql_file)

def plot_upper(db_conn, column):

    clubs = "Clubs"
    players = "Players"

    df_clubs = get_counts_by_item(db_conn, column, clubs.lower()[:-1])
    df_players = get_counts_by_item(db_conn, column, players.lower()[:-1])

    df = pd.merge(df_clubs, df_players, on=column, how='outer').fillna(0)
    df = df.sort_values(column)

    df_melted = df.melt(
        id_vars=column,
        value_vars=["club_count", "player_count"],
        var_name="type",
        value_name="count"
    )

    df_melted["type"] = df_melted["type"].replace({
        "club_count": clubs,
        "player_count": players
    })

    chart = alt.Chart(df_melted).mark_line(point=True).encode(
        x=alt.X(f"{column}:T", title="Date"),
        y=alt.Y("count:Q", title=f"Number {'inserted' if column == 'inserted_at' else 'updated'}"),
        color=alt.Color(
            "type:N",
            scale=alt.Scale(
                domain=[clubs, players],
                range=["#1f77b4", "#ffcc00"]
            ),
            title="Item"
        ),
        tooltip=[f"{column}:T", "type:N", "count:Q"]
    ).properties(
        title=f"Daily {'insertion' if column == 'inserted_at' else 'update'} - Upper items",
    )

    st.altair_chart(chart, use_container_width=True)