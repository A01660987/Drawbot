import tkinter as tk
from math import trunc
import re

# se implementa el parser utilizando el método de descenso recursivo

def sigToken():
    global t
    t += 1
    if t < len(entrada):
        return entrada[t]
    else:
        raise Exception("Error: Fin de línea inesperado después de " + entrada[t-1] + ".")

def parse_int():
    if token.isdigit():
        return True
    else:
        return False

def comando():
    if parse_adelante() or parse_atras() or parse_izquierda() or parse_derecha() or parse_levantar() or parse_bajar() or parse_color() or parse_limpiar() or parse_centro() or parse_repetir() or parse_script():
        return True
    elif t == 0:
        raise Exception("Error: Se esperaba comando.")
    else:
        raise Exception("Error: Se esperaba comando después de: " + entrada[t-1] + ".")
    
def bucle(n, t_inicio, i):
    global token, t
    if re.match(r"\)", token):
        i += 1
        if i == n:
            return True
        else:
            t = t_inicio - 1
            token = sigToken()
            bucle(n, t_inicio, i)
    elif t < len(entrada) and comando():
        token = sigToken()
        bucle(n, t_inicio, i)
    else:
        raise Exception("Error: Se esperaba comando o ')' después de: " + entrada[t-1] + ".")
    
def parse_adelante():
    global token
    if re.match(r"adelante", token):
        token = sigToken()
        if parse_int():
            adelante(int(token))
            return True
        else:
            raise Exception("Error: Se esperaba int después de: " + entrada[t-1] + ".")
    else:
        return False
    
def parse_atras():
    global token
    if re.match(r"atras", token):
        token = sigToken()
        if parse_int():
            atras(int(token))
            return True
        else:
            raise Exception("Error: Se esperaba int después de: " + entrada[t-1] + ".")
    else:
        return False
    
def parse_izquierda():
    global token
    if re.match(r"izquierda", token):
        rotar(90)
        return True
    else:
        return False
    
def parse_derecha():
    global token
    if re.match(r"derecha", token):
        rotar(-90)
        return True
    else:
        return False
    
def parse_levantar():
    global token
    if re.match(r"levantar", token):
        pluma(False)
        return True
    else:
        return False
    
def parse_bajar():
    global token
    if re.match(r"bajar", token):
        pluma(True)
        return True
    else:
        return False
    
def parse_color():
    global token
    if re.match(r"color", token):
        token = sigToken()
        if re.match(r"#[0-9a-fA-F]{6}", token):
            set_color(token)
            return True
        else:
            raise Exception("Error: Se esperaba código hexadecimal de color (#nnnnnn) después de: " + entrada[t-1] + ".")
    else:
        return False
    
def parse_limpiar():
    global token
    if re.match(r"limpiar", token):
        limpiar()
        return True
    else:
        return False
    
def parse_centro():
    global token
    if re.match(r"centro", token):
        centro()
        return True
    else:
        return False
    
def parse_repetir():
    global token
    if re.match(r"repetir", token):
        token = sigToken()
        if parse_int():
            n = int(token)
            token = sigToken()
            if re.match(r"\(", token):
                token = sigToken()
                bucle(n, t, 0)
                return True
            else:
                raise Exception("Error: Se esperaba '(' después de: " + entrada[t-1] + ".")
        else:
            raise Exception("Error: Se esperaba int después de: " + entrada[t-1] + ".")
    else:
        return False

def parse_script():
    global token
    if re.match(r"script", token):
        token = sigToken()
        if re.match(r"\".*\"", token):
            script(token)
            return True
        else:
            raise Exception("Error: Se esperaba nombre de archivo entre comillas después de: " + entrada[t-1] + ".")
    else:
        return False

ventana = tk.Tk()
ventana.title("Drawbot")

# se definen los parámetros iniciales

tamaño_pantalla = 500                   # default: 500
num_celdas = 25                         # default: 25
celda = (tamaño_pantalla/num_celdas)    # default: 500/25 = 20

angulo = 90                             # default: 90
pluma_abajo = True                      # default: True
color = "#000000"                       # default: "#000000"

canvas = tk.Canvas(ventana, width=tamaño_pantalla, height=tamaño_pantalla, bg="white")
canvas.pack()

for i in range(1, num_celdas):          # se dibuja la cuadrícula
    canvas.create_line(i*celda, 0, i*celda, tamaño_pantalla, fill="#e3e3e3")
    canvas.create_line(0, i*celda, tamaño_pantalla, i*celda, fill="#e3e3e3")

x = trunc(num_celdas/2)*celda
y = x

# se definen las funciones que rigen el comportamiento de Drawbot

