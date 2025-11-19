import altair as alt
import pandas as pd
import streamlit as st

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.commons.get_slots import get_distinct_slots
from components.queries.execute_query import execute_query
from components.commons.streamlit_widgets import (select__get_one_comp, select__get_one_season, radio__select_side,
                                                  check__filter_by_week, check__filter_by_date, check__filter_by_slot,
                                                  slider__get_one_week, date__get_one_date,
                                                  select__get_combined_ranking, select__get_combined_ranking_sorting,
                                                  multiselect__get_slots, download_button)

from utils.file_helper.reader import read_sql_file
from config import COMPETITIONS, KIND_C_CUP


@st.cache_data(show_spinner=False)
def get_combined_ranking(
        _db_conn,
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots,
):
    day_slots = [slot.split(' ')[0] for slot in slots]
    time_slots = [slot.split(' ')[1] for slot in slots]

    sql_file = read_sql_file(
        file_name="components/queries/team_stats/given_competition/combined/get_combined_ranking_one_season.sql",
        name_comp=chosen_comp,
        season=chosen_season,
        combined_ranking=combined_ranking.lower(),
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
def get_combined_ranking_enriched(
        _db_conn,
        chosen_comp,
        chosen_season,
        combined_ranking,
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
        file_name="components/queries/team_stats/given_competition/combined/get_combined_ranking_one_season_enriched.sql",
        name_comp=chosen_comp,
        season=chosen_season,
        combined_ranking=combined_ranking.lower(),
        first_week=first_week,
        last_week=last_week,
        first_date=first_date,
        last_date=last_date,
        day_slots=day_slots,
        time_slots=time_slots,
        in_side=side.lower()
    )

    return execute_query(_db_conn, sql_file)


def get_combined_ranking_one_season(db_conn):
    prefix = "combined_ranking_one_season"
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}

    chosen_comp = select__get_one_comp(prefix=prefix)

    if chosen_comp:
        seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

        chosen_season = select__get_one_season(
            prefix=prefix,
            custom_options=seasons_by_comp
        )

        if chosen_season:
            first_week = 1
            last_week = 100
            first_date = '1970-01-01'
            last_date = '2099-12-31'
            slots = []

            if comps_and_kind[chosen_comp] == KIND_C_CUP:
                sides = ["Home", "Both", "Away", "Neutral", "All"]
                # rankings = [ranking for ranking in TEAM_RANKINGS if ranking not in C_CUPS_TEAMS_EXCLUDED_RANKINGS]
            else:
                sides = ["Home", "Both", "Away"]
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

            side = radio__select_side(
                prefix=prefix,
                custom_options=sides
            )

            combined_ranking = select__get_combined_ranking(
                prefix=prefix,
                options=["", "Shots", "Passes", "Outcomes", "xG"],
            )

            if combined_ranking != "":
                df = get_chosen_combined_ranking(
                    db_conn,
                    combined_ranking,
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

                if not df.empty:
                    csv = df.to_csv(index=False, sep='|')
                    download_button(
                        prefix=prefix,
                        data=csv,
                        file_name=f"{chosen_comp.replace(' ', '_').lower()}_{chosen_season}_"
                                  f"{combined_ranking.replace(' ', '_').lower()}_simple_ranking.csv",
                        mime="text/csv"
                    )


def get_chosen_combined_ranking(
        db_conn,
        combined_ranking,
        prefix,
        chosen_comp,
        chosen_season,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots
):
    if combined_ranking == "Shots":
        df = get_combined_shots(
            db_conn,
            prefix,
            chosen_comp,
            chosen_season,
            combined_ranking,
            side,
            first_week,
            last_week,
            first_date,
            last_date,
            slots
        )
    elif combined_ranking == "Passes":
        df = get_combined_passes(
            db_conn,
            prefix,
            chosen_comp,
            chosen_season,
            combined_ranking,
            side,
            first_week,
            last_week,
            first_date,
            last_date,
            slots
        )
    elif combined_ranking == "Outcomes":
        df = get_combined_outcomes(
            db_conn,
            prefix,
            chosen_comp,
            chosen_season,
            combined_ranking,
            side,
            first_week,
            last_week,
            first_date,
            last_date,
            slots
        )
    elif combined_ranking == "xG":
        df = get_combined_xgs(
            db_conn,
            prefix,
            chosen_comp,
            chosen_season,
            combined_ranking,
            side,
            first_week,
            last_week,
            first_date,
            last_date,
            slots
        )

    else:
        df = pd.DataFrame()

    return df


def get_combined_shots(
        db_conn,
        prefix,
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots
):
    df = get_combined_ranking(
        db_conn,
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots
    )

    df['Shots Against'] = -df['Shots Against']
    df['Shots on Target Against'] = -df['Shots on Target Against']
    df['Goals Against'] = -df['Goals Against']
    df['Ranking'] = df['Ranking'].astype(int)

    chosen_sorting = select__get_combined_ranking_sorting(
        prefix=prefix,
        suffix="shots",
        options=[
            "Ranking",
            "Shots For", "Shots on Target For",
            "Shots Against", "Shots on Target Against",
            "Goals For", "Goals Against"
        ]
    )

    club_order = df.sort_values(chosen_sorting, ascending=chosen_sorting == "Ranking")['Club'].tolist()

    df_melted = df.melt(
        id_vars=['Club', 'Ranking'],
        value_vars=[
            'Shots For', 'Shots Against',
            'Shots on Target For', 'Shots on Target Against',
            'Goals For', 'Goals Against'
        ],
        var_name='Kind',
        value_name='Shots'
    )

    df_melted['Shots_abs'] = df_melted['Shots'].abs()

    df_melted['Category'] = df_melted['Kind'].apply(
        lambda x: 'Shots' if 'Shots' in x and 'on Target' not in x else
        'Shots on Target' if 'on Target' in x else
        'Goals'
    )
    df_melted['Side'] = df_melted['Kind'].apply(lambda x: 'For' if 'For' in x else 'Against')

    bars_data = df_melted[df_melted['Category'] != 'Goals']
    goals_data = df_melted[df_melted['Category'] == 'Goals']

    bars = alt.Chart(bars_data).mark_bar().encode(
        x=alt.X(shorthand='Shots:Q'),
        y=alt.Y(shorthand='Club:N', sort=club_order),
        color=alt.Color(
            'Category:N',
            scale=alt.Scale(
                domain=['Shots', 'Shots on Target', 'Goals'],
                range=['steelblue', 'orange', 'firebrick']
            )
        ),
        tooltip=['Club', 'Ranking', 'Category', alt.Tooltip('Shots_abs:Q', title='Shots')],
        order=alt.Order('Category', sort='descending')
    )

    goals = alt.Chart(goals_data).mark_bar().encode(
        x=alt.X(shorthand='Shots:Q'),
        y=alt.Y(shorthand='Club:N', sort=club_order),
        color=alt.Color('Category:N', scale=alt.Scale(scheme='tableau10')),
        tooltip=['Club', 'Ranking', 'Category', alt.Tooltip('Shots_abs:Q', title='Shots')],
        order=alt.Order('Category', sort='descending')
    )

    rule = alt.Chart(df_melted).mark_rule(color='white', strokeWidth=3).encode(
        x=alt.datum(0)
    )

    final_chart = (bars + goals + rule).resolve_scale(
        y='shared'
    ).properties(
        title="Shots, Shots on Target, Goals — For vs Against",
        width=600
    )

    st.altair_chart(final_chart, use_container_width=True)

    return df


def get_combined_passes(
        db_conn,
        prefix,
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots
):
    df = get_combined_ranking(
        db_conn,
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots
    )

    df['Ranking'] = df['Ranking'].astype(int)
    df["Failed Passes"] = df["Att Passes"] - df["Succ Passes"]

    chosen_sorting = select__get_combined_ranking_sorting(
        prefix=prefix,
        suffix="passes",
        options=["Ranking", "Succ Passes", "Att Passes", "Total Passes", "Succ Passes Rate"]
    )

    club_order = df.sort_values(chosen_sorting, ascending=chosen_sorting == "Ranking")['Club'].tolist()

    df_melted = df.melt(
        id_vars=["Club", "Att Passes"],
        value_vars=["Succ Passes", "Failed Passes"],
        var_name="Kind",
        value_name="Count"
    )

    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X(shorthand='Count:Q', title="Number of passes"),
        y=alt.Y(shorthand='Club:N', sort=club_order),
        color=alt.Color(
            'Kind:N',
            title="Passes",
            scale=alt.Scale(
                domain=['Succ Passes', 'Failed Passes'],
                range=['steelblue', 'orange']
            )
        ),
        order=alt.Order("Kind:N", sort='descending'),
        tooltip=['Club:N', 'Att Passes:Q', 'Kind:N', 'Count:Q']
    )

    rate = alt.Chart(df).mark_text(
        align='left',
        baseline='middle',
        fontSize=12,
        dx=4,
        color='black'
    ).encode(
        y=alt.Y(shorthand='Club:N', sort=club_order),
        x=alt.X(shorthand='Att Passes:Q', title="Number of passes"),
        text=alt.Text('Succ Passes Rate:Q', format='.0%'),
        tooltip=["Club:N", "Att Passes:Q", alt.Text('Succ Passes Rate:Q', format='.0%')]
    )

    chart = alt.layer(chart, rate).properties(
        title="Successful vs Attempted Passes",
        width=600
    )

    st.altair_chart(chart, use_container_width=True)

    return df


