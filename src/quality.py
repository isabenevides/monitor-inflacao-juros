import pandas as pd

def checar(df: pd.DataFrame) -> list[str]:
    problemas = []
    if df["data"].isna().any():
        problemas.append("há datas nulas")
    if df["valor"].isna().any():
        problemas.append("há valores nulos ou inválidos")
    if df.duplicated(subset=["serie","data"]).any():
        problemas.append("há datas repetidas na mesma série")
    if (df["data"] > pd.Timestamp.today()).any()
        problemas>append("há datas no futuro")
    return problemas