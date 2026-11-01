# Zmniejszanie kolejnych warstw (10, 15, 17, 18, 20–25): KL, mapa, zgodność i testy kodu

*2026-11-01 17:55 — Claude Opus 5.5*

**Status raportu:** do przeczytania

## Co masz zrobić

Przeczytaj i odpowiedz na **K48–K50** w `AGENTS/phases/phase-2/agents-issues-11.md`:
- K48: którą miarą wybierać warstwy i warianty;
- K49: jaki następny krok;
- K50: czy zamknąć Phase 2.

Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”. Uwagi pisz pod raportem.

W skrócie (liczby zadań „+” z 542, oryginał rozwiązuje 200):
- **nowe warstwy zmniejszone o 40% tracą od 0 do 11 zadań.** Wyniki: warstwa 24 rozwiązuje 200 zadań, warstwa 17 194, warstwa 20 192, a warstwa 10 189. Wcześniej warstwa 13 traciła 9–16 zadań, a warstwa 26 zyskała 5;
- **zgodność odpowiedzi z oryginałem przewiduje testy kodu, a KL nie.** Na 8 modelach z testami korelacja rang zgodności z liczbą zadań wynosi 0,86, a KL na Pythonie tylko 0,48. Przewidywanie zapisałem przed testami i trafiło, poza zamianą warstw 20 i 17, które różnią się o 2 zadania;
- **zestaw 510 zadań spoza testów (K46 B) działa tak samo dobrze jak zadania testowe**, więc może być codzienną miarą;
- **w końcowych warstwach (20–25) KL wychodzi duża, a programowanie się trzyma.** Model traci tam głównie tekst: KL na C4 jest 2–2,5× większa niż w środku modelu. Mapa zaniża ich koszt w KL 1,1–2,6×, ale ich kolejność według zgodności i testów kodu oddaje dobrze;
- **naprawa (najmniejsze kwadraty + trening) prawie nie działa w końcowych warstwach.** Zostaje tam 83–93% szkody, a w środku modelu 52–58%.

---

## 1. Co policzono

Kolejka 14:59–17:51 (Twoja zgoda w @T019; 172 min wobec szacunku 167):
1. **10 warstw, każda osobno, przy −20% i −40% neuronów**, przepisem z @T017 (mapa 75/25 → najmniejsze kwadraty → 6 epok celem za warstwą, krok $5 \cdot 10^{-5}$). Warstwy 24, 25, 20, 23, 21, 22, 17, 18, 15 to najtańsze według mapy, a warstwa 10 jest kontrolna. Warstwy 2, 13, 14 i 26 były policzone tym samym przepisem w etapie 4b, więc dołączyłem je do porównania;
2. **zestaw spoza testów (K46 B):** oryginał napisał odpowiedzi na 510 zadań MBPP, których nie ma w testach. Zgodność policzyłem dla wszystkich nowych wariantów i dla 9 wcześniejszych;
3. **testy kodu** (jedna odpowiedź bez losowania, EvalPlus w kontenerze) dla warstw 24, 20, 17 i 10 przy −40%. Te warstwy wybrałem z góry, zanim cokolwiek było policzone.

Za każdym razem zmniejszona jest tylko jedna warstwa (0,6% parametrów modelu przy −40%).

## 2. Testy kodu i zgodność odpowiedzi

![Zgodność a testy kodu](AGENTS/phases/phase-2/figures/kod-warstwy-zgodnosc-testy.png)

Na obu wykresach oś pozioma to zgodność tokenu z oryginałem, czyli odsetek miejsc w odpowiedziach oryginału, w których zmniejszony model wybrałby ten sam token. Oś pionowa to liczba zadań HumanEval+ i MBPP+ rozwiązanych w testach. Niebieskie punkty to nowe warstwy, pomarańczowe to 4 wcześniejsze modele. Przerywana linia pionowa to szum samego bf16, a kropkowana pozioma to oryginał. Lewy wykres: zgodność na odpowiedziach na zadania testowe. Prawy: na 510 zadaniach spoza testów.

