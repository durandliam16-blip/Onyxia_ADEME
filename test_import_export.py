import _acces_stockageV2 as acces

#Test1
import pandas as pd
df_test = pd.DataFrame({'nom': ['Alice', 'Bob'], 'age': [25, 30]})
df_test.to_csv('test.csv', sep=';', index=False)
acces.export_csv(df_test)

#Test2
import sqlite3
import pandas as pd
# Création de la base
conn = sqlite3.connect("test.db")
cur = conn.cursor()
# Création d'une table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    nom TEXT,
    age INTEGER
)
""")
# Insertion de données
cur.execute("INSERT INTO users (nom, age) VALUES (?, ?)", ("Alice", 25))
cur.execute("INSERT INTO users (nom, age) VALUES (?, ?)", ("Bob", 30))
# Valider et fermer
conn.commit()
conn.close()
# Vérification avec pandas
conn = sqlite3.connect("test.db")
df_test = pd.read_sql_query("SELECT * FROM users", conn)
conn.close()
print(df_test)
acces.export_db("test.db")

#Test3
print(acces.import_db("test.db"))