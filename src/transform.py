import json
import shutil #operações em arquivos e diretórios, como copiar, mover, apagar árvores de pastas e criar arquivos compactados.
from pathlib import Path

import pandas as pd
from src.quality import checar

RAW = Path("data/raw")
CURATED = Path("data/curated/ipca")

def carregar_raw() -> pd.DataFrame:
    partes = []
    for arquivo in RAW.glob("serie=*/ingestao=*/dados.json"):
        serie = int(arquivo.parent.parent.name.split("=")[1])
        ingestao = arquivo.parent.name.split("=")[1]
        df = pd.DataFrame(json.loads(arquivo.read_text()))
        df["serie"] = serie
        df["ingestao"] = ingestao
        partes.append(df)
    return pd.concat(partes, ignore_index=True)

def transformar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df.sort_values(["serie", "data","ingestao"])
    df = df.drop_duplicates(subset=["serie", "data"], keep="last")
    df["ano"] = df["data"].dt.year
    return df.drop(columns=["ingestao"]).reset_index(drop=True)


def salvar(df: pd.DataFrame) -> None:
    if CURATED.exists():
        shutil.rmtree(CURATED)
    df.to_parquet(CURATED, partition_cols=["ano"], index=False, engine="pyarrow")


if __name__ == "__main__":
    df = transformar(carregar_raw())
    problemas = checar(df)
    if problemas:
        raise SystemExit("Problemas de qualidade:\n- " + "\n- ".join(problemas))
    salvar(df)
    print(f"{len(df)} registros salvos em {CURATED}")