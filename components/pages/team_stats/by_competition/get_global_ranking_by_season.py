import altair as alt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file
from config import COMPETITIONS


@st.cache_data(show_spinner=False)
def ranking_by_chp_by_week_of_season(_db_conn, chosen_ranking, chosen_comp, season):
    df_season = pd.DataFrame()

    teams = get_teams_by_comp_by_season(_db_conn, chosen_comp, [season])
    nb_weeks = 2 * (len(teams) - 1)
    for week in range(1, nb_weeks + 1):
        sql_file = read_sql_file(
            file_name="components/queries/team_stats/by_competition/over_many_seasons/get_ranking_by_season.sql",
            ranking=chosen_ranking,
            name_comp=chosen_comp,
            season=season,
            week=week
        )
        df_week = execute_query(_db_conn, sql_file)
        df_season = pd.concat([df_season, df_week], ignore_index=True)

    return df_season


@st.cache_data(show_spinner=False)
def ranking_by_chp_by_week_by_season(_db_conn, chosen_ranking, chosen_comp, chosen_seasons):
    complete_df = pd.DataFrame()

    for season in chosen_seasons:
        df_season = ranking_by_chp_by_week_of_season(_db_conn, chosen_ranking, chosen_comp, season)

        complete_df = pd.concat([complete_df, df_season], ignore_index=True)

    return complete_df


def get_global_ranking_by_season(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    comps = list(comps_and_kind.keys())

    chosen_comp = st.selectbox(
        key="global_ranking_by_season__comp",
        label="Choose competition...",
        options=[""] + comps
    )

    if chosen_comp:
        # kind_of_comp = comps_and_kind[chosen_comp]

        seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

        chosen_seasons = st.multiselect(
            key="global_ranking_by_season__seasons",
            label="Choose season...",
            options=seasons_by_comp
        )

        if chosen_seasons:
            # n_seasons = len(seasons_by_comp)

            with st.spinner("Data loading..."):
                df = ranking_by_chp_by_week_by_season(
                    _db_conn=db_conn,
                    chosen_ranking="Points",
                    chosen_comp=chosen_comp,
                    chosen_seasons=chosen_seasons,
                )

            teams = get_teams_by_comp_by_season(db_conn, chosen_comp, chosen_seasons)
            n_teams = len(teams)

            chosen_teams = st.multiselect(
                key="global_ranking_by_season__teams",
                label="Choose teams...",
                options=["All"] + teams
            )

            if 'All' in chosen_teams:
                chosen_teams = teams

            if chosen_teams:

                # set_plot(df, chosen_comp, chosen_teams, n_teams)
                set_plot_cumulative_ranking(df, chosen_comp, chosen_teams, n_teams)
                set_plot_cumulative_ranking_per_match(df, chosen_comp, chosen_teams, n_teams)

                csv = df.to_csv(index=False, sep='|', decimal=',')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"{chosen_comp.replace(' ', '_').lower()}_global_ranking_by_season.csv",
                    mime="text/csv"
                )


def set_plot(df, chosen_comp, chosen_teams, n_teams):
    filtered_df = df[df["Club"].isin(chosen_teams)]
    filtered_df["Club_Season"] = filtered_df["Club"] + ' - ' + filtered_df["Season"]

    line_chart = alt.Chart(filtered_df).mark_line(point=True, interpolate="linear").encode(
        x=alt.X(shorthand='Week:O'),
        y=alt.Y(shorthand='Points:Q'),
        color=alt.Color('Club_Season:N', legend=alt.Legend(title="Club - Season", orient="right", labelLimit=2000)),
        tooltip=['Club', 'Season', "Points", "Ranking"]
    ).properties(
        title=f"Number of points over weeks by season - {chosen_comp}",
        height=510 if n_teams == 20 else 460 if n_teams == 18 else 600
    )

    line_text = line_chart.mark_text(
        align='center',
        baseline='bottom',
        fontSize=12,
        dy=-2,
        color='black'
    ).encode(
        text=alt.Text('Ranking:Q')
    )

    chart = alt.layer(
        line_chart,
        line_text
    )

    st.altair_chart(chart, use_container_width=True)


