"""Calcula os grupos de homologia de um complexo simplicial."""

import algelinpy


def sublistas(lista):
    """Retorna todas as sublistas de uma lista com o conjunto vazio no final."""
    if len(lista) == 0:
        return [[]]
    primeiro = lista[0]
    subpartes = sublistas(lista[1:])
    return [[primeiro] + x for x in subpartes] + subpartes

class ComplexoSimplicial():
    def __init__(self, nome, complexo):
        if isinstance(nome, str) is False:
            raise Exception("Nome deve ser uma string.")
        if ComplexoSimplicial._verifica_complexo(complexo) is False:
            raise Exception("O complexo informado não satisfaz os axiomas.")
        self.nome = nome
        self.complexo = complexo
        self.dimensao = len(max(self.complexo, key=len)) - 1

    def __repr__(self):
        return f'Espaço: {self.nome}\n\
Dimensão: {self.dimensao}\n\
Característica de Euler: {self.caracteristica_de_euler()}\n\
Números de Betti: {self.homologia()}\n'

    def _verifica_complexo(complexo):
        """Verifica se o complexo digitado satisfaz os axiomas.

        Essencialmente os axiomas são: a lista deve ser ordenada (definição
        de orientação) e todas as faces de um simplexo devem estar no
        complexo. Se tiver face repetida, aviso o usuário. A face repetida
        aparece na lista freq, que marca se o simplexo já apareceu ou não.
        Também verifico se os vértices dos simplexos são inteiros, ie, se
        foi digitado [0,1,2] ao invés de ["0","1","2"], por exemplo. E
        também não trabalhamos com o simplexo vazio.
        """
        freq = []
        if len(complexo) == 0:
            return False
        for s in complexo:
            if len(s) == 0 or all(isinstance(v, int) for v in s) is False:
                return False
            if all(s[i] < s[i+1] for i in range(len(s) - 1)) is False:
                raise ValueError(f"O simplexo {s} não está ordenado.")
            faces = sublistas(s)
            faces.pop() # elimina o conjunto vazio, que tá no final.
            for face in faces:
                if face not in complexo:
                    return False
            if s in freq:
                raise Warning(f"Simplexo {s} repetido, dará erro nas contas.")
            freq.append(s)
        return True

    def _n_simplexos(self, n):
        """Retorna uma lista com os n-simplexos do complexo simplicial."""
        nsimps = []
        for simplexo in self.complexo:
            if len(simplexo) == n+1:
                nsimps.append(simplexo)
        return nsimps

    def caracteristica_de_euler(self):
        """Retorna a Característica de Euler do complexo simplicial.

        Lembrando: a Característica de Euler é a soma alternada
        k_0 - k_1 + k_2 - k_3 + ...,
        sendo k_n a quantidade de n-simplexos no complexo. Tal fórmula
        generaliza V - A + F = 2.
        """
        chi = 0
        for i in range(self.dimensao + 1):
            chi += ((-1) ** i) * len(self._n_simplexos(i))
        return chi

    def _d_matriz(self, n):
        """Retorna a representação matricial do n-ésimo operador bordo.

        Lembrando: o operador bordo d_n:C_n(X) -> C_{n-1}(X) sai do espaço
        das n-cadeias (ie, combinações lineares formais dos n-simplexos)
        e chega no espaço das n-cadeias. Um exemplo de como é tal operador:

        d_n([0,1,2]) := [1,2] - [0,2] + [0,1]
        """
        C_n = self._n_simplexos(n)
        C_n_menos_1 = self._n_simplexos(n-1)
        d = [[0.0 for _ in range(len(C_n))] for _ in range(len(C_n_menos_1))]
        for dom in C_n:
            for k in range(len(dom)):
                aux = dom[:k] + dom[k+1:]
                if aux in C_n_menos_1:
                    i = C_n_menos_1.index(aux)
                    j = C_n.index(dom)
                    d[i][j] = (-1) ** k
        return d

    def _betti(self, n):
        """Retorna o n-ésimo número de Betti do complexo simplicial.

        Lembrando: o n-ésimo número de Betti é a dimensão do n-ésimo grupo de
        homologia e o n-ésimo grupo de homologia é definido como sendo o
        quociente

        H_n := Z_n / B_n = ker d_n / im d_{n+1}.

        Como queremos calcular dim ker d_n e dim im d_{n+1}, escalonamos as
        matrizes e contamos o número de pivôs. Lembrando que, pelo
        Teorema do Núcleo-Imagem, dim ker d_n = dim C_n - dim im d_n, e
        também sabemos que dim V/W = dimV - dimW, o que dá o resultado final
        ao fazermos V = Z_n e W = B_n.
        """
        d_n = self._d_matriz(n)
        d_n_mais_1 = self._d_matriz(n+1)

        algelinpy.escalona(d_n)
        algelinpy.escalona(d_n_mais_1)

        dim_dom = len(d_n_mais_1)
        dim_ciclos = dim_dom - algelinpy.numero_pivos(d_n)
        dim_bordos = algelinpy.numero_pivos(d_n_mais_1)

        return dim_ciclos - dim_bordos

    def homologia(self):
        """Retorna uma lista com todos os números de Betti do complexo."""
        bettis = []
        for n in range(self.dimensao + 1):
            bettis.append(self._betti(n))
        return bettis


