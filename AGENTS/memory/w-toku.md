# Praca w toku — notatnik bieżącego zadania

Co agent robi **teraz**, w którym kroku jest i co dalej. Aktualizowany w trakcie dłuższych zadań, nie tylko na końcu sesji, żeby po końcu kontekstu albo dłuższej przerwie dało się wrócić dokładnie w to miejsce. Zasady: `AGENTS/memory/procedury.md`, sekcja 7.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Teraz

**@L13: Phase 2 — autor (22:07): „uruchom wszystkie etapy, idę spać”.** Plan nocy i zastrzeżenia: @T010.
- **Etap 1 (pilot) liczy się w float32 od 22:10**, PID 110275 (`nohup`), 4096 tokenów (sekwencje 0 = C4, 3 = kod; szum na 4 i 7). Wznowienie: `HF_HUB_DOWNLOAD_TIMEOUT=60 nohup .venv/bin/python scripts/phase2_stage1_pilot.py >> results/phase2/stage1/stdout.log 2>&1 &` (gotowe kroki i warstwy są pomijane).
- Zrobione: `precision.pt` (bf16 = szum 1,3e-3; float32 kontrola −2e-9, mediana wyłączenia 1,3e-5 → float32), `statistics.pt` (bf16, 8 sekwencji, wystarczy).
- Gotowe (CPU, commit 846b5e4): `scripts/phase2_stage1_analysis.py` (→ `results/phase2/stage1/summary.json` + wykresy w `AGENTS/phases/phase-pomysl/figures/`), `scripts/phase2_stage2_full_map.py --mode screened|exact-all`, `scripts/phase2_stage4_one_layer.py --layer N` (sprawdzony na CPU na małym modelu; najlepsza epoka). 34 testy. Zbiór treningowy etapu 4: `~/qwen3-checkpoints/phase2/training-set.pt` (488 × 2048, ziarno 1). Wpis „zamknąłem…” przeniesiony do planu metryk. @L14: brak reprodukcji w kodzie — zapytać autora o kroki.
- Do napisania po etapie 2: skrypt etapu 3 (progi z danych; „martwy” względnie, bo 92% neuronów jest aktywnych; masywne neurony: warstwa 2 #55, #1489, #128 do 3728, warstwa 27).
- Dalej: analiza → raport `etap-1-pilot.md` → etap 2 według reguł z @T010 → etap 3 (bez klasyfikatora) → etap 4 (warstwa tymczasowa).

## Na co czekam (co odblokuje pracę)

| Czekam na | Odblokuje |
|---|---|
| **„uruchom etap 1”** od autora | @L13: pilot (~3 h GPU) |
| opinia o `AGENTS/phases/phase-0/plan-metryki-oceny.md` | @L7 zestaw pytań (dopiero Phase 3) |

## Odłożone pytania

- brak (proporcje tekstu pomiarowego zadane jako @phase-pomysl:K11).

## Ostatnia sesja

2026-10-29 21:49: plan Phase 2 zatwierdzony (21:36), plan metryk zatwierdzony (21:37). Napisany kod etapu 1 + testy + zbiór pomiarowy. Czekam na „uruchom etap 1”.
