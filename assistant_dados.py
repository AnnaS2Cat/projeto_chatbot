import os
from dotenv import load_dotenv
import openai
import pandas as pd

load_dotenv(override=True)  #carrega a chave da API do arquivo .env
client= openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

df =pd.read_csv("sales_data.csv")  #lê o csv gerado pelo faker com os 300 registros de vendas

ranking = (   #calcula o ranking médio de vendas por categoria direto no pandas
    df.groupby("Product line")["Total"]  #agrupa por linha de produto
    .mean()                              # calcula a média de vendas de cada uma
    .sort_values(ascending=False)        # ordena da que vende mais para a que vende menos
)

ranking_texto= ranking.to_string() #transformei o resultado em texto para poder mandar na mensagem

#monta um resumo completo com os números já calculados e a ia explica
total_vendas = df["Total"].sum()
media_vendas = df["Total"].mean()

resumo_negocio =f"""
Total geral de vendas: {total_vendas:.2f}
Média de vendas por transação: {media_vendas:.2f}
Ranking médio de vendas por categoria:
{ranking_texto}
"""

#a ia interpreta os dados, só lê os resultados e gera insights
resposta = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "Você é um analista de dados. Explique os resultados de forma clara, objetiva e com insights de negócio."},
        {"role": "user",
            # manda o resumo processado sem dados brutos
            "content": f"Analise os seguintes dados de vendas e gere insights:\n\n{resumo_negocio}"}
    ]
)
print(resposta.choices[0].message.content)