def get_combined_outcomes(
        db_conn,
        prefix,
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots
):
    df = get_combined_ranking(
        db_conn,
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots
    )

    df['Ranking'] = df['Ranking'].astype(int)

    chosen_sorting = select__get_combined_ranking_sorting(
        prefix=prefix,
        suffix="outcomes",
        options=["Ranking", "Wins", "Draws", "Loses"],
        index=None
    )

    club_order = df.sort_values(chosen_sorting, ascending=chosen_sorting == "Ranking")['Club'].tolist()

    df_melted = df.melt(
        id_vars=['Club', 'Ranking'],
        value_vars=['Wins', 'Draws', 'Loses'],
        var_name='Outcome',
        value_name='Count'
    )

    if chosen_sorting == "Draws":
        draws_order = {'Draws': 0, 'Wins': 1, 'Loses': 2}
        df_melted['OutcomeOrder'] = df_melted['Outcome'].map(draws_order)
    else:
        outcome_order = {'Wins': 0, 'Draws': 1, 'Loses': 2}
        df_melted['OutcomeOrder'] = df_melted['Outcome'].map(outcome_order)

    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X(shorthand='Count:Q', stack='zero'),
        y=alt.Y(shorthand='Club:N', sort=club_order),
        color=alt.Color(
            shorthand='Outcome:N',
            scale=alt.Scale(
                domain=['Wins', 'Draws', 'Loses'],
                range=['steelblue', 'orange', 'firebrick'],
            )
        ),
        order=alt.Order(
            'OutcomeOrder:N',
            sort='ascending'
        ),
        tooltip=["Club", "Outcome", "Count", "Ranking"]
    )

    st.altair_chart(chart, use_container_width=True)

    return df


