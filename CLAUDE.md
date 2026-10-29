# Komunikacja z autorem przez AGENTS/ (agents_board)

Ten projekt używa struktury `AGENTS/` i GUI `agents_board` do komunikacji autora z Claude Code. Autor odpowiada w przeglądarce (`python3 -m agents_board`), a do Ciebie trafia przez pliki `.md` w `AGENTS/`.

**Pełna instrukcja dla agenta: `AGENTS/todo/llm/INSTRUKCJA.md` — przeczytaj ją na początku każdej sesji i trzymaj się jej.** Mapa folderu: `AGENTS/README.md`. Pamięć projektu: `AGENTS/memory/`.

## Najważniejsze reguły (skrót; szczegóły w INSTRUKCJA.md)

- **Prompt „Odpowiedziałem w AGENTS board. Podsumowanie: AGENTS/talk/koniec/… kontynuuj według AGENTS/todo/llm/INSTRUKCJA.md”:** przeczytaj ten plik Koniec i pliki zmienione od ostatniego briefingu (`git status`, `git diff`), odpowiedz we właściwych miejscach i zakończ sesję jak w INSTRUKCJA.md.
- **Odpowiadasz w plikach, które autor widzi w GUI:** wątki (`AGENTS/talk/threads/`), bloki „🤖 ODPOWIEDŹ LLM” w `AGENTS/todo/author/raport-TODO-autora.md`, sekcje `## Dyskusja` w planach, pola w `AGENTS/phases/*/agents-issues-N.md`. Nigdy nie proś autora, żeby „odpisał w pliku X” spoza listy kanałów w INSTRUKCJA.md.
- **Podpis każdego wpisu:** `*RRRR-MM-DD GG:MM — <Twój model>*` jako ostatnia linia wpisu; godzina zawsze z `date "+%Y-%m-%d %H:%M"`, nigdy szacowana. W wątkach po podpisie trzy linie `---`.
- **Koniec każdej odpowiedzi na prompt autora:**
  1. briefing `AGENTS/talk/briefings/RRRR-MM-DD-GGMM.md` z tą samą treścią co odpowiedź w czacie;
  2. **commit** z sensownym opisem, potem **`git push`** (decyzja @phase-0:K17 = B);
  3. odpowiedź w czacie tylko z dwóch części: **Zmiany** (linki do plików z CRE/MOD/DEL) i **Do odpowiedzi** (miejsce w drzewie GUI + krótki opis).
- **„Co ty na to?”, „co sądzisz?”, „jak widzisz?”** = tylko opinia (plusy, minusy, rekomendacja); niczego nie uruchamiasz bez wyraźnej zgody.
- **Każdy plik dla autora zaczyna się od `## Co masz zrobić`** z pytaniem i gotowymi opcjami.
- **Nie edytujesz wcześniejszych wpisów** (wątki, raporty, decyzje); dopisujesz na końcu.
- **Formaty plików są kontraktem z GUI** (zadania `- [ ] **A12. …**`, pytania `### K1. …` z `- **Decyzja:**`, wątki `# T001 · …`, plany `**Status planu:** …`). Nie zmieniaj ich bez zmiany `agents_board/model.py` i testów `tests/test_agents_board.py`.
- Komunikacja z autorem po polsku.
