import streamlit as st
import altair as alt

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file
from config import TEAM_RANKINGS, COMPETITIONS, C_CUPS_TEAMS_EXCLUDED_RANKINGS, KIND_C_CUP


@st.cache_data(show_spinner=False)
def get_one_ranking(
            _db_conn,
        chosen_comp,
        chosen_season,
        chosen_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date
):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/single/get_single_ranking_one_season.sql",
        name_comp=chosen_comp,
        season=chosen_season,
        ranking=chosen_ranking,
        first_week=first_week,
        last_week=last_week,
        first_date=first_date,
        last_date=last_date,
        in_side=side.lower()
    )

    return execute_query(_db_conn, sql_file)

def get_single_ranking_one_season(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    comps = list(comps_and_kind.keys())

    chosen_comp = st.selectbox(
        key="single_ranking_one_season__comp",
        label="Choose competition...",
        options=comps
    )

    seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

    chosen_season = st.selectbox(
        key="single_ranking_one_season__season",
        label="Choose season...",
        options=[""] + seasons_by_comp
    )

    if chosen_season:

        first_week = 1
        last_week = 100
        first_date = '1970-01-01'
        last_date = '2099-12-31'

        if comps_and_kind[chosen_comp] == KIND_C_CUP:
            rankings = [ranking for ranking in TEAM_RANKINGS if ranking not in C_CUPS_TEAMS_EXCLUDED_RANKINGS]
        else:
            all_teams_of_comp_of_season = get_teams_by_comp_by_season(db_conn, chosen_comp, [chosen_season])
            n_teams = len(all_teams_of_comp_of_season)

            filter_weeks = st.checkbox(
                key='single_ranking_one_season__filter_weeks',
                label='Filter by week'
            )

            if filter_weeks:

                col1, col2 = st.columns(2)
                max_week = 2 * (n_teams - 1)

                with col1:
                    first_week = st.slider(
                        key='single_ranking_one_season__first_week',
                        label="First week",
                        min_value=1,
                        max_value=max_week,
                        value=1
                    )

                if first_week == max_week:
                    last_week = max_week
                else:

                    with col2:
                        last_week = st.slider(
                            key='single_ranking_one_season__last_week',
                            label="Last week",
                            min_value=first_week,
                            max_value=max_week,
                            value=first_week
                        )

            rankings = TEAM_RANKINGS

        filter_dates = st.checkbox(
            key='single_ranking_one_season__filter_dates',
            label='Filter by date'
        )

        if filter_dates:

            col1, col2 = st.columns(2)

            with col1:
                first_date = st.date_input(
                    key='single_ranking_one_season__first_date',
                    label="First date",
                    value="today"
                )

            with col2:
                last_date = st.date_input(
                    key='single_ranking_one_season__last_date',
                    label="Last date",
                    value=first_date
                )

        sides = ["Home", "Both", "Away", "Neutral", "All"] if comps_and_kind[chosen_comp] == KIND_C_CUP else ["Home", "Both", "Away"]
        side = st.radio(
            key='single_ranking_one_season__side',
            label="Side",
            options=sides,
            horizontal=True,
            label_visibility="collapsed",
            index=1
        )

        chosen_ranking = st.selectbox(
            key="single_ranking_one_season__ranking",
            label="Choose ranking...",
            options=[""] + rankings,
            index=0
        )

        if chosen_ranking != "":
            df = get_one_ranking(
                db_conn,
                chosen_comp,
                chosen_season,
                chosen_ranking,
                side,
                first_week,
                last_week,
                first_date,
                last_date
            )

            ordered_clubs = df.sort_values(by=f"{chosen_ranking} Ranking", ascending=True)['Club'].tolist()

            if chosen_ranking == "Points":
                tooltip = ["Club", chosen_ranking, "Global Ranking"]
            else:
                tooltip = ["Club", chosen_ranking, "Global Ranking", f"{chosen_ranking} Ranking"]

            bars = alt.Chart(df).mark_bar().encode(
                x=chosen_ranking,
                y=alt.Y('Club', sort=ordered_clubs),
                tooltip=tooltip
            )

            text_pos = alt.Chart(df).mark_text(
                align='left',
                baseline='middle',
                dx=3
            ).encode(
                x=chosen_ranking,
                y=alt.Y('Club', sort=ordered_clubs),
                text=chosen_ranking
            ).transform_filter(
                alt.datum[chosen_ranking] >= 0
            )

            text_neg = alt.Chart(df).mark_text(
                align='right',
                baseline='middle',
                dx=-3
            ).encode(
                x=chosen_ranking,
                y=alt.Y('Club', sort=ordered_clubs),
                text=chosen_ranking
            ).transform_filter(
                alt.datum[chosen_ranking] < 0
            )

            chart = alt.layer(bars, text_pos, text_neg)

            st.altair_chart(chart, use_container_width=True)

            csv = df.to_csv(index=False, sep='|')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{chosen_comp.replace(' ', '_').lower()}_{chosen_season}_{chosen_ranking.replace(' ', '_').lower()}_simple_ranking.csv",
                mime="text/csv"
            )