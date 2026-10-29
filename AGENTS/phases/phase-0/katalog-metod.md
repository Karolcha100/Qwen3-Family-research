# Katalog metod kompresji (do wyboru przez autora)

*2026-10-29 16:21 — Claude Opus 5.5*

**Status planu:** do opiniowania

## Co masz zrobić

To materiał do Twojego wyboru metod (@phase-0:K6: gotowe biblioteki, metody wybierasz Ty; @phase-0:K34 = B). Nic tu nie jest zdecydowane. Przejrzyj, kiedy będziesz rozpisywać fazy, i napisz w dyskusji pytania albo co Cię ciekawi. Na końcu jest moja propozycja zestawu startowego. Możesz ją przyjąć, zmienić albo zignorować.

Oznaczenia w kolumnie „Qwen3”: ✅ biblioteka obsługuje Qwen3 (albo dowolne warstwy liniowe), ⚠️ kod badawczy pisany pod Llamę, który może wymagać przeróbek; sprawdzę to przed wyborem. Stan bibliotek według mojej wiedzy (do połowy 2026), do potwierdzenia przy instalacji.

---

## 1. Kwantyzacja wag (mniej bitów na wagę)

Wspólna idea: każdą wagę $w$ zastępujemy jedną z $2^b$ wartości ($b$ = liczba bitów). W najprostszej wersji z grupą wag dzielącą skalę $s$ i zero $z$:

$$q = \mathrm{clamp}\!\left(\mathrm{round}\!\left(\frac{w}{s}\right) + z,\; 0,\; 2^b - 1\right), \qquad \hat{w} = s\,(q - z)$$

Słownie: dzielimy wagę przez skalę, przesuwamy o zero $z$, zaokrąglamy do liczby całkowitej z zakresu $0 \dots 2^b-1$ (to zapisujemy jako $q$, np. w 4 bitach) i przy użyciu odwracamy: $\hat{w}$ to przybliżenie oryginalnej wagi. Metody różnią się tym, **jak wybierają skale i zaokrąglenia**.

| Metoda | Idea w skrócie | Dane | Biblioteka | Qwen3 | Na 12 GB | Czego uczy |
|---|---|---|---|---|---|---|
| **RTN** | zwykłe zaokrąglenie, skala z min/max w grupie | nie | PyTorch / dowolna | ✅ | wszystko | punkt odniesienia; jak bardzo szkodzą outliery |
| **HQQ** | optymalizuje skale i zera pod błąd rekonstrukcji wag | nie | `hqq` | ✅ | wszystko | ile da się wycisnąć bez danych |
| **bitsandbytes NF4** | 4-bitowe poziomy dopasowane do rozkładu normalnego wag | nie | `bitsandbytes` | ✅ | wszystko | format z QLoRA; kwantyle zamiast równych przedziałów |
| **GPTQ** | kwantyzuje kolumny po kolei i kompensuje błąd w pozostałych wagach (Hesjan $H = 2XX^\top$) | tak | `GPTQModel`, `llm-compressor` | ✅ | 8B warstwa po warstwie | kompensacja błędu drugiego rzędu |
| **AWQ** | skaluje kanały z dużymi aktywacjami przed kwantyzacją, żeby je chronić | tak | `llm-compressor` (AutoAWQ zarchiwizowany) | ✅ | 8B warstwa po warstwie | rola outlierów w aktywacjach |
| **GGUF k-quants / i-quants + imatrix** | formaty llama.cpp (Q4_K_M, IQ3…); imatrix to statystyki aktywacji, które ważą błąd | opcjonalnie | llama.cpp | ✅ | wszystko | jak kwantyzuje się „w praktyce” lokalnie |
| **EXL3** | kwantyzacja trellisowa (QTIP) w wielu bitrate'ach, np. 2,5 bita | tak | `exllamav3` | ⚠️ | do 8B | ułamkowe bity na wagę |
| **AQLM** | kwantyzacja wektorowa: grupy wag → indeksy w książce kodowej, ~2 bity | tak, długo | `aqlm` | ⚠️ | 0.6B–1.7B (godziny) | kwantyzacja wektorowa |
| **QuIP#** | rotacja Hadamarda „rozmazuje” outliery + kraty E8 | tak | kod badawczy | ⚠️ | 0.6B–4B | niekoherencja i rotacje |

## 2. Rotacje i kwantyzacja aktywacji (W4A4, W8A8)

| Metoda | Idea | Dane | Biblioteka | Qwen3 | Czego uczy |
|---|---|---|---|---|---|
| **SmoothQuant (W8A8)** | przenosi „trudność” z aktywacji na wagi skalowaniem kanałów: $Y = (X\,\mathrm{diag}(s)^{-1})(\mathrm{diag}(s)\,W)$ | tak | `llm-compressor` | ✅ | dlaczego aktywacje kwantyzuje się trudniej niż wagi |
| **FP8 (W8A8)** | 8-bitowe liczby zmiennoprzecinkowe; RTX 4070S (Ada) ma sprzętowe FP8 | opcjonalnie | `llm-compressor`, `torchao` | ✅ | formaty zmiennoprzecinkowe vs całkowite |
| **QuaRot / SpinQuant** | rotacje ortogonalne $W \to RW$, $X \to XR^\top$ (wynik bez zmian), które usuwają outliery i pozwalają na W4A4 | tak | kod badawczy; częściowo `llm-compressor` | ⚠️ | najważniejszy pomysł ostatnich lat w kwantyzacji |

## 3. Pruning (zerowanie wag)

Ocena ważności wagi, a potem zerowanie najmniej ważnych:

