# Phase 2 — raport zbiorczy: co zrobiliśmy, jak teraz liczymy i co dalej

*2026-11-01 14:29 — Claude Opus 5.5*

**Status raportu:** do przeczytania

## Co masz zrobić

Przeczytaj. Ten raport zastępuje 12 wcześniejszych raportów Phase 2, które zamknąłem na Twoją prośbę (@T018). Nic tu nie wymaga decyzji. Jedyna otwarta sprawa to **sygnał do puszczenia kolejki warstw** (@phase-2:K47 = B): wystarczy napisać w czacie „puść kolejkę warstw”. Uwagi i pytania pisz pod raportem.

W skrócie:
- **Mapa ważności działa:**
  - wybór neuronów do usunięcia według mapy daje mniejszą szkodę niż wybór po średniej aktywacji, także po treningu;
  - mapa trafnie porządkuje warstwy, poza końcowymi.
- **Jedna warstwa zmniejszona o 40%** (0,6% parametrów modelu) prawie nie zmienia tego, jak model programuje:
  - przy 1 losowanej próbie w. 13 rozwiązuje 133 zadania, a oryginał 134 (z 542);
  - w. 26 przy jednej odpowiedzi bez losowania rozwiązuje 205 zadań wobec 200.
- **Metoda zmieniła się od planu.** Szczegóły są w sekcji 2. Najważniejsze zmiany:
  - celem jest programowanie w Pythonie;
  - mapę liczymy na 75% Pythona i 25% tekstu;
  - mamy jeden przepis naprawy warstwy;
  - nowa miara: zgodność odpowiedzi z oryginałem, liczona na zadaniach spoza testów.
- **Dalej:**
  - kolejka 10 mało ważnych warstw (czeka na Twój sygnał);
  - potem pytania o zmniejszanie wielu warstw naraz.

---

## 1. Co zrobiliśmy (chronologicznie)

| Kiedy | Co | Najważniejszy wynik | Raport (zamknięty) |
|---|---|---|---|
| 29.10 | Twój pomysł zapisany wzorami i oceniony; plan etapów 1–4 | plan zatwierdzony 29.10 21:36 | `raport-1-opis-matematyczny.md`, `raport-2-opinia.md`, `plan-phase-2.md` |
| noc 29/30.10 | **Etap 1:** pilot na warstwach 2, 13, 25 | pomiar dokładny musi iść w float32 (szum bf16 jest 100× większy niż skutek jednego neuronu); przybliżenie gradientem zgadza się z pomiarem dokładnym w 0,96–0,98 i jest ~1000× tańsze | `etap-1-pilot.md` |
| noc 29/30.10 | **Etap 2:** mapa ważności wszystkich 86 016 neuronów | mapa z przybliżenia na 131 tys. tokenów; neurony ważne dla kodu i dla tekstu to prawie inne neurony | `etap-2-mapa.md` |
| noc 29/30.10 | **Etap 3:** rodzaje neuronów | prawie nie ma martwych (5) ani zbędnych (0,5%); ważność skupiona w ostatniej warstwie 27 i w warstwie 2 | `etap-3-rodzaje-neuronow.md` |
| noc 29/30.10 | **Etap 4:** zmniejszenie warstwy 13 | −40% neuronów → perpleksja +0,5%; mapa lepsza od średniej aktywacji o 14–37% KL | `etap-4-jedna-warstwa.md` |
| 30.10 | Jak oceniać kod | EvalPlus (HumanEval+, MBPP+) w kontenerze bez sieci, jakość i sprawność kodu | `raport-3-ocena-kodu.md` |
| 30.10 | **Etap 4b:** przejście na kod (Python) | mapa kodu: KL na Pythonie −37%; warstwy 13 i 14 znoszą zmniejszenie najlepiej, 2 i 26 ~3,5× gorzej | `etap-4b-kod.md` |
| 30.10 | **Etap 4c:** punkt startu, cel treningu, waga kodu, testy kodu | oryginał 36,9 pkt EvalPlus (raport Qwen3: 36,23); start z mapy najlepszy; scalanie neuronów gorsze od usuwania | `etap-4c-k31-k38.md` |
| 30.10 | Porównanie z oryginałem w liczbach zadań | oryginał 200 zadań, w. 26 −40% 205, w. 13 −40% 184–191 | `porownanie-z-oryginalem.md` |
| 1.11 | **K43:** zgodność tokenu z oryginałem | zgodność na odpowiedziach oryginału na zadania programistyczne ustawia modele w tej samej kolejności co testy kodu | `k43-zgodnosc-tokenu.md` |
| 1.11 | **K44:** pass@1–3 z 10 losowań | w. 13 −40% ≈ oryginał (różnice w granicach przypadku) | `k44-pass-at-k.md` |

