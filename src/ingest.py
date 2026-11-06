import json 
import time
from datetime import date
from pathlib import Path

import requests #requests: permite fazer requisições HTTP, ou seja, conversar com APIs pela internet.

BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
#trecho {codigo}. Ele funciona como um espaço reservado que será substituído pelo número da série desejada.

SERIES = {433: "ipca_mensal", 432: "selic_meta", 1 : "dolar_compra"}
ANO_INICIAL = 2015

def buscar_periodo(codigo, inicio, fim):
    params = {"formato": "json", "dataInicial": inicio, "dataFinal": fim}
    resp = requests.get(BASE.format(codigo=codigo), params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def buscar_serie(codigo, ano_inicial, ano_final): 
   dados = []
   for ano in range(ano_inicial, ano_final + 1):
      dados += buscar_periodo(codigo, f"01/01/{ano}", f"31/12/{ano}")
      time.sleep(0.3)
   return dados


def salvar_raw(codigo, dados):
    pasta = Path(f"data/raw/serie={codigo}/ingestao={date.today()}")
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = pasta / "dados.json"
    arquivo.write_text(json.dumps(dados, ensure_ascii=False))
    return arquivo

if __name__ == "__main__":
    ano_final = date.today().year 
    for codigo, nome in SERIES.items():
        dados = buscar_serie(codigo, ANO_INICIAL, ano_final)
        print(salvar_raw(codigo, dados), len(dados),"registros")

''' if __name__ == "__main__": é uma convenção do Python usada para definir o ponto
 de entrada de um programa.

Isso permite reutilizar funções do arquivo sem disparar código de teste ou execução 
automática.
'''