# Praca w toku — notatnik bieżącego zadania

Co agent robi **teraz**, w którym kroku jest i co dalej. Aktualizowany w trakcie dłuższych zadań, nie tylko na końcu sesji, żeby po końcu kontekstu albo dłuższej przerwie dało się wrócić dokładnie w to miejsce. Zasady: `AGENTS/memory/procedury.md`, sekcja 7.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Teraz

**@L13: Phase 2 — autor (22:07): „uruchom wszystkie etapy, idę spać”.** Plan nocy: @T010 (wpisy 22:09, 22:10, 02:06).
- **Etap 1 gotowy** (01:37): `results/phase2/stage1/`, raport `AGENTS/phases/phase-pomysl/etap-1-pilot.md`. 4096 tokenów → ranking 0,51 (za mało); $\mathrm{KL} \propto \delta^2$.
- **Etap 2:** mapa przesiewu gotowa (64 sekw. × 64 próbki, 21 min): `results/phase2/stage2/fisher-map.pt`, `fisher-summary.json`, raport `etap-2-mapa.md` (sekcja 6 = pomiar dokładny, do dopisania jako nowy wpis).
- **Etap 3 policzony wstępnie** (`results/phase2/stage3/`), bez raportu. Po pomiarze dokładnym etapu 2 uruchomić ponownie (`uv run --no-sync python scripts/phase2_stage3_neuron_kinds.py`; `source-statistics.pt` jest już gotowe) → raport `etap-3-rodzaje-neuronow.md`.
- **Kolejka GPU** `results/phase2/night-chain.sh` (PID 125608, start 02:03): etap 4 `--layer 13 --measurement-sequences 0..7` → potem `phase2_stage2_full_map.py --mode screened` (δ ±1, top 10% + 5% losowych, pomija warstwy 2/13/25). Wyjścia: `results/phase2/night-chain.log`, `stage4/stdout.log`, `stage2/stdout.log`. Oba skrypty wznawiają się same.
- Pytania K16–K22: `AGENTS/phases/phase-pomysl/agents-issues-3.md` (K19 zmiana nazwy folderu dopiero gdy nic nie liczy).
- Dalej: raport etapu 4 → dopisek w etap-2 (sekcja 6) → etap 3 ponownie + raport → briefing, commit, push.

## Na co czekam (co odblokuje pracę)

| Czekam na | Odblokuje |
|---|---|
| **„uruchom etap 1”** od autora | @L13: pilot (~3 h GPU) |
| opinia o `AGENTS/phases/phase-0/plan-metryki-oceny.md` | @L7 zestaw pytań (dopiero Phase 3) |

## Odłożone pytania

- brak (proporcje tekstu pomiarowego zadane jako @phase-pomysl:K11).

## Ostatnia sesja

2026-10-29 21:49: plan Phase 2 zatwierdzony (21:36), plan metryk zatwierdzony (21:37). Napisany kod etapu 1 + testy + zbiór pomiarowy. Czekam na „uruchom etap 1”.