Wszystkie raporty zostają w folderze `AGENTS/phases/phase-2/`. Są zamknięte, ale można do nich zajrzeć po szczegóły.

## 2. Metoda: jak było w planie, a jak liczymy teraz

| Element | Plan (29.10) | Teraz | Skąd zmiana |
|---|---|---|---|
| cel zmniejszania | zachować sens modelu | **zachować programowanie** | @phase-2:K25 |
| język | tekst + kod w 7 językach | **tylko Python** | K28 |
| dane do mapy i naprawy | 75% tekst C4 + 25% kod | **75% Python + 25% tekst C4** | K18, K26 |
| ważność neuronu | dokładna zmiana KL po zaburzeniu | **przybliżenie gradientem (Fisher)**; pomiar dokładny tylko do kontroli | K16, K17 |
| mapa | jedna | **osobno Python i tekst, połączone 75/25** | K26, K38, K41 |
| które warstwy | najmniej wrażliwa (13) | **środkowe warstwy z najmniejszym kosztem według mapy** | K21, K44, K45 |
| start zmniejszonej warstwy | zachowane neurony + najmniejsze kwadraty | bez zmian; scalanie neuronów porzucone | K7, K31, K42 |
| cel treningu | wyjście warstwy następnej | bez zmian (cel na wyjściu modelu sprawdzony i odrzucony) | K5, K37, K40 |
| długość treningu | 4 epoki | **6 epok, krok $5 \cdot 10^{-5}$** | K23, @T017 |
| miary | KL + perpleksja | **KL na Pythonie, zgodność odpowiedzi na zadaniach spoza testów, testy EvalPlus „na kamienie milowe”, wyniki w liczbach zadań, pass@1–3** | K27, K32, K43, K44, K46, @T015 |

### 2.1. Obecny przepis krok po kroku (wzory)

**Krok 1. Ważność każdego neuronu** (mapa Fishera). Dla neuronu $j$ w warstwie $l$:

$$
F_{l,j} = \frac{1}{2\,S\,T} \sum_{\text{sekwencje}} \sum_{s=1}^{S} \Big( \sum_{t} g^{(s)}_{t,l,j} \, a_{t,l,j} \Big)^2
$$

Słownie:
- $a_{t,l,j}$ to aktywacja neuronu przy tokenie $t$;
- $g$ mówi, jak mocno zmieniłoby się wyjście modelu, gdyby ta aktywacja trochę się zmieniła (liczone wsteczną propagacją od wyjścia przez wszystkie dalsze warstwy);
- $S$ to liczba losowań tokenu na sekwencję, $T$ to liczba tokenów.

Wynik to **szacowany przyrost KL na wyjściu modelu po usunięciu samego tego neuronu**.

**Krok 2. Mapa 75/25.** Mapy liczymy osobno dla Pythona ($F^{\text{kod}}$) i tekstu ($F^{\text{tekst}}$) i łączymy w każdej warstwie:

$$
\hat F_{l,j} = \left( 0{,}75 \, \frac{F^{\text{kod}}_{l,j}}{\sum_i F^{\text{kod}}_{l,i}} + 0{,}25 \, \frac{F^{\text{tekst}}_{l,j}}{\sum_i F^{\text{tekst}}_{l,i}} \right) \sum_i F^{\text{kod}}_{l,i}
$$

Słownie: w każdej warstwie obie mapy skalujemy do sumy 1, łączymy w proporcji 3 : 1, a potem mnożymy z powrotem przez sumę mapy kodu. Dzięki temu warstwy da się ze sobą porównywać.

**Krok 3. Wybór warstwy i neuronów.** Koszt usunięcia ułamka $r$ neuronów warstwy $l$ to suma $\hat F$ jej $r \cdot 3072$ najmniej ważnych neuronów (614 przy 20%, 1229 przy 40%). Usuwamy właśnie te neurony, a warstwy wybieramy spośród najtańszych.

**Krok 4. Najmniejsze kwadraty.** Pozostałym neuronom liczymy od nowa wagi wyjściowe $W_{\text{down}}$. Niech $A$ to aktywacje zachowanych neuronów, a $Y$ to wyjście oryginalnego MLP na ok. 1 mln tokenów:

$$
\widetilde W_{\text{down}} = Y A^\top \big( A A^\top + \lambda I \big)^{-1}
$$

Słownie: pozostałe neurony dostają takie kierunki wyjścia, które najlepiej zastępują wkład usuniętych. To kilka sekund rachunku. Daje więcej niż cały późniejszy trening: KL spada o ~1/3.

