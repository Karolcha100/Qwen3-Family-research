# Etap 4c — punkt startu, cel treningu, waga kodu i pierwsze testy kodu (K31–K38)

*2026-10-30 17:13 — Claude Opus 5.5*

**Status raportu:** zamknięty (2026-11-01 14:28, Claude Opus 5.5 na prośbę autora @T018)
## Co masz zrobić

Przeczytaj raport i odpowiedz na pytania **K40–K43** w `AGENTS/phases/phase-2/agents-issues-8.md`. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”. Uwagi do raportu możesz pisać pod nim w GUI.

W skrócie:
- **oryginalny model odtwarza raport Qwen3:** średnia EvalPlus 36,9 u nas, 36,23 w raporcie;
- **zmniejszenie warstwy 13 o 40% kosztuje ~2,5–2,9 punktu pass@1, a warstwy 26 o 40% nic** (każde to −0,6% parametrów), choć KL warstwy 26 jest 3× większa: **KL nie przewiduje pass@1 między warstwami**;
- **punkt startu ma znaczenie także po 16 epokach:** mapa kodu jest najlepsza, start losowy o 64% gorszy (KL na Pythonie); **scalanie neuronów jest gorsze niż ich zwykłe usunięcie**;
- **cel na wyjściu modelu** pomaga tam, gdzie stary cel zawodzi (warstwa 26: −17% KL), ale w warstwie 13 nie jest lepszy, a jest ~18× wolniejszy;
- **mapa 100% kod** daje na Pythonie o 11–17% mniejszą KL niż 75/25, za to na tekście o 25–35% większą.

---

## 1. Co zrobiono

Kolejka z decyzji @phase-2:K31–K38 (uruchomienie: @phase-2:K39), 14:31–16:38, i dodatkowa kolejka 16:38–17:13 (Twoja zgoda z 16:30: „możesz dodać trochę więcej obliczeń, tak abyś się uwinął do 17:30”).

Wszędzie jak w etapie 4b: dane 75% Python + 25% C4, zmniejszenie jednej warstwy (start z wybranych neuronów → najmniejsze kwadraty dla $W_{down}$ → trening), ocena całego modelu przez KL do oryginału na odłożonym Pythonie i odłożonym C4. KL to średnia na token różnica między rozkładem następnego tokenu oryginału i zmniejszonego modelu; im mniej, tym bliżej oryginału.

Testy kodu (@phase-2:K32, K34–K36): HumanEval i MBPP z rozszerzonymi testami EvalPlus (HumanEval+, MBPP+), jedna odpowiedź na zadanie, dekodowanie zachłanne (bez losowania), maks. 768 nowych tokenów. Kod napisany przez model uruchamia się tylko w kontenerze bez sieci (@phase-2:K36). pass@1 to odsetek zadań, w których ta jedna odpowiedź przechodzi wszystkie testy.

## 2. Oryginalny model: odtworzenie raportu Qwen3

| Zestaw | pass@1 |
|---|---|
| HumanEval | 29,9% |
| HumanEval+ | 23,2% |
| MBPP | 51,6% |
| MBPP+ | 42,9% |
| **średnia (jak w raporcie Qwen3)** | **36,9** (raport: 36,23) |

Różnica 0,7 punktu to mniej niż jedno zadanie w HumanEval (1 zadanie = 0,6 punktu), więc sposób zadawania pytań i oceny jest zgodny z tym, którego używa Qwen. Rozwiązania wzorcowe przechodzą testy w 99,4–100% (jedno zadanie HumanEval ma w EvalPlus zbyt ciasną tolerancję liczbową), więc kontener i testy działają.

## 3. K31: od czego zacząć, gdy trening jest długi

![K31](AGENTS/phases/phase-2/figures/kod-k31-punkty-startu.png)

Warstwa 13, zmniejszenie o 40%, 16 epok treningu (cel za następną warstwą). Każda grupa słupków to jeden punkt startu; trzy słupki to kolejne kroki: samo wycięcie, najmniejsze kwadraty, trening. Lewy wykres: KL na Pythonie, prawy: na tekście C4.

