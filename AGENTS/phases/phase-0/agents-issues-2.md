# Phase 0 — pytania startowe (runda 2): GitHub i system oceny odpowiedzi

*2026-10-29 13:30 — Claude Opus 5.5*

## Co masz zrobić

Nowe decyzje po Twoich odpowiedziach z 13:28: K17 dotyczy GitHuba (@phase-0:K1), a K18–K27 projektu sędziego, czyli modelu nagrody i metryk (@T002). Każde pytanie ma rekomendację, więc wystarczy wpisać „rek” albo literę. Pytania o sędziego nie blokują Phase 1, więc możesz je zostawić na później.

---

### K17. 🟡 Push do GitHuba po sesji

- **Problem:** `CLAUDE.md` mówi „commit bez push”. Teraz jest remote (po @A1). Polecenie wysyłające dane na GitHub zablokowały moje uprawnienia, więc push z mojej strony wymaga reguły w ustawieniach Claude Code.
- **Opcje:**
  - **A** — ja tylko commituję, a push robisz Ty, kiedy chcesz (bez zmian w ustawieniach);
  - **B** — po każdym commicie robię też `git push`. Wtedy dodaję regułę pozwalającą na `git push` w `.claude/settings.json` projektu i zmieniam regułę w `CLAUDE.md`;
  - **C** — push robię tylko na Twoje wyraźne polecenie w danej sesji.
- **Rekomendacja:** A na razie. Repo jest prywatne i tylko Twoje, więc nic nie tracisz, a zachowujesz kontrolę nad tym, co wychodzi z komputera. B ma sens, jeśli chcesz kopię zapasową po każdej sesji.
- **Decyzja:** Opcja B - Po każdym commicie rób też git push.

### K18. 🟡 Z czego składa się sędzia

- **Problem:** „model nagrody” w ścisłym sensie (np. Skywork-Reward-V2) zwraca **jedną liczbę** na odpowiedź, więc nie da 16 osobnych metryk. Szczegóły: @T002.
- **Opcje:**
  - **A** — sam skalarny model nagrody: 1 metryka „ogólna jakość”;
  - **B** — wieloatrybutowy model nagrody (np. ArmoRM: ~19 atrybutów, m.in. pomocność, poprawność, spójność, złożoność, rozwlekłość) + reguły w Pythonie dla metryk 0/1;
  - **C** — hybryda: reguły w Pythonie (metryki 0/1, które da się sprawdzić bez modelu) + model nagrody (ogólna jakość) + sędzia generatywny z rubryką (pozostałe metryki 0–100 i 0/1 wymagające rozumienia);
  - **D** — tylko sędzia generatywny z rubryką, osobno dla każdej metryki.
- **Rekomendacja:** C. Każda metryka idzie do najtańszego narzędzia, które ją dobrze mierzy. Reguły są darmowe i nieomylne, a model nagrody jest szybki. Sędzia generatywny jest wolny (~50 pytań × kilka metryk × każdy wariant modelu), więc zostawiamy mu tylko to, czego reszta nie umie.
- **Decyzja:**

### K19. 🟡 Skala metryk 0–100

- **Problem:** modele-sędziowie słabo rozróżniają 100 poziomów. Ocena „73 vs 76” jest w praktyce losowa, a modele lubią okrągłe liczby (70, 80, 85).
- **Opcje:**
  - **A** — sędzia wprost podaje 0–100;
  - **B** — sędzia podaje 1–10 według rubryki z opisem każdego poziomu, a my przeliczamy na 0–100;
  - **C** — B plus średnia ważona prawdopodobieństwami tokenów oceny (metoda G-Eval): ciągła wartość, stabilniejsza niż jedna wylosowana liczba;
  - **D** — skala 1–5 (jak w Prometheus 2).
- **Rekomendacja:** C. Dostajesz 0–100, które naprawdę coś znaczy, a llama.cpp zwraca logprob tokenów.
- **Decyzja:**

### K20. 🟡 Ocena bezwzględna czy względem BF16

- **Problem:** pytamy, czy zmodyfikowany Qwen jest dobry, ale w badaniu kompresji ważniejsze jest, *o ile pogorszył się względem oryginału*.
- **Opcje:**
  - **A** — tylko bezwzględna (każda odpowiedź oceniana sama);
  - **B** — tylko parami: „czy odpowiedź po kompresji jest gorsza od odpowiedzi BF16 na to samo pytanie?” (win/tie/loss);
  - **C** — obie: bezwzględne metryki dla każdego wariantu + porównanie parami z BF16 jako główna liczba w porównaniu metod.
- **Rekomendacja:** C. Porównanie parami jest czulsze i mniej podatne na bias sędziego. Przy porównaniu parami oceniamy obie kolejności (A/B i B/A), bo sędziowie faworyzują pierwszą odpowiedź.
- **Decyzja:**

### K21. 🟡 Język pytań

