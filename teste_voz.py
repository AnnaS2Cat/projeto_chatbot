import os
from gtts import gTTS
from dotenv import load_dotenv
import openai

load_dotenv(override=True)

client = openai.OpenAI(    #groq para transcrição
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)
texto = """
    Olá! Eu sou um chatbot inteligente desenvolvido em Python. Posso responder perguntas, ter conversas naturais e até gerar imagens para você. 
Para conversar comigo, basta digitar sua mensagem. Se quiser uma imagem, é só pedir: gera uma imagem de uma garota segurando uma flor, por exemplo.
Fui desenvolvido usando a API da Groq com o modelo LLaMA, e para imagens uso o Hugging Face de forma totalmente gratuita.
"""

# síntese de voz, de texto para áudio gtts
os.makedirs("files", exist_ok=True)
arquivo = "files/voz.mp3"
tts = gTTS(text=texto, lang="pt")
tts.save(arquivo)
print(f"Áudio salvo em '{arquivo}'")

#transcrição, de áudio para texto groq whisper
audio = open(arquivo, "rb")
transcricao = client.audio.transcriptions.create(
    model="whisper-large-v3",
    file=audio,
    prompt="transcrição de um texto sobre o chatbot da Anna"
)
print("\nTranscrição:")
print(transcricao.text)