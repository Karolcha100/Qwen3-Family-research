# Główny pomysł — pytania (runda 5): start zmniejszonej warstwy i ocena kodu

*2026-10-30 11:10 — Claude Opus 5.5*

## Co masz zrobić

**K31** wynika z Twojej uwagi w @T011: zmniejszone warstwy trenujemy, a wybór neuronów to tylko punkt startu. **K32–K36** wynikają z @phase-2:K20 = C i są opisane w `AGENTS/phases/phase-2/raport-3-ocena-kodu.md`. Najważniejsze są K31, K32 i K36. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”.

---

### K31. 🔴 Czy punkt startu zmniejszonej warstwy ma znaczenie po treningu

- **Problem:** zmniejszona warstwa zaczyna dziś od części neuronów oryginału (wybranej mapą), potem dostaje nowe $W_{down}$ z najmniejszych kwadratów i jest trenowana. W etapie 4 (4 epoki) start z mapy przesiewu dawał po treningu o 17–37% mniejszą KL niż start według średniej aktywacji, więc przy krótkim treningu start ma znaczenie. Nie wiemy, czy zostaje tak przy długim treningu. Jeśli nie, mapa ważności przestaje być potrzebna, a wysiłek należy przenieść na trening.
- **Opcje:**
  - **A** — porównanie dla warstwy 13 przy 40%: start z mapy, start według średniej aktywacji, start losowy (losowe neurony oryginału) oraz start z **połączonych** neuronów (podobne neurony łączone w jeden zamiast wyrzucania), każdy z długim treningiem (ustawienie z K23); ~1 h GPU;
  - **B** — jak A, ale bez łączenia neuronów (prostsze, ~45 min);
  - **C** — nie badamy; zostajemy przy starcie z mapy.
- **Rekomendacja:** A. To bezpośrednio sprawdza Twoją uwagę z @T011: ile daje start, a ile trening. Łączenie neuronów to najprostszy sposób, żeby zmniejszona warstwa zaczynała od całej wiedzy oryginału, a nie od jej części.
- **Decyzja:** A

### K32. 🔴 Główny test poprawności kodu

- **Problem:** raport 3, rozdz. 2. Zadania z testami mówią, czy model pisze działający kod. Raport techniczny Qwen3 podaje dla Qwen3-0.6B-Base: EvalPlus 36,23 i MBPP 36,60.
- **Opcje:**
  - **A** — HumanEval, MBPP, HumanEval+ i MBPP+ (EvalPlus), pass@1 zachłannie; porównanie oryginał–zmniejszony na tych samych zadaniach;
  - **B** — tylko HumanEval i MBPP;
  - **C** — A plus trudniejsze zestawy (np. LiveCodeBench).
- **Rekomendacja:** A. Te zestawy pozwalają porównać się z liczbami Qwen, a wersje „+” utrudniają przypadkowe zaliczenie.
- **Decyzja:** A

### K33. 🟡 Klasyfikator (model oceniający kod)

- **Problem:** raport 3, rozdz. 3. W zadaniach z testami klasyfikator przewiduje to, co testy sprawdzają wprost. Przydałby się do czytelności i stylu oraz do kodu bez testów.
- **Opcje:**
  - **A** — na razie bez klasyfikatora: testy i analiza statyczna;
  - **B** — model nagrody do kodu AceCodeRM-7B (w 8 lub 4 bitach, żeby zmieścić się w 12 GB);
  - **C** — model-sędzia (np. Qwen2.5-Coder-7B-Instruct w GGUF przez llama.cpp) z listą kryteriów czytelności.
- **Rekomendacja:** A teraz. C dodać, jeśli zmniejszony model zacznie pisać kod „działający, ale gorszy”.
- **Decyzja:** A, przy czym faktycznie klasyfikatora można dać nawet do future research

### K34. 🟢 Jakość kodu bez uruchamiania

- **Problem:** raport 3, rozdz. 4. Liczby błędów ruff i pyright, złożoność cyklomatyczna i długość rozwiązań, porównane między oryginałem a zmniejszonym modelem.
- **Opcje:**
  - **A** — tak, dla każdego rozwiązania z K32 (prawie darmowe);
  - **B** — nie.
- **Rekomendacja:** A.
- **Decyzja:** A

### K35. 🟡 Sprawność

- **Problem:** raport 3, rozdz. 5. „Sprawność” to albo szybkość i rozmiar zmniejszonego modelu, albo szybkość działania napisanego kodu (np. zestaw Mercury, zadania w stylu LeetCode).
- **Opcje:**
  - **A** — zawsze sprawność modelu (parametry, pamięć, tokeny/s); Mercury dopiero, gdy zobaczymy, ile zadań oryginał rozwiązuje;
  - **B** — od razu obie;
  - **C** — tylko sprawność modelu.
- **Rekomendacja:** A.
- **Decyzja:** A

### K36. 🔴 Zgoda na uruchamianie kodu napisanego przez model

- **Problem:** testy z K32 wymagają uruchomienia kodu wygenerowanego przez model, którego nikt nie sprawdził (raport 3, rozdz. 6).
- **Opcje:**
  - **A** — zgoda: kontener podman bez sieci, system plików tylko do odczytu, limity pamięci, procesora i czasu; pobranie obrazu `python:3.12-slim` (~50 MB);
  - **B** — zgoda, ale tylko po Twoim przejrzeniu konfiguracji kontenera;
  - **C** — nie uruchamiamy; zostaje KL i analiza statyczna.
- **Rekomendacja:** A.
- **Decyzja:** A
