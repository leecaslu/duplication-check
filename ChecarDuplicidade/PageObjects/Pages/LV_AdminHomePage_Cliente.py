import sys
sys.path.append(".")
from selenium.webdriver.common.by import By
from Locators import LVLocator


# import os
# Uncomment if the above example gives you a relative path error
# sys.path.append(os.getcwd())


class LVAdminHomePageC(object):

    def __init__(self, driver):
        self.driver = driver
        self._lv_adm_cod_cliente = driver.find_element(By.XPATH, LVLocator.lv_adm_cod_cliente)
        self._lv_adm_linha_cod_clientes = driver.find_element(By.XPATH, LVLocator.lv_adm_linha_cod_clientes)
        self._lv_adm_produtos = driver.find_element(By.XPATH, LVLocator.lv_adm_produtos)
        self._lv_adm_icone_acessar_cliente = driver.find_element(By.XPATH, LVLocator.lv_adm_icone_acessar_cliente)
        self._lv_adm_search_cod_cliente = driver.find_element(By.XPATH, LVLocator.lv_adm_search_cod_cliente)

    @property
    def lv_adm_cod_cliente(self):
        return self._lv_adm_cod_cliente

    @property
    def lv_adm_linha_cod_clientes(self):
        return self._lv_adm_linha_cod_clientes

    @property
    def lv_adm_produtos(self):
        return self._lv_adm_produtos

    @property
    def lv_adm_icone_acessar_cliente(self):
        return self._lv_adm_icone_acessar_cliente

    @property
    def lv_adm_search_cod_cliente(self):
        return self._lv_adm_search_cod_cliente
