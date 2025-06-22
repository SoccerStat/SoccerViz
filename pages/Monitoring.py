from utils.commons.BasePage import BasePage
from config import MONITORING_PAGE


class MonitoringPage(BasePage):
    def content(self):
        pass

if __name__ == "__main__" or True:
    page = MonitoringPage(MONITORING_PAGE)
    page.render()