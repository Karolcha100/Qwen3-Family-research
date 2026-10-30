# Etap 2 — mapa wrażliwości wszystkich 86 016 neuronów

*2026-10-30 02:05 — Claude Opus 5.5*

**Status raportu:** do przeczytania

## Co masz zrobić

Przeczytaj i odpowiedz na **K17** i **K18** w `AGENTS/phases/phase-pomysl/agents-issues-3.md` (czy akceptujesz mapę z przesiewu oraz co zrobić z tym, że tekst i kod mają różne ważne neurony). Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”. Uwagi i pytania do raportu możesz pisać w GUI pod tym raportem (Drzewo → Raporty albo „Co czeka na mnie” → Raporty do przeczytania i dyskusji); przyciskiem „🔒 Zakończ dyskusję” zamykasz raport.

---

## 1. Jak policzona

Dlaczego tak, a nie „wszystko dokładnie”: `etap-1-pilot.md`, rozdz. 2.5 i 3. W skrócie: 4096 tokenów daje ranking o wiarygodności ~0,5, a przesiew jest ~1000× tańszy, więc można go policzyć na dużo większej liczbie tokenów.

**Przesiew (Fisher)** dla każdego neuronu $j$ każdej warstwy:

$$
\widehat{\mathrm{KL}}_j(\delta = -1) = \frac{1}{2\,S\,T} \sum_{\text{sekwencje}} \sum_{s=1}^{S} \Bigg( \sum_{t} \frac{\partial \log p\big(y^{(s)}\big)}{\partial a_{j,t}}\; a_{j,t} \Bigg)^2 .
$$

Słownie:
1. dla każdej sekwencji losujemy z samego modelu $S$ alternatywnych ciągów następnych tokenów $y^{(s)}$;
2. liczymy, jak bardzo logarytm ich prawdopodobieństwa zmieniłby się po przeskalowaniu aktywacji $a_j$ neuronu $j$ (gradient razy aktywacja, zsumowane po pozycjach $t$);
3. średni kwadrat tej zmiany, podzielony przez $2T$, przybliża KL po wyłączeniu neuronu.

Jeden przebieg w przód i $S$ przebiegów wstecz daje wynik dla wszystkich 86 016 neuronów naraz.

| Ustawienie | Wartość |
|---|---|
| tokeny | 64 sekwencje × 2048 = **131 072** (48 sekwencji C4 + 16 kodu) |
| próbki $S$ | 64 na sekwencję |
| precyzja | float32, bez TF32 |
| czas | **21 min** |

Wynik zapisany per sekwencja (`results/phase2/stage2/fisher-per-sequence-64.pt`), dzięki czemu dało się sprawdzić powtarzalność. Mapa (średnia z 64 sekwencji): `results/phase2/stage2/fisher-map.pt`.

## 2. Czy przesiew zgadza się z pomiarem dokładnym

Na tych samych 4096 tokenach co pilot (3 warstwy, wszystkie neurony):

| Warstwa | Spearman | wspólne „top 10%” | suma przesiew / suma dokładnie |
|---|---|---|---|
| 2 | 0,96 | 84% | 1,44 |
| 13 | 0,98 | 87% | 1,00 |
| 25 | 0,98 | 87% | 0,96 |

Na **drugim** zbiorze 4096 tokenów (166 neuronów na warstwę): 0,94 / 0,98 / 0,96. Przesiew odtwarza więc pomiar dokładny prawie idealnie, gdy oba liczone są na tych samych tokenach. Wyjątek to kilka masywnych neuronów warstwy 2: ich skutek jest przeszacowany 1,7–4×, stąd suma 1,44.

## 3. Ile tokenów potrzeba do stabilnego rankingu

![Mapa przesiewu](AGENTS/phases/phase-pomysl/figures/etap2-mapa-przesiewu.png)

Lewy wykres: losujemy dwa rozłączne zbiory po $k$ sekwencji i porównujemy rankingi neuronów (średnia z 8 losowań). Krzyżyki to pomiar dokładny z pilota.

| Tokenów w każdym zbiorze | 2048 | 4096 | 8192 | 16 384 | 32 768 | 65 536 |
|---|---|---|---|---|---|---|
| zgodność (średnio po 28 warstwach) | 0,30 | 0,47 | 0,52 | 0,62 | 0,75 | 0,85 |

Dwie połówki pełnej mapy (po 65 536 tokenów) zgadzają się w 0,66–0,93, najlepiej w środkowych warstwach 12–20 (0,87–0,93), a najsłabiej w warstwach 2–3 i 24–25 (0,66–0,68). Z tego, jak zgodność rośnie z liczbą tokenów (wzór Spearmana–Browna $r_{2k} = \frac{2 r_k}{1 + r_k}$), cała mapa ze 131 tys. tokenów ma wiarygodność około **0,89** (średnio; od 0,80 w warstwach 2, 3 i 25 do 0,96 w warstwach 16–17).

**Co to znaczy w praktyce:** ranking „środka” rozkładu (neurony o zbliżonej ważności) nadal zależy od tekstu. Ranking skrajności (najważniejsze i najmniej ważne neurony) jest stabilny. Przy wycinaniu 5–40% neuronów decydują właśnie skrajności i okolice progu.

## 4. Tekst a kod: inne ważne neurony

| | warstwy 0–27 (zakres) |
|---|---|
| ranking z 48 sekwencji C4 vs ranking z 16 sekwencji kodu | od −0,15 do 0,23 |
| dwie porcje C4 po 16 sekwencji (ta sama wielkość co kod) | 0,74–0,94 |