| Start | wycięcie | najmn. kwadraty | po treningu | względem mapy |
|---|---|---|---|---|
| mapa kodu 75/25 | 0,00586 | 0,00403 | **0,00306** | — |
| scalanie neuronów | 0,00938 | 0,00504 | 0,00339 | +11% |
| aktywacje (RMS) | 0,00631 | 0,00450 | 0,00344 | +12% |
| losowo | 0,0128 | 0,00733 | 0,00503 | +64% |

(KL na odłożonym Pythonie; na C4 mapa też jest najlepsza, ale różnice są mniejsze: 0,0078 dla mapy, 0,0084–0,0085 dla pozostałych trzech)

Co widać:
- **trening zmniejsza różnice między startami, ale ich nie znosi:** losowy start jest po wycięciu 2,2× gorszy od mapy, po 16 epokach nadal 1,6× gorszy. Mapa jest więc potrzebna także przy długim treningu;
- aktywacje (RMS) są niewiele gorsze od mapy (+12%), więc tanią miarę można traktować jako przybliżenie mapy;
- 16 epok zamiast 6 (ten sam start z mapy) zmniejsza KL tylko o 5% (0,00321 → 0,00306), jak w @phase-2:K23.

**Scalanie neuronów.** Pary podobnych neuronów praktycznie nie istnieją (mediana największego podobieństwa aktywacji usuwanego neuronu do zostającego: 0,13), więc scalałem według wag: 1229 usuwanych neuronów dołączyłem do ~150 grup wokół neuronów z mapy (średnia wag wejściowych, suma wag wyjściowych), potem najmniejsze kwadraty i trening. Wynik: **scalanie jest gorsze niż samo usunięcie tych neuronów** na każdym kroku (0,00938 vs 0,00586 po wycięciu, 0,00339 vs 0,00306 po treningu). Uśrednianie wag psuje neurony, które zostają, bo usuwane neurony robią co innego.

## 4. K37: cel treningu na wyjściu modelu

![K37](AGENTS/phases/phase-2/figures/kod-k37-cel-treningu.png)

Trzy przypadki (grupy słupków), w każdym trzy warianty: same najmniejsze kwadraty (przed treningiem), trening z dotychczasowym celem (zgodność za następną warstwą) i trening z celem na wyjściu modelu (KL rozkładu następnego tokenu; reszta modelu zamrożona). Oba treningi: 6 epok, krok $5 \cdot 10^{-5}$.

| Przypadek | najmn. kwadraty | cel za warstwą | cel na wyjściu | czas treningu (za warstwą / na wyjściu) |
|---|---|---|---|---|
| warstwa 13, −40% | 0,00403 | **0,00321** (−20%) | 0,00375 (−7%) | 1,4 / 24,7 min |
| warstwa 13, −20% | 0,00163 | **0,00133** (−18%) | 0,00163 (0%) | 1,4 / 25,0 min |
| warstwa 26, −40% | 0,0114 | 0,0113 (−1%) | **0,00940** (−18%) | 1,4 / 9,7 min |

(KL na odłożonym Pythonie; w nawiasach zmiana względem najmniejszych kwadratów)

Co widać:
- **w warstwie 26 cel na wyjściu działa, a stary nie:** −18% zamiast −1% (na C4: −12% zamiast −2%). Potwierdza to przypuszczenie z etapu 4b: za ostatnią warstwą sygnał „za warstwą” źle oddaje to, co widzi wyjście;
- **w warstwie 13 cel na wyjściu jest gorszy** niż stary, a przy 20% nie poprawił niczego: najlepsza była epoka 0 (stan po najmniejszych kwadratach), a błąd na walidacji rósł od pierwszej epoki. To wygląda na **za duży krok uczenia** dla tego celu: jego gradient jest bardziej „zaszumiony”, bo przechodzi przez całą resztę modelu. Sprawdzenie z mniejszym krokiem: sekcja 5;
- cel na wyjściu jest **~18× wolniejszy** w warstwie 13 (każdy krok przechodzi przez całą resztę modelu i liczy rozkład na 152 tys. tokenów słownika) i ~7× w warstwie 26 (mniej warstw za nią).

