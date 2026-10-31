# Praca w toku — notatnik bieżącego zadania

Co agent robi **teraz**, w którym kroku jest i co dalej. Aktualizowany w trakcie dłuższych zadań, nie tylko na końcu sesji, żeby po końcu kontekstu albo dłuższej przerwie dało się wrócić dokładnie w to miejsce. Zasady: `AGENTS/memory/procedury.md`, sekcja 7.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Teraz

- **Noc 1.11 (zgoda autora w czacie 00:05: GPU do ~6:00, termin miękki — kolejki puszczone wcześniej wolno dokończyć, nowych po 6:00 nie zaczynać).**
- Kolejka 1 `results/phase2/code/queue-k43-k44.json` (PID run_queue 282067): K43 zrobione (raport `AGENTS/phases/phase-2/k43-zgodnosc-tokenu.md`), K44 pass@1–3 (10 losowań, oryginał + w. 13 cel za warstwą) → `results/phase2/code-eval/<model>-sampled/`.
- Kolejka 2 `results/phase2/code/queue-layers.json` startuje po końcu PID 282067: warstwy 24, 25, 20, 23, 21, 22, 17, 18, 15, 10 (−20/−40%, przepis @T017) → `results/phase2/code/layers/`, MLP w `~/qwen3-checkpoints/phase2-code/mlps-layers/`; zgodność → `results/phase2/code-eval/token-agreement-layers.json`; testy kodu w. 24/20/17/10 −40% → `results/phase2/code-eval/layer<L>-40-window/`.
- Po końcu: raport K44 (liczby zadań: rozwiązane w ≥1 z k prób + pass@k), raport warstw (KL, zgodność, mapa vs pomiar, testy), wykresy, briefing, commit, push.

## Na co czekam (co odblokuje pracę)

| Czekam na | Odblokuje |
|---|---|
| K46 (`AGENTS/phases/phase-2/agents-issues-10.md`) | zestaw zadań do codziennej zgodności (B: MBPP spoza MBPP+) |
| opinia o `AGENTS/phases/phase-0/katalog-metod.md` | wybór metod klasycznych |

## Odłożone pytania

- klasyfikator kodu: „future research” (@phase-2:K33).

## Ostatnia sesja

2026-11-01 00:07: K43 (zgodność tokenu), odpowiedzi T017 i dyskusja 4c, nocne kolejki K44 + warstwy.
