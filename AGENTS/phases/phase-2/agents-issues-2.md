# Główny pomysł — pytania (runda 2): szczegóły Phase 2

*2026-10-29 21:13 — Claude Opus 5.5*

## Co masz zrobić

Szczegóły potrzebne do planu `AGENTS/phases/phase-2/plan-phase-2.md` (etapy 1–4, @phase-2:K9). Plan działa z rekomendacjami; jeśli się zgadzasz, wystarczy „rek” albo litera.

---

### K10. 🟢 Numer fazy

- **Problem:** w K9 napisałeś „w phase 1 tylko etapy 1–4”, ale Phase 1 to już skończone środowisko.
- **Opcje:**
  - **A** — etapy 1–4 to **Phase 2**, etapy 5–6 to Phase 3;
  - **B** — inna nazwa (wpisz).
- **Rekomendacja:** A.
- **Decyzja:** A, wcześniej się pomyliłem z numerami sorry xD

### K11. 🟡 Tekst, na którym mierzymy zaburzenia

- **Problem:** KL liczymy na stałym zbiorze tokenów. W @phase-0:K8 wybrałeś mieszankę C4 + kod (dla kalibracji); proponuję ją też tutaj. Trzeba ustalić proporcje.
- **Opcje:**
  - **A** — 75% C4 (zwykły tekst z internetu) + 25% kod z GitHuba (różne języki programowania);
  - **B** — 50% + 50%;
  - **C** — sam C4.
- **Rekomendacja:** A. Większość użycia to zwykły tekst, ale z 25% kodu wyłapiemy też neurony „od kodu”. Wielkość zbioru (np. 4096 lub 16 384 tokenów) ustali pilot.
- **Decyzja:** A

### K12. 🟢 Które warstwy w pilocie (etap 1)

- **Problem:** pilot liczy dokładnie wszystkie neurony 3 warstw (~1,5 h GPU).
- **Opcje:**
  - **A** — wczesna, środkowa, późna: warstwy 2, 13, 25 (z 0–27);
  - **B** — wybór po statystykach aktywacji (np. warstwa z największymi „masywnymi” aktywacjami + dwie typowe);
  - **C** — inne (wpisz).
- **Rekomendacja:** A. Warstwy w różnych miejscach modelu zachowują się różnie, a statystyki i tak zbierzemy przy okazji.
- **Decyzja:** A

### K13. 🟢 Ile tokenów zapisać do treningu warstwy (etap 4)

- **Problem:** wybrałeś zapis na dysk (@phase-2:K6). W wariancie „przez następną warstwę” (K5 = B) zapisujemy wejście $h^{(\ell-1)}$ i cel $h^{(\ell+1)}$, czyli 2 × 1024 liczb BF16 = 4 KB na token.
- **Opcje:**
  - **A** — 1 mln tokenów (~4 GB na warstwę);
  - **B** — 250 tys. (~1 GB);
  - **C** — 4 mln (~16 GB).
- **Rekomendacja:** A. Warstwa ma ~9,4 mln parametrów, więc 1 mln tokenów × 1024 wymiary celu daje ~100 razy więcej liczb niż parametrów. Jeśli okaże się, że to za mało, dorzucimy.
- **Decyzja:** A

### K14. 🟡 Jak mocno zmniejszamy warstwę w etapie 4

- **Problem:** jedna warstwa, ile neuronów wyciąć.
- **Opcje:**
  - **A** — jeden stopień: 3072 → 2458 (−20%);
  - **B** — krzywa: −10%, −20%, −30%, −50% (4 przebiegi treningu jednej warstwy);
  - **C** — inne (wpisz).
- **Rekomendacja:** B. Krzywa pokaże, gdzie warstwa zaczyna „pękać”, a to wprost wskazówka do etapu 5. Koszt to kilka razy po kilkanaście minut.
- **Decyzja:** B aczkolwiek proponuje -5%, -10%, -20%, -40%

### K15. 🟢 Układ kodu

- **Problem:** w @phase-0:K12 pakiet `src/…` był „spoko”, ale bez znanych metod. Teraz wiadomo, co robimy.
- **Opcje:**
  - **A** — pakiet `src/qwen_compression/` z modułami `activations.py` (zbieranie aktywacji), `perturbation.py` (zaburzenia), `metrics.py` (KL, strata), `importance.py` (przesiew gradientem), `reconstruction.py` (najmniejsze kwadraty, trening warstwy) i cienkimi skryptami w `scripts/` (po jednym na etap) + testy w `tests/`;
  - **B** — same skrypty w `scripts/`, bez pakietu;
  - **C** — inna nazwa pakietu (wpisz).
- **Rekomendacja:** A. Etapy korzystają ze wspólnych części, więc bez pakietu kod szybko by się powtarzał.
- **Decyzja:** A
