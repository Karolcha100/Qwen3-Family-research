# Główny pomysł — opis matematyczny (raport 1 z 2)

*2026-10-29 20:45 — Claude Opus 5.5*

**Status raportu:** zamknięty (2026-11-01 14:28, Claude Opus 5.5 na prośbę autora @T018)
## Co masz zrobić

Sprawdź, czy dobrze zrozumiałem Twój pomysł (@T009). To **zapis Twojego pomysłu językiem matematyki**, bez oceny; ocena jest w `AGENTS/phases/phase-2/raport-2-opinia.md`. Miejsca, w których pomysł dopuszcza kilka odczytań, oznaczyłem **[wybór → K…]**. Decyzje są w `AGENTS/phases/phase-2/agents-issues-1.md`. Jeśli coś zrozumiałem źle, napisz w @T009.

---

## 0. Czym jest „neuron” w Qwen3-0.6B

Qwen3-0.6B to 28 warstw (bloków). Każdy blok ma dwie części, które dopisują swój wynik do wspólnego „strumienia” $h \in \mathbb{R}^{1024}$ (tzw. strumień rezydualny):

$$h \leftarrow h + \mathrm{Attn}_\ell\big(\mathrm{RMSNorm}(h)\big), \qquad h \leftarrow h + \mathrm{MLP}_\ell\big(\mathrm{RMSNorm}(h)\big)$$

Słownie: każda warstwa czyta strumień, liczy poprawkę i ją do niego dodaje.

Część MLP (typu SwiGLU) dla wejścia $x \in \mathbb{R}^{1024}$:

$$\mathrm{MLP}(x) = W_{\text{down}}\Big(\mathrm{SiLU}(W_{\text{gate}}\,x) \odot W_{\text{up}}\,x\Big), \qquad W_{\text{gate}}, W_{\text{up}} \in \mathbb{R}^{3072 \times 1024},\; W_{\text{down}} \in \mathbb{R}^{1024 \times 3072}$$

**Neuron $j$ warstwy $\ell$** to jedna z 3072 „ścieżek” w środku MLP. Ma swoją aktywację (jedną liczbę na token)

$$a_j = \mathrm{SiLU}(g_j^\top x)\cdot(u_j^\top x)$$

i dopisuje do strumienia wektor $a_j\, d_j$, gdzie $g_j, u_j$ to $j$-te wiersze $W_{\text{gate}}, W_{\text{up}}$, a $d_j$ to $j$-ta kolumna $W_{\text{down}}$. Słownie: neuron sprawdza, czy wejście „pasuje” do jego wzorca, i jeśli tak, dodaje do strumienia swój kierunek $d_j$ z siłą $a_j$.

Tak rozumiany neuron da się **usunąć z modelu** (skasować wiersz $g_j$, wiersz $u_j$ i kolumnę $d_j$), co jest dokładnie Twoim „z 1000 neuronów do 800”. W liczbach: $28 \times 3072 = 86\,016$ neuronów. MLP to 44% z 596 mln parametrów modelu (reszta: atencja 30%, słownik/embedding 26%).

**[wybór → K1]** Inne możliwe „neurony”: wymiary strumienia (1024, wspólne dla wszystkich warstw, więc nie da się ich zmniejszyć w jednej warstwie) albo głowy atencji (16 na warstwę).

## A. Wpływ zaburzenia pojedynczego neuronu

**Zaburzenie** neuronu $j$ w warstwie $\ell$ o $\delta \in \{-1, -0{,}5, 0{,}5, 1\}$ **[wybór → K2]**:

- mnożące (rekomendacja): $a_j \leftarrow (1+\delta)\,a_j$. $\delta = -1$ **wyłącza** neuron, $-0{,}5$ go osłabia, $+0{,}5$ i $+1$ wzmacniają (×1,5 i ×2);
- dodające, w skali neuronu: $a_j \leftarrow a_j + \delta\,\sigma_j$, gdzie $\sigma_j$ to typowe odchylenie aktywacji tego neuronu w danych;
- dodające, wprost: $a_j \leftarrow a_j + \delta$ (ta sama liczba dla neuronów o bardzo różnej skali, więc wyniki trudno porównać).

**Miara skutku** (czy model nadal ma sens) **[wybór → K3]**. Na zbiorze $T$ tokenów porównujemy rozkład następnego tokenu modelu oryginalnego $p_t$ i zaburzonego $p_t^{(\ell,j,\delta)}$:

