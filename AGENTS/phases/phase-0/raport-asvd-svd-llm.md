# Raport: jak działają ASVD i SVD-LLM

*2026-10-29 19:48 — Claude Opus 5.5*

## Co masz zrobić

Nic do decyzji, to raport do nauki (prośba z dyskusji `AGENTS/phases/phase-0/katalog-metod.md`). Pytania albo „rozwiń X” napisz w tej samej dyskusji katalogu.

**W jednym zdaniu:** obie metody zastępują macierz wag $W$ iloczynem dwóch chudych macierzy (rozkład SVD), ale zamiast zachowywać to, co duże *w wagach*, zachowują to, co ważne *dla wyjścia warstwy na prawdziwych danych*. ASVD robi to przybliżoną, prostą sztuczką, a SVD-LLM robi to dokładnie.

---

## 0. Punkt wyjścia: zwykłe SVD i dlaczego zawodzi

Warstwa liniowa liczy $y = Wx$, gdzie $W \in \mathbb{R}^{m \times n}$ ($n$ wejść, $m$ wyjść). Każdą macierz da się rozłożyć (SVD):

$$W = U \Sigma V^\top = \sum_{i} \sigma_i\, u_i v_i^\top, \qquad \sigma_1 \ge \sigma_2 \ge \dots \ge 0$$

Słownie: $W$ to suma prostych „warstw” $u_i v_i^\top$, każda z wagą $\sigma_i$ (wartość osobliwa). **Kompresja:** zostawiamy $k$ największych:

$$W \approx W_k = \underbrace{U_k \Sigma_k}_{A\;(m \times k)}\; \underbrace{V_k^\top}_{B\;(k \times n)}$$

Zamiast $mn$ liczb trzymamy $k(m+n)$, a warstwa liczy $y \approx A(Bx)$, czyli dwa mniejsze mnożenia. Opłaca się, gdy $k < \frac{mn}{m+n}$.

Zwykłe SVD minimalizuje **błąd wag** $\lVert W - W_k \rVert_F$ (twierdzenie Eckarta–Younga). Nas obchodzi jednak **błąd wyjścia** na prawdziwych danych. Gdy $X \in \mathbb{R}^{n \times N}$ to $N$ tokenów z danych kalibracyjnych (kolumny), chodzi o $\lVert WX - W_kX \rVert_F$. Czym są dane kalibracyjne: `AGENTS/phases/phase-0/A3-dane-kalibracyjne.md`.

**Przykład, który pokazuje problem.** Weźmy $W = \begin{pmatrix} 1 & 0 \\ 0 & 2 \end{pmatrix}$ i przytnijmy do rzędu $k = 1$. Wartości osobliwe to 2 i 1, więc zwykłe SVD zostawia $\sigma = 2$ (wejście 2) i wyrzuca wejście 1. Załóżmy jednak, że w danych **wejście 1 ma wartości około 100**, a wejście 2 około 1 (w LLM takie „kanały-outliery” naprawdę występują):

- zwykłe SVD wyrzuca wejście 1, więc błąd wyjścia to ok. $1 \cdot 100 = 100$;
- gdyby wyrzucić wejście 2, błąd wyniósłby ok. $2 \cdot 1 = 2$.

Zwykłe SVD wybrało **50 razy gorzej**, bo nie patrzy na dane. To dlatego naiwne SVD tak szybko psuje LLM.

## 1. ASVD (*Activation-aware SVD*, 2023)

**Pomysł:** zanim zrobimy SVD, „powiększamy” kolumny $W$ mnożone przez duże aktywacje, żeby SVD uznało je za ważne.

1. Z danych kalibracyjnych liczymy dla każdego wejścia $j$ średnią wielkość aktywacji i robimy z niej skalę:
$$s_j = \Big(\tfrac{1}{N} \textstyle\sum_t \lvert X_{jt} \rvert\Big)^{\alpha}, \qquad S = \mathrm{diag}(s_1, \dots, s_n), \quad \alpha \approx 0{,}5$$
2. Zapisujemy $W = (WS)\,S^{-1}$ (to nic nie zmienia, bo $SS^{-1} = I$) i robimy SVD **przeskalowanej** macierzy: $WS \approx U_k \Sigma_k V_k^\top$.
3. Odwracamy skalowanie w drugim czynniku:
$$W \approx \underbrace{U_k \Sigma_k}_{A}\; \underbrace{V_k^\top S^{-1}}_{B}$$

Słownie: skala $S$ „wchodzi” do SVD i „wychodzi” w macierzy $B$. Za darmo, bo nie dochodzi żadna dodatkowa macierz. W przykładzie wyżej $S \approx \mathrm{diag}(10, 1)$ (pierwiastek ze 100 i z 1), więc $WS = \mathrm{diag}(10, 2)$ i SVD zachowuje już wejście 1.

**Dwa dodatki ASVD:**
- **Różny rząd w różnych warstwach:** warstwy różnią się wrażliwością. ASVD dla każdej warstwy sprawdza, o ile rośnie perplexity (`AGENTS/phases/phase-0/A4-perplexity.md`) przy różnym stopniu kompresji, i daje większe $k$ warstwom wrażliwym, a mniejsze odpornym.
- **Mniejszy KV cache:** jeśli tak skompresujemy macierze kluczy i wartości w atencji, w pamięci kontekstu można trzymać krótszy wektor $Bx$ zamiast pełnych kluczy i wartości. Przy długim myśleniu Qwen3 to sporo pamięci.

