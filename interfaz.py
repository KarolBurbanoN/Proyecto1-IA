import customtkinter as ctk
from PIL import Image, ImageTk
import time
from ambiente import Ambiente
from busquedas import beam_search, dynamic_weighted_a_star

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

CELDA = 40
COLOR_BOTON = "#D7AA89"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Buscando el hongo mágico - Proyecto IA")
        self.geometry("1180x730")
        self.resizable(False, False)

        # --- Fondo ---
        fondo_img = Image.open("imagenes/Frame1.png")
        fondo_img = fondo_img.resize((1180, 730))
        self.fondo = ImageTk.PhotoImage(fondo_img)

        self.canvas_fondo = ctk.CTkCanvas(self, width=1180, height=730, highlightthickness=0)
        self.canvas_fondo.pack(fill="both", expand=True)
        self.canvas_fondo.create_image(0, 0, image=self.fondo, anchor="nw")

        # --- Parámetros iniciales ---
        self.filas = 10
        self.columnas = 16
        self.num_venenos = 25
        self.ambiente = Ambiente(self.filas, self.columnas, self.num_venenos)

        # --- Campo de dibujo (cuadro blanco) ---
        self.canvas_matriz = ctk.CTkCanvas(
            self,
            width=640,
            height=670,
            bg="white",
            highlightthickness=1,
            highlightbackground="green"
        )
        self.canvas_matriz.place(x=511, y=30)

        # --- Sprites de la hormiga ---
        self.hormiga_sprites = [
            ImageTk.PhotoImage(Image.open("imagenes/3.png").resize((CELDA, CELDA))),   # Estática
            ImageTk.PhotoImage(Image.open("imagenes/4.png").resize((CELDA, CELDA))),   # Mov1
            ImageTk.PhotoImage(Image.open("imagenes/6.png").resize((CELDA, CELDA))),   # Mov1 parpadeo
            ImageTk.PhotoImage(Image.open("imagenes/5.png").resize((CELDA, CELDA))),   # Mov2
            ImageTk.PhotoImage(Image.open("imagenes/7.png").resize((CELDA, CELDA))),   # Mov2 parpadeo
            ImageTk.PhotoImage(Image.open("imagenes/HongoHormiga.png").resize((CELDA, CELDA)))  # Final con hongo
        ]

        # --- Otras imágenes ---
        self.img_hongo = ImageTk.PhotoImage(Image.open("imagenes/Hongo2.png").resize((CELDA, CELDA)))
        self.img_veneno = ImageTk.PhotoImage(Image.open("imagenes/cesped.jpeg").resize((CELDA, CELDA)))
        self.img_camino = ImageTk.PhotoImage(Image.open("imagenes/camino.png").resize((CELDA, CELDA)))

        # --- Entradas ---
        self.entry_filas = ctk.CTkEntry(self, width=55, height=20, border_color="green")
        self.entry_filas.insert(0, str(self.filas))
        self.entry_filas.place(x=263, y=213)

        self.entry_columnas = ctk.CTkEntry(self, width=55, height=20, border_color="green")
        self.entry_columnas.insert(0, str(self.columnas))
        self.entry_columnas.place(x=263, y=243)

        self.entry_venenos = ctk.CTkEntry(self, width=55, height=20, border_color="green")
        self.entry_venenos.insert(0, str(self.num_venenos))
        self.entry_venenos.place(x=263, y=273)
        
        # --- Campos de información ---
        self.label_inicio = ctk.CTkLabel(self, text="", text_color="black", bg_color="white")
        self.label_inicio.place(x=300, y=390)

        self.label_meta = ctk.CTkLabel(self, text="", text_color="black", bg_color="white")
        self.label_meta.place(x=250, y=410)

        self.label_tiempo = ctk.CTkLabel(self, text="", text_color="black", bg_color="white")
        self.label_tiempo.place(x=250, y=440)

        self.text_solucion = ctk.CTkTextbox(self, width=190, height=92, border_color="black", border_width=1)
        self.text_solucion.place(x=164, y=496)

        # --- Botones ---
        self.btn_nuevo = ctk.CTkButton(self, text="Nuevo Tablero", width=120, height=30, fg_color=COLOR_BOTON, text_color="black", hover_color="#A76D43",command=self.nuevo_tablero)
        self.btn_nuevo.place(x=198, y=310)

        self.btn_beam = ctk.CTkButton(self, text="Beam Search", width=120, height=30, fg_color=COLOR_BOTON, text_color="black", hover_color="#A76D43",command=self.ejecutar_beam)
        self.btn_beam.place(x=198, y=599)

        self.btn_dwastar = ctk.CTkButton(self, text="Dynamic Weighted A*", width=150, height=30, fg_color=COLOR_BOTON, text_color="black", hover_color="#A76D43", command=self.ejecutar_dwastar)
        self.btn_dwastar.place(x=184, y=646)

        # --- Dibuja tablero inicial ---
        self.dibujar_tablero()

    def dibujar_tablero(self):
        self.canvas_matriz.delete("all")

        for i in range(self.filas):
            for j in range(self.columnas):
                valor = self.ambiente.matriz[i][j]
                x, y = j * CELDA, i * CELDA

                # Dibuja fondo de césped (camino)
                self.canvas_matriz.create_image(x, y, image=self.img_camino, anchor="nw")

                # Luego dibuja encima el elemento correspondiente
                if valor == "A":
                    self.canvas_matriz.create_image(x, y, image=self.hormiga_sprites[0], anchor="nw")
                elif valor == "H":
                    self.canvas_matriz.create_image(x, y, image=self.img_hongo, anchor="nw")
                elif valor == "V":
                    self.canvas_matriz.create_image(x, y, image=self.img_veneno, anchor="nw")


    def animar_camino(self, camino):
            # Secuencia cíclica de movimiento: mov1 → mov1 parpadeo → mov2 → mov2 parpadeo
            secuencia = [1, 2, 3, 4]
            indice = 0

            for i, (fila, col) in enumerate(camino):
                self.dibujar_tablero()

                # Si es la última posición, muestra la hormiga con el hongo
                if i == len(camino) - 1:
                    sprite = self.hormiga_sprites[5]
                else:
                    sprite = self.hormiga_sprites[secuencia[indice]]
                    indice = (indice + 1) % len(secuencia)

                self.canvas_matriz.create_image(col * CELDA, fila * CELDA, image=sprite, anchor="nw")
                self.update()
                time.sleep(0.25)  # velocidad de la animación
                
    def actualizar_info(self, metodo, camino, tiempo):
        """Actualiza los campos de información (inicio, meta, tiempo, solución)."""
        inicio = self.ambiente.pos_hormiga
        meta = self.ambiente.pos_hongo

        self.label_inicio.configure(text=f"{inicio}")
        self.label_meta.configure(text=f"{meta}")
        self.label_tiempo.configure(text=f"{tiempo*1000:.3f} ms")

        self.text_solucion.configure(state="normal")
        self.text_solucion.delete("1.0", "end")
        if camino:
            self.text_solucion.insert("end", f"Algoritmo: {metodo}\nLongitud del camino: {len(camino)} pasos\n\nCamino:\n{camino}")
        else:
            self.text_solucion.insert("end", f"Algoritmo: {metodo}\n❌ No se encontró camino.")
        self.text_solucion.configure(state="disabled")

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
        import time
        inicio_t = time.perf_counter()  # más preciso para medir tiempos cortos
        camino = beam_search(self.ambiente.matriz, self.ambiente.pos_hormiga, self.ambiente.pos_hongo, beta=4)
        tiempo = time.perf_counter() - inicio_t  # calcula la diferencia exacta

        self.actualizar_info("Beam Search", camino, tiempo)

        if camino:
            self.animar_camino(camino)
        else:
            self.mostrar_mensaje("❌ No se encontró camino con Beam Search.")
            
    def ejecutar_dwastar(self):
        import time
        inicio_t = time.perf_counter()
        camino = dynamic_weighted_a_star(self.ambiente.matriz, self.ambiente.pos_hormiga, self.ambiente.pos_hongo, epsilon=2.0)
        tiempo = time.perf_counter() - inicio_t

        self.actualizar_info("Dynamic Weighted A*", camino, tiempo)

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
