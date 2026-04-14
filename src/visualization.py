import pygame
import sys
from src.astar import astar_animado

TAMANHO_CELULA = 60
LINHAS = 10
COLUNAS = 10

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
CINZA = (200, 200, 200)
CINZA_CLARO = (180, 180, 180)
VERDE = (0, 255, 0)
ROXO = (160, 32, 240)

def criar_grid():
    return [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]

def desenhar_grid(tela, grid, caminho, inicio, objetivo, abertos, fechados, atual):
    for i in range(LINHAS):
        for j in range(COLUNAS):
            pos = (i,j)
            cor = BRANCO

            if grid[i][j] == 1:
                cor = PRETO

            elif pos == inicio:
                cor = AZUL

            elif pos == objetivo:
                cor = VERMELHO

            elif pos == atual:
                cor = ROXO

            elif caminho and pos in caminho:
                cor = AMARELO

            elif pos in fechados:
                cor = CINZA_CLARO

            elif pos in abertos:
                cor = VERDE


            pygame.draw.rect(
                tela,
                cor,
                (j * TAMANHO_CELULA, i * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA)
            )

            pygame.draw.rect(
                tela,
                CINZA,
                (j * TAMANHO_CELULA, i * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA),
                1
            )

def obter_posicao_mouse(pos):
    x, y = pos
    linha = y // TAMANHO_CELULA
    coluna = x // TAMANHO_CELULA
    return linha, coluna

def desenhar_painel_info(tela, caminho, fechados, velocidade):
    fonte = pygame.font.SysFont(None, 24)

    x_base = COLUNAS * TAMANHO_CELULA + 10
    y = 20

    textos = [
        "CONTROLES: ",
        "S + clique = Início",
        "G + clique = Objetivo",
        "Clique = Obstáculos",
        "R = Reset",
        "Espaço = Execução",
        "Setas (CIMA/BAIXO) = Velocidade",
        ""
    ]

    if caminho:
        textos += [
            f"Caminho: {len(caminho)}",
            f"Nós explorados: {len(fechados)}",
            f"Custo: {len(caminho) - 1}",
        ]

    else:
        textos += [
            "Aguardando execução..."
        ]

    textos.append(f"Velocidade: {velocidade} ms")

    for texto in textos:
        superficie = fonte.render(texto, True, (0, 0, 0))
        tela.blit(superficie, (x_base, y))
        y += 30
            
def executar_visualizacao():
    pygame.init()

    LARGURA_INFO = 300

    largura = COLUNAS * TAMANHO_CELULA + LARGURA_INFO
    altura = LINHAS * TAMANHO_CELULA

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("A* Pathfinding Interativo")

    gerador = None
    atual = None
    abertos = []
    fechados = []

    grid = criar_grid()
    inicio = None
    objetivo = None
    caminho = None

    modo = None

    velocidade = 100

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    modo = "inicio"

                elif evento.key == pygame.K_g:
                    modo = "objetivo"

                elif evento.key == pygame.K_SPACE:
                    if inicio and objetivo:
                        caminho = None
                        abertos = []
                        fechados = []
                        gerador = astar_animado(grid, inicio, objetivo)

                elif evento.key == pygame.K_r:
                    grid = criar_grid()
                    inicio = None
                    objetivo = None
                    caminho = None
                    gerador = None
                    atual = None
                    abertos = []
                    fechados = []

                elif evento.key == pygame.K_UP:
                    velocidade = max(10, velocidade - 10)

                elif evento.key == pygame.K_DOWN:
                    velocidade = min(1000, velocidade + 10)

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                linha, coluna = obter_posicao_mouse(pos)

                if 0 <= linha < LINHAS and 0 <= coluna < COLUNAS:
                    if modo == "inicio":
                        inicio = (linha, coluna)
                        modo = None
                    elif modo == "objetivo":
                        objetivo = (linha, coluna)
                        modo = None
                    else:
                        grid[linha][coluna] = 1 if grid[linha][coluna] == 0 else 0

        if gerador:
            try:
                estado = next(gerador)

                atual = estado.get("atual", None)
                abertos = estado.get("abertos", [])
                fechados = estado.get("fechados", [])

                if estado.get("caminho"):
                    caminho = estado["caminho"]
                    gerador = None

                    pygame.time.delay(velocidade)

            except StopIteration:
                gerador = None

        tela.fill(BRANCO)

        desenhar_grid(tela, grid, caminho, inicio, objetivo, abertos, fechados, atual)
        
        pygame.draw.rect(
            tela,
            (230, 230, 230),
            (COLUNAS * TAMANHO_CELULA, 0, LARGURA_INFO, altura)
        )

        desenhar_painel_info(tela, caminho, fechados, velocidade)

        pygame.display.flip()