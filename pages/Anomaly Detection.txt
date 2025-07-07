from utils.commons.BasePage import BasePage
from config import ANOMALY_DETECTION_PAGE

class MonitoringPage(BasePage):
    def content(self):
        pass

if __name__ == "__main__" or True:
    page = MonitoringPage(ANOMALY_DETECTION_PAGE)
    page.render()