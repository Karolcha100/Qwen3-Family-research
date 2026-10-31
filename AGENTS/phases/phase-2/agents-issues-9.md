# Główny pomysł — pytania (runda 9): pass@2 i pass@3, wybór warstw według mapy

*2026-10-30 18:38 — Claude Opus 5.5*

## Co masz zrobić

Dwa pytania z Twoich uwag (@T015 i dyskusja raportu `etap-4c-k31-k38.md`). Oba wymagają GPU, więc zgoda w nich to też „uruchom” (@phase-0:K10). Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”, a jeśli chcesz obu obliczeń od razu jedno po drugim, dopisz „uruchom”.

---

### K44. 🟡 pass@2 i pass@3: ile odpowiedzi losować i dla których modeli

- **Problem:** pass@k to szansa, że **co najmniej jedna z k odpowiedzi** modelu rozwiązuje zadanie (@T015). Żeby ją policzyć, model musi dać kilka **różnych** odpowiedzi, więc zamiast jednej najbardziej prawdopodobnej odpowiedzi losujemy kilka (z „temperaturą”, która ustala, jak bardzo odpowiedzi mogą się różnić). Z n odpowiedzi, z których c jest poprawnych, standardowy wzór (Chen i in. 2021, ten sam co w EvalPlus) daje pass@k bez zgadywania:

$$
\text{pass@}k = 1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}
$$

  Słownie: jeden minus szansa, że k odpowiedzi wybranych z n samych są błędne; potem średnia po zadaniach. Przy losowaniu pass@1 wychodzi zwykle trochę niższy niż przy jednej najbardziej prawdopodobnej odpowiedzi (bo losowanie czasem wybiera gorszy token), więc **porównujemy oryginał i nasze modele zawsze w tym samym ustawieniu**.

  Kod jest gotowy i sprawdzony bez GPU: `scripts/phase2_code_generate.py --samples-per-task 10`, `scripts/phase2_code_evaluate.py` liczy pass@1, @2, @3 (test wzoru: `tests/test_qwen_compression.py`; sprawdzenie w kontenerze na dwóch gotowych zestawach odpowiedzi dało dokładnie oczekiwane liczby).
- **Opcje** (wszędzie 10 odpowiedzi na zadanie, temperatura 0,8, top-p 0,95 — typowe ustawienie dla pass@k):
  - **A** — oryginał + dwa warianty (w. 13 cel za warstwą, w. 26): moim szacunkiem **~2–2,5 h GPU** (pewność mała: zmierzę na oryginale i pasek poprawi czas);
  - **B** — oryginał + wszystkie cztery warianty: ~3,5–4 h;
  - **C** — na razie tylko oryginał (~45 min), żeby zobaczyć liczby i czas; resztę później;
  - **D** — pass@k tylko dla „kamieni milowych” (razem z K43), teraz nie liczymy.
- **Rekomendacja:** A. Pokaże, czy różnica warstwa 13 vs 26 utrzymuje się przy kilku próbach, i to na trzech modelach zamiast pięciu. Wyniki podam jako liczby zadań (np. „rozwiązane w co najmniej 1 z 3 prób”) i jako pass@k.
- **Decyzja:** A, ale bez warstwy 26, uważam ją za zbędną do trenowania (docelowo będziemy zmniejszać środkowe warstwy raczej niż początkowe/końcowe)

### K45. 🔴 Sprawdzić warstwy, które mapa wskazuje jako najtańsze

- **Problem:** napisałeś, że wolisz trzymać się jednego celu treningu (za warstwą) i wybierać warstwy pełne mało ważnych neuronów. Według mapy najtańsze do zmniejszenia są warstwy **20–25**, potem 17, 26, 18 (wykres w dyskusji raportu `etap-4c-k31-k38.md`). Dotąd zmniejszaliśmy tylko 2, 13, 14 i 26. Warstwa 26 w testach kodu nie straciła nic, a mapa uważa 20–25 za jeszcze tańsze. Mapa sumuje jednak ważność neuronów osobno i nie uwzględnia ich współdziałania; w warstwie 26 zmierzona KL była 2× większa, niż mapa przewidywała.
- **Opcje:**
  - **A** — warstwy 20–25, każda osobno, −40%, start z mapy 75/25, najmniejsze kwadraty, 6 epok celem za warstwą; pomiar KL (Python, C4) i perpleksji. Potem testy kodu (jedna odpowiedź) dla dwóch najlepszych. Szacunek: ~45 min + ~15 min testów kodu, **~1 h GPU**, ~24 GB na dysku na dane treningowe warstw (wolne 174 GB);
  - **B** — jak A, ale testy kodu dla wszystkich sześciu warstw (~1 h 30 min);
  - **C** — tylko warstwy 20 i 24 (najtańsza według mapy przy 20% i najtańsza przy 40%), ~30 min;
  - **D** — nie teraz.
- **Rekomendacja:** A. Sprawdza Twój pomysł na całym obszarze, który mapa uważa za tani, i pokaże, czy mapa dobrze wybiera warstwy, zanim zaczniemy zmniejszać wiele warstw naraz.
- **Decyzja:** Narazie sprawdźmy czy nasze metryki mają sens, używając @phase-2:K43 - potem zadasz mi to pytanie jeszcze raz

*2026-10-30 18:38 — Claude Opus 5.5*
