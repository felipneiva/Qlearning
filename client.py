#Aqui vocês irão colocar seu algoritmo de aprendizado
import connection as cn
import random as rd

alpha = 0.1


# U(s) = R(s) + γ maxa Σs’ T(s,a,s’) U(s’)
def utilidade_estado(next_st, rec):
    gama = 0.9

    utilidade = rec + gama * max(matriz_utilidade[next_st])
    return utilidade

def melhor_acao(estado):
    melhor_escolha = matriz_utilidade[estado].index(max(matriz_utilidade[estado]))

    if melhor_escolha == 0:
        matriz_escolha = [
            0,
            0,
            0,
            0,
            0,
            1,
            2,
            1,
            2,
            1]
    elif melhor_escolha == 1:
        matriz_escolha = [
            1,
            1,
            1,
            1,
            1,
            2,
            1,
            2,
            1,
            2]
    else:
        matriz_escolha = [
            2,
            2,
            2,
            2,
            2,
            2,
            1,
            2,
            1,
            2]
    
    
    #return matriz_escolha[rd.randint(0, 9)]
    return melhor_escolha

# criando a matriz de utilidade, inicializando todas as acoes dos estados com 0
""" matriz_utilidade = []
for i in range(96):
    row = []

    for j in range(3):
        row.append(0)

    matriz_utilidade.append(row) """

with open('resultado.txt','r') as f:
    matriz_utilidade = [[float(num) for num in line.split(' ')] for line in f]

    f.close()

for line in matriz_utilidade:
    print(line)

s = cn.connect(2037)
curr_state = 92
curr_reward = -1
acoes = ["left", "right", "jump"]

while True:
    #acao = acoes[rd.randint(0, 2)]  # escolher uma acao aleatoria

    acao = acoes[melhor_acao(curr_state)]

    #print(acao)

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

    #print("antes:")
    #print(matriz_utilidade[curr_state])

    matriz_utilidade[curr_state][col_acao] = matriz_utilidade[curr_state][col_acao] + alpha*(utilidade_estado(next_state, curr_reward) - matriz_utilidade[curr_state][col_acao])

    #print("depois:")
    #print(matriz_utilidade[curr_state])

    curr_state = next_state
    curr_reward = recompensa

    with open('resultado.txt','w') as f:
        for line in matriz_utilidade:
            f.write(' '.join(str(q) for q in line) + '\n')

        f.close()