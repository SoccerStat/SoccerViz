from abc import ABC, abstractmethod
from typing import Literal

import streamlit as st

from components.commons.set_button_style import set_button_with_style
from components.commons.set_titles import set_main_title, set_sub_title, set_sub_sub_title
from config import PREFIX_PAGE, APP_CONFIG
from components.sidebar import sidebar_connection
from utils.database_helper.connection import set_connection_or_warning


class BasePage(ABC):
    def __init__(self, page_title):
        self.page_title = page_title

    def render(self, home=False):
        self._set_page_config(home)

        self._set_page_title()

        sidebar_connection()

        set_connection_or_warning(self.content)

        if not home:
            self._set_back_home_button()

    def _set_page_config(self, home=False):
        if home:
            page_title = PREFIX_PAGE
            sidebar: Literal["expanded", "collapsed"] = "expanded"
        else:
            page_title = f"{PREFIX_PAGE} {self.page_title}"
            sidebar: Literal["expanded", "collapsed"] = "collapsed"

        st.set_page_config(
            page_title=page_title,
            page_icon=APP_CONFIG['icon'],
            layout=APP_CONFIG['layout'],
            initial_sidebar_state=sidebar,
        )

    def _set_page_title(self):
        set_main_title(self.page_title)

    def set_expander(self, label):
        return st.expander(f"**{label}**")

    def set_sub_title(self, name):
        set_sub_title(name)

    def set_sub_sub_title(self, name):
        set_sub_sub_title(name)

    def _set_back_home_button(self):
        with set_button_with_style("back_home", width="auto"):
            if st.button("← Return to Home"):
                st.switch_page("Home.py")

    @abstractmethod
    def content(self):
        pass
