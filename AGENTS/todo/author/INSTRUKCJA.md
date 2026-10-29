# Instrukcja TODOs — dla autora

*Ten plik możesz dowolnie edytować. Agenci go czytają, ale nie zmieniają. Szablon: 2026-10-29*

---

## Najprościej: przez GUI

Uruchom `python3 -m agents_board` w folderze projektu. Wszystko poniżej robisz kliknięciami („Co czeka na mnie”), a GUI zapisuje to do plików. Gdy skończysz, kliknij **✅ Koniec** i wklej skopiowany prompt w czat Claude Code.

## Pliki

| Plik | Co tam jest | Kto pisze |
|---|---|---|
| `WAZNE-TODO-dla-autora.md` | zadania, które blokują agentów | agenci dodają, Ty odhaczasz |
| `SREDNIE-TODO-dla-autora.md` | ważne, ale nie blokują | j.w. |
| `MALE-TODO-dla-autora.md` | drobiazgi | j.w. |
| `raport-TODO-autora.md` | Twoje odpowiedzi do zadań `A…` + odpowiedzi agentów | Ty; agenci dopisują oznaczone bloki |

Zadania dla agentów są w `AGENTS/todo/llm/`.

## Numeracja

- Twoje zadania: **A1, A2, A3…**, jedna numeracja dla wszystkich trzech plików.
- Numer nie zmienia się, gdy zadanie przechodzi do innego priorytetu, i nigdy nie jest używany ponownie.
- Zadania agentów mają osobną numerację: **L1, L2…**.

## Statusy (litera w nawiasie)

| Zapis | Znaczenie |
|---|---|
| `[ ]` | do zrobienia |
| `[~]` | w toku |
| `[x]` | zrobione |
| `[?]` | czeka na odpowiedź / zablokowane (dopisz na co) |
| `[>]` | przeniesione do innego pliku (dopisz dokąd, np. `[>] → MALE`) |
| `[-]` | porzucone (dopisz krótko dlaczego) |

Zadań **nie usuwamy**, tylko zmieniamy literę.

## Jak odpowiadać ręcznie (bez GUI)

1. W `raport-TODO-autora.md` dodaj wpis:
   ```
   ### [A7] tytuł zadania

   treść…

   *RRRR-MM-DD GG:MM — Autor*

   ---
   ```
2. Zmień status zadania w pliku WAŻNE / ŚREDNIE / MAŁE.
3. Agent przy następnej sesji przeczyta wpis i odpowie pod nim blokiem „🤖 ODPOWIEDŹ LLM — początek / koniec”, z datą, godziną i podpisem.

## Gdzie jeszcze piszesz

- `AGENTS/talk/threads/`: rozmowy (wątki) — w GUI „➕ Nowy wątek” i „Odpowiedz w wątku”.
- `AGENTS/talk/od-autora-dla-llmow.md`: Twoje ogólne uwagi; agent tylko oznacza je jako przeczytane.
- `AGENTS/phases/phase-*/agents-issues-N.md`: pytania agentów z polami **Decyzja**.
- Pliki z linią `**Status planu:**`: plany do zatwierdzenia (zakładka „Plany”).