$$\Delta_{\ell,j,\delta} = \frac{1}{T}\sum_{t=1}^{T} D_{\mathrm{KL}}\!\left(p_t \,\Big\|\, p_t^{(\ell,j,\delta)}\right)$$

Słownie: średnio o ile zmienia się to, co model „chce powiedzieć”, gdy ruszymy jeden neuron. 0 oznacza brak zmiany. Uzupełniająco: zmiana straty (perplexity), a dla neuronów o największym $\Delta$ ręczne sprawdzenie wygenerowanego tekstu.

**Koszt.** Pełne przeszukanie to $86\,016 \times 4 \approx 344$ tys. przebiegów modelu po $T$ tokenach. Dwie sztuczki zmniejszają koszt **[wybór → K4]**:

1. **Start od zaburzanej warstwy:** wyniki warstw $1..\ell-1$ są wspólne dla wszystkich neuronów warstwy $\ell$. Liczymy je raz, a różne zaburzenia upychamy w jeden wsad (batch).
2. **Przybliżenie gradientem (przesiew):** dla małych zaburzeń zmianę logitów $z$ można przybliżyć liniowo, $\Delta z \approx \delta\, a_j\, J_j$, gdzie $J_j = \partial z / \partial a_j$. Wtedy

$$D_{\mathrm{KL}} \approx \frac{\delta^2 a_j^2}{2}\; J_j^\top\big(\mathrm{diag}(p) - pp^\top\big)\,J_j$$

Słownie: jeden przebieg wstecz (gradient) daje przybliżony wpływ **wszystkich** neuronów naraz. Dokładnie liczymy tylko te, które przybliżenie wskazało jako ważne. Ten wzór jest symetryczny w $\delta$, więc **różnica skutku dla $-1$ i $+1$ to efekt nieliniowy**, ciekawy sam w sobie (patrz B).

## B. Rodzaje neuronów w każdej warstwie

Każdy neuron dostaje zestaw etykiet (może mieć kilka). Przykładowe definicje; progi ($\tau, \kappa, \rho, \lambda$) ustalimy po zobaczeniu rozkładów:

| Rodzaj | Warunek (słownie) | Wzór |
|---|---|---|
| martwy | prawie nigdy się nie aktywuje | $\Pr_t\big(\lvert a_{j,t}\rvert > \epsilon\big) < \tau$ |
| krytyczny | wyłączenie mocno zmienia model | $\Delta_{\ell,j,-1} > \kappa$ |
| zbędny | żadne zaburzenie nic nie zmienia | $\max_\delta \Delta_{\ell,j,\delta} < \kappa_0$ |
| asymetryczny | inaczej znosi osłabienie niż wzmocnienie | $\dfrac{\lvert \Delta_{\ell,j,+1} - \Delta_{\ell,j,-1}\rvert}{\max(\Delta_{\ell,j,+1}, \Delta_{\ell,j,-1})} > \rho$ |
| „masywny” | rzadko, ale ogromnie duże aktywacje | $\max_t \lvert a_{j,t}\rvert > \lambda \cdot \mathrm{mediana}_t \lvert a_{j,t}\rvert$ |
| selektywny | aktywuje się dla wąskiej grupy tokenów (np. kod, liczby, inny język) | niska entropia rozkładu „masy aktywacji” po typach tokenów |

**Wykresy:** dla każdej warstwy $\ell$ liczba neuronów każdego rodzaju (wykres słupkowy warstwa × rodzaj albo mapa ciepła) oraz rozkład $\Delta_{\ell,j,-1}$ w każdej warstwie.

## C. Zmniejszenie wybranych warstw

**C1. Wybór warstw i neuronów.** Ważność neuronu $I_{\ell,j}$ (np. $\Delta_{\ell,j,-1}$ z A) i wrażliwość warstwy $S_\ell$ (np. jak rośnie KL, gdy usuwamy jej najmniej ważne neurony). Zostawiamy w warstwie $\ell$ tylko $k_\ell = \lfloor r_\ell \cdot 3072 \rfloor$ najważniejszych neuronów, a ułamki $r_\ell$ dobieramy tak, żeby przy zadanej łącznej liczbie usuniętych neuronów suma wrażliwości była najmniejsza:

