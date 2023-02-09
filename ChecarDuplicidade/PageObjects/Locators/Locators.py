class LVLocator(object):
    # locator for login page
    lv_login = '//*[@id="app"]/div/main/div[2]/div[1]/div[1]/form/div/button'

    # locators for admin homepage - clientes
    lv_adm_cod_cliente = '//*[@id="wnoDL"]/div[2]/div[2]'
    lv_adm_linha_cod_clientes = '//*[@id="gsVbx"]/div[2]/div[2]'
    lv_adm_produtos = '//*[@id="app"]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div'
    lv_adm_icone_acessar_cliente = '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/tbody[1]/tr/td[8]/div/div/div '
    lv_adm_search_cod_cliente = '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/div/input '

    # locators for admin homepage - produtos
    lv_adm_search_produto = '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div/input'
    lv_adm_linha_produto = '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[2]/div/div[2]/tbody[1]'
    lv_adm_cod_produto = '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[2]/div/div[2]/tbody[1]/tr/td[2]/p'

    # locators for homepage do cliente
    lv_cimento_to = "//a[@title='Ir para Todas as obras']"
    lv_cimento_est = "//a[@title='Ir para Obras Estruturais']"

    # locators for pagina de cimentos
    lv_codigos_cimentos = 'description-title'

    # locators for pagina de produto
    lv_produto_div_regra_exibicao = '//*[@id="app"]/div/div[1]'
    lv_produto_seletor_regra = '//*[@id="app"]/div/div[1]/fieldset/div[1]/div/div[1]/div[1]/div[1]'
    lv_produto_lista_regras = "v-list-item__title"
    lv_produto_escopo_adicionar = '//*[@id="app"]/div/div[1]/fieldset/div[2]/div[1]'
    lv_produto_escopo_retirar = '//*[@id="app"]/div/div[1]/fieldset/div[2]/div[3]'
    lv_produto_microregiao_lista = 'jsm-checkbox__wrapper'
    lv_produto_botoes = 'v-btn__content'
    lv_produto_popup = 'jsm-notification__wrapper'
