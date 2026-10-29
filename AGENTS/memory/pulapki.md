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
9. **Polecenia wysyłające dane na zewnątrz (`gh repo create --push`, `git push`) blokuje tryb auto Claude Code**, nawet przy decyzji autora. Nie obchodzimy blokady. Dajemy autorowi gotowe polecenie w zadaniu A (tak powstało @A1), a o stałe pozwolenie pytamy w agents-issues (@phase-0:K17). *(2026-10-29, Claude Opus 5.5)*
10. **Agent nie może sam zmienić swoich uprawnień** (`.claude/settings.json`): tryb auto blokuje to jako „self-modification”, nawet przy decyzji autora (@phase-0:K17). Dajemy autorowi instrukcję w zadaniu A (@A5). *(2026-10-29, Claude Opus 5.5)*
11. **Polecenia z `local-llm-conversation.md` warto sprawdzić na żywym systemie:** `dnf remove 'cuda-*-12-8*'` pomijało 42 pakiety `lib*-12-[89]` i `gds-tools`. Przed podaniem autorowi poleceń z `sudo` sprawdzaj wzorce na `rpm -qa`. *(2026-10-29, Claude Opus 5.5)*
12. **`dnf remove` usuwa też „nieużywane zależności”**, których nie widać w `rpm -qa | grep wzorzec` (przy CUDA 12: nsight, `java-25-openjdk`, czcionki). Przed podaniem autorowi polecenia `dnf remove` uprzedź o tym albo sprawdź pełną listę bez `sudo`: `dnf remove --assumeno …` (działa bez uprawnień, sprawdzone 2026-10-29). *(2026-10-29, Claude Opus 5.5)*
13. **Nazwa briefingu „na zapas”:** dwa razy nazwałem briefing minutą późniejszą niż wynik `date`. Nazwę pliku i nagłówek biorę **z wyniku `date` w tym samym poleceniu**, które tworzy plik (np. `f=AGENTS/talk/briefings/$(date +%Y-%m-%d-%H%M).md`). *(2026-10-29, Claude Opus 5.5)*
