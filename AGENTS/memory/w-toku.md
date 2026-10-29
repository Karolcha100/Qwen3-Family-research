# Praca w toku — notatnik bieżącego zadania

Co agent robi **teraz**, w którym kroku jest i co dalej. Aktualizowany w trakcie dłuższych zadań, nie tylko na końcu sesji, żeby po końcu kontekstu albo dłuższej przerwie dało się wrócić dokładnie w to miejsce. Zasady: `AGENTS/memory/procedury.md`, sekcja 7.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Teraz

**@L13: Phase 2, etap 1 (pilot) — kod gotowy, czeka na „uruchom etap 1”.**
- Zrobione: pakiet `src/qwen_compression/` (data, model_parts, perturbation z `measure_perturbations`, metrics, activations, importance), 28 testów CPU, ruff/pyright czyste; zbiór pomiarowy `~/qwen3-checkpoints/phase2/measurement-set.pt` (64 × 2048, co 4. = kod, 7 języków); skrypt `scripts/phase2_stage1_pilot.py` (kroki: precision, statistics, exact, noise, fisher; każdy zapisuje wynik i jest pomijany przy wznowieniu).
- Następny krok po „uruchom”: `uv run python scripts/phase2_stage1_pilot.py` w tle (wyniki: `results/phase2/stage1/`, log: `results/phase2/stage1/log.jsonl`), ~3 h; potem skrypt analizy (Spearman przesiew ↔ dokładnie, pokrycie top 10%, szum, 4096 vs 16 384 tokenów, bf16 vs fp32) i raport `AGENTS/phases/phase-pomysl/etap-1-pilot.md`.
- Wznowienie po przerwaniu: to samo polecenie (gotowe kroki i warstwy są pomijane).

## Na co czekam (co odblokuje pracę)

| Czekam na | Odblokuje |
|---|---|
| **„uruchom etap 1”** od autora | @L13: pilot (~3 h GPU) |
| opinia o `AGENTS/phases/phase-0/plan-metryki-oceny.md` | @L7 zestaw pytań (dopiero Phase 3) |

## Odłożone pytania

- brak (proporcje tekstu pomiarowego zadane jako @phase-pomysl:K11).

## Ostatnia sesja

2026-10-29 21:49: plan Phase 2 zatwierdzony (21:36), plan metryk zatwierdzony (21:37). Napisany kod etapu 1 + testy + zbiór pomiarowy. Czekam na „uruchom etap 1”.
