(def num_carruseles 30)
(def filas 10)
(def columnas 5)
(def medicamentos '("Paracetamol" "Ibuprofeno" "Aspirina" "Naproxeno" "Diazepam" "Ketorolaco" "Lorazepam" "Alprazolam" "Clonazepam" "Sertralina" "Fluoxetina" "Paroxetina" "Citalopram" "Amitriptilina" "Venlafaxina" "Escitalopram" "Duloxetina" "Pregabalina" "Gabapentina" "Carbamazepina" "Valproato" "Lamotrigina" "Levotiroxina" "Metformina" "Insulina glargina" "Insulina lispro" "Insulina aspart" "Insulina detemir" "Gliclazida" "Glimepirida" "Rosuvastatina" "Atorvastatina" "Simvastatina" "Ezetimiba" "Fenofibrato" "Omeprazol" "Lansoprazol" "Pantoprazol" "Esomeprazol" "Ranitidina" "Famotidina" "Metoclopramida" "Ondansetron" "Domperidona" "Cetirizina" "Loratadina" "Fexofenadina" "Clorfenamina" "Desloratadina" "Pseudoefedrina" "Oximetazolina" "Salbutamol" "Albuterol" "Budesonida" "Fluticasona" "Montelukast" "Cromoglicato de sodio" "Ketotifeno" "Amoxicilina" "Azitromicina" "Cefalexina" "Ceftriaxona" "Ciprofloxacino" "Doxiciclina" "Metronidazol" "Trimetoprima" "Aciclovir" "Valaciclovir" "Oseltamivir" "Rituximab" "Infliximab" "Adalimumab" "Etanercept" "Interferon beta-1a" "Interferon beta-1b" "Natalizumab" "Alemtuzumab" "Bevacizumab" "Trastuzumab" "Cisplatino" "Carboplatino" "Paclitaxel" "Docetaxel" "Irinotecan" "5-Fluorouracilo" "Doxorrubicina" "Ciclofosfamida" "Vincristina" "Vinblastina" "Bleomicina" "Procarbazina" "Dacarbazina" "Tamoxifeno" "Letrozol" "Anastrozol" "Fulvestrant" "Leuprorelina" "Goserelina" "Degarelix" "Abiraterona"))



(defn gen-prod [lst f]
  (if (empty? lst) (partition columnas (partition 3 f))
      (recur (rest lst) (concat f (list (first lst) (rand-int 301) (double (+ (rand-int 20) (/ (rand-int 11) 10))))))))
(defn gen-carr [n]
  (let [lst-meds (take (* filas columnas) (shuffle medicamentos))
        carr (gen-prod lst-meds '())]
    (spit (str "carrusel" n ".txt") (list carr (first (first (first carr)))))))

(doall (map #(gen-carr %) (range 1 (inc num_carruseles))))

(defn transacciones []
  (list (list 'a) (list 'b) (list 'c) (list 'd) (list 'agregar (rand-int 51)) (list 'retirar (rand-int 51)) (list 'agregar (rand-int 51) (nth medicamentos (rand-int (count medicamentos)))) (list 'retirar (rand-int 51) (nth medicamentos (rand-int (dec (count medicamentos)))))))

(defn gen-trans [n]
  (let [transaccion (nth (transacciones) (rand-int (dec (count (transacciones)))))]
    transaccion))

(defn arch-trans [n]
  (spit (str "transacciones" n ".txt") (rest (doall (map #(gen-trans %) (range 1 (rand-int 30)))))))

(doall (map #(arch-trans %) (range 1 (inc num_carruseles))))