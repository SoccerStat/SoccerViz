import streamlit as st

from components.commons.get_seasons import get_all_season_schemas

from config import COMPETITIONS


def select__get_one_comp(prefix, label="Choose one competition...", custom_options=None, all_comps=False):
    if custom_options:
        options = custom_options
    else:
        options = [comp["label"] for _, comp in COMPETITIONS.items()]
        if all_comps:
            options = ["All"] + options

    return st.selectbox(
        key=f"{prefix}__comp",
        label=label,
        options=[""] + options
    )


def select__get_one_season(db_conn, prefix, label="Choose one season...", custom_options=None):
    if custom_options:
        options = custom_options
    else:
        options = get_all_season_schemas(db_conn)

    return st.selectbox(
        key=f"{prefix}__season",
        label=label,
        options=[""] + options
    )


def check__generic(prefix, suffix, label):
    return st.checkbox(
        key=f"{prefix}__{suffix}",
        label=label
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
    return st.slider(
        key=f"{prefix}__{suffix}",
        label=label,
        min_value=min_value,
        max_value=max_value,
        value=default_value
    )


def date__get_one_date(prefix, suffix, default_value="today", label="Select a date"):
    return st.date_input(
        key=f"{prefix}__{suffix}",
        label=label,
        value=default_value
    )


def multiselect__get_slots(prefix, options, label="Select slots..."):
    return st.multiselect(
        key=f"{prefix}__slots",
        label=label,
        options=options
    )


def radio__select_side(prefix, label="Select one side...", default_index=1, custom_options=None):
    if custom_options:
        options = custom_options
    else:
        options = ["Home", "Both", "Away"]

    return st.radio(
        key=f"{prefix}__side",
        label=label,
        options=options,
        horizontal=True,
        label_visibility="collapsed",
        index=default_index
    )
