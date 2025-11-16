import streamlit as st

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_all_season_schemas
from components.commons.get_slots import get_distinct_slots
from components.queries.execute_query import execute_query
from config import COMPETITIONS

from utils.file_helper.reader import read_sql_file


def get_coaches_stats_by_comp_by_season(
    _db_conn,
    chosen_comp,
    chosen_season,
    chosen_side,
    first_week,
    last_week,
    first_date,
    last_date,
    slots,
    group_clubs,
    group_competitions,
):
    sql_file = read_sql_file(
        file_name="components/queries/coaches_stats/coaches_stats.sql",
        comp=chosen_comp,
        season=chosen_season,
        side=chosen_side.lower(),
        first_week=first_week,
        last_week=last_week,
        first_date=first_date,
        last_date=last_date,
        slots=slots,
        group_clubs=group_clubs,
        group_competitions=group_competitions,
    )

    df = execute_query(_db_conn, sql_file)
    df.index = range(1, len(df) + 1)

    return df


def get_coaches_stats(db_conn):
    col, _ = st.columns(2)

    with col:
        chosen_comp = st.selectbox(
            key="coaches_stats__comp",
            label="Choose one competition...",
            options=[""] + ["All"] + [comp["label"] for _, comp in COMPETITIONS.items()]
        )

        if chosen_comp:
            all_seasons = [season_schema[7:] for season_schema in get_all_season_schemas(db_conn)]

            chosen_season = st.selectbox(
                key="coaches_stats__season",
                label="Choose one season...",
                options=[""] + all_seasons
            )

            if chosen_season:
                first_week = 1
                last_week = 100
                first_date = '1970-01-01'
                last_date = '2099-12-31'
                slots = []

                all_teams_of_comp_of_season = get_teams_by_comp_by_season(db_conn, chosen_comp, [chosen_season])
                n_teams = len(all_teams_of_comp_of_season)

                filter_weeks = st.checkbox(
                    key='combined_ranking_one_season__filter_weeks',
                    label='Filter by week'
                )

                if filter_weeks:
                    col1, col2 = st.columns(2)
                    max_week = 2 * (n_teams - 1)

                    with col1:
                        first_week = st.slider(
                            key='combined_ranking_one_season__first_week',
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
                                key='combined_ranking_one_season__last_week',
                                label="Last week",
                                min_value=first_week,
                                max_value=max_week,
                                value=first_week
                            )

                # rankings = TEAM_RANKINGS

                filter_dates = st.checkbox(
                    key='combined_ranking_one_season__filter_dates',
                    label='Filter by date'
                )

                if filter_dates:
                    col1, col2 = st.columns(2)

                    with col1:
                        first_date = st.date_input(
                            key='combined_ranking_one_season__first_date',
                            label="First date",
                            value="today"
                        )

                    with col2:
                        last_date = st.date_input(
                            key='combined_ranking_one_season__last_date',
                            label="Last date",
                            value=first_date
                        )

                filter_slots = st.checkbox(
                    key='combined_ranking_one_season__filter_slots',
                    label="Filter by slot"
                )

                if filter_slots:
                    col, _ = st.columns(2)

                    with col:
                        slots = st.multiselect(
                            key="combined_ranking_one_season__slots",
                            label="Slot",
                            options=get_distinct_slots(db_conn, chosen_comp, chosen_season)
                        )
                chosen_side = st.radio(
                    key="coaches_stats__side",
                    label="Side",
                    options=["Home", "Both", "Away"],
                    horizontal=True,
                    label_visibility="collapsed",
                    index=1
                )

                group_clubs = st.checkbox(
                    key="coaches_stats__group_clubs",
                    label="Group clubs",
                    value=False
                )

                if chosen_comp == 'ALL':
                    group_competitions = st.checkbox(
                        key="coaches_stats__group_competitions",
                        label="Group clubs",
                        value=False
                    )
                else:
                    group_competitions = False

    if chosen_comp and chosen_season:
        coaches_stats = get_coaches_stats_by_comp_by_season(
            db_conn,
            chosen_comp,
            chosen_season,
            chosen_side,
            first_week,
            last_week,
            first_date,
            last_date,
            slots,
            group_clubs,
            group_competitions
        )

        st.write(coaches_stats)
