import customtkinter as ctk
from PIL import Image, ImageTk
import time
from ambiente import Ambiente
from busquedas import beam_search, dynamic_weighted_a_star

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

CELDA = 40

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Buscando el hongo mágico - Proyecto IA")
        self.geometry("650x740")
        self.resizable(False, False)

        # --- Fondo ---
        fondo_img = Image.open("imagenes/Frame1.png")
        fondo_img = fondo_img.resize((650, 740))
        self.fondo = ImageTk.PhotoImage(fondo_img)

        self.canvas_fondo = ctk.CTkCanvas(self, width=650, height=740, highlightthickness=0)
        self.canvas_fondo.pack(fill="both", expand=True)
        self.canvas_fondo.create_image(0, 0, image=self.fondo, anchor="nw")

        # --- Parámetros iniciales ---
        self.filas = 9
        self.columnas = 15
        self.num_venenos = 25
        self.ambiente = Ambiente(self.filas, self.columnas, self.num_venenos)

        # --- Campo de dibujo (cuadro blanco) ---
        self.canvas_matriz = ctk.CTkCanvas(
            self,
            width=600,
            height=365,
            bg="white",
            highlightthickness=1,
            highlightbackground="green"
        )
        self.canvas_matriz.place(x=25, y=365)

        # --- Cargar imágenes para los elementos ---
        self.img_hormiga = ImageTk.PhotoImage(Image.open("imagenes/Hormiga.jpg").resize((CELDA, CELDA)))
        self.img_hongo = ImageTk.PhotoImage(Image.open("imagenes/Hongo.jpeg").resize((CELDA, CELDA)))
        self.img_veneno = ImageTk.PhotoImage(Image.open("imagenes/cesped.jpeg").resize((CELDA, CELDA)))

        # --- Entradas ---
        self.entry_filas = ctk.CTkEntry(self, width=55, height=20)
        self.entry_filas.insert(0, str(self.filas))
        self.entry_filas.place(x=205, y=221)

        self.entry_columnas = ctk.CTkEntry(self, width=55, height=20)
        self.entry_columnas.insert(0, str(self.columnas))
        self.entry_columnas.place(x=205, y=251)

        self.entry_venenos = ctk.CTkEntry(self, width=55, height=20)
        self.entry_venenos.insert(0, str(self.num_venenos))
        self.entry_venenos.place(x=205, y=283)

        # --- Botones ---
        self.btn_nuevo = ctk.CTkButton(self, text="Nuevo Tablero", width=120, height=30, command=self.nuevo_tablero)
        self.btn_nuevo.place(x=140, y=318)

        self.btn_beam = ctk.CTkButton(self, text="Beam Search", width=120, height=30, command=self.ejecutar_beam)
        self.btn_beam.place(x=289, y=318)

        self.btn_dwastar = ctk.CTkButton(self, text="Dynamic Weighted A*", width=150, height=30, command=self.ejecutar_dwastar)
        self.btn_dwastar.place(x=429, y=318)

        # --- Dibuja tablero inicial ---
        self.dibujar_tablero()

    def dibujar_tablero(self):
        self.canvas_matriz.delete("all")
        for i in range(self.filas):
            for j in range(self.columnas):
                valor = self.ambiente.matriz[i][j]
                x, y = j * CELDA, i * CELDA
                self.canvas_matriz.create_rectangle(x, y, x + CELDA, y + CELDA, outline="#ccc", fill="#fff")
                if valor == "A":
                    self.canvas_matriz.create_image(x, y, image=self.img_hormiga, anchor="nw")
                elif valor == "H":
                    self.canvas_matriz.create_image(x, y, image=self.img_hongo, anchor="nw")
                elif valor == "V":
                    self.canvas_matriz.create_image(x, y, image=self.img_veneno, anchor="nw")

    def animar_camino(self, camino):
        for fila, col in camino:
            self.dibujar_tablero()
            self.canvas_matriz.create_image(col * CELDA, fila * CELDA, image=self.img_hormiga, anchor="nw")
            self.update()
            time.sleep(0.2)

    def nuevo_tablero(self):
        try:
            filas = int(self.entry_filas.get())
            columnas = int(self.entry_columnas.get())
            venenos = int(self.entry_venenos.get())
            self.filas = filas
            self.columnas = columnas
            self.num_venenos = min(venenos, filas * columnas - 2)
            self.ambiente = Ambiente(self.filas, self.columnas, self.num_venenos)
            self.dibujar_tablero()
        except ValueError:
            self.mostrar_mensaje("⚠️ Tamaño o cantidad inválida.")

    def ejecutar_beam(self):
        camino = beam_search(self.ambiente.matriz, self.ambiente.pos_hormiga, self.ambiente.pos_hongo, beta=4)
        if camino:
            self.animar_camino(camino)
        else:
            self.mostrar_mensaje("❌ No se encontró camino con Beam Search.")

    def ejecutar_dwastar(self):
        camino = dynamic_weighted_a_star(self.ambiente.matriz, self.ambiente.pos_hormiga, self.ambiente.pos_hongo, epsilon=2.0)
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


def iniciar_interfaz():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    iniciar_interfaz()
