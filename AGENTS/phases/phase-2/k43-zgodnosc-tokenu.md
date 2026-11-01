# K43: czy zgodność najbardziej prawdopodobnego tokenu przewiduje testy kodu

*2026-11-01 00:04 — Claude Opus 5.5*

**Status raportu:** zamknięty (2026-11-01 14:28, Claude Opus 5.5 na prośbę autora @T018)
## Co masz zrobić

Przeczytaj. Z raportu wynika jedno pytanie: **K46**, na jakich zadaniach liczyć codziennie zgodność odpowiedzi (`AGENTS/phases/phase-2/agents-issues-10.md`). Uwagi możesz pisać pod raportem.

W skrócie:
- **zgodność tokenu na zwykłym kodzie Pythona** (ten sam zestaw co do KL) poprawia błąd KL (warstwa 26 nie wygląda już 3× gorzej), ale **nie odtwarza** kolejności z testów kodu;
- **zgodność na odpowiedziach oryginału na zadania EvalPlus odtwarza tę kolejność dokładnie**: warstwa 26 jest prawie tak blisko oryginału jak sam szum liczb w bf16, warianty warstwy 13 są dalej. Liczy się to bez uruchamiania kodu, w ~30 s na wariant.

---

## 1. Co zmierzyłem

Dla 9 zapisanych zmniejszonych warstw (wszystkie z etapu 4c) i dla kontroli porównałem z oryginałem (float32) **najbardziej prawdopodobny następny token** w każdym miejscu tekstu. Kontrolą był ten sam oryginał w bf16, czyli w precyzji, w której generujemy odpowiedzi do testów kodu. „Zgodność” to odsetek miejsc, w których model wybrałby ten sam token co oryginał.

Dwa zestawy tekstu:
1. **zestaw do KL:** 16 plików Pythona i 16 tekstów C4 po 2048 tokenów (te same, na których od etapu 4b liczymy KL);
2. **odpowiedzi oryginału na zadania EvalPlus:** do każdego zadania HumanEval (164) i MBPP (378) wstawiam treść zadania i odpowiedź, którą oryginał dał w teście pass@1, razem 42 343 tokeny odpowiedzi. Sprawdzam, czy zmniejszony model w każdym miejscu tej odpowiedzi wybrałby ten sam token. Jeśli tak jest w każdym miejscu, zmniejszony model napisałby **dokładnie tę samą odpowiedź**, więc nie może zmienić wyniku testu.

Przy okazji policzyłem ponownie KL na Pythonie: wyszła identyczna z zapisaną w etapie 4c (np. 0,00306 dla w. 13 z celem za warstwą), więc pomiar jest spójny z wcześniejszymi.

## 2. Wynik na czterech modelach z testami kodu

![Zgodność tokenu a testy kodu](AGENTS/phases/phase-2/figures/kod-k43-zgodnosc-tokenu.png)

Na obu wykresach oś pozioma to zgodność tokenu z oryginałem, a oś pionowa to liczba zadań HumanEval+ i MBPP+ rozwiązanych w teście pass@1 (z 542). Przerywana linia to oryginał w bf16, czyli ile zgodności traci się przez samo zaokrąglanie liczb. Lewy wykres: zestaw do KL. Prawy: odpowiedzi oryginału na zadania EvalPlus.

| Model | rozwiązane zadania „+” (z 542) | KL na Pythonie | zgodność: Python | zgodność: odpowiedzi EvalPlus | odpowiedzi bez zmiany (z 542) |
|---|---|---|---|---|---|
| oryginał | 200 | 0 | 100% | 100% | 542 |
| oryginał w bf16 (kontrola) | — | 0,00045 | 98,93% | 99,59% | 393 |
| **w. 26, cel na wyjściu** | **205** | 0,00940 | 98,19% | **99,44%** | **373** |
| w. 13, mapa 100% kod | 191 | 0,00284 | 98,30% | 98,66% | 252 |
| w. 13, cel za warstwą | 186 | 0,00306 | 98,23% | 98,43% | 229 |
| w. 13, cel na wyjściu | 184 | 0,00375 | 98,02% | 98,27% | 222 |

(„odpowiedzi bez zmiany”: w ilu zadaniach zmniejszony model wybrałby ten sam token w każdym miejscu odpowiedzi oryginału)

Co widać:
- **KL na Pythonie myli się co do warstwy 26** (jest 3× większa niż w warstwie 13, a w testach warstwa 26 wypada najlepiej);
- **zgodność na zestawie do KL** stawia warstwę 26 na równi z warstwą 13 (98,19% wobec 98,23%). To lepsze niż KL, ale nadal nie pokazuje, że warstwa 26 jest lepsza. Do tego wszystkie modele są blisko szumu bf16 (98,93%), więc różnice są małe;
- **zgodność na odpowiedziach EvalPlus ustawia cztery modele dokładnie w tej samej kolejności co testy kodu** (205 > 191 > 186 > 184 zadań i 99,44% > 98,66% > 98,43% > 98,27%). Warstwa 26 jest tu prawie przy szumie bf16 (99,44% wobec 99,59%): w 373 z 542 zadań odpowiedź zostałaby co do tokenu ta sama, a przy samym bf16 w 393;
- KL liczona na tych samych odpowiedziach też ustawia warstwę 26 najlepiej (0,0017 wobec 0,0063–0,0091). **Różnicę robi więc zestaw tekstu, nie sama miara.**

