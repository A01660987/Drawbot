# Drawbot
### Evidencia #1: Diseño e implementación básica de un DSL para enseñar a programar a niños

La situación problema del primer periodo de esta materia consistió en la creación de un lenguaje de programación de dominio específico (DSL) inspirado en Logo, un lenguaje simple que consiste en un ambiente gráfico con una tortuga que dibuja en pantalla y cuyo movimiento puede ser controlado con comandos básicos. Para este fin, he diseñado a “Drawbot” un ambiente gráfico construido en Python 3 utilizando el paquete Tkinter, que consiste en una flechita que, al igual que la tortuga de Logo, dibuja en pantalla y se mueve mediante comandos escritos por el usuario o cargados en un script.

Los comandos o lexemas que acepta Drawbot son los siguientes:

• **adelante n** – Drawbot se moverá hacia adelante n número de casillas.

• **atras n** – Drawbot se moverá hacia atrás n número de casillas.

• **izquierda** – Drawbot rotará 90° a la izquierda.

• **derecha** – Drawbot rotará 90° a la derecha.

• **levantar** – Drawbot dejará de dibujar al moverse.

• **bajar** – Drawbot comenzará a dibujar al moverse.

• **color #nnnnnn** – El color de la pluma cambiará al valor hexadecimal especificado.

• **limpiar** – La pantalla se despejará de todos los dibujos.

• **centro** – Drawbot regresará al centro exacto de la pantalla apuntando hacia arriba.

• **repetir n (comando1, comando2, …)** – Los comandos dentro de los paréntesis se repetirán en orden n número de veces.

• **script “archivo.txt”** – Se ejecutarán los comandos escritos línea por línea dentro del archivo txt especificado.
