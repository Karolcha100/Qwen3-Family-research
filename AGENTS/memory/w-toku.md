# Praca w toku — notatnik bieżącego zadania

Co agent robi **teraz**, w którym kroku jest i co dalej. Aktualizowany w trakcie dłuższych zadań, nie tylko na końcu sesji, żeby po końcu kontekstu albo dłuższej przerwie dało się wrócić dokładnie w to miejsce. Zasady: `AGENTS/memory/procedury.md`, sekcja 7.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Teraz

- Nic nie liczy się na GPU. Kolejki K31–K38 i dodatkowa (do 17:13) skończone; raport `AGENTS/phases/phase-2/etap-4c-k31-k38.md`, pytania K40–K43 w `AGENTS/phases/phase-2/agents-issues-8.md`. Jeśli K43 = A: najpierw policzyć zgodność najbardziej prawdopodobnego tokenu (top-1) z oryginałem dla 4 gotowych modeli (`~/qwen3-checkpoints/phase2-code/mlps/`, ~5 min GPU) i porównać z pass@1 (warstwa 13 −2,7 pkt, warstwa 26 0 pkt).
- Analiza: `scripts/phase2_code_k31_k38_analysis.py` → `results/phase2/code/k31-k38-summary.json` + wykresy `kod-k31-*`, `kod-k37-*`, `kod-k38-*`, `kod-testy-pass1.png`.

## Na co czekam (co odblokuje pracę)

| Czekam na | Odblokuje |
|---|---|
| K40–K43 (`AGENTS/phases/phase-2/agents-issues-8.md`) | cel treningu, waga mapy, scalanie, miara kodu (K43 A: ~5 min GPU) |
| opinia o `AGENTS/phases/phase-0/katalog-metod.md` | wybór metod klasycznych |

## Odłożone pytania

- klasyfikator kodu: „future research” (@phase-2:K33).

## Ostatnia sesja

2026-10-30 17:13: kolejka K31–K38 i dodatkowa kolejka (zgoda autora 16:30), raport etap 4c, pytania K40–K43.
