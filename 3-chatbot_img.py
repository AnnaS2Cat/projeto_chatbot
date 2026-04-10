import os
import requests
from dotenv import load_dotenv
import openai
from colorama import Fore, Style, init

load_dotenv(override=True)

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

init(autoreset=True)

#palavras que indicam que quer uma imagem
GATILHOS_IMAGEM = ["gera uma imagem", "crie uma imagem", "desenha", "gerar imagem", "cria uma imagem", "me mostra uma imagem"]

def gerar_imagem(prompt):
    print(f"{Fore.MAGENTA}bot: gerando imagem, aguarde...")
    
    token = os.environ.get("HF_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    # salva a imagem
    os.makedirs("files", exist_ok=True)
    nome_arquivo = f"files/imagem_gerada.png"
    with open(nome_arquivo, "wb") as f:
        f.write(response.content)
    
    print(f"{Fore.MAGENTA}bot: imagem salva em '{nome_arquivo}' ✅")

def geracao_texto(mensagens):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model="llama-3.1-8b-instant",
        max_tokens=1000,
        temperature=0,
        stream=True
    )
    print(f"{Fore.MAGENTA}bot:", end="")
    texto_completo = ""
    for resposta_stream in resposta:
        texto = resposta_stream.choices[0].delta.content
        if texto:
            print(texto, end="")
            texto_completo += texto
    print()
    mensagens.append({"role": "assistant", "content": texto_completo})
    return mensagens

if __name__ == "__main__":
    print(f"{Fore.YELLOW}bem vindo ao chatbot ! 🤖")
    mensagens = []
    while True:
        in_user = input(f"{Fore.CYAN}User:{Style.RESET_ALL} ")
        
        if any(gatilho in in_user.lower() for gatilho in GATILHOS_IMAGEM): #verifica se a pessoa quer uma imagem
            gerar_imagem(in_user)
        else:
            mensagens.append({"role": "user", "content": in_user})
            mensagens = geracao_texto(mensagens)