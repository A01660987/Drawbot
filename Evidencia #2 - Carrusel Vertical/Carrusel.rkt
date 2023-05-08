#lang racket/load

(define transacciones (read (open-input-file "transacciones.txt")))

(define (archivo)
  (define lectura (open-input-file "carrusel.txt"))
  (define contenido (read lectura))
  (close-input-port lectura)
  contenido)

(define (carrusel) (car (archivo)))
(define (est-actual) (cadr (archivo)))
(define filas (length (carrusel)))
(define columnas (length (car (carrusel))))

(define (coordenadas lst f x y)
  (if (null? lst) f
      (if (<= y columnas)
          (coordenadas (cdr lst) (append f (list (list (caar lst) (cons x y)))) x (+ y 1))
          (coordenadas lst f (+ x 1) 1))))

(define (diccionario) (coordenadas (apply append (carrusel)) '() 1 1))

(define (buscar producto)
  (cadar (filter (lambda (p) (equal? producto (car p))) (diccionario))))

(define (detalles x y lst)
  (define (elemento y lst)
    (if (not (= 1 y))
        (elemento (- y 1) (cdr lst))
        (car lst)))
  (if (not (= 1 x))
      (detalles (- x 1) y (cdr lst))
      (elemento y (car lst))))

(define (reemplazar-elem producto x y lst f)
  (define (reemplazar-fila producto y lst f)
    (cond
      ((null? lst) f)
      ((= y 1) (reemplazar-fila producto (- y 1) (cdr lst) (append (list f) producto)))
      (else (reemplazar-fila producto (- y 1) (cdr lst) (append (list f) (car lst))))))
  (cond
    ((null? lst) f)
    ((= 1 x) (reemplazar-elem producto (- x 1) y (cdr lst) (append (list f) (reemplazar-fila producto y (car lst) '()))))
    (else (reemplazar-elem producto (- x 1) y (cdr lst) (append (list f) (car lst))))))

(define valor-total (apply + (map (lambda (x) (* (cadr x) (caddr x))) (apply append (carrusel)))))

(define (productos-bajos-aux lst f)
  (if (null? lst) f
      (productos-bajos-aux (cdr lst) (append f (list (list (caar lst) (cadar lst) (buscar (caar lst))))))))
(define productos-bajos (productos-bajos-aux (filter (lambda (x) (> 20 (cadr x))) (apply append (carrusel))) '()))

(define (escribir lst)
  (define output (open-output-file "carrusel.txt" #:exists 'replace))
  (write lst output)
  (close-output-port output))

(define (a)
  (define coords (buscar (est-actual)))
  (define lista (carrusel))
  (if (= 0 (- (car coords) 1))
      (begin
        (displayln (detalles filas (cdr coords) lista))
        (escribir (list lista (car (detalles filas (cdr coords) lista)))))
      (begin
        (displayln (detalles (- (car coords) 1) (cdr coords) lista))
        (escribir (list (carrusel) (car (detalles (- (car coords) 1) (cdr coords) lista)))))))

(define (b)
  (define coords (buscar (est-actual)))
  (define lista (carrusel))
  (if (= filas (+ (car coords) 1))
      (begin
        (displayln (detalles 1 (cdr coords) lista))
        (escribir (list lista (car (detalles 1 (cdr coords) lista)))))
      (begin
        (displayln (detalles (+ (car coords) 1) (cdr coords) lista))
        (escribir (list lista (car (detalles (+ (car coords) 1) (cdr coords) lista)))))))

(define (c)
  (define coords (buscar (est-actual)))
  (define lista (carrusel))
  (if (= 0 (- (cdr coords) 1))
      (begin
        (displayln "Movimiento inválido.")
        (escribir (list lista (car (detalles (car coords) (cdr coords) lista)))))
      (begin
        (displayln (detalles (car coords) (- (cdr coords) 1) lista))
        (escribir (list lista (car (detalles (car coords) (- (cdr coords) 1) lista)))))))

(define (d)
  (define coords (buscar (est-actual)))
  (define lista (carrusel))
  (if (< columnas (+ (cdr coords) 1))
      (begin
        (displayln "Movimiento inválido.")
        (escribir (list lista (car (detalles (car coords) (cdr coords) lista)))))
      (begin
        (displayln (detalles (car coords) (+ (cdr coords) 1) lista))
        (escribir (list lista (car (detalles (car coords) (+ (cdr coords) 1) lista)))))))

(define (retirar cantidad)
  (define coords (buscar (est-actual)))
  (define lista (carrusel))
  (define producto (detalles (car coords) (cdr coords) lista))
  (if (< (- (cadr producto) cantidad) 0)
      (begin
        (displayln "Se intentó retirar más de la cantidad existente.")
        (displayln (list (reemplazar-elem (list (car producto) 0 (caddr producto)) (car coords) (cdr coords) lista '()) (car producto))))
      (void)))

(define (realizar-transacciones arch)
  (load arch))

(realizar-transacciones "transacciones.txt")

(display "Valor total del inventario: ") (displayln valor-total)
(display "Productos con poco o nulo inventario: ") (displayln productos-bajos)