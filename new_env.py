import requests
import os

API_URL = "https://mon-onyxia.example.com/api" #A adapter selon l'instance Onyxia, trouer url api
TOKEN = os.environ["ONYXIA_TOKEN"] #déclarer ? 

payload = {
    "regionId": "demo",
    "serviceId": "jupyterlab",
    "version": "latest",
    "name": "env_test", 
    "parameters": {
        "cpu": 2,
        "memory": "4Gi"
    }
}

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

resp = requests.post(f"{API_URL}/my-lab/environments",
                     headers=headers,
                     json=payload,
                     verify=False)  # (à ajuster selon SSL)

if resp.status_code == 201:
    print("Environnement créé :", resp.json())
else:
    print("Erreur", resp.status_code, resp.text)