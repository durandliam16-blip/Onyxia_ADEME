import duckdb
import pandas as pd

conn = duckdb.connect() #temporary in memory if nothing in ()
cols = conn.execute("""
    SELECT * 
    FROM read_csv_auto('~/work/Sport_predict/run_result.csv', header=True)
    LIMIT 0
""").df().columns
print(cols)

result = conn.execute("""
    SELECT REPLACE(Vitesse, ',', '.')::FLOAT AS Vivi, *
    FROM read_csv_auto('~/work/Sport_predict/run_result.csv', header=True)
    LIMIT 3
    OFFSET 10;
    """).df() #to have dataframe
#if simple file ou dataset/*.csv si dossier de tables
print(result)

conn.register("view",result)
print(conn.execute("DESCRIBE view").df())
print(conn.execute("""SELECT * FROM result WHERE "Vitesse">14.0 """).df())