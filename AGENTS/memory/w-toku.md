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
| @A6 (w toku, @T008) → @A7 (CUDA 13.4) + @A8 | @L3 budowa llama.cpp (kod już sklonowany) |
| „uruchom” autora | @L4 testy dymne na GPU |
| opinia o `AGENTS/phases/phase-0/plan-metryki-oceny.md` + środowisko | @L7 zestaw 200 pytań |
| **opis głównego pomysłu autora** (nowy wątek) + wybór metod | @L9 weryfikacja bibliotek, @L10 notatki do nauki, plan Phase 2 |

## Odłożone pytania (zadać, gdy autor opisze główny pomysł)

- proporcje mieszanki kalibracyjnej C4 + kod i źródło kodu (@phase-0:K8 = C) — o ile pomysł autora w ogóle używa kalibracji.

## Ostatnia sesja

2026-10-29 19:49: plan Phase 1 zatwierdzony (19:39); odpowiedź w @T008 (123 pakiety przy @A6 to w porządku: +6 nieużywanych zależności, m.in. graficzna Java); llama.cpp sklonowane; raport `AGENTS/phases/phase-0/raport-asvd-svd-llm.md` (prośba z dyskusji katalogu metod). Autor pyta o metody niskiego rzędu, co może być wskazówką do jego głównego pomysłu, ale **nie zakładać** tego.