**Krok 5. Trening „za następną warstwą”.** Uczymy tylko zmniejszony MLP. Wejściem jest stan modelu przed warstwą $l$, a celem wyjście oryginalnej warstwy $l+1$ (warstwa $l+1$ jest zamrożona):

$$
\mathcal{L} = \frac{\big\lVert \widetilde{B}_{l+1}\big(\widetilde{B}_{l}(h^{(l-1)})\big) - h^{(l+1)} \big\rVert^2}{\operatorname{Var}\big(h^{(l+1)}\big)}
$$

Słownie: $\widetilde B_l$ to warstwa $l$ ze zmniejszonym MLP, $\widetilde B_{l+1}$ to niezmieniona warstwa następna, a błąd jest dzielony przez zmienność celu, żeby był porównywalny między warstwami. Nie karzemy błędów, które warstwa następna i tak „wygasza”. 6 epok, krok $5 \cdot 10^{-5}$, ~2,3 min na warstwę.

### 2.2. Jak oceniamy

**1. KL na odłożonym Pythonie i tekście.** średnio o ile rozkład następnego tokenu zmniejszonego modelu różni się od oryginału. Szybka, ale **myli się między warstwami**: w. 26 ma 3× większą KL niż w. 13, a w testach kodu wypada lepiej.

**2. Zgodność odpowiedzi** (K43, K46). bierzemy odpowiedź oryginału na zadanie programistyczne i sprawdzamy, w ilu miejscach zmniejszony model wybrałby ten sam najbardziej prawdopodobny token:

$$
Z = \frac{1}{N} \sum_{t=1}^{N} \mathbf{1}\Big[ \arg\max_v \tilde p_t(v) = \arg\max_v p_t(v) \Big]
$$

Słownie: odsetek miejsc w odpowiedziach oryginału, w których zmniejszony model wybrałby ten sam token. Liczymy ją **na 510 zadaniach MBPP, których nie ma w testach** (K46 = B), więc wybierając warianty, nie patrzymy na zadania testowe.

**3. Testy EvalPlus** (HumanEval+ 164 i MBPP+ 378 zadań, kod uruchamiany w kontenerze bez sieci) tylko dla ważnych modeli. Wyniki podaję w **liczbach zadań**, a od K44 także w 1, 2 i 3 próbach:

$$
\text{pass@}k = 1 - \binom{n-c}{k} \Big/ \binom{n}{k}
$$

Słownie: szansa, że co najmniej jedna z $k$ odpowiedzi wylosowanych spośród $n$ (z czego $c$ poprawnych) rozwiązuje zadanie. Suma po zadaniach to oczekiwana liczba rozwiązanych zadań.

## 3. Najważniejsze wyniki

### 3.1. Neurony i mapa

![Rodzaje neuronów](AGENTS/phases/phase-2/figures/etap3-rodzaje-neuronow.png)

Co widać: w każdej warstwie prawie wszystkie neurony coś robią. Martwych jest 5 z 86 016, zbędnych 422 (0,5%). Neurony krytyczne są skupione w ostatniej warstwie 27 (53 z 75) i w warstwie 2. Nie ma więc dużej puli „darmowych” neuronów: zmniejszanie zawsze wymienia trochę jakości na parametry, a pytanie brzmi, gdzie ta wymiana jest najtańsza.

![Koszt warstw](AGENTS/phases/phase-2/figures/kod-mapa-koszt-warstw.png)

Co widać:
- lewy wykres: według mapy najtańsze do zmniejszenia są warstwy 20–25, a najdroższe początkowe (0 i 2–6);
- prawy wykres: dla warstw 2, 13 i 14 mapa trafia z dokładnością do ~30%. Warstwa 26 wychodzi 2× droższa, niż przewiduje mapa, bo w końcowych warstwach usunięte neurony działają razem.

### 3.2. Zmniejszanie jednej warstwy

![Cztery warstwy](AGENTS/phases/phase-2/figures/kod-etap4-warstwy.png)

Co widać: po pełnym przepisie (start z mapy, najmniejsze kwadraty, trening) warstwy 13 i 14 mają przy −40% ~3,5× mniejszą KL niż warstwy 2 i 26 na Pythonie i ~3× mniejszą na tekście.

Inne wnioski z etapów 4–4c:
- **wybór neuronów ma znaczenie także po długim treningu:** start losowy daje o 64% większą KL niż start z mapy;
- **scalanie podobnych neuronów** zamiast usuwania jest gorsze. Neurony są prawie niezależne (podobieństwo aktywacji ~0,13), więc nie ma czego scalać. To wynik negatywny do pracy (K42);
- **trening z celem na wyjściu modelu** pomógł tylko w w. 26 (−17% KL), był ~18× wolniejszy i nie pomógł w środku modelu. Dlatego wszędzie trenujemy celem za warstwą (K40).