ponto = [[0]]
ponto = ComplexoSimplicial("Ponto", ponto)
print(ponto)


dois_pontos = [[0], [1]]
dois_pontos = ComplexoSimplicial("Dois pontos", dois_pontos)
print(dois_pontos)


seg = [[0,1], [0], [1]]
seg = ComplexoSimplicial("Segmento de reta", seg)
print(seg)


circulo = [[0,1], [0,2], [1,2], [0], [1], [2]]
circulo = ComplexoSimplicial("Círculo", circulo)
print(circulo)


circulo_seg = [[0,1], [0,2], [1,2], [0], [1], [2], [3], [4], [3,4]]
circulo_seg = ComplexoSimplicial("Círculo + segmento", circulo_seg)
print(circulo_seg)


disco_fechado = [[0,1,2], [0,1], [0,2], [1,2], [0], [1], [2]]
disco_fechado = ComplexoSimplicial("Disco fechado", disco_fechado)
print(disco_fechado)


tetraedro_com_alca = [[0], [1], [2], [3], [4], [0,1], [0,3], [0,2], [0,4],
                      [1,2], [1,3], [2,3], [2,4], [0,1,2], [0,1,3], [0,2,3],
                      [1,2,3]]
tetraedro_com_alca = ComplexoSimplicial("Tetraedro com alça",
                                        tetraedro_com_alca)
print(tetraedro_com_alca)


tetraedro = [[0,1,2], [0,1,3], [0,2,3], [1,2,3], [0,1], [0,2],
             [0,3], [1,2], [1,3], [2,3], [0], [1], [2], [3]]
tetraedro = ComplexoSimplicial("Tetraedro", tetraedro)
print(tetraedro)


octaedro = [[0,1,2], [0,1,4], [0,2,3], [0,3,4], [1,2,5], [1,4,5],
            [2,3,5], [3,4,5], [0,1], [0,2], [0,3], [0,4], [1,2],
            [1,4], [1,5], [2,3], [2,5], [3,4], [3,5], [4,5], [0], [1],
            [2], [3], [4], [5]]
octaedro = ComplexoSimplicial("Octaedro", octaedro)
print(octaedro)


toro = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [0,1], [1,2], [0,2],
        [4,8], [7,8], [4,7], [3,5], [5,6], [3,6], [0,4], [3,4],
        [0,3], [1,8], [5,8], [1,5], [2,7], [6,7], [2,6], [0,8],
        [2,8], [0,7], [3,8], [5,7], [4,6], [0,5], [1,6], [0,6],
        [0,4,8], [0,1,8], [1,2,8], [2,7,8], [0,2,7], [0,4,7],
        [3,4,8], [3,5,8], [5,7,8], [5,6,7], [4,6,7], [3,4,6],
        [0,3,5], [0,1,5], [1,5,6], [1,2,6], [0,2,6], [0,3,6]]
toro = ComplexoSimplicial("Toro", toro)
print(toro)


projetivo = [[0], [1], [2], [3], [4], [5], [0,1], [0,2], [0,3], [0,4],
             [0,5], [1,2], [1,3], [1,4], [1,5], [2,3], [2,4], [2,5],
             [3,4], [3,5], [4,5], [0,2,3], [0,3,4], [0,1,4], [0,1,5],
             [0,2,5], [1,2,3], [1,3,5], [3,4,5], [2,4,5], [1,2,4]]
projetivo = ComplexoSimplicial("Plano projetivo", projetivo)
print(projetivo)


mobius = [[0], [1], [2], [3], [4], [0,1], [0,2], [0,3], [0,4], [1,2], [1,3],
          [2,3], [2,4], [3,4], [0,1,3], [1,2,3], [2,3,4], [0,2,4]]
mobius = ComplexoSimplicial("Faixa de Möbius", mobius)
print(mobius)


klein = [[0], [1], [2], [3], [4], [5], [6], [7], [8],
         [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [0,7], [0,8],
         [1,2], [1,5], [1,6], [1,7], [1,8], [2,6], [2,8],
         [3,4], [3,5], [3,6], [3,8], [4,6], [4,7], [4,8],
         [5,6], [5,7], [5,8], [6,7], [7,8], [0,1,5], [0,3,5],
         [1,2,6], [1,5,6], [0,2,6], [0,3,6], [3,5,8], [3,4,8],
         [5,6,7], [5,7,8], [4,6,7], [3,4,6], [0,4,8], [0,2,8],
         [1,7,8], [1,2,8], [0,1,7], [0,4,7]]
klein = ComplexoSimplicial("Garrafa de Klein", klein)
print(klein)


cilindro = [[0], [1], [2], [3], [4], [5], [0,1], [0,2], [0,3], [0,4], [0,5],
            [1,2], [1,4], [1,5], [2,5], [3,4], [3,5], [4,5], [0,3,4], [0,3,5],
            [0,1,4], [0,2,5], [1,2,5], [1,4,5]]
cilindro = ComplexoSimplicial("Cilindro", cilindro)
print(cilindro)
