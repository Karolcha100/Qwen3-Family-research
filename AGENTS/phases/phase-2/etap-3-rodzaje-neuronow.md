# Etap 3 — rodzaje neuronów w 28 warstwach

*2026-10-30 02:31 — Claude Opus 5.5*

**Status raportu:** do przeczytania

## Co masz zrobić

Przeczytaj. Decyzje dotyczące tego etapu: **K20** (klasyfikator, czyli odłożona część etapu) i **K24** (czy progi rodzajów są sensowne) w `AGENTS/phases/phase-2/agents-issues-3.md`. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”. Uwagi i pytania do raportu możesz pisać w GUI pod tym raportem (Drzewo → Raporty albo „Co czeka na mnie” → Raporty do przeczytania i dyskusji); przyciskiem „🔒 Zakończ dyskusję” zamykasz raport.

---

## 1. Na czym oparte

- **Skutek wyłączenia** $\mathrm{KL}_j$: mapa przesiewu z etapu 2 (131 tys. tokenów), dla każdego z 86 016 neuronów.
- **Aktywacje:** średnia $\overline{|a_j|}$ i maksimum $\max |a_j|$ z 8 sekwencji (16 tys. tokenów); osobno średnia $\overline{|a_j|}$ na 12 sekwencjach C4 i 4 sekwencjach kodu.
- **Asymetria** ($\delta = +1$ vs $\delta = -1$): tylko neurony zmierzone dokładnie (pilot: wszystkie neurony warstw 2, 13, 25; etap 2: 15% neuronów pozostałych warstw).
- **Bez klasyfikatora:** ocena generacji dla ~250 najważniejszych neuronów odłożona (@T010 punkt 3, pytanie **K20**).

## 2. Rodzaje (progi ustalone przed obliczeniem)

| Rodzaj | Warunek | Słownie |
|---|---|---|
| martwy | $\overline{\lvert a_j \rvert} < 0{,}05 \cdot$ mediana warstwy | prawie się nie aktywuje |
| zbędny | $\mathrm{KL}_j < 0{,}1 \cdot$ mediana globalna | wyłączenie prawie nic nie zmienia |
| krytyczny | $\mathrm{KL}_j > 100 \cdot$ mediana globalna | wyłączenie zmienia bardzo dużo |
| masywny | $\max \lvert a_j \rvert \,/\, \overline{\lvert a_j \rvert} > 300$ | zwykle cichy, rzadko ogromny |
| asymetryczny | $\frac{\lvert \mathrm{KL}_j(+1) - \mathrm{KL}_j(-1) \rvert}{\max} > 0{,}5$ | podwojenie działa inaczej niż wyłączenie |
| kodowy / tekstowy | $\overline{\lvert a_j \rvert}_{\text{kod}} / \overline{\lvert a_j \rvert}_{\text{C4}} > 2$ (lub $< 0{,}5$) | dużo silniej aktywny na kodzie (tekście) |

Mediana globalna $\mathrm{KL}_j$ = $1{,}8 \cdot 10^{-5}$ nat na token.

## 3. Wyniki

![Rodzaje neuronów](AGENTS/phases/phase-2/figures/etap3-rodzaje-neuronow.png)

| Rodzaj | Razem | Gdzie |
|---|---|---|
| martwy | **5** | warstwy 19, 21, 26, 27 (2) |
| zbędny | **422** (0,5%) | prawie tylko warstwy 15–27, najwięcej w 20 (74) |
| krytyczny | **75** | **53 w ostatniej warstwie 27**, 6 w warstwie 2, 5 w warstwie 26, 4 w warstwie 0 |
| masywny | 883 | warstwy 1–2 (29), 6 (1) i 17–27 (853, z tego 414 w warstwie 27) |
| asymetryczny | 143 | (tylko zmierzone dokładnie; uzupełnię po pomiarze etapu 2) |
| kodowy | 6446 (7,5%) | rośnie z głębokością: 28 w warstwie 0 → 599 w warstwie 27 |
| tekstowy | 5818 (6,8%) | podobnie: 12 → 707 w warstwie 26 |

![KL w warstwach](AGENTS/phases/phase-2/figures/etap3-kl-w-warstwach.png)

### Co z tego wynika

