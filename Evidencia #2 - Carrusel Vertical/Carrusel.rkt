#lang racket

(define carrusel (read (open-input-file "carrusel.txt")))
(define filas (length carrusel))
(define columnas (length (car carrusel)))

carrusel
filas
columnas

(define (coordenadas lst)
  (apply append (map (lambda (n) ()) lst)))

carrusel
(coordenadas carrusel)