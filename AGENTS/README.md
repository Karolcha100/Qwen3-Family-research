# AGENTS — mapa

Wszystko, co dotyczy współpracy autora z agentami LLM (Claude Code): plany, fazy, pytania i decyzje, zadania, rozmowy, pamięć projektu.
Najwygodniej przeglądasz to w przeglądarce: `python3 -m agents_board` (drzewo + odpowiadanie, instrukcja pod przyciskiem „❓ Instrukcja”).

*Szablon z projektu economics-model-pol-vs-rus, 2026-10-29. Agenci aktualizują ten plik przy każdej zmianie struktury.*

---

## Struktura

```
AGENTS/
  README.md                       ← ten plik
  memory/                         pamięć projektu: stan, zasady współpracy, pułapki (agent czyta na starcie sesji)
  plan/
    phases-plans.md               kolejność faz i statusy (przycisk „🗺️ Plan” w GUI; aktualizują agenci)
    phases-description.md         zakres faz
    future-work.md                pomysły na później
  phases/
    phase-<nazwa>/                wszystko o jednej fazie: plany, raporty, pytania agentów (agents-issues-N.md)
  todo/
    author/                       zadania autora A… (WAŻNE / ŚREDNIE / MAŁE), raport autora, instrukcja
    llm/                          zadania agentów L…, raport agentów, instrukcja dla agentów
  talk/
    od-autora-dla-llmow.md        ogólne uwagi autora (agenci tylko oznaczają jako przeczytane)
    threads/T001-….md             rozmowy: jeden temat = jeden wątek; odgałęzienia, zamykanie 🔒
    briefings/RRRR-MM-DD-GGMM.md  podsumowanie każdej sesji agenta (to samo, co w okienku czatu)
    koniec/RRRR-MM-DD-GGMM.md     lista odpowiedzi autora z jednej sesji (przycisk ✅ Koniec)
```

## Zasady

1. **Wszystko o jednej fazie leży w jej folderze** w `phases/`. W `todo/` i `talk/` są tylko rzeczy wspólne dla wielu faz.
2. **Pytania agentów:** `phases/<faza>/agents-issues-N.md`, każde z polem **Decyzja** dla autora. Każda nowa runda pytań to kolejny numer N.
3. **Zadania:** autor `A…`, agenci `L…`. Statusy `[ ]` `[~]` `[x]` `[?]` `[>]` `[-]`; nic nie jest usuwane. Szczegóły: `AGENTS/todo/author/INSTRUKCJA.md`, `AGENTS/todo/llm/INSTRUKCJA.md`.
4. **Wcześniejszych wpisów się nie edytuje** (wątki, raporty, decyzje). Nowe dopisuje się na końcu.
5. **Bez polskich znaków w nazwach plików** (treść po polsku).
6. **Plan do zatwierdzenia:** dowolny plik z linią `**Status planu:** do zatwierdzenia` (albo `do opiniowania`) i sekcją `## Dyskusja` na końcu — GUI pokazuje go w zakładce „Plany”.

## GUI: `python3 -m agents_board`

- Otwiera przeglądarkę na `http://127.0.0.1:8765/`. Tylko podgląd: `--read-only`; jeden plik HTML bez serwera: `--static plik.html`.
- Wszystko, co autor wpisze w GUI, trafia do zwykłych plików `.md` w tym folderze.
- Pełna instrukcja obsługi: `agents_board/HELP.md` (w GUI: „❓ Instrukcja”).
