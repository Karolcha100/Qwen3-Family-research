# Plan: metryki oceny odpowiedzi Qwen3 (poziom 3 — klasyfikatory)

*2026-10-29 15:45 — Claude Opus 5.5*

**Status planu:** do opiniowania

## Co masz zrobić

To lista metryk, którymi będziemy oceniać odpowiedzi skompresowanego Qwen3 na nasze 200 pytań (@phase-0:K27 = C). Napisz w dyskusji, co usunąć, dodać albo zmienić, np. „bez rozwlekłości, dodaj X”. Plan nie dotyczy metod kompresji (wybierzesz je Ty) ani poziomów 1–2 (perplexity, KL, benchmarki); ich podział jest w @T002.

Kilka miejsc zależy od otwartych pytań. Zaznaczyłem je, więc odpowiedzi na K36–K40 (`AGENTS/phases/phase-0/agents-issues-5.md`) mogą zmienić szczegóły.

---

## Skąd metryki

Według Twoich decyzji: **reguły w Pythonie** (@phase-0:K28 = A) + **wieloatrybutowy model nagrody** (@phase-0:K29 = B), bez sędziów generatywnych (@phase-0:K19). Sam model nagrody wybierzemy później (@phase-0:K18). Najbardziej znany kandydat to **ArmoRM** (8B, na Llamie 3). Według jego karty daje 19 ocen z kilku zbiorów danych (np. HelpSteer, UltraFeedback) plus wynik ogólny. Przed wyborem sprawdzę dokładną listę i nowsze modele.

## Proponowane metryki (16)

**A. Reguły w Pythonie — 0/1, bez GPU** (sprawdzają też część `<think>`; @phase-0:K38 = A)

| # | Metryka | Kiedy 1 |
|---|---|---|
| 1 | kompletna | odpowiedź niepusta i niezakończona limitem **8192 tokenów** (@phase-0:K37 = B) |
| 2 | bez pętli | brak powtórzonych fragmentów ponad próg |
| 3 | właściwy język | odpowiedź po angielsku (@phase-0:K21 = A) |
| 4 | czysty tekst | bez tokenów specjalnych, śmieciowych znaków, niezamkniętego `<think>` |
| 5 | wynik zgodny z wzorcem | tylko pytania z jednoznaczną odpowiedzią (@phase-0:K40 = A) |

**B. Atrybuty z modelu nagrody — 0–100** (percentyl względem odpowiedzi BF16; @phase-0:K36)

| # | Atrybut | Co mierzy |
|---|---|---|
| 6 | pomocność | czy odpowiedź rozwiązuje problem pytającego |
| 7 | poprawność | czy fakty i rozumowanie są prawdziwe |
| 8 | spójność | czy tekst jest logiczny i dobrze zbudowany |
| 9 | złożoność | jak zaawansowana jest odpowiedź (informacyjnie, nie „im więcej, tym lepiej”) |
| 10 | rozwlekłość | ile tekstu względem potrzeby (informacyjnie) |
| 11 | wykonanie polecenia | czy trzyma się tego, o co pytano |
| 12 | prawdomówność | brak zmyśleń |
| 13 | uczciwość | czy przyznaje się do niepewności |
| 14 | bezpieczeństwo | czy nie ma szkodliwych treści (zwykle 1; kompresja może to zepsuć) |

**C. Wyniki zbiorcze — 0–100**

| # | Metryka | Jak liczona |
|---|---|---|
| 15 | wynik ogólny | skalar modelu nagrody, percentyl względem BF16 |
| 16 | porównanie z BF16 | $100 \cdot \sigma(r_{\text{po kompresji}} - r_{\text{BF16}})$ dla tego samego pytania; 50 = tak samo dobra (@phase-0:K20 = C, K36 = A) |

**D. Ranking wszystkich wariantów — Elo** (@phase-0:K36, propozycja z @A10)

Nie jest to osobna metryka odpowiedzi, tylko **podsumowanie**. Każdy wariant (BF16, każda metoda × ustawienie) to „gracz”, a „mecz” to odpowiedzi dwóch wariantów na to samo pytanie, z szansą wygranej $\sigma(r_a - r_b)$ z modelu nagrody. Z wszystkich meczów dopasowujemy ranking Bradleya–Terry'ego na skali Elo:

