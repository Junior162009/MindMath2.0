import tkinter as tk
from PIL import Image, ImageTk
import random
import os
import math

# ======= CONFIGURACIÓN GENERAL ======= #
ANCHO, ALTO = 500, 600
FONDO_IMAGEN = "fondo_matematico.png"
LOGO_IMAGEN = "logo.png"

# ======= VARIABLE GLOBAL DE ACCESIBILIDAD ======= #
modo_discapacidad = False

def crear_boton(master, texto, comando, color="#4CAF50"):
    return tk.Button(
        master, text=texto, command=comando,
        font=("Arial Rounded MT Bold", 18 if modo_discapacidad else 16),
        bg=color if not modo_discapacidad else "#222222",
        fg="white" if not modo_discapacidad else "yellow",
        activebackground=color, relief="flat", bd=0, padx=25, pady=12, cursor="hand2"
    )

# ======= CLASE BASE ======= #
class BaseVentana:
    def __init__(self, master):
        self.master = master
        self.master.geometry(f"{ANCHO}x{ALTO}")
        self.master.resizable(False, False)
        self.aplicar_fondo()

    def aplicar_fondo(self):
        if modo_discapacidad:
            self.master.configure(bg="black")
            return
        if os.path.exists(FONDO_IMAGEN):
            imagen = Image.open(FONDO_IMAGEN).resize((ANCHO, ALTO))
            self.fondo_tk = ImageTk.PhotoImage(imagen)
            fondo_label = tk.Label(self.master, image=self.fondo_tk)
            fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
            fondo_label.lower()
        else:
            self.master.configure(bg="#1e3c72")

    def limpiar(self):
        for w in self.master.winfo_children():
            w.destroy()

# ======= PANTALLA DE INICIO ======= #
class PantallaInicio(BaseVentana):
    def __init__(self, master):
        super().__init__(master)
        self.crear_interfaz()

    def crear_interfaz(self):
        try:
            logo = Image.open(LOGO_IMAGEN).resize((250, 250))
            self.logo_tk = ImageTk.PhotoImage(logo)
            tk.Label(self.master, image=self.logo_tk, bg="#000000").pack(pady=60)
        except:
            tk.Label(self.master, text="🎮 MindMath",
                     font=("Arial Rounded MT Bold", 42 if modo_discapacidad else 36),
                     fg="yellow" if modo_discapacidad else "white",
                     bg="black" if modo_discapacidad else "#1e3c72").pack(pady=100)

        crear_boton(self.master, "🚀 Iniciar", self.mostrar_niveles, "#4CAF50").pack(pady=30)
        crear_boton(self.master, "♿ Modo Discapacidad", self.activar_modo, "#9C27B0").pack(pady=10)
        tk.Label(self.master, text="Versión educativa 2025",
                 fg="yellow" if modo_discapacidad else "white",
                 bg="black" if modo_discapacidad else "#1e3c72",
                 font=("Arial", 14 if modo_discapacidad else 10)).pack(side="bottom", pady=10)

    def activar_modo(self):
        global modo_discapacidad
        modo_discapacidad = not modo_discapacidad
        self.limpiar()
        PantallaInicio(self.master)

    def mostrar_niveles(self):
        self.limpiar()
        SeleccionNivel(self.master)

# ======= MENÚ DE NIVELES ======= #
class SeleccionNivel(BaseVentana):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self.master, text="🎚️ Selecciona Nivel",
                 font=("Arial Rounded MT Bold", 32 if modo_discapacidad else 26),
                 fg="yellow" if modo_discapacidad else "white",
                 bg="black" if modo_discapacidad else "#1e3c72").pack(pady=40)

        niveles = [
            ("🌱 Fácil (90s)", "facil", "#4CAF50"),
            ("🚀 Intermedio (70s)", "intermedio", "#2196F3"),
            ("🔥 Difícil (50s)", "dificil", "#FF9800"),
            ("💀 Extremo (30s)", "extremo", "#E91E63")
        ]
        for texto, nivel, color in niveles:
            crear_boton(self.master, texto, lambda n=nivel: self.iniciar(n), color).pack(pady=10, fill="x", padx=60)

        crear_boton(self.master, "🏠 Menú Principal", self.volver, "#9E9E9E").pack(pady=20)

    def iniciar(self, nivel):
        self.limpiar()
        JuegoPrincipal(self.master, nivel)

    def volver(self):
        self.limpiar()
        PantallaInicio(self.master)

