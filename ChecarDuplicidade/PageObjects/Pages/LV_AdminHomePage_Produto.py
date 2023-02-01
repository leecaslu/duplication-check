import sys
from selenium.webdriver.common.by import By
from PageObjects.Locators.Locators import LVLocator

sys.path.append(sys.path[0] + "/....")
# import os
# Uncomment if the above example gives you a relative path error
# sys.path.append(os.getcwd())


class LVAdminHomePageP(object):

    def __init__(self, driver):
        self.driver = driver
        self._lv_adm_search_produto = driver.find_element(By.XPATH, LVLocator.lv_adm_search_produto)
        self._lv_adm_linha_produto = driver.find_element(By.XPATH, LVLocator.lv_adm_linha_produto)
        self._lv_adm_cod_produto = driver.find_element(By.XPATH, LVLocator.lv_adm_cod_produto)

    @property
    def lv_adm_search_produto(self):
        return self._lv_adm_search_produto

    @property
    def lv_adm_linha_produto(self):
        return self._lv_adm_linha_produto

    @property
    def lv_adm_cod_produto(self):
        return self._lv_adm_cod_produto
