from abc import ABC, abstractmethod
import streamlit as st

from config import PREFIX_PAGE
from utils.page_helper.page_config import set_page_config


class BasePage(ABC):
    def __init__(self, page_title):
        self.page_title = page_title

    def set_page_config(self):
        set_page_config(f"{PREFIX_PAGE} {self.page_title}")

    def set_page_title(self):
        st.markdown(f'<h1 class="main-title">{self.page_title}</h1>', unsafe_allow_html=True)

    def set_back_home_button(self):
        if st.button("← Return to Home"):
            st.switch_page("Home.py")

    @abstractmethod
    def render(self):
        pass

