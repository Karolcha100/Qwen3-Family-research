# T007 · Co mam teraz zrobić?

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Rozpisz mi po krótce co mam teraz zrobić

*2026-10-29 17:41 — Autor*

---
---
---

## Co masz zrobić

Kolejność od tego, co **najbardziej odblokowuje pracę**. Kroki 1–4 to razem ~40 minut, a potem mogę działać sam. Sprawdziłem system: żadna z instalacji nie jest jeszcze zrobiona.

### Teraz (do startu Phase 1)

| # | Co | Gdzie w GUI | Czas | Odblokowuje |
|---|---|---|---|---|
| 1 | **Zatwierdź plan Phase 1** (✅ Zatwierdzam plan) | Plany do zatwierdzenia i opinii → `phases/phase-1/plan.md` | 2 min | wszystkie moje prace w Phase 1 |
| 2 | **@A8:** jedno polecenie `sudo dnf install …` (pakiety + uv) | Twoje zadania (otwarte) → Ważne → A8 | 3 min | @L2: stawiam środowisko Pythona |
| 3 | **@A6:** usunięcie CUDA 12 (4 kroki, przejrzyj listę przed `y`) | Twoje zadania (otwarte) → Ważne → A6 | 10 min | @A7 |
| 4 | **@A7:** pobranie i instalacja CUDA 13.4 | Twoje zadania (otwarte) → Ważne → A7 | 15–20 min | @L3: buduję llama.cpp |

Po każdym zadaniu wklej wynik sprawdzenia w raporcie (albo napisz „zrobione”). Kroki 2 i 3–4 są niezależne: możesz zrobić najpierw A8, a CUDA później.

### Przy okazji (po minucie każde)

| # | Co | Gdzie |
|---|---|---|
| 5 | odpowiedź końcowa w **K14**: „A” (ruff/pyright/pytest; wyjaśnienie pod @A9) | Pytania w toku (przeniesione do zadań) → K14 |
| 6 | odpowiedź końcowa w **K36**: „zgoda” na porównanie z BF16 + percentyle + Elo (pod @A10) | Pytania w toku (przeniesione do zadań) → K36 |

### Spokojnie, przed Phase 2 (nie blokuje Phase 1)

| # | Co | Gdzie | Czas |
|---|---|---|---|
| 7 | przeczytaj raporty i wybierz w **@A2** (Base czy instrukcyjny), **@A3** (kalibracja), **@A4** (perplexity); we wszystkich rekomenduję A | Twoje zadania (otwarte) → Ważne → A2, A3, A4 | 20–30 min |
| 8 | przejrzyj **katalog metod**, wybierz metody i rozpisz kolejne fazy (Twoja decyzja z @phase-0:K2) | Plany → `phases/phase-0/katalog-metod.md` | ile chcesz |
| 9 | opinia o **liście 16 metryk** | Plany → `phases/phase-0/plan-metryki-oceny.md` | 10 min |

### Co ja zrobię, gdy skończysz 1–4

1. środowisko Pythona (uv, Python 3.14, PyTorch, transformers, lm-eval) — @L2;
2. budowa llama.cpp z CUDA — @L3;
3. potem napiszę Ci „gotowe do testu” i **poczekam na Twoje „uruchom”**, zanim użyję GPU do testów dymnych (@L4).

Pełna lista „co odblokowuje co” jest zawsze aktualna w `AGENTS/memory/w-toku.md`.

*2026-10-29 17:42 — Claude Opus 5.5*

---
---
---

## Co masz zrobić

Zaktualizowana lista (stan na 19:33). Zrobione od ostatniej listy: odpowiedzi końcowe w K7, K8, K9, K14 i K36. Zamknąłem zadania @A2, @A3, @A4, @A9, @A10, a Elo jest już w planie metryk (@L6). Sprawdziłem system: instalacje nadal nie są zrobione, a plan Phase 1 czeka na zatwierdzenie.

### Teraz (do startu Phase 1) — bez zmian

| # | Co | Gdzie w GUI | Czas | Odblokowuje |
|---|---|---|---|---|
| 1 | **Zatwierdź plan Phase 1** (✅ Zatwierdzam plan) | Plany do zatwierdzenia i opinii → `phases/phase-1/plan.md` | 2 min | wszystkie moje prace w Phase 1 |
| 2 | **@A8:** jedno polecenie `sudo dnf install …` (pakiety + uv) | Twoje zadania (otwarte) → Ważne → A8 | 3 min | @L2: środowisko Pythona |
| 3 | **@A6:** usunięcie CUDA 12 | Twoje zadania (otwarte) → Ważne → A6 | 10 min | @A7 |
| 4 | **@A7:** instalacja CUDA 13.4 | Twoje zadania (otwarte) → Ważne → A7 | 15–20 min | @L3: budowa llama.cpp |

### Przed Phase 2 — nowe, najważniejsze

| # | Co | Gdzie |
|---|---|---|
| 5 | **Napisz mi swój główny pomysł.** W K8 wspomniałeś, że nie chcesz kwantyzować modelu w klasyczny sposób i że głównego pomysłu jeszcze nie opisałeś. Od niego zależy, które metody, dane kalibracyjne i kod mają sens, więc dopóki go nie znam, niczego pod metody nie projektuję. | ➕ Nowy wątek |
| 6 | Na podstawie pomysłu: wybór metod i opis kolejnych faz (możesz skorzystać z katalogu albo nie) | Plany → `phases/phase-0/katalog-metod.md` |
| 7 | Opinia o liście 16 metryk (teraz z sekcją Elo) | Plany → `phases/phase-0/plan-metryki-oceny.md` |

### Co ja zrobię, gdy skończysz 1–4

1. środowisko Pythona — @L2;
2. budowa llama.cpp — @L3;
3. napiszę „gotowe do testu” i **poczekam na Twoje „uruchom”** (@L4).

*2026-10-29 19:33 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-10-29 20:59 — Autor*

---
---
---
