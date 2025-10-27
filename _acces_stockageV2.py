import os #Librairie pour interagir avec le système d'exploitation
import s3fs # Librairie pour interagir avec S3
import pandas as pd # Librairie pour la manipulation de données
print("test")

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
def import_csv (bucket, file,mode_open): 
#Nom du bucket (ademe ou user ex ldurand) - doc_name.type - mode_open qui est r pour lecture seule ou rb pour binaire
    choix_user_bucket()
    fs=connection()
    path=str(bucket+"/"+ file)
    with fs.open(path, mode=mode_open) as file_in:
        df = pd.read_csv(file_in, sep=";") #pour CSV, adapter si autre format
    return df

#Exporter données
def export_csv (bucket, df, mode_write):
#Nom du bucket (ademe ou user ex ldurand) - Dataframe à exporter - mode_write qui est w pour écraser ou a pour ajouter
    choix_user_bucket()
    fs=connection()
    path=str(bucket+"/"+ df)
    with fs.open(path, mode=mode_write) as file_out:
        df.to_csv(file_out, sep=";", index=False) #pour CSV, adapter si autre format

    print(f"Fichier exporté vers s3://{path}") #Confirmation de l'exportation
