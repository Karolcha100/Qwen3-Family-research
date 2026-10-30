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
14. **Zerwane połączenie przy pobieraniu z Hugging Face może zawiesić proces bez błędu** (wiszące gniazdo), a w cache zostają pliki `.incomplete`. Objaw: proces nic nie robi, a w snapshocie modelu brakuje `model.safetensors`. Pobieranie uruchamiaj z `HF_HUB_DOWNLOAD_TIMEOUT=60` i sprawdzaj, czy wagi są w cache, zanim zaczniesz konwersję. *(2026-10-29, Claude Opus 5.5)*
15. **`.float()` obcina float64 do float32.** W teście w float64 dokładna KL wyszła szumem i przybliżenie Fishera wyglądało na zepsute (korelacja 0,03, stosunek 0,13). Po zamianie na `at_least_float32` (promocja, nie rzutowanie) korelacja wynosi 0,994. Zawsze `tensor.to(torch.promote_types(tensor.dtype, torch.float32))`. *(2026-10-29, Claude Opus 5.5)*
16. **Godzina w podpisie wpisu wieloetapowego:** jeśli między `date` a zapisem wpisu mija kilka kroków, sprawdź `date` jeszcze raz tuż przed zapisem (21:51 zamiast 21:49 w dyskusji planu Phase 2). *(2026-10-29, Claude Opus 5.5)*
17. **bf16 nie nadaje się do pomiaru skutku pojedynczego neuronu.** Szum numeryczny bf16 (KL kontrolna 1,3e-3, bo wsad 8 vs 1 zmienia zaokrąglenia) jest 100× większy niż typowy skutek (1,3e-5). Do zaburzeń używaj float32 bez TF32, a w każdym nowym pomiarze dodawaj kontrolę „skala 1”. *(2026-10-29, Claude Opus 5.5)*
18. **`pkill -f wzorzec` zabija też własną powłokę**, jeśli jej polecenie zawiera ten wzorzec (exit 144). Zatrzymuj procesy po PID (`echo $!` przy starcie, zapis do pliku). *(2026-10-29, Claude Opus 5.5)*
19. **Heredoc bez cudzysłowu (`<<EOF`) rozwija `$` w TeX-u.** `$1{,}3$` traci `$1`, a `$-2` staje się flagami powłoki (`569JXkl2`); tak zepsuła się tabela w @T010 (naprawiona 2026-10-30 01:40). Treści dla autora zapisuj przez `<<'EOF'` albo narzędziem Write, a po zapisie `grep -nP '(^|[\s|(])\{,\}'`. *(2026-10-30, Claude Opus 5.5)*
20. **Przesiew Fishera w float32 przez `logits` → OOM** (2048 × 151 936 × 4 B w grafie, kilka kopii). Gradient po stanie końcowym liczony jawnie: $W_y - \sum_v p_v W_v$, bez grafu przez logity; 10 s na 4096 tokenów × 16 próbek. *(2026-10-30, Claude Opus 5.5)*
21. **Obrazek ze ścieżką względną (`![x](figures/a.png)`) się w GUI nie pokazuje**, a `|` we wzorze w tabeli rozcina komórkę. Tak wyglądały raporty etapów 1–4 Phase 2 (naprawione 2026-10-30). Ścieżki zawsze `AGENTS/…`, w tabelach `\lvert a \rvert`, `$$` bez wcięcia. Przed oddaniem raportu: zrzut z `python -m agents_board --static plik.html` + `firefox --headless --screenshot`. *(2026-10-30, Claude Opus 5.5)*
22. **W transformers ostatni element `hidden_states` (indeks 28 w Qwen3-0.6B) ma już nałożoną końcową normalizację**, a pozostałe nie. Cel „wyjście warstwy ℓ+1” brany jako `hidden_states[ℓ+2]` jest więc zły dla ℓ = 26 (norma ~76 zamiast ~935); warstwa 26 po treningu dawała KL ~1,1. Wyjście konkretnej warstwy przechwytuj hookiem na tej warstwie. Objaw do sprawdzania: błąd okna przed treningiem ≫ 1 (było 18). *(2026-10-30, Claude Opus 5.5)*
