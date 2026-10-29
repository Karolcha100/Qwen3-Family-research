# Fazy — jak wyglądają pliki

Każda faza ma swój folder `AGENTS/phases/phase-<nazwa>/` (np. `phase-1`, `phase-2.1`). Tam leży wszystko o tej fazie: plan, raporty, pytania agentów.

*Szablon, 2026-10-29*

---

## Pytania agentów do autora: `agents-issues-N.md`

GUI szuka pytań tylko w plikach `AGENTS/phases/<faza>/agents-issues-N.md`. Pytanie to sekcja:

```
### K1. 🔴 Krótki tytuł

- **Problem:** prostymi słowami, co trzeba zdecydować.
- **Opcje:**
  - **A** — … (plusy, minusy);
  - **B** — … (plusy, minusy).
- **Rekomendacja:** B, bo …
- **Decyzja:**
```

- Puste pole **Decyzja** = pytanie czeka na autora („Co czeka na mnie → Pytania bez decyzji”).
- Kolor: 🔴 blokuje pracę, 🟡 ważne, 🟢 drobne.
- Wzmianka w tekście: `@phase-1:K1`.
- Autor wpisuje decyzję w GUI albo przenosi pytanie do zadania (Decyzja `⏳ w toku → @A12`).

## Plan fazy do zatwierdzenia

Plik np. `AGENTS/phases/phase-1/plan.md`, w tej kolejności:

1. tytuł `# Phase 1 — plan` i podpis `*RRRR-MM-DD GG:MM — model*`;
2. osobna linia, od początku wiersza: `**Status planu:** do zatwierdzenia`;
3. `## Co masz zrobić` — np. „Przeczytaj plan i zatwierdź (✅ Zatwierdzam plan) albo napisz w dyskusji, co zmienić.”;
4. treść planu;
5. na końcu pusta sekcja `## Dyskusja` (wpisy jak w wątkach).

`do opiniowania` zamiast `do zatwierdzenia` = plan, o którym autor tylko się wypowiada. Status `zatwierdzony (…)` ustawia autor w GUI.

Uwaga: GUI uznaje za plan **każdy** plik z linią zaczynającą się od `**Status planu:**` — nawet w bloku kodu. W przykładach pisz ją w środku zdania, jak wyżej.
