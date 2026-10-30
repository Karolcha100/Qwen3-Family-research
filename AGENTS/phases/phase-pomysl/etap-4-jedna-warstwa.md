# Etap 4 — zmniejszanie jednej warstwy (warstwa 13)

*2026-10-30 02:29 — Claude Opus 5.5*

**Status raportu:** do przeczytania

## Co masz zrobić

Przeczytaj i odpowiedz na **K21** (czy warstwa 13 jest w porządku i czy powtórzyć dla innej) oraz **K23** (dłuższy trening) w `AGENTS/phases/phase-pomysl/agents-issues-3.md`. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”. Uwagi i pytania do raportu możesz pisać w GUI pod tym raportem (Drzewo → Raporty albo „Co czeka na mnie” → Raporty do przeczytania i dyskusji); przyciskiem „🔒 Zakończ dyskusję” zamykasz raport.

---

## 1. Co zrobiono

**Warstwa 13** (wybór tymczasowy, @T010 punkt 4). Ma najmniejszą sumaryczną wrażliwość w mapie etapu 2 (suma przewidywanej KL 0,045, prawie remis z warstwą 14) i pełny pomiar dokładny z pilota.

Z MLP tej warstwy wycinamy 5%, 10%, 20% i 40% neuronów (@phase-pomysl:K14) z 3072, w kolejności od najmniej ważnych. Ważność liczymy na dwa sposoby:
- **przesiew KL:** mapa z etapu 2 (przewidywana KL po wyłączeniu neuronu, 131 tys. tokenów);
- **średnia $\lvert a \rvert$:** średnia wielkość aktywacji neuronu (prosta miara porównawcza z planu).

Dla każdego wyboru trzy warianty:

1. **tylko wycięcie:** usuwamy kolumny $W_{down}$ i wiersze $W_{gate}$, $W_{up}$ wyciętych neuronów, nic więcej;
2. **+ najmniejsze kwadraty** (@phase-pomysl:K7): nowa macierz $W_{down}$ dla pozostałych $k$ neuronów, tak żeby wyjście MLP jak najlepiej odtwarzało oryginał:

$$
\widehat W_{down} = \arg\min_{W \in \mathbb{R}^{1024 \times k}} \sum_{t} \big\| W\, a_{K,t} - y_t \big\|^2 + \lambda \|W\|^2 ,
$$

   gdzie $a_{K,t}$ to aktywacje zachowanych neuronów dla tokenu $t$, a $y_t$ to oryginalne wyjście MLP. Słownie: pozostałe neurony przejmują pracę wyciętych tak dobrze, jak to możliwe liniowo. Liczone na 1 mln tokenów (488 sekwencji × 2048, mieszanka 75/25 jak w @phase-pomysl:K11), $\lambda$ = $10^{-6}$ × średnia przekątnej;
3. **+ trening przez następną warstwę** (@phase-pomysl:K5 = B, K8): start z wariantu 2, trenujemy wszystkie wagi zmniejszonego MLP. Wejście to stan przed warstwą 13, cel to oryginalny stan po warstwie 14 (warstwa 14 zamrożona):

$$
\mathcal{L} = \frac{\big\| f_{14}\big(f_{13}^{\text{mniejsza}}(h^{(12)})\big) - h^{(14)} \big\|^2}{\operatorname{Var}\big(h^{(14)}\big)} .
$$

   Słownie: błąd względem oryginału liczymy dopiero za następną warstwą, bo ona może część błędu „wybaczyć”. Adam, lr $5 \cdot 10^{-5}$, 4 epoki po 1 mln tokenów, wybór najlepszej epoki na walidacji.

**Ocena:** KL do oryginalnego modelu na 8 sekwencjach (16 384 tokenów, w tym 2 kodu) oraz perpleksja WikiText-2 (okna 2048).

**Czas:** zebranie par na dysk 2,5 min (4 GB), każdy wariant ~40 s, trening ~95 s. Całość 26 min.

## 2. Wyniki

![Krzywe etapu 4](AGENTS/phases/phase-pomysl/figures/etap4-warstwa-13.png)

Oryginał: perpleksja WikiText-2 **12,660**.

