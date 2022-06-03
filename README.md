# check-duplicidade / duplication-check
Projeto pequeno que consulta dados de clientes de uma planilha Excel e pesquisa por produtos duplicados ligados aos clientes na rede.
Projeto criado para verificação de produtos duplicados dentro da Loja Virtual de uma empresa de material de construção.
Por questões de segurança e confidencialidade, os dados do exemplo e variáveis do programa foram generalizados. Toda informação presente é fictícia

Esse projeto é composto por 3 pequenos arquivos Python, além do arquivo "main".

O arquivo "Navegador" faz uso de funções da biblioteca Selenium por um objeto para realizar o acesso via navegador Google Chrome. O objeto, então, realiza o webscraping de acordo com a lista de clientes extraída e retorna a verificação dos produtos encontrados.

O arquivo "Registro" trata os dados presentes fazendo uso das bibliotecas pandas e openpyxl. Este arquivo contém funções usadas para extrair os dados e moldá-los da maneira desejada. Também registra os resultados do webscrape em diferentes formatos de arquivo.

O arquivo "dados_duplicidade" enuncia uma dataclass "DadosCliente", cujo objeto é usado para guardar as informações e dados dos clientes listados na planilha.

Esse arquivo é de livre reprodução. Espero que sirva de ajuda a quem precisar.

-----------------------------------------------------------------------------------------------------------------------------------------------------------

A portuguese-based small project that extracts clients's data from an Excel sheet and searches for duplicate products linked to those clients on the web.
It was created in order to verify duplicated products on a building material company's virtual shop.
For security and confidentiality reasons, the examples' data and files' variables were abstracted.

This project contains 3 small python files, aside from the 'main' file. 

The file 'Navegador' apllies features from the Selenium libraries in order to access the web via Google Chrome driver. It then proceeds to webscrape the virtual shop website according to the extracted clients' list. It returns a verified products per clients' list.

The file 'Registro' manipulates present data via pandas and openpyxl libraries. This file contains functions used to extract and model data for adequate use. It also registers the webscraping results in different file formats.

The file 'dados_duplicidade' declares a dataclass 'DadosCliente'. Its object is used to store clients' information and data, according to the sheet.

Feel free to use any idea, class or function declared in this project. I hope it helps whoever needs it.
