def troca_linha(M, i, j):
    for k in range(len(M[0])):
        M[i][k], M[j][k] = M[j][k], M[i][k]

def multiplica_linha(M, i, c):
    for j in range(len(M[0])):
        M[i][j] *= c

def combina_linha(M, add, mul, c):
    for j in range(len(M[0])):
        M[add][j] += c * M[mul][j]

def escalona(M):
    if len(M) == 0:
        return
    
    num_linhas, num_colunas = len(M), len(M[0])
    i, j = 0, 0

    while True:
        if i >= num_linhas or j >= num_colunas:
            break

        if M[i][j] == 0:
            linha_naozero = i

            while linha_naozero < num_linhas and M[linha_naozero][j] == 0:
                linha_naozero += 1

            if linha_naozero == num_linhas:
                j += 1
                continue

            troca_linha(M, i, linha_naozero)

        for linha in range(i+1, num_linhas):
            if M[linha][j] != 0:
                fator = - (M[linha][j] / M[i][j])
                combina_linha(M, linha, i, fator)

        i, j = i+1, j+1

def numero_pivos(M):
    if len(M) == 0:
        return 0
    
    z, res = [0.0 for _ in range(len(M[0]))], 0
    for i in range(len(M)):
        if M[i] != z:
            res += 1
    return res
