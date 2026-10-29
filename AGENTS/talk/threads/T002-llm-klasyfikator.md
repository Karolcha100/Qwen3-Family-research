# T002 · LLM klasyfikator

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Hej zastanawiam się czy jest jakiś open source (podobnie jak ten Qwen3) klasyfikator oparty o architekture LMM, który moglibyśmy puścić lokalnie.

To znaczy, chcę go używać nie do badań, a do klasyfikacji odpowiedzi z Qwen3 (czy Qwen3 dobrze/źle działa).

Co o tym sądzisz?

*2026-10-29 13:04 — Autor*

---
---
---

## Co masz zrobić

Pytałeś o opinię, więc niczego nie uruchamiam. Decyzja jest w @phase-0:K13 (rekomendacja: jeszcze nie; najpierw metryki automatyczne, potem porównanie dwóch sędziów z Twoimi ręcznymi ocenami). Wystarczy wpisać „rek” albo literę.

**Krótko: tak, takie modele istnieją i da się je uruchomić lokalnie na 12 GB.** Nazywa się to *LLM-as-a-judge* (model ocenia tekst) albo *reward model* (LLM z głową, która zwraca jedną liczbę). Są dwa typy:

1. **Sędzia generatywny** — dostaje pytanie, odpowiedź i rubrykę, a zwraca ocenę z uzasadnieniem. Przykład: **Prometheus 2** (7B, oparty na Mistralu), uczony specjalnie do oceniania według rubryki; jest też wariant z odpowiedzią wzorcową. W GGUF Q8 przez llama.cpp zajmuje ~8 GB.
2. **Model nagrody (klasyfikator)** — zwraca liczbę „jak dobra jest odpowiedź”. Przykład: **Skywork-Reward-V2**, w wariantach od 0.6B do 8B (na bazie Qwen3 i Llamy). Jest szybki i ma czysty sygnał, ale nie mówi, *dlaczego* odpowiedź jest zła.

Są też klasyfikatory bezpieczeństwa (Llama Guard, Qwen3Guard), ale oceniają szkodliwość, a nie poprawność, więc tu się nie przydadzą.

Ta lista pochodzi z mojej wiedzy. Przed wyborem sprawdzę aktualny ranking (RewardBench, JudgeBench), bo ta dziedzina szybko się zmienia.

**Plusy:**
- ocenia rzeczy, których perplexity nie widzi: spójność, sens, trzymanie się pytania, bełkot po agresywnej kwantyzacji;
- dobrze pasuje do porównania parami „odpowiedź BF16 vs odpowiedź po kompresji: czy jest gorsza?”; to stabilniejsze niż ocena bezwzględna;
- działa lokalnie i za darmo; przy 0.6B–4B oceny i tak generujemy wsadowo.

**Minusy:**
- **sędzia też się myli**, a jego błąd jest systematyczny (lubi długie odpowiedzi, pewny ton, pierwszą odpowiedź z pary). Bez sprawdzenia na Twoich ocenach nie wiadomo, ile wart jest jego wynik;
- **bias rodziny:** sędzia z rodziny Qwen może faworyzować odpowiedzi Qwen. Lepiej wybrać inną rodzinę (Prometheus/Mistral, Skywork na Llamie);
- **VRAM:** sędzia i oceniany model nie zmieszczą się razem w 12 GB przy 4B i 8B. Trzeba działać w dwóch krokach: najpierw generujemy odpowiedzi do pliku, potem je oceniamy;
- tam, gdzie jest twarda odpowiedź (matematyka, kod, wybór ABCD), lepsze są metryki deterministyczne: exact match w lm-eval, testy jednostkowe w evalplus i KL względem BF16. Są tańsze i nie mają biasu.

**Rekomendacja:** sędzia jako uzupełnienie, nie główna metryka. Kolejność:
1. najpierw KL, lm-eval i evalplus (Phase 2);
2. potem zestaw ~50 pytań otwartych; odpowiedzi BF16 i po kompresji oceniasz ręcznie, a równolegle oceniają je 2 kandydaci (np. Prometheus 2 i Skywork-Reward-V2 na Llamie);
3. zostaje ten sędzia, który najbardziej zgadza się z Tobą, i używamy go do porównań parami.

*2026-10-29 13:05 — Claude Opus 5.5*

---
---
---

To znaczy, w mojej opinii KL, Lm-eval, evalplus są spoko, ale obok tego chcę "Model Nagrody" czyli ten klasyfikator. 

Trzeba wypracować na nim zbiór metryk pod względem których ma oceniać wypowiedzi modelu z rodziny Qwen3.

