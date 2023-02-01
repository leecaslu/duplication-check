import sys
from navegador import Usuario
import registro
from datetime import date
import os


def main() -> None:
  # declarando variáveis
  email = "svc.rpaeo@vcimentos.com"
  user = "svc.rpaeo"
  senha = "Suporte@26"
  planilha_dupli = os.path.join(
    os.sep + os.sep + "brcwbwvfs01vc",
    "COMERCIA",
    "Relatorios",
    "50 - CAC",
    "Gestão EO",
    "JS+",
    "Remoção Duplicidades",
    "Análise micro X produto LV",
    "Base_Consulta_Duplicidade_LV.xlsx",
  )
  # Criando o usuário com o driver
  conectado = Usuario(username=user, password=senha, email=email, proxy_con=False, proxy="")
  
  res = tuple(range(0, 6))
  dia = date.today()
  dia_semana = dia.weekday()

  if dia_semana in res:
    clientes = registro.geracao_vistoria_diaria(planilha_dupli, dia_semana) # 100 clientes/dia
  else:
    sys.exit()

  # clientes = registro.geracao_relatorio_mensal(planilha_dupli) # 470 clientes de uma vez
  conectado.login_lv()
  count = 0
  while (len(list(filter(lambda c: not c.verificado, clientes))) > 0) and (count < 5):
    for indice, cliente in enumerate(clientes):
      if not cliente.verificado:
        clientes[indice] = conectado.checando_duplicidade(cliente)
    count += 1
  conectado.driver.close()

  dup = registro.report_duplicidade(clientes=clientes, plan=planilha_dupli)
  registro.criando_relatorio_exec_int(clientes)
  registro.report_backup(clientes)
  print(
    registro.enviar_email(
      len(clientes), emails=lista_emails, plan=planilha_dupli, dupli=dup
    )
  )


if __name__ == "__main__":
  main()
