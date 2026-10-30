# T016 · Generalny Raport z wykresami i statystykami

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Porównaj mi proszę zasadniczo oryginalnego Qwen i naszego względem ostatnich obliczeń (włącznie z tymi dodatkowymi do 17:30)

*2026-10-30 18:31 — Autor*

---
---
---

## Co masz zrobić

Przeczytaj raport **`AGENTS/phases/phase-2/porownanie-z-oryginalem.md`** (Drzewo → Raporty). Uwagi możesz pisać pod raportem albo tutaj.

### Co jest w raporcie

1. Co dokładnie porównuję: oryginał i 4 warianty z jedną zmniejszoną warstwą, w tym oba z dodatkowej kolejki do 17:13.
2. **Liczba rozwiązanych zadań** w HumanEval, HumanEval+, MBPP i MBPP+ (wykres i tabela).
3. **Które zadania się zmieniły:** ile każdy wariant zyskał, a ile stracił względem oryginału, i czy to przypadek (test McNemara).
4. KL, perpleksja, sprawność (parametry, pamięć, szybkość), jakość kodu bez uruchamiania.
5. Wnioski.

Najważniejsze:
- warstwa 26 zmniejszona o 40% rozwiązuje **205** zadań „+” wobec **200** u oryginału, więc nic nie traci;
- warstwa 13 rozwiązuje **184–191**;
- KL i perpleksja pokazują odwrotną kolejność niż testy kodu.

Dalej proponuję dwa obliczenia: pass@2 i pass@3 (**K44**) oraz warstwy najtańsze według mapy (**K45**), w `AGENTS/phases/phase-2/agents-issues-9.md`.

*2026-10-30 18:39 — Claude Opus 5.5*

---
---
---
