# Stan projektu

Krótko: co już jest, co teraz robimy, co dalej i jakie decyzje czekają. Agent aktualizuje ten plik na końcu sesji, gdy coś się zmieniło.

*Szablon, 2026-10-29*

---

## Gdzie jesteśmy

- **Cel:** nauka for fun — badania nad kompresją LLM (kwantyzacja, pruning, rozkłady niskiego rzędu, destylacja) na rodzinie **Qwen3** (0.6B → 1.7B → 4B → 8B). Pełny kontekst z rozmowy 27–29.10.2026: `local-llm-conversation.md`.
- **Sprzęt:** RTX 4070 SUPER 12 GB (sm_89), Ryzen 7 9700X, 30 GiB RAM, Fedora 44, zsh z oh-my-zsh, GCC 16, sterownik NVIDIA 615.78.08 (RPM Fusion, nie ruszamy). Python systemowy 3.14.8. Miniconda w `~/miniconda3` (zsh init zrobiony, `auto_activate` wyłączone) — tylko zapas.
- **Repo:** `github.com/Karolcha100/Qwen3-Family-research` (prywatne). Commit + push po każdej sesji (@phase-0:K17 = B); stałe pozwolenie na push czeka na @A5.
- **Decyzje (phase-0):** K1 GitHub; K2 rozpisujemy tylko Phase 1, dalsze fazy autor; K3 instalacje z `sudo` jako zadania A (@A6–@A8); K4 **uv**; K5 **Python 3.14**; K6 **gotowe biblioteki, metody wybiera autor**; K10 agent pisze kod, **uruchamia na GPU tylko na „uruchom” autora**; K13 sędzia = model nagrody (do dopracowania, K18–K30). K7/K8/K9 → @A2/@A3/@A4 (raporty edukacyjne w `AGENTS/phases/phase-0/A2…A4-*.md`, czekają na wybór).
- **Phase 1 (środowisko):** plan `AGENTS/phases/phase-1/plan.md` do zatwierdzenia; zadania autora @A6 (usunięcie CUDA 12, 117 pakietów), @A7 (CUDA 13.4), @A8 (pakiety + uv).
- **Ewaluacja warstwami (@T002):** 1) perplexity + KL, 2) lm-eval (z IFEval) + evalplus, 3) sędzia na ~50 pytaniach otwartych.
- **Kod:** Python 3.14, z typami, po angielsku, bez komentarzy, pełne nazwy zmiennych.

## Następny krok

1. Autor: zatwierdzenie planu Phase 1, @A6–@A8, wybory w @A2–@A4, pytania K11–K16, K18–K34 (najpilniejsze K33).
2. Agent po zatwierdzeniu planu i @A8: kroki 5–6 (środowisko uv); po @A7: budowa llama.cpp; GPU tylko po „uruchom”.
3. Agent: katalog metod, jeśli @phase-0:K34 = A/B.

## Otwarte decyzje autora

- `AGENTS/phases/phase-0/agents-issues-1.md` (K11, K12, K14–K16), `-2.md` (K18–K27), `-3.md` (K28–K30), `-4.md` (K31–K34); @A2–@A4.
- Plan `AGENTS/phases/phase-1/plan.md`.

*Zmiana: 2026-10-29 15:03 — decyzje K3–K17, zadania A5–A8, raporty A2–A4 — Claude Opus 5.5*