def adelante(casillas):
    global x, y, dibujo, dibujos
    i = 0
    while i < casillas:
        if angulo == 0 and x < trunc(tamaño_pantalla-celda):
            x += celda
            if pluma_abajo:
                dibujo = canvas.create_line(x+celda/2, y+celda/2, x-celda+celda/2, y+celda/2, fill=color)
                dibujos.append(dibujo)
        elif angulo == 90 and y > 0:
            y -= celda
            if pluma_abajo:
                dibujo = canvas.create_line(x+celda/2, y+celda/2, x+celda/2, y+celda+celda/2, fill=color)
                dibujos.append(dibujo)
        elif angulo == 180 and x > 0:
            x -= celda
            if pluma_abajo:
                dibujo = canvas.create_line(x+celda/2, y+celda/2, x+celda+celda/2, y+celda/2, fill=color)
                dibujos.append(dibujo)
        elif angulo == 270 and y < trunc(tamaño_pantalla-celda):
            y += celda
            if pluma_abajo:
                dibujo = canvas.create_line(x+celda/2, y+celda/2, x+celda/2, y-celda+celda/2, fill=color)
                dibujos.append(dibujo)
        i += 1
    render()

def atras(casillas):
    global x, y
    i = 0
    while i < casillas:
        if angulo == 0 and x < trunc(tamaño_pantalla-celda):
            x -= celda
            if pluma_abajo:
                dibujo = canvas.create_line(x+celda/2, y+celda/2, x+celda+celda/2, y+celda/2, fill=color)
                dibujos.append(dibujo)
        elif angulo == 90 and y > 0:
            y += celda
            if pluma_abajo:
                dibujo = canvas.create_line(x+celda/2, y+celda/2, x+celda/2, y-celda+celda/2, fill=color)
                dibujos.append(dibujo)
        elif angulo == 180 and x > 0:
            x += celda
            if pluma_abajo:
                dibujo = canvas.create_line(x+celda/2, y+celda/2, x-celda+celda/2, y+celda/2, fill=color)
                dibujos.append(dibujo)
        elif angulo == 270 and y < trunc(tamaño_pantalla-celda):
            y -= celda
            if pluma_abajo:
                dibujo = canvas.create_line(x+celda/2, y+celda/2, x+celda/2, y+celda+celda/2, fill=color)
                dibujos.append(dibujo)
        i += 1
    render()

def rotar(grados):
    global angulo
    angulo += grados
    if angulo == 360:
        angulo = 0
    elif angulo == -90:
        angulo = 270
    render()

def pluma(bool):
    global pluma_abajo
    pluma_abajo = bool

def set_color(hex):
    global color
    color = hex
    render()

def limpiar():
    global dibujo, dibujos
    try:
        for i in dibujos:
            canvas.delete(i)
    except:
        pass
    
def centro():
    global x, y, angulo
    x = trunc(num_celdas/2)*celda
    y = x
    angulo = 90
    render()

def script(nombre):
    global entrada, t, token
    nombre = re.sub(r'"', "", nombre)
    try:
        archivo = open(nombre, 'r')
    except:
        raise Exception("Error: El archivo especificado no existe.")
    lineas = archivo.readlines()
    for linea in lineas:
        global entrada, t, token, display
        input = linea
        input = re.sub(r"\(", "( ", input)
        input = re.sub(r"\)", " )", input)
        entrada = re.split(r"\s+", input)
        t = 0
        token = entrada[t]
        comando()
    
def render():
    global x, y, drawbot
    canvas.delete(drawbot)
    if angulo == 0:
        drawbot = canvas.create_polygon(x, y, x+celda, y+celda/2, x, y+celda, x+celda/3, y+celda/2, fill=color)
    elif angulo == 90:
        drawbot = canvas.create_polygon(x+celda/2, y, x+celda, y+celda, x+celda/2, y+2*celda/3, x, y+celda, fill=color)
    elif angulo == 180:
        drawbot = canvas.create_polygon(x+celda, y, x, y+celda/2, x+celda, y+celda, x+2*celda/3, y+celda/2, fill=color)
    elif angulo == 270:
        drawbot = canvas.create_polygon(x+celda/2, y+celda, x+celda, y, x+celda/2, y+celda/3, x, y, fill=color)

def recibirInput(event):
    global entrada, t, token, display
    input = cajaInput.get()
    input = re.sub(r"\(", "( ", input)      # se añaden espacios entre los paréntesis para separar los tokens correctamente
    input = re.sub(r"\)", " )", input)
    entrada = re.split(r"\s+", input)
    t = 0
    token = entrada[t]
    try:
        comando()
        display.set(input)                  # si el comando ingresado fue correcto, se muestra en pantalla
    except Exception as error:              # si hubo un error, este se muestra
        display.set(error)
    cajaInput.delete(0, tk.END)

cajaInput = tk.Entry(width=80)  # se crea el cuadro de texto para ingresar comandos
cajaInput.pack(pady=5)

ventana.bind('<Return>', recibirInput)      # al presionar la tecla Enter, se ejecuta el comando escrito

display = tk.StringVar()
mensaje = tk.Label(textvariable=display)
mensaje.pack()

drawbot = canvas.create_polygon(x+celda/2, y, x+celda, y+celda, x+celda/2, y+2*celda/3, x, y+celda, fill=color)
dibujos = []
ventana.mainloop()