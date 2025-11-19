import streamlit as st
import altair as alt

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.commons.set_titles import set_sub_sub_title, set_sub_sub_sub_title
from components.commons.get_slots import get_distinct_slots
from components.commons.streamlit_widgets import (select__get_one_ranking, select__get_one_comp, select__get_one_season,
                                                  check__filter_by_week, check__filter_by_date, check__filter_by_slot,
                                                  slider__get_one_week, date__get_one_date, multiselect__get_slots,
                                                  radio__select_side, radio__generic, slider__generic,
                                                  download_button)
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file
from config import TEAM_RANKINGS, COMPETITIONS, C_CUPS_TEAMS_EXCLUDED_RANKINGS, KIND_C_CUP


@st.cache_data(show_spinner=False)
def get_players_age_by_team(_db_conn, chosen_comp, chosen_season):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/given_competition/single/get_players_age_by_team.sql",
        name_comp=chosen_comp,
        season=chosen_season,
        r=2
    )

    return execute_query(_db_conn, sql_file)


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
        last_date,
        slots
):
    day_slots = [slot.split(' ')[0] for slot in slots]
    time_slots = [slot.split(' ')[1] for slot in slots]

    sql_file = read_sql_file(
        file_name="components/queries/team_stats/given_competition/single/get_single_ranking_one_season.sql",
        name_comp=chosen_comp,
        season=chosen_season,
        ranking=chosen_ranking,
        first_week=first_week,
        last_week=last_week,
        first_date=first_date,
        last_date=last_date,
        day_slots=day_slots,
        time_slots=time_slots,
        in_side=side.lower()
    )

    return execute_query(_db_conn, sql_file)


@st.cache_data(show_spinner=False)
def get_global_ranking(
        _db_conn,
        chosen_comp,
        chosen_season,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots
):
    day_slots = [slot.split(' ')[0] for slot in slots]
    time_slots = [slot.split(' ')[1] for slot in slots]

    sql_file = read_sql_file(
        file_name="components/queries/team_stats/given_competition/single/get_overall_ranking.sql",
        name_comp=chosen_comp,
        season=chosen_season,
        first_week=first_week,
        last_week=last_week,
        first_date=first_date,
        last_date=last_date,
        day_slots=day_slots,
        time_slots=time_slots,
        in_side=side.lower()
    )

    return execute_query(_db_conn, sql_file)


def get_players_age_ranking(db_conn, prefix, chosen_comp, chosen_season):
    players_stats_and_age = get_players_age_by_team(db_conn, chosen_comp, chosen_season)

    col, _ = st.columns(2)
    with col:
        chosen_slider = radio__generic(
            prefix=prefix,
            suffix="slider",
            label="Slider",
            default_index=0,
            options=["Minutes", "Matches"]
        )

        chosen_rate = slider__generic(
            prefix=prefix,
            suffix="rate_players",
            label="Minimum % played",
            min_value=0,
            max_value=100,
            default_value=0
        )

        if chosen_slider == "Minutes":
            filtered_players = players_stats_and_age[players_stats_and_age["% of minutes played"] >= chosen_rate / 100]
        else:
            filtered_players = players_stats_and_age[players_stats_and_age["% of matches played"] >= chosen_rate / 100]

    avg_age_of_squads = (
        filtered_players
        .groupby("Club", as_index=False)
        .agg(
            Age=("Age", "mean"),
            Count=("Age", "count")
        )
        .sort_values("Age", ascending=True)
        .reset_index(drop=True)
    )

    avg_age_of_squads["Age"] = avg_age_of_squads["Age"].apply(
        lambda x: f"{int(x)} years, {int((x % 1) * 365)} days"
    )
    avg_age_of_squads.rename(columns={'Count': 'Number of players'}, inplace=True)
    avg_age_of_squads.index = range(1, len(avg_age_of_squads) + 1)

    st.dataframe(avg_age_of_squads)


