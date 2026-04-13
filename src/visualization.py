import pygame
import sys
from src.astar import astar

TAMANHO_CELULA = 60
LINHAS = 5
COLUNAS = 5

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
CINZA = (200, 200, 200)

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
            
def executar_visualizacao():
    pygame.init()

    largura = COLUNAS * TAMANHO_CELULA
    altura = LINHAS * TAMANHO_CELULA

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("A* Pathfinding")

    grid = [
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    inicio = (0,0)
    objetivo = (4,4)

    caminho = astar(grid, inicio, objetivo)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill(BRANCO)
        desenhar_grid(tela, grid, caminho, inicio, objetivo)
        pygame.display.flip()