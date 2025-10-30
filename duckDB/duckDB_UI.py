import streamlit as st
import duckdb
import pandas as pd
import os

st.set_page_config(page_title="DuckDB UI", layout="wide")

st.title("🦆 DuckDB – Interface Web légère")

db_path = st.text_input("Chemin vers la base (.duckdb)", "mydb.duckdb")

if not os.path.exists(db_path):
    st.warning("La base n’existe pas encore — elle sera créée à la première requête.")

query = st.text_area("Écris ta requête SQL :", "SELECT * FROM sqlite_master;")

if st.button("Exécuter la requête"):
    try:
        con = duckdb.connect(database=db_path)
        df = con.execute(query).fetchdf()
        st.dataframe(df)
    except Exception as e:
        st.error(f"Erreur : {e}")