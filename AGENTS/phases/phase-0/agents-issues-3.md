# Phase 0 — pytania (runda 3): metryki sędziego i checkpointy

*2026-10-29 14:09 — Claude Opus 5.5*

## Co masz zrobić

Trzy nowe decyzje po Twoich wpisach z 14:07–14:08: K28 i K29 wynikają z @T002, K30 z @T003. Każda ma rekomendację, więc wystarczy wpisać „rek” albo literę.

---

### K28. 🟢 Które metryki regułowe zostają

- **Problem:** dwie metryki 0/1 ze szkicu dublują benchmarki: „format zgodny z instrukcją” to IFEval (gotowe zadanie w lm-eval), a „kod działa” to evalplus. Pozostałe cztery wyłapują typowe awarie po kompresji, których benchmarki nie raportują. Uzasadnienie: @T002.
- **Opcje:**
  - **A** — zostają 4: kompletna, bez pętli, właściwy język, czysty tekst; IFEval dodajemy do zadań lm-eval;
  - **B** — zostaje wszystkie 6 (dublowanie, ale wszystko w jednym raporcie z naszych 50 pytań);
  - **C** — żadnych reguł, polegamy na benchmarkach i sędzim.
- **Rekomendacja:** A. Te 4 są tanie, a przy okazji odfiltrowują zepsute odpowiedzi, zanim oceni je model nagrody.
- **Decyzja:** A

### K29. 🟡 Czy jeden model nagrody da kilka metryk

- **Problem:** pomysł z @T002: ten sam skalarny model nagrody uruchamiany kilka razy z różnym kryterium w treści daje kilka metryk 0–100. Zwykłe modele nagrody często ignorują takie kryterium, a wtedy wszystkie „metryki” to ta sama liczba.
- **Opcje:**
  - **A** — sprawdzamy to na danych: ~50 odpowiedzi Qwen3-0.6B, skalarny model nagrody z 6 kryteriami, macierz korelacji. Jeśli korelacje są bliskie 1, przechodzimy na model wieloatrybutowy (np. ArmoRM) albo na sędziego z rubryką. Jeśli są wyraźnie różne, zostajemy przy Twoim pomyśle;
  - **B** — od razu model wieloatrybutowy (kilkanaście ocen w jednym przebiegu);
  - **C** — od razu sędzia generatywny z rubryką dla każdej metryki 0–100;
  - **D** — od razu Twój pomysł, bez sprawdzania.
- **Rekomendacja:** A. To ~10 minut GPU i uczy czegoś o samych modelach nagrody. Kiedy: po Phase 1, bo potrzebne jest środowisko.
- **Decyzja:** B

### K30. 🟢 Czy zapisujemy skompresowane modele

- **Problem:** każdy wariant (metoda × bity/rzadkość × rozmiar) to osobny model: od ~0,4 GB (0.6B w 4 bitach) do ~16 GB (8B w BF16 po pruningu). Przy dziesiątkach wariantów 184 GB wolnego szybko się skończy.
- **Opcje:**
  - **A** — nie zapisujemy: tylko metryki i konfiguracja z ziarnem, żeby dało się odtworzyć wariant skryptem;
  - **B** — zapisujemy tylko wybrane warianty (najlepsze w swojej klasie albo te, które chcesz przetestować ręcznie w czacie), w folderze poza repo (np. `~/qwen3-checkpoints/`), z listą w repo;
  - **C** — zapisujemy wszystko.
- **Rekomendacja:** B. Większość wariantów jest potrzebna tylko na czas pomiaru, a najlepsze warto mieć pod ręką do porównań w llama.cpp i do sędziego.
- **Decyzja:** B, aczkolwiek zauważ znowu że jeszcze nie wiesz co będziemy tak naprawdę robić!!!
