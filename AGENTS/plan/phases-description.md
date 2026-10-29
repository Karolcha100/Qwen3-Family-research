# Opis faz

Zakres każdej fazy: cel, co wchodzi, czego nie robimy, kiedy faza jest skończona. Kolejność i statusy: `AGENTS/plan/phases-plans.md`.

*Szablon, 2026-10-29*

---

## Phase 0 — start i organizacja

- **Cel:** decyzje, które ustalają sposób pracy na cały projekt.
- **Zakres:** pytania w `AGENTS/phases/phase-0/agents-issues-*.md` (git i GitHub, narzędzia Pythona, implementacje vs biblioteki, protokół pomiarów, sędzia odpowiedzi).
- **Koniec fazy, gdy:** pytania 🔴 i 🟡 mają decyzje.

## Phase 1 — środowisko

- **Cel:** Qwen3-0.6B działa na GPU w PyTorchu i w llama.cpp; środowisko da się odtworzyć.
- **Zakres:** usunięcie CUDA 12.x, CUDA 13.4, budowa llama.cpp, środowisko Pythona, testy dymne, raport wersji. Plan: `AGENTS/phases/phase-1/plan.md`.
- **Koniec fazy, gdy:** spełnione warunki z sekcji „Koniec fazy” w planie.

## Phase 2+ — rozpisze autor

- Kierunki z `local-llm-conversation.md`: baseline ewaluacji, kwantyzacja, pruning, rozkłady niskiego rzędu, destylacja, sędzia odpowiedzi (@T002).
