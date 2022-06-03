import registro
from random import randint

# Programa com exemplo de uso. Esse programa não usa o diretório navegador pois esse diretório é específico
# para um site.

# declarando variáveis
email = 'exemplo@exemplo.com'
user = 'usuario'
senha = 'senha'
planilha = r"Exemplo-teste1.xlsx"
proxy = 'proxy'
lista_emails = ('email@exemplo.com', 'email2@exemplo.com')  # implementar


# conectado = navegador.Usuario(username=user, password=senha, email=email, proxy_con=False)
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
for cliente in clientes:
    # Aqui, colocar as funções do programa navegador
    for key in cliente.cimento_todas_obras.keys():
        cliente.cimento_todas_obras[key] = randint(0, 2)
    for key in cliente.cimento_estrutural.keys():
        cliente.cimento_estrutural[key] = randint(0, 2)
print(clientes)
registro.report_backup(clientes)
dup = registro.report_duplicidade(clientes=clientes, plan=planilha)
registro.criando_relatorio_csv_excel(clientes)
print(registro.enviar_email(len(clientes), emails=lista_emails, plan=planilha, dupli=dup))
