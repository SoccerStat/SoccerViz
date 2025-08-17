import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file
from config import TEAM_RANKINGS, COMPETITIONS, C_CUPS_TEAMS_EXCLUDED_RANKINGS, KIND_C_CUP, KIND_CHP, \
    TEAM_STATS_RANKINGS_PLOTTABLE


@st.cache_data(show_spinner=False)
def ranking_by_chp_week(_db_conn, chosen_ranking, chosen_comp, chosen_season, nb_chp_weeks):
    complete_df = pd.DataFrame()
    
    for j in range(1, nb_chp_weeks + 1):
        sql_file = read_sql_file(
            file_name="components/queries/team_stats/by_competition/over_one_season/get_cumulative_ranking_one_season.sql",
            ranking=chosen_ranking,
            name_comp=chosen_comp,
            season=chosen_season,
            week=j,
        )
        df_j = execute_query(_db_conn, sql_file)
        complete_df = pd.concat([complete_df, df_j], ignore_index=True)

    return complete_df


@st.cache_data(show_spinner=False)
def ranking_by_c_cup_week(_db_conn, chosen_ranking, chosen_comp, chosen_season):
    complete_df = pd.DataFrame()

    return complete_df


def get_ranking_one_season(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    comps = list(comps_and_kind.keys())

    chosen_comp = st.selectbox(
        key="ranking_one_season__comp",
        label="Choose competition...",
        options=comps
    )

    kind_of_comp = comps_and_kind[chosen_comp]

    seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

    chosen_season = st.selectbox(
        key="ranking_one_season__season",
        label="Choose season...",
        options=[""] + seasons_by_comp
    )

    if chosen_season:

        teams = get_teams_by_comp_by_season(db_conn, chosen_comp, [chosen_season])
        n_teams = len(teams)

        chosen_ranking = st.selectbox(
            key="ranking_one_season__ranking",
            label="Choose ranking...",
            options=TEAM_STATS_RANKINGS_PLOTTABLE,
            index=1
        )

        if chosen_ranking:
            with st.spinner("Data loading..."):
                if kind_of_comp == KIND_CHP:
                    n_weeks = 2 * (n_teams - 1)
                    df = ranking_by_chp_week(
                        _db_conn=db_conn,
                        chosen_ranking=chosen_ranking,
                        chosen_comp=chosen_comp,
                        chosen_season=chosen_season,
                        nb_chp_weeks=n_weeks
                    )

                elif kind_of_comp == KIND_C_CUP:
                    # n_weeks = 100
                    df = ranking_by_c_cup_week(
                        _db_conn=db_conn,
                        chosen_ranking=chosen_ranking,
                        chosen_comp=chosen_comp,
                        chosen_season=chosen_season
                    )

            st.multiselect(
                key="ranking_one_season__teams",
                label="Choose teams...",
                options=["All"] + teams
            )

            chosen_teams = st.session_state.ranking_one_season__teams

            if 'All' in chosen_teams:
                chosen_teams = teams

            if chosen_teams:
                set_plots(df, n_teams, chosen_comp, chosen_season, chosen_ranking, chosen_teams)

                csv = df.to_csv(index=False, sep='|')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"{chosen_comp.replace(' ', '_').lower()}_{chosen_season}_ranking_one_season.csv",
                    mime="text/csv"
                )


def set_plots(df, n_teams, chosen_comp, chosen_season, chosen_ranking, chosen_teams):
    df = df.sort_values(by=["Week", chosen_ranking], ascending=[True, False])
    filtered_df = df[df["Club"].isin(chosen_teams)]

    set_plot_cumulative_ranking(filtered_df, chosen_comp, chosen_season, chosen_ranking, n_teams)
    set_plot_cumulative_ranking_per_match(filtered_df, chosen_comp, chosen_season, chosen_ranking, n_teams)


