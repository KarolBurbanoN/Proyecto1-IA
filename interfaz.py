import customtkinter as ctk
import time
from ambiente import Ambiente
from busquedas import beam_search, dynamic_weighted_a_star

# ---------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA INTERFAZ
# ---------------------------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

CELDA = 40  # tamaño de cada celda en píxeles
COLOR_CAMINO = "#444"
COLOR_HORMIGA = "#00ff7f"
COLOR_HONGO = "#ffcc00"
COLOR_VENENO = "#ff4444"
COLOR_VACIO = "#222"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🐜 Buscando el hongo mágico 🍄 - Proyecto IA")
        self.geometry("1000x750")

        # Parámetros iniciales
        self.filas = 10
        self.columnas = 10
        self.num_venenos = 12

        # Crear entorno inicial
        self.ambiente = Ambiente(self.filas, self.columnas, self.num_venenos)

        # ------------------- Layout principal -------------------
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Canvas donde se dibuja el tablero
        self.canvas = ctk.CTkCanvas(
            self.frame,
            width=self.columnas * CELDA,
            height=self.filas * CELDA,
            bg=COLOR_CAMINO,
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # ------------------- Controles -------------------
        ctk.CTkLabel(self.frame, text="Filas:").grid(row=1, column=0, sticky="e")
        self.entry_filas = ctk.CTkEntry(self.frame, width=60)
        self.entry_filas.insert(0, str(self.filas))
        self.entry_filas.grid(row=1, column=1, sticky="w", padx=5)

        ctk.CTkLabel(self.frame, text="Columnas:").grid(row=1, column=2, sticky="e")
        self.entry_columnas = ctk.CTkEntry(self.frame, width=60)
        self.entry_columnas.insert(0, str(self.columnas))
        self.entry_columnas.grid(row=1, column=3, sticky="w", padx=5)

        ctk.CTkLabel(self.frame, text="Venenos:").grid(row=2, column=0, sticky="e")
        self.entry_venenos = ctk.CTkEntry(self.frame, width=60)
        self.entry_venenos.insert(0, str(self.num_venenos))
        self.entry_venenos.grid(row=2, column=1, sticky="w", padx=5)

        # Botones
        self.btn_nuevo = ctk.CTkButton(self.frame, text="🔁 Nuevo tablero", command=self.nuevo_tablero)
        self.btn_nuevo.grid(row=3, column=0, pady=10, columnspan=1)

        self.btn_beam = ctk.CTkButton(self.frame, text="🌀 Beam Search", command=self.ejecutar_beam)
        self.btn_beam.grid(row=3, column=1, pady=10, columnspan=1)

        self.btn_dwastar = ctk.CTkButton(self.frame, text="⚡ Dynamic Weighted A*", command=self.ejecutar_dwastar)
        self.btn_dwastar.grid(row=3, column=2, pady=10, columnspan=1)

        self.btn_salir = ctk.CTkButton(self.frame, text="❌ Salir", fg_color="#cc3333", command=self.destroy)
        self.btn_salir.grid(row=3, column=3, pady=10, columnspan=1)

        # Dibuja el tablero inicial
        self.dibujar_tablero()

    # ---------------------------------------------------
    # Dibuja la matriz actual en el canvas
    # ---------------------------------------------------
    def dibujar_tablero(self):
        self.canvas.delete("all")

        # Ajustar tamaño del canvas dinámicamente
        ancho = self.columnas * CELDA
        alto = self.filas * CELDA
        self.canvas.config(width=ancho, height=alto)

        for i in range(self.filas):
            for j in range(self.columnas):
                valor = self.ambiente.matriz[i][j]
                color = COLOR_VACIO
                if valor == "A":
                    color = COLOR_HORMIGA
                elif valor == "H":
                    color = COLOR_HONGO
                elif valor == "V":
                    color = COLOR_VENENO
                self.canvas.create_rectangle(
                    j * CELDA, i * CELDA, (j + 1) * CELDA, (i + 1) * CELDA,
                    fill=color, outline="#111"
                )

    # ---------------------------------------------------
    # Animación del movimiento de la hormiga
    # ---------------------------------------------------
    def animar_camino(self, camino):
        for pos in camino:
            fila, col = pos
            self.dibujar_tablero()
            self.canvas.create_rectangle(
                col * CELDA, fila * CELDA,
                (col + 1) * CELDA, (fila + 1) * CELDA,
                fill=COLOR_HORMIGA, outline="#111"
            )
            self.update()
            time.sleep(0.2)

    # ---------------------------------------------------
    # Funciones de botones
    # ---------------------------------------------------
    def nuevo_tablero(self):
        try:
            filas = int(self.entry_filas.get())
            columnas = int(self.entry_columnas.get())
            venenos = int(self.entry_venenos.get())

            if filas <= 1 or columnas <= 1:
                raise ValueError

            self.filas = filas
            self.columnas = columnas
            self.num_venenos = min(venenos, filas * columnas - 2)

            self.ambiente = Ambiente(self.filas, self.columnas, self.num_venenos)
            self.dibujar_tablero()

        except ValueError:
            self.mostrar_mensaje("⚠️ Tamaño o cantidad de venenos inválido.")

    def ejecutar_beam(self):
        camino = beam_search(
            self.ambiente.matriz,
            self.ambiente.pos_hormiga,
            self.ambiente.pos_hongo,
            beta=4
        )
        if camino:
            self.animar_camino(camino)
        else:
            self.mostrar_mensaje("❌ No se encontró camino con Beam Search.")

    def ejecutar_dwastar(self):
        camino = dynamic_weighted_a_star(
            self.ambiente.matriz,
            self.ambiente.pos_hormiga,
            self.ambiente.pos_hongo,
            epsilon=2.0
        )
        if camino:
            self.animar_camino(camino)
        else:
            self.mostrar_mensaje("❌ No se encontró camino con Dynamic Weighted A*.")

    def mostrar_mensaje(self, texto):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Mensaje")
        ventana.geometry("320x120")
        label = ctk.CTkLabel(ventana, text=texto, wraplength=280)
        label.pack(pady=20)

# ---------------------------------------------------
# EJECUCIÓN PRINCIPAL
# ---------------------------------------------------
def iniciar_interfaz():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
