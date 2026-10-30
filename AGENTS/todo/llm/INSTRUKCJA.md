# Instrukcja dla agentów LLM (Claude Code)

*Szablon z projektu economics-model-pol-vs-rus, 2026-10-29. Agenci mogą ten plik ulepszać (z podpisem i datą zmiany na dole).*

Autor rozmawia z Tobą głównie przez pliki w `AGENTS/` i przeglądarkowe GUI `python3 -m agents_board`. Ten plik mówi, co czytać, gdzie odpowiadać i jakich formatów pilnować, żeby autor widział Twoje odpowiedzi w GUI.

---

## Typowy prompt autora

> Odpowiedziałem w AGENTS board. Podsumowanie: AGENTS/talk/koniec/RRRR-MM-DD-GGMM.md (N pozycji). Przeczytaj je i kontynuuj według AGENTS/todo/llm/INSTRUKCJA.md.

Wtedy przejdź kroki z sekcji „Na początku każdej sesji”, odpowiedz na wszystko z pliku Koniec, wykonaj to, na co autor się zgodził, i zakończ sesję jak w sekcji „Koniec sesji”.

## Na początku każdej sesji (w tej kolejności)

0. **`AGENTS/README.md`** (mapa), potem **`AGENTS/memory/`** (zacznij od `README.md`): **praca w toku (`w-toku.md`)**, stan projektu, indeks decyzji, zasady współpracy, procedury, pułapki.
1. **`AGENTS/talk/od-autora-dla-llmow.md`**: przeczytaj nowe uwagi i oznacz każdą jako przeczytaną, dopisując na końcu jej linii `— *przeczytane: RRRR-MM-DD (model)*`. Poza tym w tym pliku **nic nie piszesz**.
2. **`AGENTS/plan/phases-plans.md`**: na jakim etapie jest projekt.
3. **Najnowszy plik w `AGENTS/talk/koniec/`** (jeśli jest nowszy niż Twój ostatni briefing): lista tego, na co autor odpowiedział — od tego zaczynasz. **Mimo to sprawdź pliki zmienione od ostatniego briefingu** (`git status`, `git diff`) i przeczytaj je — lista z Konca bywa niepełna (autor pisze też w VS Code).
4. **`AGENTS/todo/author/raport-TODO-autora.md`**: nowe wpisy autora. Na każdy odpowiedz blokiem LLM (format niżej).
5. **`AGENTS/talk/threads/`**: wątki, w których ostatni wpis jest od autora. Odpowiadasz w tym samym wątku.
6. **Plany** (pliki z linią `**Status planu:**`): nowe wpisy autora w `## Dyskusja`, zatwierdzenia.
7. Najnowsze pola **Decyzja** w `AGENTS/phases/*/agents-issues-N.md`.
8. **`AGENTS/todo/llm/TODO-dla-LLM.md`**: otwarte zadania.

## Koniec sesji (zawsze, w tej kolejności)

1. **Odpowiedzi** we wszystkich miejscach, na które autor czekał (wątki, raport autora, dyskusje planów, propozycje końcowe w pytaniach).
2. **TODO i raport:** statusy zadań `L…`, nowe zadania `A…` dla autora, wpisy w `raport-TODO-LLM.md`, plan faz.
3. **Pamięć:** popraw `AGENTS/memory/*.md`, jeśli zmieniło się coś ważnego; zawsze zaktualizuj `w-toku.md` i odśwież `decyzje.md` (`AGENTS/memory/procedury.md`, sekcja 6).

**W trakcie dłuższych zadań** (instalacja, budowa, eksperyment) aktualizuj `AGENTS/memory/w-toku.md` po każdym ukończonym kroku, a nie dopiero na końcu sesji. Kontekst może się skończyć w połowie pracy.
4. **Briefing:** `AGENTS/talk/briefings/RRRR-MM-DD-GGMM.md` (godzina z `date`) z **tą samą treścią** co odpowiedź w czacie. Nagłówek np. `# Briefing RRRR-MM-DD GG:MM — temat`.
5. **Commit** z sensownym opisem, potem **`git push`** — po każdym prompcie autora (decyzja @phase-0:K17 = B). Jeśli push się nie uda, napisz to w briefingu i podaj autorowi polecenie w bloku kodu.
6. **Odpowiedź w czacie** — tylko dwie części:
   - **Zmiany:** pliki jako linki markdown z oznaczeniem **CRE / MOD / DEL** (utworzony / zmieniony / usunięty);
   - **Do odpowiedzi:** rzeczy dla autora z miejscem w drzewie GUI (np. „Co czeka na mnie → Wątki — agent odpowiedział → @T003”) i bardzo krótkim opisem.

   Reszta treści trafia do plików w `AGENTS/`.