| Model (−40%) | rozwiązane „+” (z 542) | zgodność spoza testów | zgodność na zadaniach testowych | KL na Pythonie |
|---|---|---|---|---|
| oryginał | 200 | 100% | 100% | 0 |
| w. 26 (cel na wyjściu, etap 4c) | **205** | 99,34% | 99,44% | 0,0094 |
| **w. 24 (nowa)** | **200** | 98,98% | 99,29% | 0,0070 |
| **w. 17 (nowa)** | 194 | 98,24% | 98,49% | 0,0030 |
| **w. 20 (nowa)** | 192 | 98,52% | 98,92% | 0,0039 |
| w. 13, mapa 100% kod | 191 | 98,35% | 98,66% | 0,0028 |
| **w. 10 (nowa)** | 189 | 97,90% | 98,23% | 0,0047 |
| w. 13, cel za warstwą | 186 | 98,23% | 98,43% | 0,0031 |
| w. 13, cel na wyjściu | 184 | 98,11% | 98,27% | 0,0038 |

Co widać:
- **zgodność układa modele prawie w kolejności testów.** Korelacja rang wynosi 0,86 dla obu zestawów (p = 0,007), a dla KL na Pythonie tylko 0,48. Przykład: warstwa 24 ma ponad 2× większą KL niż warstwa 17, a rozwiązuje o 6 zadań więcej;
- **sprawdzenie z góry.** Kolejność 24 > 20 > 17 > 10 zapisałem przed końcem testów (commit 626e771, `AGENTS/memory/w-toku.md`). Wyszło 24 > 17 > 20 > 10. Jedyna pomyłka to zamiana warstw 17 i 20, które różnią się o 2 zadania, czyli mniej niż szum testów (sam bf16 zmienia ~27% odpowiedzi). Przewidziane liczby trafiły dla w. 24 (195–200 → 200) i w. 20 (188–192 → 192). Dla w. 17 (184–188 → 194) i w. 10 („poniżej 184” → 189) wynik był lepszy;
- **zestaw spoza testów przewiduje tak samo dobrze jak zadania testowe.** Możemy więc wybierać warianty bez patrzenia na zadania testowe (K46 = B);
- warstwa 25 nie miała testów kodu, ale ma najwyższą zgodność ze wszystkich: przy −20% 99,67%, czyli bliżej oryginału niż sam szum bf16 (99,47%), a przy −40% 99,38%.

Ostrożnie: to 8 modeli i różnice rzędu kilku zadań. Pewne jest, że zgodność jest dużo lepsza od KL. Dokładna kolejność modeli różniących się o 2–3 zadania jest już przypadkowa.

## 3. KL i mapa

![KL po treningu](AGENTS/phases/phase-2/figures/kod-warstwy-kl.png)

Co widać: na Pythonie (lewy wykres) najmniejszą KL po zmniejszeniu mają warstwy 13–18. Warstwa 20 ma niewiele więcej, a w warstwach 21–24 KL jest 2–2,7× większa niż w warstwie 13. Wyjątkiem jest warstwa 25. Na tekście C4 (prawy wykres) wzrost jest jeszcze wyraźniejszy: przy −40% w warstwach 21–25 KL wynosi 0,019–0,021, czyli ~2,4× więcej niż w warstwie 13 (0,008).

![Mapa a pomiar](AGENTS/phases/phase-2/figures/kod-warstwy-mapa.png)

Każdy punkt to warstwa (liczba przy punkcie). Oś pozioma pokazuje przewidywany koszt z mapy, a oś pionowa zmierzoną KL na Pythonie po samym wycięciu. Punkty na przerywanej linii oznaczają, że mapa trafia dokładnie.

