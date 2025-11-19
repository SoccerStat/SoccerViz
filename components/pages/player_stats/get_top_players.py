import streamlit as st

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_all_season_schemas
from components.commons.get_slots import get_distinct_slots
from components.commons.set_titles import set_sub_sub_title
from components.commons.streamlit_widgets import (select__get_one_comp, select__get_one_season, radio__select_side,
                                                  check__filter_by_week, check__filter_by_date, check__filter_by_slot,
                                                  slider__get_one_week, date__get_one_date, multiselect__get_slots,
                                                  check__group_by_club, check__group_by_competition, check__group_by_season)
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file


# @st.cache_data(show_spinner=False)
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
        group_by_club,
        group_by_competition,
        group_by_season,
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
        group_by_club=group_by_club,
        group_by_competition=group_by_competition,
        group_by_season=group_by_season
    )

    df = execute_query(_db_conn, sql_file)
    df.index = range(1, len(df) + 1)

    return df


def get_top_players(db_conn):
    prefix = "top_players"
    col, _ = st.columns(2)

    with col:
        chosen_comp = select__get_one_comp(
            prefix=prefix,
            all_comps=True
        )

        if chosen_comp:
            all_seasons = [season_schema[7:] for season_schema in get_all_season_schemas(db_conn)]

            chosen_season = select__get_one_season(
                db_conn=db_conn,
                prefix=prefix,
                custom_options=all_seasons,
            )

            if chosen_season:
                first_week = 1
                last_week = 100
                first_date = '1970-01-01'
                last_date = '2099-12-31'
                slots = []

                all_teams_of_comp_of_season = get_teams_by_comp_by_season(db_conn, chosen_comp, [chosen_season])
                n_teams = len(all_teams_of_comp_of_season)

                filter_weeks = check__filter_by_week(prefix=prefix)

                if filter_weeks:
                    col1, col2 = st.columns(2)
                    max_week = 2 * (n_teams - 1)

                    with col1:
                        first_week = slider__get_one_week(
                            prefix=prefix,
                            suffix="first_week",
                            label="First week",
                            min_value=1,
                            max_value=max_week,
                            default_value=1
                        )

                    if first_week == max_week:
                        last_week = max_week
                    else:
                        with col2:
                            last_week = slider__get_one_week(
                                prefix=prefix,
                                suffix="last_week",
                                min_value=first_week,
                                max_value=max_week,
                                default_value=first_week
                            )

                # rankings = TEAM_RANKINGS

                filter_dates = check__filter_by_date(prefix=prefix)

                if filter_dates:
                    col1, col2 = st.columns(2)

                    with col1:
                        first_date = date__get_one_date(
                            prefix=prefix,
                            suffix="first_date",
                            label="First date"
                        )

                    with col2:
                        last_date = date__get_one_date(
                            prefix=prefix,
                            suffix="last_date",
                            label="Last date",
                            default_value=first_date
                        )

                filter_slots = check__filter_by_slot(prefix=prefix)

                if filter_slots:
                    col, _ = st.columns(2)

                    with col:
                        slots = multiselect__get_slots(
                            prefix=prefix,
                            options=get_distinct_slots(db_conn, chosen_comp, chosen_season)
                        )

                chosen_side = radio__select_side(prefix=prefix)

                group_by_club = check__group_by_club(prefix=prefix)

                if chosen_comp.lower() == 'all':
                    group_by_competition = check__group_by_competition(prefix=prefix)
                else:
                    group_by_competition = False

                group_by_season = check__group_by_season(prefix=prefix)

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
            slots,
            group_by_club,
            group_by_competition,
            group_by_season
        )

        top_assists = get_top_players_by_stat(
            db_conn,
            'Assists',
            chosen_comp,
            chosen_season,
            chosen_side,
            first_week,
            last_week,
            first_date,
            last_date,
            slots,
            group_by_club,
            group_by_competition,
            group_by_season
        )
        top_decisive = top_scorers.merge(top_assists, how="inner", on="Player", suffixes=('_scorers', '_assists'))
        top_decisive['M'] = top_decisive['M_scorers']
        top_decisive['Club'] = top_decisive['Club_scorers']
        top_decisive['G+A'] = top_decisive[['Goals', 'Assists']].sum(axis=1, skipna=True)
        top_decisive = top_decisive[['Player', 'Club', 'M', 'G+A']].sort_values(by=['G+A', 'M'], ascending=[False, True])
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
