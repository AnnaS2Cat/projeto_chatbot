import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

token= os.environ.get("HF_TOKEN")
headers = {"Authorization": f"Bearer {token}"}

API_URL= "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

prompt="Crie uma imagem com dois robôs em uma praia lendo livro de finanças"
nome = "robo_praia"
response = requests.post(API_URL, headers=headers, json={"inputs": prompt}) #gera a imagem

os.makedirs("files", exist_ok=True) # salva o arquivo
nome_arquivo = f"files/{nome}.png"
with open(nome_arquivo, "wb") as f:
    f.write(response.content)

print(f"Imagem salva em {nome_arquivo}")