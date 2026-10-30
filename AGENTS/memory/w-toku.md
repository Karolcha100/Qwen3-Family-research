# Praca w toku — notatnik bieżącego zadania

Co agent robi **teraz**, w którym kroku jest i co dalej. Aktualizowany w trakcie dłuższych zadań, nie tylko na końcu sesji, żeby po końcu kontekstu albo dłuższej przerwie dało się wrócić dokładnie w to miejsce. Zasady: `AGENTS/memory/procedury.md`, sekcja 7.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Teraz

- Nic się nie liczy (GPU wolne od 04:30). **@L13 zrobione** w nocy 29/30.10: raporty `AGENTS/phases/phase-pomysl/etap-1-pilot.md` … `etap-4-jedna-warstwa.md`, wyniki `results/phase2/`, nocny przebieg @T010 (wpisy 22:09, 22:10, 02:06).
- Dane poza repo: `~/qwen3-checkpoints/phase2/` (`measurement-set.pt`, `training-set.pt`, `layer-13-pairs/` 4 GB).
- Powtórka etapu 4 dla innej warstwy: `uv run --no-sync python scripts/phase2_stage4_one_layer.py --layer N --measurement-sequences 0 1 2 3 4 5 6 7` (ℓ ≤ 25), wykres: `scripts/phase2_stage4_analysis.py --layer N`.

## Na co czekam (co odblokuje pracę)

| Czekam na | Odblokuje |
|---|---|
| K25–K30 (`AGENTS/phases/phase-pomysl/agents-issues-4.md`): model ma dobrze programować | wybór danych mapy i naprawy (kod/tekst), pomiar programowania, języki, model odniesienia, powtórka etapu 4 pod kod (K30) |
| K16–K24 (`AGENTS/phases/phase-pomysl/agents-issues-3.md`) | dalsze kroki Phase 2 (K21 warstwy, K23 trening, K19 nazwa folderu, K22 → @L14 GUI) |
| opinia o `AGENTS/phases/phase-0/katalog-metod.md` | wybór metod klasycznych |

## Odłożone pytania

- brak (proporcje tekstu pomiarowego zadane jako @phase-pomysl:K11).

## Ostatnia sesja

2026-10-30 10:43: odpowiedź w dyskusji `etap-2-mapa.md` (autor: wykresy w sekcji 5; „żeby Qwen jak najlepiej programował”). Sekcja 3 i 5 z osobnymi wykresami; analiza CPU `scripts/phase2_code_text_maps.py`: obecna mapa 75/25 szkodzi kodowi ~1,75× bardziej niż mapa pod kod (na odłożonych sekwencjach); pytania K25–K30. Starsze `raport-1`, `raport-2` w zakładce Raporty (@T010: „tak”). Autor jeszcze czyta raporty.
