from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_slots import get_distinct_slots
from components.commons.streamlit_widgets import *
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file


# @st.cache_data(show_spinner=False)
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
    group_by_club,
    group_by_competition,
    group_by_season,
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
        group_by_club=group_by_club,
        group_by_competition=group_by_competition,
        group_by_season=group_by_season,
    )

    df = execute_query(_db_conn, sql_file)
    df.index = range(1, len(df) + 1)

    return df


def get_all_coaches_stats(db_conn):
    prefix="coach_stats"
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
                custom_options=all_seasons
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
                            label="Last week",
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
                            default_value=last_date
                        )

                filter_slots = check__filter_by_slot(prefix=prefix)

                if filter_slots:
                    col, _ = st.columns(2)

                    with col:
                        slots = multiselect__get_slots(
                            prefix=prefix,
                            label="Slot",
                            options=get_distinct_slots(db_conn, chosen_comp, chosen_season)
                        )

                chosen_side = radio__select_side(
                    prefix=prefix,
                    label="Side"
                )

                group_by_club = check__group_by_club(prefix=prefix)

                if chosen_comp.lower() == 'all':
                    group_by_competition = check__group_by_competition(prefix=prefix)
                else:
                    group_by_competition = False

                group_by_season = check__group_by_season(prefix=prefix)

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
            group_by_club,
            group_by_competition,
            group_by_season
        )

        st.write(coaches_stats)
