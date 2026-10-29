# Phase 2 — plan: mapa neuronów i zmniejszenie jednej warstwy (etapy 1–4 głównego pomysłu)

*2026-10-29 21:13 — Claude Opus 5.5*

**Status planu:** zatwierdzony (2026-10-29 21:36, Autor)
## Co masz zrobić

Przeczytaj plan i zatwierdź (✅ Zatwierdzam plan) albo napisz w dyskusji, co zmienić. Plan obejmuje etapy 1–4 z `AGENTS/phases/phase-pomysl/raport-2-opinia.md` (@phase-pomysl:K9). Uwzględnia wszystkie Twoje decyzje K1–K15 (`AGENTS/phases/phase-pomysl/agents-issues-1.md`, `agents-issues-2.md`). **Każdy etap na GPU uruchamiam dopiero po Twoim „uruchom”** (@phase-0:K10).

## Cel

Zmierzyć, jak ważny jest każdy neuron MLP Qwen3-0.6B, opisać rodzaje neuronów w warstwach i sprawdzić na jednej warstwie, czy da się ją zmniejszyć, zachowując sens modelu.

## Ustalenia (z decyzji)

| | |
|---|---|
| neuron | jedna z 3072 ścieżek MLP w każdej z 28 warstw, razem 86 016 (@phase-pomysl:K1 = A) |
| zaburzenie | $a \to (1+\delta)\,a$, $\delta \in \{-1, -0{,}5, 0{,}5, 1\}$ (K2 = A) |
| miara skutku | średnia KL względem oryginału + zmiana straty; generacja i klasyfikator tylko dla ~250 najważniejszych neuronów (K3 = A) |
| sposób liczenia A | pilot, potem decyzja (K4 = C) |
| model | Qwen3-0.6B-Base, BF16 (pomiary na zwykłym tekście, @phase-0:K7 = A) |
| trening warstwy | „przez następną warstwę”: wejście $h^{(\ell-1)}$, cel $h^{(\ell+1)}$, warstwa $\ell+1$ zamrożona (K5 = B); dane zapisane na dysk (K6); start: zachowane neurony + $W_{\text{down}}$ z najmniejszych kwadratów (K7 = A) |
| wyniki | `results/phase2/*.jsonl` i małe tablice (np. KL dla 86 016 × 4) w repo; duże dane (aktywacje, pary do treningu) w `~/qwen3-checkpoints/phase2/` |

## Etapy

### Etap 1 — pilot części A (3 warstwy)

1. Zbiór pomiarowy: 75% C4 + 25% kod z GitHuba (K11 = A), stałe ziarno, 16 384 tokenów (zapas; pilot sprawdzi, czy wystarczy mniej).
2. Statystyki aktywacji wszystkich 86 016 neuronów (jeden przebieg): średnia, odchylenie, maksimum, odsetek aktywności. Przydadzą się w B.
3. **Dokładnie:** wszystkie neurony warstw 2, 13, 25 (K12) × 4 zaburzenia = 36 864 przebiegi, każdy od zaburzanej warstwy w górę.
4. **Przesiew gradientem** dla tych samych neuronów (raport 1, część A).
5. **Szum:** dla 500 losowych neuronów powtórka dokładnego pomiaru na drugim, rozłącznym zbiorze tokenów.
6. Porównanie: korelacja rang (Spearman) przybliżenie ↔ dokładnie, pokrycie „top 10%”, wielkość szumu, wpływ liczby tokenów (4096 vs 16 384).

**Wynik:** raport `AGENTS/phases/phase-pomysl/etap-1-pilot.md` z rekomendacją, jak liczyć etap 2 i na ilu tokenach. Czas GPU: ~1,5–3 h.

### Etap 2 — część A dla całego modelu

Sposób według pilota: albo wszystko dokładnie (do ~28 h, w kilku sesjach, gdy nie grasz), albo przesiew gradientem dla wszystkich + dokładnie dla ~10% najważniejszych i próbki kontrolnej. **Wynik:** $\Delta_{\ell,j,\delta}$ dla wszystkich neuronów (`results/phase2/`), raport `etap-2-mapa.md`. Czas GPU: od ~1 h do ~28 h.

