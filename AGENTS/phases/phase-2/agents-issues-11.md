# Główny pomysł — pytania (runda 11): miara wyboru, następny krok, koniec Phase 2

*2026-11-01 17:54 — Claude Opus 5.5*

## Co masz zrobić

Trzy pytania z raportu `AGENTS/phases/phase-2/warstwy-10-25.md`. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”. Obliczenia z K49 uruchomię dopiero po Twoim osobnym „uruchom” (@phase-0:K10).

---

### K48. 🔴 Którą miarą wybierać warstwy i warianty

- **Problem:** na 8 modelach z testami kodu zgodność odpowiedzi z oryginałem przewiduje liczbę rozwiązanych zadań (korelacja rang 0,86), a KL na Pythonie słabo (0,48). KL karze końcowe warstwy (20–25), które w testach kodu wypadają dobrze (w. 24: 200 zadań, tyle co oryginał). Te same warstwy tracą jednak wyraźnie więcej tekstu: KL na C4 jest ~2,4× większa niż w środku modelu, a perpleksja rośnie o 2–2,7% zamiast ~1%.
- **Opcje:**
  - **A** — główna miara to **zgodność na 510 zadaniach spoza testów**. KL na Pythonie i na tekście oraz perpleksję dalej mierzę i pokazuję, ale nie decydują o wyborze;
  - **B** — jak A, ale z **limitem utraty tekstu**: wariant odpada, jeśli perpleksja WikiText-2 rośnie o więcej niż ustalony próg (np. +2% na warstwę). Chroni tekst kosztem kodu;
  - **C** — zostajemy przy KL na Pythonie jako głównej mierze.
- **Rekomendacja:** A. Twój cel to programowanie (@phase-2:K25), a zgodność dwa razy trafiła tam, gdzie KL się myliła (w. 26, w. 24). Wybierz B, jeśli zależy Ci też na zwykłym tekście.
- **Decyzja:**

### K49. 🔴 Następny krok: zmniejszanie kilku warstw naraz

- **Problem:** do tej pory zmniejszaliśmy zawsze jedną warstwę (0,6% parametrów). Żeby model był naprawdę mniejszy, trzeba zmniejszyć wiele warstw, a wtedy straty się sumują. Każdą warstwę trenowaliśmy na wejściach z oryginalnego modelu. W modelu z kilkoma zmniejszonymi warstwami dostanie wejścia już zmienione przez wcześniejsze warstwy (@T017).
- **Opcje:**
  - **A** — **kilka warstw naraz, dwa sposoby na tych samych warstwach**:
    1. **złożenie gotowych warstw** trenowanych osobno, bez nowego treningu, np. 4 najlepsze według zgodności (25, 24, 23, 22) przy −20% i przy −40%. To ~10 min GPU na zgodność i KL;
    2. **zmniejszanie po kolei:** dane do treningu kolejnej warstwy zbieram z modelu, w którym wcześniejsze są już zmniejszone. To ~1 h GPU i trochę kodu (bez GPU).

    Dla lepszego sposobu robię testy kodu (~8 min na model). Wynik pokaże, ile tracimy przy ~2,4% parametrów i czy trening po kolei jest potrzebny;
  - **B** — najpierw **poprawić naprawę w końcowych warstwach:** trening celem na wyjściu modelu dla warstw 20–25, bo obecny przepis usuwa tam tylko 7–17% szkody. To ~25 min GPU na warstwę, razem ~2,5 h;
  - **C** — najpierw **zmierzyć pozostałe warstwy** (0–9, 11, 12, 16, 19) tym samym przepisem, żeby mieć pełny obraz wszystkich 28 warstw (~2 h GPU).
- **Rekomendacja:** A. To najkrótsza droga do odpowiedzi na najważniejsze pytanie: ile kosztuje zmniejszenie kilku warstw naraz. Złożenie gotowych warstw jest prawie darmowe. B i C mogą przyjść później, jeśli A pokaże, że są potrzebne.
- **Decyzja:**

### K50. 🟡 Czy zamknąć Phase 2

- **Problem:** kryteria końca z planu Phase 2 (`AGENTS/phases/phase-2/plan-phase-2.md`) są spełnione: jest mapa wszystkich neuronów, wykresy rodzajów neuronów, krzywa zmniejszania jednej warstwy i raporty etapów. Ponad plan doszły: przejście na kod, testy EvalPlus i pomiar 14 warstw. Plan przypisał zmniejszanie wielu warstw i dotrenowanie całego modelu do Phase 3 (@phase-2:K10).
- **Opcje:**
  - **A** — zostajemy w Phase 2: kilka warstw (K49) to kolejny etap Phase 2, a ja dopisuję go do planu;
  - **B** — zamykamy Phase 2 i zakładam Phase 3 („zmniejszanie wielu warstw i dotrenowanie modelu”). Napiszę do niej plan do zatwierdzenia, a pierwszym etapem będzie K49;
  - **C** — decyzję odkładamy do wyników K49.
- **Rekomendacja:** B. Tak przewidywał zatwierdzony plan, a w pracy łatwiej opisać zamknięty etap „jedna warstwa” i osobny etap „wiele warstw”. Jeśli wolisz nie mnożyć planów, wybierz C.
- **Decyzja:**

*2026-11-01 17:54 — Claude Opus 5.5*
