# Stan projektu

Krótko: co już jest, co teraz robimy, co dalej i jakie decyzje czekają. Agent aktualizuje ten plik na końcu sesji, gdy coś się zmieniło.

*Szablon, 2026-10-29*

---

## Gdzie jesteśmy

- **Cel:** nauka for fun — badania nad kompresją LLM (kwantyzacja, pruning, rozkłady niskiego rzędu, destylacja) na rodzinie **Qwen3** (0.6B → 1.7B → 4B → 8B). Pełny kontekst z rozmowy 27–29.10.2026: `local-llm-conversation.md`.
- **Sprzęt:** RTX 4070 SUPER 12 GB (sm_89), Ryzen 7 9700X, 30 GiB RAM, Fedora 44, zsh z oh-my-zsh, GCC 16, sterownik NVIDIA 615.78.08 (RPM Fusion, nie ruszamy). Python systemowy 3.14.8. Miniconda 26.3.2 w `~/miniconda3` (init tylko w bashu, @T004); `uv` nie jest zainstalowane.
- **Zrobione:** diagnoza systemu; lokalne repo git (`main`, `.gitignore`), pierwszy commit 2026-10-29.
- **Niezrobione:** usunięcie CUDA 12.8/12.9, CUDA 13.4 (nie 13.2 — błąd na niskobitowych kwantach), llama.cpp. Kroki z `sudo` wykonuje autor.
- **GitHub:** decyzja @phase-0:K1 = B, prywatne repo `Qwen3-Family-research` (konto Karolcha100). Moje `gh repo create` zostało zablokowane przez uprawnienia → zadanie @A1 dla autora. Push w kolejnych sesjach: @phase-0:K17.
- **Fazy:** @phase-0:K2 = C — rozpisujemy tylko Phase 1 (środowisko, `AGENTS/phases/phase-1/plan.md`, do zatwierdzenia); dalsze fazy rozpisze autor. Phase 0 = pytania startowe.
- **Sędzia odpowiedzi (@T002):** autor chce modelu nagrody/klasyfikatora oceniającego odpowiedzi Qwen3 (~50 pytań, ~16 metryk 0–100 i 0/1), obok KL, lm-eval i evalplus. Projekt: pytania @phase-0:K18–K27.
- **Kod:** Python w najnowszej wersji, z typami, po angielsku, bez komentarzy, pełne nazwy zmiennych.

## Następny krok

1. Autor: @A1 (GitHub), zatwierdzenie planu Phase 1, decyzje K3–K27 (w szczególności K3, K4, K5, K6).
2. Agent po zatwierdzeniu: kroki 5–7 planu Phase 1 (środowisko Pythona) — nie czekają na CUDA.

## Otwarte decyzje autora

- @phase-0:K3–K16 (`agents-issues-1.md`), @phase-0:K17–K27 (`agents-issues-2.md`).
- Plan `AGENTS/phases/phase-1/plan.md`.

*Zmiana: 2026-10-29 — wypełnienie stanu na podstawie `local-llm-conversation.md` — Claude Opus 5.5*
*Zmiana: 2026-10-29 — pytania startowe przeniesione do phase-0 — Claude Opus 5.5*
*Zmiana: 2026-10-29 13:30 — git, decyzje K1/K2, plan Phase 1, conda, sędzia — Claude Opus 5.5*
