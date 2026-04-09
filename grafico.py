import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sales_data.csv")

vendas_por_linha = df.groupby("Product line")["Total"].sum()
percentual = (vendas_por_linha / vendas_por_linha.sum()) * 100

plt.figure(figsize=(10, 8))
plt.pie(percentual, labels=percentual.index, autopct='%1.1f%%')
plt.title("Percentual de vendas por linha de produto")
plt.show()