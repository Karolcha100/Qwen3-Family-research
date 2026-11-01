# Praca w toku — notatnik bieżącego zadania

Co agent robi **teraz**, w którym kroku jest i co dalej. Aktualizowany w trakcie dłuższych zadań, nie tylko na końcu sesji, żeby po końcu kontekstu albo dłuższej przerwie dało się wrócić dokładnie w to miejsce. Zasady: `AGENTS/memory/procedury.md`, sekcja 7.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Teraz

- Kolejka warstw skończona 17:51 (start 14:59). Raport `AGENTS/phases/phase-2/warstwy-10-25.md`, pytania K48–K50 (`AGENTS/phases/phase-2/agents-issues-11.md`).
- Przy K49 = A potrzebny kod: opcja „wcześniejsze zmniejszone warstwy” w `scripts/phase2_stage4_one_layer.py` (zbieranie par z modelu z już zmniejszonymi warstwami) + skrypt składający kilka gotowych MLP (zgodność, KL, testy kodu). GPU dopiero po „uruchom”.

## Na co czekam (co odblokuje pracę)

| Czekam na | Odblokuje |
|---|---|
| K48–K50 (`AGENTS/phases/phase-2/agents-issues-11.md`) | miara wyboru, kilka warstw naraz, koniec Phase 2 |
| opinia o `AGENTS/phases/phase-0/katalog-metod.md` | wybór metod klasycznych |

## Odłożone pytania

- klasyfikator kodu: „future research” (@phase-2:K33).

## Ostatnia sesja

2026-11-01 17:55: kolejka warstw policzona, raport `warstwy-10-25.md`, K48–K50.

## Przewidywanie przed testami kodu kolejki warstw (2026-11-01 17:19)

Wynik: 24 → 200, 17 → 194, 20 → 192, 10 → 189 (zamiana 17/20 o 2 zadania; raport `warstwy-10-25.md`). Zapisane, zanim testy kodu warstw 24, 20, 17, 10 (−40%) się skończyły. Według zgodności na 510 zadaniach spoza testów (`results/phase2/code-eval/token-agreement-layers.json`):
- kolejność rozwiązanych zadań „+”: **24 (98,98%) > 20 (98,52%) > 17 (98,24%) > 10 (97,90%)**;
- skala z 4 wcześniejszych modeli (w. 26 99,34% → 205 zadań; w. 13 98,11–98,35% → 184–191): w. 24 ok. 195–200, w. 20 ok. 188–192, w. 17 ok. 184–188, w. 10 poniżej 184.