## 5. K37: mniejszy krok uczenia (dodatkowa kolejka)

Warstwa 13, zmniejszenie o 20%, cel na wyjściu, krok $1 \cdot 10^{-5}$ (5× mniejszy), 4 epoki.

| Wariant | KL Python | KL C4 | błąd walidacji po kolejnych epokach |
|---|---|---|---|
| najmniejsze kwadraty (start) | 0,00163 | 0,00436 | 0,00319 |
| cel na wyjściu, krok $5 \cdot 10^{-5}$ | 0,00163 (0%) | 0,00436 (0%) | 0,00321 / 0,00334 / 0,00335 / 0,00355 / 0,00325 / 0,00325 (gorzej niż start) |
| cel na wyjściu, krok $1 \cdot 10^{-5}$ | 0,00152 (−7%) | 0,00382 (−12%) | 0,00305 / 0,00300 / 0,00300 / 0,00295 |
| cel za warstwą, krok $5 \cdot 10^{-5}$, 6 epok | **0,00133** (−18%) | **0,00340** (−22%) | — |

(błąd walidacji to KL na wyjściu modelu na odłożonej porcji danych treningowych)

Co widać: z mniejszym krokiem trening **stabilnie się poprawia** w każdej epoce, więc przyczyną porażki przy 20% był za duży krok. Mimo to w warstwie 13 cel na wyjściu (−7%) jest nadal **słabszy od starego celu** (−18%) i ~12× wolniejszy (16,4 min na 4 epoki wobec 1,4 min na 6). W środku modelu stary cel jest więc lepszym wyborem; cel na wyjściu ma sens dla ostatnich warstw (pytanie K40).

## 6. K38: mapa 100% kod

![K38](AGENTS/phases/phase-2/figures/kod-k38-waga-kodu.png)

Warstwa 13, 6 epok. Trzy mapy startowe: tylko kod, 75% kod / 25% tekst (obecna), tylko tekst (stara).

| Zmniejszenie | Mapa | KL Python | KL C4 |
|---|---|---|---|
| 20% | 100% kod | **0,00111** (−17%) | 0,00458 (+35%) |
| 20% | 75/25 | 0,00133 | 0,00340 |
| 20% | tekst | 0,00215 (+61%) | **0,00255** (−25%) |
| 40% | 100% kod | **0,00284** (−11%) | 0,0101 (+25%) |
| 40% | 75/25 | 0,00321 | 0,00813 |
| 40% | tekst | 0,00504 (+57%) | **0,00643** (−21%) |

(procenty względem mapy 75/25)

Co widać: waga kodu w mapie działa jak suwak. Przejście 75/25 → 100% kod daje na Pythonie mniej (11–17%) niż traci na tekście (25–35%); przejście 75/25 → tekst traci na Pythonie dużo więcej (57–61%), niż zyskuje na tekście (21–25%). 75/25 jest więc rozsądnym środkiem; wybór zależy od tego, jak bardzo zależy nam na tekście (pytanie K41).

## 7. Testy kodu: czy KL przekłada się na pass@1

![Testy kodu](AGENTS/phases/phase-2/figures/kod-testy-pass1.png)

Cztery grupy słupków to cztery zestawy testów; w każdej grupie kolejne modele: oryginał i cztery modele, w których jedna warstwa jest zmniejszona o 40% (każdy to −3,8 mln parametrów, czyli −0,6% modelu).

| Model | KL Python | HumanEval | HumanEval+ | MBPP | MBPP+ | średnia |
|---|---|---|---|---|---|---|
| oryginał | 0 | 29,9 | 23,2 | 51,6 | 42,9 | **36,9** |
| w. 13, cel za warstwą (16 epok) | 0,00306 | 26,8 | 20,7 | 49,2 | 40,2 | 34,2 |
| w. 13, cel na wyjściu | 0,00375 | 27,4 | 20,7 | 48,1 | 39,7 | 34,0 |
| w. 13, mapa 100% kod | 0,00284 | 25,6 | 19,5 | 50,3 | 42,1 | 34,4 |
| w. 26, cel na wyjściu | 0,00940 | 30,5 | 24,4 | 51,9 | 43,7 | **37,6** |

