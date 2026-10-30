# Główny pomysł — pytania (runda 3): po nocy z etapami 1–4

*2026-10-30 02:04 — Claude Opus 5.5*

## Co masz zrobić

Pytania wynikają z nocnych wyników: raporty `etap-1-pilot.md`, `etap-2-mapa.md`, `etap-3-rodzaje-neuronow.md`, `etap-4-jedna-warstwa.md` w tym folderze. Najważniejsze są **K17** (czy akceptujesz, jak policzyłem etap 2) i **K21** (warstwa w etapie 4). K23 dotyczy dłuższego treningu w etapie 4. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek” albo litera.

---

### K16. 🟢 Które δ mierzyć dalej

- **Problem:** pilot pokazał, że skutek rośnie dokładnie jak $\delta^2$. Słownie: osłabienie neuronu o połowę daje równo ¼ skutku wyłączenia (mediana 0,250 we wszystkich trzech warstwach), a podwojenie daje to samo co wyłączenie (0,99–1,00). Pomiary dla $\delta = \pm 0{,}5$ nie wnoszą więc nowej informacji, a kosztują połowę czasu.
- **Opcje:**
  - **A** — dalej tylko $\delta = -1$ i $\delta = +1$ (wyłączenie i podwojenie; $+1$ dla nielicznych neuronów asymetrycznych);
  - **B** — tylko $\delta = -1$;
  - **C** — wszystkie cztery, jak w planie (@phase-pomysl:K2).
- **Rekomendacja:** A. W nocy etap 2 liczę już według A (zmiana względem planu, dlatego pytam).
- **Decyzja:**

### K17. 🔴 Etap 2 policzony przesiewem na dużej liczbie tokenów

- **Problem:** nocne reguły z @T010 miały trzy warunki. Wynik:
  - **precyzja:** float32, warunek spełniony;
  - **przesiew vs dokładnie:** przy 16 próbkach nie spełniony (0,88–0,95 i 78%), przy 64 próbkach spełniony (0,96–0,98 i 84–87%);
  - **liczba tokenów:** **nie spełniony**. Ranking z dwóch rozłącznych zbiorów po 4096 tokenów zgadza się tylko w 0,51.

  Pomiar dokładny na 4096 tokenach jest więc mało wiarygodny, niezależnie od metody. Przesiew jest ~1000× tańszy, więc policzyłem go na **131 tys. tokenów** (64 sekwencje × 64 próbki, 21 min), a dokładnie mierzę 10% najważniejszych i 5% losowych neuronów każdej warstwy (~2 h). To jest tryb „przesiew” z reguł, tylko z 64 próbkami zamiast 16.
- **Opcje:**
  - **A** — akceptuję: mapa = przesiew na 131 tys. tokenów, pomiar dokładny tylko do kontroli;
  - **B** — chcę też pomiaru dokładnego **wszystkich** neuronów, ale na większej liczbie tokenów (np. 32 tys. tokenów i $\delta = \pm 1$ to ~5 dni GPU, więc w praktyce tylko dla kilku warstw);
  - **C** — inaczej (wpisz).
- **Rekomendacja:** A. Szczegóły w `etap-1-pilot.md` (rozdz. 2.5 i 3) i `etap-2-mapa.md`.
- **Decyzja:**

### K18. 🟡 Mapa osobno dla tekstu i dla kodu?

- **Problem:** ranking neuronów policzony na samym kodzie i ranking na samym tekście (C4) są **praktycznie niezależne** (Spearman od −0,15 do 0,23 w zależności od warstwy). Dwie porcje samego tekstu tej samej wielkości zgadzają się w 0,74–0,94. Neurony ważne dla kodu to w dużej mierze inne neurony niż ważne dla tekstu. Przy zmniejszaniu warstwy ma to znaczenie: mieszanka 75/25 (@phase-pomysl:K11) to wybór, jaki „sens” modelu chronimy.
- **Opcje:**
  - **A** — zostajemy przy jednej mapie z mieszanki 75% tekstu + 25% kodu, a w etapie 4 sprawdzamy osobno, ile model traci na tekście i na kodzie;
  - **B** — dwie mapy (tekst, kod) i przy zmniejszaniu zachowujemy neurony ważne dla **któregokolwiek** z nich;
  - **C** — inne proporcje (wpisz).
- **Rekomendacja:** A na teraz, a B jako kolejny eksperyment etapu 4, jeśli wyjdzie, że kod traci wyraźnie więcej niż tekst.
- **Decyzja:**

### K19. 🟢 Nazwa folderu `phase-pomysl`

- **Problem:** pisałeś, że nie widzisz planu Phase 2 w GUI (@T010, punkt 5). Plan jest w `AGENTS/phases/phase-pomysl/plan-phase-2.md`; nazwa folderu nie mówi, że to Phase 2.
- **Opcje:**
  - **A** — przemianować na `phase-2` (zmienię też odwołania `@phase-pomysl:K…` → `@phase-2:K…` w plikach, które je zawierają, oprócz starych wpisów w wątkach, które zostają bez zmian);
  - **B** — zostawić `phase-pomysl`.
