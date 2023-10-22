import csv
import random

from utils import extract_float

# Carregar os dados do CSV original
with open('main-dataset-2021.csv', 'r') as f:
    reader = csv.DictReader(f)
    jogadores = list(reader)

# Atualizar os valores
for jogador in jogadores:
    for key in [
        'Gls', 'Ast', 'SoT', 'MP', 'Starts', 'Int', 'Blocks', 'CrdY', 'CrdR',
        'Min', 'Passes Attempted', 'Cmp%', 'Market value'
    ]:
        # Suponha que cada métrica pode aumentar de 0% a 10% em um ano
        aumento_percentual = 1 + random.uniform(0, 1)
        if key == 'Market value':
            jogador[key] = f"{float(extract_float(jogador[key]) * aumento_percentual)}s"
            continue
        value = str(float(jogador[key] or 0) * aumento_percentual)
        jogador[key] = value

# Escrever os novos dados em um novo arquivo CSV
with open('main-dataset-2022.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=jogadores[0].keys())
    writer.writeheader()
    for jogador in jogadores:
        writer.writerow(jogador)
