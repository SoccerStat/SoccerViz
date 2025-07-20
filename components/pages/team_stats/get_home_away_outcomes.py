import streamlit as st
import altair as alt

from components.commons.search_for_item import make_search_function
from components.commons.get_all_teams import get_all_teams
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file
from config import COMPETITIONS, DUAL_STATS


@st.cache_data(show_spinner=False)
def get_outcomes(_db_conn):
    sql_file = read_sql_file("components/queries/team_stats/get_home_away_outcomes.sql",)
    return execute_query(_db_conn, sql_file)


def get_home_away_outcomes(db_conn):
    df = get_outcomes(db_conn)

    df_melt = df.melt(
        id_vars="Competition",
        value_vars=["Home Wins", "Draws", "Away Wins"],
        var_name="Outcome",
        value_name="Count"
    )

    chart = alt.Chart(df_melt).mark_bar().encode(
        x=alt.X("Competition:N"),
        y=alt.Y('Count:Q', title='#'),
        xOffset=alt.XOffset('Outcome:N', sort=['Home Wins', 'Draws', 'Away Wins']),
        color=alt.Color(
            "Outcome:N",
            scale=alt.Scale(
                domain=["Home Wins", "Draws", "Away Wins"],
                range=['#1f77b4', '#aec7e8', '#1f77b4']
            ),
            sort=['Home Wins', 'Draws', 'Away Wins'],
            legend=alt.Legend(title='Outcome')
        )
    ).properties(
        title="Match Outcomes by Competition in the 21th century"
    )

    st.altair_chart(chart, use_container_width=True)