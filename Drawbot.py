import tkinter as tk
from math import trunc
import re

lista_regex = {r"^adelante [0-9]+$", r"^atras [0-9]+$", r"^izquierda$", r"^derecha$", r"^levantar$", r"^bajar$", r"^color #[0-9a-fA-F]{6}$", r"^limpiar$", r"^centro$", r"^repetir [0-9]+ \((adelante [0-9]+|atras [0-9]+|izquierda|derecha|levantar|bajar|color #[0-9a-fAF]{6}|limpiar|centro|, )+\)$"}

def adelante(casillas, angulo, x, y):
    i = 0
    while i < casillas and x in range(0, tamaño_pantalla-celda) and y in range(0, tamaño_pantalla-celda):
        if angulo == 0:
            x += celda
        elif angulo == 90:
            y += celda
        elif angulo == 180:
            x -= celda
        elif angulo == 270:
            y -= celda
        i += 1


ventana = tk.Tk()
ventana.title("DrawbotTK")

tamaño_pantalla = 500       # default: 900
num_celdas = 25             # default: 25
celda = (tamaño_pantalla/num_celdas)

canvas = tk.Canvas(ventana, width=tamaño_pantalla, height=tamaño_pantalla, bg="white")
canvas.pack()

for i in range(1, num_celdas):      # se dibuja la cuadrícula
    canvas.create_line(i*celda, 0, i*celda, tamaño_pantalla, fill="#e3e3e3")
    canvas.create_line(0, i*celda, tamaño_pantalla, i*celda, fill="#e3e3e3")

x = trunc(num_celdas/2)*celda
y = x
angulo = 270
color = "#000000"

if angulo == 0:
    drawbot = canvas.create_polygon(x, y, x+celda, y+celda/2, x, y+celda, x+celda/3, y+celda/2, fill=color)
elif angulo == 90:
    drawbot = canvas.create_polygon(x+celda/2, y, x+celda, y+celda, x+celda/2, y+2*celda/3, x, y+celda, fill=color)
elif angulo == 180:
    drawbot = canvas.create_polygon(x+celda, y, x, y+celda/2, x+celda, y+celda, x+2*celda/3, y+celda/2, fill=color)
elif angulo == 270:
    drawbot = canvas.create_polygon(x+celda/2, y+celda, x+celda, y, x+celda/2, y+celda/3, x, y, fill=color)

texto = tk.Text(ventana, width=80, height=1)        # se crea el cuadro de texto para ingresar comandos
texto.pack()

def mover(event):
    if texto.get("1.0", "end-1c").strip() == "adelante":
        adelante(1, angulo, x, y)
    texto.delete("1.0", "end")

texto.bind('<Return>', mover)       # al oprimir la tecla Enter se ejecuta el comando escrito en el cuadro de texto

ventana.mainloop()