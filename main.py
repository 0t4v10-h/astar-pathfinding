from src.astar import astar

def imprimir_grid(grid, caminho=None, inicio=None, objetivo=None):
    """
    Mostra o grid no terminal com o caminho encontrado.
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            posicao = (i,j)

            if posicao == inicio:
                print("S", end=" ")
            elif posicao == objetivo:
                print("G", end=" ")
            elif caminho and posicao in caminho:
                print("*", end=" ")
            elif grid[i][j] == 1:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()

def main():
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

    if caminho:
        print("Caminho encontrado:\n")
        imprimir_grid(grid, caminho, inicio, objetivo)
    else:
        print("Nenhum caminho encontrado!")

if __name__ == "__main__":
    main()