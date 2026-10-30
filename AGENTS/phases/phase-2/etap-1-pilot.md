# Etap 1 — pilot: trzy warstwy policzone dokładnie

*2026-10-30 02:03 — Claude Opus 5.5*

**Status raportu:** do przeczytania

## Co masz zrobić

Przeczytaj, a potem odpowiedz na pytania **K16–K18** w `AGENTS/phases/phase-2/agents-issues-3.md`. Dotyczą tego raportu: dalsze pomiary tylko dla $\delta = \pm 1$, odstępstwo od nocnych reguł, liczba tokenów. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”. Uwagi i pytania do raportu możesz pisać w GUI pod tym raportem (Drzewo → Raporty albo „Co czeka na mnie” → Raporty do przeczytania i dyskusji); przyciskiem „🔒 Zakończ dyskusję” zamykasz raport.

---

## 1. Co policzono

Model Qwen3-0.6B-Base w **float32** (bez TF32). Warstwy 2, 13 i 25 (@phase-2:K12). Dla **każdego** z 3072 neuronów MLP w tych warstwach i każdego $\delta \in \{-1; -0{,}5; +0{,}5; +1\}$ zmieniamy aktywację neuronu na $(1+\delta)\,a$ i mierzymy:

$$
\mathrm{KL}_j(\delta) = \frac{1}{T}\sum_{t=1}^{T} \sum_{v} p_t(v)\,\log\frac{p_t(v)}{\tilde p_t(v)},
$$

czyli średnio na token: jak bardzo rozkład następnego tokenu $\tilde p$ po zaburzeniu neuronu $j$ różni się od oryginalnego $p$. $\delta = -1$ to wyłączenie neuronu, a $\delta = +1$ to podwojenie jego aktywacji.

| Krok | Tokeny | Czas |
|---|---|---|
| precyzja (bf16 vs float32, 64 neurony warstwy 13) | 2048 | 1 min |
| dokładnie: warstwa 2 / 13 / 25 | 4096 (1 sekwencja C4 + 1 sekwencja kodu) | 96 / 66 / 34 min |
| szum: 166 losowych neuronów na warstwę, **inne** 4096 tokenów | 4096 | 11 min |
| przesiew gradientem (Fisher), wszystkie 28 warstw | 4096 | **10 s** |

Kolejne warstwy liczą się szybciej, bo przebieg zaczyna się od zaburzonej warstwy, a nie od początku modelu.

## 2. Wyniki

### 2.1. Precyzja: bf16 odpada

| | bf16 | float32 |
|---|---|---|
| KL kontrolna („skala 1”, powinno być 0) | $1{,}3 \cdot 10^{-3}$ | $1{,}9 \cdot 10^{-9}$ |
| mediana KL wyłączenia neuronu | $1{,}3 \cdot 10^{-3}$ (sam szum) | $1{,}3 \cdot 10^{-5}$ |

W bf16 szum numeryczny jest 100× większy niż skutek wyłączenia typowego neuronu, więc pomiar mierzy szum. W float32 szum jest ~1000× mniejszy od najmniejszego zmierzonego skutku ($2{,}4 \cdot 10^{-6}$). Zgodnie z regułą z @T010 dalej liczymy w float32.

### 2.2. Skutek wyłączenia neuronu (δ = −1)

| Warstwa | mediana KL | 90. percentyl | maksimum | najważniejsze neurony |
|---|---|---|---|---|
| 2 | $1{,}4 \cdot 10^{-5}$ | $4{,}3 \cdot 10^{-5}$ | $9{,}2 \cdot 10^{-3}$ | #128, #55, #1489 (masywne, $\max \lvert a \rvert \approx 3000$) |
| 13 | $1{,}1 \cdot 10^{-5}$ | $3{,}3 \cdot 10^{-5}$ | $3{,}8 \cdot 10^{-4}$ | #37, #183, #65 (zwykłe, $\max \lvert a \rvert \approx 5$) |
| 25 | $1{,}1 \cdot 10^{-5}$ | $5{,}0 \cdot 10^{-5}$ | $1{,}8 \cdot 10^{-3}$ | #2953, #1638, #1499 ($\max \lvert a \rvert \approx 50$–$80$) |

![Rozkład KL](AGENTS/phases/phase-2/figures/etap1-rozklad-kl.png)

- Rozkład jest **wąski**: między 10. a 90. percentylem jest tylko 5× (warstwa 2), 6× (warstwa 13) i 19× (warstwa 25). Nie ma dużej grupy neuronów „za darmo” (KL ≈ 0). Najmniejszy skutek to ~$10^{-6}$, czyli ~10× mniej niż mediana.
- Odstają pojedyncze neurony, np. trzy masywne w warstwie 2 mają skutek ~700× większy niż mediana. W warstwie 13 najważniejsze neurony nie mają wcale dużych aktywacji.
- Zmiana straty (log-likelihood prawdziwego następnego tokenu) idzie w parze z KL: mediana ~$+10^{-5}$ nat na token. Dla części neuronów jest ujemna, czyli wyłączenie minimalnie **poprawia** przewidywanie na tym tekście (do $-7 \cdot 10^{-4}$).

### 2.3. Skutek rośnie jak $\delta^2$

| Warstwa | $\mathrm{KL}(-0{,}5)/\mathrm{KL}(-1)$ | $\mathrm{KL}(+1)/\mathrm{KL}(-1)$ | neurony z asymetrią > 50% |
|---|---|---|---|
| 2 | 0,250 | 0,99 | 63 |
| 13 | 0,250 | 1,00 | 6 |
| 25 | 0,250 | 1,00 | 74 |

