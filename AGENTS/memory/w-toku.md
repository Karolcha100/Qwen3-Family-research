# Praca w toku — notatnik bieżącego zadania

Co agent robi **teraz**, w którym kroku jest i co dalej. Aktualizowany w trakcie dłuższych zadań, nie tylko na końcu sesji, żeby po końcu kontekstu albo dłuższej przerwie dało się wrócić dokładnie w to miejsce. Zasady: `AGENTS/memory/procedury.md`, sekcja 7.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Teraz

- Nic nie liczy się na GPU. Czekam na K40–K45. Autor w dyskusji etapu 4c: jeden cel (za warstwą) + wybór warstw z mapy, mapa 75/25 → poproszony o wpisanie K40 = C, K41 = A w `agents-issues-8.md`.
- K44 = A (pass@2/3): kolejka z `scripts/phase2_code_generate.py --samples-per-task 10 --batch-size 30` (10 odpowiedzi, T 0,8, top-p 0,95; pamięć KV: ~112 KB/token, 30 sekwencji mieści się w 12 GB) dla `original`, `layer13-40-window`, `layer26-40-output`; wyniki do osobnych katalogów (np. `results/phase2/code-eval/<model>-sampled/`), żeby nie nadpisać odpowiedzi zachłannych. Najpierw oryginał, zmierzyć czas.
- K45 = A: `scripts/phase2_stage4_one_layer.py --layer L --importances perturbation --removed-fractions 0.4 --epochs 6 --save-mlps …` dla L = 20–25 (każda warstwa: ~3 min zbieranie par, 4 GB na dysku), potem testy kodu dla dwóch najlepszych.

## Na co czekam (co odblokuje pracę)

| Czekam na | Odblokuje |
|---|---|
| K40–K43 (`AGENTS/phases/phase-2/agents-issues-8.md`) | cel treningu, waga mapy, scalanie, miara kodu (K43 A: ~5 min GPU) |
| K44, K45 (`AGENTS/phases/phase-2/agents-issues-9.md`) | pass@2/3 (~2–2,5 h GPU), warstwy 20–25 (~1 h GPU) |
| opinia o `AGENTS/phases/phase-0/katalog-metod.md` | wybór metod klasycznych |

## Odłożone pytania

- klasyfikator kodu: „future research” (@phase-2:K33).

## Ostatnia sesja

2026-10-30 18:39: porównanie z oryginałem (liczby zadań), mapa warstw, przygotowanie pass@k, pytania K44–K45.