## Gdzie autor może odpisywać

Autor pisze **tylko przez GUI** (albo w czacie). Prosząc go o odpowiedź, zawsze wskaż jeden z tych kanałów i miejsce w drzewie, które naprawdę istnieje — w razie wątpliwości sprawdź `renderTree()` w `agents_board/static/index.html`.

| Kanał | Plik | „Co czeka na mnie” |
|---|---|---|
| Decyzja w pytaniu (❓ otwarte, 🤖 propozycja) | `AGENTS/phases/<faza>/agents-issues-N.md` | Pytania bez decyzji |
| Odpowiedź końcowa w pytaniu 🔄 | to samo pytanie, Decyzja `⏳ w toku` | Pytania w toku (przeniesione do zadań) |
| Wpis w raporcie + status zadania A | `AGENTS/todo/author/raport-TODO-autora.md`, `AGENTS/todo/author/*-TODO-dla-autora.md` | Twoje zadania (otwarte) |
| Wątek: odpowiedź, nowy, 🔒 | `AGENTS/talk/threads/T…md` | Wątki — agent odpowiedział; ➕ Nowy wątek |
| Dyskusja i zatwierdzenie planu | plik z linią `**Status planu:**` | Plany do zatwierdzenia i opinii (też Drzewo → Plany) |
| Dyskusja o raporcie z wynikami, 🔒 | plik z linią `**Status raportu:**` | Raporty do przeczytania i dyskusji (też Drzewo → Raporty) |
| Uwaga dla agentów | `AGENTS/talk/od-autora-dla-llmow.md` | Uwagi dla LLM |
| Koniec + uwaga | `AGENTS/talk/koniec/…md` | przycisk ✅ Koniec |

**Wszystkie inne pliki są dla autora tylko do czytania.** Nie pisz „odpowiedz w pliku X”. Jeśli plik wymaga rozmowy, zrób z niego plan (niżej) albo podlinkuj go w zadaniu A — wtedy jego treść jest widoczna w zadaniu.

## Numeracja i statusy zadań

- Zadania agentów: **L…** w `AGENTS/todo/llm/TODO-dla-LLM.md`. Zadania autora: **A…** w `AGENTS/todo/author/` (WAŻNE / ŚREDNIE / MAŁE). Nowe zadanie dostaje kolejny wolny numer (sprawdź najwyższy we wszystkich plikach). Numerów nie używamy ponownie.
- Statusy: `[ ]` do zrobienia, `[~]` w toku, `[x]` zrobione, `[?]` zablokowane (napisz na co), `[>]` przeniesione (napisz dokąd), `[-]` porzucone (napisz dlaczego).
- **Niczego nie usuwasz**, zmieniasz tylko literę i dopisujesz krótką notkę.

### Jak wziąć i zamknąć zadanie L

1. Biorąc zadanie: `[~]` + `*(w toku: model, RRRR-MM-DD GG:MM)*`.
2. Po wykonaniu: `[x]` + `*(zrobione: RRRR-MM-DD GG:MM, raport: raport-TODO-LLM.md)*`.
3. W `AGENTS/todo/llm/raport-TODO-LLM.md` dopisz wpis:
   ```
   ### [L6] tytuł

   - co zrobiono, gdzie są pliki, jak sprawdzono (testy),
   - co zostało / nowe problemy (→ nowe L… albo A…, albo agents-issues),

   *RRRR-MM-DD GG:MM — model*

   ---
   ```
4. Jeśli zadanie wymaga decyzji autora: status `[?]` i pytanie w `agents-issues-N.md` albo nowe zadanie A….

## Odpowiedzi w raporcie autora

**Jeden blok odpowiedzi = jedno zadanie**: GUI pokazuje przy zadaniu tylko jego blok. Nie edytujesz tekstu autora (wyjątek: miejsce, które autor wyraźnie zostawił do uzupełnienia). Odpowiedź dopisujesz pod jego wpisem:

```
---

> 🤖 **ODPOWIEDŹ LLM — początek** (model)
>
> ### [A2] Re: tytuł
>
> treść…
>
> *przeczytane i odpowiedziane: RRRR-MM-DD GG:MM — model*
>
> 🤖 **ODPOWIEDŹ LLM — koniec**

---
```

Odpowiedź na pytanie przeniesione do raportu ma identyfikator pytania, np. `### [phase-1:K1] Re: tytuł`.

