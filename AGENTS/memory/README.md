# Pamięć projektu — spis

Wiedza, która ma przetrwać między sesjami agentów: stan projektu, ustalenia z autorem i błędy, których nie powtarzamy. Szczegóły są w podlinkowanych plikach źródłowych; tu jest tylko to, co trzeba wiedzieć od razu.

*Szablon, 2026-10-29*

---

## Co masz zrobić

Nic do decyzji. Przejrzyj, jeśli chcesz, i popraw albo napisz w wątku, jeśli agent zapamiętał coś źle.

## Pliki

| Plik | O czym |
|---|---|
| `AGENTS/memory/stan-projektu.md` | gdzie jesteśmy, co dalej, otwarte decyzje |
| `AGENTS/memory/zasady-wspolpracy.md` | jak pracujemy z autorem: cykl pracy, format odpowiedzi, commity, podpisy |
| `AGENTS/memory/pulapki.md` | błędy, które już się zdarzyły, i jak ich unikać |

## Zasady dla agentów

- **Czytaj na początku sesji**, zaraz po `AGENTS/README.md` (krok 0 w `AGENTS/todo/llm/INSTRUKCJA.md`).
- **Aktualizuj na końcu sesji**, gdy zmieniło się coś ważnego: nowa decyzja autora, nowy etap, nowa pułapka. Zmieniasz treść na aktualną, bo to pamięć, a nie dziennik — historia jest w raportach, wątkach i git. Na dole pliku dopisz linię `*Zmiana: data — co — model*`.
- Jeden temat = jeden plik. Nowy temat → nowy plik + wiersz w tabeli wyżej (np. `dane-konwencje.md` dla ustaleń o danych projektu).
- Gdy pamięć i plik źródłowy się różnią, **wygrywa plik źródłowy** (decyzje w `agents-issues-*.md`, wątki, `INSTRUKCJA.md`). Wtedy popraw pamięć.
