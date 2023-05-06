#lang racket

(define carrusel (read (open-input-file "carrusel.txt")))
(define filas (length carrusel))
(define columnas (length (car carrusel)))

carrusel
filas
columnas

(define (coordenadas lst f x y)
  (if (null? lst) f
      (if (<= y columnas)
          (coordenadas (cdr lst) (append f (list (list (caar lst) (cons x y)))) x (+ y 1))
          (coordenadas lst f (+ x 1) 1))))

(define diccionario (coordenadas (apply append carrusel) '() 1 1))

(define (retirar cantidad producto)
  ())