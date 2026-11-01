import pandas as pd 
from src.quality import checar 

def _df(datas, valores):
    return pd.DataFrame(
        {"serie": 433, "data": pd.to_datetime(datas), "valor": valores}
    )


def test_dados_validos_nao_tem_problemas():
    assert checar(_df(["2025-01-01", "2025-02-01"], [0.16, 0.31])) == []


def test_detecta_data_repetida():
    problemas = checar(_df(["2025-01-01", "2025-01-01"], [0.16, 0.16]))
    assert "há datas repetidas na mesma série" in problemas


def test_detecta_valor_nulo():
    problemas = checar(_df(["2025-01-01"], [None]))
    assert "há valores nulos ou inválidos" in problemas