def get_single_stat_ranking(
        db_conn,
        prefix,
        chosen_comp,
        chosen_season,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots,
        rankings,
):
    chosen_ranking = select__get_one_ranking(
        prefix=prefix,
        options=rankings
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
            last_date,
            slots
        )

        ordered_clubs = df.sort_values(by=f"{chosen_ranking} Ranking", ascending=True)['Club'].tolist()

        if chosen_ranking == "Points":
            tooltip = ["Club", chosen_ranking, "Global Ranking"]
        else:
            tooltip = ["Club", chosen_ranking, "Global Ranking", f"{chosen_ranking} Ranking"]

        bars = alt.Chart(df).mark_bar().encode(
            x=chosen_ranking,
            y=alt.Y(shorthand='Club', sort=ordered_clubs),
            tooltip=tooltip
        )

        text_pos = alt.Chart(df).mark_text(
            align='left',
            baseline='middle',
            dx=3
        ).encode(
            x=chosen_ranking,
            y=alt.Y(shorthand='Club', sort=ordered_clubs),
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
            y=alt.Y(shorthand='Club', sort=ordered_clubs),
            text=chosen_ranking
        ).transform_filter(
            alt.datum[chosen_ranking] < 0
        )

        chart = alt.layer(bars, text_pos, text_neg)

        st.altair_chart(chart, use_container_width=True)

        csv = df.to_csv(index=False, sep='|')
        download_button(
            prefix=prefix,
            suffix="single_ranking",
            data=csv,
            file_name=f"{chosen_comp.replace(' ', '_').lower()}_{chosen_season}_"
                      f"{chosen_ranking.replace(' ', '_').lower()}_simple_ranking.csv",
            mime="text/csv"
        )


def get_overall_ranking(
        db_conn,
        prefix,
        chosen_comp,
        chosen_season,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots,
):
    df = get_global_ranking(
        db_conn,
        chosen_comp,
        chosen_season,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots
    )

    st.dataframe(df.set_index("Ranking"))

    csv = df.to_csv(index=False, sep='|')
    download_button(
        prefix=prefix,
        suffix="overall_ranking",
        data=csv,
        file_name=f"{chosen_comp.replace(' ', '_').lower()}_{chosen_season}_"
                  "overall_ranking.csv",
        mime="text/csv"
    )


def get_rankings(db_conn, prefix, chosen_comp, chosen_season, comps_and_kind):
    first_week = 1
    last_week = 100
    first_date = '1970-01-01'
    last_date = '2099-12-31'
    slots = []

    if comps_and_kind[chosen_comp] == KIND_C_CUP:
        rankings = [ranking for ranking in TEAM_RANKINGS if ranking not in C_CUPS_TEAMS_EXCLUDED_RANKINGS]
    else:
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

        rankings = TEAM_RANKINGS

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
            slots = multiselect__get_slots(prefix=prefix, options=get_distinct_slots(db_conn, chosen_comp, chosen_season))

    sides = (
        ["Home", "Both", "Away", "Neutral", "All"]
        if comps_and_kind[chosen_comp] == KIND_C_CUP
        else ["Home", "Both", "Away"]
    )
    side = radio__select_side(
        prefix=prefix,
        custom_options=sides
    )

    set_sub_sub_title("Overall ranking")
    get_overall_ranking(
        db_conn,
        prefix,
        chosen_comp,
        chosen_season,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots
    )

    set_sub_sub_sub_title("Single Stat ranking")
    get_single_stat_ranking(
        db_conn,
        prefix,
        chosen_comp,
        chosen_season,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots,
        rankings
    )


def get_single_stat_and_squad_age_rankings_one_season(db_conn):
    prefix = "single_ranking_one_season"
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}

    chosen_comp = select__get_one_comp(prefix=prefix)

    if chosen_comp:
        seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

        chosen_season = select__get_one_season(
            prefix=prefix,
            custom_options=seasons_by_comp
        )

        if chosen_season:
            set_sub_sub_title("Rankings")
            get_rankings(db_conn, prefix, chosen_comp, chosen_season, comps_and_kind)

            set_sub_sub_title("Average age of teams' squad")
            get_players_age_ranking(db_conn, prefix, chosen_comp, chosen_season)
