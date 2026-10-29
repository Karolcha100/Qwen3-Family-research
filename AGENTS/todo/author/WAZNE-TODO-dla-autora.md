# WAŻNE — TODO dla autora

Rzeczy, które blokują dalszą pracę agentów. Zasady (numeracja `A…`, statusy, raporty): `AGENTS/todo/author/INSTRUKCJA.md`.

*Szablon, 2026-10-29*

---

- [x] **A1. Utwórz prywatne repozytorium GitHub „Qwen3-Family-research”** (decyzja @phase-0:K1 = B). Lokalne repo i pierwszy commit już są, ale moje polecenie `gh repo create` zablokowały uprawnienia Claude Code (wysyłanie danych na zewnątrz). Uruchom w katalogu projektu:
  `gh repo create Qwen3-Family-research --private --source=. --remote=origin --push`
  Potem `gh repo view --json visibility,url` powinno pokazać `PRIVATE`. Napisz w raporcie „zrobione” (albo wklej błąd). Kto pushuje w kolejnych sesjach: @phase-0:K17.
  *(zrobione: 2026-10-29 13:54 według raportu autora; sprawdzone przez agenta: `origin` = github.com/Karolcha100/Qwen3-Family-research, `main` zsynchronizowany)*
- [ ] **A2. K7: 🟡 Qwen3 Base czy wersja instrukcyjna** — z pytania @phase-0:K7 (`phases/phase-0/agents-issues-1.md`). *(dodane 2026-10-29 14:52)*
  Raport agenta: `AGENTS/phases/phase-0/A2-base-czy-instrukcyjna.md` — wybór napisz w raporcie pod @A2. *(agent, 2026-10-29 15:03)*
- [ ] **A3. K8: 🟡 Dane kalibracyjne** — z pytania @phase-0:K8 (`phases/phase-0/agents-issues-1.md`). *(dodane 2026-10-29 14:53)*
  Raport agenta: `AGENTS/phases/phase-0/A3-dane-kalibracyjne.md` — wybór napisz w raporcie pod @A3. *(agent, 2026-10-29 15:03)*
- [ ] **A4. K9: 🟡 Protokół perplexity** — z pytania @phase-0:K9 (`phases/phase-0/agents-issues-1.md`). *(dodane 2026-10-29 14:54)*
  Raport agenta: `AGENTS/phases/phase-0/A4-perplexity.md` — wybór napisz w raporcie pod @A4. *(agent, 2026-10-29 15:03)*
- [ ] **A6. Usuń CUDA 12.8 i 12.9** (decyzja @phase-0:K3 = A, plan Phase 1 krok 1). Polecenia i co sprawdzić: `AGENTS/phases/phase-1/A6-usuniecie-cuda-12.md`. Wynik kroku 4 wklej w raporcie. *(dodane 2026-10-29 15:00)*
- [ ] **A7. Zainstaluj CUDA 13.4 (sam toolkit)** — po @A6 (plan Phase 1 krok 2). Polecenia: `AGENTS/phases/phase-1/A7-instalacja-cuda-13-4.md`. Wynik `nvcc --version` wklej w raporcie. *(dodane 2026-10-29 15:00)*
- [ ] **A8. Zainstaluj pakiety do budowy llama.cpp i uv** (plan Phase 1 krok 3; @phase-0:K4 = A). Polecenia: `AGENTS/phases/phase-1/A8-pakiety-do-budowy-i-uv.md`. *(dodane 2026-10-29 15:00)*
