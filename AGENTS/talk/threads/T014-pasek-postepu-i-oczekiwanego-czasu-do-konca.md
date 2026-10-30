# T014 · Pasek postępu i oczekiwanego czasu do końca

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Chciałbym ciebie prosić o jakiś pasek postępu (ile % obliczeń zostało zrobionych) wraz z informacją ile czasu upłyneło oraz jaki jest oczekiwany od teraz czas do zakończenia działania obliczeń.

*2026-10-30 14:19 — Autor*

---
---
---

## Co masz zrobić

**Uruchom ponownie AGENTS board** (zatrzymaj `python3 -m agents_board` i włącz go jeszcze raz), bo zmieniłem część serwera. Pasek pojawi się, gdy zacznie się liczyć kolejka (@phase-2:K39). Jeśli coś w pasku chcesz inaczej, napisz tutaj.

### Zrobione: pasek postępu w GUI

![Pasek postępu](AGENTS/talk/threads/T014-pasek.png)

(zrzut z przykładowymi danymi: kolejka K31–K38 po 40 minutach)

W drugiej linii górnego paska, tylko gdy coś się liczy, widać:
- **pasek i procent** zrobionej pracy, liczony według czasu: ile minęło / (ile minęło + ile zostało);
- **krok N z M** i nazwę bieżącego kroku, a w nawiasie, ile procent tego kroku zgłosił skrypt (np. kolejne epoki treningu);
- **minęło** od startu, **zostało** i **o której** mniej więcej koniec;
- po najechaniu myszą listę kroków: ✅ zrobione, ⏳ trwa, ❌ nieudane, · czeka.

Odświeża się sam co 15 s, bez przycisku „Odśwież”.

**Jak liczę „zostało”.** Każdy krok kolejki ma mój szacowany czas. W trakcie pracy szacunek jest poprawiany na dwa sposoby:
- jeśli skończone kroki trwały np. 1,2× dłużej, niż szacowałem, czekające kroki też liczę 1,2× dłużej;
- dla bieżącego kroku, gdy skrypt zgłosi co najmniej 5% postępu, biorę jego własne tempo, np. 25% w 10 min, więc całość ~40 min.

**Ostrzeżenia:**
- kolor pomarańczowy i „⚠️ brak sygnału od N min”: od 3 minut nic nie zapisało postępu, więc obliczenia mogły się przerwać;
- „❌ nieudane: …” to kroki, które skończyły się błędem; kolejka idzie wtedy dalej, bo kroki są od siebie niezależne;
- zielony pasek: koniec, z godziną i całkowitym czasem.

Od teraz każde dłuższe obliczenie uruchamiam w ten sposób (zapisane w instrukcji dla agenta).

Pliki: `agents_board/model.py` (liczenie procentu i czasu, z testami), `agents_board/server.py` (`/api/progress`), `agents_board/static/index.html` (pasek), `scripts/run_queue.py` (uruchamia kroki i zapisuje postęp do `AGENTS/postep-obliczen.json`, pliku poza gitem), `src/qwen_compression/progress.py`.

*2026-10-30 14:26 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-10-30 17:59 — Autor*

---
---
---