# ======= JUEGO PRINCIPAL ======= #
class JuegoPrincipal(BaseVentana):
    def __init__(self, master, nivel):
        super().__init__(master)
        self.nivel = nivel
        self.puntos = 0
        self.vidas = self.obtener_vidas()
        self.tiempo = self.obtener_tiempo()
        self.crear_interfaz()
        self.generar_pregunta()
        self.contar_tiempo()

    def obtener_tiempo(self):
        if modo_discapacidad:
            return 150
        tiempos = {"facil": 90, "intermedio": 70, "dificil": 50, "extremo": 30}
        return tiempos.get(self.nivel, 60)

    def obtener_vidas(self):
        if modo_discapacidad:
            return 5
        vidas = {"facil": 5, "intermedio": 4, "dificil": 3, "extremo": 2}
        return vidas.get(self.nivel, 3)

    def crear_interfaz(self):
        tk.Label(self.master, text=f"🧮 Nivel: {self.nivel.title()}",
                 font=("Arial Rounded MT Bold", 28 if modo_discapacidad else 22),
                 fg="yellow" if modo_discapacidad else "white",
                 bg="black" if modo_discapacidad else "#1e3c72").pack(pady=10)

        estado = tk.Frame(self.master, bg="black" if modo_discapacidad else "#1e3c72")
        estado.pack(pady=5)
        self.lbl_puntos = tk.Label(estado, text=f"🏆 Puntos: {self.puntos}",
                                   fg="yellow" if modo_discapacidad else "white",
                                   bg="black" if modo_discapacidad else "#1e3c72",
                                   font=("Arial Rounded MT Bold", 18 if modo_discapacidad else 14))
        self.lbl_puntos.grid(row=0, column=0, padx=20)
        self.lbl_vidas = tk.Label(estado, text=f"❤️ Vidas: {self.vidas}",
                                  fg="yellow" if modo_discapacidad else "white",
                                  bg="black" if modo_discapacidad else "#1e3c72",
                                  font=("Arial Rounded MT Bold", 18 if modo_discapacidad else 14))
        self.lbl_vidas.grid(row=0, column=1, padx=20)
        self.lbl_tiempo = tk.Label(estado, text=f"⏱️ {self.tiempo}s",
                                   fg="yellow" if modo_discapacidad else "white",
                                   bg="black" if modo_discapacidad else "#1e3c72",
                                   font=("Arial Rounded MT Bold", 18 if modo_discapacidad else 14))
        self.lbl_tiempo.grid(row=0, column=2, padx=20)

        self.lbl_pregunta = tk.Label(self.master, text="", font=("Arial Rounded MT Bold", 32 if modo_discapacidad else 22),
                                     fg="yellow" if modo_discapacidad else "white",
                                     bg="black" if modo_discapacidad else "#333333")
        self.lbl_pregunta.pack(pady=40)

        self.entrada = tk.Entry(self.master, font=("Arial Rounded MT Bold", 28 if modo_discapacidad else 22),
                                justify="center", width=12 if modo_discapacidad else 10)
        self.entrada.pack(pady=10)
        self.entrada.bind("<Return>", lambda e: self.verificar())

        crear_boton(self.master, "✅ Enviar", self.verificar, "#4CAF50").pack(pady=10)
        crear_boton(self.master, "🏠 Menú Principal", self.volver, "#9E9E9E").pack(pady=10)

    def generar_pregunta(self):
        nivel = self.nivel
        if nivel in ["facil", "intermedio"]:
            operaciones = ["+", "-", "×"]
        else:
            operaciones = ["+", "-", "×", "÷", "√"]
        op = random.choice(operaciones)
        if op == "+":
            n1, n2 = random.randint(1, 20), random.randint(1, 20)
            self.respuesta = n1 + n2
            texto = f"{n1} + {n2}"
        elif op == "-":
            n1, n2 = random.randint(1, 20), random.randint(1, 20)
            self.respuesta = n1 - n2
            texto = f"{n1} - {n2}"
        elif op == "×":
            n1, n2 = random.randint(2, 10), random.randint(2, 10)
            self.respuesta = n1 * n2
            texto = f"{n1} × {n2}"
        elif op == "÷":
            divisor = random.randint(2, 10)
            cociente = random.randint(2, 10)
            dividendo = divisor * cociente
            self.respuesta = cociente
            texto = f"{dividendo} ÷ {divisor}"
        elif op == "√":
            raiz = random.randint(2, 12)
            cuadrado = raiz * raiz
            self.respuesta = raiz
            texto = f"√{cuadrado}"
        self.lbl_pregunta.config(text=f"¿Cuánto es {texto}?")

    def verificar(self):
        try:
            valor = int(self.entrada.get())
            if valor == self.respuesta:
                self.puntos += 10
                self.lbl_puntos.config(text=f"🏆 Puntos: {self.puntos}")
                self.lbl_pregunta.config(fg="green" if not modo_discapacidad else "lime")
            else:
                self.vidas -= 1
                self.lbl_vidas.config(text=f"❤️ Vidas: {self.vidas}")
                self.lbl_pregunta.config(fg="red")
                if self.vidas <= 0:
                    self.fin_juego()
                    return
            self.entrada.delete(0, tk.END)
            self.master.after(800 if not modo_discapacidad else 1500, self.generar_pregunta)
        except ValueError:
            self.entrada.delete(0, tk.END)

    def contar_tiempo(self):
        if self.tiempo > 0 and self.vidas > 0:
            self.tiempo -= 1
            self.lbl_tiempo.config(text=f"⏱️ {self.tiempo}s")
            self.master.after(1000, self.contar_tiempo)
        else:
            self.fin_juego()

    def fin_juego(self):
        self.limpiar()
        tk.Label(self.master, text=f"🎯 Fin del Juego\nPuntos: {self.puntos}",
                 font=("Arial Rounded MT Bold", 32 if modo_discapacidad else 24),
                 fg="yellow" if modo_discapacidad else "white",
                 bg="black" if modo_discapacidad else "#1e3c72").pack(pady=150)
        crear_boton(self.master, "🔁 Jugar de Nuevo", self.reiniciar, "#4CAF50").pack(pady=10)
        crear_boton(self.master, "🏠 Menú Principal", self.volver, "#9E9E9E").pack(pady=10)

    def reiniciar(self):
        self.limpiar()
        JuegoPrincipal(self.master, self.nivel)

    def volver(self):
        self.limpiar()
        PantallaInicio(self.master)

# ======= EJECUCIÓN ======= #
if __name__ == "__main__":
    root = tk.Tk()
    root.title("🎮 MindMath")
    PantallaInicio(root)
    root.mainloop()