def set_plot_cumulative_ranking(df, chosen_comp, chosen_season, chosen_ranking, n_teams):
    data = []

    if chosen_ranking == "Points":
        # Ligne Max Possible
        weeks = sorted(df['Week'].unique())
        max_ranking = [3 * int(w) for w in weeks]
        max_line = go.Scatter(
            x=weeks,
            y=max_ranking,
            mode='lines',
            line=dict(color='gray', dash='dash'),
            name='Max Possible',
            hoverinfo='skip',
            showlegend=True
        )
        data = data + [max_line]

    # Points réels
    df_actual = df[["Global Ranking", "Club", "Week", chosen_ranking, f"{chosen_ranking} Ranking", "Side", "Result", "Opponent"]].drop_duplicates()
    clubs = sorted(df_actual['Club'].unique())
    colors = px.colors.qualitative.D3  # palette qualitative de Plotly

    # Map club -> color
    club_colors = {club: colors[i % len(colors)] for i, club in enumerate(clubs)}

    actual_traces = []
    for club in clubs:
        df_club = df_actual[df_actual['Club'] == club].sort_values('Week')
        actual_traces.append(
            go.Scatter(
                x=df_club['Week'],
                y=df_club[chosen_ranking],
                mode='lines+markers+text',
                name=club,
                text=df_club['Global Ranking'].astype(str),
                textposition='top center',
                textfont=dict(color=club_colors[club]),
                hovertemplate=(
                    f"<b>{club}</b><br>" +
                    "Week: %{x}<br>" +
                    "Side: %{customdata[2]}<br>" +
                    "Result: %{customdata[3]}<br>" +
                    "<b>Opponent: </b>%{customdata[4]}<br><br>" +
                    f"<b>{chosen_ranking}:</b> %{{y}}<br>" +
                    f"<b>{chosen_ranking} Ranking:</b> %{{customdata[1]}}<br>" +
                    "Global Ranking: %{customdata[0]}<extra></extra>"
                ),
                customdata=df_club[["Global Ranking", f"{chosen_ranking} Ranking", "Side", "Result", "Opponent"]],
                line=dict(color=club_colors[club]),
                marker=dict(color=club_colors[club]),
                showlegend=True,
            )
        )

    data = data + actual_traces

    # Layout
    layout = go.Layout(
        title=f"Evolution of {chosen_ranking} - {chosen_comp} ({chosen_season})<br><sup>With global ranking</sup>",
        xaxis=dict(title='Week', type='category'),
        yaxis=dict(title=chosen_ranking),
        height=510 if n_teams == 20 else 460 if n_teams == 18 else 600,
        legend=dict(title='Clubs', y=1, yanchor='top', x=1.05, xanchor='left'),
        margin=dict(l=50, r=150, t=80, b=50)
    )

    fig = go.Figure(data=data, layout=layout)

    st.plotly_chart(fig, use_container_width=True)


def set_plot_cumulative_ranking_per_match(df, chosen_comp, chosen_season, chosen_ranking, n_teams):
    df_actual = df[["Global Ranking", "Club", "Week", f"{chosen_ranking}/Match", f"{chosen_ranking} Ranking", "Side", "Result", "Opponent"]].drop_duplicates()

    weeks = sorted(df['Week'].unique())
    # Ticks toutes les 2 semaines (ex: impaires)
    tickvals = [w for w in weeks if int(w) % 2 == 1]
    clubs = sorted(df_actual['Club'].unique())
    colors = px.colors.qualitative.D3  # palette qualitative de Plotly

    # Map club -> color
    club_colors = {club: colors[i % len(colors)] for i, club in enumerate(clubs)}

    actual_traces = []
    for club in clubs:
        df_club = df_actual[df_actual['Club'] == club].sort_values('Week')
        actual_traces.append(
            go.Scatter(
                x=df_club['Week'],
                y=df_club[f'{chosen_ranking}/Match'],
                mode='lines+markers+text',
                name=club,
                text=df_club['Global Ranking'].astype(str),
                textposition='top center',
                textfont=dict(color=club_colors[club]),
                hovertemplate=(
                    f"<b>{club}</b><br>" +
                    "Week: %{x}<br>" +
                    "Side: %{customdata[2]}<br>" +
                    "Result: %{customdata[3]}<br>" +
                    "<b>Opponent: </b>%{customdata[4]}<br><br>" +
                    f"<b>{chosen_ranking}/Match:</b> %{{y:.2f}}<br>" +
                    f"<b>{chosen_ranking} Ranking:</b> %{{customdata[1]}}<br>" +
                    "Global Ranking: %{customdata[0]}<extra></extra>"
                ),
                customdata=df_club[["Global Ranking", f"{chosen_ranking} Ranking", "Side", "Result", "Opponent"]],
                line=dict(color=club_colors[club]),
                marker=dict(color=club_colors[club]),
                showlegend=True
            )
        )

    data = actual_traces

    layout = go.Layout(
        title=f"Actual evolution of {chosen_ranking} per match - {chosen_comp} ({chosen_season})<br><sup>With global ranking</sup>",
        xaxis=dict(
            title='Week',
            type='category',
            tickmode='array',
            tickvals=tickvals,
            ticktext=[str(w) for w in tickvals],
        ),
        yaxis=dict(title=f'{chosen_ranking} per Match'),
        height=510 if n_teams == 20 else 460 if n_teams == 18 else 600,
        legend=dict(title='Clubs', y=1, yanchor='top', x=1.05, xanchor='left'),
        margin=dict(l=50, r=150, t=80, b=50),
    )

    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig, use_container_width=True)
