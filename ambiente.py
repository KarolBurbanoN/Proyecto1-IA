import random

class Ambiente:
    def __init__(self, filas=10, columnas=10, num_venenos=10):
        self.filas = filas
        self.columnas = columnas
        self.num_venenos = num_venenos
        self.matriz = []
        self.pos_hormiga = None
        self.pos_hongo = None
        self.venenos = []
        self.generar_matriz()

    def generar_matriz(self):
        """
        Genera una matriz vacía y coloca los elementos:
        - Hormiga (A)
        - Hongo (H)
        - Venenos (V)
        """
        # Inicializar matriz vacía
        self.matriz = [["." for _ in range(self.columnas)] for _ in range(self.filas)]

        # Posición aleatoria de la hormiga
        self.pos_hormiga = (random.randint(0, self.filas - 1), random.randint(0, self.columnas - 1))
        self.matriz[self.pos_hormiga[0]][self.pos_hormiga[1]] = "A"

        # Posición aleatoria del hongo, distinta a la hormiga
        while True:
            pos_hongo = (random.randint(0, self.filas - 1), random.randint(0, self.columnas - 1))
            if pos_hongo != self.pos_hormiga:
                self.pos_hongo = pos_hongo
                self.matriz[pos_hongo[0]][pos_hongo[1]] = "H"
                break

        # Posiciones aleatorias de los venenos
        self.venenos = []
        for _ in range(self.num_venenos):
            while True:
                pos_veneno = (random.randint(0, self.filas - 1), random.randint(0, self.columnas - 1))
                if pos_veneno not in [self.pos_hormiga, self.pos_hongo] and pos_veneno not in self.venenos:
                    self.venenos.append(pos_veneno)
                    self.matriz[pos_veneno[0]][pos_veneno[1]] = "V"
                    break

    def mostrar(self):
        """Imprime la matriz (solo para pruebas, la interfaz la mostrará gráficamente)."""
        for fila in self.matriz:
            print(" ".join(fila))
        print("\nHormiga:", self.pos_hormiga, "Hongo:", self.pos_hongo, "Venenos:", len(self.venenos))


if __name__ == "__main__":
    # Prueba básica
    ambiente = Ambiente(filas=8, columnas=8, num_venenos=12)
    ambiente.mostrar()
