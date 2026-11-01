# T019 · Co teraz zostanie policzone?

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Chciałbym się dowiedzieć co będzie teraz liczone na GPU (jak wydam zgodę)

*2026-11-01 14:46 — Autor*

---
---
---

## Co masz zrobić

Przeczytaj. Jeśli plan Ci odpowiada, napisz w czacie „puść kolejkę warstw”. Jeśli chcesz coś zmienić (np. inne warstwy, bez testów kodu, krócej), napisz tutaj co.

### Co policzy się na GPU (kolejka `results/phase2/code/queue-layers.json`, razem ~2 h 50 min)

Kroki idą po kolei, a postęp widać na pasku w GUI.

**1. Zmniejszanie 10 warstw, każda osobno (~110 min, po ~11 min na warstwę).** Kolejno warstwy 24, 25, 20, 23, 21, 22, 17, 18, 15 (najtańsze według mapy, środek i druga połowa modelu) i kontrolnie 10 (wcześniejsza, droższa). W każdej warstwie, osobno przy −20% i −40% neuronów (614 albo 1229 z 3072), przepisem z @T017:
- usuwam najmniej ważne neurony według mapy 75/25;
- najmniejszymi kwadratami poprawiam wagi wyjściowe pozostałych;
- trenuję 6 epok celem za następną warstwą.

Po każdym z tych trzech kroków mierzę **KL na odłożonym Pythonie i na tekście C4** oraz **perpleksję WikiText-2**. Zmniejszone warstwy zapisuję na dysk (`~/qwen3-checkpoints/phase2-code/mlps-layers/`). Zawsze zmniejszona jest tylko jedna warstwa, reszta modelu zostaje bez zmian.

**2. Zestaw zgodności spoza testów, K46 = B (~11 min).**
- Oryginał pisze odpowiedzi na 510 zadań MBPP, których nie ma w testach (jedna odpowiedź bez losowania).
- Liczę zgodność na tych odpowiedziach dla 9 wariantów warstw 13 i 26 z etapu 4c. Sprawdzę w ten sposób, czy nowy zestaw ustawia 4 modele z testami kodu w tej samej kolejności co testy, tak jak zestaw EvalPlus w K43.

**3. Zgodność tokenu dla 20 nowych wariantów (~14 min).** Na zwykłym Pythonie i tekście, na odpowiedziach oryginału na zadania EvalPlus i na nowym zestawie spoza testów.

**4. Testy kodu dla warstw 24, 20, 17 i 10 przy −40% (~32 min, po ~8 min na warstwę).**
- Każdy model pisze jedną odpowiedź bez losowania na 164 zadania HumanEval i 378 MBPP.
- Odpowiedzi idą do testów EvalPlus w kontenerze bez sieci.
- Wynik podam w liczbach zadań, obok oryginału (200 z 542).

Te cztery warstwy wybrałem z góry, żeby uczciwie sprawdzić, czy zgodność przewiduje testy.

### Czego nie będzie

- zmniejszania kilku warstw naraz (o to zapytam po wynikach);
- losowania wielu odpowiedzi (pass@2/3), bo trwa ~40 min na model;
- dotrenowania całego modelu.

### Co dostaniesz potem

Raport z odpowiedziami na trzy pytania:
- czy mapa trafnie przewiduje koszt w warstwach 15–25 (w warstwie 26 się myliła);
- czy zgodność przewiduje testy kodu na nowych warstwach;
- które warstwy najlepiej znoszą zmniejszenie, w liczbach zadań.

W czasie obliczeń karta graficzna jest zajęta (~5 GB), reszta komputera działa normalnie. Testy kodu mają teraz limit czasu, więc nocna awaria się nie powtórzy.

*2026-11-01 14:51 — Claude Opus 5.5*

---
---
---

puść kolejkę warstw

*2026-11-01 14:57 — Autor*

---
---
---

## Co masz zrobić

Nic. Kolejka się liczy, postęp widać na pasku w GUI. Napiszę, gdy będą wyniki.

**Kolejka warstw uruchomiona o 14:59** (Twoja zgoda powyżej, 14:57). Według szacunku skończy się ok. 17:49. Tym razem pilnuje jej strażnik: zgłasza mi każdy zakończony krok i każdy krok, który trwa ponad 2× dłużej niż szacunek. Nocne zawieszenie nie przejdzie więc niezauważone.

*2026-11-01 14:59 — Claude Opus 5.5*

---
---
---

## Co masz zrobić

Przeczytaj raport `AGENTS/phases/phase-2/warstwy-10-25.md` i odpowiedz na K48–K50 w `AGENTS/phases/phase-2/agents-issues-11.md`. Ten wątek możesz zamknąć.

**Kolejka policzona** (14:59–17:51, bez awarii). Najważniejsze, w liczbach zadań „+” z 542 (oryginał 200): warstwa 24 zmniejszona o 40% rozwiązuje 200, warstwa 17 194, warstwa 20 192, a warstwa 10 189. Zgodność na zadaniach spoza testów przewidziała tę kolejność przed testami, poza zamianą warstw 17 i 20 (2 zadania różnicy).

*2026-11-01 17:55 — Claude Opus 5.5*

---
---
---
