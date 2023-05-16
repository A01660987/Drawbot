#lang racket/load

; Solución a la situación problema #2
; Diego Andrés Figueroa Peart
; A01660987


(define (archivo)   ; Se lee el archivo que contiene el carrusel y el estado actual.
  (define lectura (open-input-file "carrusel.txt"))
  (define contenido (read lectura))
  (close-input-port lectura)
  contenido)

(define (carrusel) (car (archivo)))   ; Se genera la lista del carrusel cada vez que se ejecuta una transacción.
(define (est-actual) (cadr (archivo)))
(define filas (length (carrusel)))
(define columnas (length (car (carrusel))))

(define (coordenadas lst f x y)
  (if (null? lst) f
      (if (<= y columnas)
          (coordenadas (cdr lst) (append f (list (list (caar lst) (cons x y)))) x (+ y 1))
          (coordenadas lst f (+ x 1) 1))))

(define (diccionario) (coordenadas (apply append (carrusel)) '() 1 1))

(define (buscar producto)   ; Se busca un producto a partir de su nombre, se regresan sus coordenadas.
   (cadar (filter (lambda (p) (equal? producto (car p))) (diccionario))))

(define (buscar-f producto)   ; Se busca un producto especificado por el usuario, si se regresa falso es que no existe.
  (define x (filter (lambda (p) (equal? producto (car p))) (diccionario)))
  (if (null? x) #f
      (cadar x)))

(define (detalles x y lst)   ; Se reciben las coordenadas del producto y se regresa su nombre, cantidad y precio.
  (define (elemento y lst)
    (if (not (= 1 y))
        (elemento (- y 1) (cdr lst))
        (car lst)))
  (if (not (= 1 x))
      (detalles (- x 1) y (cdr lst))
      (elemento y (car lst))))

(define (reemplazar-elem producto x y lst f)  ; Se cambia la cantidad del producto en el carrusel para luego sobreescribir el archivo.
  (define (reemplazar-fila producto y lst f)
    (cond
      ((null? lst) (list f))
      ((= y 1) (reemplazar-fila producto (- y 1) (cdr lst) (append f (list producto))))
      (else (reemplazar-fila producto (- y 1) (cdr lst) (append f (list (car lst)))))))
  (cond
    ((null? lst) f)
    ((= 1 x) (reemplazar-elem producto (- x 1) y (cdr lst) (append f (reemplazar-fila producto y (car lst) '()))))
    (else (reemplazar-elem producto (- x 1) y (cdr lst) (append f (list (car lst)))))))

(define valor-total (apply + (map (lambda (x) (* (cadr x) (caddr x))) (apply append (carrusel)))))  ; Se calcula el valor total del inventario.

(define (productos-bajos-aux lst f)
  (if (null? lst) f
      (productos-bajos-aux (cdr lst) (append f (list (list (caar lst) (cadar lst) (buscar (caar lst))))))))
(define productos-bajos (productos-bajos-aux (filter (lambda (x) (> 20 (cadr x))) (apply append (carrusel))) '()))  ; Se regresan los productos con menos de 20 unidades.

(define (escribir lst)   ; Se sobreescribe el archivo del carrusel con la lista recibida.
  (define output (open-output-file "carrusel.txt" #:exists 'replace))
  (write lst output)
  (close-output-port output))

(define (a)   ; Movimiento hacia arriba.
  (define coords (buscar (est-actual)))
  (define lista (carrusel))
  (if (= 0 (- (car coords) 1))
      (begin
        (displayln (detalles filas (cdr coords) lista)))
      (begin
        (displayln (detalles (- (car coords) 1) (cdr coords) lista))
        (escribir (list (carrusel) (car (detalles (- (car coords) 1) (cdr coords) lista)))))))

(define (b)   ; Movimiento hacia abajo.
  (define coords (buscar (est-actual)))
  (define lista (carrusel))
  (if (= filas (+ (car coords) 1))
      (begin
        (displayln (detalles 1 (cdr coords) lista)))
      (begin
        (displayln (detalles (+ (car coords) 1) (cdr coords) lista))
        (escribir (list lista (car (detalles (+ (car coords) 1) (cdr coords) lista)))))))

(define (c)  ; Movimiento hacia la izquierda.
  (define coords (buscar (est-actual)))
  (define lista (carrusel))
  (if (= 0 (- (cdr coords) 1))
      (begin
        (displayln "Movimiento inválido."))
      (begin
        (displayln (detalles (car coords) (- (cdr coords) 1) lista))
        (escribir (list lista (car (detalles (car coords) (- (cdr coords) 1) lista)))))))

(define (d)   ; Movimiento hacia la derecha.
  (define coords (buscar (est-actual)))
  (define lista (carrusel))
  (if (< columnas (+ (cdr coords) 1))
      (begin
        (displayln "Movimiento inválido."))
      (begin
        (displayln (detalles (car coords) (+ (cdr coords) 1) lista))
        (escribir (list lista (car (detalles (car coords) (+ (cdr coords) 1) lista)))))))

(define (arriba x1 x2 lst)
  (if (= x1 x2) lst
      (if (= x1 1)
          (arriba filas x2 (append lst (list 'a)))
          (arriba (- x1 1) x2 (append lst (list 'a))))))

(define (abajo x1 x2 lst)
  (if (= x1 x2) lst
      (if (= x1 filas)
          (abajo 1 x2 (append lst (list 'b)))
          (abajo (+ x1 1) x2 (append lst (list 'b))))))

(define (distancia-y y1 y2 lst)
  (if (= y1 y2) lst
      (if (> y1 y2)
          (distancia-y (- y1 1) y2 (append lst (list 'c)))
          (distancia-y (+ y1 1) y2 (append lst (list 'd))))))

(define (distancia x1 y1 x2 y2 lst)   ; Se calcula la distancia entre el producto actual y el producto al que se desea llegar, se determina la ruta más rápida.
  (cond
    ((< x1 x2) (if (> (- x2 x1) (/ filas 2))
                   (distancia 0 y1 0 y2 (arriba x1 x2 lst))
                   (distancia 0 y1 0 y2 (abajo x1 x2 lst))))
    ((> x1 x2) (if (> (- x1 x2) (/ filas 2))
                   (distancia 0 y1 0 y2 (abajo x1 x2 lst))
                   (distancia 0 y1 0 y2 (arriba x1 x2 lst))))
    (else (begin
            (display "Ruta más corta: ")
            (displayln (distancia-y y1 y2 lst))))))

(define (retirar-n cantidad)  ; Se retira la cantidad del producto que se muestra actualmente.
  (define coords (buscar (est-actual)))
  (define lista (carrusel))
  (define producto (detalles (car coords) (cdr coords) lista))
  (if (< (- (cadr producto) cantidad) 0)  ; Se revisa si la cantidad a retirar es mayor que la existencia.
      (begin
        (displayln "Se intentó retirar más de la cantidad existente.")
        (escribir (list (reemplazar-elem (list (car producto) 0 (caddr producto)) (car coords) (cdr coords) lista '()) (car producto))))
      (escribir (list (reemplazar-elem (list (car producto) (- (cadr producto) cantidad) (caddr producto)) (car coords) (cdr coords) lista '()) (car producto)))))

(define (retirar-p cantidad prod)  ; Se retira la cantidad del producto especificado.
  (define origen (buscar (est-actual)))
  (define destino (buscar-f (car prod)))
  (define lista (carrusel))
  (if (not destino)
      (displayln "Producto no encontrado.")
      (begin
        (if (equal? origen destino)
            (void)
            (distancia (car origen) (cdr origen) (car destino) (cdr destino) '()))
        (if (< (- (cadr (detalles (car destino) (cdr destino) lista)) cantidad) 0)
            (begin
              (displayln "Se intentó retirar más de la cantidad existente.")
              (escribir (list (reemplazar-elem (list (car (detalles (car destino) (cdr destino) lista)) 0 (caddr (detalles (car destino) (cdr destino) lista))) (car destino) (cdr destino) lista '()) (car (detalles (car destino) (cdr destino) lista)))))
            (escribir (list (reemplazar-elem (list (car (detalles (car destino) (cdr destino) lista)) (- (cadr (detalles (car destino) (cdr destino) lista)) cantidad) (caddr (detalles (car destino) (cdr destino) lista))) (car destino) (cdr destino) lista '()) (car (detalles (car destino) (cdr destino) lista))))))))

(define (retirar cantidad . producto)  ; Se especifica un argumento opcional para la función retirar.
  (if (null? producto)
      (retirar-n cantidad)
      (retirar-p cantidad producto)))

(define (agregar-n cantidad)  ; Se agrega la cantidad al producto que se muestra actualmente.
  (define coords (buscar (est-actual)))
  (define lista (carrusel))
  (define producto (detalles (car coords) (cdr coords) lista))
  (escribir (list (reemplazar-elem (list (car producto) (+ (cadr producto) cantidad) (caddr producto)) (car coords) (cdr coords) lista '()) (car producto))))

(define (agregar-p cantidad prod)  ; Se agrega la cantidad al producto especificado.
  (define origen (buscar (est-actual)))
  (define destino (buscar-f (car prod)))
  (define lista (carrusel))
  (if (not destino)
      (displayln "Producto no encontrado.")
      (begin
        (if (equal? origen destino)
            (void)
            (distancia (car origen) (cdr origen) (car destino) (cdr destino) '()))
        (escribir (list (reemplazar-elem (list (car (detalles (car destino) (cdr destino) lista)) (+ (cadr (detalles (car destino) (cdr destino) lista)) cantidad) (caddr (detalles (car destino) (cdr destino) lista))) (car destino) (cdr destino) lista '()) (car (detalles (car destino) (cdr destino) lista)))))))

(define (agregar cantidad . producto)  ; Se especifica un argumento opcional para la función agregar.
  (if (null? producto)
      (agregar-n cantidad)
      (agregar-p cantidad producto)))

(define (realizar-transacciones arch)  ; Se leerán y ejecutarán las transacciones línea por línea.
  (load arch))

(realizar-transacciones "transacciones.txt")

(display "Valor total del inventario: ") (displayln valor-total)
(display "Productos con poco o nulo inventario: ") (displayln productos-bajos)