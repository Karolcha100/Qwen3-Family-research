# Główny pomysł — pytania (runda 6): co trenować i od jakiej mapy zaczynać

*2026-10-30 12:48 — Claude Opus 5.5*

## Co masz zrobić

Oba pytania wynikają z obliczeń, które zrobiłem pod Twoją nieobecność (@T012). Wyniki są w raporcie `AGENTS/phases/phase-2/etap-4b-kod.md`. Najważniejsze jest K37. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”.

---

### K37. 🔴 Co trenować, żeby trening odrobił więcej

- **Problem:** zmniejszoną warstwę trenujemy dziś tak, żeby wynik **za następną warstwą** zgadzał się z oryginałem. Przy tym celu 16 epok zamiast 4 zmniejsza KL tylko o ~5% (@phase-2:K23), a na danych z Pythona 6 epok zmniejsza KL tylko o 11–20% względem samych najmniejszych kwadratów (warstwy 2, 13, 14), a w warstwie 26 tylko o 1%. Granicą jest więc to, co trenujemy, a nie jak długo (zgodnie z Twoją uwagą z @T011, trening jest głównym narzędziem, więc warto go poprawić).
- **Opcje:**
  - **A** — trenować zmniejszoną warstwę z celem **na wyjściu modelu**: KL między rozkładem następnego tokenu oryginału i modelu ze zmniejszoną warstwą (reszta modelu zamrożona). To dokładnie ta miara, którą oceniamy. Koszt: każdy krok przechodzi przez cały model, według mojego szacunku 5–10× wolniej na epokę, czyli dla jednej warstwy ~30–60 min GPU;
  - **B** — trenować zmniejszoną warstwę razem z **kilkoma następnymi warstwami** (np. 2–3), które też mogą się dostosować; cel nadal za oknem warstw. Taniej niż A, ale zmienia też warstwy, których nie zmniejszaliśmy;
  - **C** — A i B porównane na warstwie 13 przy 40%;
  - **D** — zostajemy przy obecnym celu.
- **Rekomendacja:** A. Cel na wyjściu modelu jest zgodny z tym, co mierzymy, i nie rusza innych warstw. Jeśli A da dużo więcej niż obecny cel, wiemy, że to droga dla Phase 3.
- **Decyzja:** A

### K38. 🟡 Waga kodu w mapie

- **Problem:** nowa mapa to 75% kod + 25% tekst (@phase-2:K26). Na warstwie 13 start z niej daje po treningu o 36–38% mniejszą KL na Pythonie niż start ze starej mapy (z tekstu), za to o 26–33% większą KL na tekście C4. W @phase-2:K18 pisałeś o mapie tylko z kodu.
- **Opcje:**
  - **A** — dodatkowo sprawdzić mapę 100% kod na warstwie 13 (mapa jest już policzona, trening ~10 min GPU) i wybrać wagę na podstawie wyniku;
  - **B** — zostajemy przy 75/25;
  - **C** — przechodzimy na 100% kod bez sprawdzania.
- **Rekomendacja:** A. Koszt jest mały, a pokaże, ile tekstu „kosztuje” każdy punkt kodu.
- **Decyzja:** A

*2026-10-30 12:48 — Claude Opus 5.5*