### Etap 3 — część B: rodzaje neuronów i wykresy

1. Etykiety (raport 1, część B): martwy, krytyczny, zbędny, asymetryczny, „masywny”, selektywny. Progi z rozkładów z etapu 2, z uwzględnieniem szumu z pilota.
2. Wykresy (PNG w folderze fazy, widoczne w GUI): liczba neuronów każdego rodzaju w każdej warstwie, rozkład KL w warstwach, mapa ciepła warstwa × rodzaj.
3. Dla ~250 neuronów o największym KL: generacja odpowiedzi z wyłączonym neuronem i ocena (K3).

**Wynik:** raport `etap-3-rodzaje-neuronow.md` z wykresami. Czas GPU: minuty, plus generacja dla ~250 neuronów.

### Etap 4 — część C na jednej warstwie

1. Wybór warstwy: najmniej wrażliwa według etapów 2–3 (do Twojej akceptacji w raporcie etapu 3).
2. Zapis par $(h^{(\ell-1)}, h^{(\ell+1)})$ dla 1 mln tokenów (K13, ~4 GB).
3. Dla każdego stopnia zmniejszenia (K14: −5%, −10%, −20%, −40%):
   - zostawiamy najważniejsze neurony (według $\Delta_{\ell,j,-1}$);
   - liczymy $\widetilde W_{\text{down}}$ metodą najmniejszych kwadratów;
   - trenujemy zmniejszony MLP „przez zamrożoną warstwę $\ell+1$”;
   - mierzymy KL i perplexity **całego modelu** po podmianie: (a) samo wycięcie, (b) + najmniejsze kwadraty, (c) + trening.
4. Punkt odniesienia na tej samej warstwie: wybór neuronów według prostej ważności „średnia |aktywacja|” (jak w Minitronie), żeby zobaczyć, ile daje ważność z części A.

**Wynik:** raport `etap-4-jedna-warstwa.md` z krzywą „ile wycięte → ile model stracił” dla wariantów (a)/(b)/(c) i obu sposobów wyboru neuronów. Czas GPU: ~1–2 h.

## Czego w tej fazie nie robimy

Zmniejszania wielu warstw naraz, dotrenowania całego modelu i pełnej ewaluacji (lm-eval, evalplus, klasyfikatory). To etapy 5–6, czyli Phase 3 (K10).

## Kod

Pakiet `src/qwen_compression/` (`activations.py`, `perturbation.py`, `metrics.py`, `importance.py`, `reconstruction.py`) + skrypty w `scripts/` (po jednym na etap) + testy w `tests/` (K15 = A). Python 3.14 z typami, bez komentarzy, pełne nazwy. Każdy skrypt zapisuje wyniki z ziarnem i wersjami bibliotek.

## Koniec fazy, gdy

- jest rekomendacja z pilota i pełna mapa $\Delta$ dla 86 016 neuronów;
- są wykresy rodzajów neuronów w 28 warstwach;
- dla jednej warstwy jest krzywa zmniejszania z wariantami (a)/(b)/(c) i porównaniem z prostą ważnością;
- raporty etapów 1–4 są w folderze fazy.

## Dyskusja

---
---
---

Zmiany po Twoich decyzjach z 21:34:
- K3 = A, ale **~250** (nie ~100) neuronów o największym wpływie dostaje generację i ocenę klasyfikatorem (etap 3);
- K14: stopnie zmniejszenia w etapie 4 to **−5%, −10%, −20%, −40%** (Twoja propozycja);
- K10–K13, K15 = A: Phase 2, tekst 75% C4 + 25% kod, warstwy pilota 2/13/25, 1 mln tokenów na dysk, pakiet `src/qwen_compression/`.

Plan czeka na zatwierdzenie (✅ Zatwierdzam plan). Po zatwierdzeniu piszę kod (bez GPU), a etap 1 uruchamiam po Twoim „uruchom”.

