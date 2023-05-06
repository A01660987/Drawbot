#lang racket

(define archivo (open-input-file "carrusel.txt"))
(define transacciones (open-input-file "transacciones.txt"))

(define carrusel (read archivo))
(define est-actual (read archivo))
(define filas (length carrusel))
(define columnas (length (car carrusel)))

(define (coordenadas lst f x y)
  (if (null? lst) f
      (if (<= y columnas)
          (coordenadas (cdr lst) (append f (list (list (caar lst) (cons x y)))) x (+ y 1))
          (coordenadas lst f (+ x 1) 1))))

(define diccionario (coordenadas (apply append carrusel) '() 1 1))

(define (buscar producto)
  (cadar (filter (lambda (producto) (equal? producto (car diccionario))) diccionario)))

(define valor-total (apply + (map (lambda (x) (* (cadr x) (caddr x))) (apply append carrusel))))

(define (productos-bajos-aux lst f)
  (if (null? lst) f
      (productos-bajos-aux (cdr lst) (append f (list (list (caar lst) (cadar lst) (buscar (caar lst))))))))
(define productos-bajos (productos-bajos-aux (filter (lambda (x) (> 20 (cadr x))) (apply append carrusel)) '()))

(define a (print "hola"))

(define (realizar-transacciones)
  (define transaccion (read transacciones))
  (if (eof-object? transaccion)
      (void)
      (begin
        transaccion
        (realizar-transacciones))))

(realizar-transacciones)

"Valor total del inventario:" valor-total
"Productos con poco o nulo inventario:" productos-bajos