- **Problem:** małe Qwen3 (0.6B, 1.7B) słabo radzą sobie po polsku, a sędziowie są uczeni głównie po angielsku. Kwantyzacja zwykle mocniej psuje języki inne niż angielski, co samo w sobie jest ciekawym wynikiem.
- **Opcje:**
  - **A** — tylko angielski;
  - **B** — tylko polski;
  - **C** — angielski jako główny zestaw + ~10 pytań po polsku (te same co część angielskich), żeby mierzyć, czy kompresja psuje polski szybciej.
- **Rekomendacja:** C.
- **Decyzja:**

### K22. 🟡 Skąd wziąć 50 pytań

- **Problem:** pytania decydują, co sędzia w ogóle może zauważyć.
- **Opcje:**
  - **A** — wszystkie piszemy sami;
  - **B** — z gotowych zestawów: MT-Bench (8 kategorii: pisanie, rozumowanie, matematyka, kod, ekstrakcja, STEM, humanistyka, odgrywanie ról), IFEval (instrukcje sprawdzalne regułą, np. „dokładnie 3 punkty”, „odpowiedz w JSON”), Arena-Hard;
  - **C** — mieszanka: ~20 w stylu IFEval (metryki 0/1 sprawdzane regułą), ~20 z kategorii MT-Bench, ~10 własnych z tego, co Cię ciekawi.
- **Rekomendacja:** C. Pytania IFEval dają metryki 0/1 bez sędziego, a MT-Bench ma odpowiedzi wzorcowe do matematyki i rozumowania.
- **Decyzja:**

### K23. 🟢 Liczba pytań

- **Problem:** przy 50 pytaniach różnica między metodami rzędu kilku punktów często mieści się w szumie. Ocena jednej metryki 0/1 na 50 pytaniach ma niepewność około ±7 punktów procentowych.
- **Opcje:**
  - **A** — 50 i koniec;
  - **B** — 50 na start (do ręcznej kalibracji sędziego z Tobą), potem ~150–200 do właściwych porównań;
  - **C** — od razu 200.
- **Rekomendacja:** B. 50 pytań wystarczy, żeby wybrać i sprawdzić sędziego, a 150–200, żeby wiarygodnie porównywać metody kompresji.
- **Decyzja:**

### K24. 🟡 Jak generować odpowiedzi do oceny

- **Problem:** przy losowaniu tokenów (sampling) ten sam model daje różne odpowiedzi, więc różnice między wariantami mieszają się z losowością.
- **Opcje:**
  - **A** — greedy (zawsze najbardziej prawdopodobny token): powtarzalne, ale małe modele częściej wpadają w pętle;
  - **B** — sampling z ustawieniami zalecanymi przez Qwen, 3 odpowiedzi na pytanie, wyniki uśredniane: realistyczne, ale 3× drożej;
  - **C** — greedy do porównań między metodami + B tylko dla wariantów końcowych.
- **Rekomendacja:** C.
- **Decyzja:**

### K25. 🟡 Tryb myślenia Qwen3 przy ocenie

- **Problem:** wersje instrukcyjne Qwen3 mają tryb myślenia (`<think>…</think>`). Z nim odpowiedzi są lepsze, ale dużo dłuższe, a kompresja może psuć samo rozumowanie (pętle, urwane myśli).
- **Opcje:**
  - **A** — myślenie wyłączone (taniej, prościej ocenić);
  - **B** — myślenie włączone;
  - **C** — A jako standard, a B jako osobny eksperyment („czy kompresja psuje rozumowanie bardziej niż odpowiedź?”).
- **Rekomendacja:** C.
- **Decyzja:**

### K26. 🟢 Ręczna kalibracja sędziego

- **Problem:** żeby wiedzieć, czy sędzia ocenia sensownie, trzeba porównać go z oceną człowieka na części odpowiedzi.
- **Opcje:**
  - **A** — oceniasz ręcznie ~50 odpowiedzi (kilka kluczowych metryk, nie wszystkie 16) w prostej lokalnej stronie HTML z przyciskami; wynik zapisuje się do pliku w repo;
  - **B** — to samo w arkuszu CSV;
  - **C** — bez ręcznej kalibracji, wierzymy sędziemu.
- **Rekomendacja:** A, bo zajmie ~30–45 minut. Potem liczymy zgodność (korelacja Spearmana, Cohen κ dla 0/1) i wybieramy sędziego, który najlepiej zgadza się z Tobą.
- **Decyzja:**

### K27. 🟡 Lista 16 metryk

- **Problem:** potrzebny jest zestaw metryk. Szkic 16 metryk (8 typu 0/1 i 8 typu 0–100, z narzędziem do każdej) jest w @T002, w mojej odpowiedzi z 13:30.
- **Opcje:**
  - **A** — szkic zatwierdzony bez zmian;
  - **B** — szkic ze zmianami (napisz w decyzji: usuń / dodaj / zamień);
  - **C** — rozpisz szkic jako osobny plan do opiniowania z dyskusją i dopracujemy go tam.
- **Rekomendacja:** C, bo lista metryk to temat na kilka wymian zdań, a plan ma dyskusję widoczną w GUI.
- **Decyzja:**