![Tekst a kod](AGENTS/phases/phase-pomysl/figures/etap2-tekst-kod.png)

Dwie górne linie: rankingi z dwóch porcji tego samego rodzaju tekstu zgadzają się w 0,7–0,9 w każdej warstwie. Dolna linia: ranking z tekstu C4 i ranking z kodu zgadzają się prawie wcale (wokół zera).

Gdyby różnica wynikała tylko z szumu, tekst i kod zgadzałyby się mniej więcej tak jak dwie porcje tekstu. Zgadzają się jednak **prawie wcale**. Neurony ważne dla kodu to w dużej mierze inne neurony niż ważne dla tekstu. Mapa z mieszanki 75/25 jest kompromisem; pytanie **K18**.

## 5. Mapa: jak wrażliwe są warstwy

Prawy wykres: mediana, pasmo 10–90% i maksimum przewidywanej KL po wyłączeniu jednego neuronu.

| Warstwy | mediana KL | suma KL po neuronach | uwagi |
|---|---|---|---|
| 0–5 | $2{,}0$–$2{,}4 \cdot 10^{-5}$ | 0,08–0,15 | warstwa 2: maksimum $1{,}6 \cdot 10^{-2}$ (masywne neurony #55, #1489, #128) |
| 6–16 | $1{,}1$–$1{,}9 \cdot 10^{-5}$ | **0,045–0,08** | najmniej wrażliwe: 13 i 14 (suma 0,045) |
| 17–26 | $1{,}6$–$3{,}1 \cdot 10^{-5}$ | 0,07–0,21 | |
| 27 (ostatnia) | $3{,}6 \cdot 10^{-5}$ | **0,76** | maksimum $5{,}3 \cdot 10^{-2}$; tu jest 53 z 75 neuronów „krytycznych” |

„Suma KL po neuronach” nie jest skutkiem wycięcia całej warstwy (skutki nie dodają się), ale dobrze porównuje warstwy między sobą. Środek modelu jest najmniej wrażliwy na pojedyncze neurony, a ostatnia warstwa jest ~17× bardziej wrażliwa niż warstwa 13.

## 6. Pomiar dokładny 10% najważniejszych + 5% losowych (kontrola)

Liczy się po etapie 4 (kolejka GPU), ~2 h. Wynik dopiszę w tym miejscu jako nowy wpis.

## 7. Pliki

- `results/phase2/stage2/fisher-per-sequence-64.pt` (64 × 28 × 3072), `fisher-map.pt`, `fisher-summary.json`;
- kod: `scripts/phase2_stage2_fisher_map.py`, `scripts/phase2_stage2_fisher_analysis.py`, `scripts/phase2_stage2_full_map.py` (pomiar dokładny), `src/qwen_compression/importance.py`.

*2026-10-30 02:05 — Claude Opus 5.5*

---

## 8. Dopisek: pomiar dokładny 10% najważniejszych + 5% losowych (sekcja 6)

Policzony 02:29–04:30 (2 h) w float32 dla 25 warstw (bez 2, 13 i 25, które pilot policzył w całości). W każdej warstwie 307 neuronów najważniejszych według mapy i 153 losowe z reszty, $\delta = \pm 1$ (@K16), na tych samych 4096 tokenach co pilot.

**Przesiew (z tych samych 4096 tokenów, 64 próbki) vs pomiar dokładny:**

| | Spearman | średnio |
|---|---|---|
| wszystkie zmierzone neurony, 25 warstw | 0,96–0,99 | 0,978 |
| tylko 10% najważniejszych | 0,90–0,98 | 0,963 |
| tylko 5% losowych | 0,95–0,99 | 0,971 |

Mediana stosunku przesiew / dokładnie wynosi 0,95–1,01 w każdej warstwie. Pojedyncze neurony są przeszacowane do 2–5×; to te same, co w pilocie, czyli o bardzo dużym skutku, gdzie przybliżenie kwadratowe słabnie. **Przesiew jest wiarygodny w całym modelu, nie tylko w 3 warstwach pilota.**

![Przesiew a pomiar dokładny w 25 warstwach](AGENTS/phases/phase-pomysl/figures/etap2-przesiew-vs-dokladnie.png)

Lewy wykres: każdy punkt to jeden zmierzony neuron (pomarańczowe: 10% najważniejszych, niebieskie: 5% losowych); im bliżej przekątnej, tym lepiej przesiew przewiduje pomiar dokładny. Prawy wykres: zgodność rankingów osobno w każdej warstwie, od 0,96 do 0,99.

**Neurony krytyczne potwierdzone dokładnie.** Wyłączenie jednego neuronu ostatniej warstwy daje:

| Neuron | KL dokładnie | KL przesiew (te same tokeny) |
|---|---|---|
| 27 / #39 | 0,043 | 0,040 |
| 27 / #386 | 0,034 | 0,033 |
| 27 / #222 | 0,032 | 0,043 |
| 27 / #81 | 0,028 | 0,034 |
| 27 / #0 | 0,026 | 0,021 |
| 27 / #191 | 0,016 | 0,017 |

To ~2000× więcej niż mediana ($1{,}8 \cdot 10^{-5}$). Dla porównania: wycięcie 40% neuronów warstwy 13 z douczeniem dało KL 0,006 (`etap-4-jedna-warstwa.md`).

Wyniki: `results/phase2/stage2/layer-XX.pt` (neurony, KL i zmiana straty dla $\delta = \pm 1$, osobno dla 2 sekwencji).

*2026-10-30 04:30 — Claude Opus 5.5*