- **Rekomendacja:** A, ale dopiero gdy nic nie będzie się liczyć (skrypty zapisują wykresy do `AGENTS/phases/phase-pomysl/figures/`).
- **Decyzja:**

### K20. 🟡 Klasyfikator do oceny generacji w etapie 3

- **Problem:** plan etapu 3 zakładał generację i ocenę klasyfikatorem dla ~250 najważniejszych neuronów (@phase-pomysl:K3). Klasyfikator (model nagrody, @phase-0:K18) nie jest wybrany, a zestaw pytań (@L7) nie istnieje, więc tę część odłożyłem.
- **Opcje:**
  - **A** — przygotuję krótki raport z 2–3 kandydatami na model nagrody mieszczącymi się na 12 GB obok Qwen3-0.6B, a Ty wybierzesz;
  - **B** — pomijamy ocenę klasyfikatorem w Phase 2; KL i zmiana straty wystarczą, klasyfikator dopiero w Phase 3;
  - **C** — inaczej (wpisz).
- **Rekomendacja:** B. W Phase 2 i tak wybieramy neurony po KL, a ocena generacji ma największą wartość dla całego zmniejszonego modelu (Phase 3).
- **Decyzja:**

### K21. 🔴 Warstwa do zmniejszania w etapie 4

- **Problem:** plan zakładał, że warstwę wybierasz Ty. Żeby noc nie przepadła, wziąłem **warstwę 13**: ma najmniejszą sumaryczną wrażliwość (suma przewidywanej KL po neuronach 0,045, praktycznie remis z warstwą 14) i ma pełny pomiar dokładny z pilota. Wyniki: `etap-4-jedna-warstwa.md`.
- **Opcje:**
  - **A** — warstwa 13 jest w porządku, idziemy dalej na jej wynikach;
  - **B** — powtórz dla innej warstwy (wpisz którą; np. wrażliwa warstwa 2 albo 26 dla porównania);
  - **C** — powtórz dla kilku warstw (wpisz które).
- **Rekomendacja:** C dla jednej wrażliwej warstwy (np. 2) obok 13. Pokaże, czy krzywa „ile wyciąć” bardzo zależy od warstwy, co jest kluczowe dla etapu 5.
- **Decyzja:**

### K22. 🟢 GUI: zatwierdzenie planu a następny plan (@L14)

- **Problem:** Twój wpis „zamknąłem bo chyba z tego nie korzystamy” trafił do planu Phase 2 zamiast do planu metryk. W kodzie GUI nie znalazłem przyczyny. Potrzebuję wiedzieć, jak to się stało.
- **Opcje:**
  - **A** — zatwierdziłem plan Phase 2, a potem od razu pisałem komentarz, myśląc, że jestem w planie metryk (GUI zostawiło zaznaczony poprzedni plan);
  - **B** — wpisałem komentarz w polu pod planem metryk, a zapisał się w innym planie;
  - **C** — inaczej (opisz kroki).
- **Rekomendacja:** brak, to pytanie o fakty. Po odpowiedzi poprawię GUI (np. po zatwierdzeniu planu wybór przechodzi na następny plan albo na listę).
- **Decyzja:**

### K23. 🟡 Dłuższy trening zmniejszonej warstwy

- **Problem:** w etapie 4 trening „przez następną warstwę” poprawia wynik najmniejszych kwadratów tylko o 12–19%, a w 6 z 8 przebiegów najlepsza była ostatnia (4.) epoka. Trening był więc za krótki albo z za małym krokiem. Jeden przebieg trwa ~95 s.
- **Opcje:**
  - **A** — dla warstwy 13 i stopni 20% / 40% sprawdzić: 16 epok, oraz lr $2 \cdot 10^{-4}$ (~15 min GPU);
  - **B** — zostawić jak jest; trening dopracujemy dopiero przy zmniejszaniu wielu warstw (etap 5);
  - **C** — inaczej (wpisz).
- **Rekomendacja:** A. Tanie, a pokaże, ile da się wycisnąć z samego treningu warstwy, zanim przejdziemy do wielu warstw.
- **Decyzja:**

### K24. 🟢 Progi rodzajów neuronów w etapie 3

- **Problem:** progi rodzajów ustaliłem sam przed obliczeniem (tabela w `etap-3-rodzaje-neuronow.md`, rozdz. 2). Wyszło 5 martwych, 422 zbędne, 75 krytycznych, 883 masywne, 6446 kodowych i 5818 tekstowych. Progi są argumentami skryptu, więc zmiana to ~1 min liczenia.
- **Opcje:**
  - **A** — progi są w porządku;
  - **B** — zmień progi (wpisz, np. „zbędny < 0,2 × mediana”);
  - **C** — zamiast progów chcę ciągłą skalę (np. percentyl ważności w warstwie i w całym modelu).
- **Rekomendacja:** A na teraz. Do zmniejszania i tak używamy ciągłej mapy KL, a rodzaje służą tylko do opisu.
- **Decyzja:**
