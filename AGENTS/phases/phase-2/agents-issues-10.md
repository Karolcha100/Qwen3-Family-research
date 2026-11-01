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
- **Decyzja:** B

*2026-11-01 00:04 — Claude Opus 5.5*

---

## Co masz zrobić (dopisane 2026-11-01 13:08)

Drugie pytanie, po nocy: nocna kolejka warstw nie ruszyła, bo zawiesiły się testy K44 (raport `AGENTS/phases/phase-2/k44-pass-at-k.md`, sekcja 4). Uruchomienie wymaga Twojej zgody na GPU, bo nocna zgoda była do ~6:00. Jeśli zgadzasz się z rekomendacją, wystarczy „rek”.

### K47. 🟡 Kiedy puścić kolejkę mało ważnych warstw, która w nocy nie ruszyła

- **Problem:** kolejka `results/phase2/code/queue-layers.json` jest gotowa i bez zmian w treści obliczeń: warstwy 24, 25, 20, 23, 21, 22, 17, 18, 15 (najtańsze według mapy) i kontrolnie 10, każda przy −20% i −40%, przepisem z @T017. Potem zgodność tokenu i testy kodu (jedna odpowiedź bez losowania) dla warstw 24, 20, 17 i 10 przy −40%. Mój szacunek to ~2,5 h GPU. W tym czasie karta graficzna jest zajęta (~5 GB pamięci), a reszta komputera działa normalnie. Zgodność w K46 A miała policzyć ta kolejka, więc dla nowych warstw jej jeszcze nie ma.
- **Opcje:**
  - **A** — puszczam od razu po Twojej odpowiedzi (wyniki dziś po ~2,5 h);
  - **B** — puszczam dziś wieczorem lub w nocy, w godzinach, które podasz w decyzji;
  - **C** — nie puszczam; najpierw chcesz omówić wyniki K43/K44 albo zmienić listę warstw (napisz, jak).
- **Rekomendacja:** A, jeśli nie potrzebujesz teraz karty graficznej. W przeciwnym razie B.
- **Decyzja:** B, poinformuje gdy będziemy puszczać, chcę jeszcze zapoznać się z raportami bardziej

*2026-11-01 13:08 — Claude Opus 5.5*

---

## Co masz zrobić (dopisane 2026-11-01 14:03)

Nic pilnego. Kiedy zechcesz puścić kolejkę warstw (K47 = B), napisz w czacie np. „puść kolejkę warstw” (~2 h 50 min GPU). Gdybyś chciał zmienić listę warstw, napisz które.

### Wykonanie K46 = B i K47 = B

**K46 B: zestaw zadań spoza testów jest gotowy** (bez GPU, `scripts/phase2_code_agreement_set.py` → `results/phase2/code-agreement/mbpp-problems.jsonl`):
- pełne MBPP ma 974 zadania. Odrzuciłem 378 zadań, które są w MBPP+, oraz zadania, które mogłyby się z nimi pokrywać:
  - 2 z identyczną treścią;
  - 61 z bardzo podobną treścią (podobieństwo napisów ≥ 0,9);
  - 23 z tą samą nazwą funkcji co zadanie z testów.
- **zostało 510 zadań.** Zadania tuż pod progiem podobieństwa sprawdziłem ręcznie i są już różne (np. „iloczyn niepowtarzających się elementów” wobec „sumy” w testach);
- zadania mają ten sam format co w EvalPlus (treść + jeden przykład `assert`).

Brakuje jeszcze odpowiedzi oryginału na te zadania (~5 min GPU). Dopisałem je do kolejki warstw, razem z ponownym policzeniem zgodności dla 9 wcześniejszych wariantów. Dzięki temu sprawdzę, czy zgodność na nowym zestawie też ustawia 4 modele z testami kodu w tej samej kolejności co testy. Skrypt zgodności liczy ten zestaw automatycznie, gdy są odpowiedzi.

**K47 B: kolejka czeka na Twój sygnał.** Bez zmian w treści obliczeń warstw, ale doszły:
- 2 kroki K46 (~11 min);
- limit czasu i 4 testy naraz przy testach kodu (żeby nie zawiesiło się jak w nocy).

Szacunek całości to 167 min.

Przepis z @T017 zapisałem jako domyślny (Twoja zgoda 13:45).

*2026-11-01 14:03 — Claude Opus 5.5*
