import sys
from selenium.webdriver.common.by import By
from PageObjects.Locators.Locators import LVLocator

sys.path.append(sys.path[0] + "/....")
# import os
# Uncomment if the above example gives you a relative path error
# sys.path.append(os.getcwd())


class LVCimentoPage(object):
    def __init__(self, driver):
        self.driver = driver
        self._lv_codigos_cimentos = driver.find_elements(By.CLASS_NAME, LVLocator.lv_codigos_cimentos)

    @property
    def lv_codigos_cimentos(self):
        return self._lv_codigos_cimentos