### 3.3. Programowanie: liczby zadań

![Liczba zadań](AGENTS/phases/phase-2/figures/porownanie-liczba-zadan.png)

Co widać (jedna odpowiedź bez losowania): oryginał rozwiązuje 49 zadań HumanEval i 195 MBPP. W testach „+” jest to 38 i 162, razem 200 z 542. Warstwa 26 −40% ma 205, a warianty warstwy 13 −40% od 184 do 191.

![pass@1–3](AGENTS/phases/phase-2/figures/kod-k44-pass-at-k.png)

Co widać (10 losowanych odpowiedzi na zadanie, K44): w. 13 −40% rozwiązuje w 1 próbie 133 zadania wobec 134 u oryginału, a w 3 próbach 217 wobec 226. Przedziały 95% przecinają zero, więc różnice mogą być przypadkowe. Strata 14 zadań przy jednej odpowiedzi bez losowania była więc w dużej części przypadkiem. Samo przejście z float32 na bf16 zmienia ~27% takich odpowiedzi.

### 3.4. Którą miarą wybierać warianty

![Zgodność tokenu](AGENTS/phases/phase-2/figures/kod-k43-zgodnosc-tokenu.png)

Co widać: zgodność na zwykłym kodzie (lewy wykres) nie odróżnia warstwy 26 od 13. Zgodność na odpowiedziach oryginału na zadania programistyczne (prawy wykres) ustawia 4 modele dokładnie w kolejności testów kodu: w. 26 (99,44%, 205 zadań) jest prawie przy szumie bf16 (99,59%), warianty w. 13 są dalej (98,27–98,66%, 184–191 zadań). To tylko 4 modele, więc kolejka warstw sprawdzi to na 4 nowych.

## 4. Co jeszcze nie jest zrobione i co dalej

### 4.1. Gotowe, czeka na Twój sygnał (@phase-2:K47 = B)

Kolejka `results/phase2/code/queue-layers.json`, ~2 h 50 min GPU:
1. **10 warstw przepisem z sekcji 2.1:** 24, 25, 20, 23, 21, 22, 17, 18, 15 (najtańsze według mapy) i kontrolnie 10, każda przy −20% i −40%;
2. **zestaw zgodności spoza testów** (K46 = B): odpowiedzi oryginału na 510 zadań MBPP i zgodność dla wszystkich wariantów;
3. **testy kodu** dla warstw 24, 20, 17 i 10 przy −40%. Te warstwy wybrałem z góry, żeby uczciwie sprawdzić, czy zgodność przewiduje testy.

Po kolejce napiszę raport z odpowiedziami na trzy pytania:
- czy mapa trafnie przewiduje koszt w końcowych warstwach 17–25, czy myli się jak w w. 26;
- czy zgodność na zadaniach spoza testów przewiduje wyniki testów nowych warstw;
- które warstwy najlepiej znoszą zmniejszenie, w liczbach zadań.

### 4.2. Pytania, które zadam później (nie zakładam odpowiedzi)

- **Zmniejszanie wielu warstw naraz.** Każdą warstwę uczymy na wejściach z oryginalnego modelu, a w modelu z wieloma zmniejszonymi warstwami dostanie wejścia już zmienione. Typowa odpowiedź to zmniejszanie po kolei: dane do warstwy $l$ zbiera się z modelu, w którym wcześniejsze warstwy są już zmniejszone (@T017). Zapytam, gdy będą wyniki kolejki.
- **Ile zmniejszać łącznie i w których warstwach:** cel w parametrach albo w dopuszczalnej stracie zadań.
- **Dotrenowanie całego modelu po zmniejszeniu** (w pierwotnym planie część C4, @phase-2:K8 = D: najpierw tylko zmniejszone warstwy, potem LoRA).
- **Koniec Phase 2.** Kryteria końca z planu (mapa, wykresy rodzajów, krzywa dla jednej warstwy, raporty etapów 1–4) są spełnione. Zmniejszanie wielu warstw i dotrenowanie całego modelu plan przypisał Phase 3 (@phase-2:K10). Czy i kiedy zamknąć Phase 2, decydujesz Ty. Zapytam o to razem z pytaniem o wiele warstw.

### 4.3. Odłożone