Co widać:
- **warstwy 10–18 leżą na linii albo pod nią.** Zmierzony koszt to 0,72–1,08 przewidywanego, więc mapa trafia albo lekko zawyża;
- **warstwy 20–24 leżą wysoko nad linią.** Zmierzony koszt to 1,1–2,6 przewidywanego, a warstwa 25 jest znowu blisko linii (1,1–1,3). To ten sam efekt co wcześniej w w. 26: w końcowych warstwach usunięte neurony działają razem, więc ich skutki się sumują;
- mimo to **kolejność końcowych warstw według mapy dobrze pasuje do zgodności i testów kodu.** Warstwy 24 i 25 są najlepsze według zgodności, a w. 24 nic nie traci w testach. Mapa wskazuje warstwy dobre do pisania kodu, a KL karze je głównie za utratę tekstu.

## 4. Naprawa nie działa w końcowych warstwach

Ile KL na Pythonie zostaje po najmniejszych kwadratach i treningu, w procentach KL samego wycięcia:

| Warstwy | −20% | −40% |
|---|---|---|
| 10–18 | 52–58% | 53–58% |
| 20–21 | 70–80% | 67–74% |
| 22–26 | 88–93% | 83–92% |
| 2 (początek, dla porównania) | 69% | 72% |

W środku modelu naprawa usuwa prawie połowę szkody, a w końcowych warstwach tylko 7–17%. Możliwe wyjaśnienie (niesprawdzone): cel treningu to „wyjście następnej warstwy”. Pod koniec modelu mały błąd w strumieniu rezydualnym daje dużą zmianę na wyjściu, a cel tego nie widzi. W w. 26 pomógł cel na wyjściu modelu (−17% KL, etap 4c), ale był ~18× wolniejszy.

Perpleksja WikiText-2 (oryginał 12,66) rośnie przy −40% o 0,7–1,3% w warstwach 10–18 i o 2,1–2,7% w warstwach 20–25. Jest to ten sam obraz co w KL na tekście.

## 5. Wszystkie liczby

(* = policzone tym samym przepisem w etapie 4b)

