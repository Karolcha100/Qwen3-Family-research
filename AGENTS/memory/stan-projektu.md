# Stan projektu

Krótko: co już jest, co teraz robimy, co dalej i jakie decyzje czekają. Agent aktualizuje ten plik na końcu sesji, gdy coś się zmieniło.

*Szablon, 2026-10-29*

---

## Gdzie jesteśmy

- **Cel:** nauka for fun — badania nad kompresją LLM (kwantyzacja, pruning, rozkłady niskiego rzędu, destylacja) na rodzinie **Qwen3** (0.6B → 1.7B → 4B → 8B). Pełny kontekst z rozmowy 27–29.10.2026: `local-llm-conversation.md`.
- **Sprzęt:** RTX 4070 SUPER 12 GB (sm_89), Ryzen 7 9700X, 30 GiB RAM, Fedora 44, zsh z oh-my-zsh, GCC 16, sterownik NVIDIA 615.78.08 (RPM Fusion, nie ruszamy). Python systemowy 3.14.8. Miniconda w `~/miniconda3` (zsh init zrobiony, `auto_activate` wyłączone) — tylko zapas.
- **Repo:** `github.com/Karolcha100/Qwen3-Family-research` (prywatne). Commit + push po każdej sesji (@phase-0:K17 = B); stałe pozwolenie na push czeka na @A5.
- **Decyzje (phase-0):** K1 GitHub; K2 rozpisujemy tylko Phase 1, dalsze fazy autor; K3 instalacje z `sudo` jako zadania A (@A6–@A8); K4 **uv**; K5 **Python 3.14**; K6 **gotowe biblioteki, metody wybiera autor**; K10 agent pisze kod, **uruchamia na GPU tylko na „uruchom” autora**; K11 wyniki w `results/*.jsonl`; K12 pakiet `src/…` „spoko”, ale **struktura dopiero po wyborze metod**; K15 notatki do nauki przy każdej metodzie; K16 `phase-0` na pytania ogólne; K17 commit + push; K30 zapisujemy tylko wybrane checkpointy (poza repo). W toku: K7/K8/K9 → @A2/@A3/@A4 (raporty w `AGENTS/phases/phase-0/A2…A4-*.md`), K14 → @A9 (wyjaśnione, rekomendacja A).
- **Phase 1 (środowisko):** plan `AGENTS/phases/phase-1/plan.md` do zatwierdzenia; zadania autora @A6 (usunięcie CUDA 12, 117 pakietów), @A7 (CUDA 13.4), @A8 (pakiety + uv).
- **Ewaluacja (@T002):** 1) perplexity + KL, 2) lm-eval (z IFEval) + evalplus, 3) **klasyfikatory, bez sędziów generatywnych**: 4 reguły (K28) + wieloatrybutowy model nagrody (K29 = B, np. ArmoRM; wybór modelu: K18 „do rozważenia”). 200 pytań po angielsku (K21, K23), mieszanka źródeł (K22), sampling 3 odpowiedzi (K24), **tryb myślenia włączony** (K25), ocena bezwzględna + parami z BF16 (K20), ręczna kalibracja ~50 odpowiedzi w HTML (K26). Lista metryk: `AGENTS/phases/phase-0/plan-metryki-oceny.md` (do opiniowania). Otwarte: K35–K40.
- **Kod:** Python 3.14, z typami, po angielsku, bez komentarzy, pełne nazwy zmiennych.

## Następny krok

1. Autor: zatwierdzenie planu Phase 1, @A6–@A8, wybory w @A2–@A4 i @A9, opis dalszych faz i metod, pytania K32–K40 (najpilniejsze K33), opinia o planie metryk.
2. Agent po zatwierdzeniu planu i @A8: kroki 5–6 (środowisko uv); po @A7: budowa llama.cpp; GPU tylko po „uruchom”.
3. Agent: katalog metod, jeśli @phase-0:K34 = A/B.

## Otwarte decyzje autora

- `AGENTS/phases/phase-0/agents-issues-4.md` (K32–K34), `-5.md` (K35–K40); @A2–@A4, @A9.
- Plany: `AGENTS/phases/phase-1/plan.md` (zatwierdzenie), `AGENTS/phases/phase-0/plan-metryki-oceny.md` (opinia).

*Zmiana: 2026-10-29 15:03 — decyzje K3–K17, zadania A5–A8, raporty A2–A4 — Claude Opus 5.5*
*Zmiana: 2026-10-29 15:45 — decyzje K11–K31, ocena klasyfikatorami — Claude Opus 5.5*
