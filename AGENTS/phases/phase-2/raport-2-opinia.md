# Główny pomysł — co o tym sądzę (raport 2 z 2)

*2026-10-29 20:47 — Claude Opus 5.5*

**Status raportu:** zamknięty (2026-11-01 14:28, Claude Opus 5.5 na prośbę autora @T018)
## Co masz zrobić

Przeczytaj i odpowiedz w @T009, jeśli masz uwagi. Decyzje są w `AGENTS/phases/phase-2/agents-issues-1.md` (K1–K9). Formalny opis pomysłu: `AGENTS/phases/phase-2/raport-1-opis-matematyczny.md`.

**Krótko: pomysł jest dobry i wykonalny na Twoim sprzęcie. Polecam go robić, ale etapami i z kilkoma zmianami, które oszczędzą dziesiątki godzin liczenia i pozwolą odróżnić prawdziwe efekty od szumu.** Szacunki czasu opieram na pomiarach z dzisiejszych testów (@L4): Qwen3-0.6B w PyTorchu przetwarza ok. 28 tys. tokenów/s (WikiText-2: 299 tys. tokenów w 10,6 s).

---

## 1. Co jest w nim dobre

- **Uczy dwóch rzeczy naraz:** jak model działa w środku (interpretowalność) i jak go zmniejszyć (kompresja). Część A i B to klasyczne narzędzia interpretowalności, a część C to przycinanie strukturalne z leczeniem.
- **Ma sensowną logikę:** najpierw zmierzyć, co jest ważne (A), zrozumieć (B), a dopiero potem ciąć (C). Wiele metod tnie na ślepo, według samej wielkości wag.
- **Wpisuje się w znane, działające kierunki,** co jest zaletą, bo wiemy, że da się dojść do wyniku:
  - A ≈ *activation patching* / ablacja neuronów, standard w interpretowalności;
  - B ≈ badania typu „Neurons in LLMs: dead, n-gram, positional” (Voita i in., 2023): ich kategorie neuronów są bardzo bliskie Twoim. Do tego „massive activations” (Sun i in., 2024) i „super weights” (Yu i in., 2024): pojedyncze neurony/wagi, których usunięcie niszczy model. **Część A prawie na pewno znajdzie takie neurony w Qwen3**, co samo w sobie będzie ciekawym wynikiem;
  - C ≈ przycinanie szerokości MLP z rekonstrukcją warstwy i destylacją, jak w NVIDIA Minitron (2024), FLAP czy Sheared-LLaMA. Twoja wersja różni się źródłem ważności neuronów (pomiar zaburzeń zamiast prostych statystyk).
- **Porównanie z literaturą daje kontrolę:** jeśli Twoja ważność z A tnie lepiej niż prosta ważność „średnia wielkość aktywacji” (podstawa Minitronu), to jest to prawdziwy wynik.
- **Dobra skala:** 0.6B mieści się w całości na GPU razem z kopią oryginału, więc można liczyć cele w locie (K6) i destylować bez sztuczek.

## 2. Ryzyka i co z nimi zrobić

**(1) Koszt części A przy liczeniu wszystkiego.** $86\,016$ neuronów × 4 zaburzenia ≈ 344 tys. przebiegów:

| Zbiór pomiarowy $T$ | Wszystko dokładnie | Ze startem od zaburzanej warstwy (~½ modelu) |
|---|---|---|
| 4 096 tokenów | ~14 h | ~7 h |
| 16 384 tokenów | ~56 h | ~28 h |

Przesiew gradientem (raport 1, część A) daje przybliżenie dla wszystkich neuronów w **kilka minut**. Proponuję pilot na 2–3 warstwach: dokładnie i przybliżeniem, potem porównanie (K4 = C).

**(2) Pojedynczy neuron zwykle zmienia bardzo mało.** Modele mają dużą nadmiarowość: wyłączenie jednego z 86 tys. neuronów często daje KL rzędu szumu pomiarowego. Bez znajomości szumu część „zbędny vs krytyczny” w B będzie losowa. Rozwiązanie: KL zamiast perplexity (czulsza), wystarczająco duże $T$, a w pilocie powtórka na innym zbiorze tokenów, żeby zmierzyć szum.

**(3) Efekty nie sumują się.** Wyłączenie 600 „zbędnych” neuronów naraz to nie 600 × mały efekt. Neurony mogą się nawzajem zastępować: każdy osobno jest zbędny, a razem już nie. Dlatego w C po wyborze neuronów trzeba **zmierzyć skutek usunięcia całej grupy**, a lepiej usuwać stopniowo (np. po 5%, z pomiarem po każdym kroku).

