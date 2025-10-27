import streamlit as st

from components.commons.set_titles import set_sub_title, set_sub_sub_title
from components.pages.instagram_publishing.publish_vs_post import publish_vs_post

from config import PUBLISHING_PAGE, INSTAGRAM_SUBJECTS

from utils.commons.BasePage import BasePage


class PublishingPage(BasePage):
    def content(self):
        set_sub_title("Automated generation of an Instagram post")

        if 'powerpoint_path' not in st.session_state:
            st.session_state.powerpoint_path = None
        if 'slides_png_paths' not in st.session_state:
            st.session_state.slides_png_paths = []

        chosen_subject = st.selectbox(
            key="instagram_publishing__subject",
            label="Select a subject...",
            options=[""] + list(INSTAGRAM_SUBJECTS.keys())
        )

        if chosen_subject:
            set_sub_sub_title(chosen_subject)

            template_path = INSTAGRAM_SUBJECTS[chosen_subject]

            if chosen_subject == "VS":
                publish_vs_post(
                    template_path = template_path
                )

if __name__ == "__main__" or True:
    page = PublishingPage(PUBLISHING_PAGE)
    page.render()