Zgadzam się z zestawem 50 pytań, na które odpowiada każdy zmodyfikowany Qwen i które to jego odpowiedzi są następnie oceniane w np. 16 metrykach (typu od 0 do 100, oraz typu boolowskiego że 0 lub 1) przez któryś klasyfikator.

Co o tym sądzisz?

*2026-10-29 13:21 — Autor*

---
---
---

## Co masz zrobić

Pytałeś o opinię, więc niczego nie uruchamiam. Decyzje rozbiłem na pytania @phase-0:K18–K27 w `AGENTS/phases/phase-0/agents-issues-2.md`. Wystarczy wpisać „rek” albo literę. Otwarte jest też @phase-0:K13 („czy i kiedy sędzia”); po Twojej odpowiedzi tutaj możesz tam wpisać np. „sędzia: tak, według K18–K27”.

**Krótko:** pomysł jest dobry. Jest jeden haczyk: **model nagrody w ścisłym sensie zwraca jedną liczbę**, a nie 16. Dlatego proponuję hybrydę (@phase-0:K18, opcja C):

| Rodzaj metryki | Narzędzie | Koszt |
|---|---|---|
| 0/1 sprawdzalne regułą | Python (regex, wykrywanie języka, uruchomienie kodu) | ~0 |
| ogólna jakość 0–100 | skalarny model nagrody (np. Skywork-Reward-V2) albo wieloatrybutowy (np. ArmoRM) | sekundy |
| 0/1 i 0–100 wymagające rozumienia | sędzia generatywny z rubryką (np. Prometheus 2) | minuty–godzina na wariant |

**Szkic 16 metryk** (do dopracowania w @phase-0:K27):

0/1 według reguł:
1. **Kompletna** — niepusta i nie urwana na limicie tokenów;
2. **Bez pętli** — brak powtórzeń n-gramów ponad próg (typowy objaw agresywnej kwantyzacji);
3. **Właściwy język** — w języku pytania;
4. **Format zgodny z instrukcją** — pytania w stylu IFEval („3 punkty”, „JSON”, „poniżej 50 słów”);
5. **Kod działa** — dla pytań o kod: kompiluje się i przechodzi test;
6. **Czysty tekst** — bez wycieku `<think>`, tokenów specjalnych i śmieciowych znaków.

0/1 od sędziego:

7. **Na temat** — odpowiada na zadane pytanie;
8. **Poprawny wynik końcowy** — dla pytań z odpowiedzią wzorcową.

0–100 od modelu nagrody:

9. **Ogólna jakość** — skalar z modelu nagrody, znormalizowany do 0–100 (np. percentyl względem odpowiedzi BF16).

0–100 od sędziego (rubryka 1–10 → 0–100):

10. **Poprawność merytoryczna**;
11. **Brak halucynacji** — zmyślone fakty, nazwy, liczby;
12. **Spójność i logika** — czy wywód się trzyma;
13. **Pomocność** — czy rozwiązuje problem pytającego;
14. **Płynność językowa** — gramatyka, naturalność (ważne dla pytań po polsku);
15. **Zwięzłość** — bez lania wody i niepotrzebnych powtórzeń.

Porównanie z BF16:

16. **Nie gorsza niż BF16** — porównanie parami (win/tie/loss → 0–100), ocenione w obu kolejnościach.

**Na co uważać:**
- **skala 0–100:** sędziowie słabo rozróżniają 100 poziomów, więc lepiej rubryka 1–10 i średnia ważona prawdopodobieństwami (@phase-0:K19);
- **szum:** 50 pytań wystarczy, żeby wybrać i skalibrować sędziego, ale do porównywania metod kompresji lepiej ~150–200 (@phase-0:K23);
- **koszt:** sędzia generatywny 7–8B na RTX 4070S to rząd ~50 tokenów/s na jedno zapytanie; równoległe sloty w llama.cpp mocno to przyspieszają. Przy 50 pytaniach × 8 metrykach × każdy wariant warto mieć ocenę wszystkich metryk w jednym wywołaniu albo cache;
- **VRAM:** najpierw generujemy odpowiedzi wszystkich wariantów do pliku, potem w osobnym kroku ładujemy sędziów. Na 12 GB nie zmieszczą się jednocześnie Qwen3-4B/8B i sędzia 8B;
- **bias rodziny:** jako sędziów lepiej wziąć modele spoza rodziny Qwen (Skywork na Llamie, ArmoRM na Llamie, Prometheus na Mistralu).

Nazwy modeli są z mojej wiedzy. Przed wyborem sprawdzę aktualne rankingi (RewardBench 2, JudgeBench), czy nie ma czegoś nowszego.