1. **Neuronów martwych prawie nie ma** (5 z 86 016), a 92% neuronów jest aktywnych ($|a| > 0{,}01$) na typowym tokenie. Proste „wycinanie nieużywanych” nic tu nie da.
2. **Zbędnych też jest mało** (0,5%). Rozkład ważności jest wąski: większość neuronów ma skutek w przedziale ~$5 \cdot 10^{-6}$–$10^{-4}$. Zmniejszanie warstw będzie więc zawsze wymieniać „trochę jakości” na „trochę parametrów”, bez dużej darmowej puli. Etap 4 pokazuje jednak, że ta wymiana jest łagodna (warstwa 13: −40% neuronów → perpleksja +0,5%).
3. **Ważność jest skupiona w kilku miejscach:**
   - ostatnia warstwa 27: 53 neurony krytyczne, a 1% najważniejszych neuronów odpowiada za **46%** sumy KL warstwy (w typowej warstwie 6–16%);
   - warstwa 2: 6 krytycznych (#46, #55, #128, #321, #646, #1489), w tym masywne o aktywacjach do ~3700; 1% neuronów = **47%** sumy KL;
   - warstwy 0 i 26: po kilka krytycznych.
   Te neurony trzeba bezwzględnie chronić przy zmniejszaniu.
4. **Neurony masywne to nie to samo co krytyczne.** Tylko 14 z 883 masywnych jest krytycznych. W późnych warstwach masywne są często „kodowe” (296 z 883): rzadko, ale bardzo mocno włączają się na kodzie.
5. **Specjalizacja tekst/kod rośnie z głębokością.** We wczesnych warstwach neurony działają podobnie na obu rodzajach tekstu, a w warstwach 17–27 od ~1/5 do ~1/3 neuronów jest wyraźnie „kodowych” albo „tekstowych”. Pasuje to do wyniku z etapu 2 (ranking ważności z tekstu i z kodu jest prawie niezależny; @K18).
6. Ciekawostka: w warstwie 27 krytyczne neurony mają głównie małe numery (42 z 53 ma numer < 700). Nie badałem, z czego to wynika.

## 4. Pliki

- `results/phase2/stage3/summary.json` (liczby, progi, 25 najważniejszych neuronów), `labels.pt` (maski rodzajów), `source-statistics.pt`;
- kod: `scripts/phase2_stage3_neuron_kinds.py` (progi jako argumenty).

*2026-10-30 02:31 — Claude Opus 5.5*

---

## 5. Dopisek: asymetria po pomiarze dokładnym etapu 2

Etap 3 przeliczony 04:30 z pomiarem dokładnym etapu 2. Zmienia się tylko liczba **asymetrycznych**: 571 (zamiast 143), z 20 716 zmierzonych dokładnie (24% wszystkich neuronów). Pozostałe rodzaje bez zmian.

| Warstwy | asymetryczne |
|---|---|
| 0–6 | 18–63 na warstwę (najwięcej warstwa 2: 63) |
| 7–16 | 1–12 na warstwę |
| 17–27 | 14–74 na warstwę (najwięcej warstwa 25: 74, warstwa 27: 54) |

Asymetria dotyczy głównie **ważnych** neuronów: ma ją 5,1% neuronów z „top 10%” i tylko 0,9% losowych. Zwykle wyłączenie szkodzi bardziej niż podwojenie: tak jest u 452 z 571 asymetrycznych (w warstwie 27 u 39 z 54). Liczby na warstwach 2, 13 i 25 obejmują wszystkie neurony, a na pozostałych tylko zmierzone 15%, więc nie są wprost porównywalne.

![Asymetria](AGENTS/phases/phase-2/figures/etap3-asymetria.png)

Lewy wykres: każdy zmierzony dokładnie neuron; na przekątnej podwojenie szkodzi tyle samo co wyłączenie. Pomarańczowe punkty to asymetryczne, głównie **pod** przekątną (wyłączenie szkodzi bardziej). Prawy wykres: liczba asymetrycznych w warstwach z podziałem na kierunek; najwięcej we wczesnych (0–6) i późnych (17–27) warstwach, prawie wcale w środku.

*2026-10-30 04:30 — Claude Opus 5.5*
