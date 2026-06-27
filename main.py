import tkinter as tk
import random


# Configuración general del juego
ANCHO_VENTANA = 700
ALTO_VENTANA = 500

ANCHO_JUEGO = 600
ALTO_JUEGO = 380

TAMANO_JUGADOR = 40
TAMANO_ESTRELLA = 30
VELOCIDAD = 20
TIEMPO_INICIAL = 30


class JuegoAtrapaEstrella:
    def __init__(self, root):
        self.root = root
        self.root.title("Atrapa la Estrella")
        self.root.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
        self.root.resizable(False, False)

        self.puntaje = 0
        self.tiempo_restante = TIEMPO_INICIAL
        self.juego_activo = True

        self.jugador_x = 30
        self.jugador_y = 30

        self.crear_interfaz()
        self.crear_elementos_juego()
        self.mover_estrella()
        self.actualizar_temporizador()

        self.root.bind("<KeyPress>", self.mover_jugador)

    def crear_interfaz(self):
        self.titulo = tk.Label(
            self.root,
            text="Atrapa la Estrella",
            font=("Arial", 22, "bold"),
            fg="#1f3c88"
        )
        self.titulo.pack(pady=10)

        self.panel = tk.Frame(self.root)
        self.panel.pack()

        self.label_puntaje = tk.Label(
            self.panel,
            text=f"Puntaje: {self.puntaje}",
            font=("Arial", 14, "bold")
        )
        self.label_puntaje.grid(row=0, column=0, padx=25)

        self.label_tiempo = tk.Label(
            self.panel,
            text=f"Tiempo: {self.tiempo_restante}s",
            font=("Arial", 14, "bold")
        )
        self.label_tiempo.grid(row=0, column=1, padx=25)

        self.canvas = tk.Canvas(
            self.root,
            width=ANCHO_JUEGO,
            height=ALTO_JUEGO,
            bg="white",
            highlightthickness=3,
            highlightbackground="#1f3c88"
        )
        self.canvas.pack(pady=15)

        self.boton_reiniciar = tk.Button(
            self.root,
            text="Reiniciar juego",
            font=("Arial", 12),
            bg="#1f3c88",
            fg="white",
            command=self.reiniciar_juego
        )
        self.boton_reiniciar.pack(pady=5)

        self.instrucciones = tk.Label(
            self.root,
            text="Usa las flechas del teclado para mover el jugador y atrapar la estrella.",
            font=("Arial", 10),
            fg="#333333"
        )
        self.instrucciones.pack(pady=5)

    def crear_elementos_juego(self):
        self.jugador = self.canvas.create_rectangle(
            self.jugador_x,
            self.jugador_y,
            self.jugador_x + TAMANO_JUGADOR,
            self.jugador_y + TAMANO_JUGADOR,
            fill="#0078d4",
            outline=""
        )

        self.estrella = self.canvas.create_text(
            200,
            200,
            text="★",
            font=("Arial", 28, "bold"),
            fill="gold"
        )

    def mover_jugador(self, evento):
        if not self.juego_activo:
            return

        if evento.keysym == "Up" and self.jugador_y > 0:
            self.jugador_y -= VELOCIDAD

        elif evento.keysym == "Down" and self.jugador_y < ALTO_JUEGO - TAMANO_JUGADOR:
            self.jugador_y += VELOCIDAD

        elif evento.keysym == "Left" and self.jugador_x > 0:
            self.jugador_x -= VELOCIDAD

        elif evento.keysym == "Right" and self.jugador_x < ANCHO_JUEGO - TAMANO_JUGADOR:
            self.jugador_x += VELOCIDAD

        self.canvas.coords(
            self.jugador,
            self.jugador_x,
            self.jugador_y,
            self.jugador_x + TAMANO_JUGADOR,
            self.jugador_y + TAMANO_JUGADOR
        )

        self.verificar_colision()

    def mover_estrella(self):
        self.estrella_x = random.randint(TAMANO_ESTRELLA, ANCHO_JUEGO - TAMANO_ESTRELLA)
        self.estrella_y = random.randint(TAMANO_ESTRELLA, ALTO_JUEGO - TAMANO_ESTRELLA)

        self.canvas.coords(self.estrella, self.estrella_x, self.estrella_y)

    def verificar_colision(self):
        jugador_coords = self.canvas.coords(self.jugador)
        estrella_coords = self.canvas.coords(self.estrella)

        jugador_izquierda = jugador_coords[0]
        jugador_arriba = jugador_coords[1]
        jugador_derecha = jugador_coords[2]
        jugador_abajo = jugador_coords[3]

        estrella_x = estrella_coords[0]
        estrella_y = estrella_coords[1]

        if (
            jugador_izquierda <= estrella_x <= jugador_derecha
            and jugador_arriba <= estrella_y <= jugador_abajo
        ):
            self.puntaje += 1
            self.label_puntaje.config(text=f"Puntaje: {self.puntaje}")
            self.mover_estrella()

    def actualizar_temporizador(self):
        if self.juego_activo:
            if self.tiempo_restante > 0:
                self.label_tiempo.config(text=f"Tiempo: {self.tiempo_restante}s")
                self.tiempo_restante -= 1
                self.root.after(1000, self.actualizar_temporizador)
            else:
                self.juego_activo = False
                self.label_tiempo.config(text="Tiempo: 0s")
                self.mostrar_fin_juego()

    def mostrar_fin_juego(self):
        self.canvas.create_text(
            ANCHO_JUEGO / 2,
            ALTO_JUEGO / 2,
            text=f"Juego terminado\nPuntaje final: {self.puntaje}",
            font=("Arial", 22, "bold"),
            fill="red",
            justify="center"
        )

    def reiniciar_juego(self):
        self.puntaje = 0
        self.tiempo_restante = TIEMPO_INICIAL
        self.juego_activo = True

        self.jugador_x = 30
        self.jugador_y = 30

        self.label_puntaje.config(text=f"Puntaje: {self.puntaje}")
        self.label_tiempo.config(text=f"Tiempo: {self.tiempo_restante}s")

        self.canvas.delete("all")
        self.crear_elementos_juego()
        self.mover_estrella()
        self.actualizar_temporizador()


if __name__ == "__main__":
    ventana = tk.Tk()
    juego = JuegoAtrapaEstrella(ventana)
    ventana.mainloop()