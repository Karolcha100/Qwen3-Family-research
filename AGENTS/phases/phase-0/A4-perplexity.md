# A4 — perplexity i protokół pomiaru (raport do @phase-0:K9)

*2026-10-29 15:01 — Claude Opus 5.5*

## Co masz zrobić

Przeczytaj raport i wybierz protokół z @phase-0:K9. Wystarczy napisać w raporcie pod @A4 np. „A” (albo zadać pytanie):

- **A** — kontekst 2048 tokenów, okna bez nakładania; WikiText-2 cały zbiór testowy, C4 256 okien z walidacji. Tak liczą artykuły o GPTQ i Wanda. **Rekomendacja.**
- **B** — kontekst 4096 (bliżej realnego użycia, ale liczby nieporównywalne z literaturą i dłuższe liczenie).
- **C** — A jako standard + dodatkowy pomiar 4096 dla najlepszych wariantów.

W skrócie: perplexity mówi, **jak bardzo model jest „zaskoczony” prawdziwym tekstem**. Im niżej, tym lepiej. Protokół (długość okna, sposób cięcia tekstu, zbiór) zmienia same liczby, więc musi być stały, żeby warianty dało się porównywać.

---

## 1. Czym jest perplexity

Model językowy czyta tekst token po tokenie (token to kawałek słowa; Qwen3 ma słownik ~152 tys. tokenów). Na każdej pozycji $i$ podaje rozkład prawdopodobieństwa następnego tokenu, znając wszystkie poprzednie: $p_\theta(x_i \mid x_{<i})$. Tutaj $\theta$ to wagi modelu, a $x_{<i}$ to tokeny przed pozycją $i$.

Bierzemy prawdziwy tekst i patrzymy, **jakie prawdopodobieństwo model dał tokenowi, który naprawdę wystąpił**. Średni ujemny logarytm tych prawdopodobieństw to *entropia krzyżowa* (ta sama wielkość, którą model minimalizuje podczas treningu):

$$\mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N} \log p_\theta(x_i \mid x_{<i})$$

**Perplexity** to jej wykładnik:

$$\mathrm{PPL} = e^{\mathcal{L}} = \left(\prod_{i=1}^{N} \frac{1}{p_\theta(x_i \mid x_{<i})}\right)^{1/N}$$

Słownie: perplexity to **średnia geometryczna z „1 / prawdopodobieństwo prawidłowego tokenu”**.

**Intuicja:** PPL = 10 znaczy, że model jest średnio tak niepewny, jakby wybierał losowo spośród 10 równie prawdopodobnych tokenów. PPL = 1 to model idealny (zawsze daje 100% prawidłowemu tokenowi). Model zgadujący losowo ze słownika ma PPL ≈ 152 000.

**Mini-przykład:** tekst ma 3 tokeny, a model dał prawidłowym tokenom prawdopodobieństwa $0{,}5$, $0{,}25$ i $0{,}125$. Odwrotności to 2, 4 i 8, a ich średnia geometryczna to $\sqrt[3]{2 \cdot 4 \cdot 8} = \sqrt[3]{64} = 4$. Zatem PPL = 4.

## 2. Po co nam to przy kompresji

- **Tanie:** jeden przebieg modelu po tekście, bez generowania. Dla 0.6B to sekundy–minuty.
- **Czułe na zepsucie:** kompresja zmienia wagi, model gorzej przewiduje tekst i PPL rośnie. Typowy obraz: przy 8 bitach PPL prawie się nie zmienia, przy 4 bitach rośnie trochę, przy 2–3 bitach wyraźnie. Kiedy model się „rozsypuje”, PPL rośnie do setek albo tysięcy.
- **Standard w literaturze:** każdy artykuł o GPTQ, AWQ, Wanda, SparseGPT podaje PPL na WikiText-2 (często też C4). Możemy więc sprawdzić, czy nasze wyniki wyglądają rozsądnie.

W praktyce raportujemy **zmianę względem modelu BF16** (tego samego, nieskompresowanego): $\Delta\mathrm{PPL} = \mathrm{PPL}_{\text{po kompresji}} - \mathrm{PPL}_{\text{BF16}}$.

## 3. Ograniczenia (dlatego są też inne metryki)

- **Zależy od tokenizera:** PPL Qwen3 i Llamy są nieporównywalne, bo modele tną tekst inaczej. Porównujemy tylko warianty tego samego modelu.
- **Mierzy przewidywanie tekstu, nie umiejętności.** Model może mieć prawie tę samą PPL, a gorzej rozumować albo pisać kod. Stąd lm-eval, evalplus i sędzia (@T002).
- **Patrzy tylko na prawidłowy token.** Czulsza jest **dywergencja KL**: porównuje *cały* rozkład modelu skompresowanego z rozkładem BF16 na każdej pozycji, czyli wszystkie ~152 tys. tokenów, a nie tylko ten prawidłowy:

$$D_{\mathrm{KL}}(P \,\|\, Q) = \sum_{v} P(v)\,\log\frac{P(v)}{Q(v)}$$

Słownie: $P$ to rozkład modelu BF16, $Q$ to rozkład modelu po kompresji. KL mierzy, ile „informacji tracimy”, używając $Q$ zamiast $P$. Wynosi 0 tylko wtedy, gdy rozkłady są identyczne. Uśredniamy ją po wszystkich pozycjach tekstu.

## 4. Co zmienia protokół (o to jest pytanie K9)

Tekstu testowego nie da się wrzucić do modelu w całości, więc tniemy go na **okna** po $L$ tokenów.

**a) Długość okna $L$.** Tokeny na początku okna mają mało kontekstu, więc model gorzej je przewiduje. Im dłuższe okno, tym więcej tokenów z bogatym kontekstem i **niższa PPL**. PPL przy 2048 i przy 4096 to dwie różne liczby: obie są „prawdziwe”, ale nieporównywalne ze sobą.

**b) Okna bez nakładania vs przesuwane.** Bez nakładania: tekst dzielimy na kolejne kawałki $[1..L], [L{+}1..2L], \dots$, co jest szybkie, ale część tokenów ma mało kontekstu. Przesuwane (krok $s < L$): okno przesuwa się o $s$, a liczymy tylko ostatnie $s$ tokenów, więc każdy ma prawie pełny kontekst. PPL wychodzi niższa, ale liczenie trwa ~$L/s$ razy dłużej. Artykuły o GPTQ i Wanda używają okien bez nakładania.

**c) Zbiór i jego wycinek.**
- **WikiText-2:** artykuły z Wikipedii (wybrane jako „dobre” i „medalowe”). Zbiór testowy jest mały (rzędu 0,3 mln tokenów), więc liczymy go w całości.
- **C4:** oczyszczony tekst z internetu (Common Crawl), ogromny. Bierzemy stały wycinek walidacji: 256 okien po 2048 tokenów, ze stałym ziarnem losowania.

| | A (rek.) | B | C |
|---|---|---|---|
| okno | 2048 | 4096 | 2048 + 4096 dla najlepszych |
| porównywalność z artykułami | tak | słaba | tak |
| czas | 1× | ~2× | 1× + trochę |
| bliżej realnego użycia | mniej | bardziej | oba |

**Najważniejsze:** nie ma jednej „prawdziwej” perplexity. Liczy się to, żeby **każdy wariant był mierzony identycznie**. Opcja A daje dodatkowo porównywalność z literaturą.