**(4) „Sensowność” trzeba mierzyć tanio.** Dla 344 tys. zaburzeń nie da się generować odpowiedzi i oceniać ich modelem nagrody (raz: ~5 s, razem: ~20 dni). KL i perplexity wystarczą do A. Pełną ewaluację (poziomy 1–3 z @T002) robimy dla modeli po C.

**(5) Zysk z samego MLP jest umiarkowany.** MLP to 44% parametrów Qwen3-0.6B. Słownik (embedding) to aż 26%, bo przy małym modelu słownik 152 tys. tokenów jest drogi. Zmniejszenie **wszystkich** MLP o 20% daje ok. 9% mniej parametrów. Do nauki to nie przeszkadza, ale żeby model był wyraźnie mniejszy, trzeba ciąć mocniej albo dołożyć głowy atencji (K1 = D).

**(6) Pamięć przy dotrenowaniu całego modelu.** Pełny trening 0.6B z Adamem to ok. 10 GB na wagi i optymalizator, plus nauczyciel 1,2 GB i aktywacje, więc na 12 GB jest ciasno. Stąd propozycja: najpierw trenujemy tylko zmniejszone warstwy, potem ewentualnie LoRA (K8 = D). Destylacja przy ~3× koszcie przebiegu to ok. 9 tys. tokenów/s, czyli ~3 h na 100 mln tokenów.

**(7) Drobne doprecyzowania:** co to neuron (K1), jak zaburzamy (K2), cel treningu warstwy (K5). Zamiast zgadywać, zadałem pytania.

## 3. Proponowane etapy (do Twojej decyzji, K9)

| Etap | Co | Czas GPU (szac.) | Wynik |
|---|---|---|---|
| 1 | **Pilot A** na 2–3 warstwach: dokładnie + przesiew gradientem, pomiar szumu | 1–2 h | czy przybliżenie działa; jaki $T$ wystarczy |
| 2 | **A dla całego modelu** (sposób według pilota) | od minut do ~28 h | $\Delta_{\ell,j,\delta}$ dla 86 016 neuronów |
| 3 | **B: rodzaje neuronów i wykresy** (progi dobrane do rozkładów z etapu 2) | minuty | wykresy warstwa × rodzaj, katalog ciekawych neuronów |
| 4 | **C na jednej warstwie:** wybór neuronów, najmniejsze kwadraty, trening lokalny vs „przez następną” (K5), pomiar KL | ~1 h | czy rekonstrukcja działa |
| 5 | **C na wielu warstwach** + porównanie z ważnością „średnia aktywacja” (punkt odniesienia z literatury) | kilka h | czy Twoja ważność tnie lepiej |
| 6 | **Dotrenowanie i pełna ewaluacja** (poziomy 1–3 z @T002) | kilka h | finalny mniejszy model i jego jakość |

Każdy etap kończy się wynikiem, który sam w sobie jest ciekawy. Po etapie 3 masz już „mapę neuronów Qwen3”, nawet jeśli C pójdzie gorzej.

## 4. Rekomendacja

**Robić.** Kolejność jak w tabeli, z pilotem na początku. Najważniejsze zmiany względem Twojego opisu:
1. **przesiew gradientem + dokładne liczenie tylko dla wybranych** (oszczędza dziesiątki godzin);
2. **pomiar szumu** przed nadawaniem etykiet w B;
3. **usuwanie grupowe/stopniowe** w C zamiast sumowania efektów pojedynczych neuronów;
4. **start warstwy z najmniejszych kwadratów** (sekundy, często prawie gotowy wynik);
5. **porównanie z prostą ważnością z literatury**, żeby wiedzieć, ile wnosi Twoje podejście.

Jak to wpływa na wcześniejsze decyzje: część pytań o ocenę odpowiedzi (@T002, plan metryk) dotyczy dopiero etapu 6. Katalog metod (`AGENTS/phases/phase-0/katalog-metod.md`) staje się materiałem pobocznym: przycinanie strukturalne i SVD-LLM to najbliżsi „konkurenci” Twojego pomysłu, z którymi warto się porównać.

## Dyskusja

---
---
---

🔒 Dyskusja zakończona na prośbę autora (@T018). Podsumowanie wszystkich raportów Phase 2: `AGENTS/phases/phase-2/raport-zbiorczy-phase-2.md`.

*2026-11-01 14:28 — Claude Opus 5.5*

---
---
---
