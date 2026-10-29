# Praca w toku — notatnik bieżącego zadania

Co agent robi **teraz**, w którym kroku jest i co dalej. Aktualizowany w trakcie dłuższych zadań, nie tylko na końcu sesji, żeby po końcu kontekstu albo dłuższej przerwie dało się wrócić dokładnie w to miejsce. Zasady: `AGENTS/memory/procedury.md`, sekcja 7.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Teraz

Brak zadania w toku. @L3 zrobione 20:16 (llama.cpp z CUDA zbudowane w `~/llama.cpp/build/bin`, GPU jeszcze nietestowane).

## Na co czekam (co odblokuje pracę)

| Czekam na | Odblokuje |
|---|---|
| @A8 (uv) — plan Phase 1 zatwierdzony 19:39 | @L2 środowisko Pythona |
| „uruchom” autora (+ @L2 dla części PyTorch) | @L4 testy dymne na GPU (część llama.cpp gotowa) |
| opinia o `AGENTS/phases/phase-0/plan-metryki-oceny.md` + środowisko | @L7 zestaw 200 pytań |
| **opis głównego pomysłu autora** (nowy wątek) + wybór metod | @L9 weryfikacja bibliotek, @L10 notatki do nauki, plan Phase 2 |

## Odłożone pytania (zadać, gdy autor opisze główny pomysł)

- proporcje mieszanki kalibracyjnej C4 + kod i źródło kodu (@phase-0:K8 = C) — o ile pomysł autora w ogóle używa kalibracji.

## Ostatnia sesja

2026-10-29 20:17: @A7 zrobione i sprawdzone (CUDA 13.4.92); @L3 zrobione (llama.cpp z CUDA, nvcc 13.4 przyjął GCC 16). @A8 sprowadza się do `sudo dnf install uv`.
