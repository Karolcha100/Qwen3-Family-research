# T011 · Czemu piszesz o wycinaniu neuronów

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Ja tylko przypomnę że my nie mamy tyle co wycinać mało ważne neurony, co raczej trenować zmniejszone warstwy by odtwarzały te oryginalne

*2026-10-30 11:01 — Autor*

---
---
---

## Co masz zrobić

Odpowiedz na @phase-2:K31 (`AGENTS/phases/phase-2/agents-issues-5.md`): czy sprawdzamy, ile daje punkt startu zmniejszonej warstwy, a ile trening. Rekomenduję A.

### 1. Masz rację: pisałem tak, jakby celem było wycinanie

W etapie 4 zmniejszona warstwa powstaje w trzech krokach:
1. **start:** zmniejszona warstwa zaczyna od części neuronów oryginału (np. 60% przy zmniejszeniu o 40%); mapa ważności mówi tylko, **od których** neuronów zacząć;
2. **najmniejsze kwadraty:** nowe wagi wyjścia, żeby pozostałe neurony przejęły pracę reszty;
3. **trening:** wszystkie wagi zmniejszonej warstwy uczą się odtwarzać oryginał, mierzone za następną warstwą.

Trzeci krok jest właściwym celem, a pierwszy tylko punktem startu. Od teraz piszę „zmniejszanie warstwy” i „start z …”, a nie „wycinanie”. Stare raporty zostawiam bez zmian; ten wpis wyjaśnia, jak je czytać.

### 2. Co z tego wynika

- **Kluczowe pytanie:** czy po porządnym treningu punkt startu ma jeszcze znaczenie. Przy krótkim treningu (4 epoki) ma: start z mapy przesiewu dawał po treningu o 17–37% mniejszą KL niż start według średniej aktywacji. Ale trening był za krótki (w 6 z 8 przebiegów najlepsza była ostatnia epoka).
- **Jeśli przy długim treningu start przestaje mieć znaczenie,** mapa ważności jest mało potrzebna, a cały wysiłek idzie w trening (dane, czas, sposób).
- **Jeśli start nadal ma znaczenie,** opłaca się start, który zachowuje jak najwięcej oryginału. Na przykład zamiast wyrzucać neurony, można **łączyć** podobne neurony w jeden, żeby nic nie przepadało od razu.

Dlatego pytanie @phase-2:K31: porównanie startów (mapa, średnia aktywacja, losowy, połączone neurony) przy tym samym długim treningu.

### 3. Co już się liczy w tym kierunku

Pod Twoją nieobecność liczy się m.in. @phase-2:K23, czyli dłuższy trening warstwy 13 (16 epok, dwa kroki uczenia). Trening zapisuje teraz stratę po każdej epoce, więc będzie widać, czy dalej się poprawia. Szczegóły i wyniki: @T012.

*2026-10-30 11:10 — Claude Opus 5.5*

---
---
---