*2026-10-29 21:34 — Claude Opus 5.5*

---
---
---

✅ Plan zatwierdzony.

*2026-10-29 21:36 — Autor*

---
---
---

Zamknąłem bo chyba z tego nie korzystamy ostatecznie jak coś - jeżeli nie, to wznów

*2026-10-29 21:38 — Autor*

---
---
---

## Co masz zrobić

1. **Kod etapu 1 (pilot) jest gotowy.** Gdy GPU będzie wolne na ~3 h (np. gdy nie grasz), napisz **„uruchom etap 1”** tutaj albo w czacie. Pilot zapisuje wyniki po każdym kroku, więc da się go przerwać i wznowić.
2. Twój wpis z 21:38 („zamknąłem, bo chyba z tego nie korzystamy”) trafił do tego planu, ale chodzi chyba o **plan metryk** (`AGENTS/phases/phase-0/plan-metryki-oceny.md`). Niech zostanie zatwierdzony: **korzystamy z niego** w etapie 3 (ocena ~250 najważniejszych neuronów klasyfikatorem) i w Phase 3 (ocena zmniejszonych modeli). Jeśli chodziło o coś innego, napisz tutaj.

---

**Co jest zrobione (bez GPU):**
- pakiet `src/qwen_compression/`:
  - `data.py`: zbiór pomiarowy;
  - `model_parts.py`: liczenie „od zaburzanej warstwy”;
  - `perturbation.py`: zaburzenia, także wiele naraz w jednym wsadzie;
  - `metrics.py`: KL i zmiana straty;
  - `activations.py`: statystyki neuronów;
  - `importance.py`: przesiew gradientem.

  `data.py` i `model_parts.py` to dwa moduły ponad listę z @phase-pomysl:K15, wydzielone dla porządku;
- **28 testów** (na CPU, na małym losowym Qwen3) potwierdza najważniejsze założenia: start od warstwy daje to samo co pełny przebieg; $\delta=-1$ daje dokładnie to samo co usunięcie neuronu z wag; wsad wielu zaburzeń = osobne pomiary; KL i zmiana straty zgadzają się z liczeniem wprost; **przesiew gradientem trafia w ranking dokładnej KL z korelacją 0,994**;
- **zbiór pomiarowy:** 64 × 2048 tokenów, co czwarta sekwencja to kod (@phase-pomysl:K11 = A). Kod w 7 językach po równo (Python, JavaScript, Java, C++, C, C#, PHP); HTML pominąłem jako język znaczników. Pomiar używa pierwszych 8 sekwencji (16 384 tokenów), a sprawdzenie szumu kolejnych 8;
- skrypt `scripts/phase2_stage1_pilot.py`.

**Co zrobi pilot (kolejno, każdy krok zapisuje wynik):**

| Krok | Co | Czas GPU (szac.) |
|---|---|---|
| precyzja | 64 losowe neurony warstwy 13 w bf16 i w float32, plus pomiar kontrolny „skala 1” (zaburzenie, które nic nie zmienia, więc KL powinna być 0, a każda inna wartość to szum numeryczny) | ~5 min |
| statystyki | średnia, odchylenie, maksimum, odsetek aktywności dla wszystkich 86 016 neuronów | ~1 min |
| dokładnie | warstwy 2, 13, 25 × 3072 neurony × 4 zaburzenia na 16 384 tokenach | ~2,5–3 h |
| szum | 500 losowych neuronów na drugim, rozłącznym zbiorze tokenów | ~10 min |
| przesiew | przybliżenie gradientowe dla wszystkich 28 warstw | ~5 min |

Nowe względem planu: **sprawdzenie precyzji.** Testy pokazały, że KL pojedynczego neuronu może być bardzo mała (w małym modelu rzędu $10^{-9}$), czyli na granicy błędu zaokrągleń. Jeśli w bf16 szum okaże się porównywalny z efektami, etap 2 trzeba będzie liczyć w float32 (wolniej). Pilot to rozstrzygnie.

*2026-10-29 21:49 — Claude Opus 5.5*

---
---
---
