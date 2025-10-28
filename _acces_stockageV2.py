import os #Librairie pour interagir avec le système d'exploitation
import s3fs # Librairie pour interagir avec S3
import pandas as pd # Librairie pour la manipulation de données

#Def les codes d'accès
def choix_user_bucket():
    choix = str(input("Voulez vous utiliser le stockage déja configurer ou un autre ? (Conf/Autre) : "))
    if choix.lower() == "autre":
        print("Vous allez devoir rentrer vos codes d'accès à votre S3, acessible dans votre profil")
        os.environ["AWS_ACCESS_KEY_ID"] = str(input("Entrez votre AWS_ACCESS_KEY_ID : "))
        os.environ["AWS_SECRET_ACCESS_KEY"] = str(input("Entrez votre AWS_SECRET_ACCESS_KEY : "))
        os.environ["AWS_SESSION_TOKEN"] = str(input("Entrez votre AWS_SESSION_TOKEN : "))
        os.environ["AWS_DEFAULT_REGION"] = str(input("Entrez votre AWS_DEFAULT_REGION : "))

#Configure l'accès au stockage S3 Onyxia
def connection ():
    fs = s3fs.S3FileSystem(
        client_kwargs={
            'endpoint_url': 'https://minio.lab.incubateur.finances.rie.gouv.fr',
            'verify': False  # Désactive la vérification SSL
        },
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
        token=os.environ["AWS_SESSION_TOKEN"]
    )
    return fs

#Importer des données
def import_csv(file): 
    bucket=str(input("De quel bucket voulez vous importer votre document ? (ID_user/ademe) : "))
    choix_user_bucket()
    fs=connection()
    path=str(bucket+"/"+ file)
    a=str(input("Quel est le type de séparateur ? (,/;) : "))
    with fs.open(path, mode="r") as file_in:
        df = pd.read_csv(file_in, sep=a) 
    return df

def import_db(file):
    choix_user_bucket()
    fs=connection()
    bucket=str(input("De quel bucket voulez vous importer votre document ? (ID_user/ademe) : "))
    path=str(bucket+"/"+ file)
    import sqlite3
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        #Télécharger la base depuis S3
        tmp.write(fs.open(path, "rb").read())
        tmp_path = tmp.name
    #Connexion à la base locale temporaire
    conn = sqlite3.connect(tmp_path)
    table_name = input("Nom de la table précisément à importer : ")
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


#Exporter données
def export_csv (df):
    name=str(input("Quel nom à donner au fichier ? (name.csv) : "))
    bucket=str(input("Dans quel bucket voulez vous exporter votre document ? (ID_user/ademe) : "))
    mode_write=str(input("Voulez vous écraser le précedent fichier ou simplement ajouter celui-ci ? (w/a) : "))
    choix_user_bucket()
    fs=connection()
    path=str(bucket+"/"+ name)
    with fs.open(path, mode=mode_write) as file_out:
        df.to_csv(file_out, sep=";", index=False) #pour CSV, adapter si autre format
    print(f"Fichier exporté vers s3://{path}") #Confirmation de l'exportation

def export_db(local_db):
    name=str(input("Quel nom à donner au fichier ? (name.db) : "))
    bucket = input("Dans quel bucket voulez-vous exporter votre base ? (ID_user/ademe) : ")
    choix_user_bucket()
    fs = connection()
    path = f"{bucket}/{name}"  # inclure .db si souhaité
    with open(local_db, "rb") as src, fs.open(path, "wb") as dst:
        dst.write(src.read())
    print(f"Base exportée vers s3://{path}")