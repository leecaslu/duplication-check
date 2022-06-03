import navegador
import registro

# Programa principal que reúne os outros arquivos. Como era usado na empresa

# declarando variáveis
email = 'exemplo@exemplo.com'
user = 'usuario'
senha = 'senha'
planilha = r"Exemplo-teste1.xlsx"
proxy = 'proxy'
lista_emails = ('email@exemplo.com', 'email2@exemplo.com')  # implementar


conectado = navegador.Usuario(username=user, password=senha, email=email, proxy_con=False)
res = ('1', '2', '3')
while True:
    ans = input(
        'O que deseja fazer? (Favor digitar o número desejado)'
        '\n1- Relatório mensal\n2- Vistoria diária\n3- Vistoria filtrada'
    )
    if ans in res:
        break
    else:
        print('Favor escolher uma das opções')
if ans == '1':
    clientes = registro.geracao_relatorio_mensal(planilha)
elif ans == '2':
    clientes = registro.geracao_vistoria_diaria(planilha, 12)
else:
    filtro = input('Qual será o filtro a ser usado nas regiões')
    clientes = registro.geracao_vistoria_filtrada(planilha, filtro)
registro.criacao_pastas()
conectado.login_lv()
for indice, cliente in enumerate(clientes):
    clientes[indice] = conectado.checando_duplicidade(cliente)
conectado.driver.close()
registro.report_backup(clientes)
dup = registro.report_duplicidade(clientes=clientes, plan=planilha)
registro.criando_relatorio_csv_excel(clientes)
print(registro.enviar_email(len(clientes), emails=lista_emails, plan=planilha, dupli=dup))
