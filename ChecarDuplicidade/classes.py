from dataclasses import dataclass

# Dados do cliente: Duplicidade para cimentos todas as obras e estrutural, CNPJ e microrregiao,
# códigos dos produtos que ele tem
@dataclass
class DadosCliente:
    identificacao: tuple
    cimento_todas_obras: dict
    cimento_estrutural: dict
    codigos_analisados: list
    verificado: bool = False

@dataclass
class DadosProduto:
    codigo: str
    micros_sanear: list
    inativar: bool = False
