import streamlit as st

from components.commons.streamlit.titles import set_sub_title
from components.pages.instagram_publishing.automated.panel import automated_publishing
from components.pages.instagram_publishing.automated.questions import question_to_stat

from config import PUBLISHING_PAGE

from utils.page_helper.BasePage import BasePage


class PublishingPage(BasePage):
    def content(self):
        set_sub_title("Automated generation of social posts")

        automated_tab, question_tab = st.tabs(["Auto. Publishing", "Ask something"])

        with automated_tab:
            automated_publishing()

        with question_tab:
            question_to_stat()


if __name__ == "__main__" or True:
    page = PublishingPage(PUBLISHING_PAGE)
    page.render()
