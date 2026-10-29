# Pułapki — błędy, których nie powtarzamy

Każda pułapka: co się stało, jak tego unikać. Agent dopisuje nowe na końcu listy (numeracja ciągła). Pierwsze pochodzą z projektu economics-model-pol-vs-rus.

*Szablon, 2026-10-29*

---

1. **`open(p, "w").write(open(p).read() + …)` czyści plik przed odczytem.** Tak zginęły raporty i wątek. Zawsze najpierw `s = open(p).read()`, potem osobno `open(p, "w").write(…)`. Po zapisie: `git diff --stat` — w dopisanym pliku nie może być usuniętych linii.
2. **Heredoc w powłoce z `$`** (wzory TeX, kwoty) rozwija zmienne. Używaj `<<'EOF'` (w apostrofach), gdy tekst ma być dosłowny.
3. **zsh rozwija `*`** w argumentach (np. `POL:*`) — bierz je w apostrofy.
4. **Godzina w podpisie z głowy** bywała zła. Zawsze `date "+%Y-%m-%d %H:%M"` tuż przed podpisem.
5. **Odpowiedź w miejscu, którego GUI nie pokazuje** (np. blok odpowiedzi z nieznanym identyfikatorem, prośba „odpisz w pliku X”) — autor jej nie widzi. Przed prośbą o odpowiedź sprawdź, że wskazane miejsce w drzewie istnieje (`renderTree()` w `agents_board/static/index.html`).
6. **Lista z pliku Koniec bywa niepełna** (autor dopisuje też w VS Code). Zawsze sprawdź `git status` / `git diff` od ostatniego briefingu.
7. **Zmiana konwencji plików bez zmiany GUI** psuje drzewo (zadania, pytania, wątki). Konwencje: `AGENTS/todo/llm/INSTRUKCJA.md`, sekcja „Konwencje, na których opiera się GUI”.
8. **Duże wyniki wczytywane w całości** potrafią wyczerpać RAM i zamknąć edytor autora. Przy dużych danych czytaj tylko potrzebne kolumny i kawałki.
