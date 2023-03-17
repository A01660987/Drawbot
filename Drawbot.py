import tkinter as tk
from math import trunc
import re

def sigToken():
    global t
    t += 1
    if t < len(entrada):
        return entrada[t]
    else:
        error
    return entrada[t]

def int():
    if token.isdigit():
        return True
    else:
        return False

def comando():
    if adelante() or atras() or izquierda() or derecha() or levantar() or bajar() or color() or limpiar() or centro() or repetir() or script():
        return True
    else:
        return False
    
def adelante():
    global token
    if re.match(r"adelante", token):
        token = sigToken()
        if int():
            return True
        else:
            return False
    else:
        return False
    
def atras():
    global token
    if re.match(r"atras", token):
        token = sigToken()
        if int():
            return True
        else:
            return False
    else:
        return False
    
def izquierda():
    global token
    if re.match(r"izquierda", token):
        return True
    else:
        return False
    
def derecha():
    global token
    if re.match(r"derecha", token):
        return True
    else:
        return False
    
def levantar():
    global token
    if re.match(r"levantar", token):
        return True
    else:
        return False
    
def bajar():
    global token
    if re.match(r"bajar", token):
        return True
    else:
        return False
    
def color():
    global token
    if re.match(r"color", token):
        token = sigToken()
        if re.match(r"#[0-9a-fA-F]{6}", token):
            return True
        else:
            return False
    else:
        return False
    
def limpiar():
    global token
    if re.match(r"limpiar", token):
        return True
    else:
        return False
    
def centro():
    global token
    if re.match(r"centro", token):
        return True
    else:
        return False
    
def repetir():
    global token
    if re.match(r"repetir", token):
        token = sigToken()
        if int():
            token = sigToken()
            if comando():
                while t < len(entrada)-1:
                    token = sigToken()
                    if not comando():
                        return False
                return True
            else:
                return False
        else:
            return False
    else:
        return False
    
def script():
    global token
    if re.match(r"script", token):
        token = sigToken()
        if re.match(r"\".*\"", token):
            return True
        else:
            return False
    else:
        return False

ventana = tk.Tk()
ventana.title("DrawbotTK")

tamaño_pantalla = 500       # default: 500
num_celdas = 25             # default: 25
celda = (tamaño_pantalla/num_celdas)
angulo = 0
pluma_abajo = True
color = "#000000"

canvas = tk.Canvas(ventana, width=tamaño_pantalla, height=tamaño_pantalla, bg="white")
canvas.pack()

for i in range(1, num_celdas):      # se dibuja la cuadrícula
    canvas.create_line(i*celda, 0, i*celda, tamaño_pantalla, fill="#e3e3e3")
    canvas.create_line(0, i*celda, tamaño_pantalla, i*celda, fill="#e3e3e3")

x = trunc(num_celdas/2)*celda
y = x

def funcAdelante(casillas, angulo, x, y):
    i = 0
    while i < casillas and x in range(0, trunc(tamaño_pantalla-celda)) and y in range(0, trunc(tamaño_pantalla-celda)):
        if angulo == 0:
            x += celda
        elif angulo == 90:
            y += celda
        elif angulo == 180:
            x -= celda
        elif angulo == 270:
            y -= celda
        i += 1
        return x, y


def render(x, y):
    if angulo == 0:
        canvas.create_polygon(x, y, x+celda, y+celda/2, x, y+celda, x+celda/3, y+celda/2, fill=color)
    elif angulo == 90:
        canvas.create_polygon(x+celda/2, y, x+celda, y+celda, x+celda/2, y+2*celda/3, x, y+celda, fill=color)
    elif angulo == 180:
        canvas.create_polygon(x+celda, y, x, y+celda/2, x+celda, y+celda, x+2*celda/3, y+celda/2, fill=color)
    elif angulo == 270:
        canvas.create_polygon(x+celda/2, y+celda, x+celda, y, x+celda/2, y+celda/3, x, y, fill=color)

def recibirInput(event):
    global entrada
    entrada = re.split(r" |\(|, " ,cajaInput.get())
    global t
    t = 0
    global token
    token = entrada[t]
    comando()
    cajaInput.delete(0, tk.END)

cajaInput = tk.Entry(width=80)  # se crea el cuadro de texto para ingresar comandos
cajaInput.pack(pady=5)

ventana.bind('<Return>', recibirInput)      # al presionar la tecla Enter, se ejecuta el comando escrito

render(x, y)
ventana.mainloop()


# <programa> ::= <comando> {"\n" <comando>}
# <int> ::= (0 | 1 | 2 | 3 | 4 | 5| 6 | 7 | 8 | 9)*;
# <hex> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F';
# <comando> ::= <adelante> | <atras> | <izquierda> | <derecha> | <levantar> | <bajar> | <color> | <limpiar> | <centro> | <repetir> | <script>;
# <bucle> ::= 
# <adelante> ::= "adelante " <int>;
# <atras> ::= "atras " <int>;
# <izquierda> ::= "izquierda";
# <derecha> ::= "derecha";
# <levantar> ::= "levantar";
# <bajar> ::= "bajar";
# <color>  ::= "color " '#' <hex> <hex> <hex> <hex> <hex> <hex>;
# <limpiar> ::= "limpiar";
# <centro> ::= "centro";
# <repetir> ::= "repetir " <int> <comando> {<comando>};
# <script> ::= "script " '"' {.} '"';
