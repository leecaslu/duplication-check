import os
from datetime import date


def report_backup() -> None:
    """Gera um arquivo .txt de backup do report"""
    today = date.today()
    file = os.path.join(
        os.getcwd(),
        "RPA",
        "ChecarDuplicidade" "relatorios",
        f'report_duplicidade{today.strftime("%d.%m.%y")}.txt',
    )
    with open(file, "w+") as wb:
        wb.write("oi")


# RPA\ChecarDuplicidade\relatorios\relatorio_exec_int_01.06.22.csv
print(os.getcwd())
report_backup()
