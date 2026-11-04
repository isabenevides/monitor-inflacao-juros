import duckdb

con = duckdb.connect()
con.sql("INSTALL httpfs; LOAD httpfs;")
con.sql("""
    CREATE OR REPLACE SECRET local_s3 (
        TYPE S3, KEY_ID 'local', SECRET 'local',
        ENDPOINT 'localhost:8333', USE_SSL false, URL_STYLE 'path'
    )
""")

TABELA = ("read_parquet('s3://monitor-inflacao-juros/curated/ipca/*/*.parquet', "
          "hive_partitioning = true)")

print(con.sql(f"""
    SELECT ano, ROUND(AVG(valor), 2) AS media_mensal, COUNT(*) AS meses
    FROM {TABELA}
    GROUP BY ano ORDER BY ano
""").df())

print(con.sql(f"""
    SELECT ano,
           ROUND(AVG(valor), 2) AS media_mensal,
           COUNT(*) AS meses
    FROM {TABELA}
    GROUP BY ano
    ORDER BY ano
""").df())

print(con.sql(f"""
    WITH j AS (
        SELECT data, valor,
               SUM(LN(1 + valor / 100)) OVER w AS soma_ln,
               COUNT(*) OVER w AS n
        FROM {TABELA}
        WINDOW w AS (
            ORDER BY data
            ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
        )
    )
    SELECT data,
           valor AS ipca_mes,
           ROUND((EXP(soma_ln) - 1) * 100, 2) AS ipca_12m
    FROM j
    WHERE n = 12
    ORDER BY data
""").df())