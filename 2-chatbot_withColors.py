import os
from dotenv import load_dotenv
import openai
from colorama import Fore,Style,init 

load_dotenv(override=True) #carrega as variáveis do arquivo .env (onde fica a chave secreta)

client = openai.OpenAI(   #configura a conexão com a API da Groq, usando a interface da OpenAI (são compatíveis)
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)
#iniciando o colorama
init(autoreset=True)

def geracao_texto(mensagens):
    resposta = client.chat.completions.create(
        messages=mensagens, # envia todo o histórico
        model="llama-3.1-8b-instant",
        max_tokens=1000,
        temperature=0,
        stream=True #dá a resposta enquanto pensa
    )
    print(f"{Fore.MAGENTA}bot:", end="") #faz com que não pule linha na hora mostrar a resposta do bot
    texto_completo = "" #cria um espaço vazio para receber cada palavra e juntar em um texto no final
    for resposta_stream in resposta:
        texto = resposta_stream.choices[0].delta.content #guarda tudo de resposta em texto
        if texto:
            print(texto, end="")
            texto_completo += texto #junta os fragmentos
    print() #pula a linha ao terminar
    mensagens.append({"role": "assistant", "content": texto_completo})
    return mensagens  #add a resposta completa do bot ao histórico e retorna a lista atualizada

if __name__ == "__main__":  # esse bloco só roda se você executar o arquivo diretamente
    print(f"{Fore.YELLOW}bem vindo ao chatbot ! 🤖")
    mensagens = [] #começa de histórico vazio
    while True:   #vai rodando sempre esperando uma pergunta do user
        in_user = input(f"{Fore.CYAN}User:{Style.RESET_ALL} ")
        mensagens.append({"role": "user", "content": in_user})  #salva o histórico de conversa
        mensagens = geracao_texto(mensagens)
