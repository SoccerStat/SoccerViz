import altair as alt
import plotly.express as px
import streamlit as st

from components.commons.set_titles import set_sub_sub_sub_title
from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file

from config import COMPETITIONS


@st.cache_data(show_spinner=False)
def get_balance(_db_conn):
    sql_file = read_sql_file("components/queries/team_stats/all_competitions/balance/get_home_away_balance.sql")
    return execute_query(_db_conn, sql_file)


def compute_ratio(row):
    if row["Side"] == "Home Goals":
        return row["% Home Goals"]*100
    elif row["Side"] == "Away Goals":
        return row["% Away Goals"]*100
    else:
        return 100

def set_colors_by_comp():
    color_by_comp = {}
    for i, comp in enumerate(COMPETITIONS):
        comp_config = COMPETITIONS[comp]
        color_by_comp[comp_config["label"]] = comp_config["style"]["bg_color"]
    return color_by_comp

def get_home_away_balance(db_conn):
    df = get_balance(db_conn)

    set_sub_sub_sub_title("All seasons")
    df_all_seasons = df[df["Season"] == "All"]
    get_home_away_outcomes_all_seasons_plotly(df_all_seasons)

    colors_by_comp = set_colors_by_comp()
    df_by_season = df[df["Season"] != "All"]
    df_by_season = df_by_season.sort_values(["Season", "Competition"])

    set_sub_sub_sub_title("Goals by season")
    side_goals = st.radio(
        key='home_away_balance__side_goals',
        label="Side",
        options=["Home Goals", "Total Goals", "Away Goals"],
        horizontal=True,
        label_visibility="collapsed",
        index=1
    )
    get_home_away_goals_by_season_plotly(df_by_season, side_goals, colors_by_comp)

    set_sub_sub_sub_title("Outcomes by season")
    side_outcomes = st.radio(
        key='home_away_balance__side_outcomes',
        label="Side",
        options=["Home Wins", "Draws", "Away Wins"],
        horizontal=True,
        label_visibility="collapsed",
        index=0
    )
    get_home_away_outcomes_by_season_plotly(df_by_season, side_outcomes, colors_by_comp)


def get_home_away_outcomes(df):

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
        value_vars=["Home Goals", "Total Goals", "Away Goals"],
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
                domain=["Home Wins", "Draws", "Away Wins", "Home Goals", "Total Goals", "Away Goals"],
                range=['#1f77b4', '#aec7e8', '#1f77b4', 'orange', 'firebrick', 'orange']
            ),
            sort=['Home Wins', 'Draws', 'Away Wins', "Home Goals", "Total Goals", "Away Goals"],
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
                domain=["Home Wins", "Draws", "Away Wins", "Home Goals", "Total Goals", "Away Goals"],
                range=['#1f77b4', '#aec7e8', '#1f77b4', 'orange', 'firebrick', 'orange']
            )
        ),
        tooltip=["Competition", "Side", "Count:Q", alt.Tooltip("Avg:Q", format=".2f", title="Per match")]
    )

    chart = (goals_chart + outcome_chart).properties(
        title="Match Outcomes and Goals by Competition in the 21th century",
        height=600
    )

    st.altair_chart(chart, use_container_width=True)

def get_home_away_outcomes_all_seasons_plotly(df):
    color_map_outcomes = {
        "Home Wins": '#1f77b4',
        "Draws": '#aec7e8',
        "Away Wins": '#1f77b4'
    }
    color_map_goals = {
        "Home Goals": 'orange',
        "Total Goals": 'firebrick',
        "Away Goals": 'orange'
    }

    df_outcomes_melt = df.melt(
        id_vars=["Competition", "Matches"],
        value_vars=["Home Wins", "Draws", "Away Wins"],
        var_name="Side",
        value_name="Count"
    )
    df_outcomes_melt['Ratio'] = (df_outcomes_melt['Count'] / df_outcomes_melt['Matches']) * 100
    df_outcomes_melt["Color"] = df_outcomes_melt["Side"].map(color_map_outcomes)

    df_goals_melt = df.melt(
        id_vars=["Competition", "Matches", "% Home Goals", "% Away Goals"],
        value_vars=["Home Goals", "Total Goals", "Away Goals"],
        var_name="Side",
        value_name="Count"
    )
    df_goals_melt['Avg'] = (df_goals_melt['Count'] / df_goals_melt['Matches'])
    df_goals_melt['Ratio'] = df_goals_melt.apply(compute_ratio, axis=1)
    df_goals_melt["Color"] = df_goals_melt["Side"].map(color_map_goals)

    # Graphique outcomes
    fig_outcomes = px.bar(
        df_outcomes_melt,
        x='Competition',
        y='Count',
        color='Side',
        color_discrete_map=color_map_outcomes,
        barmode='group',
        title='Outcomes',
        hover_data={'Side': '', 'Ratio': ':.2f', 'Color': ''}
    )

    fig_outcomes.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br><br>" +
            "<span style='color:%{customdata[2]}'>⬤</span> %{customdata[0]}<br>"
            "<b>Count</b> %{y}<br>" +
            "<b>Ratio</b> %{customdata[1]:.2f}%<extra></extra>"
        )
    )
    fig_outcomes.update_yaxes(title_text="Number of Matches")

    # Graphique goals
    fig_goals = px.bar(
        df_goals_melt,
        x='Competition',
        y='Count',
        color='Side',
        color_discrete_map=color_map_goals,
        barmode='group',
        title='Goals',
        hover_data={'Side': '', 'Avg': ':.2f', 'Ratio': ':.2f', 'Color': ''}
    )

    fig_goals.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br><br>" +
            "<span style='color:%{customdata[3]}'>⬤</span> %{customdata[0]}<br>" +
            "<b>Avg</b> %{customdata[1]:.2f}<br>" +
            "<b>Ratio</b> %{customdata[2]:.2f}%<extra></extra>"
        )
    )
    fig_goals.update_yaxes(title_text="Number of Goals")

    # Affichage côte à côte dans Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_outcomes, use_container_width=True)
    with col2:
        st.plotly_chart(fig_goals, use_container_width=True)


def get_home_away_goals_by_season_plotly(df, side, colors):
    df["Goals / Match"] = df[side] / df["Matches"]

    fig = px.line(
        df,
        x='Season',
        y='Goals / Match',
        color='Competition',
        color_discrete_map=colors,
        title=f"{"" if side == 'Both' else f'{side} '}Goals per Match"
    )

    fig.update_traces(
        hovertemplate=(
                "<b>Competition: </b>%{fullData.name}<br>" +
                "<b>Season: </b>%{x}<br>" +
                f"<b>Side: </b>{side}<br><br>" +
                "<b>Goals / Match: </b>%{y:.2f}" +
                "<extra></extra>"
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    csv = df.to_csv(index=False, sep='|')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"all_competitions_{side.lower()}_stats_by_season.csv",
        mime="text/csv"
    )

def get_home_away_outcomes_by_season_plotly(df, side, colors):
    fig = px.line(
        df,
        x='Season',
        y=side,
        color='Competition',
        color_discrete_map=colors,
        title=side
    )

    fig.update_traces(
        hovertemplate=(
                "<b>Competition: </b>%{fullData.name}<br>" +
                "<b>Season: </b>%{x}<br>" +
                f"<b>Side: </b>{side}<br><br>" +
                f"<b>Outcome: </b>%{{y}}" +
                "<extra></extra>"
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    csv = df.to_csv(index=False, sep='|')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"all_competitions_{side.lower()}_stats_by_season.csv",
        mime="text/csv"
    )
