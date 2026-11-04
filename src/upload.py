import argparse
from pathlib import Path 

from src.storage import cliente_s3


def enviar_pasta(s3, bucket: str, pasta_local: Path, prefixo: str) -> int:
    total = 0
    for arquivo in pasta_local.rglob("*"):
        if arquivo.is_file():
            chave = f"{prefixo}/{arquivo.relative_to(pasta_local).as_posix()}"
            s3.upload_file(str(arquivo),bucket, chave)
            total += 1
    return total

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True)
    args = parser.parse_args()

    s3 = cliente_s3()
    for camada in ("raw", "curated"):
        n = enviar_pasta(s3, args.bucket, Path("data") / camada, camada)
        print(f"{camada}: {n} arquivos enviados")