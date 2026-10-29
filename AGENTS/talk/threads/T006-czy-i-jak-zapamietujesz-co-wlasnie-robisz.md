# T006 · Czy i jak zapamiętujesz co właśnie robisz?

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Chciałem się spytać, czy oraz jeżeli tak, to jak, zapamiętujesz co właśnie robisz, nad czym pracujesz. Powinieneś mieć wypracowane własną listę TODO, własne instrukcje tego jak obsługiwać rzeczy, jak robić rzeczy oraz jak planować rzeczy - Wraz z własnymi planami etc. etc.

Generalnie chodzi mi o takie notatniki dla ciebie, jeżeli skończy się kontekst albo wrócę po dłuższym czasie.

*2026-10-29 16:53 — Autor*

---
---
---

## Co masz zrobić

Przeczytaj. Na podstawie Twojego wpisu założyłem brakujące notatniki (lista niżej). Jeśli chcesz w nich coś inaczej, napisz tutaj. Jest też jedno drobne pytanie: @phase-0:K43.

---

**Kontekst.** Pytałeś, czy i jak zapamiętuję, nad czym pracuję, i czy mam własne TODO, instrukcje i plany na wypadek końca kontekstu albo Twojego powrotu po dłuższym czasie.

### Jak naprawdę działa moja pamięć

| Sytuacja | Co pamiętam |
|---|---|
| w trakcie jednej rozmowy | wszystko, co jest w kontekście rozmowy |
| kontekst się kończy | Claude Code automatycznie **streszcza** rozmowę i pracuję dalej na streszczeniu, więc szczegóły mogą zginąć |
| nowa sesja (albo wracasz po tygodniu) | **nic poza plikami.** Automatycznie dostaję tylko `CLAUDE.md`, który każe przeczytać `AGENTS/todo/llm/INSTRUKCJA.md` i `AGENTS/memory/` |

Wniosek: **jedyna trwała pamięć to pliki w repo.** Claude Code ma też własny katalog pamięci poza projektem, ale dla tego projektu jest pusty i celowo z niego nie korzystam. `AGENTS/memory/` jest w gicie, widzisz ją w GUI i może ją przeczytać każdy agent.

### Co już było przed Twoim pytaniem

- `AGENTS/memory/stan-projektu.md`: gdzie jesteśmy, decyzje w skrócie, następny krok;
- `AGENTS/memory/zasady-wspolpracy.md`: jak z Tobą pracować (np. „nie zakładaj metod z góry”, „GPU tylko na uruchom”);
- `AGENTS/memory/pulapki.md`: 11 błędów, których nie powtarzamy;
- briefingi: co było w każdej sesji.

### Czego brakowało (masz rację)

1. **Moja lista TODO była prawie pusta.** Było tylko L1, a to, co mam zrobić, gdy coś odblokujesz, istniało jedynie w moim kontekście i w briefingach;
2. **brak zapisu pracy w toku:** gdyby kontekst skończył się w połowie budowy llama.cpp, następna sesja nie wiedziałaby, w którym kroku przerwałem;
3. **brak instrukcji „jak robię rzeczy”:** sposoby dopisywania wpisów, sprawdzania GUI itp. miałem w plikach tymczasowych, które znikają po sesji;
4. **decyzje rozrzucone po 7 plikach** (`agents-issues-1…7.md`): przy każdej sesji trzeba było je zbierać od nowa.

### Co zrobiłem teraz

| Notatnik | Po co |
|---|---|
| `AGENTS/todo/llm/TODO-dla-LLM.md` | **moje TODO:** L2–L11 z tym, na co każde czeka (np. „L3 budowa llama.cpp — czeka na @A7, @A8”) |
| `AGENTS/memory/w-toku.md` | **notatnik bieżącej pracy:** zadanie, zrobione kroki, następny krok, na co czekam. Aktualizowany **po każdym kroku**, nie tylko na końcu sesji |
| `AGENTS/memory/procedury.md` | **moje instrukcje:** start i koniec sesji, gotowe polecenia (wpis do wątku, blok w raporcie, sprawdzenie GUI, indeks decyzji), czego nie mogę zrobić sam. Polecenia sprawdziłem na żywych plikach |
| `AGENTS/memory/decyzje.md` | **indeks decyzji:** K1–K42 w jednej tabeli, generowany z plików pytań |
| plany | już są: plan Phase 1, plan metryk, katalog metod. Moje własne plany pracy to zadania L + `w-toku.md` |

Dodatkowo `AGENTS/todo/llm/INSTRUKCJA.md` mówi teraz, żeby każda sesja zaczynała od `w-toku.md`, a w trakcie dłuższych zadań aktualizowała go po każdym kroku.

### Co się stanie, gdy wrócisz po miesiącu

Nowa sesja czyta `CLAUDE.md` → `INSTRUKCJA.md` → `w-toku.md` (czy coś jest przerwane?) → `stan-projektu.md` i `decyzje.md` (co ustaliliśmy) → `TODO-dla-LLM.md` (co mam do zrobienia i na co czekam) → `procedury.md` (jak to robić). To kilka minut czytania zamiast przekopywania 6 wątków.

*2026-10-29 16:56 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-10-29 19:01 — Autor*

---
---
---