**Słabość:** skala $\alpha$ to heurystyka, a $S$ jest diagonalna, czyli każde wejście skalujemy osobno i pomijamy, że wejścia są ze sobą skorelowane. Nie ma gwarancji, że odcięcie najmniejszych $\sigma_i$ macierzy $WS$ daje najmniejszy błąd wyjścia.

## 2. SVD-LLM (2024)

**Pomysł:** zamiast heurystycznej skali bierzemy taką macierz $S$, przy której odcięcie najmniejszych wartości osobliwych daje **dokładnie** najmniejszy błąd wyjścia.

1. Z danych liczymy $XX^\top$ (macierz $n \times n$: jak wejścia współwystępują; **ta sama macierz co Hesjan $H$ w GPTQ**) i robimy rozkład Cholesky'ego:
$$XX^\top = SS^\top \qquad (S \text{ — dolnotrójkątna})$$
2. SVD macierzy $WS = U \Sigma V^\top$ i przycięcie:
$$W' = U_k \Sigma_k V_k^\top S^{-1}$$

**Dlaczego to działa (krok po kroku):**

$$WX - W'X = \big(WS - U_k\Sigma_kV_k^\top\big)\, S^{-1}X$$

Macierz $S^{-1}X$ ma tę własność, że

$$(S^{-1}X)(S^{-1}X)^\top = S^{-1}XX^\top S^{-\top} = S^{-1}SS^\top S^{-\top} = I$$

czyli mnożenie przez nią **nie zmienia normy Frobeniusa**. Stąd

$$\lVert WX - W'X \rVert_F = \lVert WS - U_k\Sigma_kV_k^\top \rVert_F = \sqrt{\textstyle\sum_{i > k} \sigma_i^2}$$

Słownie: $S^{-1}$ **„wybiela” dane**. Po przekształceniu wszystkie kierunki wejścia są równie ważne i niezależne, więc zwykłe SVD (optymalne dla wag) staje się optymalne dla wyjścia. Do tego każda wartość osobliwa $\sigma_i$ mówi **dokładnie**, ile kosztuje jej usunięcie. ASVD tego nie gwarantuje.

**Drugi element SVD-LLM: dostrojenie po przycięciu.** Przy mocnej kompresji (np. 40–60% parametrów mniej) sam rozkład zostawia już spory błąd. SVD-LLM dostraja więc oba czynniki ($A$, a potem $B$) krótkim treningiem LoRA na danych. To krok opcjonalny i kosztowniejszy (trening zamiast samych obliczeń). Późniejsza wersja metody (2025) dobiera dodatkowo stopień kompresji osobno dla każdej warstwy.

**Szczegół techniczny:** $XX^\top$ bywa prawie osobliwa (rozkład Cholesky'ego się wtedy nie udaje), więc dodaje się małe $\lambda I$ i liczy w podwójnej precyzji.

## 3. Porównanie

| | Zwykłe SVD | ASVD | SVD-LLM |
|---|---|---|---|
| patrzy na dane | nie | tak (średnie aktywacje) | tak (pełne $XX^\top$) |
| skala $S$ | brak | diagonalna, heurystyczna | trójkątna, z rozkładu Cholesky'ego |
| odcina optymalnie dla wyjścia | nie | w przybliżeniu | **tak (dowód wyżej)** |
| koszt policzenia | sekundy | minuty (+ szukanie rzędów) | minuty (+ opcjonalny trening LoRA) |
| dodatki | — | rząd per warstwa, mniejszy KV cache | dostrojenie LoRA |

## 4. Co to znaczy u nas (Qwen3-0.6B)

- Warstwa MLP `up_proj` ma $W \in \mathbb{R}^{3072 \times 1024}$. Opłacalność zaczyna się od $k < \frac{3072 \cdot 1024}{3072 + 1024} = 768$. Żeby mieć 40% mniej parametrów w tej warstwie: $k \approx 0{,}6 \cdot 768 \approx 460$.
- Rachunki są małe ($XX^\top$ to $1024 \times 1024$ albo $3072 \times 3072$), więc dla 0.6B cała kompresja zajmie minuty, a 8B da się zrobić warstwa po warstwie na 12 GB.
- **Przyspieszenie** jest realne dopiero przy wyraźnie małym $k$ (dwa mnożenia zamiast jednego). **Oszczędność pamięci** jest wprost proporcjonalna.
- Da się to łączyć z kwantyzacją: czynniki $A$ i $B$ też można skwantyzować.
- Dane kalibracyjne: według @phase-0:K8 = C mieszanka C4 + kod.
- Kod: oficjalne repozytoria obu metod są pisane pod Llamę (⚠️ w katalogu), ale rdzeń metody to kilkadziesiąt linii (`torch.linalg.cholesky`, `torch.linalg.svd`). Jeśli wybierzesz te metody, sprawdzę, co łatwiej uruchomić na Qwen3 (@L9).
