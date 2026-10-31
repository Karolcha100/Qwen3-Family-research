# T017 · Plan na kolejną kolejkę

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Generalnie, napisz mi co sądzisz o użyciu tylko mapy kodu z treningiem (ewentualnie najmniejsze kwadraty), z celem za warstwą (nie na samym końcu).

*2026-10-31 23:45 — Autor*

---
---
---

A i jeszcze z mniejszym krokiem (5e-5)

*2026-10-31 23:46 — Autor*

---
---
---

## Co masz zrobić

Nic do decyzji, to tylko opinia (o nic nie pytasz, więc niczego na jej podstawie nie uruchamiam). Jeśli się zgadzasz, przyjmuję to jako przepis na kolejne etapy, a konkretne obliczenia (np. K45) i tak przyjdą jako osobne pytania.

**Krótko: zgadzam się, i to jest dokładnie przepis, którego używaliśmy dla wariantu „w. 13, cel za warstwą”.** Jedna poprawka do Twojego drugiego wpisu: krok $5 \cdot 10^{-5}$ to już nasz krok dla celu za warstwą. Mniejszy krok ($1 \cdot 10^{-5}$) sprawdzałem tylko dla celu na wyjściu, bo tam $5 \cdot 10^{-5}$ był za duży.

Przepis:
1. **start z mapy kodu 75/25:** usuwamy najmniej ważne neurony (@phase-2:K41 = A);
2. **najmniejsze kwadraty** dla `down_proj`;
3. **trening z celem za następną warstwą**, krok $5 \cdot 10^{-5}$, 6 epok (@phase-2:K40 = C).

### Plusy

- **Każdy krok wyraźnie pomaga** (warstwa 13, −40%, KL na Pythonie):

  | Etap | KL na Pythonie | zmiana |
  |---|---|---|
  | samo wycięcie | 0,00586 | |
  | najmniejsze kwadraty | 0,00403 | −31% |
  | 6 epok | 0,00321 | −20% |
  | 16 epok | 0,00306 | −5% |

- **Najmniejsze kwadraty zostawiłbym na stałe, nie „ewentualnie”.** Trwają kilka sekund i dają większą poprawę niż cały trening.
- **Krok $5 \cdot 10^{-5}$ jest dobry dla tego celu.** We wszystkich 10 dotychczasowych treningach tym celem najlepsza była ostatnia epoka. Błąd walidacji spadał prawie w każdej epoce; był tylko jeden drobny wzrost (o ~2%, mapa z etapu 2, −20%). Za duży krok objawiłby się wyraźnymi skokami w górę, a takich nie było. Mniejszy krok tylko spowolniłby trening.
- **Szybko:** ~2,3 min na warstwę (6 epok), wobec ~25 min przy celu na wyjściu.
- **Jedna metoda wszędzie** ułatwia porównania i opis w pracy.

### Minusy i ryzyka

- **Końcowe warstwy prawie nie korzystają z treningu** (warstwa 26: −1% KL). Skoro chcesz zmniejszać głównie środek modelu (@phase-2:K44), to mało ważne.
- **Przy wielu warstwach naraz cel za warstwą nie widzi sumowania się błędów.** Każda warstwa jest uczona na wejściach z oryginalnego modelu, a w zmniejszonym modelu dostanie wejścia już zmienione przez wcześniejsze zmniejszone warstwy. Typowa odpowiedź to zmniejszanie po kolei: dane do treningu warstwy L zbiera się z modelu, w którym warstwy przed L są już zmniejszone. To pytanie zadam, kiedy dojdziemy do wielu warstw, nie teraz.
- **KL nie zawsze idzie w parze z testami kodu** (warstwa 26). Dlatego K43: od teraz obok KL liczę zgodność najbardziej prawdopodobnego tokenu. Pierwsze sprawdzenie właśnie się liczy.

### Rekomendacja

Przyjąć ten przepis bez zmian (mapa 75/25 → najmniejsze kwadraty → 6 epok celem za warstwą, krok $5 \cdot 10^{-5}$) jako domyślny w kolejnych etapach.

*2026-10-31 23:59 — Claude Opus 5.5*

---
---
---
