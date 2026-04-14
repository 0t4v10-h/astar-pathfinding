class Grid:
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        self.matriz = [[0 for _ in range(colunas)] for _ in range(linhas)]

    def alternar_obstaculo(self, linha, coluna):
        if self.matriz[linha][coluna] == 0:
            self.matriz[linha][coluna] = 1
        else:
            self.matriz[linha][coluna] = 0

    def resetar(self):
        self.matriz = [[0 for _ in range(self.colunas)] for _ in range(self.linhas)]

    def eh_obstaculo(self, linha, coluna):
        return self.matriz[linha][coluna] == 1
    
    def get_matriz(self):
        return self.matriz