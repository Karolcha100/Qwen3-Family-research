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

## Phase 2 — mapa neuronów i zmniejszenie jednej warstwy (główny pomysł, etapy 1–4)

- **Cel:** zmierzyć ważność każdego z 86 016 neuronów MLP Qwen3-0.6B, opisać ich rodzaje w warstwach, sprawdzić zmniejszanie jednej warstwy z rekonstrukcją.
- **Zakres i koniec fazy:** `AGENTS/phases/phase-pomysl/plan-phase-2.md`. Uzasadnienie: `AGENTS/phases/phase-pomysl/raport-1-opis-matematyczny.md`, `raport-2-opinia.md`.

## Phase 3 — wiele warstw, dotrenowanie, ewaluacja (etapy 5–6)

- Do rozpisania po Phase 2. Zmniejszanie wielu warstw, porównanie z prostą ważnością, dotrenowanie (@phase-pomysl:K8 = D), pełna ewaluacja (poziomy 1–3, @T002).
