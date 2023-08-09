#Aqui vocês irão colocar seu algoritmo de aprendizado
import connection as cn
import random as rd
import numpy as np

alpha = 0.4


# U(s) = R(s) + γ maxa Σs’ T(s,a,s’) U(s’)
def utilidade_estado(next_st, rec):
    gama = 0.8

    utilidade = rec + gama * max(matriz_utilidade[next_st])
    return utilidade

def melhor_acao(estado):
    if matriz_utilidade[estado, 0] > matriz_utilidade[estado, 1] and matriz_utilidade[estado, 0] > matriz_utilidade[estado, 2]:
        return 0
    elif matriz_utilidade[estado, 1] > matriz_utilidade[estado, 0] and matriz_utilidade[estado, 1] > matriz_utilidade[estado, 2]:
        return 1
    else:
        return 2

# importando a matriz de utilidade
matriz_utilidade = np.loadtxt('resultado.txt')
np.set_printoptions(precision=6)


for line in matriz_utilidade:
    print(line)

s = cn.connect(2037)
curr_state = 84
curr_reward = -3
acoes = ["left", "right", "jump"]
aleatoriedade = 0.4

while True:
    if rd.random() < aleatoriedade:
        acao = acoes[rd.randint(0, 2)]  # escolher uma acao aleatoria
        print(f'Ação aleatória escolhida {acao}')
    else:
        acao = acoes[melhor_acao(curr_state)]
        print(f'Melhor ação escolhida {acao}')

    if acao == "left":
        col_acao = 0
    elif acao == "right":
        col_acao = 1
    else:
        col_acao = 2

    estado, recompensa = cn.get_state_reward(s, acao)
    print(f"a recompensa de chegar em {estado} foi {recompensa}")
    estado = estado[2:]

    # converter o estado e direcao de binario para decimal
    estado = int(estado, 2)
    next_state = estado

    #print("antes:")
    #print(matriz_utilidade[curr_state])

    matriz_utilidade[curr_state][col_acao] = matriz_utilidade[curr_state][col_acao] + alpha*(utilidade_estado(next_state, curr_reward) - matriz_utilidade[curr_state][col_acao])

    #print("depois:")
    #print(matriz_utilidade[curr_state])

    curr_state = next_state
    curr_reward = recompensa

    np.savetxt('resultado.txt', matriz_utilidade, fmt="%f")