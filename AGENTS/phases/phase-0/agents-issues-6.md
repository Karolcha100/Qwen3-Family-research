# Phase 0 — pytania (runda 6): skład 200 pytań do oceny

*2026-10-29 16:21 — Claude Opus 5.5*

## Co masz zrobić

Dwie decyzje wynikające z @phase-0:K39 = A. Wyjaśnienie jest w @T005. Nie blokują Phase 1. Wystarczy „rek” albo litera.

---

### K41. 🟡 Skąd wziąć 200 pytań

- **Problem:** po K39 w naszym zestawie nie ma pytań IFEval, a MT-Bench ma tylko 80 pytań. Brakuje ~120. Do tego Qwen3-0.6B jest mały: na bardzo trudnych pytaniach już BF16 odpowiada słabo, więc pogorszenie po kompresji trudno zauważyć (wszystko jest „na dnie”). Potrzebna jest mieszanka trudności.
- **Opcje:**
  - **A** — 80 MT-Bench + 100 Arena-Hard (trudne, z prawdziwych rozmów) + 20 własnych;
  - **B** — 80 MT-Bench + 120 AlpacaEval (prostsze, różnorodne);
  - **C** — 80 MT-Bench + 60 Arena-Hard + 40 AlpacaEval + 20 własnych;
  - **D** — inny podział (wpisz jaki).
- Pytania z Arena-Hard i AlpacaEval losujemy raz, ze stałym ziarnem, i zapisujemy listę w repo. 20 własnych napiszesz Ty (o tym, co Cię ciekawi), albo zaproponuję listę do Twojej akceptacji.
- **Rekomendacja:** C. Mieszanka trudności działa dla 0.6B i dla 8B. Pytania z jednoznaczną odpowiedzią (metryka 5, @phase-0:K40 = A) dają głównie kategorie matematyka i rozumowanie z MT-Bench oraz część własnych.
- **Decyzja:** C

### K42. 🟢 Druga tura pytań MT-Bench

- **Problem:** każde pytanie MT-Bench ma dopytanie, np. „Napisz wiersz o morzu” → „Teraz przerób go na limeryk”. Druga tura sprawdza, czy model pamięta rozmowę, a to kompresja też może psuć.
- **Opcje:**
  - **A** — tylko pierwsza tura (prościej, 80 pytań);
  - **B** — obie tury: druga tura z własną pierwszą odpowiedzią modelu w kontekście, oceniana osobno (80 dodatkowych ocen, poza liczbą 200);
  - **C** — A jako standard, B jako osobny eksperyment dla wybranych wariantów.
- **Rekomendacja:** C.
- **Decyzja:** B