(pass@1 w %; średnia jak w raporcie Qwen3)

Porównanie parami z oryginałem (zadania rozwiązane z testami „+”: ile model zyskał, ile stracił; p to dokładny test McNemara, czyli prawdopodobieństwo takiej lub większej przewagi strat nad zyskami, gdyby zmiana nic nie psuła):

| Model | HumanEval+: zysk / strata (p) | MBPP+: zysk / strata (p) |
|---|---|---|
| w. 13, cel za warstwą | 6 / 10 (0,45) | 5 / 15 (**0,04**) |
| w. 13, cel na wyjściu | 5 / 9 (0,42) | 4 / 16 (**0,01**) |
| w. 13, mapa 100% kod | 5 / 11 (0,21) | 11 / 14 (0,69) |
| w. 26, cel na wyjściu | 4 / 2 (0,69) | 6 / 3 (0,51) |

Co widać:
- **zmniejszenie warstwy 13 o 40% kosztuje ~2,5–2,9 punktu** średniej; na MBPP+ strata jest statystycznie wyraźna (p 0,01–0,04) dla obu celów treningu;
- **trzy warianty warstwy 13 są nie do odróżnienia** (34,0–34,4): różnice KL między nimi (0,0028–0,0038) nie przekładają się na mierzalną różnicę pass@1;
- **niespodzianka: warstwa 26 nie traci nic** (37,6 wobec 36,9; zyski i straty w szumie), choć jej KL na Pythonie jest 3× większa niż w warstwie 13. **KL nie przewiduje więc pass@1 między warstwami.** Moje przypuszczenie (niesprawdzone): przy dekodowaniu zachłannym liczy się tylko, czy najbardziej prawdopodobny token się nie zmienia; zmiany w końcowej warstwie mogą głównie „rozmywać” rozkład (co KL mocno karze), nie zmieniając najczęściej wybranego tokenu. Da się to sprawdzić tanio, licząc odsetek tokenów, w których zmniejszony model wybiera ten sam token co oryginał (pytanie K43);
- nawet przy braku zmiany średniej model rozwiązuje inaczej ~5–15% zadań (zyski i straty), więc pojedyncze różnice ~1–2 punktów to szum;
- **sprawność:** parametry 596,0 → 592,3 mln (−0,6%), szczyt pamięci 3,38 → 3,37 GB; szybkość generowania waha się 101–141 tokenów/s bez związku z modelem (to szum pomiaru przy małej zmianie, a nie efekt zmniejszenia);
- **jakość kodu (analiza statyczna):** bez zmian; średnio 0,04–0,09 uwag ruff i 0,01–0,04 błędów pyright na rozwiązanie, długość rozwiązań 19,6–21,6 (HumanEval) i 6,8–7,5 (MBPP) niepustych linii we wszystkich modelach.

## 8. Czasy: szacunek a rzeczywistość

| Krok | szacunek | faktycznie |
|---|---|---|
| generowanie HumanEval / MBPP (jeden model) | 4 / 6 min | 2,3 / 3,5–3,8 min |
| testy HumanEval / MBPP w kontenerze | 1,5 / 1,5 min | 0,5 / 0,8–1,2 min |
| K38 (mapa 100% kod, 2 zmniejszenia, 6 epok) | 10 min | 8,5 min |
| K31 (4 starty, 16 epok) | 28 min | 26,7 min |
| K37 warstwa 13 (2 zmniejszenia, cel na wyjściu) | 76 min | 56 min |
| K37 warstwa 26 | 14 min | 13,3 min |
| **cała kolejka K31–K38** | **167 min** | **~127 min** |

