# Programa que le o excel, procura na web e preenche os dados necessarios.
"""
TODO implementar o PageObjects.
Funciona sem PageObjects, mas seria interessante refatorar, levando em consideração as limitações da LV.
"""

# imports necessarios: openpyxl, selenium.
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from os import getcwd

# from PageObjects.Pages.LV_LoginPage import LVLogin
# from PageObjects.Pages.LV_ProdutoPage import LVProdutoPage
# from PageObjects.Pages.LV_AdminHomePage_Cliente import LVAdminHomePageC
# from PageObjects.Pages.LV_AdminHomePage_Produto import LVAdminHomePageP
# from PageObjects.Pages.LV_CimentoPage import LVCimentoPage
# from PageObjects.Pages.LV_ClienteHomePage import LVClienteHomePage
from time import sleep
from datetime import date
from classes import DadosCliente, DadosProduto

# tempo de espera para carregar elementos na LV. É alto pois a LV demora muito.
timeout = 100


class Usuario:
  """Classe que representa o usuário. Ele tem um user, email e senha e pode realizar login e checar duplicidade"""

  def __init__(
    self, username: str, password: str, email: str, proxy_con: bool, proxy: str = ""
):
    self.user = username
    self.senha = password
    self.email = email
    self.proxy = proxy_con
    # inicializando o driver Chrome.
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("window-size=1360,760")
    if proxy_con:
      options.add_argument(f"--proxy-server={proxy}")
    self.driver = webdriver.Chrome(
      executable_path="RPA\ChecarDuplicidade\webdrivers\chromedriver108.exe",
      options=options,
    )

  # Realizando o login na LV
  def login_lv(self, produto=False) -> None:
    """Método que realiza o login em um link, neste caso específico, a Loja Virtual. Inicializa o Chrome driver e
    navega até o link, faz o login administrativo e insere user e senha, com pyautoGUI pois selenium não reconhece
    alertas de API (do SO)"""
    self.driver.get("https://admin-loja.juntossomosmais.com.br/login")
    self.driver.find_element(By.CLASS_NAME, "jsm-button__button--medium").click()
    # Entrando email, login e senha
    WebDriverWait(self.driver, timeout=timeout).until(
      ec.presence_of_element_located((By.NAME, "loginfmt"))
    )
    self.driver.find_element(By.NAME, "loginfmt").send_keys(self.email, Keys.ENTER)
    WebDriverWait(self.driver, timeout=timeout).until(
      ec.presence_of_element_located((By.CLASS_NAME, "jsm-table__select-filter"))
    )
    self.driver.execute_script(
      "arguments[0].click();",
      self.driver.find_element_by_class_name("jsm-table__select-filter"),
    )
    WebDriverWait(self.driver, timeout=timeout).until(
      ec.presence_of_element_located((By.CLASS_NAME, "jsm-select__options"))
    )
    self.driver.execute_script(
      "arguments[0].click();",
      self.driver.find_elements_by_class_name("jsm-select__options")[1],
    )
    if produto:
      WebDriverWait(self.driver, timeout=timeout).until(
        ec.presence_of_element_located(
          (
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/p",
          )
        )
      )
      self.driver.execute_script(
        "arguments[0].click();",
        self.driver.find_element(
          By.XPATH,
          "/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/p",
        ),
      )

  def checando_duplicidade(self, cliente: DadosCliente) -> DadosCliente:
    codigo = str(cliente.identificacao[2])
    microregiao = str(cliente.identificacao[0])
    today = date.today()
    cliente.cimento_todas_obras = {"25 to": 0, "42 to": 0, "50 to": 0}
    cliente.cimento_estrutural = {"40 e": 0, "50 e": 0}
    check_to = cliente.cimento_todas_obras
    check_e = cliente.cimento_estrutural

    codigos_analisados = cliente.codigos_analisados
    # O driver precisa esperar o elemento carregar
    try:
      WebDriverWait(self.driver, timeout=timeout).until(
        ec.presence_of_element_located(
          (
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/div/input",
          )
        )
      )
    except selenium.common.exceptions.TimeoutException:
        cliente.cimento_todas_obras = {
            "comentario": "Loja Virtual demorou muito para responder."
        }
        cliente.cimento_estrutural = cliente.cimento_todas_obras
        return cliente
    # Pesquisando o código

    sleep(2)
    self.driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div[1]/"
        "div[2]/div[1]/div/input",
    ).send_keys(Keys.CONTROL + "a", Keys.DELETE)
    sleep(2)
    self.driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div[1]/"
        "div[2]/div[1]/div/input",
    ).send_keys(codigo, Keys.ENTER)
    # Como o carregamento demora muito, usamos esse while True para esperar o quanto tiver que esperar.

    tent = 0
    while True:
        try:
            if codigo in self.driver.find_elements(
                By.CLASS_NAME, "jsm-table__data-field"
            )[2].get_attribute("title"):
                break
            else:
                tent += 1
                if tent > 6:
                    cliente.cimento_todas_obras = {
                        "comentario": f"{codigo} não encontrado na Loja Virtual."
                    }
                    cliente.cimento_estrutural = cliente.cimento_todas_obras
                    cliente.verificado = True
                    print(cliente)
                    return cliente
                else:
                    sleep(2)
                    pass
        except selenium.common.exceptions.StaleElementReferenceException:
            pass
        except IndexError:
            cliente.cimento_todas_obras = {
                "comentario": f"{codigo} não encontrado na Loja Virtual."
            }
            cliente.cimento_estrutural = cliente.cimento_todas_obras
            cliente.verificado = True
            return cliente

    # Selecionando o cliente
    element = self.driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/"
        "div/div[2]/tbody[1]/tr/td[8]/div/div/div/img",
    )
    self.driver.execute_script("arguments[0].click();", element)
    sleep(10)
    if len(self.driver.window_handles) < 2:
        cliente.cimento_todas_obras = {
            "comentario": f"{codigo} não encontrado na Loja Virtual."
        }
        cliente.cimento_estrutural = cliente.cimento_todas_obras
        cliente.verificado = True
        return cliente

    self.driver.switch_to.window(self.driver.window_handles[1])
    try:
        WebDriverWait(self.driver, timeout=timeout).until(
            ec.presence_of_element_located(
                (By.CLASS_NAME, "navbar-items__departments")
            )
        )
        sleep(1)
    except selenium.common.exceptions.TimeoutException:
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        cliente.cimento_todas_obras = {
            "comentario": "Loja Virtual demorou muito para responder."
        }
        cliente.cimento_estrutural = cliente.cimento_todas_obras
        print(cliente)
        return cliente

    # Indo para a página dos cimentos todas as obras
    try:
        self.driver.execute_script(
            "arguments[0].click();",
            self.driver.find_element(
                By.XPATH, "//a[@title='Ir para Todas as obras']"
            ),
        )
        # Checar a duplicidade
        WebDriverWait(self.driver, timeout=timeout).until(
            ec.presence_of_element_located(
                (By.CLASS_NAME, "description-title")
            )
        )
        sleep(5)
        elements = self.driver.find_elements(
          By.CLASS_NAME, "description-title"
        )
        elements = tuple(
          filter(
            lambda x: x.get_attribute("innerHTML").lower().find("toda") >= 0,
            elements,
          )
        )
        for key in check_to.keys():
          for el in elements:
            if el.get_attribute("innerHTML").find(str(key)[:2]) >= 0:
              check_to[key] += 1
              codigos_analisados.append(
                self.driver.execute_script(
                  "return arguments[0].previousElementSibling", el
                ).get_attribute("innerHTML")
              )
        webdriver.ActionChains(self.driver).move_to_element(
          self.driver.find_element(By.CLASS_NAME, "products--grid-view ")
        ).perform()
        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            self.driver.find_element(By.CLASS_NAME, "products--grid-view "),
        )
        print(
            self.driver.get_screenshot_as_file(
                getcwd() + f'\{today.strftime("%d.%m.%y")}\T.O.\{microregiao}.png'
            )
        )
    except selenium.common.exceptions.NoSuchElementException:
        pass
    except selenium.common.exceptions.TimeoutException:
        cliente.cimento_todas_obras = {
            "comentario": "Loja Virtual demorou muito para responder."
        }
        cliente.cimento_estrutural = cliente.cimento_todas_obras
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        print(cliente)
        return cliente

    # Indo para a página dos cimentos estruturais
    try:
        self.driver.execute_script(
            "arguments[0].click();",
            self.driver.find_element(
                By.XPATH, "//a[@title='Ir para Obras Estruturais']"
            ),
        )
        WebDriverWait(self.driver, timeout=timeout).until(
            ec.presence_of_element_located(
                (By.CLASS_NAME, "description-title")
            )
        )
        sleep(5)
        elements = self.driver.find_elements(
            By.CLASS_NAME, "description-title"
        )
        elements = tuple(
            filter(
                lambda x: x.get_attribute("innerHTML").lower().find("estrutura")
                >= 0,
                elements,
            )
        )
        for key in check_e.keys():
            for el in elements:
                if el.get_attribute("innerHTML").find(str(key)[:2] + "KG") >= 0:
                    check_e[key] += 1
                    codigos_analisados.append(
                        self.driver.execute_script(
                            "return arguments[0].previousElementSibling", el
                        ).get_attribute("innerHTML")
                    )
        webdriver.ActionChains(self.driver).move_to_element(
            self.driver.find_element(By.CLASS_NAME, "products--grid-view ")
        ).perform()
        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            self.driver.find_element(By.CLASS_NAME, "products--grid-view "),
        )
        sleep(1)

        print(
            self.driver.get_screenshot_as_file(
                r"C:\Users\lucashl\OneDrive - Votorantim\Documentos"
                + f'\{today.strftime("%d.%m.%y")}\Est.\{microregiao}.png'
            )
        )
    except selenium.common.exceptions.NoSuchElementException:
        pass
    except selenium.common.exceptions.TimeoutException:
        cliente.cimento_todas_obras = {
            "comentario": "Loja Virtual demorou muito para responder."
        }
        cliente.cimento_estrutural = cliente.cimento_todas_obras
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        print(cliente)
        return cliente

    # Fechando a aba e retornando para a aba de pesquisa.
    self.driver.close()
    self.driver.switch_to.window(self.driver.window_handles[0])
    cliente.verificado = True
    print(cliente)
    return cliente

  # DEPRECADO
  def sanear_produto(self, produto: DadosProduto, ativar: bool = False):
      codigo = produto.codigo
      micros = produto.micros_sanear
      # Pesquisando o código
      WebDriverWait(self.driver, timeout=timeout).until(
          ec.presence_of_element_located(
              (
                  By.XPATH,
                  "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div/input",
              )
          )
      )
      self.driver.find_element(
          By.XPATH,
          "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div["
          "1]/div[1]/div/input",
      ).send_keys(Keys.CONTROL + "a", Keys.DELETE)
      sleep(2)
      self.driver.find_element(
          By.XPATH,
          "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div["
          "1]/div[1]/div/input",
      ).send_keys(codigo, Keys.ENTER)
      sleep(2)
      # Esperando carregamento
      tent = 0
      while True:
          try:
              if codigo.strip() in self.driver.find_elements(
                  By.CLASS_NAME, "jsm-table__data-field"
              )[1].get_attribute("title"):
                  break
              else:
                  tent += 1
                  if tent > 6:
                      print("demorou muito para responder")
                      return
                  else:
                      sleep(5)
                      pass
          except selenium.common.exceptions.StaleElementReferenceException:
              pass
          except IndexError:
              print("erro: não foi encontrado")
              return
      sleep(2)
      self.driver.execute_script(
          "arguments[0].click();",
          self.driver.find_elements(By.CLASS_NAME, "jsm-table__data-field")[1],
      )
      # Caso queiramos inativar o produto
      if produto.inativar:
          WebDriverWait(self.driver, timeout=timeout).until(
              ec.presence_of_element_located((By.XPATH, "//a[text()='Inativo']"))
          )
          self.driver.execute_script(
              "arguments[0].click();",
              self.driver.find_element(By.XPATH, "//a[text()=" "'Inativo']"),
          )
          return
      # Selecionando como sanear o produto
      WebDriverWait(self.driver, timeout=timeout).until(
          ec.presence_of_element_located((By.CLASS_NAME, "form-group"))
      )
      sleep(2)
      scope = self.driver.find_elements(By.CLASS_NAME, "form-group")[2]
      WebDriverWait(self.driver, timeout=timeout).until(
          ec.presence_of_element_located((By.CLASS_NAME, "v-select__selections"))
      )
      sleep(1)
      scope.find_element(By.CLASS_NAME, "v-select__selections").click()
      WebDriverWait(self.driver, timeout=timeout).until(
          ec.presence_of_element_located((By.CLASS_NAME, "v-list-item__title"))
      )
      elements = scope.find_elements(By.CLASS_NAME, "v-list-item__title")
      print(elements)
      for e in elements:
          if e.get_attribute("innerHTML") == "Microregiao":
              self.driver.execute_script("arguments[0].click();", e)
      sleep(1)

      # /html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/fieldset/div[2]/div[3]

      # Pesquisando a MR e tirando a seleção
      if not ativar:
          WebDriverWait(self.driver, timeout=timeout).until(
              ec.presence_of_element_located(
                  (
                      By.XPATH,
                      "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/fieldset/div[2]/div[3]",
                  )
              )
          )
          parent = scope.find_element(
              By.XPATH,
              "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div[1]"
              "/fieldset/div[2]/div[3]",
          )
      else:
          WebDriverWait(self.driver, timeout=timeout).until(
              ec.presence_of_element_located(
                  (
                      By.XPATH,
                      "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/fieldset/div[2]/div[1]",
                  )
              )
          )
          parent = scope.find_element(
              By.XPATH,
              "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div[1]"
              "/fieldset/div[2]/div[1]",
          )
      # Verificar esse try
      save = False
      try:
          elements = parent.find_elements(By.CLASS_NAME, "jsm-checkbox__wrapper")
          for e in elements:
              if e.get_attribute("innerHTML") in micros:
                  save = True
                  print(f'{e.get_attribute("innerHTML")} saneado do produto {codigo}')
                  e.click()
      except selenium.common.exceptions.StaleElementReferenceException:
          pass
      except selenium.common.exceptions.NoSuchElementException:
          print(f"não foi possível encontrar o produto {codigo}")
          pass
      if save:
          buttons = self.driver.find_elements(By.CLASS_NAME, "v-btn__content")
          for b in buttons:
              if b.get_attribute("innerHTML") == "SALVAR":
                  self.driver.execute_script("arguments[0].click();", b)
          # jsm-notification__wrapper
          WebDriverWait(self.driver, timeout=timeout).until(
              ec.presence_of_element_located(
                  (By.CLASS_NAME, "jsm-notification__wrapper")
              )
          )
          popup = self.driver.find_element(By.CLASS_NAME, "jsm-notification__wrapper")
          sucesso = (
              "jsm-notification__wrapper-active--success"
              in popup.get_attribute("class")
          )
          if sucesso:
              return
          else:
              WebDriverWait(self.driver, timeout=timeout).until(
                  ec.presence_of_element_located(
                      (
                          By.XPATH,
                          "/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/p",
                      )
                  )
              )
              self.driver.execute_script(
                  "arguments[0].click();",
                  self.driver.find_element(
                      By.XPATH,
                      "/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/p",
                  ),
              )
              return
      else:
          WebDriverWait(self.driver, timeout=timeout).until(
              ec.presence_of_element_located(
                  (
                      By.XPATH,
                      "/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/p",
                  )
              )
          )
          self.driver.execute_script(
              "arguments[0].click();",
              self.driver.find_element(
                  By.XPATH,
                  "/html/body/div[1]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/p",
              ),
          )
          return
