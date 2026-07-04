import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
import random

# ===============================
# Estados
# ===============================
SUSCETIVEL = 0
INFECTADO = 1
RECUPERADO = 2
MORTO = 3

# ===============================
# Parâmetros
# ===============================
TAMANHO = 60

PROB_INFECCAO = 0.30

TEMPO_RECUPERACAO = 12

PROB_MORTE = 0.05

ITERACOES = 120

INFECTADOS_INICIAIS = 5

# ===============================
# Inicialização
# ===============================

grade = np.zeros((TAMANHO, TAMANHO), dtype=int)

tempo_infectado = np.zeros((TAMANHO, TAMANHO), dtype=int)

for _ in range(INFECTADOS_INICIAIS):
    x = random.randint(0, TAMANHO - 1)
    y = random.randint(0, TAMANHO - 1)

    grade[x, y] = INFECTADO

# Histórico

historico_s = []
historico_i = []
historico_r = []
historico_d = []

# ===============================
# Vizinhança de Moore
# ===============================

def possui_vizinho_infectado(x, y):

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:

            if dx == 0 and dy == 0:
                continue

            nx = x + dx
            ny = y + dy

            if 0 <= nx < TAMANHO and 0 <= ny < TAMANHO:

                if grade[nx, ny] == INFECTADO:
                    return True

    return False


# ===============================
# Atualização
# ===============================

def atualizar(frame):

    global grade
    global tempo_infectado

    nova_grade = grade.copy()
    novo_tempo = tempo_infectado.copy()

    for i in range(TAMANHO):
        for j in range(TAMANHO):

            estado = grade[i, j]

            # Suscetível
            if estado == SUSCETIVEL:

                if possui_vizinho_infectado(i, j):

                    if random.random() < PROB_INFECCAO:

                        nova_grade[i, j] = INFECTADO
                        novo_tempo[i, j] = 0

            # Infectado
            elif estado == INFECTADO:

                novo_tempo[i, j] += 1

                if novo_tempo[i, j] >= TEMPO_RECUPERACAO:

                    if random.random() < PROB_MORTE:

                        nova_grade[i, j] = MORTO

                    else:

                        nova_grade[i, j] = RECUPERADO

    grade = nova_grade
    tempo_infectado = novo_tempo

    historico_s.append(np.sum(grade == SUSCETIVEL))
    historico_i.append(np.sum(grade == INFECTADO))
    historico_r.append(np.sum(grade == RECUPERADO))
    historico_d.append(np.sum(grade == MORTO))

    imagem.set_array(grade)

    ax.set_title(f"Iteração {frame}")

    return [imagem]

# ===============================
# Visualização
# ===============================

cores = ListedColormap([
    "green",      # Suscetível
    "red",        # Infectado
    "blue",       # Recuperado
    "black"       # Morto
])

fig, ax = plt.subplots(figsize=(7,7))

imagem = ax.imshow(
    grade,
    cmap=cores,
    vmin=0,
    vmax=3
)

ax.set_xticks([])
ax.set_yticks([])

animacao = FuncAnimation(
    fig,
    atualizar,
    frames=ITERACOES,
    interval=120,
    repeat=False
)

plt.show()

# ===============================
# Gráfico
# ===============================

plt.figure(figsize=(10,5))

plt.plot(historico_s, label="Suscetíveis")
plt.plot(historico_i, label="Infectados")
plt.plot(historico_r, label="Recuperados")
plt.plot(historico_d, label="Mortos")

plt.xlabel("Iterações")
plt.ylabel("Quantidade de células")

plt.title("Evolução da Epidemia")

plt.legend()

plt.grid(True)

plt.show()
