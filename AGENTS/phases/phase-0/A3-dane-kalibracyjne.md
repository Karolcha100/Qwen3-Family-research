# A3 — dane kalibracyjne (raport do @phase-0:K8)

*2026-10-29 15:01 — Claude Opus 5.5*

## Co masz zrobić

Przeczytaj raport i wybierz dane kalibracyjne z @phase-0:K8. Wystarczy napisać w raporcie pod @A3 np. „A” (albo zadać pytanie):

- **A** — C4: 128 kawałków po 2048 tokenów, stałe ziarno. Standard z artykułów o GPTQ i Wanda. **Rekomendacja** jako ustawienie domyślne.
- **B** — WikiText-2 (ryzyko zawyżonych wyników, opis w punkcie 3).
- **C** — mieszanka C4 i kodu (lepiej chroni programowanie, trudniej porównać z literaturą). Dobra jako osobny eksperyment później.

W skrócie: większość metod kompresji **nie patrzy tylko na wagi, ale też na to, jakie dane przez nie przepływają**. Dane kalibracyjne to próbka „typowego tekstu”, na której metoda sprawdza, które wagi są ważne. Metoda chroni to, co widzi w tej próbce, więc wybór próbki zmienia wynik.

---

## 1. Po co metodom dane

Warstwa liniowa modelu mnoży wejście $X$ przez macierz wag $W$ i daje wyjście $WX$. Kompresja zamienia $W$ na przybliżenie $\widehat{W}$ (mniej bitów, zera, niski rząd).

**Bez danych** (RTN, HQQ) minimalizujemy błąd samych wag:

$$\min_{\widehat{W}} \; \|W - \widehat{W}\|_F^2$$

Słownie: chcemy, żeby skompresowane wagi były jak najbliżej oryginalnych, każda tak samo ważna.

**Z danymi** (GPTQ, AWQ, Wanda, SparseGPT, ASVD) minimalizujemy błąd **wyjścia** warstwy na prawdziwych wejściach:

$$\min_{\widehat{W}} \; \|WX - \widehat{W}X\|_F^2$$

Słownie: nie przejmujemy się błędem wagi, jeśli wejście, które ją mnoży, jest prawie zawsze bliskie zera. Bardzo dbamy za to o wagi mnożone przez duże, częste wartości. **$X$ bierze się właśnie z danych kalibracyjnych:** przepuszczamy przez model próbkę tekstu i zapisujemy, co wchodzi do każdej warstwy.

Jak to wykorzystują konkretne metody:
- **GPTQ / SparseGPT** budują macierz $H = 2XX^\top$ (tzw. Hesjan). Mówi ona, które kierunki w danych wejściowych są ważne, i według niej kompensują błąd w pozostałych wagach;
- **Wanda** ocenia ważność wagi jako $S_{ij} = |W_{ij}| \cdot \|X_j\|_2$, czyli wielkość wagi razy typowa wielkość wejścia, które ją mnoży. Najmniej ważne wagi zeruje;
- **AWQ** mierzy średnią wielkość aktywacji w każdym kanale i skaluje kanały z dużymi aktywacjami tak, żeby kwantyzacja mniej je psuła.

## 2. Czym są C4 i WikiText-2

- **C4** (*Colossal Clean Crawled Corpus*): oczyszczony tekst z internetu (Common Crawl): strony, blogi, artykuły. Różnorodny, „przeciętny” tekst.
- **WikiText-2:** artykuły z Wikipedii. Jednolity, encyklopedyczny styl.

## 3. Jak wybór wpływa na wyniki

**a) Domena.** Metoda chroni kierunki ważne w próbce. Kalibracja na Wikipedii lepiej chroni encyklopedyczny angielski, a **gorzej to, czego w próbce nie ma**: kod, matematykę, polski, format czatu. Ten efekt jest zwykle słaby przy 4–8 bitach, ale wyraźnieje przy 2–3 bitach i przy mocnym pruningu.

**b) Zawyżenie wyniku.** Kalibracja na WikiText-2 i pomiar perplexity na WikiText-2 (inny wycinek, ale ten sam styl) daje wynik zbyt optymistyczny: model jest „dostrojony” do testu. Dlatego standard to **kalibracja na C4, a pomiar na WikiText-2 i C4**.

**c) Ilość.** 128 × 2048 = 262 144 tokenów. Macierz $H$ ma rozmiar $d \times d$, gdzie $d$ to szerokość wejścia warstwy (w Qwen3-0.6B: 1024, a w MLP do 3072). Żeby $H$ była wiarygodna, potrzeba dużo więcej tokenów niż $d$; 262 tys. ≫ 3072, więc z zapasem. Więcej danych daje coraz mniejszy zysk, a liczenie trwa dłużej.

**d) Losowość.** Inne losowe 128 kawałków daje nieco inny wynik. Gdy dwie metody różnią się o ułamek punktu perplexity, nie wiadomo, czy to różnica metod, czy losowania. Pomaga powtórzenie z 2–3 ziarnami; pytanie o to: @phase-0:K31.

**e) Format przy modelu instrukcyjnym.** Model po post-treningu (@A2) zwykle widzi tekst w formacie czatu. Kalibracja na zwykłym tekście z internetu może słabiej chronić zachowania czatowe (wykonywanie poleceń, tryb myślenia) niż kalibracja na dialogach. Pytanie o to: @phase-0:K32.

## 4. Podsumowanie opcji

| | A — C4 (rek.) | B — WikiText-2 | C — C4 + kod |
|---|---|---|---|
| porównywalność z literaturą | tak | częściowo | słaba |
| ryzyko zawyżenia PPL na WikiText-2 | nie | **tak** | nie |
| ochrona kodu (evalplus) | przeciętna | słaba | lepsza |
| zastosowanie | domyślne | — | osobny eksperyment |