## Wątki (`AGENTS/talk/threads/T001-….md`)

- Jeden temat = jeden plik. Nagłówek `# T001 · tytuł`, potem wpisy oddzielone trzema liniami `---`.
- **Wpis agenta:** treść, pusta linia, podpis `*RRRR-MM-DD GG:MM — model*` jako **ostatnia linia**, pusta linia, `---` ×3. Wcześniejszych wpisów nie edytujesz.
- Po podpisie GUI rozpoznaje, że wpis jest od agenta (słowa Claude/GPT/Gemini/LLM/model po myślniku). Wpisy autora kończą się podpisem `— Autor*`.
- **Nowy temat od agenta:** nowy plik z kolejnym numerem T i nagłówkiem jak w `agents_board/model.py` (`thread_header`). Odgałęzienie: linia `*Odgałęzienie od: T002*` pod tytułem.
- Wątek jest **zamknięty**, gdy któryś wpis zaczyna się od `🔒`. W zamkniętym wątku nie odpowiadasz; zamykasz tylko na wyraźne życzenie autora.
- **Wzmianki:** `@T002` (wątek), `@A12` / `@L3` (zadanie), `@phase-1:K1` (pytanie w fazie). GUI robi z nich linki i krawędzie grafu. Używaj ich w wątkach, raportach i briefingu.

## Plany do zatwierdzenia i opiniowania

- **Plan** to dowolny plik w `AGENTS/` (poza `talk/` i `todo/`) z linią `**Status planu:** do zatwierdzenia` albo `**Status planu:** do opiniowania` pod nagłówkiem i podpisem (linia od początku wiersza). GUI pokazuje go w „Plany do zatwierdzenia i opinii” oraz w Drzewo → Plany.
- **Rozmowa** toczy się w ostatniej sekcji `## Dyskusja`; wpisy jak w wątkach. Jeśli zmieniasz treść planu, napisz w dyskusji, co zmieniłeś. Plan czeka na autora, gdy ostatni wpis jest od agenta (albo dyskusji jeszcze nie ma).
- **Status `zatwierdzony (…)`** ustawia autor przyciskiem ✅ Zatwierdzam plan. Agent go nie ustawia. Po zatwierdzeniu agent wykonuje plan.
- Plan do zatwierdzenia nie potrzebuje osobnego zadania A.

## Raporty z wynikami

- **Raport** (wyniki etapu, eksperymentu, analizy) to plik w `AGENTS/` (poza `talk/` i `todo/`) z linią `**Status raportu:** do przeczytania` pod nagłówkiem i podpisem. GUI pokazuje go w „Raporty do przeczytania i dyskusji” oraz w Drzewo → Raporty.
- **Rozmowa** jak w planie: sekcja `## Dyskusja` na końcu, wpisy jak w wątkach. Raport czeka na autora, gdy ostatni wpis jest od agenta (albo dyskusji jeszcze nie ma).
- **Status `zamknięty (…)`** ustawia autor przyciskiem 🔒 Zakończ dyskusję. Agent go nie ustawia.
- **Wykresy:** raport z liczbami ma wykresy pokazujące główne wyniki, każdy z 1–2 zdaniami „co widać”.

## Pytania do autora (`AGENTS/phases/<faza>/agents-issues-N.md`)

- Sekcja `### K1. 🔴 tytuł` z **Problemem**, **Opcjami**, **Rekomendacją** i pustym polem `- **Decyzja:**`. Przykład: `AGENTS/phases/README.md`.
- Pytanie z Decyzją `⏳ w toku → @A43` to sprawa przeniesiona do zadania: rozmowa toczy się pod zadaniem, odpowiadasz w raporcie autora.
- `- **Propozycja końcowa:** (czeka na agenta)` = autor prosi o propozycję końcową: zastąp `(czeka na agenta)` swoją propozycją (zwięzłą, tak by mogła stać się decyzją). Autor ją akceptuje (Decyzja `✅ …`) albo odrzuca (`❌ …`).
- Pola Decyzja `⏳ …` nie zmieniasz; `✅ …` wpisuje autor.

## Konwencje, na których opiera się GUI (`agents_board`)

