import os
import openai
import speech_recognition as sr #captar áudio do microfone
from playsound import playsound #tocar áudio
from pathlib import Path 
from io import BytesIO #simula arquivo em memória
from dotenv import load_dotenv 
from gtts import gTTS #transforma texto em áudio

load_dotenv(override=True)

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

arquivo_audio = "files/hello.mp3" 
recognizer = sr.Recognizer()

def grava_audio():
    """Captura áudio do microfone e retorna o áudio gravado"""
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=1) #ajusta o reconhecedor para o ruído ambiente antes de ouvir
        audio =recognizer.listen(source)
    return audio

def transcricao_audio(audio):
    """Transcreve o áudio usando whisper pelo groq"""
    try:
        wav_data = BytesIO(audio.get_wav_data()) #pega os bytes do áudio e o BytesIO transforma isso em arq falso na memória para a API pensar que é um arq(n salva no disco)
        wav_data.name = "audio.wav" #dando nome para o arq
        transcricao = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=wav_data
        )
        return transcricao.text
    except Exception as e:
        print(f"Erro na transcrição do audio {e}")
        return ""

def completa_texto(mensagens):
    """Gera uma resposta usando LLaMA pelo groq"""
    try:
        resposta = client.chat.completions.create(
            messages=mensagens,  #passando o histórico para a API
            model="llama-3.1-8b-instant",
            max_tokens=1000,
            temperature=0
        )
        return resposta.choices[0].message.content
    except Exception as e:
        print(f"Erro na geração de resposta {e}")
        return "Desculpe, não consegui entender"

def cria_audio(texto):
    """Cria áudio a partir do texto usando gTTS"""
    if Path(arquivo_audio).exists():  #transforma ele em um objeto para ver se existe
        Path(arquivo_audio).unlink()  #remove o arquivo anterior se existir pra n acumular
    try:
        tts = gTTS(text=texto, lang="pt")
        tts.save(arquivo_audio) #cria o arquivo hello.mp3 e salva dentro da pasta files
    except Exception as e:
        print(f"Erro na criação de áudio {e}")

def roda_audio():
    """Reproduz o arquivo de áudio gerado"""
    if Path(arquivo_audio).exists():
        playsound(arquivo_audio)
    else:
        print("Erro: O arquivo de áudio não foi encontrado.")

def main():
    """Função principal para executar o assistente de voz"""
    mensagens = [
        {
            "role": "system",
            "content": "Você é um assistente de voz. Responda de forma curta e objetiva, em no máximo 2 frases. Sem listas, sem formatação, só texto direto."
        }
    ]
    while True:
        audio = grava_audio() #grava o que o usuário falou
        transcricao = transcricao_audio(audio) # transcreve o áudio para texto

        if not transcricao:  #se a transcrição falhar, pede para tentar de novo
            print("Não foi possível transcrever o áudio. Tente novamente")
            continue

        mensagens.append({"role": "user", "content": transcricao}) #add a fala do usuário ao histórico
        print(f"Você disse: {transcricao}")

        resposta_texto = completa_texto(mensagens) #gera a resposta com base no histórico completo

        #add a resposta ao histórico
        mensagens.append({"role": "assistant", "content": resposta_texto})
        print(f"Assistente: {resposta_texto}")

        #transforma a resposta em áudio e reproduz
        cria_audio(resposta_texto)
        roda_audio()

if __name__ == "__main__":
    main()