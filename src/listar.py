import sys

from src.storage import cliente_s3

bucket = sys.argv[1]
s3 = cliente_s3()
paginador = s3.get_paginator("list_objects_v2")
for pagina in paginador.paginate(Bucket=bucket):
    for obj in pagina.get("Contents", []):
        print(obj["Key"], obj["Size"])