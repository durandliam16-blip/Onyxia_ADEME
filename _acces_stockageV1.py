import os #Library pour interagir avec le système d'exploitation
import s3fs # Librairie pour interagir avec S3
import pandas as pd # Library pour la manipulation de données


## 4 lignes suivantes à modifier :
# Si S3 déja configurer dans vm, supprimer les lignes suivantes
#Si pas de connexion, remplacer les 4 lignes suivantes par les lignes 3 à 6 de 
    #votre profil puis Connexion puis Python(s3fs)

os.environ["AWS_ACCESS_KEY_ID"] = ''
os.environ["AWS_SECRET_ACCESS_KEY"] = ''
os.environ["AWS_SESSION_TOKEN"] = ''
os.environ["AWS_DEFAULT_REGION"] = ''


#Configurer l'accès au stockage S3 Onyxia (MinIO)

fs = s3fs.S3FileSystem(
    client_kwargs={
        'endpoint_url': 'https://minio.lab.incubateur.finances.rie.gouv.fr',
        'verify': False  # Désactive la vérification SSL
    },
    key=os.environ["AWS_ACCESS_KEY_ID"],
    secret=os.environ["AWS_SECRET_ACCESS_KEY"],
    token=os.environ["AWS_SESSION_TOKEN"]
)


#Importer des données

BUCKET = "" #Nom du bucket Onyxia donc ademe ou votre nom d'utilisateur
FILE_KEY_S3 = ""  # doc_name.type
FILE_PATH_S3 = BUCKET + "/" + FILE_KEY_S3

with fs.open(FILE_PATH_S3, mode="rb") as file_in: #Ouverture du fichier en mode lecture 
    df_bpe = pd.read_csv(file_in, sep=";") #pour CSV, adapter si autre format
print(df_bpe)


#Exporter données

BUCKET = "ademe" #Nom du bucket Onyxia donc ademe ou votre nom d'utilisateur
FILE_KEY = "" # doc_name.type
FILE_PATH_S3 = f"{BUCKET}/{FILE_KEY}"
df = pd.DataFrame({"a": [1, 2], "b": [3, 4]}) #Exemple à exporter

with fs.open(FILE_PATH_S3, mode="a") as f: #Mettre 'w' au lieud de 'a' pour écraser le fichier existant
    df.to_csv(f, sep=";", index=False) #pour CSV, adapter si autre format
print(f"Fichier exporté vers s3://{FILE_PATH_S3}") #Confirmation de l'exportation