import altair as alt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query
from config import TEAM_STATS_RANKINGS_PLOTTABLE, COMPETITIONS
from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def ranking_by_chp_week(_db_conn, chosen_ranking, chosen_comp, chosen_seasons):
    complete_df = pd.DataFrame()

    for season in chosen_seasons:
        sql_file = read_sql_file(
            file_name="components/queries/team_stats/given_competition/over_many_seasons/get_ranking_over_many_seasons.sql",
            ranking=chosen_ranking,
            name_comp=chosen_comp,
            season=season,
        )
        df_season = execute_query(_db_conn, sql_file)
        complete_df = pd.concat([complete_df, df_season], ignore_index=True)

    return complete_df


def get_ranking_over_many_seasons(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    comps = list(comps_and_kind.keys())

    chosen_comp = st.selectbox(
        key="ranking_over_many_seasons__comp",
        label="Choose competition...",
        options=[""] + comps
    )

    if chosen_comp:
        with st.spinner("Data loading..."):
            # kind_of_comp = comps_and_kind[chosen_comp]

            seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)
            # n_seasons = len(seasons_by_comp)

            teams = get_teams_by_comp_by_season(db_conn, chosen_comp, seasons_by_comp)
            n_teams = len(teams)

            chosen_ranking = st.selectbox(
                key="ranking_many_seasons__ranking",
                label="Choose ranking...",
                options=TEAM_STATS_RANKINGS_PLOTTABLE,
                index=1
            )

            df = ranking_by_chp_week(
                _db_conn=db_conn,
                chosen_ranking=chosen_ranking,
                chosen_comp=chosen_comp,
                chosen_seasons=seasons_by_comp,
            )

            all_combinations = pd.MultiIndex.from_product(
                [teams, seasons_by_comp],
                names=['Club', 'Season']
            ).to_frame(index=False)

            df = pd.merge(all_combinations, df, how='left', on=['Club', 'Season'])

        chosen_teams = st.multiselect(
            key="ranking_over_many_seasons__teams",
            label="Choose teams...",
            options=["All"] + teams,
        )

        if 'All' in chosen_teams:
            chosen_teams = teams

        if chosen_teams:
            # set_plot(df, chosen_comp, chosen_teams, n_teams)
            set_plot_plotly(df, chosen_comp, chosen_teams, chosen_ranking, n_teams)

            csv = df.to_csv(index=False, sep='|')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{chosen_comp.replace(' ', '_').lower()}_ranking_over_many_seasons.csv",
                mime="text/csv"
            )


def set_plot(df, chosen_comp, chosen_teams, chosen_ranking, n_teams):
    filtered_df = df[df["Club"].isin(chosen_teams)]

    line_chart = alt.Chart(filtered_df).mark_line(point=True, interpolate="linear").encode(
        x=alt.X(shorthand='Season:O', title='Season'),
        y=alt.Y(shorthand='chosen_ranking:Q', title=chosen_ranking),
        color=alt.Color(shorthand='Club:N', legend=alt.Legend(title="Clubs", orient="right", labelLimit=2000)),
        tooltip=['Club', 'Season', chosen_ranking, "Ranking"]
    ).properties(
        title=f"Number of points over seasons - {chosen_comp}",
        height=510 if n_teams == 20 else 460 if n_teams == 18 else 600
    )

    weeks_per_season = (
        df[df["Ranking"].notnull()].groupby('Season')['Club']
        .nunique()
        .reset_index(name='NumClubs')
    )
    weeks_per_season["Weeks"] = 2 * (weeks_per_season["NumClubs"] - 1)
    weeks_per_season['MaxPoints'] = weeks_per_season['Weeks'] * 3
    max_points_df = weeks_per_season[['Season', 'MaxPoints']]

    line_text = line_chart.mark_text(
        align='center',
        baseline='bottom',
        fontSize=12,
        dy=-2,
        color='black'
    ).encode(
        text=alt.Text('Ranking:Q')
    )

    if chosen_ranking == "Points":
        max_line = alt.Chart(max_points_df).mark_line(
            strokeDash=[6, 4],
            color='gray'
        ).encode(
            x=alt.X(shorthand='Season:O'),
            y=alt.Y(shorthand='MaxPoints:Q'),
            tooltip=['Season', 'MaxPoints']
        )

        chart = alt.layer(
            line_chart,
            max_line,
            line_text
        )
    else:
        chart = alt.layer(
            line_chart,
            line_text
        )

    st.altair_chart(chart, use_container_width=True)


def set_plot_plotly(df, chosen_comp, chosen_teams, chosen_ranking, n_teams):
    filtered_df = df[df["Club"].isin(chosen_teams)]

    clubs = sorted(filtered_df['Club'].unique())
    colors = px.colors.qualitative.D3
    club_colors = {club: colors[i % len(colors)] for i, club in enumerate(clubs)}

    traces = []

    if chosen_ranking == "Points":
        weeks_per_season = (
            df[df["Global Ranking"].notnull()].groupby('Season')['Club']
            .nunique()
            .reset_index(name='NumClubs')
        )
        weeks_per_season["Weeks"] = 2 * (weeks_per_season["NumClubs"] - 1)
        weeks_per_season['MaxPoints'] = weeks_per_season['Weeks'] * 3

        max_points_df = weeks_per_season[['Season', 'MaxPoints']].sort_values('Season')

        max_line = go.Scatter(
            x=max_points_df['Season'],
            y=max_points_df['MaxPoints'],
            mode='lines',
            name='Max Possible',
            line=dict(color='gray', dash='dash'),
            hovertemplate='Season: %{x}<br>Max Points: %{y}<extra></extra>',
            showlegend=True
        )

        traces.append(max_line)

    for club in clubs:
        df_club = filtered_df[filtered_df['Club'] == club].sort_values('Season')
        traces.append(
            go.Scatter(
                x=df_club['Season'],
                y=df_club[chosen_ranking],
                mode='lines+markers+text',
                name=club,
                line=dict(color=club_colors[club]),
                marker=dict(color=club_colors[club]),
                text=df_club[f"{chosen_ranking} Ranking"].astype(str),
                textposition='top center',
                textfont=dict(color=club_colors[club]),
                customdata=df_club[["Global Ranking"]],
                hovertemplate=(
                        f"<b>{club}</b><br>" +
                        "<b>Season: </b>%{x}<br><br>" +
                        f"<b>{chosen_ranking}: </b>%{{y}}<br>" +
                        f"<b>{chosen_ranking} Ranking: </b>%{{text}}<br>" +
                        "Global Ranking: %{customdata[0]}<extra></extra>"
                ),
                showlegend=True
            )
        )

    layout = go.Layout(
        title=f"Number of {chosen_ranking} over seasons - {chosen_comp}<br><sup>With global ranking</sup>",
        xaxis=dict(title='Season', type='category', tickangle=270),
        yaxis=dict(title=chosen_ranking),
        height=510 if n_teams == 20 else 460 if n_teams == 18 else 600,
        legend=dict(title='Clubs', y=1, yanchor='top', x=1.05, xanchor='left'),
        margin=dict(l=50, r=150, t=80, b=50)
    )

    fig = go.Figure(data=traces, layout=layout)
    st.plotly_chart(fig, use_container_width=True)
