import sys
from selenium.webdriver.common.by import By
from PageObjects.Locators.Locators import LVLocator

sys.path.append(sys.path[0] + "/....")
# import os
# Uncomment if the above example gives you a relative path error
# sys.path.append(os.getcwd())


class LVProdutoPage(object):

    def __init__(self, driver, ativar):
        self.driver = driver
        self._lv_produto_div_regra_exibicao = driver.find_element(By.XPATH, LVLocator.lv_produto_div_regra_exibicao)
        self._lv_produto_seletor_regra = driver.find_element(By.XPATH, LVLocator.lv_produto_seletor_regra)
        self._lv_produto_lista_regras = driver.find_elements(By.CLASS_NAME, LVLocator.lv_produto_lista_regras)
        if ativar:
            self._lv_produto_escopo = driver.find_element(By.XPATH, LVLocator.lv_produto_escopo_adicionar)
        else:
            self._lv_produto_escopo = driver.find_element(By.XPATH, LVLocator.lv_produto_escopo_retirar)
        self._lv_produto_microregiao_lista = self._lv_produto_escopo.find_elements(
            By.CLASS_NAME, LVLocator.lv_produto_microregiao_lista)
        self._lv_produto_botoes = driver.find_elements(By.CLASS_NAME, LVLocator.lv_produto_botoes)
        self._lv_produto_popup = driver.find_element(By.CLASS_NAME, LVLocator.lv_produto_popup)

    @property
    def lv_produto_popup(self):
        return self._lv_produto_popup

    @property
    def lv_produto_microregiao_lista(self):
        return self._lv_produto_microregiao_lista

    @property
    def lv_produto_botoes(self):
        return self._lv_produto_botoes

    @property
    def lv_produto_div_regra_exibicao(self):
        return self._lv_produto_div_regra_exibicao

    @property
    def lv_produto_seletor_regra(self):
        return self._lv_produto_seletor_regra

    @property
    def lv_produto_lista_regras(self):
        return self._lv_produto_lista_regras

    @property
    def lv_produto_escopo(self):
        return self._lv_produto_escopo
