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

## Co masz zrobić

Nic; to wynik pierwszego kroku (@phase-2:K23). Reszta się liczy.

### Dłuższy trening warstwy 13: daje mało

![Długi trening](AGENTS/phases/phase-2/figures/k23-dlugi-trening-13.png)

Wykres: błąd zmniejszonej warstwy za następną warstwą (na odłożonych danych walidacyjnych) w kolejnych epokach; 100% = start z najmniejszych kwadratów.

Co widać:
- **krok uczenia $5 \cdot 10^{-5}$** (pomarańczowa linia): błąd spada gładko, po 16 epokach o ~15% (20%: 85,8%, 40%: 84,5% startu), ale od 8. epoki już tylko o ~1 punkt;
- **krok $2 \cdot 10^{-4}$** (niebieska linia): za duży, błąd skacze; przy 20% prawie nie spada.

| Zmniejszenie | Trening | KL do oryginału | Perpleksja WikiText-2 |
|---|---|---|---|
| 20% | 4 epoki (noc) | 0,00216 | 12,679 |
| 20% | 16 epok, $5 \cdot 10^{-5}$ | **0,00204** (−5,5%) | 12,680 |
| 20% | 16 epok, $2 \cdot 10^{-4}$ | 0,00218 | 12,686 |
| 40% | 4 epoki (noc) | 0,00574 | 12,725 |
| 40% | 16 epok, $5 \cdot 10^{-5}$ | **0,00543** (−5,4%) | 12,721 |
| 40% | 16 epok, $2 \cdot 10^{-4}$ | 0,00553 | 12,721 |

(oryginał: perpleksja 12,660)

**Wniosek:** 4× dłuższy trening tej samej warstwy daje tylko ~5% mniejszą KL. Granicą nie jest więc długość treningu, tylko to, co zmniejszona warstwa potrafi odtworzyć sama, przy celu „zgodność za następną warstwą”. Dotyczy to Twojej uwagi z @T011. Jeśli trening ma odrobić więcej, prawdopodobnie trzeba zmienić to, **co** trenujemy (np. kilka warstw razem albo cel liczony na wyjściu modelu), a nie **jak długo**. To zapiszę jako pytanie, gdy skończą się obliczenia.

Dalsze kroki (Python) liczą się z krokiem $5 \cdot 10^{-5}$ i 6 epokami (od 8. epoki zysk jest już mały).

Wyniki: `results/phase2/k23/summary.json`, kod: `scripts/phase2_k23_analysis.py`.

*2026-10-30 11:30 — Claude Opus 5.5*

---
---
---

## Co masz zrobić

Przeczytaj raport `AGENTS/phases/phase-2/etap-4b-kod.md` (zakładka Raporty) i odpowiedz na **K37** i **K38** w `AGENTS/phases/phase-2/agents-issues-6.md`. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”.

### Wszystkie obliczenia skończone (11:30–12:59)

Najważniejsze wyniki (szczegóły, wykresy i tabele są w raporcie):

| | wynik |
|---|---|
| mapa kodu | powtarzalna (wiarygodność ok. 0,9); dla kodu ważne są inne neurony niż dla tekstu (korelacja ok. 0) |
| warstwa 13, start z mapy kodu vs ze starej mapy | KL na Pythonie **o 36–38% mniejsza**, na tekście C4 o 26–33% większa |
| warstwy 2, 13, 14, 26 przy 40% | KL na Pythonie: 0,0107 / **0,0032** / **0,0030** / 0,0113 |
| zysk z treningu po najmniejszych kwadratach | 18–20% (13, 14), 8–11% (2), 1% (26) |

Wnioski:
- start z mapy kodu ma znaczenie także po treningu, więc mapa jest potrzebna;
- trening z obecnym celem („zgodność za następną warstwą”) odrabia mało, a w warstwie 26 prawie nic. Stąd pytanie **K37**: czy trenować z celem na wyjściu modelu;
- **K38**: czy sprawdzić mapę 100% kod (o której pisałeś w @phase-2:K18).

**Błąd i poprawka:** w pierwszym przebiegu warstwa 26 po treningu psuła model (KL ~1,1). Skrypt brał cel treningu z elementu `hidden_states`, który dla ostatniej warstwy ma już nałożoną końcową normalizację. Poprawiłem to i policzyłem warstwę 26 ponownie (12:47–12:59). Wcześniejsze wyniki (warstwa 13: etap 4 i @phase-2:K23) nie były dotknięte; sprawdziłem, że dla warstwy 13 cel jest identyczny.

GPU jest wolne. Nic więcej nie uruchamiam, dopóki nie zdecydujesz.

*2026-10-30 13:00 — Claude Opus 5.5*

---
---
---
