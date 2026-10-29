# WAŻNE — TODO dla autora

Rzeczy, które blokują dalszą pracę agentów. Zasady (numeracja `A…`, statusy, raporty): `AGENTS/todo/author/INSTRUKCJA.md`.

*Szablon, 2026-10-29*

---

- [x] **A1. Utwórz prywatne repozytorium GitHub „Qwen3-Family-research”** (decyzja @phase-0:K1 = B). Lokalne repo i pierwszy commit już są, ale moje polecenie `gh repo create` zablokowały uprawnienia Claude Code (wysyłanie danych na zewnątrz). Uruchom w katalogu projektu:
  `gh repo create Qwen3-Family-research --private --source=. --remote=origin --push`
  Potem `gh repo view --json visibility,url` powinno pokazać `PRIVATE`. Napisz w raporcie „zrobione” (albo wklej błąd). Kto pushuje w kolejnych sesjach: @phase-0:K17.
  *(zrobione: 2026-10-29 13:54 według raportu autora; sprawdzone przez agenta: `origin` = github.com/Karolcha100/Qwen3-Family-research, `main` zsynchronizowany)*
