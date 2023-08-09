#Aqui vocês irão colocar seu algoritmo de aprendizado
import connection as cn
import random as rd
import numpy as np

alpha = 0.15


# U(s) = R(s) + γ maxa Σs’ T(s,a,s’) U(s’)
def utilidade_estado(next_st, rec):
    gama = 0.45

    utilidade = rec + gama * max(matriz_utilidade[next_st])
    return utilidade

def melhor_acao(estado):
    if matriz_utilidade[estado, 0] > matriz_utilidade[estado, 1] and matriz_utilidade[estado, 0] > matriz_utilidade[estado, 2]:
        return 0
    elif matriz_utilidade[estado, 1] > matriz_utilidade[estado, 0] and matriz_utilidade[estado, 1] > matriz_utilidade[estado, 2]:
        return 1
    else:
        return 2


matriz_utilidade = np.loadtxt('resultado.txt')
np.set_printoptions(precision=6)


s = cn.connect(2037)
curr_state = 0
curr_reward = -14
acoes = ["left", "right", "jump"]
aleatoriedade = 0.1

while True:
    if rd.random() < aleatoriedade:
        acao = acoes[rd.randint(0, 2)]  # escolher uma acao aleatoria
        print(f'Ação aleatória escolhida para o estado {curr_state}: {acao}')
    else:
        acao = acoes[melhor_acao(curr_state)]
        print(f'Melhor ação escolhida para o estado {curr_state}: {acao}')

    if acao == "left":
        col_acao = 0
    elif acao == "right":
        col_acao = 1
    else:
        col_acao = 2

    estado, recompensa = cn.get_state_reward(s, acao)
    estado = estado[2:]


    # converter o estado e direcao de binario para decimal
    estado = int(estado, 2)
    next_state = estado

    matriz_utilidade[curr_state][col_acao] = matriz_utilidade[curr_state][col_acao] + alpha*(utilidade_estado(next_state, curr_reward) - matriz_utilidade[curr_state][col_acao])

    curr_state = next_state
    curr_reward = recompensa

    np.savetxt('resultado.txt', matriz_utilidade, fmt="%f")
