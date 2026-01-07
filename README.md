# kontenery

1. Reprezentacja rozwiązania

Genotyp jest wektorem liczb zmiennoprzecinkowych z zakresu [0, 1].
Struktura chromosomu:
Gen 0: Odpowiada za globalny kąt obrotu całego układu (wartość skalowana do 0-90 stopni).
Kolejne pary genów: Każda para odpowiada za decyzję dotyczącą kolejnego potencjalnego kontenera w siatce:
Pierwszy gen z pary: Wybór typu kontenera (Residential, Kitchen, Sanitary, Common).
Drugi gen z pary: Orientacja kontenera (poziomy/pionowy).

Dekodowanie (LayoutDecoder):
Dekoder przesuwa się po obszarze (Area) z zadanym krokiem (step), próbując umieścić kontener zdefiniowany przez geny. Sprawdza przy tym dwa kluczowe warunki:

- Czy kontener mieści się całkowicie wewnątrz zdefiniowanego wielokąta.
- Czy nie nakłada się na już wstawione kontenery.

2. Operatory, parametry, metoda selekcji

W projekcie wykorzystano bibliotekę leap_ec. Zastosowano następujące operatory genetyczne:

- mutacja gaussowska (mutate_gaussian)
- krzyżowanie jednorodne (UniformCrossover)

W eksperymentach testowano różne warianty parametrów dla tych operatorów.
Jako metodę selekcji osobników do nowej populacji wybrano selekcję turniejową (tournament_selection).

3. Funkcja oceny

Wzór funkcji oceny:
10*N - 2*D_k - 3*D_s - D_c + 20*R - P

Gdzie:
N: Liczba kontenerów mieszkalnych (priorytetem jest ich maksymalizacja).
D_k, D_s, D_c: Odległość od kontenerów mieszkalnych do odpowiednio: kuchni, sanitariatów i części wspólnych
R: Współczynnik wolnej przestrzeni - algorytm jest nagradzany za pozostawienie pewnego "oddechu" przestrzennego.
P: Kara nakładana za brak kluczowych typów kontenerów (brak kuchni: -50, brak sanitariatów: -80, brak części wspólnej: -30) lub zbyt małą przestrzeń wolną.



5. **Wnioski**
   * z analizy parametrów dla main_generational.py

  Najwyższą wartość funkcji fitness (716.33) uzyskano przy:
  
  max_generations: 100
  
  pop_size: 50
  
  mutation_std: 0.05
  
  crossover_p_swap: 0.5
  
  Niższa siła mutacji (0.05) generalnie prowadziła do lepszych wyników niż wyższa (0.1), co sugeruje, że przy tym problemie mniejsza wariancja zmian sprzyja stabilniejszej ewolucji.
  Wyższe prawdopodobieństwo wymiany genów (0.5 vs 0.2) często korelowało z wyższym fitness, szczególnie w połączeniu z większą liczbą pokoleń, co potwierdza rolę rekombinacji w eksploracji przestrzeni rozwiązań.

  * z analizy parametrów dla main_solve.py