- klasyfikator do oceny kodu: „future research” (@phase-2:K33);
- model do kodu ~0,5B jako odniesienie (@phase-2:K29 = B): jeszcze nie liczony;
- sprawność kodu w benchmarku Mercury (@phase-2:K35): później.

## 5. Pliki

- kod: pakiet `src/qwen_compression/` + skrypty `scripts/phase2_*.py` (każdy raport etapu wymienia swoje);
- wyniki: `results/phase2/` (mapa: `results/phase2/code/`, testy kodu: `results/phase2/code-eval/`, zestaw spoza testów: `results/phase2/code-agreement/`);
- decyzje: `AGENTS/memory/decyzje.md` (@phase-2:K1–K47).

*2026-11-01 14:29 — Claude Opus 5.5*

## Dyskusja

---
---
---

Czy liczba ważnych neuronów (w sumie ważności usuwanych neuronów - tj. na wykresie) uwzględnia odległość warstwy do końca modelu? Dziwi mnie to że wydaje się że im bliżej końca modelu tym mniej ważne są warstwy.

*2026-11-01 14:49 — Autor*

---
---
---

## Co masz zrobić

Nic do decyzji, to odpowiedź na pytanie. Jeśli coś jest niejasne, dopisz pod spodem.

### Czy koszt warstwy uwzględnia odległość do końca modelu

**Tak.** Ważność neuronu {l,j}$ (wzór w sekcji 2.1) jest liczona **na wyjściu modelu**: mówi, jak zmieniłoby się to, co model przewiduje, gdyby neuron zniknął. Zmiana w warstwie 2 przechodzi do wyjścia przez warstwy 3–27, a zmiana w warstwie 26 tylko przez warstwę 27, i obie drogi są w liczbie $ już uwzględnione. Niczego nie mierzymy lokalnie.

### Dlaczego końcowe warstwy wychodzą „tanie”

**Końcowe warstwy nie są mniej ważne.** Tanie jest tylko ich najsłabsze 40% neuronów. Złożyły się na to dwa efekty.

![Skupienie ważności](AGENTS/phases/phase-2/figures/kod-mapa-skupienie-waznosci.png)

Co widać:
- **wykres 1, łączna ważność warstwy** (suma po wszystkich 3072 neuronach, mapa Pythona). Przez środek modelu (8–15) maleje, a pod koniec rośnie. Warstwy 19–23 mają jej więcej niż środek. Warstwa 26 ma jej 3× więcej niż warstwa 13, a ostatnia warstwa 27 aż 16× więcej. Ważność wcale więc nie maleje w stronę końca;
- **wykres 2, ile ważności niesie najsłabsze 40% neuronów.** W środku modelu (8–14) jest to 16–19% ważności warstwy, a w warstwach 20–26 tylko 5–11%, w ostatniej 1%. Pod koniec modelu ważność skupia się w kilku neuronach. Na przykład w warstwie 26 najważniejsze 5% neuronów niesie 56% ważności, a w warstwie 13 tylko 23%. Zostaje dużo neuronów, które prawie nic nie robią, i właśnie je usuwamy. Pasuje to do etapu 3, w którym neuronów „zbędnych” i „masywnych” jest najwięcej w warstwach 15–27;
- **wykres 3, koszt usunięcia 40% osobno dla Pythona i dla tekstu.** Na tekście koszt końcowych warstw jest podobny jak w środku, a w warstwach 24–26 rośnie aż do poziomu początku modelu. **Tanie są one tylko na Pythonie:** w warstwach 20–26 koszt to ~0,003, czyli o połowę mniej niż w środku (~0,006). Z etapu 3: w końcowych warstwach od 1/5 do 1/3 neuronów jest wyraźnie „tekstowych” albo „kodowych”. Neurony potrzebne do tekstu przy kodzie prawie nic nie robią. Mapa 75/25 porównuje warstwy w skali Pythona (sekcja 2.1, krok 2), więc te neurony wychodzą tanie.

**Zastrzeżenie:** mapa sumuje skutki pojedynczych neuronów. W warstwie 26 prawdziwe wycięcie kosztowało 1,7–1,9× więcej, niż przewidziała mapa (neurony działają razem). Możliwe, że podobnie jest w warstwach 20–25. **Kolejka warstw to właśnie sprawdzi** (@T019): dla każdej z warstw 15–25 porównam przewidywanie mapy ze zmierzoną KL i z testami kodu. Jeśli końcowe warstwy okażą się droższe, niż mówi mapa, poprawię wybór warstw.

Skrypt wykresu: `scripts/phase2_code_map_concentration.py`, liczby: `results/phase2/code/map-concentration.json`.

*2026-11-01 14:51 — Claude Opus 5.5*

---
---
---