def get_combined_xgs(
        db_conn,
        prefix,
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots
):
    df = get_combined_ranking_enriched(
        db_conn,
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        slots
    )

    df["xG Against (fbref)"] = -df["xG Against (fbref)"]
    df["xG Against (understat)"] = -df["xG Against (understat)"]
    df["Goals Against"] = -df["Goals Against"]
    df["Ranking"] = df["Ranking"].astype(int)

    chosen_sorting = select__get_combined_ranking_sorting(
        prefix=prefix,
        suffix="xgs",
        options=[
            "Ranking",
            "Goals For",
            "Goals Against",
            "xG For (fbref)",
            "xG For (understat)",
            "xG Against (fbref)",
            "xG Against (understat)"
        ]
    )

    club_order = df.sort_values(chosen_sorting, ascending=chosen_sorting == "Ranking")['Club'].tolist()

    df_melted = df.melt(
        id_vars=["Club", "Ranking"],
        value_vars=[
            "xG For (fbref)",
            "xG For (understat)",
            "xG Against (fbref)",
            "xG Against (understat)",
            "Goals For",
            "Goals Against"
        ],
        var_name="Side",
        value_name="Value"
    )

    df_melted['Value_abs'] = df_melted['Value'].abs()
    df_melted['Category'] = df_melted['Side'].apply(
        lambda x: 'xG (fbref)' if 'fbref' in x else 'xG (understat)' if 'understat' in x else 'Goals'
    )
    df_melted['Side'] = df_melted['Side'].apply(lambda x: 'For' if 'For' in x else 'Against')

    xg_fbref_data = df_melted[df_melted['Category'] == 'xG (fbref)']
    xg_understat_data = df_melted[df_melted['Category'] == 'xG (understat)']
    goals_data = df_melted[df_melted['Category'] == 'Goals']

    goals = alt.Chart(goals_data).mark_bar().encode(
        x=alt.X(shorthand='Value:Q'),
        y=alt.Y(shorthand='Club:N', sort=club_order),
        color=alt.Color(
            shorthand='Side:N',
            scale=alt.Scale(
                domain=["For", "Against"],
                range=['steelblue', 'orange']
            ),
            legend=alt.Legend(title="Goals")
        ),
        tooltip=["Club", "Category", "Side", alt.Tooltip('Value_abs:Q', title='Goals'), "Ranking"]
    )

    expected_fbref = alt.Chart(xg_fbref_data).mark_tick(thickness=4, size=20).encode(
        x=alt.X(shorthand='Value:Q'),
        y=alt.Y(shorthand='Club:N', sort=club_order),
        color=alt.Color(
            shorthand='Category:N',
            scale=alt.Scale(
                domain=["xG (fbref)", "xG (understat)"],
                range=['green', 'black']
            ),
            legend=alt.Legend(title="xG Source")
        ),
        tooltip=["Club", "Category", "Side", alt.Tooltip('Value_abs:Q', title='xG'), "Ranking"]
    )

    expected_understat = alt.Chart(xg_understat_data).mark_tick(thickness=4, size=20).encode(
        x=alt.X(shorthand='Value:Q'),
        y=alt.Y(shorthand='Club:N', sort=club_order),
        color=alt.Color(
            shorthand='Category:N',
            scale=alt.Scale(
                domain=["xG (fbref)", "xG (understat)"],
                range=['green', 'black']
            ),
            legend=None
        ),
        tooltip=["Club", "Category", "Side", alt.Tooltip('Value_abs:Q', title='xG'), "Ranking"]
    )

    rule = alt.Chart(df_melted).mark_rule(color='white', strokeWidth=3).encode(
        x=alt.datum(0)
    )

    final_chart = (goals + expected_fbref + expected_understat + rule).resolve_scale(
        y='shared'
    ).resolve_scale(
        color='independent',
        y='shared'
    ).properties(
        title="xG — For vs Against",
        width=600
    )

    st.altair_chart(final_chart, use_container_width=True)

    return df
