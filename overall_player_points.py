import math

# Pesos para cada métrica
attributes_weights = {
    'Gls': 5,
    'Ast': 4,
    'G/Sh': 3,
    'Ast90': 3,
    'Cmp%': 2,
    'Tackle': 2,
    'Succ_x': 2,
    'Int': 1,
    'Blocks': 1
}


# Definindo a função de pontuação bruta
def raw_points(player):
    points = 0
    for metrica, peso in attributes_weights.items():
        points += player[metrica] * peso
    return points


# Função Sigmoide
def sigmoide(x):
    return 1 / (1 + math.exp(-x))


# Função para calcular a pontuação final usando sigmoide
def calc_overall_player_points(player):
    # Calcule a pontuação bruta
    points = raw_points(player)

    # Escalona usando a função sigmoide e multiplica por 100
    staggered_points = sigmoide(points / 100.0) * 100  # Dividimos por 100 para ajustar a escala da entrada

    return staggered_points
