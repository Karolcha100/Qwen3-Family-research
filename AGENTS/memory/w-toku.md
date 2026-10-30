# Praca w toku — notatnik bieżącego zadania

Co agent robi **teraz**, w którym kroku jest i co dalej. Aktualizowany w trakcie dłuższych zadań, nie tylko na końcu sesji, żeby po końcu kontekstu albo dłuższej przerwie dało się wrócić dokładnie w to miejsce. Zasady: `AGENTS/memory/procedury.md`, sekcja 7.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Teraz

- Nic się nie liczy (GPU wolne od 12:59). **@L18 zrobione** (obliczenia pod nieobecność autora, @T012): raport `AGENTS/phases/phase-2/etap-4b-kod.md`, wyniki `results/phase2/code/`, `results/phase2/k23/`.
- Dane poza repo: `~/qwen3-checkpoints/phase2-code/` (zbiory Python/C4 rozłączne; pary warstw 2, 13, 14, 26 po 4 GB), `~/qwen3-checkpoints/phase2/` (stare, tekst).
- Etap 4 na danych Python: argumenty jak w `results/phase2/code/rerun-26.sh` (zmień `--layer`); wykresy `scripts/phase2_code_stage4_analysis.py`. Cel treningu przechwytywany hookiem (@pulapki 22).

## Na co czekam (co odblokuje pracę)

| Czekam na | Odblokuje |
|---|---|
| K37–K38 (`AGENTS/phases/phase-2/agents-issues-6.md`) | cel treningu na wyjściu modelu; mapa 100% kod |
| K31–K36 (`AGENTS/phases/phase-2/agents-issues-5.md`) | eksperyment ze startem (mapa / losowy / łączenie), testy HumanEval/MBPP/EvalPlus, uruchamianie kodu w podman |
| opinia o `AGENTS/phases/phase-0/katalog-metod.md` | wybór metod klasycznych |

## Odłożone pytania

- brak.

## Ostatnia sesja

2026-10-30 13:01: decyzje K16–K30 wprowadzone (folder `phase-pomysl` → `phase-2`, @L14 etykiety formularzy, raport 3 o ocenie kodu, K31–K36). Pod nieobecność autora (zgoda na GPU ~2 h): K23 (długi trening daje ~5%), dane i mapa kodu, etap 4 dla warstw 13/2/14/26, poprawiony błąd celu dla warstwy 26; pytania K37–K38.
