import json 
from datetime import date
from pathlib import Path
import requests #requests: permite fazer requisições HTTP, ou seja, conversar com APIs pela internet.

BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
#trecho {codigo}. Ele funciona como um espaço reservado que será substituído pelo número da série desejada.

def buscar_serie(codigo, inicio, fim): 
    url = BASE.format(codigo=codigo)
    params = {"formato": "json", "dataInicial": inicio, "dataFinal": fim}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def salvar_raw(codigo, dados):
    pasta = Path(f"data/raw/serie={codigo}/ingestao={date.today()}")
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = pasta / "dados.json"
    arquivo.write_text(json.dumps(dados, ensure_ascii=False))
    return arquivo

if __name__ == "__main__":
    dados = buscar_serie(433, "01/01/2020", "31/12/2025")
    print(salvar_raw(433, dados), len(dados),"registros")


''' if __name__ == "__main__": é uma convenção do Python usada para definir o ponto
 de entrada de um programa.

Isso permite reutilizar funções do arquivo sem disparar código de teste ou execução 
automática.
'''