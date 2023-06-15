# Carrusel Vertical
### Evidencia #2: Implementación de un simulador de almacén automatizado

La situación problema de este segundo periodo consistió en programar la simulación de un carrusel vertical de almacenamiento en el lenguaje de programación Racket, del paradigma funcional. Racket es un dialecto moderno del lenguaje Lisp, y es derivado de Scheme.

El carrusel vertical de almacenamiento tiene la ventaja de ser compacto y ocupar poco espacio de suelo para la cantidad de productos que puede almacenar, mientras que todos los productos permanecen fácilmente accesibles para el usuario.

#### Diseño de las estructuras de datos

Para simular esta estructura dentro de Racket, utilizaré listas anidadas que contengan el nombre del producto, su cantidad y su precio unitario, en el siguiente formato:
(((producto 1 cantidad precio) (producto 2 cantidad precio) (producto 3 cantidad precio))
((producto 4 cantidad precio) (producto 5 cantidad precio) (producto 6 cantidad precio))
((producto 7 cantidad precio) (producto 8 cantidad precio) (producto 9 cantidad precio)))

El tamaño del carrusel será configurable y dinámico; el código se adaptará sin importar el número de filas y columnas, lo único imperativo es que no varíe el número de columnas en cada fila y el número de filas en cada columna.

Este será almacenado dentro de un archivo de texto llamado “carrusel.txt”, el cuál deberá estar colocado dentro del mismo directorio que el archivo de Racket. Después de la lista que representa al carrusel, este archivo de texto contendrá un elemento más que representará el producto que actualmente estará mostrando el carrusel.

Para simular el movimiento del carrusel, se utilizarán cuatro letras para moverse:

• **a**, hacia arriba.

• **b**, hacia abajo.

• **c**, hacia la izquierda.

• **d**, hacia la derecha

Las transacciones que se desean realizar con el carrusel deberán estar almacenadas en un archivo llamado “transacciones.txt”, también almacenado en el mismo directorio que el archivo Racket. Las transacciones posibles en el sistema serán:

• **(a)** – El carrusel se moverá hacia arriba.

• **(b)** – El carrusel se moverá hacia abajo.

• **(c)** – El carrusel se moverá hacia la izquierda.

• **(d)** – El carrusel se moverá hacia la derecha.

• **(retirar cantidad {producto})** – Si no se especifica producto, se retirará la cantidad del producto actualmente mostrado. Si se especifica un producto existente, el carrusel se moverá a la posición del producto especificado, y mostrará la ruta más eficiente para llegar a esta posición. Si se intentan retirar más de las existencias del producto, se retirará todo y se marcará un error.

• **(agregar cantidad {producto})** – Al igual que la función retirar, si no se especifica un producto se agregará al producto actual, y si sí, se moverá el carrusel a la posición del producto utilizando la ruta más eficiente.
