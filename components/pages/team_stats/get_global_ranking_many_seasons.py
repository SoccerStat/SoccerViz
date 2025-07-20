import streamlit as st
import pandas as pd
import altair as alt

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file
from config import TEAM_RANKINGS, COMPETITIONS, C_CUPS_TEAMS_EXCLUDED_RANKINGS, KIND_C_CUP, KIND_CHP


@st.cache_data(show_spinner=False)
def ranking_by_chp_week(_db_conn, chosen_ranking, chosen_comp, chosen_seasons):
    complete_df = pd.DataFrame()

    for season in chosen_seasons:
        sql_file = read_sql_file(
            file_name="components/queries/team_stats/get_ranking_many_seasons.sql",
            ranking=chosen_ranking,
            name_comp=chosen_comp,
            season=season,
        )
        df_season = execute_query(_db_conn, sql_file)
        complete_df = pd.concat([complete_df, df_season], ignore_index=True)

    return complete_df


def get_global_ranking_many_seasons(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    comps = list(comps_and_kind.keys())

    chosen_comp = st.selectbox(
        key="global_ranking_many_seasons__comp",
        label="Choose competition...",
        options=comps
    )

    # kind_of_comp = comps_and_kind[chosen_comp]

    seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)
    # n_seasons = len(seasons_by_comp)

    teams = get_teams_by_comp_by_season(db_conn, chosen_comp, seasons_by_comp)
    n_teams = len(teams)

    chosen_teams = st.multiselect(
        key="global_ranking_many_seasons__teams",
        label="Choose teams...",
        options=["All"] + teams,
    )

    if 'All' in chosen_teams:
        chosen_teams = teams

    if chosen_teams:
        with st.spinner("Data loading..."):

            df = ranking_by_chp_week(
                _db_conn=db_conn,
                chosen_ranking="Points",
                chosen_comp=chosen_comp,
                chosen_seasons=seasons_by_comp,
            )

            all_combinations = pd.MultiIndex.from_product(
                [teams, seasons_by_comp],
                names=['Club', 'Season']
            ).to_frame(index=False)

            df = pd.merge(all_combinations, df, how='left', on=['Club', 'Season'])

            filtered_df = df[df["Club"].isin(chosen_teams)]

            line_chart = alt.Chart(filtered_df).mark_line(point=True, interpolate="linear").encode(
                x=alt.X('Season:O', title='Season'),
                y=alt.Y('Points:Q', title=f'Points'),
                color=alt.Color('Club:N', legend=alt.Legend(title="Clubs", orient="right", labelLimit=2000)),
                tooltip=['Club', 'Season', "Points", "Ranking"]
            ).properties(
                title=f"Number of points over seasons - {chosen_comp}",
                height=510 if n_teams == 20 else 460 if n_teams == 18 else 600
            )

            weeks_per_season = (
                df[df["Ranking"].notnull()].groupby('Season')['Club']
                .nunique()
                .reset_index(name='NumClubs')
            )
            weeks_per_season["Weeks"] = 2*(weeks_per_season["NumClubs"]-1)
            weeks_per_season['MaxPoints'] = weeks_per_season['Weeks'] * 3
            max_points_df = weeks_per_season[['Season', 'MaxPoints']]

            max_line = alt.Chart(max_points_df).mark_line(
                strokeDash=[6, 4],
                color='gray'
            ).encode(
                x=alt.X('Season:O'),
                y=alt.Y('MaxPoints:Q'),
                tooltip=['Season', 'MaxPoints']
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
                max_line,
                line_text
            )

            st.altair_chart(chart, use_container_width=True)

            csv = df.to_csv(index=False, sep='|')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{chosen_comp.replace(' ', '_').lower()}_global_ranking_many_seasons.csv",
                mime="text/csv"
            )
