"""Arquivo que vai verificar a data e retornar a ação a ser feita de acordo com o dia"""

from datetime import date


def check_data() -> str:
    data = date.today()
    dia_mes = data.day
    dia_semana = data.weekday()
    if dia_semana in [5, 6]:
        return '0'
    if dia_mes > 26:
        return '1'
    return '2'