| Metoda | Ważność wagi | Dane | Biblioteka | Qwen3 | Czego uczy |
|---|---|---|---|---|---|
| **Magnitude** | $\lvert W_{ij}\rvert$ | nie | PyTorch | ✅ | punkt odniesienia (w LLM słaby) |
| **Wanda** | $\lvert W_{ij}\rvert \cdot \lVert X_j \rVert_2$ | tak | `llm-compressor`, repo autorów | ✅ | jak aktywacje zmieniają ważność |
| **SparseGPT** | jak GPTQ: usuwa wagi i kompensuje błąd w pozostałych | tak | `llm-compressor` | ✅ | kompensacja błędu przy pruningu |
| **2:4** | wariant powyższych: w każdej czwórce wag zostają 2 | tak | j.w. + kernele PyTorch | ✅ | sprzętowe przyspieszenie (RTX 4070S je ma) |
| **Usuwanie warstw** (np. ShortGPT) | usuwa całe bloki, które najmniej zmieniają reprezentację | tak | prosty własny skrypt | ✅ | redundancja głębokości modelu |
| **Strukturalny** (LLM-Pruner, w stylu Minitron) | usuwa neurony/głowy, potem leczenie | tak | kod badawczy, NVIDIA ModelOpt | ⚠️ | kompromis jakość ↔ realne przyspieszenie |

## 4. Rozkłady niskiego rzędu

$W \approx AB$, gdzie $W \in \mathbb{R}^{m \times n}$, $A \in \mathbb{R}^{m \times r}$, $B \in \mathbb{R}^{r \times n}$. Opłaca się, gdy $r(m+n) < mn$, czyli $r < \frac{mn}{m+n}$.

| Metoda | Idea | Dane | Biblioteka | Qwen3 | Czego uczy |
|---|---|---|---|---|---|
| **SVD (naiwne)** | obcinamy najmniejsze wartości osobliwe | nie | PyTorch | ✅ | dlaczego wagi LLM nie są niskiego rzędu |
| **ASVD** | SVD ważone wielkością aktywacji | tak | kod badawczy | ⚠️ | znowu: aktywacje decydują, co ważne |
| **SVD-LLM** | SVD po „wybieleniu” danych (rozkład Cholesky'ego $XX^\top$) + aktualizacja | tak | kod badawczy | ⚠️ | związek błędu rozkładu z błędem wyjścia |

## 5. Leczenie po kompresji

| Metoda | Idea | Biblioteka | Qwen3 | Na 12 GB |
|---|---|---|---|---|
| **LoRA + destylacja** | dokładamy małe macierze $\Delta W = BA$ i uczymy je naśladować BF16 (strata KL) | `peft` | ✅ | 0.6B–4B; 8B z QLoRA |
| **QAT** | trening „świadomy kwantyzacji” | `torchao` | ✅ | 0.6B–1.7B |

## 6. Poza wagami (dla ciekawości)

- **Kwantyzacja KV cache** (pamięć kontekstu): przy trybie myślenia (@phase-0:K25 = B, do 8192 tokenów) to ona zjada VRAM. llama.cpp ma ją wbudowaną.

---

## Moja propozycja zestawu startowego (do Twojej decyzji)

Kryteria: dojrzałe biblioteki z obsługą Qwen3, szybkie na 0.6B, a razem pokazują główne idee (bez danych vs z danymi, kompensacja błędu, rola aktywacji).

1. **Kwantyzacja 4 i 3 bity:** RTN → HQQ → GPTQ → AWQ. Ta sama liczba bitów, cztery coraz mądrzejsze pomysły.
2. **llama.cpp:** Q4_K_M bez i z imatrix. Łączy się ze zbudowaną llama.cpp i pokazuje praktykę.
3. **Pruning 50% i 2:4:** magnitude → Wanda → SparseGPT. Odpowiednik punktu 1 dla zerowania wag.

Na później, jeśli Cię wciągnie: rotacje (QuaRot/SpinQuant), kwantyzacja wektorowa (AQLM/QuIP#), SVD-LLM, leczenie LoRA.

## Dyskusja

---
---
---

Zrób mi proszę raport o tym jak działa ASVD oraz SVD-LLM

*2026-10-29 19:42 — Autor*

---
---
---

## Co masz zrobić

Przeczytaj raport `AGENTS/phases/phase-0/raport-asvd-svd-llm.md`. Pytania albo „rozwiń X” napisz tutaj.

**Krótko:**
- **ASVD:** przed rozkładem SVD mnoży kolumny $W$ przez skalę z wielkości aktywacji, więc SVD zachowuje to, co dla danych ważne. To prosta heurystyka, a do tego ASVD dobiera rząd dla każdej warstwy i potrafi zmniejszyć KV cache;
- **SVD-LLM:** zamiast heurystyki „wybiela” dane rozkładem Cholesky'ego $XX^\top = SS^\top$. Wtedy odcięcie najmniejszych wartości osobliwych daje **dowodnie najmniejszy** błąd wyjścia warstwy, a każda $\sigma_i$ mówi dokładnie, ile kosztuje jej usunięcie. Opcjonalnie dostraja wynik przez LoRA.

Przykład z raportu (dwa wejścia, jedno z aktywacjami ~100) i tożsamość SVD-LLM sprawdziłem numerycznie: przy rzędzie 1 zwykłe SVD daje błąd wyjścia ~98, a SVD-LLM ~2. Tożsamość $\lVert WX - W'X \rVert_F = \sqrt{\sum_{i>k}\sigma_i^2}$ zgadza się co do 14 cyfr.

*2026-10-29 19:49 — Claude Opus 5.5*

---
---
---
