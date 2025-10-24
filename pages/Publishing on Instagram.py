from config import PUBLISHING_PAGE

from utils.commons.BasePage import BasePage


class PublishingPage(BasePage):
    def content(self):
        ""


if __name__ == "__main__" or True:
    page = PublishingPage(PUBLISHING_PAGE)
    page.render()
