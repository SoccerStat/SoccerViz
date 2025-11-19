import streamlit as st

from components.commons.get_seasons import get_all_season_schemas

from config import COMPETITIONS


def select__generic(prefix, suffix, label, options, default_index=0):
    return st.selectbox(
        key=f"{prefix}__{suffix}",
        label=label,
        options=[""] + options,
        index=default_index
    )


def check__generic(prefix, suffix, label):
    return st.checkbox(
        key=f"{prefix}__{suffix}",
        label=label
    )


def radio__generic(prefix, suffix, label, options, default_index):
    return st.radio(
        key=f"{prefix}__{suffix}",
        label=label,
        options=options,
        horizontal=True,
        label_visibility="collapsed",
        index=default_index
    )


def multiselect__generic(prefix, suffix, label, options):
    return st.multiselect(
        key=f"{prefix}__{suffix}",
        label=label,
        options=options,
    )


def slider__generic(prefix, suffix, label, min_value, max_value, default_value):
    return st.slider(
        key=f"{prefix}__{suffix}",
        label=label,
        min_value=min_value,
        max_value=max_value,
        value=default_value
    )


def check__filter_by_week(prefix, label="Filter by week"):
    return check__generic(prefix=prefix, suffix="filter_by_week", label=label)


def check__filter_by_date(prefix, label="Filter by date"):
    return check__generic(prefix=prefix, suffix="filter_by_date", label=label)


def check__filter_by_slot(prefix, label="Filter by slot"):
    return check__generic(prefix=prefix, suffix="filter_by_slot", label=label)


def check__group_by_club(prefix, label="Group by club"):
    return check__generic(prefix=prefix, suffix="group_by_club", label=label)


def check__group_by_competition(prefix, label="Group by competition"):
    return check__generic(prefix=prefix, suffix="group_by_competition", label=label)


def check__group_by_season(prefix, label="Group by season"):
    return check__generic(prefix=prefix, suffix="group_by_season", label=label)


def slider__get_one_week(prefix, suffix, min_value, max_value, default_value, label="Select a week"):
    return slider__generic(
        prefix=prefix,
        suffix=suffix,
        label=label,
        min_value=min_value,
        max_value=max_value,
        default_value=default_value
    )


def date__get_one_date(prefix, suffix, default_value="today", label="Select a date"):
    return st.date_input(
        key=f"{prefix}__{suffix}",
        label=label,
        value=default_value,
        format="YYYY-MM-DD"
    )


def radio__select_side(prefix, label="Select one side...", default_index=1, custom_options=None):
    if custom_options:
        options = custom_options
    else:
        options = ["Home", "Both", "Away"]

    return radio__generic(
        prefix=prefix,
        suffix="side",
        label=label,
        default_index=default_index,
        options=options
    )


def select__get_one_comp(prefix, label="Choose one competition...", custom_options=None, all_comps=False):
    if custom_options:
        options = custom_options
    else:
        options = [comp["label"] for _, comp in COMPETITIONS.items()]
        if all_comps:
            options = ["All"] + options

    return select__generic(prefix=prefix, suffix="comp", label=label, options=options)


def select__get_one_season(prefix, label="Choose one season...", db_conn=None, custom_options=None):
    if db_conn and not custom_options:
        options = get_all_season_schemas(db_conn)
    else:
        options = custom_options

    return select__generic(prefix=prefix, suffix="season", label=label, options=options)


def select__get_one_ranking(prefix, options, label="Choose one ranking..."):
    return select__generic(prefix=prefix, suffix="one_ranking", label=label, options=options)


def select__get_combined_ranking(prefix, options, label="Choose one combined ranking..."):
    return select__generic(prefix=prefix, suffix="one_combined_ranking", label=label, options=options)


def select__get_combined_ranking_sorting(prefix, options, suffix=None, label="Sort by..."):
    return select__generic(
        prefix=prefix,
        suffix=f"one_combined_ranking__sorting{f'_{suffix}' if suffix else ''}",
        label=label,
        options=options
    )


def select__get_many_teams(prefix, options, label="Choose teams...", all_teams=False):
    if all_teams:
        options = ["All"] + options

    return multiselect__generic(prefix=prefix, suffix="teams", label=label, options=options)


def multiselect__get_slots(prefix, options, label="Select slots..."):
    return multiselect__generic(prefix=prefix, suffix="slots", label=label, options=options)


def download_button(prefix, data, file_name, mime, suffix=None, label="📥 Download CSV"):
    return st.download_button(
        key=f"{prefix}__download_button{f'_{suffix}' if suffix else ''}",
        label=label,
        data=data,
        file_name=file_name,
        mime=mime
    )
