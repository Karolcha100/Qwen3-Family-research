# Etap 2 — mapa wrażliwości wszystkich 86 016 neuronów

*2026-10-30 02:05 — Claude Opus 5.5*

**Status raportu:** zamknięty (2026-11-01 14:28, Claude Opus 5.5 na prośbę autora @T018)
## Co masz zrobić

Przeczytaj i odpowiedz na **K17** i **K18** w `AGENTS/phases/phase-2/agents-issues-3.md` (czy akceptujesz mapę z przesiewu oraz co zrobić z tym, że tekst i kod mają różne ważne neurony). Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”. Uwagi i pytania do raportu możesz pisać w GUI pod tym raportem (Drzewo → Raporty albo „Co czeka na mnie” → Raporty do przeczytania i dyskusji); przyciskiem „🔒 Zakończ dyskusję” zamykasz raport.

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

![Ile tokenów potrzeba](AGENTS/phases/phase-2/figures/etap2-ile-tokenow.png)

Jak powstał wykres: losujemy dwa rozłączne zbiory po $k$ sekwencji, z każdego liczymy ranking neuronów i sprawdzamy, jak bardzo oba rankingi się zgadzają (średnia z 8 losowań). Kolorowe linie to warstwy pilota, kropkowana to średnia z 28 warstw, krzyżyki to pomiar dokładny z pilota (4096 tokenów), a przerywana linia to próg 0,95 z reguł @T010. Co widać: zgodność rośnie z liczbą tokenów i nawet przy 65 tys. tokenów nie dochodzi do 0,95. Pomiar dokładny na 4096 tokenach (krzyżyki) jest tak samo niepewny jak przesiew na tej samej liczbie tokenów.

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

![Tekst a kod](AGENTS/phases/phase-2/figures/etap2-tekst-kod.png)

Dwie górne linie: rankingi z dwóch porcji tego samego rodzaju tekstu zgadzają się w 0,7–0,9 w każdej warstwie. Dolna linia: ranking z tekstu C4 i ranking z kodu zgadzają się prawie wcale (wokół zera).

Gdyby różnica wynikała tylko z szumu, tekst i kod zgadzałyby się mniej więcej tak jak dwie porcje tekstu. Zgadzają się jednak **prawie wcale**. Neurony ważne dla kodu to w dużej mierze inne neurony niż ważne dla tekstu. Mapa z mieszanki 75/25 jest kompromisem; pytanie **K18**.

## 5. Mapa: jak wrażliwe są warstwy

![Wrażliwość warstw](AGENTS/phases/phase-2/figures/etap2-wrazliwosc-warstw.png)

Lewy wykres: dla każdej warstwy mediana (niebieska linia), pasmo, w którym mieści się 80% neuronów (niebieskie tło), i najważniejszy neuron (pomarańczowa linia); oś pionowa jest logarytmiczna. Co widać: typowy neuron ma w każdej warstwie podobny, mały skutek ($1$–$4 \cdot 10^{-5}$), najmniejszy w warstwach 12–15. Różnice między warstwami robią pojedyncze bardzo ważne neurony: w warstwie 2 i w dwóch ostatnich warstwach są 400–1500× ważniejsze od mediany.

Prawy wykres: suma przewidywanej KL wszystkich neuronów warstwy, osobno z tekstu (48 sekwencji C4) i z kodu (16 sekwencji). Co widać: ostatnia warstwa 27 odstaje dla obu rodzajów tekstu. W warstwach 0–8 suma dla kodu jest najwyżej o 1/5 mniejsza niż dla tekstu, w warstwach 9–18 około 1,3× mniejsza, a w warstwach 19–26 1,6–2,3× mniejsza. Nie znaczy to, że te warstwy są dla kodu nieważne. Kod jest dla modelu łatwiej przewidywalny (pewniejsze przewidywania), więc pojedynczy neuron mniej zmienia rozkład następnego tokenu. Liczy się to, **które** neurony są ważne, a to dla tekstu i kodu są różne neurony (sekcja 4).

Liczby w tabeli dotyczą mapy z całej mieszanki.

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

![Przesiew a pomiar dokładny w 25 warstwach](AGENTS/phases/phase-2/figures/etap2-przesiew-vs-dokladnie.png)

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

## Dyskusja

---
---
---

Nie widzę w "5. Mapa: jak wrażliwe są warstwy" wykresów (ani opisu lewego wykresu, jeżeli był)

*2026-10-30 10:22 — Autor*

---
---
---

Najbardziej interesuje mnie "4. Tekst a kod: inne ważne neurony", a dokładnie, to żeby qwen jak najlepiej programował, co możesz na ten temat powiedzieć?

*2026-10-30 10:25 — Autor*

---
---
---

## Co masz zrobić

Odpowiedz na pytania **K25–K30** w `AGENTS/phases/phase-2/agents-issues-4.md`; najważniejsze są K25 (co ma najlepiej przetrwać zmniejszanie) i K26 (na jakich danych liczymy mapę). Jeśli coś tu jest niejasne, napisz pod raportem.

### 1. Wykresy w sekcji 5

Masz rację. Wykres był jeden, z dwiema połowami: stał w sekcji 3, lewa połowa była opisana tam, a prawą opisywała sekcja 5, w której nie było obrazka. Rozdzieliłem go:
- **sekcja 3:** własny wykres „ile tokenów potrzeba” z opisem, jak powstał i co widać;
- **sekcja 5:** nowy wykres z dwiema częściami: pojedyncze neurony w każdej warstwie oraz suma dla całej warstwy, osobno dla tekstu i kodu. Pod nim jest opis „co widać”.