Nie zmieniaj ich bez zmiany `agents_board/model.py` i testów `tests/test_agents_board.py`:
- zadanie: `- [ ] **A12. tytuł** reszta…` (linie kontynuacji wcięte spacjami);
- pytanie: `### W1. 🔴 tytuł` … `- **Decyzja:**` (pole puste = czeka na autora), tylko w `AGENTS/phases/<faza>/agents-issues-N.md`;
- raport autora: wpisy `### [A13] tytuł`;
- wątek: `# T001 · tytuł`, wpisy oddzielone `---` ×3, podpis jako ostatnia linia wpisu;
- plan: linia `**Status planu:** …` i sekcja `## Dyskusja`;
- raport z wynikami: linia `**Status raportu:** …` i sekcja `## Dyskusja`;
- briefing i Koniec: `AGENTS/talk/briefings/RRRR-MM-DD-GGMM.md`, `AGENTS/talk/koniec/RRRR-MM-DD-GGMM.md`.

## Ustalenia, które obowiązują zawsze

- **Godzina w podpisie zawsze z `date "+%Y-%m-%d %H:%M"`**, uruchomionego tuż przed podpisem, nigdy szacowana.
- **Pytania o opinię** („Co ty na to…?”, „jak widzisz…?”, „co sądzisz…?”) to nie zgoda na działanie. Odpowiadasz plusami, minusami i rekomendacją, możesz dodać zadanie A z decyzją, i niczego nie uruchamiasz, dopóki autor wyraźnie nie zdecyduje („robimy”, „zgoda”, „wybieram…”).
- **Każdy plik dla autora zaczyna się od sekcji `## Co masz zrobić`:** jednym-dwoma zdaniami problem prostymi słowami, potem pytanie albo decyzja z gotowymi opcjami (np. „wystarczy: tak, B”). Szczegóły techniczne dopiero niżej. To samo w blokach odpowiedzi.
- **Jeden plik na zadanie:** plan, raport albo propozycja dla konkretnego zadania lub pytania to osobny plik w folderze fazy, podlinkowany w zadaniu. Plik zbiorczy tylko jako spis z linkami.
- **Ścieżki plików** zawsze w backtickach i pełne od katalogu projektu (np. `AGENTS/phases/phase-1/plan.md`) — GUI robi z nich linki; w czacie jako linki markdown `[nazwa](ścieżka)`.
- **Obrazki i wykresy:** plik `.png`/`.svg` w `AGENTS/`, w tekście `![opis](AGENTS/…/x.png)` — GUI go pokazuje. **Ścieżka zawsze pełna od `AGENTS/`**; względna (`figures/x.png`) się nie wyświetla. Sprawdź wykres (otwórz plik), zanim go wstawisz.
- **Wzory w TeX:** w tekście `$…$`, osobno `$$…$$`, nie w blokach kodu. GUI je składa (KaTeX). Kwoty pisz ze spacją przed `$` („0,5 $”). **W tabelach nie używaj `|` we wzorach** (`\lvert a \rvert` zamiast `|a|`, `\Vert` zamiast `\|`), a `$$…$$` pisz bez wcięcia, poza listą, z pustą linią przed i po.
- **Dopisywanie do pliku:** najpierw `s = open(p).read()`, potem osobno `open(p, "w").write(…)`. Nigdy `open(p, "w").write(open(p).read() …)` — tryb `"w"` czyści plik przed odczytem. Po zapisie `git diff --stat`.
- **Heredoki z `$`** (TeX, kwoty) zawsze w formie `<<'EOF'`.
- **Pliki tymczasowe** tylko w katalogu tymczasowym sesji, nigdy w repozytorium.
- **Język:** komunikacja z autorem i pliki w `AGENTS/` po polsku; kod i nazwy plików po angielsku (chyba że projekt ustali inaczej — patrz `AGENTS/memory/zasady-wspolpracy.md`).

## Praca wielu agentów naraz (subagenci)

1. **Prompt w pliku,** agent dostaje tylko „przeczytaj i wykonaj”. Prompt zapisz potem w folderze fazy.
2. **Wynik do CSV o ustalonych kolumnach,** który koordynator czyta skryptem. Raporty tekstowe agentów trudno zebrać.
3. **Jedna reguła = jeden agent** (albo jedna lista przypadków), zamiast wielu agentów, z których każdy robi po swojemu.
4. **Każde ograniczenie ma ścieżkę dla wyjątków:** „nie zmieniaj X” zawsze razem z „zgłoś kandydata do pliku Y”.
5. **Pilot na różnych przypadkach** przed pełną falą; **krok koordynatora** po fali w planie fazy.
6. **Agent recenzujący nie zapisuje danych** — zapis robi koordynator.
*Zmiana: 2026-10-29 16:54 — notatniki agenta (w-toku, decyzje, procedury), @T006 — Claude Opus 5.5*
