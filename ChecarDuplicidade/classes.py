from dataclasses import dataclass

# Client login code, verification status and data
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
