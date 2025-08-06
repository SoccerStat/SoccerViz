from abc import ABC, abstractmethod
import streamlit as st

from components.commons.set_button_style import set_button_with_style
from components.commons.set_titles import set_main_title, set_sub_title, set_sub_sub_title
from config import PREFIX_PAGE
from utils.page_helper.page_config import set_page_config
from components.sidebar import sidebar_connection
from components.commons.ensure_connection_or_warning import set_connection_or_warning


class BasePage(ABC):
    def __init__(self, page_title):
        self.page_title = page_title

    def set_page_config(self, home=False):
        if home:
            set_page_config(f"{PREFIX_PAGE}", hide_sidebar=False)
        else:
            set_page_config(f"{PREFIX_PAGE} {self.page_title}")

    def set_page_title(self):
        set_main_title(self.page_title)

    def set_expander(self, label):
        return st.expander(f"**{label}**")

    def set_sub_title(self, name):
        set_sub_title(name)

    def set_sub_sub_title(self, name):
        set_sub_sub_title(name)

    def set_back_home_button(self):
        with set_button_with_style("back_home", width="auto"):
            if st.button("← Return to Home"):
                st.switch_page("Home.py")

    def render(self):
        self.set_page_config()

        self.set_page_title()

        sidebar_connection()

        set_connection_or_warning(self.content)

        self.set_back_home_button()

    @abstractmethod
    def content(self):
        pass

