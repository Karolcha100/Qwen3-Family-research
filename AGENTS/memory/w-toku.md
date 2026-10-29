# Praca w toku — notatnik bieżącego zadania

Co agent robi **teraz**, w którym kroku jest i co dalej. Aktualizowany w trakcie dłuższych zadań, nie tylko na końcu sesji, żeby po końcu kontekstu albo dłuższej przerwie dało się wrócić dokładnie w to miejsce. Zasady: `AGENTS/memory/procedury.md`, sekcja 7.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Teraz

Brak zadania w toku. @L3 częściowo zrobione: llama.cpp sklonowane do `~/llama.cpp` (commit `eb4e244be`, 2026-10-29, 640 MB); budowa czeka na @A7 i @A8.

## Na co czekam (co odblokuje pracę)

| Czekam na | Odblokuje |
|---|---|
| @A8 (uv) — plan Phase 1 zatwierdzony 19:39 | @L2 środowisko Pythona |
| @A7 (CUDA 13.4; @A6 zrobione 20:04) + @A8 | @L3 budowa llama.cpp (kod już sklonowany) |
| „uruchom” autora | @L4 testy dymne na GPU |
| opinia o `AGENTS/phases/phase-0/plan-metryki-oceny.md` + środowisko | @L7 zestaw 200 pytań |
| **opis głównego pomysłu autora** (nowy wątek) + wybór metod | @L9 weryfikacja bibliotek, @L10 notatki do nauki, plan Phase 2 |

## Odłożone pytania (zadać, gdy autor opisze główny pomysł)

- proporcje mieszanki kalibracyjnej C4 + kod i źródło kodu (@phase-0:K8 = C) — o ile pomysł autora w ogóle używa kalibracji.

## Ostatnia sesja

2026-10-29 20:05: @A6 zrobione i sprawdzone (CUDA 12 usunięta czysto, 208 GB wolnego). Następne: @A7, @A8.