Szacunki dla treningów były trafne (±10%), poza celem na wyjściu w warstwie 13 (zawyżony o ~35%); testy kodu są ~1,6× szybsze, niż zakładałem. Nowe szacunki wpisałem do procedur (sekcja 10).

## 9. Pliki

- wyniki: `results/phase2/code/k31/`, `results/phase2/code/k37/`, `results/phase2/code/k37-lr1e-5/`, wiersze `code-only` w `results/phase2/code/stage4/layer-13/`; zbiorczo `results/phase2/code/k31-k38-summary.json`;
- testy kodu: `results/phase2/code-eval/<model>/` (rozwiązania, wyniki testów, `*-summary.json` z pass@1 i analizą statyczną, `*-efficiency.json`);
- zmniejszone warstwy: `~/qwen3-checkpoints/phase2-code/mlps/`;
- kod: `scripts/phase2_code_generate.py`, `scripts/phase2_code_evaluate.py`, `scripts/phase2_code_k31_k38_analysis.py`, `src/qwen_compression/training.py`, kontener `sandbox/`.

*2026-10-30 17:13 — Claude Opus 5.5*

## Dyskusja

---
---
---

w "5. K37: mniejszy krok uczenia (dodatkowa kolejka)" nie widać wykresu (o ile jest).

Generalnie uważam że lepiej trzymać się jednej metody, czyli cel za warstwą i po prostu wybierać warstwy które są pełne mało znaczących neuronów (tutaj przydałaby się wizualizacja mapy - dodaj ją)

Co do "6. K38: mapa 100% kod", uważam że powinniśmy trzymać się mapy 75% kod / 25 % tekst

Zastanawiam się nad pass@1,2,3

*2026-10-30 18:28 — Autor*

---
---
---

## Co masz zrobić

Potwierdź dwie decyzje, które wynikają z Twojego wpisu, i odpowiedz na nowe pytania:
- w `AGENTS/phases/phase-2/agents-issues-8.md` wpisz **K40: C** (zawsze cel za warstwą) i **K41: A** (mapa 75/25). Odczytuję tak Twój wpis, ale pola Decyzja wypełniasz Ty; K42 i K43 nadal czekają;
- pytania **K44** (pass@2, pass@3) i **K45** (warstwy najtańsze według mapy) są w `AGENTS/phases/phase-2/agents-issues-9.md`.

### Wykres do sekcji 5 (brakowało go)

![Krok uczenia](AGENTS/phases/phase-2/figures/kod-k37-krok-uczenia.png)

Lewy wykres: błąd walidacji (KL na wyjściu modelu na odłożonej porcji danych treningowych) po kolejnych epokach. Epoka 0 to start po najmniejszych kwadratach. Pomarańczowa linia (krok $5 \cdot 10^{-5}$) przez cały trening jest powyżej startu, więc trening nic nie poprawia. Zielona (krok $1 \cdot 10^{-5}$) spada w każdej epoce. Prawy wykres: KL na odłożonym Pythonie po treningu. Nawet z mniejszym krokiem cel na wyjściu (zielony) zostaje za starym celem za warstwą (żółty).

### Jeden cel treningu i wybór warstw: zgadzam się

Z wyników też to wynika: cel za warstwą działa w środku modelu i jest ~12–18× szybszy. Jedyny argument za celem na wyjściu to końcowe warstwy (26). Tam jednak testy kodu nic nie straciły, więc ta przewaga widać tylko w KL. Wybór warstw według mapy jest prostszy i spójny z Twoim pomysłem z @T009.

### Wizualizacja mapy

![Mapa warstw](AGENTS/phases/phase-2/figures/kod-mapa-warstwy.png)

Każdy wiersz to jedna warstwa (0 u góry, 27 na dole), a w wierszu 3072 neurony ułożone od najważniejszego (lewo) do najmniej ważnego (prawo). Kolor to ważność neuronu (z mapy kodu 75/25) w skali logarytmicznej względem średniej całego modelu: ciemny = ważny, jasny = mało ważny. Pomarańczowe linie pokazują, które neurony usuwamy przy −20% i −40%.