*2026-10-29 13:30 — Claude Opus 5.5*

---
---
---

Dobra, czyli byśmy robili to co tutaj proponujesz, oraz te KL, Lm-eval, evalplus? - Czy w takim wypadku potrzebna jest metryka "0/1 sprawdzalne regułą" ? Dodatkowo metryki 0-100 czy 0-10, mogą być wypełniane klasyfikatorem na zasadzie że kilka razy używamy jednego modelu nagrody aby uzyskać te kilka metryk.

*2026-10-29 14:07 — Autor*

---
---
---

## Co masz zrobić

Dwie nowe decyzje wynikające z Twoich pytań: @phase-0:K28 (które metryki regułowe zostają) i @phase-0:K29 (czy sprawdzamy na danych, czy jeden model nagrody uruchamiany kilka razy daje osobne metryki). Wystarczy wpisać „rek”. Poprzednie pytania o sędziego (K18–K27) są nadal aktualne.

**1. Tak: robimy wszystko razem, warstwami** (od najtańszej):

| Warstwa | Co | Na czym | Kiedy |
|---|---|---|---|
| 1 | perplexity, KL względem BF16 | WikiText-2, C4 | każdy wariant, minuty |
| 2 | lm-eval (ARC, HellaSwag, PIQA… + IFEval), evalplus | gotowe zestawy z odpowiedziami | warianty, które przeszły warstwę 1 |
| 3 | sędzia (reguły + model nagrody + ewentualnie sędzia z rubryką) | nasze ~50 pytań otwartych | najciekawsze warianty |

**2. Czy metryki „0/1 sprawdzalne regułą” są potrzebne, skoro jest lm-eval i evalplus?** Część nie:
- **#4 Format zgodny z instrukcją** dubluje IFEval, który jest w lm-eval jako gotowe zadanie (~500 poleceń sprawdzanych regułą) → **usuwamy**;
- **#5 Kod działa** dubluje evalplus → **usuwamy**.

Cztery zostają: **#1 kompletna, #2 bez pętli, #3 właściwy język, #6 czysty tekst**. Nie mierzą „jak dobra jest odpowiedź”, tylko wyłapują **typowe awarie po kompresji** (pętle, bełkot, urwany tekst, przełączenie na chiński). Benchmarki tego nie raportują: zepsuta odpowiedź po prostu dostaje 0, a nie dowiadujemy się dlaczego. Są też **bramką dla sędziego**: model nagrody potrafi dać zapętlonej odpowiedzi zaskakująco wysoki wynik, więc taką odpowiedź oznaczamy przed oceną. Koszt to kilkadziesiąt linii Pythona, bez GPU. Decyzja: @phase-0:K28.

**3. Jeden model nagrody uruchomiony kilka razy, po razie na metrykę?** Da się to zrobić technicznie: w treści przed odpowiedzią dopisujemy kryterium („oceń tylko poprawność merytoryczną”) i odpalamy model po razie na metrykę. Haczyk: **zwykły skalarny model nagrody był uczony na ogólnych preferencjach („która odpowiedź lepsza”) i zwykle ignoruje takie polecenie.** Wtedy „poprawność”, „spójność” i „pomocność” wyjdą prawie tymi samymi liczbami, a my będziemy mieli 8 kopii jednej metryki pod różnymi nazwami.

Są trzy sposoby, żeby to zadziałało:
- **model wieloatrybutowy** (np. ArmoRM): w jednym przebiegu zwraca kilkanaście osobnych ocen (pomocność, poprawność, spójność, złożoność, rozwlekłość…). To najbliżej Twojego pomysłu i jest najtańsze;
- **modele nagrody uczone pod kryterium/zasadę** (tzw. principle-following reward models): przyjmują kryterium jako wejście i są pod to trenowane. To nowszy kierunek; sprawdzę, co jest dostępne w rozmiarze do ~8B;
- **sędzia generatywny z rubryką:** na pewno rozróżnia kryteria, ale jest najwolniejszy.

**Rekomendacja:** zamiast zakładać, sprawdźmy to na danych. Na ~50 odpowiedziach puszczamy skalarny model nagrody z 6 różnymi kryteriami i liczymy korelacje między „metrykami”. Jeśli wychodzą bliskie 1, model ignoruje kryterium i bierzemy model wieloatrybutowy albo z rubryką. Jeśli są wyraźnie różne, Twój pomysł działa i jest najtańszy. To ~10 minut GPU na Qwen3-0.6B. Decyzja: @phase-0:K29.

*2026-10-29 14:09 — Claude Opus 5.5*

---
---
---
