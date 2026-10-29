# Stan projektu

Krótko: co już jest, co teraz robimy, co dalej i jakie decyzje czekają. Agent aktualizuje ten plik na końcu sesji, gdy coś się zmieniło.

*Szablon, 2026-10-29*

---

## Gdzie jesteśmy

- **Cel:** nauka for fun — badania nad kompresją LLM (kwantyzacja, pruning, rozkłady niskiego rzędu, destylacja) na rodzinie **Qwen3** (0.6B → 1.7B → 4B → 8B). Pełny kontekst z rozmowy 27–29.10.2026: `local-llm-conversation.md`.
- **Sprzęt:** RTX 4070 SUPER 12 GB (sm_89), Ryzen 7 9700X, 30 GiB RAM, Fedora 44, zsh z oh-my-zsh, GCC 16, sterownik NVIDIA 615.78.08 (RPM Fusion, nie ruszamy). Python systemowy 3.14.8. Miniconda w `~/miniconda3` (zsh init zrobiony, `auto_activate` wyłączone) — tylko zapas.
- **Repo:** `github.com/Karolcha100/Qwen3-Family-research` (prywatne). Commit + push po każdej sesji (@phase-0:K17 = B); pozwolenie `Bash(git push)` w `.claude/settings.json` (@A5).
- **Decyzje (phase-0):** K1 GitHub; K2 rozpisujemy tylko Phase 1, dalsze fazy autor; K3 instalacje z `sudo` jako zadania A (@A6–@A8); K4 **uv**; K5 **Python 3.14**; K6 **gotowe biblioteki, metody wybiera autor**; K10 agent pisze kod, **uruchamia na GPU tylko na „uruchom” autora**; K11 wyniki w `results/*.jsonl`; K12 pakiet `src/…` „spoko”, ale **struktura dopiero po wyborze metod**; K15 notatki do nauki przy każdej metodzie; K16 `phase-0` na pytania ogólne; K17 commit + push; K30 zapisujemy tylko wybrane checkpointy (poza repo). K32 kalibracja zawsze C4; K33 bez „uruchom” wolno instalować, budować i pobierać (po zatwierdzeniu planu), GPU tylko na „uruchom”; K34 katalog metod + propozycja (`AGENTS/phases/phase-0/katalog-metod.md`, L1); K35 szum ziaren mierzony raz na 0.6B. K7 = A (Base do perplexity/KL/lm-eval, instrukcyjny do evalplus/IFEval/klasyfikatorów); K8 = C (kalibracja: mieszanka C4 + kod), ale **autor ma główny pomysł, inny niż klasyczna kwantyzacja, jeszcze nieopisany**; K9 = A (okna 2048 bez nakładania); K14 = A (ruff, pyright, pytest).
- **Phase 1 (środowisko):** plan `AGENTS/phases/phase-1/plan.md` **zatwierdzony 2026-10-29 19:39**; llama.cpp sklonowane do `~/llama.cpp`; @A6 zrobione (CUDA 12 usunięta 2026-10-29 20:04, 208 GB wolnego); zadania autora @A6 (usunięcie CUDA 12, 117 pakietów), @A7 (CUDA 13.4), @A8 (pakiety + uv).
- **Ewaluacja (@T002):** 1) perplexity + KL, 2) lm-eval (z IFEval) + evalplus, 3) **klasyfikatory, bez sędziów generatywnych**: 4 reguły (K28) + wieloatrybutowy model nagrody (K29 = B, np. ArmoRM; wybór modelu: K18 „do rozważenia”). 200 pytań po angielsku (K21, K23), mieszanka źródeł (K22), sampling 3 odpowiedzi (K24), **tryb myślenia włączony** (K25), ocena bezwzględna + parami z BF16 (K20), ręczna kalibracja ~50 odpowiedzi w HTML (K26). Lista metryk: `AGENTS/phases/phase-0/plan-metryki-oceny.md` (do opiniowania). K37 limit 8192 tokenów; K38 model nagrody widzi tylko odpowiedź końcową; K39 bez pytań IFEval w naszych 200 (@T005); K40 metryka zgodności z wzorcem. K36: porównanie z BF16 + percentyle + ranking Elo (sekcja D planu metryk). K41 = C: 80 MT-Bench + 60 Arena-Hard + 40 AlpacaEval + 20 własnych; K42 = B: obie tury MT-Bench (druga oceniana osobno).
- **Kod:** Python 3.14, z typami, po angielsku, bez komentarzy, pełne nazwy zmiennych.

## Następny krok

1. Autor: @A7, @A8; potem **opis głównego pomysłu**, wybór metod i opis faz, opinia o planie metryk (lista: @T007).
2. Agent: zadania L2–L11 w `AGENTS/todo/llm/TODO-dla-LLM.md` (co czeka na co: `AGENTS/memory/w-toku.md`). Bez blokad: L8 (przegląd modeli nagrody).

## Otwarte decyzje autora

- brak otwartych pytań (K43 = C: zostają notatki w `procedury.md`); czekają zadania @A7, @A8 i główny pomysł autora.
- Plany: `AGENTS/phases/phase-1/plan.md` (zatwierdzenie), `AGENTS/phases/phase-0/plan-metryki-oceny.md` i `AGENTS/phases/phase-0/katalog-metod.md` (opinia).

*Zmiana: 2026-10-29 15:03 — decyzje K3–K17, zadania A5–A8, raporty A2–A4 — Claude Opus 5.5*
*Zmiana: 2026-10-29 15:45 — decyzje K11–K31, ocena klasyfikatorami — Claude Opus 5.5*
*Zmiana: 2026-10-29 16:23 — decyzje K32–K40, katalog metod, push skonfigurowany — Claude Opus 5.5*
*Zmiana: 2026-10-29 16:56 — K41/K42, notatniki agenta (@T006) — Claude Opus 5.5*
*Zmiana: 2026-10-29 19:33 — K7/K8/K9/K14/K36 zamknięte, główny pomysł autora — Claude Opus 5.5*
*Zmiana: 2026-10-29 19:49 — plan Phase 1 zatwierdzony, llama.cpp sklonowane, raport ASVD/SVD-LLM — Claude Opus 5.5*
