import streamlit as st

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_all_season_schemas
from components.commons.get_slots import get_distinct_slots
from components.commons.set_titles import set_sub_sub_title
from components.queries.execute_query import execute_query
from config import COMPETITIONS

from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_top_players_by_stat(
        _db_conn,
        in_ranking,
        chosen_comp,
        chosen_season,
        chosen_side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots,
):
    sql_file = read_sql_file(
        file_name="components/queries/player_stats/top_players.sql",
        ranking=in_ranking,
        comp=chosen_comp,
        season=chosen_season,
        side=chosen_side.lower(),
        first_week=first_week,
        last_week=last_week,
        first_date=first_date,
        last_date=last_date,
        slots=slots,
    )

    df = execute_query(_db_conn, sql_file)
    df.index = range(1, len(df) + 1)

    return df


def get_top_players(db_conn):
    col, _ = st.columns(2)

    with col:
        chosen_comp = st.selectbox(
            key="top_players__comp",
            label="Choose one competition...",
            options=[""] + ["All"] + [comp["label"] for _, comp in COMPETITIONS.items()]
        )

        if chosen_comp:
            all_seasons = [season_schema[7:] for season_schema in get_all_season_schemas(db_conn)]

            chosen_season = st.selectbox(
                key="top_players__season",
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
                    key="top_players__side",
                    label="Side",
                    options=["Home", "Both", "Away"],
                    horizontal=True,
                    label_visibility="collapsed",
                    index=1
                )

                # TODO: ajouter filtres week / date / slots

    if chosen_comp and chosen_season:
        goals, decisive, assists = st.columns(3)
        top_scorers = get_top_players_by_stat(
            db_conn,
            'Goals',
            chosen_comp,
            chosen_season,
            chosen_side,
            first_week,
            last_week,
            first_date,
            last_date,
            slots
        )
        top_assists= get_top_players_by_stat(
            db_conn,
            'Assists',
            chosen_comp,
            chosen_season,
            chosen_side,
            first_week,
            last_week,
            first_date,
            last_date,
            slots
        )
        top_decisive = top_scorers.merge(top_assists, how="inner", on="Player", suffixes=('_scorers', '_assists'))
        top_decisive['Matches'] = top_decisive['Matches_scorers']
        top_decisive['G+A'] = top_decisive[['Goals', 'Assists']].sum(axis=1, skipna=True)
        top_decisive = top_decisive[['Player', 'Matches', 'G+A']].sort_values(by=['G+A', 'Matches'], ascending=[False, True])
        top_decisive.index = range(1, len(top_decisive) + 1)

        with goals:
            set_sub_sub_title("Goals")
            st.write(top_scorers)

        with decisive:
            set_sub_sub_title("G + A")
            st.write(top_decisive)

        with assists:
            set_sub_sub_title("Assists")
            st.write(top_assists)