$$P(a \succ b) = \frac{1}{1 + 10^{(R_b - R_a)/400}}, \qquad R_{\text{BF16}} = 1000$$

Słownie: każdy wariant dostaje jedną liczbę $R$, dobraną tak, żeby różnice między wariantami najlepiej przewidywały, który wygrywa w meczach. BF16 ma zawsze 1000. Różnica 100 punktów to ~64% szans na lepszą odpowiedź. Ranking nie wymaga GPU: liczy się z wyników modelu nagrody, które już mamy. Metrykę 16 można przeliczyć na różnicę Elo względem BF16: $\Delta R = 400 \log_{10}\frac{p}{1-p}$.

Metryki 9 i 10 są **informacyjne**: po kompresji ich zmiana w dowolną stronę jest ciekawa, ale nie znaczy „lepiej” ani „gorzej”.

## Jak liczymy wynik wariantu

- każde z 200 pytań dostaje 3 odpowiedzi (@phase-0:K24 = B); metryki uśredniamy najpierw po odpowiedziach, potem po pytaniach;
- reguły → **% odpowiedzi, które przeszły**;
- atrybuty i wyniki zbiorcze → **średnia** 0–100;
- odpowiedzi z regułą 1–4 = 0 (zepsute) zostają w średnich, ale raport pokazuje też wynik bez nich, żeby nie mieszać „model się zepsuł” z „model odpowiada gorzej”.

## Sprawdzenie klasyfikatora

Zanim zaufamy liczbom: oceniasz ręcznie ~50 odpowiedzi w lokalnej stronie HTML (@phase-0:K26 = A), w kilku kluczowych metrykach (np. 6, 7, 16). Liczymy zgodność z modelem nagrody: korelację rang Spearmana

$$\rho = 1 - \frac{6 \sum_i d_i^2}{n(n^2 - 1)}$$

gdzie $d_i$ to różnica pozycji odpowiedzi $i$ w rankingu Twoim i modelu, a $n$ to liczba odpowiedzi. Słownie: $\rho = 1$ znaczy, że model nagrody układa odpowiedzi w tej samej kolejności co Ty, a $\rho \approx 0$, że jego kolejność nie ma związku z Twoją.

## Dyskusja

---
---
---

Zmiany po Twoich decyzjach z 16:21:
- metryka 1: limit 8192 tokenów (@phase-0:K37 = B);
- reguły sprawdzają też `<think>`, a model nagrody widzi tylko odpowiedź końcową (@phase-0:K38 = A);
- metryka 5 potwierdzona (@phase-0:K40 = A);
- bez pytań IFEval w naszych 200 (@phase-0:K39 = A; wyjaśnienie w @T005). Wykonywanie poleceń mierzy IFEval w lm-eval, a metryka 11 zostaje jako miękka ocena;
- skala wyników: propozycja końcowa pod @A10 (A + B + ranking Elo). Jeśli ją przyjmiesz, dopiszę ranking Elo do sekcji C.

Dalej czekam na Twoją opinię o samej liście 16 metryk.

*2026-10-29 16:21 — Claude Opus 5.5*

---
---
---

Skład pytań po Twoich decyzjach z 16:53 (@phase-0:K41 = C, K42 = B):
- 200 pytań = 80 MT-Bench + 60 Arena-Hard + 40 AlpacaEval + 20 własnych;
- MT-Bench z obiema turami: druga tura (z własną pierwszą odpowiedzią modelu w kontekście) dostaje osobną ocenę, czyli 80 ocen więcej. W raporcie będzie osobna kolumna „rozmowa (2. tura)”, żeby było widać, czy kompresja psuje pamięć rozmowy.

Przygotowanie zestawu to moje zadanie @L7. Dalej czekam na Twoją opinię o liście 16 metryk.

*2026-10-29 16:54 — Claude Opus 5.5*

---
---
---

Zmiana po decyzji końcowej @phase-0:K36 (19:32): dodałem sekcję **D. Ranking wszystkich wariantów — Elo** i usunąłem „jeśli” przy percentylach. Lista 16 metryk bez zmian; dalej czekam na Twoją opinię o niej.

*2026-10-29 19:33 — Claude Opus 5.5*

---
---
---

