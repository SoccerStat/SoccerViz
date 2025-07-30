import streamlit as st
import altair as alt
import pandas as pd

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file
from config import TEAM_RANKINGS, COMPETITIONS, C_CUPS_TEAMS_EXCLUDED_RANKINGS, KIND_C_CUP


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
        last_date
):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/get_combined_ranking_one_season.sql",
        name_comp=chosen_comp,
        season=chosen_season,
        combined_ranking=combined_ranking.lower(),
        first_week=first_week,
        last_week=last_week,
        first_date=first_date,
        last_date=last_date,
        in_side=side.lower()
    )

    return execute_query(_db_conn, sql_file)

def get_combined_ranking_one_season(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    comps = list(comps_and_kind.keys())

    chosen_comp = st.selectbox(
        key="combined_ranking_one_season__comp",
        label="Choose competition...",
        options=comps
    )

    seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

    chosen_season = st.selectbox(
        key="combined_ranking_one_season__season",
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

            rankings = TEAM_RANKINGS

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

        sides = ["Home", "Both", "Away", "Neutral", "All"] if comps_and_kind[chosen_comp] == KIND_C_CUP else ["Home", "Both", "Away"]

        side = st.radio(
            key='combined_ranking_one_season__side',
            label="Side",
            options=sides,
            horizontal=True,
            label_visibility="collapsed",
            index=1
        )

        combined_ranking = st.selectbox(
            key="combined_ranking_one_season__ranking",
            label="Choose combined ranking...",
            options=["", "Shots", "Passes", "Outcomes", "xG"],
            index=0
        )

        if combined_ranking != "":

            if combined_ranking == "Shots":
                df = get_combined_shots(db_conn,chosen_comp, chosen_season, combined_ranking, side, first_week, last_week, first_date, last_date)
            elif combined_ranking == "Passes":
                df = get_combined_passes(db_conn,chosen_comp, chosen_season, combined_ranking, side, first_week, last_week, first_date, last_date)
            elif combined_ranking == "Outcomes":
                df = get_combined_outcomes(db_conn,chosen_comp, chosen_season, combined_ranking, side, first_week, last_week, first_date, last_date)
            elif combined_ranking == "xG":
                df = get_combined_xgs(db_conn,chosen_comp, chosen_season, combined_ranking, side, first_week, last_week, first_date, last_date)
            else:
                df = pd.DataFrame()

            if not df.empty:
                csv = df.to_csv(index=False, sep='|')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"{chosen_comp.replace(' ', '_').lower()}_{chosen_season}_{combined_ranking.replace(' ', '_').lower()}_simple_ranking.csv",
                    mime="text/csv"
                )

def get_combined_shots(
        db_conn,
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date
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
        last_date
    )

    df['Shots Against'] = -df['Shots Against']
    df['Shots on Target Against'] = -df['Shots on Target Against']
    df['Goals Against'] = -df['Goals Against']
    df['Ranking'] = df['Ranking'].astype(int)

    chosen_sorting = st.selectbox(
        key="combined_ranking_one_season__sorting",
        label="Sort by...",
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
        x=alt.X('Shots:Q'),
        y=alt.Y('Club:N', sort=club_order),
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
        x=alt.X('Shots:Q'),
        y=alt.Y('Club:N', sort=club_order),
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
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date
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
        last_date
    )

    df['Ranking'] = df['Ranking'].astype(int)
    df["Failed Passes"] = df["Att Passes"] - df["Succ Passes"]

    chosen_sorting = st.selectbox(
        key="combined_ranking_one_season__sorting",
        label="Sort by...",
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
        x=alt.X('Count:Q', title="Number of passes"),
        y=alt.Y('Club:N', sort=club_order),
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
        y=alt.Y('Club:N', sort=club_order),
        x=alt.X('Att Passes:Q', title="Number of passes"),
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
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date
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
        last_date
    )

    df['Ranking'] = df['Ranking'].astype(int)

    chosen_sorting = st.selectbox(
        key="combined_ranking_one_season__sorting",
        label="Sort by...",
        options=["Ranking", "Wins", "Draws", "Loses"]
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
        x=alt.X('Count:Q', stack='zero'),
        y=alt.Y('Club:N', sort=club_order),
        color=alt.Color('Outcome:N',
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
        chosen_comp,
        chosen_season,
        combined_ranking,
        side,
        first_week,
        last_week,
        first_date,
        last_date
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
        last_date
    )

    df["xG Against"] = -df["xG Against"]
    df["xG Against (soccerstat)"] = -df["xG Against (soccerstat)"]
    df["Goals Against"] = -df["Goals Against"]
    df["Ranking"] = df["Ranking"].astype(int)

    chosen_sorting = st.selectbox(
        key="combined_ranking_one_season__sorting",
        label="Sort by...",
        options=["Ranking", "Goals For", "Goals Against", "xG For", "xG For (soccerstat)", "xG Against", "xG Against (soccerstat)"]
    )

    club_order = df.sort_values(chosen_sorting, ascending=chosen_sorting == "Ranking")['Club'].tolist()

    df_melted = df.melt(
        id_vars=["Club", "Ranking"],
        value_vars=["xG For", "xG For (soccerstat)", "xG Against", "xG Against (soccerstat)", "Goals For", "Goals Against"],
        var_name="Side",
        value_name="Value"
    )

    df_melted['Value_abs'] = df_melted['Value'].abs()
    df_melted['Category'] = df_melted['Side'].apply(lambda x: 'xG (soccerstat)' if 'soccerstat' in x else 'xG' if 'xG' in x else 'Goals')
    df_melted['Side'] = df_melted['Side'].apply(lambda x: 'For' if 'For' in x else 'Against')

    xg_data = df_melted[df_melted['Category'] == 'xG']
    xg_soccerstat_data = df_melted[df_melted['Category'] == 'xG (soccerstat)']
    goals_data = df_melted[df_melted['Category'] == 'Goals']

    goals = alt.Chart(goals_data).mark_bar().encode(
        x=alt.X('Value:Q'),
        y=alt.Y('Club:N', sort=club_order),
        color=alt.Color('Side:N',
            scale=alt.Scale(domain=["For", "Against"], range=['steelblue', 'orange']),
            legend=alt.Legend(title="Goals")
        ),
        tooltip=["Club", "Category", "Side", alt.Tooltip('Value_abs:Q', title='Goals'), "Ranking"]
    )

    expected = alt.Chart(xg_data).mark_tick(thickness=4, size=20, color="black").encode(
        x=alt.X('Value:Q'),
        y=alt.Y('Club:N', sort=club_order),

        tooltip=["Club", "Category", "Side", alt.Tooltip('Value_abs:Q', title='xG'), "Ranking"]
    )

    expected_soccerstat = alt.Chart(xg_soccerstat_data).mark_tick(thickness=4, size=20, color="green").encode(
        x=alt.X('Value:Q'),
        y=alt.Y('Club:N', sort=club_order),

        tooltip=["Club", "Category", "Side", alt.Tooltip('Value_abs:Q', title='xG'), "Ranking"]
    )

    rule = alt.Chart(df_melted).mark_rule(color='white', strokeWidth=3).encode(
        x=alt.datum(0)
    )

    final_chart = (goals + expected + expected_soccerstat + rule).resolve_scale(
        y='shared'
    ).properties(
        title="xG — For vs Against",
        width=600
    )

    st.altair_chart(final_chart, use_container_width=True)

    return df