Możliwe wyjaśnienie (niesprawdzone): w zwykłym kodzie pisanym przez ludzi jest dużo miejsc, w których model nie jest pewny (nazwy, komentarze). Zmiana w warstwie 26 głównie „rozmywa” rozkład właśnie tam. We własnych odpowiedziach model jest zwykle pewny kolejnego tokenu, a warstwa 26 tej pewności prawie nie rusza. Mogę to sprawdzić bez GPU, dzieląc tokeny według pewności oryginału.

Ostrożnie z wnioskiem: to tylko 4 modele, a różnice między wariantami warstwy 13 (184–191 zadań) są w granicach przypadku (raport `porownanie-z-oryginalem.md`). Pewne jest rozróżnienie warstwa 26 vs warstwa 13, a kolejność wewnątrz warstwy 13 może być częściowo przypadkowa. Kolejka z nocy doda 4 nowe modele z testami kodu (sekcja 5), więc sprawdzę to na nowych punktach.

## 3. Sprawdzenie, czy „odpowiedź bez zmiany” rzeczywiście oznacza ten sam wynik

| Model | zadania ze zmienionym wynikiem testu | w tym przy odpowiedzi bez zmiany |
|---|---|---|
| w. 26, cel na wyjściu | 15 | 6 |
| w. 13, mapa 100% kod | 41 | 3 |
| w. 13, cel za warstwą | 36 | 5 |
| w. 13, cel na wyjściu | 34 | 2 |

Prawie wszystkie zmiany wyniku w warstwie 13 zdarzają się tam, gdzie zmieniła się odpowiedź. Wyjątki biorą się z tego, że test sprawdzałem w float32 bez wypełnienia, a odpowiedzi do testów kodu powstały w bf16 i w paczkach po 16 zadań. Ta różnica zmienia już sama z siebie 149 z 542 odpowiedzi (wiersz kontroli w tabeli wyżej).

**Uwaga do szumu w testach kodu:** samo przejście z float32 na bf16 zmienia co najmniej jeden token w **~27% odpowiedzi**. Odpowiedzi zachłanne są więc bardzo czułe na drobne zmiany. To tłumaczy, dlaczego każdy wariant „przerzuca” kilkanaście zadań w obie strony.

## 4. Inne warianty (bez testów kodu)

| Wariant (w. 13) | KL na Pythonie | zgodność: Python | zgodność: odpowiedzi EvalPlus |
|---|---|---|---|
| mapa 100% kod, −20% | 0,00111 | 98,91% | 99,23% |
| mapa 75/25, −20%, cel na wyjściu | 0,00163 | 98,72% | 98,76% |
| mapa 75/25, −40%, cel za warstwą, start połączone neurony | 0,00339 | 98,16% | 98,34% |
| start średnia aktywacja, −40% | 0,00344 | 98,17% | 98,11% |
| start losowy, −40% | 0,00503 | 97,75% | 98,09% |

Kolejność jest podobna do kolejności KL. Wnioski z etapu 4c (start z mapy najlepszy, scalanie i losowy start gorsze) potwierdza też nowa miara.

## 5. Wnioski i co dalej

1. Do codziennych pomiarów (@phase-2:K43 = A) dokładam **zgodność odpowiedzi** obok KL na Pythonie. Najmniejszy koszt i najlepsze przewidywanie daje zgodność na gotowych odpowiedziach oryginału na zadania programistyczne (~30 s na wariant, bez uruchamiania kodu). Na jakich zadaniach ją liczyć, to pytanie **K46**.
2. **Testy EvalPlus zostają dla „kamieni milowych”** i do sprawdzania, czy zgodność dalej przewiduje wynik.
3. **Kolejka z nocy** (Twoja zgoda w czacie 1.11 ok. 00:05: „pozwalam puszczać obliczenia do 6:00, posprawdzać, co się dzieje, gdy zmniejszane są inne mało istotne warstwy”):
   - po K44 (pass@2/3, oryginał i w. 13) liczy warstwy 24, 25, 20, 23, 21, 22, 17, 18, 15 (najtańsze według mapy) i dla kontroli warstwę 10, każdą przy −20% i −40%, przepisem z @T017;
   - potem zgodność tokenu dla wszystkich nowych warstw i testy kodu dla warstw 24, 20, 17 i 10 przy −40%. Te warstwy wybrałem z góry, nie według wyników, żeby uczciwie sprawdzić, czy zgodność przewiduje testy.

   Szacunek: koniec ~4:30. Po 6:00 nie zaczynam nowych obliczeń, ale tę kolejkę dokończę, gdyby się przeciągnęła (Twoja druga wiadomość: 6:00 nie jest ścisłym terminem). Wyniki opiszę w osobnym raporcie.

## 6. Pliki

- skrypt pomiaru: `scripts/phase2_code_token_agreement.py`, wykres: `scripts/phase2_code_token_agreement_figure.py`;
- wyniki: `results/phase2/code-eval/token-agreement.json`.

*2026-11-01 00:04 — Claude Opus 5.5*

## Dyskusja

---
---
---

🔒 Dyskusja zakończona na prośbę autora (@T018). Podsumowanie wszystkich raportów Phase 2: `AGENTS/phases/phase-2/raport-zbiorczy-phase-2.md`.

*2026-11-01 14:28 — Claude Opus 5.5*

---
---
---
