import heapq

def heuristica(a, b):
    """
    Distância de Manhattan.
    Ideal para movimentação em grid (cima, baixo, esquerda, direita).
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def obter_vizinhos(no, grid):
    """
    Retorna os vizinhos válidos.
    """
    direcoes = [(0,1), (1,0), (0,-1), (-1,0)]
    vizinhos = []

    linhas = len(grid)
    colunas = len(grid[0])

    for dx, dy in direcoes:
        x, y = no[0] + dx, no[1] + dy

        if 0 <= x < linhas and 0 <= y < colunas:
            if grid[x][y] == 0:
                vizinhos.append((x,y))

    return vizinhos

def reconstruir_caminho(veio_de, atual):
    """
    Reconstrói o caminho do objetivo até o início.
    """
    caminho = [atual]

    while atual in veio_de:
        atual = veio_de[atual]
        caminho.append(atual)

    caminho.reverse()
    return caminho

def astar_animado(grid, inicio, objetivo):
    """
    Implementação do algoritmo A*.
    :param grid: matriz 2D (0 = livre, 1 = obstáculo)
    :param inicio: tupla (x, y)
    :param objetivo: tupla (x, y)
    :return: lista com o caminho ou Nome
    """
    lista_aberta = []
    heapq.heappush(lista_aberta, (0, inicio))

    veio_de = {}

    custo_g = {inicio: 0}
    custo_f = {inicio:heuristica(inicio, objetivo)}

    conjunto_fechado = set()

    while lista_aberta:
        atual = heapq.heappop(lista_aberta)[1]

        if atual == objetivo:
            caminho =  reconstruir_caminho(veio_de, atual)
            yield {
                "caminho": caminho,
                "abertos": lista_aberta,
                "fechados": conjunto_fechado
            }
            return
        
        conjunto_fechado.add(atual)

        for vizinho in obter_vizinhos(atual, grid):
            if vizinho in conjunto_fechado:
                continue

            custo_temporario = custo_g[atual] + 1

            if vizinho not in custo_g or custo_temporario < custo_g[vizinho]:
                veio_de[vizinho] = atual
                custo_g[vizinho] = custo_temporario
                custo_f[vizinho] = custo_temporario + heuristica(vizinho, objetivo)

                heapq.heappush(lista_aberta, (custo_f[vizinho], vizinho))

        yield {
            "atual": atual,
            "abertos": [n[1] for n in lista_aberta],
            "caminho": None
        }