### 2. Tekst a kod: co wyniki mówią o programowaniu

1. **Neurony ważne dla kodu to inne neurony niż ważne dla tekstu, i to nie jest szum.** Mapa z samego kodu (16 sekwencji, 32 tys. tokenów, 7 języków z GitHuba) jest stabilna. Dwie połowy kodu zgadzają się średnio w 0,78, a dwie porcje tekstu tej samej wielkości w 0,82. Mimo to ranking z kodu i ranking z tekstu zgadzają się tylko w −0,15…0,23.
2. **Obecna mapa to w praktyce mapa tekstu.** Zgadza się z mapą z tekstu w 0,87, a z mapą z kodu tylko w 0,37 (średnio po warstwach). Kod to 1/4 danych i do tego daje mniejsze wartości KL (punkt 4), więc ma jeszcze mniejszy wpływ na ranking.
3. **Ile kosztowałoby to kod.** Sprawdziłem na gotowych wynikach, bez GPU, porównując różne mapy:
   - mapa powstaje z połowy sekwencji, a szkodę sprawdzam na drugiej połowie, żeby mapa nie „znała” tekstu, na którym ją oceniam;
   - szkoda to suma przewidywanej KL wyciętych neuronów, podzielona przez najmniejszą możliwą (1 = najlepiej).

![Mapa dla kodu](AGENTS/phases/phase-2/figures/etap2-mapa-dla-kodu.png)

Co widać:
- **obecna mieszanka** (75% tekstu) szkodzi kodowi **1,75–1,8×** bardziej, niż to konieczne, a tekstowi tylko 1,1–1,2×;
- mapa z samego tekstu szkodzi kodowi 3,8–5,8×;
- mapa z samego kodu najlepiej chroni kod, ale tekstowi szkodzi 2,7–3,9×;
- **75% kodu + 25% tekstu:** kod prawie najlepiej (1,07–1,08×), tekst 1,6–1,8×;
- pół na pół: kod 1,23–1,26×, tekst 1,36–1,48×;
- sama średnia aktywacja (bez KL) jest gorsza od obecnej mieszanki dla obu rodzajów (kod 2,6–2,9×, tekst 1,75–2,0×).

4. **Późne warstwy są na kodzie mniej wrażliwe.** W warstwach 19–26 suma przewidywanej KL dla kodu jest 1,6–2,3× mniejsza niż dla tekstu (nowy wykres w sekcji 5). Model jest pewniejszy przy kodzie, więc pojedynczy neuron mniej zmienia jego przewidywania. Hipoteza do sprawdzenia: przy celu „programowanie” późne warstwy (poza ostatnią) da się zmniejszyć mocniej niż przy celu „tekst”.
5. **Z etapu 3:** 6446 neuronów działa ponad 2× silniej na kodzie niż na tekście. Najwięcej ich jest w późnych warstwach (do 599 w warstwie 27).

**Zastrzeżenia:**
- To przewidywanie z sumy skutków pojedynczych neuronów. Przy prawdziwym wycinaniu skutki się nie dodają. W etapie 4 przewaga mapy przeniosła się na prawdziwe wycinanie (KL mniejsza o 14–37%), ale dla kodu trzeba to sprawdzić tak samo (K30).
- Mapy w tym porównaniu powstały z połowy danych (8 sekwencji kodu), więc dokładne liczby są przybliżone; kierunek jest ten sam przy 20% i 40%.
- Mniejsza KL na kodzie to nie to samo co „dobrze programuje”: tego dotyczy K27.

### 3. Co bym zrobił, żeby Qwen jak najlepiej programował

1. **Cel (K25):** ustalić, co ma przetrwać zmniejszanie. Dziś chronimy głównie zwykły tekst.
2. **Dane pod cel (K26):** rekomenduję 75% kodu + 25% zwykłego tekstu, i to nie tylko dla mapy. Najmniejsze kwadraty i trening z etapu 4 uczą się teraz na 75% tekstu, więc „naprawiają” głównie tekst; przy celu „programowanie” zbiór do naprawy też powinien być głównie kodem. Zwykłego tekstu nie usuwałbym całkiem, bo polecenia, komentarze, nazwy i opisy funkcji są pisane zwykłym językiem.
3. **Pomiar programowania (K27):** zadania z testami (HumanEval, MBPP) obok KL.
4. **Języki (K28):** napisz, w czym programujesz. Mapa chroni to, na czym ją liczymy.
5. **Punkt odniesienia (K29):** mały model Qwen trenowany od początku na kodzie, żeby wiedzieć, do czego się porównujemy.
6. **Sprawdzenie na prawdziwym wycinaniu (K30):** powtórka etapu 4 z mapą pod kod i oceną osobno na kodzie i tekście (~1 h GPU po Twoim „uruchom”).

Pliki: `scripts/phase2_code_text_maps.py` (analiza i wykres), `results/phase2/stage2/code-text-maps.json` (liczby).

*2026-10-30 10:42 — Claude Opus 5.5*

---
---
---

🔒 Dyskusja zakończona na prośbę autora (@T018). Podsumowanie wszystkich raportów Phase 2: `AGENTS/phases/phase-2/raport-zbiorczy-phase-2.md`.

*2026-11-01 14:28 — Claude Opus 5.5*

---
---
---
