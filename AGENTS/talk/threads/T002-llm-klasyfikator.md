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
