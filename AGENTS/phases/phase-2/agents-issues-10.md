# Główny pomysł — pytania (runda 10): na czym liczyć codzienną zgodność odpowiedzi

*2026-11-01 00:04 — Claude Opus 5.5*

## Co masz zrobić

Jedno pytanie z raportu `AGENTS/phases/phase-2/k43-zgodnosc-tokenu.md`. Nie wymaga GPU poza kilkoma minutami w opcji B. Jeśli zgadzasz się z rekomendacją, wystarczy „rek”.

Pytanie K45 (warstwy najtańsze według mapy) miałem zadać ponownie po K43. Twoja wiadomość w czacie z 1.11 („posprawdzać, co się dzieje, jak zmniejszane są inne mało istotne warstwy”, obliczenia do 6:00) już na nie odpowiada, więc kolejka warstw liczy się w nocy (raport K43, sekcja 5).

---

### K46. 🟡 Na jakich zadaniach liczyć codziennie zgodność odpowiedzi z oryginałem

- **Problem:** zgodność tokenu liczona na **odpowiedziach oryginału na zadania programistyczne** przewidziała kolejność modeli w testach kodu, a zgodność na zwykłym kodzie nie (raport K43, sekcja 2). Teraz te odpowiedzi pochodzą z samych zadań testowych EvalPlus. Jeśli będziemy wybierać spośród wielu wariantów według miary liczonej na zadaniach testowych, końcowy wynik EvalPlus może wyjść trochę zbyt optymistyczny: wybierzemy warianty, które akurat dobrze wypadają na tych konkretnych zadaniach. Testów przy tym nie uruchamiamy, sprawdzamy tylko podobieństwo do oryginału, więc to ryzyko jest małe, ale istnieje.
- **Opcje:**
  - **A** — zostajemy przy zadaniach EvalPlus (HumanEval + MBPP, 542 zadania). Gotowe, nic nie trzeba robić;
  - **B** — osobny zestaw zadań spoza testów: pełne MBPP ma 974 zadania, a MBPP+ korzysta tylko z części z nich. Zostaje kilkaset zadań, których w testach nie ma (dokładną liczbę i brak nakładania sprawdzę przed użyciem). Oryginał pisze do nich odpowiedzi raz (~4 min GPU), potem zgodność liczy się jak teraz. EvalPlus zostaje wtedy czystym testem końcowym;
  - **C** — tylko zgodność na zwykłym kodzie (jak w pierwotnej wersji K43 A); taniej o ~30 s na wariant, ale gorzej przewiduje testy.
- **Rekomendacja:** B. Koszt jest mały, a w pracy będzie można napisać, że wybieraliśmy warianty bez patrzenia na zadania testowe. Do czasu przygotowania zestawu B liczę też A (kolejka z nocy już to robi).
- **Decyzja:**

*2026-11-01 00:04 — Claude Opus 5.5*
