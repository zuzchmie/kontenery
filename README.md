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
   * z analizy parametrów dla main_generational.py:

      Najwyższą wartość funkcji fitness (716.33) uzyskano przy:
      
      max_generations: 100
      
      pop_size: 50
      
      mutation_std: 0.05
      
      crossover_p_swap: 0.5
      
      Niższa siła mutacji (0.05) generalnie prowadziła do lepszych wyników niż wyższa (0.1), co sugeruje, że przy tym problemie mniejsza wariancja zmian sprzyja
     stabilniejszej ewolucji.
      Wyższe prawdopodobieństwo wymiany genów (0.5 vs 0.2) często korelowało z wyższym fitness, szczególnie w połączeniu z większą liczbą pokoleń, co potwierdza
     rolę rekombinacji w eksploracji przestrzeni rozwiązań.

  * z analizy parametrów dla main_solve.py:

    W ramach eksperymentu zbadane zostały wartości fitness oraz layouty na wyjściu dla kształtów Wedge, Pentagon oraz Quadrilateral, liczbie populacji równej 100
    lub 300, liczbie generacji równej 100 lub 200, parametru spacing (odległość między modułami) o wartościach 0.1/0.3 oraz współczynniku mutacji równym 0.1
    (wartość niska) oraz 0.3 (mutacje występują częściej).
    
    Zgodnie z wykresem (boxplot.png) najwyższe wartości dla funkcji fitness zostały otrzymane dla kształtu (Area_name) sześciokąta (Wedge) i liczby generacji
    równej 200. Kolejna była wartość dla pięciokąta i 200 generacji, a następnie dla czworokąta i (wciąż) 200 generacji.
    
    Na wykresie można zauważyć dodatnią korelację między fitnessem a liczbą generacji, natomiast zmiana współczynnika fitness między próbami dla 100 i 200
    generacji nie była drastyczna - stąd można się spodziewać, że dalszy wzrost liczby generacji mógłby nie dawać dużo lepszych efektów, za to znacznie
    spowalniałby czas oczekiwania na wynik.

    Jeżeli chodzi natomiast o samą szerokość pudełek na wykresie, dla kształtów Wedge i Pentagon są one dość szerokie, co
    wskazywałoby na to, że algorytm dla bardziej skomplikowanych kształtów jest mało stabilny, natomiast Quadrilateral pudełko jest dużo węższe, natomiast wraz ze
    wzrostem liczby generacji staje się szersze, tak samo zresztą jak wąsy - czyli (dla Quadrilateral!!) stabilność algorytmu spada dla większej liczby generacji,
    mimo wyższych wartości dla fitnessu.
    
    Współczynnik mutacji równy 0.3 po wizualnej analizie layoutów na wyjściu (/results/...) wydaje się sprawiać, że pomieszczenia wspólne są bardziej rozproszone
    na zadanej przestrzeni, co przekładałoby się na lepszy dostęp do nich z różnych części budynku.

     Ponadto (może to być tylko złudne wrażenie w związku z tym, że eksperyment dla każdej z kombinacji wartości parametrów został wykonany zaledwie trzykrotnie)
    dla współczynnika mutacji 0.3 szansa na umieszczenie pokoju wspólnego wydaje się większa niż w przypadku mutacji 0.1 - dla layoutów z mutacją 0.3 liczba
    pokoi wspólnych częściej jest większa niż 1, w niektórych przypadkach pojawiają się nawet 3 lub 4 pokoje wspólne na layout dla takich samych przestrzeni
    (pytanie: czy to dobrze? Myślę, że w tym przypadku odpowiedź zależy od ilości indywidualncyh modułów mieszkalncyh oraz gęstości ich ułożenia w przestrzeni, a
    także od wielkości samej przestrzeni).

    Bazując na moich obserwacjach myślę, że możnaby postawić ostrożny wniosek, że współczynnik mutacji w okolicach ~0.3
    umożliwia uzyskanie najbardziej optymalncyh rezultatów (większe wartości mogłyby wpływać na utratę dobrych cech w wyniku mutacji).

    Kolejnym parametrem, który ulegał zmianie na przestrzeni eksperymentów był >>spacing<< oznaczający odległość między modułami.

    Dla spacingu o wartości 0.1 udało się zmieścić większą liczbę modułów, natomiast końcowy layout był dużo mniej czytelny, w związku z czym nasuwa się pytanie -
    czy lepszą opcją jest zwiększenie liczby modułów kosztem czytelności i (w przypadku wdrożenia wizji w rzeczywistość) możliwym ograniczeniem dostępności
    do innych modułów z powodu za wąskich przejść, czy lepiej nieznacznie zwiększyć spacing (np. do zaproponowanej przeze mnie wartości 0.3) i ograniczyć tym samym
    liczbę modułów (z uwagi na większe odległości między modułami spadek liczby może być znaczny - widać to również porównując layouty wyjściowe).
    