$$\min_{r_1..r_{28}} \sum_\ell S_\ell(r_\ell) \quad \text{przy} \quad \sum_\ell (1 - r_\ell)\cdot 3072 = N_{\text{usuń}}$$

Słownie: tniemy tam, gdzie boli najmniej.

**C2. Zebranie danych.** Przepuszczamy przez oryginalny model $N_{\text{tokens}}$ tokenów i dla zmniejszanej warstwy $\ell$ zapisujemy pary (wejście, cel). Według Twojego opisu **[wybór → K5]**:

- **wariant lokalny:** $x_t$ = wejście do MLP warstwy $\ell$, $y_t = \mathrm{MLP}_\ell(x_t)$;
- **wariant „przez następną warstwę”:** $x_t = h^{(\ell-1)}_t$ (wyjście warstwy poprzedniej), $y_t = h^{(\ell+1)}_t$ (wyjście warstwy następnej). Warstwa $\ell+1$ jest zamrożona, więc błędy, które ona i tak „wygasza”, nie są karane.

Danych nie trzeba zapisywać na dysk: oryginalny model (1,2 GB) mieści się obok i może liczyć cele na bieżąco **[wybór → K6]**. Dla porównania zapis na dysk: $2 \times 1024$ liczb × 2 bajty × 1 mln tokenów ≈ 4 GB na warstwę.

**C3. Trening zmniejszonej warstwy.** Zmniejszony MLP $\widetilde{\mathrm{MLP}}_\ell$ (z $k_\ell$ neuronami) uczymy, żeby odtwarzał cel:

$$\min_{\widetilde{W}} \; \frac{1}{N}\sum_{t=1}^{N} \big\lVert y_t - \widetilde{f}(x_t) \big\rVert_2^2$$

gdzie $\widetilde f$ to zmniejszony MLP (wariant lokalny) albo zmniejszony MLP + zamrożona warstwa $\ell+1$ (wariant „przez następną”). **Start** **[wybór → K7]**: z wag zachowanych neuronów oryginału. Dodatkowo macierz $\widetilde W_{\text{down}}$ można policzyć od razu dokładnie, metodą najmniejszych kwadratów. Gdy $A \in \mathbb{R}^{k \times N}$ to aktywacje zachowanych neuronów, a $Y \in \mathbb{R}^{1024 \times N}$ to cele (wariant lokalny):

$$\widetilde W_{\text{down}} = Y A^\top \big(AA^\top + \lambda I\big)^{-1}$$

Słownie: pozostałe neurony dostają nowe kierunki wyjścia, które najlepiej zastępują te usunięte. To kilka sekund rachunku, bez treningu, a dopiero potem ewentualny trening gradientowy.

**C4. Podmiana i dotrenowanie całego modelu.** Wkładamy $\widetilde{\mathrm{MLP}}_\ell$ w miejsce oryginału i dotrenowujemy cały model (uczeń), żeby naśladował oryginał (nauczyciel):

$$\mathcal{L} = \frac{1}{T}\sum_{t=1}^{T} D_{\mathrm{KL}}\!\left(p^{\text{nauczyciel}}_t \,\Big\|\, p^{\text{uczeń}}_t\right)$$

Słownie: uczymy zmniejszony model dawać te same rozkłady następnego tokenu co oryginał (destylacja). **[wybór → K8]**: dotrenowujemy wszystkie wagi, LoRA czy tylko zmniejszone warstwy.

## Podsumowanie przepływu

```text
A: zaburzenia neuronów  →  Δ(ℓ, j, δ) dla 86 016 neuronów × 4 zaburzenia
B: etykiety neuronów    →  wykresy rodzajów neuronów w 28 warstwach
C1: wybór warstw/neuronów do usunięcia (z A i B)
C2: dane (wejście, cel) dla zmniejszanych warstw
C3: trening zmniejszonej warstwy (start: zachowane neurony + najmniejsze kwadraty)
C4: podmiana + destylacja całego modelu  →  ewaluacja (poziomy 1–3, @T002)
```

## Dyskusja

---
---
---

🔒 Dyskusja zakończona na prośbę autora (@T018). Podsumowanie wszystkich raportów Phase 2: `AGENTS/phases/phase-2/raport-zbiorczy-phase-2.md`.

*2026-11-01 14:28 — Claude Opus 5.5*

---
---
---
