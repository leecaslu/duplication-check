import sys
from selenium.webdriver.common.by import By
from PageObjects.Locators.Locators import LVLocator

sys.path.append(sys.path[0] + "/....")
# import os
# Uncomment if the above example gives you a relative path error
# sys.path.append(os.getcwd())


class LVLogin(object):
    def __init__(self, driver):
        self.driver = driver
        self._lv_login_button = driver.find_element(By.XPATH, LVLocator.lv_login)

    @property
    def lv_login_button(self):
        return self._lv_login_button
