# Praca w toku — notatnik bieżącego zadania

Co agent robi **teraz**, w którym kroku jest i co dalej. Aktualizowany w trakcie dłuższych zadań, nie tylko na końcu sesji, żeby po końcu kontekstu albo dłuższej przerwie dało się wrócić dokładnie w to miejsce. Zasady: `AGENTS/memory/procedury.md`, sekcja 7.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Teraz

- Nic się nie liczy. **@L19, @L21 zrobione** (przygotowanie K31–K38 @T013, pasek postępu @T014). **Kolejka gotowa, nieuruchomiona:** `results/phase2/code/queue.json` (16 kroków, ~167 min według szacunków; czeka na @phase-2:K39 = „uruchom”).
- Uruchomienie w tle (Bash `run_in_background`): `uv run --no-sync python scripts/run_queue.py results/phase2/code/queue.json` — postęp w `AGENTS/postep-obliczen.json` (pasek w GUI). Po zakończeniu: wykresy/raport dla K31 (`results/phase2/code/k31/`), K37 (`results/phase2/code/k37/`), K38 (wiersze `code-only` w `results/phase2/code/stage4/layer-13/`), testy kodu (`results/phase2/code-eval/*/…-summary.json`, `…-efficiency.json`). Porównać faktyczne czasy kroków z szacunkami (procedury, sekcja 10).
- Kontener: `podman build -t qwen-code-sandbox sandbox` (zbudowany), wolumen `qwen-evalplus-cache` (zadania i oczekiwane wyniki). Zadania: `results/phase2/code-eval/*-problems.jsonl`.
- Dane poza repo: `~/qwen3-checkpoints/phase2-code/` (zbiory, pary warstw 2/13/14/26, `mlps/` po kolejce).

## Na co czekam (co odblokuje pracę)

| Czekam na | Odblokuje |
|---|---|
| K39 (`AGENTS/phases/phase-2/agents-issues-7.md`) | kolejka K31, K37, K38 + HumanEval/MBPP (~3–3,5 h GPU) |
| opinia o `AGENTS/phases/phase-0/katalog-metod.md` | wybór metod klasycznych |

## Odłożone pytania

- klasyfikator kodu: „future research” (@phase-2:K33).

## Ostatnia sesja

2026-10-30 14:14: decyzje K31–K38 (wszystkie A). Przygotowany kod i kontener (bez GPU), sprawdzenia na CPU i na rozwiązaniach wzorcowych; pytanie K39 o uruchomienie; opis @T013.