Co widać: końcowe warstwy (ok. 17–25) mają po prawej stronie najjaśniejsze pasy. Najsłabsze 5% neuronów jest tam **~10–20× mniej ważne niż średnia**, a w warstwie 13 ~6× mniej. Na początku modelu (0–7) neurony są bardziej wyrównane: nawet najsłabsze są tylko ~3× mniej ważne niż średnia. Warstwy 26 i 27 mają po lewej najciemniejsze neurony, czyli kilka bardzo ważnych.

![Koszt warstw](AGENTS/phases/phase-2/figures/kod-mapa-koszt-warstw.png)

Lewy wykres: przewidywany koszt usunięcia 20% (niebieskie) i 40% (pomarańczowe) najmniej ważnych neuronów każdej warstwy, czyli suma ich ważności z mapy. Im niżej, tym taniej. ▼ oznacza warstwy już zmniejszane. Prawy wykres: przewidywany koszt (oś pozioma) a zmierzona KL na Pythonie po samym wycięciu (oś pionowa) dla tych czterech warstw.

Co widać:
- **najtańsze według mapy są warstwy 20–25**, przy 40% koszt jest tam ~1,5× mniejszy niż w warstwie 13 i ~2,5× mniejszy niż w warstwach 2–6;
- mapa dobrze porządkuje warstwy 2, 13 i 14. **Warstwa 26 jest wyjątkiem:** zmierzona KL jest tam 2× większa, niż wynikałoby z mapy. Mapa sumuje ważność neuronów osobno, a w końcowych warstwach usunięte neurony najwyraźniej działają razem;
- warstwa 26 mimo to nic nie straciła w testach kodu (raport `porownanie-z-oryginalem.md`), więc mapa może trafniej przewidywać umiejętność pisania kodu niż KL. Sprawdzenie warstw 20–25 to pytanie **K45**.

Skrypt: `scripts/phase2_code_map_figures.py`, koszty warstw: `results/phase2/code/map-layer-costs.json`.

### Mapa 75/25: zgoda

Zostajemy przy 75/25 (K41 = A po Twoim potwierdzeniu).

### pass@1, 2, 3

Przygotowane bez GPU (pytanie **K44**). Wyniki będę podawał też jako liczby zadań, jak prosiłeś w @T015.

*2026-10-30 18:38 — Claude Opus 5.5*

---
---
---

Zastanawiam się czy przewidywany koszt zmniejszenia warstwy bierze pod uwagę odległość neuronu do końca - Oraz jak on w ogóle jest wyliczany

*2026-10-31 23:49 — Autor*

---
---
---

## Co masz zrobić

Nic do decyzji, to odpowiedź na pytanie. Jeśli coś jest niejasne, dopisz pod spodem.

### Jak liczony jest przewidywany koszt warstwy

**1. Ważność jednego neuronu** (mapa z etapu 2, `src/qwen_compression/importance.py`). Dla neuronu $j$ w warstwie $l$:

$$
F_{l,j} = \frac{1}{2\,S\,T} \sum_{\text{sekwencje}} \sum_{s=1}^{S} \Big( \sum_{t} g^{(s)}_{t,l,j} \, a_{t,l,j} \Big)^2
$$

Słownie:
- $a_{t,l,j}$ to aktywacja neuronu przy tokenie $t$, czyli to, co neuron wysyła dalej do `down_proj`;
- $g^{(s)}_{t,l,j}$ mówi, jak mocno zmieniłoby się **wyjście modelu** (log-prawdopodobieństwo wylosowanego tokenu, minus średnia), gdyby ta aktywacja trochę się zmieniła. Liczy się to wsteczną propagacją od wyjścia modelu przez wszystkie dalsze warstwy;
- iloczyn $g \cdot a$ przybliża zmianę wyjścia po wyzerowaniu neuronu. Kwadrat z połową to przybliżenie drugiego rzędu przyrostu KL na wyjściu (tzw. informacja Fishera);
- $S$ to liczba losowań tokenu na sekwencję, a $T$ to łączna liczba tokenów, więc wynik jest średnią na token.

