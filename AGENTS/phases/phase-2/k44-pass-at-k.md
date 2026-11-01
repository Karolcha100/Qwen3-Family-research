# K44: pass@1, pass@2 i pass@3 dla oryginału i warstwy 13

*2026-11-01 13:08 — Claude Opus 5.5*

**Status raportu:** zamknięty (2026-11-01 14:28, Claude Opus 5.5 na prośbę autora @T018)
## Co masz zrobić

Przeczytaj. Z nocy wynika jedno pytanie: **K47**, czy puścić teraz kolejkę warstw, która w nocy nie ruszyła (`AGENTS/phases/phase-2/agents-issues-10.md`). Uwagi możesz pisać pod raportem.

W skrócie:
- przy 10 losowanych odpowiedziach na zadanie **w. 13 (−40%, cel za warstwą) rozwiązuje prawie tyle samo zadań co oryginał**: w 1 próbie 133 wobec 134, w 3 próbach 217 wobec 226 (z 542). We wszystkich trzech przypadkach różnica mieści się w granicach przypadku;
- różnica 14 zadań przy jednej odpowiedzi bez losowania (200 wobec 186) była więc w dużej części przypadkiem.

---

## 1. Co policzyłem

Każdy model dał **10 losowanych odpowiedzi** na każde z 542 zadań HumanEval i MBPP (temperatura 0,8, top-p 0,95, ustawienie z K44). Wszystkie odpowiedzi przeszły testy EvalPlus w kontenerze. Jeśli z 10 odpowiedzi na zadanie c jest poprawnych, wzór z K44 daje szansę, że **co najmniej jedna z k wylosowanych odpowiedzi** jest poprawna. Suma tych szans po zadaniach to **oczekiwana liczba rozwiązanych zadań** w k próbach.

Przedział 95% dla różnicy między modelami policzyłem metodą bootstrap na parach (to samo zadanie u obu modeli; 10 000 losowań zadań ze zwracaniem).

## 2. Wynik (testy „+”, czyli HumanEval+ i MBPP+, z 542 zadań)

![pass@1–3](AGENTS/phases/phase-2/figures/kod-k44-pass-at-k.png)

Lewy wykres: oczekiwana liczba rozwiązanych zadań w 1, 2 i 3 próbach. Czarna kreska to wynik z jedną odpowiedzią bez losowania (z raportu `porownanie-z-oryginalem.md`). Prawy wykres: różnica w. 13 minus oryginał z przedziałem 95%. Jeśli przedział przecina zero, różnica może być przypadkowa.

| | oryginał | w. 13 −40% | różnica | przedział 95% |
|---|---|---|---|---|
| rozwiązane w 1 próbie (oczekiwane) | 134,0 | 133,4 | −0,6 | od −7,6 do +6,4 |
| rozwiązane w co najmniej 1 z 2 prób | 192,0 | 187,2 | −4,8 | od −14,2 do +4,5 |
| rozwiązane w co najmniej 1 z 3 prób | 225,5 | 217,1 | −8,4 | od −19,2 do +2,5 |
| rozwiązane choć raz w 10 próbach | 311 | 291 | −20 | — |
| rozwiązane za każdym razem (10 z 10) | 15 | 17 | +2 | — |
| jedna odpowiedź bez losowania | 200 | 186 | −14 | — |

Zadania, w których w. 13 miała więcej poprawnych odpowiedzi z 10 niż oryginał: 132, mniej: 147, tyle samo: 263.

Na samych testach podstawowych (bez „+”) obraz jest ten sam: 1 próba 161,1 wobec 163,4 (−2,3, przedział od −10,1 do +5,7), 3 próby 258,9 wobec 264,6 (−5,8, od −17,4 do +5,9).

## 3. Co z tego wynika

1. **Przy jednej próbie w. 13 −40% nie odstaje od oryginału** (−0,6 zadania). Strata 14 zadań przy odpowiedzi bez losowania była w dużej części przypadkiem. Pasuje to do K43: samo przejście na bf16 zmienia ~27% takich odpowiedzi.
2. **Przy większej liczbie prób różnica rośnie** (−4,8, potem −8,4), ale przedziały nadal przecinają zero. Możliwe wyjaśnienie (niesprawdzone): zmniejszona warstwa trochę rzadziej trafia w poprawne, ale mniej prawdopodobne rozwiązania, co widać dopiero przy kilku próbach. Ten sam kierunek pokazuje „choć raz w 10 próbach” (311 wobec 291). Na pewny wniosek trzeba by więcej losowań albo więcej zadań.
3. **Losowanie z temperaturą 0,8 bardzo obniża wynik tego małego modelu:** oryginał w 1 próbie rozwiązuje 134 zadania, a bez losowania 200. Dopiero 3 próby (226) dają wyraźnie więcej niż jedna odpowiedź bez losowania. W K44 pisałem, że pass@1 przy losowaniu wyjdzie „trochę niższy”, a wyszedł dużo niższy. Porównanie modeli jest uczciwe, bo oba liczone są w tym samym ustawieniu.

## 4. Co poszło nie tak w nocy

Testy MBPP dla w. 13 zawiesiły się o 01:23. Niektóre odpowiedzi modelu zajmowały po ~3 GB pamięci, a przy 8 testach naraz w kontenerze z limitem 8 GB system zabił procesy testujące. Program testów nie zgłosił błędu, tylko czekał na nie bez końca. Przez to **kolejka warstw (24, 25, 20, … , 10) w ogóle nie ruszyła**, a komputer stał bezczynnie do rana. Wykryłem to dopiero o 13:00, po Twojej wiadomości.

Naprawa:
- powtórzyłem same testy MBPP z 2 testami naraz (5 min, bez GPU, wynik powyżej);
- w kolejce warstw kroki testów mają teraz limit czasu 30 min i 4 testy naraz;
- zapisałem to jako pułapkę nr 25 w pamięci projektu.

Moje niedopatrzenie: czekałem na koniec procesu i nie sprawdzałem, czy krok testów nie trwa za długo. W następnych nocnych kolejkach przy każdym kroku będę sprawdzał czas pracy.

## 5. Pliki

- skrypt: `scripts/phase2_code_pass_at_k_analysis.py`;
- wyniki: `results/phase2/code-eval/pass-at-k-summary.json`, odpowiedzi i testy: `results/phase2/code-eval/original-sampled/`, `results/phase2/code-eval/layer13-40-window-sampled/`.

*2026-11-01 13:08 — Claude Opus 5.5*

## Dyskusja

---
---
---

🔒 Dyskusja zakończona na prośbę autora (@T018). Podsumowanie wszystkich raportów Phase 2: `AGENTS/phases/phase-2/raport-zbiorczy-phase-2.md`.

*2026-11-01 14:28 — Claude Opus 5.5*

---
---
---
