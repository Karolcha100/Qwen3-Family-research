# Stan projektu

Krótko: co już jest, co teraz robimy, co dalej i jakie decyzje czekają. Agent aktualizuje ten plik na końcu sesji, gdy coś się zmieniło.

*Szablon, 2026-10-29*

---

## Gdzie jesteśmy

- **Cel:** nauka for fun — badania nad kompresją LLM (kwantyzacja, pruning, rozkłady niskiego rzędu, destylacja) na rodzinie **Qwen3** (0.6B → 1.7B → 4B → 8B). Pełny kontekst z rozmowy 27–29.10.2026: `local-llm-conversation.md`.
- **Sprzęt:** RTX 4070 SUPER 12 GB (sm_89), Ryzen 7 9700X, 30 GiB RAM, Fedora 44, zsh, GCC 16, sterownik NVIDIA 615.78.08 (RPM Fusion, nie ruszamy).
- **Zrobione:** diagnoza systemu.
- **Niezrobione:** usunięcie CUDA 12.8/12.9, instalacja CUDA 13.4 (nie 13.2 — błąd na niskobitowych kwantach), kompilacja llama.cpp. Kroki z `sudo` wykonuje autor; polecenia są w `local-llm-conversation.md`.
- **W repozytorium:** tylko `AGENTS/`, `agents_board/`, `tests/`, `CLAUDE.md`, `local-llm-conversation.md`. Brak kodu badawczego. Katalog **nie jest repozytorium git** (stan na 2026-10-29) — commit po sesji i `git diff` nie działają, dopóki autor nie zgodzi się na `git init` (@phase-0:K1).
- **Ewaluacja (plan):** perplexity WikiText-2 i C4, KL względem BF16, lm-evaluation-harness, evalplus.
- **Kod:** Python w najnowszej wersji, z typami, po angielsku, bez komentarzy, pełne nazwy zmiennych.

## Następny krok

1. Decyzje autora w `AGENTS/phases/phase-0/agents-issues-1.md` (K1–K16). Potem: `git init` (K1), plan faz do zatwierdzenia (K2), zadania A na instalację (K3).

## Otwarte decyzje autora

- @phase-0:K1–K16: git, plan faz, instalacja, uv i wersja Pythona, własne implementacje czy biblioteki, Base czy instruct, kalibracja, protokół perplexity, kto uruchamia GPU, zapis wyników, struktura kodu, model-sędzia (z @T002), narzędzia jakości, notatki do nauki, folder phase-0.

*Zmiana: 2026-10-29 — wypełnienie stanu na podstawie `local-llm-conversation.md` — Claude Opus 5.5*
*Zmiana: 2026-10-29 — pytania startowe przeniesione do phase-0 — Claude Opus 5.5*
