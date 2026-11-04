import sys

from src.storage import cliente_s3

bucket = sys.argv[1]
s3 = cliente_s3()
existentes = [b["Name"] for b in s3.list_buckets()["Buckets"]]
if bucket in existentes:
    print(f"Bucket {bucket} já existe")
else:
    s3.create_bucket(Bucket=bucket)
    print(f"Bucket {bucket} criado")