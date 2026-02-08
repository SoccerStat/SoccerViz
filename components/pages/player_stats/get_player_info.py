import streamlit as st
from streamlit_searchbox import st_searchbox

from components.commons.get_all_players import get_all_players
from components.commons.search_for_item import player_search_function


def get_player_info(db_conn):
    prefix = "player_info"
    all_players = list(get_all_players(db_conn))
    search_function = player_search_function(all_players)

    player = st_searchbox(
        search_function=search_function,
        key=f"{prefix}__player",
        placeholder="Choose Player",
    )

    st.write(player)
