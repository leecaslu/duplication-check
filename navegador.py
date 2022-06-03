# Programa que realiza um webscraping automatizado pelo Selenium.
"""
TODO Refatorar e integrar o programa com o robô do Cleverson
TODO Implementar (no futuro) maneira de analisar banco de dados para agilizar o processo (SQL)
"""

# imports necessarios: selenium, webdriver-manager
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import date
from dados_duplicidade import DadosCliente

# tempo de espera para carregar elementos na LV. É alto pois a LV demora muito.
timeout = 100


class Usuario:
    """Classe que representa o usuário. Ele tem um user, email e senha e pode realizar login e checar duplicidade"""

    def __init__(self, username: str, password: str, email: str, proxy_con: bool, proxy: str = ''):
        self.user = username
        self.senha = password
        self.email = email
        self.proxy = proxy_con
        # inicializando o driver Chrome. Configurado opções para não fechar a janela automaticamente e arruma o tamanho
        # da janela
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument("window-size=1360,760")
        driver = webdriver.Chrome()
        if proxy_con:
            options.add_argument(f"--proxy-server={proxy}")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # Realizando o login na LV
    def login_lv(self) -> None:
        """Método que realiza o login em um link, neste caso específico, a Loja Virtual. Inicializa o Chrome driver e
        navega até o link, faz o login administrativo e insere user e senha. Modificar os links e camiknhos conforme
        desejado"""
        self.driver.get('www.linkdaloja.com')
        self.driver.find_element(By.CLASS_NAME, 'jsm-button__button--medium') \
            .click()
        # Entrando email, login e senha
        WebDriverWait(self.driver, timeout=timeout).until(ec.presence_of_element_located((By.NAME, 'loginfmt')))
        self.driver.find_element(By.NAME, 'loginfmt').send_keys(self.email, Keys.ENTER)
        WebDriverWait(self.driver, timeout=timeout).until(ec.presence_of_element_located(
            (By.CLASS_NAME, 'jsm-table__select-filter')))
        self.driver.execute_script("arguments[0].click();",
                                   self.driver.find_element(By.CLASS_NAME, 'jsm-table__select-filter'))
        WebDriverWait(self.driver, timeout=timeout).until(ec.presence_of_element_located(
            (By.CLASS_NAME, 'jsm-select__options')))
        self.driver.execute_script("arguments[0].click();",
                                   self.driver.find_element(By.CLASS_NAME, 'jsm-select__options')[1])

        if not self.proxy:
            WebDriverWait(self.driver, timeout=timeout).until(ec.presence_of_element_located((By.ID, "passwordInput")))
            self.driver.find_element(By.ID, "passwordInput").send_keys(self.senha, Keys.ENTER)
            WebDriverWait(self.driver, timeout=timeout).until(ec.presence_of_element_located((By.ID, "idSIButton9")))
            self.driver.find_element(By.ID, "idSIButton9").click()

    def checando_duplicidade(self, cliente: DadosCliente) -> DadosCliente:
        """Esse método checa a duplicidade de produtos dentro da Loja Virtual"""
        today = date.today()
        codigo = cliente.identificacao[2]
        microregiao = cliente.identificacao[0]
        check_to = cliente.cimento_todas_obras
        check_e = cliente.cimento_estrutural
        codigos_analisados = cliente.codigos_analisados
        # O driver precisa esperar o elemento carregar
        WebDriverWait(self.driver, timeout=timeout).until(
            ec.presence_of_element_located((
                By.XPATH,
                '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/div/input')))

        # Pesquisando o código
        sleep(2)
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div[1]/'
                                           'div[2]/div[1]/div/input').send_keys(Keys.CONTROL + "a", Keys.DELETE)
        sleep(2)
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div[1]/'
                                           'div[2]/div[1]/div/input').send_keys(codigo, Keys.ENTER)

        # Como o carregamento demora muito, usamos esse while True para esperar o quanto tiver que esperar.
        # Se passar de 6 tentativas, passa para o próximo código
        tent = 0
        while True:
            try:
                if codigo in self.driver.find_elements(By.CLASS_NAME, "jsm-table__data-field")[2].get_attribute('title'):
                    break
                else:
                    tent += 1
                    if tent > 6:
                        cliente.cimento_todas_obras = {'comentario': f"{codigo} não encontrado na Loja Virtual."}
                        cliente.cimento_estrutural = cliente.cimento_todas_obras
                        print(cliente)
                        return cliente
                    else:
                        sleep(5)
                        pass
            # Esse except trata no caso de mudança no estado do HTML
            except selenium.common.exceptions.StaleElementReferenceException:
                pass
            # Caso não encontre o código, IndexError aparece
            except IndexError:
                cliente.cimento_todas_obras = {'comentario': f"{codigo} não encontrado na Loja Virtual."}
                cliente.cimento_estrutural = cliente.cimento_todas_obras
                return cliente

        # Selecionando o cliente
        element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/'
                                                     'div/div[2]/tbody[1]/tr/td[8]/div/div/div/img')
        self.driver.execute_script("arguments[0].click();", element)
        while True:
            if len(self.driver.window_handles) > 1:
                break

        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            WebDriverWait(self.driver, timeout=timeout). \
                until(ec.presence_of_element_located((
                By.XPATH, '/html/body/div[1]/div/section/nav[2]/ul/li[2]/ul/li[3]/ul/li[1]/a')))
        except selenium.common.exceptions.TimeoutException:
            return cliente

        # Indo para a página dos cimentos todas as obras
        try:
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(
                By.XPATH, "//a[@title='Ir para Todas as obras']"))
            # Checar a duplicidade
            WebDriverWait(self.driver, timeout=timeout).until(ec.presence_of_element_located((By.CLASS_NAME,
                                                                                              'description-title')))
            sleep(5)
            elements = self.driver.find_elements(By.CLASS_NAME, 'description-title')
            elements = tuple(filter(lambda x: x.text.lower().find('toda') >= 0, elements))
            for key in check_to.keys():
                for el in elements:
                    if el.text.find(str(key)[:2]) >= 0:
                        check_to[key] += 1
                        # registrando os códigos analisados
                        codigos_analisados.append(self.driver.execute_script(
                            "return arguments[0].previousElementSibling", el).text)
            # tirando print
            webdriver.ActionChains(self.driver). \
                move_to_element(self.driver.find_element(By.CLASS_NAME, 'products--grid-view ')).perform()
            self.driver.execute_script("arguments[0].scrollIntoView();",
                                       self.driver.find_element(By.CLASS_NAME, 'products--grid-view '))
            self.driver.get_screenshot_as_file(
                f'\{today.strftime("%d.%m.%y")}\T.O.\{microregiao}.png'
            )
        except selenium.common.exceptions.NoSuchElementException:
            pass
        except selenium.common.exceptions.TimeoutException:
            cliente.cimento_todas_obras = {'comentario': "Loja Virtual demorou muito para responder."}
            cliente.cimento_estrutural = cliente.cimento_todas_obras
            return cliente

        # Indo para a página dos cimentos estruturais
        try:
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(
                By.XPATH, "//a[@title='Ir para Obras Estruturais']"))
            WebDriverWait(self.driver, timeout=timeout).until(ec.presence_of_element_located((By.CLASS_NAME,
                                                                                              'description-title')))
            sleep(5)
            elements = self.driver.find_elements(By.CLASS_NAME, 'description-title')
            elements = tuple(filter(lambda x: x.text.lower().find('estrutura') >= 0, elements))
            for key in check_e.keys():
                for el in elements:
                    if el.text.find(str(key)[:2]+'KG') >= 0:
                        check_e[key] += 1
                        # registrando o código dos produtos analisados
                        codigos_analisados.append(self.driver.execute_script(
                            "return arguments[0].previousElementSibling", el).text)
            # Printando a tela
            webdriver.ActionChains(self.driver). \
                move_to_element(self.driver.find_element(By.CLASS_NAME, 'products--grid-view ')).perform()
            self.driver.execute_script("arguments[0].scrollIntoView();",
                                       self.driver.find_element(By.CLASS_NAME, 'products--grid-view '))
            sleep(1)

            self.driver.get_screenshot_as_file(
                f'\{today.strftime("%d.%m.%y")}\Est.\{microregiao}.png'
            )
        except selenium.common.exceptions.NoSuchElementException:
            pass
        except selenium.common.exceptions.TimeoutException:
            cliente.cimento_todas_obras = {'comentario': "Loja Virtual demorou muito para responder."}
            cliente.cimento_estrutural = cliente.cimento_todas_obras
            return cliente

        # Fechando a aba e retornando para a aba de pesquisa.
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return cliente