def set_plot_cumulative_ranking(df, chosen_comp, chosen_teams, n_teams):
    filtered_df = df[df["Club"].isin(chosen_teams)].copy()
    filtered_df["Club_Season"] = filtered_df["Club"] + ' - ' + filtered_df["Season"].astype(str)

    club_seasons = sorted(filtered_df['Club_Season'].unique())
    colors = px.colors.qualitative.D3  # palette moderne
    club_colors = {cs: colors[i % len(colors)] for i, cs in enumerate(club_seasons)}

    traces = []
    for cs in club_seasons:
        df_cs = filtered_df[filtered_df['Club_Season'] == cs].sort_values('Week')
        traces.append(
            go.Scatter(
                x=df_cs['Week'],
                y=df_cs['Points'],
                mode='lines+markers+text',
                name=cs,
                line=dict(color=club_colors[cs]),
                marker=dict(color=club_colors[cs]),
                text=df_cs['Ranking'].astype(str),
                textposition='top center',
                textfont=dict(color=club_colors[cs]),
                hovertemplate=(
                    f"<b>{cs}</b><br>" +
                    "Week: %{x}<br>" +
                    "Side: %{customdata[0]}<br>" +
                    "Result: %{customdata[1]}<br>" +
                    "Opponent: %{customdata[2]}<br><br>" +
                    "<b>Points:</b> %{y}<br>" +
                    "<b>Ranking:</b> %{text}<extra></extra>"
                ),
                customdata=df_cs[["Side", "Result", "Opponent"]],
                showlegend=True,
            )
        )

    layout = go.Layout(
        title=f"Number of points over weeks by season - {chosen_comp}<br><sup>With global ranking</sup>",
        xaxis=dict(title='Week', type='category', tickmode='linear'),
        yaxis=dict(title='Points'),
        height=510 if n_teams == 20 else 460 if n_teams == 18 else 600,
        width=2000,
        legend=dict(title='Club - Season', y=1, yanchor='top', x=1.05, xanchor='left'),
        margin=dict(l=50, r=180, t=80, b=80)
    )

    fig = go.Figure(data=traces, layout=layout)
    st.plotly_chart(fig, use_container_width=True)


def set_plot_cumulative_ranking_per_match(df, chosen_comp, chosen_teams, n_teams):
    filtered_df = df[df["Club"].isin(chosen_teams)].copy()
    filtered_df["Club_Season"] = filtered_df["Club"] + ' - ' + filtered_df["Season"].astype(str)

    club_seasons = sorted(filtered_df['Club_Season'].unique())
    colors = px.colors.qualitative.D3  # palette moderne
    club_colors = {cs: colors[i % len(colors)] for i, cs in enumerate(club_seasons)}

    traces = []
    for cs in club_seasons:
        df_cs = filtered_df[filtered_df['Club_Season'] == cs].sort_values('Week')
        traces.append(
            go.Scatter(
                x=df_cs['Week'],
                y=df_cs['Points/Match'],
                mode='lines+markers+text',
                name=cs,
                line=dict(color=club_colors[cs]),
                marker=dict(color=club_colors[cs]),
                text=df_cs['Ranking'].astype(str),
                textposition='top center',
                textfont=dict(color=club_colors[cs]),
                hovertemplate=(
                    f"<b>{cs}</b><br>" +
                    "Week: %{x}<br>" +
                    "Side: %{customdata[0]}<br>" +
                    "Result: %{customdata[1]}<br>" +
                    "Opponent: %{customdata[2]}<br><br>" +
                    "<b>Points/Match:</b> %{y:.2f}<br>" +
                    "<b>Ranking:</b> %{text}<extra></extra>"
                ),
                customdata=df_cs[["Side", "Result", "Opponent"]],
                showlegend=True,
            )
        )

    layout = go.Layout(
        title=f"Number of points over weeks by season - {chosen_comp}<br><sup>With global ranking</sup>",
        xaxis=dict(title='Week', type='category', tickmode='linear'),
        yaxis=dict(title='Points'),
        height=510 if n_teams == 20 else 460 if n_teams == 18 else 600,
        width=2000,
        legend=dict(title='Club - Season', y=1, yanchor='top', x=1.05, xanchor='left'),
        margin=dict(l=50, r=180, t=80, b=80)
    )

    fig = go.Figure(data=traces, layout=layout)
    st.plotly_chart(fig, use_container_width=True)
