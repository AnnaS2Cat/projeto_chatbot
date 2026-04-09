import csv
import random
from faker import Faker
from datetime import datetime, timedelta

# Inicializar a biblioteca Faker
fake = Faker()

# Função para gerar dados fictícios
def generate_data():
    invoice_id = fake.uuid4()[:8]
    branch = random.choice(["A", "B", "C"])
    city = random.choice(["City A", "City B", "City C"])
    customer_type = random.choice(["Member", "Normal"])
    gender = random.choice(["Male", "Female"])
    product_line = random.choice([
        "Health and beauty",
        "Electronic accessories",
        "Home and lifestyle",
        "Sports and travel",
        "Food and beverages",
        "Fashion accessories",
    ])
    unit_price = round(random.uniform(10, 100), 2)
    quantity = random.randint(1, 10)
    tax = round((unit_price * quantity) * 0.05, 2)
    total = round((unit_price * quantity) + tax, 2)
    date = fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d")
    time = fake.time(pattern="%H:%M:%S")
    payment = random.choice(["Cash", "Credit card", "Ewallet"])
    cogs = round(unit_price * quantity, 2)
    gross_margin_percentage = 4.76  # Valor fixo conforme especificação
    gross_income = tax  # Taxa de 5% é o lucro bruto
    rating = round(random.uniform(4, 10), 1)

    return [
        invoice_id,
        branch,
        city,
        customer_type,
        gender,
        product_line,
        unit_price,
        quantity,
        tax,
        total,
        date,
        time,
        payment,
        cogs,
        gross_margin_percentage,
        gross_income,
        rating,
    ]

# Cabeçalho do arquivo CSV
header = [
    "Invoice ID",
    "Branch",
    "City",
    "Customer type",
    "Gender",
    "Product line",
    "Unit price",
    "Quantity",
    "Tax 5%",
    "Total",
    "Date",
    "Time",
    "Payment",
    "cogs",
    "gross margin percentage",
    "gross income",
    "Rating",
]

# Gerar e salvar os dados em um arquivo CSV
with open("sales_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)

    for _ in range(300):
        writer.writerow(generate_data())

print("Arquivo 'sales_data.csv' gerado com sucesso!")

