import streamlit as st
import pandas as pd
import altair as alt

from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file

def get_counts_by_item(db_conn, chosen_season, column, item):
    sql_file = read_sql_file(
        file_name=f"components/queries/monitoring/plot/by_season.sql",
        in_season=chosen_season,
        date_column=column,
        in_tab=item
    )
    return execute_query(db_conn, sql_file)

def plot_by_season(db_conn, chosen_season, column):
    matches = "Matches"
    teams = "Teams"
    team_players = "Team Players"

    df_matches = get_counts_by_item(db_conn, chosen_season, column, matches.lower()[:-2])
    df_teams = get_counts_by_item(db_conn, chosen_season, column, teams.lower()[:-1])
    df_team_players = get_counts_by_item(db_conn, chosen_season, column, team_players.lower().replace(' ', '_')[:-1])

    df = pd.merge(df_matches, df_teams, on=column, how='outer').fillna(0)
    df = pd.merge(df, df_team_players, on=column, how='outer').fillna(0)
    df = df.sort_values(column)

    df_melted = df.melt(
        id_vars=column,
        value_vars=["match_count", "team_count", "team_player_count"],
        var_name="type",
        value_name="count"
    )

    df_melted["type"] = df_melted["type"].replace({
        "match_count": matches,
        "team_count": teams,
        "team_player_count": team_players,
    })

    chart = alt.Chart(df_melted).mark_line(point=True).encode(
        x=alt.X(f"{column}:T", title="Date"),
        y=alt.Y("count:Q", title=f"Number {'inserted' if column == 'inserted_at' else 'updated'}"),
        color=alt.Color(
            "type:N",
            scale=alt.Scale(
                domain=[matches, teams, team_players],
                range=["#1f77b4", "#ffcc00", "#2ca02c"],
            ),
            title="Item"
        ),
        tooltip=[f"{column}:T", "type:N", "count:Q"]
    ).properties(
        title=f"Daily {'insertion' if column == 'inserted_at' else 'update'} - Season {chosen_season}",
    )

    st.altair_chart(chart, use_container_width=True)