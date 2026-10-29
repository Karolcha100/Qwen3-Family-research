# TODO dla agentów LLM

Zasady (numeracja `L…`, statusy, raporty): `AGENTS/todo/llm/INSTRUKCJA.md`. Kolejność faz: `AGENTS/plan/phases-plans.md`.

*Szablon, 2026-10-29*

---

- [x] **L1. Katalog metod kompresji + propozycja zestawu startowego** (@phase-0:K34 = B). *(w toku: Claude Opus 5.5, 2026-10-29 16:21)* *(zrobione: 2026-10-29 16:23, raport: raport-TODO-LLM.md)*
- [?] **L2. Phase 1 kroki 5–6: środowisko Pythona** (uv, Python 3.14, PyTorch z CUDA, transformers, accelerate, datasets, lm-eval, ruff/pyright/pytest — @phase-0:K14 = A). Czeka na: @A8 (plan zatwierdzony 2026-10-29 19:39). *(dodane 2026-10-29 16:54)*
- [?] **L3. Phase 1 krok 4: budowa llama.cpp z CUDA (sm_89)** w `~/llama.cpp`. Czeka na: @A7 (CUDA 13.4), @A8 (pakiety). *(dodane 2026-10-29 16:54)* Kod sklonowany: `~/llama.cpp`, commit `eb4e244be` *(2026-10-29 19:47)*.
- [?] **L4. Phase 1 kroki 7–8: testy dymne Qwen3-0.6B** (PyTorch: generacja + perplexity; llama.cpp: GGUF, `llama-bench`, `llama-perplexity`). Czeka na: L2, L3 i „uruchom” autora (GPU, @phase-0:K10). *(dodane 2026-10-29 16:54)*
- [ ] **L5. Phase 1 krok 9: raport środowiska** `AGENTS/phases/phase-1/srodowisko.md`. Po L2–L4. *(dodane 2026-10-29 16:54)*
- [x] **L6. Ranking Elo w planie metryk** (sekcja C `AGENTS/phases/phase-0/plan-metryki-oceny.md`). Czeka na: odpowiedź końcową w @phase-0:K36 (@A10). *(dodane 2026-10-29 16:54)* *(zrobione: 2026-10-29 19:33, raport: raport-TODO-LLM.md)*
- [?] **L7. Zestaw pytań do oceny:** 80 MT-Bench (obie tury, @phase-0:K42 = B) + 60 Arena-Hard + 40 AlpacaEval (losowanie ze stałym ziarnem, @phase-0:K41 = C) + propozycja 20 własnych do akceptacji autora; pytania z odpowiedzią wzorcową oznaczone (@phase-0:K40). Czeka na: opinię o planie metryk i L2. *(dodane 2026-10-29 16:54)*
- [ ] **L8. Przegląd wieloatrybutowych modeli nagrody** (ArmoRM i nowsze; atrybuty, rozmiar, licencja, czy mieszczą się w 12 GB) jako materiał do @phase-0:K18 („do rozważenia”). Bez uruchamiania. *(dodane 2026-10-29 16:54)*
- [?] **L9. Weryfikacja obsługi Qwen3 w bibliotekach** dla metod wybranych przez autora (⚠️ w `AGENTS/phases/phase-0/katalog-metod.md`). Czeka na: wybór metod. *(dodane 2026-10-29 16:54)*
- [?] **L10. Notatki do nauki dla każdej wybranej metody** (@phase-0:K15 = A: idea, wzór w TeX z opisem słownym, co mierzymy, co wyszło). Czeka na: wybór metod. *(dodane 2026-10-29 16:54)*
- [?] **L11. Lokalna strona HTML do ręcznej oceny ~50 odpowiedzi** (@phase-0:K26 = A). Czeka na: L7 i pierwsze wygenerowane odpowiedzi. *(dodane 2026-10-29 16:54)*