(mediany po neuronach)

Słownie: osłabienie neuronu o połowę daje dokładnie ćwierć skutku wyłączenia, a podwojenie daje to samo co wyłączenie. Wynika to z rozwinięcia KL wokół $\delta = 0$:

$$
\mathrm{KL}_j(\delta) \approx \tfrac{1}{2}\,\delta^2\, F_j,
$$

gdzie $F_j$ (informacja Fishera neuronu $j$) to jedna liczba na neuron.

![Skutek rośnie jak delta do kwadratu](AGENTS/phases/phase-2/figures/etap1-delta-kwadrat.png)

Każdy punkt to jeden neuron. Lewy wykres: skutek osłabienia o połowę leży dokładnie na linii „¼ × wyłączenie”. Prawy wykres: skutek podwojenia leży wokół linii „tyle samo co wyłączenie”, ale z rozrzutem; punkty daleko od linii to neurony asymetryczne (więcej w etapie 3).

Wniosek praktyczny: **$\delta = \pm 0{,}5$ nie wnoszą nowej informacji**, a $\delta = +1$ wnosi tylko asymetrię, i to dla nielicznych neuronów (pytanie K16).

### 2.4. Przesiew gradientem a pomiar dokładny (te same tokeny)

$F_j$ można oszacować z gradientu jednym przebiegiem wstecz dla wszystkich neuronów naraz (wzór w `raport-1-opis-matematyczny.md`). Wynik dla 16 losowanych odpowiedzi na token:

![Przesiew vs dokładnie](AGENTS/phases/phase-2/figures/etap1-przesiew-vs-dokladnie.png)

| Warstwa | Spearman | wspólne „top 10%” | suma przesiew / suma dokładnie |
|---|---|---|---|
| 2 | 0,88 | 78% | 1,59 |
| 13 | 0,91 | 78% | 0,98 |
| 25 | 0,95 | 78% | 0,94 |

Przy 16 próbkach reguła z @T010 (≥ 0,9 i ≥ 80%) **nie jest spełniona**. Po zwiększeniu do 64 próbek (krok z etapu 2, te same tokeny): **0,96 / 0,98 / 0,98 i 84% / 87% / 87%**, więc reguła jest spełniona. Przy masywnych neuronach warstwy 2 przesiew przeszacowuje skutek 1,7–4× (punkty po prawej u góry), bo dla tak dużych efektów przybliżenie kwadratowe przestaje działać. Ranking jest jednak zachowany: to nadal najważniejsze neurony warstwy.

### 2.5. Najważniejszy wynik: 4096 tokenów to za mało

Ten sam pomiar dokładny na **innych** 4096 tokenach (166 losowych neuronów na warstwę):

| Warstwa | zgodność rankingów (Spearman) | mediana względnej różnicy KL |
|---|---|---|
| 2 | 0,51 | 31% |
| 13 | 0,52 | 36% |
| 25 | 0,51 | 61% |

![Dwa teksty a przesiew](AGENTS/phases/phase-2/figures/etap1-dwa-teksty.png)

Lewy wykres: ten sam pomiar dokładny na dwóch różnych tekstach. Gdyby ranking nie zależał od tekstu, punkty leżałyby na przekątnej; leżą w szerokiej chmurze. Prawy wykres dla porównania: przesiew i pomiar dokładny na **tym samym** tekście leżą prawie idealnie na przekątnej. Rozrzut bierze się więc z tekstu, a nie z metody.

Reguła wymagała ≥ 0,95. Ranking neuronów z 4096 tokenów **w połowie zależy od tego, jaki to był tekst**. Pomiar nie jest niedokładny numerycznie (float32). Skutek wyłączenia neuronu po prostu naprawdę zależy od tekstu, a neurony w środku rozkładu różnią się między sobą mniej, niż wynosi ta zmienność.

Do tego ranking z sekwencji C4 i ranking z sekwencji kodu (po 2048 tokenów) są praktycznie niezależne (Spearman 0,01 / 0,10 / −0,02). Etap 2 sprawdził to na większej próbie.

Porównanie z prostszą miarą: średnia wielkość aktywacji $\overline{|a_j|}$ ma z dokładną KL korelację rang 0,45 / 0,65 / 0,65. Jest skorelowana, ale wyraźnie słabiej niż przesiew.

## 3. Co z tego wynika dla etapu 2

1. Pomiar dokładny na 4096 tokenach daje ranking o wiarygodności ~0,5. „Wszystko dokładnie” (reguła awaryjna z @T010) kosztowałoby ~13–26 h i dałoby mapę o tej samej, słabej wiarygodności.
2. Przesiew jest ~1000× tańszy, więc można go policzyć na **32× więcej tokenów**. Zgodność z pomiarem dokładnym na tych samych tokenach wynosi 0,96–0,98, czyli przesiew jest dobrym zamiennikiem pomiaru dokładnego.
3. Dlatego etap 2 to: **przesiew na 131 tys. tokenów (64 sekwencje × 64 próbki) + pomiar dokładny 10% najważniejszych i 5% losowych w każdej warstwie** (tryb „screened” z @T010). Szczegóły i wyniki: `etap-2-mapa.md`.

## 4. Pliki

- wyniki: `results/phase2/stage1/` (`summary.json`, `exact-layer-XX.pt`, `noise.pt`, `fisher.pt`, `precision.pt`, `statistics.pt`, `log.jsonl`);
- kod: `scripts/phase2_stage1_pilot.py`, `scripts/phase2_stage1_analysis.py`, pakiet `src/qwen_compression/`.

*2026-10-30 02:03 — Claude Opus 5.5*
