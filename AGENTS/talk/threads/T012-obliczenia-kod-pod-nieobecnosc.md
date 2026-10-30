# T012 · Obliczenia pod Twoją nieobecność: Python i dłuższy trening

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

## Co masz zrobić

Nic, dopóki nie skończy się liczyć. Wyniki dopiszę w tym wątku. Pozwoliłeś liczyć na CPU i GPU pod Twoją nieobecność (wiadomość w czacie, ~11:00), więc puściłem to, co wynika z dzisiejszych decyzji. Jeśli coś z tego jest nie po Twojej myśli, napisz tutaj.

### 1. Co się liczy (jedno po drugim na GPU)

| Krok | Skąd decyzja | Co | Czas |
|---|---|---|---|
| 1 | @phase-2:K23 = A | warstwa 13, zmniejszenie o 20% i 40%: trening 16 epok, osobno z krokiem uczenia $5 \cdot 10^{-5}$ i $2 \cdot 10^{-4}$; zapis straty po każdej epoce | ~30 min |
| 2 | @phase-2:K26 = A, @phase-2:K28 = B, @phase-2:K30 = A | nowe dane z **Pythona**: zbiór do mapy (48 sekwencji Pythona + 16 tekstu C4), do naprawy (366 + 122, ~1 mln tokenów) i odłożony do oceny (16 + 16); mapa przesiewu na nowym zbiorze | ~21 min |
| 3 | @phase-2:K26, @phase-2:K30 | etap 4 dla warstwy 13: start według nowej mapy (75% Python) i według starej (75% tekst); naprawa na nowych danych; ocena KL osobno na odłożonym Pythonie i tekście + perpleksja WikiText-2 | ~20 min |
| 4 | @phase-2:K21 = C | to samo (tylko nowa mapa) dla warstw **2** (początek, najwrażliwsza wczesna), **26** (koniec, przedostatnia) i **14** (druga najmniej wrażliwa, też na kodzie) | ~35 min |

Zbiory do mapy, naprawy i oceny są **rozłączne**: każdy kawałek tekstu jest tylko w jednym z nich. Krok 2 (dane) już się zrobił na CPU.

### 2. Uproszczenia, żeby zmieścić się w ~2 h

- **Stopnie zmniejszenia:** w krokach 3–4 tylko 20% i 40%, bez 5% i 10%.
- **Trening:** w krokach 3–4 6 epok, z lepszym krokiem uczenia z kroku 1 (skrypt wybiera go sam według KL przy 40%). Pełne 16 epok sprawdza krok 1.
- **Średnia aktywacja** jako sposób startu jest pominięta; w etapie 4 była zawsze gorsza.
- **Testy programowania** (HumanEval, MBPP) czekają na Twoją zgodę na uruchamianie kodu napisanego przez model (@phase-2:K36).
- **Model do kodu** jako punkt odniesienia (@phase-2:K29 = B) też czeka, bo bez testów z @phase-2:K32 nie ma go jak porównać.

### 3. Co zmieniłem w kodzie

- `src/qwen_compression/data.py`: zbiory z wybranych języków, rozłączne podziały, równomierne przeplatanie (z testem);
- `scripts/phase2_code_sets.py` (dane), `scripts/phase2_code_map.py` (mapa 75% Python / 25% tekst);
- `scripts/phase2_stage4_one_layer.py`: zapis straty po epokach, start według starej mapy do porównania, ocena na odłożonym zbiorze osobno dla Pythona i tekstu.

Wyniki: `results/phase2/k23/` i `results/phase2/code/` (stan: `results/phase2/code/status.txt`).

*2026-10-30 11:11 — Claude Opus 5.5*

---
---
---