Czyli **$F_{l,j}$ to szacowany przyrost KL na wyjściu modelu po usunięciu samego tego neuronu.**

**2. Mapa 75/25** (`scripts/phase2_code_map.py`). Robimy osobne mapy dla Pythona i dla tekstu C4. W każdej warstwie każdą z nich skalujemy do sumy 1 i łączymy w proporcji 0,75 i 0,25. Potem mnożymy przez sumę mapy kodu w tej warstwie, żeby warstwy dało się ze sobą porównywać.

**3. Koszt warstwy** (`scripts/phase2_code_map_figures.py`). Sortujemy neurony warstwy od najmniej ważnego. Koszt to suma $F$ dla tylu najsłabszych, ile usuwamy: 614 przy 20% albo 1229 przy 40%.

### Czy uwzględnia odległość neuronu od końca modelu

**Tak, pośrednio, i nie trzeba nic dodawać.** $g$ jest liczone na wyjściu modelu, więc obejmuje wszystko, co dzieje się w dalszych warstwach: wzmocnienie, wygaszenie i przejście przez połączenia omijające (residual). Neuron w warstwie 2 jest oceniany po tym, jak jego zmiana przejdzie przez warstwy 3–27, a neuron w warstwie 26 tylko przez warstwę 27. Mapa nie mierzy niczego lokalnie, tylko na samym wyjściu.

Wzór ma jednak trzy uproszczenia:

1. **Liniowość.** Zakłada, że dalsze warstwy reagują na zmianę proporcjonalnie, czyli jak na małą zmianę. Usunięcie 40% neuronów nie jest małą zmianą. Im dalej od końca, tym więcej nieliniowych warstw po drodze, więc przybliżenie może być gorsze.
2. **Niezależność neuronów.** Koszt warstwy to suma kosztów pojedynczych neuronów. Zakładamy więc, że skutki usuniętych neuronów ani się nie sumują ponad to, ani nie znoszą.
3. **Brak naprawy.** Mapa przewiduje koszt **samego wycięcia**, przed najmniejszymi kwadratami i treningiem. Nie wie, jak dobrze pozostałe neurony przejmą pracę usuniętych.

Jak to wygląda na zmierzonych warstwach (KL na Pythonie po samym wycięciu podzielona przez koszt z mapy; 1,0 oznacza trafną przewidywaną liczbę):

| Warstwa | −20% | −40% |
|---|---|---|
| 2 (blisko początku) | 1,03 | 1,15 |
| 13 | 0,78 | 0,77 |
| 14 | 0,74 | 0,72 |
| 26 (blisko końca) | **1,65** | **1,85** |

Co widać:
- mapa trafia rząd wielkości wszędzie, a w warstwach 2–14 myli się o najwyżej ~30%;
- warstwa 2 wypada trochę drożej, niż mapa przewiduje, a środek trochę taniej. To mały efekt w kierunku uproszczenia 1 (dłuższa droga do wyjścia) i na razie widzimy go tylko na jednej wczesnej warstwie;
- **największy błąd jest blisko końca (warstwa 26), czyli tam, gdzie droga do wyjścia jest najkrótsza.** To nie jest więc problem odległości, tylko uproszczenia 2: usunięte neurony w warstwie 26 działają razem i ich skutki się sumują.

Przy kolejnym zmniejszaniu (np. pytanie K45, które zadam ponownie po K43) będę porównywał przewidywanie mapy ze zmierzoną KL i zgodnością tokenu dla każdej nowej warstwy. Pokaże to, w których warstwach mapie można ufać.

*2026-10-31 23:59 — Claude Opus 5.5*

---
---
---

🔒 Dyskusja zakończona na prośbę autora (@T018). Podsumowanie wszystkich raportów Phase 2: `AGENTS/phases/phase-2/raport-zbiorczy-phase-2.md`.

*2026-11-01 14:28 — Claude Opus 5.5*

---
---
---
