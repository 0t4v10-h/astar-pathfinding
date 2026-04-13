import pygame
import sys
from src.astar import astar

TAMANHO_CELULA = 60
LINHAS = 10
COLUNAS = 10

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
CINZA = (200, 200, 200)

def criar_grid():
    return [[0 for _ in range(COLUNAS)] for _ in range(LINHAS)]

def desenhar_grid(tela, grid, caminho, inicio, objetivo):
    for i in range(LINHAS):
        for j in range(COLUNAS):
            cor = BRANCO

            if grid[i][j] == 1:
                cor = PRETO
            elif (i,j) == inicio:
                cor = AZUL
            elif (i,j) == objetivo:
                cor = VERMELHO
            elif caminho and (i,j) in caminho:
                cor = AMARELO

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
            
def executar_visualizacao():
    pygame.init()

    largura = COLUNAS * TAMANHO_CELULA
    altura = LINHAS * TAMANHO_CELULA

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("A* Pathfinding Interativo")

    grid = criar_grid()
    inicio = None
    objetivo = None
    caminho = None

    modo = None

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
                        caminho = astar(grid, inicio, objetivo)
                elif evento.key == pygame.K_r:
                    grid = criar_grid()
                    inicio = None
                    objetivo = None
                    caminho = None

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
                        if grid[linha][coluna] == 0:
                            grid[linha][coluna] = 1
                        else:
                            grid[linha][coluna] = 0

        tela.fill(BRANCO)
        desenhar_grid(tela, grid, caminho, inicio, objetivo)
        pygame.display.flip()