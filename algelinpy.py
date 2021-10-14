def troca_linha(M, i, j):
    M[i], M[j] = M[j], M[i]

def multiplica_linha(M, i, c):
    for j in range(len(M[0])):
        M[i][j] *= c

def combina_linha(M, add, mul, c):
    for j in range(len(M[0])):
        M[add][j] += c * M[mul][j]

def escalona(M):
    """Escalonamento por linha, ie, diagonal inferior vira 0."""
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
    """Conta o número de pivôs da matriz M.

    Lembrando que, se a matriz M estiver escalonada,
    o número de pivôs é o mesmo que a dimensão da
    imagem dessa matriz.
    """
    if len(M) == 0:
        return 0

    linha_de_zeros = [0.0 for _ in range(len(M[0]))]
    dim = 0
    
    for i in range(len(M)):
        if M[i] != linha_de_zeros:
            dim += 1

    return dim
