# Phase 0 — pytania (runda 7): narzędzia agenta

*2026-10-29 16:56 — Claude Opus 5.5*

## Co masz zrobić

Jedna decyzja wynikająca z @T006. Nie blokuje niczego. Wystarczy „rek” albo litera.

---

### K43. 🟢 Polecenia agenta: notatki czy mały skrypt

- **Problem:** powtarzalne czynności agenta (dopisanie wpisu do wątku, blok odpowiedzi w raporcie, indeks decyzji, sprawdzenie GUI) opisałem jako gotowe polecenia w `AGENTS/memory/procedury.md`. Działają, ale każdy agent przepisuje je ręcznie, a przy przepisywaniu łatwo o błąd.
- **Opcje:**
  - **A** — zostają notatki z poleceniami w `procedury.md` (bez nowego kodu);
  - **B** — mały skrypt `agents_board/agent_tools.py` (np. `python3 -m agents_board.agent_tools reply-thread T006 wpis.md`) z testami w `tests/`, korzystający z kodu GUI (`agents_board/model.py`). Nie zmienia formatów plików ani działania GUI;
  - **C** — A teraz, B dopiero wtedy, gdy któraś notatka zawiedzie albo zacznie się powtarzać błąd.
- **Rekomendacja:** C. Dziś notatki wystarczą, a skrypt to nowy kod do utrzymania. Jeśli pojawi się błąd przy dopisywaniu, przejdę na B.
- **Decyzja:** C