| Wycięte | Wybór | tylko wycięcie: KL / PPL | + najmn. kwadraty: KL / PPL | + trening: KL / PPL |
|---|---|---|---|---|
| 5% | przesiew | 0,00068 / 12,669 | 0,00045 / 12,665 | **0,00039 / 12,664** |
| 5% | średnia akt. | 0,00100 / 12,673 | 0,00075 / 12,667 | 0,00062 / 12,666 |
| 10% | przesiew | 0,00166 / 12,677 | 0,00110 / 12,670 | **0,00094 / 12,668** |
| 10% | średnia akt. | 0,00208 / 12,684 | 0,00152 / 12,676 | 0,00124 / 12,673 |
| 20% | przesiew | 0,00405 / 12,712 | 0,00266 / 12,687 | **0,00216 / 12,679** |
| 20% | średnia akt. | 0,00479 / 12,731 | 0,00334 / 12,709 | 0,00273 / 12,697 |
| 40% | przesiew | 0,0106 / 12,805 | 0,0070 / 12,744 | **0,0057 / 12,725** |
| 40% | średnia akt. | 0,0123 / 12,817 | 0,0085 / 12,762 | 0,0069 / 12,742 |

(KL w nat na token; „średnia akt.” = wybór po średniej $\lvert a \rvert$)

### Wnioski

1. **Warstwa 13 bardzo dobrze znosi zmniejszanie.** Po wycięciu 40% neuronów MLP i douczeniu perpleksja rośnie z 12,660 do 12,725 (+0,5%). Przy 20% wzrost to +0,15%. To jednak jedna warstwa, i to najmniej wrażliwa: 40% jej MLP to 3,8 mln parametrów, czyli 0,6% modelu.
2. **Wybór przesiewem jest lepszy niż wybór po średniej aktywacji** na każdym stopniu i w każdym wariancie. KL jest o 14–37% mniejsza (po treningu: 37% przy 5%, 24% przy 10%, 21% przy 20%, 17% przy 40%). Mapa z etapu 2 ma więc praktyczną wartość.
3. **Najmniejsze kwadraty to duży i darmowy zysk:** KL spada o ~1/3 względem samego wycięcia (40 s obliczeń).
4. **Trening dokłada mniej, 10–20%,** a w 6 z 8 przebiegów najlepsza była ostatnia, 4. epoka. Trening był więc za krótki albo z za małym krokiem, i tu jest zapas (pytanie **K23**).
5. Krzywa jest **gładka, bez „pęknięcia”** do 40%. Skutek rośnie nieco szybciej niż liniowo (KL przy 40% to ~2,6× KL przy 20%).

![Wybór neuronów i naprawa](AGENTS/phases/phase-pomysl/figures/etap4-wybor-i-naprawa-13.png)

Lewy wykres: każdy punkt to neuron warstwy 13 (oś pozioma: średnia aktywacja, pionowa: przewidywana KL po wyłączeniu). Przy wycinaniu 20% oba sposoby wybierają wspólnie 337 neuronów (zielone). Różnią się 277 neuronami: przesiew wycina neurony o średniej aktywacji, ale małym skutku (niebieskie), a „średnia $\lvert a \rvert$” wycina neurony słabe, ale ważne (pomarańczowe). Stąd przewaga przesiewu.

Prawy wykres: ile KL zostaje po naprawie, w procentach KL samego wycięcia. Najmniejsze kwadraty zostawiają ~65%, trening ~55%, prawie niezależnie od tego, ile wycięto.

## 3. Ograniczenia

- Jedna warstwa, najmniej wrażliwa. Dla wrażliwych warstw (2, 26–27) krzywa będzie zapewne dużo stromsza; o tym jest **K21**.
- Mapa ważności i dane treningowe pochodzą z tej samej mieszanki C4 + kod. WikiText-2 jest od nich niezależny, a KL liczona jest na sekwencjach, które weszły też do mapy (0–7 z 64).
- Nie mierzyłem osobno tekstu i kodu (@K18). Wymaga to tylko ponownej oceny, bez treningu.

## 4. Pliki

- wyniki: `results/phase2/stage4/layer-13/results.jsonl`, `log.jsonl`; pary i statystyki: `~/qwen3-checkpoints/phase2/layer-13-pairs/` (poza repozytorium);
- kod: `scripts/phase2_stage4_one_layer.py`, `scripts/phase2_stage4_analysis.py`, `src/qwen_compression/reconstruction.py`.

*2026-10-30 02:29 — Claude Opus 5.5*
