# WAŻNE — TODO dla autora

Rzeczy, które blokują dalszą pracę agentów. Zasady (numeracja `A…`, statusy, raporty): `AGENTS/todo/author/INSTRUKCJA.md`.

*Szablon, 2026-10-29*

---

- [x] **A1. Utwórz prywatne repozytorium GitHub „Qwen3-Family-research”** (decyzja @phase-0:K1 = B). Lokalne repo i pierwszy commit już są, ale moje polecenie `gh repo create` zablokowały uprawnienia Claude Code (wysyłanie danych na zewnątrz). Uruchom w katalogu projektu:
  `gh repo create Qwen3-Family-research --private --source=. --remote=origin --push`
  Potem `gh repo view --json visibility,url` powinno pokazać `PRIVATE`. Napisz w raporcie „zrobione” (albo wklej błąd). Kto pushuje w kolejnych sesjach: @phase-0:K17.
  *(zrobione: 2026-10-29 13:54 według raportu autora; sprawdzone przez agenta: `origin` = github.com/Karolcha100/Qwen3-Family-research, `main` zsynchronizowany)*
- [x] **A2. K7: 🟡 Qwen3 Base czy wersja instrukcyjna** — z pytania @phase-0:K7 (`phases/phase-0/agents-issues-1.md`). *(dodane 2026-10-29 14:52)*
  Raport agenta: `AGENTS/phases/phase-0/A2-base-czy-instrukcyjna.md` — wybór napisz w raporcie pod @A2. *(agent, 2026-10-29 15:03)*
  *(zamknięte przez agenta: 2026-10-29 19:33 — decyzja końcowa autora: K7 = A)*
- [x] **A3. K8: 🟡 Dane kalibracyjne** — z pytania @phase-0:K8 (`phases/phase-0/agents-issues-1.md`). *(dodane 2026-10-29 14:53)*
  Raport agenta: `AGENTS/phases/phase-0/A3-dane-kalibracyjne.md` — wybór napisz w raporcie pod @A3. *(agent, 2026-10-29 15:03)*
  *(zamknięte przez agenta: 2026-10-29 19:33 — decyzja końcowa autora: K8 = C)*
- [x] **A4. K9: 🟡 Protokół perplexity** — z pytania @phase-0:K9 (`phases/phase-0/agents-issues-1.md`). *(dodane 2026-10-29 14:54)*
  Raport agenta: `AGENTS/phases/phase-0/A4-perplexity.md` — wybór napisz w raporcie pod @A4. *(agent, 2026-10-29 15:03)*
  *(zamknięte przez agenta: 2026-10-29 19:33 — decyzja końcowa autora: K9 = A)*
- [x] **A6. Usuń CUDA 12.8 i 12.9** (decyzja @phase-0:K3 = A, plan Phase 1 krok 1). Polecenia i co sprawdzić: `AGENTS/phases/phase-1/A6-usuniecie-cuda-12.md`. Wynik kroku 4 wklej w raporcie. *(dodane 2026-10-29 15:00)*
  *(zrobione: 2026-10-29 20:04 według raportu autora; sprawdzone przez agenta: brak pakietów, katalogów, repozytoriów i wpisów CUDA 12)*
- [x] **A7. Zainstaluj CUDA 13.4 (sam toolkit)** — po @A6 (plan Phase 1 krok 2). Polecenia: `AGENTS/phases/phase-1/A7-instalacja-cuda-13-4.md`. Wynik `nvcc --version` wklej w raporcie. *(dodane 2026-10-29 15:00)*
  *(zrobione: 2026-10-29 20:12 według raportu autora; sprawdzone przez agenta: nvcc 13.4.92, PATH, ld.so.conf, zgodność z GCC 16)*
- [x] **A8. Zainstaluj pakiety do budowy llama.cpp i uv** (plan Phase 1 krok 3; @phase-0:K4 = A). Polecenia: `AGENTS/phases/phase-1/A8-pakiety-do-budowy-i-uv.md`. *(dodane 2026-10-29 15:00)*
  *(agent, 2026-10-29 20:12: pakiety do budowy już są w systemie — wystarczy `sudo dnf install uv`)*
  *(zrobione: 2026-10-29 20:19 według raportu autora; uv 0.12.24 sprawdzone przez agenta)*
- [x] **A9. K14: 🟢 Narzędzia jakości kodu** — z pytania @phase-0:K14 (`phases/phase-0/agents-issues-1.md`). *(dodane 2026-10-29 15:38)*
  *(zamknięte przez agenta: 2026-10-29 19:33 — decyzja końcowa autora: K14 = A)*
- [x] **A10. K36: 🟡 (ponowione K19) Jak zamienić wynik modelu nagrody na 0–100** — z pytania @phase-0:K36 (`phases/phase-0/agents-issues-5.md`). *(dodane 2026-10-29 16:18)*
  *(zamknięte przez agenta: 2026-10-29 19:33 — decyzja końcowa autora: K36 = porównanie z BF16 + percentyle + Elo)*
