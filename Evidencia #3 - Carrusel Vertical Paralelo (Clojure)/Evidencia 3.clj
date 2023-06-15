; Evidencia #3
; Implementación de un simulador de un almacén automatizado (segunda parte)
; Diego Andrés Figueroa Peart A01660987

; Se establecen los parámetros básicos de cada carrusel.
(defn carrusel [n]
  (first (read-string (slurp (str "carrusel" n ".txt")))))

(defn est-actual [n]
  (second (read-string (slurp (str "carrusel" n ".txt")))))

(defn filas [n]
  (count (carrusel n)))

(defn columnas [n]
  (count (first (carrusel n))))

; Se guardan los cambios al carrusel.
(defn escribir [n txt]
  (spit (str "carrusel" n ".txt") txt))

; El log de las transacciones se almacenará por carrusel.
(defn log [n txt]
  (spit (str "log" n ".txt") (str txt "\n") :append true))

(defn coordenadas [lst col x y f]
  (if (empty? lst) f
      (if (<= y col)
        (recur (rest lst) col x (+ y 1) (concat f (list (list (first (first lst)) (list x y)))))
        (recur lst col (+ x 1) 1 f))))
(defn diccionario [n]
  (coordenadas (apply concat (carrusel n)) (columnas n) 1 1 '()))

; Se busca un producto a partir de su nombre, se regresan sus coordenadas.
(defn buscar [producto n]
  (let [x (filter #(= producto (first %)) (diccionario n))]
    (if (nil? x) false
        (second (first x)))))

; Se reciben las coordenadas del producto y se regresa su nombre, cantidad y precio.
(defn detalles-aux [lst y]
  (if (not (= 1 y))
    (recur (rest lst) (dec y))
    (first lst)))
(defn detalles [lst x y]
  (if (not (= 1 x))
    (recur (rest lst) (dec x) y)
    (detalles-aux (first lst) y)))

; Se cambia la cantidad del producto en el carrusel para luego sobreescribir el archivo.
(defn reemplazar-y [lst y r f]
  (cond
    (empty? lst) f
    (= y 1) (recur (rest lst) (dec y) r (concat f (list r)))
    :else (recur (rest lst) (dec y) r (concat f (list (first lst))))))
(defn reemplazar-x [lst x y r f]
  (cond
    (empty? lst) f
    (= 1 x) (recur (rest lst) (dec x) y r (concat f (list (reemplazar-y (first lst) y r '()))))
    :else (recur (rest lst) (dec x) y r (concat f (list (first lst))))))
(defn reemplazar [n x y r]
  (reemplazar-x (carrusel n) x y r '()))

(defn arriba [x1 x2 lst filas]
  (if (= x1 x2) lst
      (if (= x1 1)
        (recur filas x2 (concat lst (list 'a)) filas)
        (recur (- x1 1) x2 (concat lst (list 'a)) filas))))

(defn abajo [x1 x2 lst filas]
  (if (= x1 x2) lst
      (if (= x1 filas)
        (recur 1 x2 (concat lst (list 'b)) filas)
        (recur (+ x1 1) x2 (concat lst (list 'b)) filas))))

; Se calcula la distancia entre el producto actual y el producto al que se desea llegar, se determina la ruta más rápida.
(defn distancia-y [y1 y2 lst]
  (if (= y1 y2) lst
      (if (> y1 y2)
        (recur (- y1 1) y2 (concat lst (list 'c)))
        (recur (+ y1 1) y2 (concat lst (list 'd))))))
(defn distancia [x1 y1 x2 y2 lst filas]
  (cond
    (< x1 x2) (if (> (- x2 x1) (/ filas 2))
                (recur 0 y1 0 y2 (arriba x1 x2 lst filas) filas)
                (recur 0 y1 0 y2 (abajo x1 x2 lst filas) filas))
    (> x1 x2) (if (> (- x1 x2) (/ filas 2))
                (recur 0 y1 0 y2 (abajo x1 x2 lst filas) filas)
                (recur 0 y1 0 y2 (arriba x1 x2 lst filas) filas))
    :else (distancia-y y1 y2 lst)))

; Se regresan los productos con menos de 20 unidades.
(defn productos-bajos [n]
  (let [prods (filter #(> 20 (second %)) (apply concat (carrusel n)))]
  (log n (str "Productos con menos de 20 unidades: " (list prods)))))

(defn valor-total [n]
  (apply + (map #(* (second %) (last %)) (apply concat (carrusel n)))))

; Movimiento hacia arriba.
(defn a [n]
  (let [coords (buscar (est-actual n) n)]
    (if (zero? (dec (first coords)))
      (do
        (escribir n (list (carrusel n) (first (detalles (carrusel n) (filas n) (second coords)))))
        (log n (detalles (carrusel n) (filas n) (second coords))))
      (do
        (escribir n (list (carrusel n) (first (detalles (carrusel n) (dec (first coords)) (second coords)))))
        (log n (detalles (carrusel n) (dec (first coords)) (second coords)))))))

; Movimiento hacia abajo
(defn b [n]
  (let [coords (buscar (est-actual n) n)]
    (if (< (filas n) (inc (first coords)))
      (do
        (escribir n (list (carrusel n) (first (detalles (carrusel n) 1 (second coords)))))
        (log n (detalles (carrusel n) 1 (second coords))))
      (do
        (escribir n (list (carrusel n) (first (detalles (carrusel n) (inc (first coords)) (second coords)))))
        (log n (detalles (carrusel n) (inc (first coords)) (second coords)))))))

; Movimiento hacia la izquierda.
(defn c [n]
  (let [coords (buscar (est-actual n) n)]
    (if (zero? (dec (second coords)))
      (log n "Movimiento inválido.")
      (do
        (escribir n (list (carrusel n) (first (detalles (carrusel n) (first coords) (dec (second coords))))))
        (log n (detalles (carrusel n) (first coords) (dec (second coords))))))))

; Movimiento hacia la derecha
(defn d [n]
  (let [coords (buscar (est-actual n) n)]
    (if (< (columnas n) (inc (second coords)))
      (log n "Movimiento inválido.")
      (do
        (escribir n (list (carrusel n) (first (detalles (carrusel n) (first coords) (inc (second coords))))))
        (log n (detalles (carrusel n) (first coords) (inc (second coords))))))))

(defn agregar
  ([cantidad n] ; Se agrega la cantidad al producto que se muestra actualmente.
   (let [coords (buscar (est-actual n) n)
         prod (detalles (carrusel n) (first coords) (second coords))
         reem (list (first prod) (+ (second prod) cantidad) (last prod))]
     (escribir n (list (reemplazar n (first coords) (second coords) reem) (est-actual n)))
     (log n (str "Agregadas " cantidad " unidades de " (first prod) "."))))
  ([cantidad producto n] ; Se agrega la cantidad al producto especificado.
   (let [origen (buscar (est-actual n) n)
         destino (buscar producto n)]
     (if (not destino)
       (log n (str "Producto " producto " no encontrado."))
       (let [prod (detalles (carrusel n) (first destino) (second destino))
             reem (list (first prod) (+ (second prod) cantidad) (last prod))]
         (escribir n (list (reemplazar n (first destino) (second destino) reem) producto))
         (log n (str "Agregadas " cantidad " unidades de " (str (first prod)) "."))
         (if (not (= origen destino))
           (log n (str "Ruta: " (apply str (distancia (first origen) (second origen) (first destino) (second destino) '() (filas n)))))))))))

(defn retirar
  ([cantidad n] ; Se retira la cantidad del producto que se muestra actualmente.
   (let [coords (buscar (est-actual n) n)
         prod (detalles (carrusel n) (first coords) (second coords))
         reem (list (first prod) (- (second prod) cantidad) (last prod))]
     (if (> 0 (second reem))
       (do
         (escribir n (list (reemplazar n (first coords) (second coords) (list (first reem) 0 (last reem))) (est-actual n)))
         (log n (str "Se intentaron retirar más de las existencias de " (first prod) ".")))
       (do
         (escribir n (list (reemplazar n (first coords) (second coords) reem) (est-actual n)))
         (log n (str "Retiradas " cantidad " unidades de " (first prod) "."))))))
  ([cantidad producto n] ; Se retira la cantidad del producto especificado.
   (let [origen (buscar (est-actual n) n)
         destino (buscar producto n)]
     (if (not destino)
       (log n (str "Producto " producto " no encontrado."))
       (let [prod (detalles (carrusel n) (first destino) (second destino))
             reem (list (first prod) (- (second prod) cantidad) (last prod))]
         (if (> 0 (second reem))
           (do
             (escribir n (list (reemplazar n (first destino) (second destino) (list (first reem) 0 (last reem))) producto))
             (log n (str "Se intentaron retirar más de las existencias de " (first prod) ".")))
           (do
             (escribir n (list (reemplazar n (first destino) (second destino) reem) producto))
             (log n (str "Retiradas " cantidad " unidades de " (first prod) "."))
             (if (not (= origen destino))
               (log n (str "Ruta: " (apply str (distancia (first origen) (second origen) (first destino) (second destino) '() (filas n)))))))))))))

; Se leerán y ejecutarán las transacciones línea por línea.
(defn main-aux [n transacciones]
  (eval (concat (first transacciones) (list n)))
  (if (not (empty? (rest transacciones)))
    (recur n (rest transacciones))))
(defn main-p [n]
  (main-aux n (read-string (slurp (str "transacciones" n ".txt")))))

(def num_carruseles 30) ; El número de carruseles a procesar es configurable aquí.

(defn main []
  (pmap #(main-p %) (range 1 (inc num_carruseles)))  ; Se procesan los carruseles de forma paralela.
  (Thread/sleep 1000)
  (pmap #(productos-bajos %) (range 1 (inc num_carruseles))) ; Se añade al log los productos con menos de 20 unidades.
  (Thread/sleep 1000)
  (println "Valor total del inventario de todos los carruseles:" (apply + (map #(valor-total %) (range 1 (inc num_carruseles))))) ; Se calcula el valor total del inventario de todos los carruseles.
  (println "Top 10% de carruseles con mayor valor de inventario:" (take (/ num_carruseles 10) (reverse (sort-by second (map #(list (str "Carrusel " %) (valor-total %)) (range 1 (inc num_carruseles))))))))

(main)