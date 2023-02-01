import sys
from selenium.webdriver.common.by import By
from PageObjects.Locators.Locators import LVLocator

sys.path.append(sys.path[0] + "/....")
# import os
# Uncomment if the above example gives you a relative path error
# sys.path.append(os.getcwd())


class LVClienteHomePage(object):

    def __init__(self, driver):
        self.driver = driver
        self._lv_cimento_to = driver.find_element(By.XPATH, LVLocator.lv_cimento_to)
        self._lv_cimento_est = driver.find_element(By.XPATH, LVLocator.lv_cimento_est)

    @property
    def lv_cimento_to(self):
        return self._lv_cimento_to

    @property
    def lv_cimento_est(self):
        return self._lv_cimento_est
