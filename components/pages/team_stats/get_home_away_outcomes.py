import streamlit as st
import altair as alt

from components.commons.search_for_item import make_search_function
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file
from config import COMPETITIONS, DUAL_STATS


@st.cache_data(show_spinner=False)
def get_balance(_db_conn):
    sql_file = read_sql_file("components/queries/team_stats/get_home_away_balance.sql",)
    return execute_query(_db_conn, sql_file)

def get_home_away_outcomes(db_conn):
    df = get_balance(db_conn)

    df_outcomes_melt = df.melt(
        id_vars=["Competition", "Matches"],
        value_vars=["Home Wins", "Draws", "Away Wins"],
        var_name="Side",
        value_name="Count"
    )
    df_outcomes_melt['Side Light'] = df_outcomes_melt['Side'].str.replace(' Wins', '')
    df_outcomes_melt['Ratio'] = (df_outcomes_melt['Count'] / df_outcomes_melt['Matches']) * 100

    df_goals_melt = df.melt(
        id_vars=["Competition", "Matches"],
        value_vars=["Home Goals", "Draws Goals", "Away Goals"],
        var_name="Side",
        value_name="Count"
    )
    df_goals_melt['Side Light'] = df_goals_melt['Side'].str.replace(' Goals', '')
    df_goals_melt['Avg'] = (df_goals_melt['Count'] / df_goals_melt['Matches'])

    outcome_chart = alt.Chart(df_outcomes_melt).mark_bar().encode(
        x=alt.X("Competition:N"),
        y=alt.Y('Count:Q', title='#'),
        xOffset=alt.XOffset('Side Light:N', sort=['Home', 'Draws', 'Away']),
        color=alt.Color(
            "Side:N",
            scale=alt.Scale(
                domain=["Home Wins", "Draws", "Away Wins", "Home Goals", "Away Goals"],
                range=['#1f77b4', '#aec7e8', '#1f77b4', 'orange', 'orange']
            ),
            sort=['Home Wins', 'Draws', 'Away Wins', "Home Goals", "Away Goals"],
            legend=alt.Legend(title='Outcome and Goals')
        ),
        tooltip=["Competition", "Side", "Count:Q", alt.Tooltip("Ratio:Q", format=".2f", title="Ratio (%)")]
    )

    goals_chart = alt.Chart(df_goals_melt).mark_bar().encode(
        x=alt.X("Competition:N"),
        y=alt.Y('Count:Q', title='#'),
        xOffset=alt.XOffset('Side Light:N', sort=['Home', 'Draws', 'Away']),
        color=alt.Color(
            "Side:N",
            scale=alt.Scale(
                domain=["Home Wins", "Draws", "Away Wins", "Home Goals", "Away Goals"],
                range=['#1f77b4', '#aec7e8', '#1f77b4', 'orange', 'orange']
            )
        ),
        tooltip=["Competition", "Side", "Count:Q", alt.Tooltip("Avg:Q", format=".2f", title="Per match")]
    )

    chart = (goals_chart + outcome_chart).properties(
        title="Match Outcomes and Goals by Competition in the 21th century",
        height=600
    )

    st.altair_chart(chart, use_container_width=True)