| Warstwa | usunięte | przewidywany koszt z mapy | KL Python: samo wycięcie | zmierzona / przewidziana | KL Python po treningu | ile KL zostaje po naprawie | KL C4 po treningu | perpleksja WikiText-2 | zgodność spoza testów | rozwiązane „+” |
|---|---|---|---|---|---|---|---|---|---|---|
| 2* | 20% | 0,0055 | 0,0057 | 1,03 | 0,0039 | 69% | 0,0100 | 12,81 | — | — |
| 2* | 40% | 0,0129 | 0,0148 | 1,15 | 0,0107 | 72% | 0,0261 | 12,98 | — | — |
| 10 | 20% | 0,0034 | 0,0037 | 1,08 | 0,0019 | 52% | 0,0046 | 12,69 | 98,41% | — |
| 10 | 40% | 0,0084 | 0,0089 | 1,06 | 0,0047 | 53% | 0,0110 | 12,78 | 97,90% | 189 |
| 13* | 20% | 0,0031 | 0,0024 | 0,78 | 0,0013 | 55% | 0,0034 | 12,69 | — | — |
| 13* | 40% | 0,0076 | 0,0059 | 0,77 | 0,0032 | 55% | 0,0081 | 12,75 | — | — |
| 14* | 20% | 0,0030 | 0,0022 | 0,74 | 0,0012 | 53% | 0,0037 | 12,70 | — | — |
| 14* | 40% | 0,0075 | 0,0054 | 0,72 | 0,0030 | 55% | 0,0085 | 12,75 | — | — |
| 15 | 20% | 0,0029 | 0,0021 | 0,74 | 0,0011 | 54% | 0,0035 | 12,70 | 98,83% | — |
| 15 | 40% | 0,0074 | 0,0053 | 0,72 | 0,0029 | 55% | 0,0087 | 12,77 | 98,31% | — |
| 17 | 20% | 0,0023 | 0,0020 | 0,86 | 0,0012 | 58% | 0,0042 | 12,70 | 98,89% | — |
| 17 | 40% | 0,0066 | 0,0051 | 0,78 | 0,0030 | 58% | 0,0113 | 12,83 | 98,24% | 194 |
| 18 | 20% | 0,0024 | 0,0021 | 0,88 | 0,0012 | 57% | 0,0049 | 12,71 | 98,74% | — |
| 18 | 40% | 0,0071 | 0,0060 | 0,85 | 0,0033 | 54% | 0,0128 | 12,82 | 98,29% | — |
| 20 | 20% | 0,0016 | 0,0027 | 1,67 | 0,0019 | 70% | 0,0059 | 12,74 | 98,99% | — |
| 20 | 40% | 0,0053 | 0,0058 | 1,10 | 0,0039 | 67% | 0,0158 | 12,92 | 98,52% | 192 |
| 21 | 20% | 0,0016 | 0,0031 | 1,93 | 0,0025 | 80% | 0,0063 | 12,77 | 99,10% | — |
| 21 | 40% | 0,0055 | 0,0084 | 1,54 | 0,0063 | 74% | 0,0195 | 12,95 | 98,51% | — |
| 22 | 20% | 0,0017 | 0,0042 | 2,56 | 0,0038 | 89% | 0,0077 | 12,77 | 99,16% | — |
| 22 | 40% | 0,0056 | 0,0087 | 1,55 | 0,0073 | 83% | 0,0209 | 12,95 | 98,61% | — |
| 23 | 20% | 0,0017 | 0,0037 | 2,14 | 0,0034 | 93% | 0,0070 | 12,77 | 99,30% | — |
| 23 | 40% | 0,0053 | 0,0094 | 1,76 | 0,0085 | 91% | 0,0201 | 12,97 | 98,78% | — |
| 24 | 20% | 0,0017 | 0,0032 | 1,93 | 0,0029 | 91% | 0,0074 | 12,77 | 99,36% | — |
| 24 | 40% | 0,0048 | 0,0078 | 1,62 | 0,0070 | 89% | 0,0191 | 12,99 | 98,98% | 200 |
| 25 | 20% | 0,0018 | 0,0022 | 1,27 | 0,0020 | 88% | 0,0068 | 12,78 | 99,67% | — |
| 25 | 40% | 0,0050 | 0,0054 | 1,08 | 0,0047 | 88% | 0,0188 | 13,00 | 99,38% | — |
| 26* | 20% | 0,0022 | 0,0036 | 1,65 | 0,0034 | 92% | 0,0087 | 12,89 | — | — |
| 26* | 40% | 0,0066 | 0,0122 | 1,85 | 0,0113 | 92% | 0,0233 | 13,26 | — | — |

## 6. Wnioski

1. **Dla celu „programowanie” (@phase-2:K25) miarą do wyboru wariantów powinna być zgodność na zadaniach spoza testów, a nie KL.** KL dwa razy pomyliła się co do końcowych warstw (w. 26, teraz w. 24).
2. **Pojedyncza warstwa zmniejszona o 40% kosztuje od 0 do 16 zadań (nowe warstwy 0–11), a w. 26 nawet zyskała 5.** Najlepsze kandydatki według zgodności to warstwy 25, 24 i 23, a potem 22, 21 i 20. Środek (13–18) jest lepszy według KL i dla tekstu.
3. **Końcowe warstwy oddają tekst, a zachowują kod.** Jeśli tekst ma znaczenie, trzeba to uwzględnić w wyborze (K48).
4. Przy wielu warstwach naraz straty będą się sumować. Ile, sprawdzi dopiero następny krok (K49).

## 7. Pliki

- analiza i wykresy: `scripts/phase2_code_layers_analysis.py` → `results/phase2/code/layers/summary.json`;
- wyniki warstw: `results/phase2/code/layers/layer-*/results.jsonl`, zmniejszone warstwy: `~/qwen3-checkpoints/phase2-code/mlps-layers/`;
- zgodność: `results/phase2/code-eval/token-agreement-layers.json` (nowe warstwy), `token-agreement-with-held-out.json` (wcześniejsze warianty);
- zestaw spoza testów: `results/phase2/code-agreement/` (zadania + odpowiedzi oryginału);
- testy kodu: `results/phase2/code-eval/layer{10,17,20,24}-40-window/`.

*2026-11-01 17:55 — Claude Opus 5.5*
