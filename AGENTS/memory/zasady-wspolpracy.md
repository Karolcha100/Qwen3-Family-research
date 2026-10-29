# Zasady współpracy z autorem

Skrót ustaleń. Pełne brzmienie: `AGENTS/todo/llm/INSTRUKCJA.md`, `AGENTS/README.md`, `AGENTS/talk/od-autora-dla-llmow.md`.

*Szablon z projektu economics-model-pol-vs-rus, 2026-10-29*

---

## Cykl pracy

1. Autor odpowiada w GUI (`python3 -m agents_board`) i klika **✅ Koniec**. Powstaje `AGENTS/talk/koniec/RRRR-MM-DD-GGMM.md` z listą jego działań, a do schowka trafia prompt.
2. Autor wkleja w czacie: „Odpowiedziałem w AGENTS board. Podsumowanie: AGENTS/talk/koniec/… Przeczytaj je i kontynuuj według AGENTS/todo/llm/INSTRUKCJA.md.”
3. Agent czyta plik Koniec i **tylko pliki zmienione od ostatniego briefingu** (`git status`, `git diff`). Nie czyta wszystkiego od nowa.
4. Agent odpowiada:
   - w wątkach — wpis na końcu wątku;
   - w raporcie autora — blok „🤖 ODPOWIEDŹ LLM”, jeden na zadanie;
   - w planach — wpis w sekcji `## Dyskusja`;
   - aktualizuje TODO, raport agentów, plany i pamięć.
5. Na koniec: **briefing** `AGENTS/talk/briefings/RRRR-MM-DD-GGMM.md` z tą samą treścią co odpowiedź w czacie, potem **commit**.

## Kanały, w których autor może pisać

Tylko przez GUI: Decyzja w pytaniu, odpowiedź końcowa w pytaniu 🔄, raport autora i status zadania, wątki, dyskusja planu, uwagi dla LLM, Koniec. Do tego czat. **Inne pliki są dla niego tylko do czytania** — nigdy nie pisz „odpowiedz w pliku X”. Tabela: `AGENTS/todo/llm/INSTRUKCJA.md`, sekcja „Gdzie autor może odpisywać”.

## Odpowiedź w czacie

Tylko dwie części (ta sama treść idzie do briefingu):

- **Zmiany:** linki do plików z oznaczeniem CRE / MOD / DEL;
- **Do odpowiedzi:** miejsce w drzewie GUI (np. „Co czeka na mnie → Wątki — agent odpowiedział → @T003”) i bardzo krótki opis.

Reszta treści trafia do plików w `AGENTS/`.

## Stałe reguły

- **Commit po każdym prompcie autora:** sensowny opis, bez pushowania.
- **Decyzje zawsze jako pytania w `AGENTS/phases/<faza>/agents-issues-N.md`, każda osobno** (`### K1. …` z opcjami, rekomendacją i polem Decyzja), a nie jako lista pytań w wątku. Autor **chce dużo pytań**, także o drobne decyzje, które teraz nie mają znaczenia, ale mogą mieć 200 decyzji dalej. Lepiej zapytać niż przyjąć coś po cichu. Wątek służy do rozmowy i opinii (źródło: @T001, 2026-10-29). Pytania organizacyjne, niezwiązane z jedną fazą, trafiają do `AGENTS/phases/phase-0/`.
- **Polecenia dla autora zawsze w blokach kodu** (` ```bash … ``` `, każde w osobnej linii), nigdy w tekście w pojedynczych backtickach (uwaga 1 w `AGENTS/talk/od-autora-dla-llmow.md`).
- **„Co ty na to?”, „co sądzisz?”, „jak widzisz?”** to pytanie o opinię: plusy, minusy, rekomendacja — **nic nie uruchamiasz**. Działasz dopiero po „zgoda”, „robimy”, „start”.
- **Każdy plik dla autora zaczyna się od „## Co masz zrobić”:** problem prostymi słowami i pytanie z gotowymi opcjami (np. „wystarczy: zgoda, B”).
- **Jeden plik na zadanie** (plan, raport, propozycja), podlinkowany w zadaniu. Plik zbiorczy tylko jako spis.
- **Podpis:** `*RRRR-MM-DD GG:MM — <model>*`, godzina zawsze z `date "+%Y-%m-%d %H:%M"` tuż przed podpisem, nigdy szacowana.
- **Wątki:** wpisy rozdzielone **trzema** liniami `---`; każdy wpis kończy się podpisem, a po nim są trzy linie `---`.
- **Nie edytujemy cudzych ani wcześniejszych wpisów** (wątki, raporty, decyzje). Wyjątek: naprawa ewidentnych uszkodzeń, z adnotacją.
- **Wzory w TeX:** w tekście `$…$`, osobno `$$…$$`, nie w blokach kodu. Kwoty pisz „0,5 $” (spacja przed `$`).
- **Język:** komunikacja i pliki w `AGENTS/` po polsku; kod, nazwy plików i `README.md` projektu po angielsku (chyba że autor zdecyduje inaczej). Nazwy plików bez polskich znaków.
- **Pliki tymczasowe agentów** tylko w katalogu tymczasowym sesji (scratchpad), nigdy w repozytorium.

## Styl autora

- Krótkie odpowiedzi w GUI („zgoda”, „tak”, „B”). Gdy pisze ogólnie („rozpisz mi…”), agent proponuje opcje z rekomendacją.
- Ceni, gdy agent przyznaje się do błędu i od razu go naprawia.
- Nie lubi szukać, na co ma odpowiedzieć — pytanie zawsze na górze, z opcjami.

*Zmiana: 2026-10-29 — reguła: decyzje jako osobne pytania w agents-issues, pytamy dużo (@T001) — Claude Opus 5.5*
*Zmiana: 2026-10-29 — polecenia dla autora w blokach kodu (uwaga 1) — Claude Opus 5.5*
