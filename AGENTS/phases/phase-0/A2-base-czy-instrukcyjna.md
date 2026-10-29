# A2 — Qwen3 Base czy wersja instrukcyjna (raport do @phase-0:K7)

*2026-10-29 15:01 — Claude Opus 5.5*

## Co masz zrobić

Przeczytaj raport i wybierz z @phase-0:K7. Wystarczy napisać w raporcie pod @A2 np. „A” (albo zadać pytanie):

- **A** — Base do perplexity, KL i lm-eval; wersja instrukcyjna (z wyłączonym myśleniem) do IFEval, evalplus i sędziego. **Rekomendacja.**
- **B** — wszędzie wersja instrukcyjna (jeden model, ale perplexity mniej porównywalna z literaturą).
- **C** — wszędzie Base (bez evalplus, IFEval i sędziego, bo Base nie wykonuje poleceń).

W skrócie: **Base** to model, który umie tylko dokańczać tekst. **Wersja bez sufiksu** to ten sam model douczony do rozmowy i wykonywania poleceń. Perplexity (czym jest: @A4) i część benchmarków naturalnie liczy się na Base, a wszystko, co wymaga odpowiadania na pytania, potrzebuje wersji instrukcyjnej.

---

## 1. Jak powstaje model: dwa etapy

**Etap 1 — pretrening → model `-Base`.** Model czyta ogromną ilość tekstu (Qwen3: ok. 36 bln tokenów w 119 językach) i uczy się przewidywać następny token. Cel treningu to maksymalizacja prawdopodobieństwa prawdziwego tekstu:

$$\max_\theta \; \sum_{i} \log p_\theta(x_i \mid x_{<i})$$

Słownie: zmieniamy wagi $\theta$ tak, żeby model dawał jak najwyższe prawdopodobieństwo tokenom, które naprawdę występują. **To ta sama wielkość, którą mierzy perplexity**, tylko z odwrotnym znakiem (@A4). Dlatego perplexity jest „naturalną” miarą dla modelu Base.

Efekt: model wie dużo o świecie i języku, ale **tylko dokańcza tekst**. Na pytanie „Jaka jest stolica Francji?” może odpowiedzieć „Paryż”, ale równie dobrze może dopisać kolejne pytanie z quizu.

**Etap 2 — post-trening → model bez sufiksu (np. `Qwen3-0.6B`).** Model Base jest douczany:
- **SFT** (*supervised fine-tuning*): na przykładowych dialogach „pytanie → dobra odpowiedź”. Wzór jest ten sam co wyżej, ale liczony tylko na tokenach odpowiedzi;
- **RL** (uczenie ze wzmocnieniem): model generuje odpowiedzi $y$, a coś je ocenia nagrodą $r(x, y)$, np. **model nagrody** (ten sam rodzaj co w @T002) albo automatyczny sprawdzacz (testy kodu, wynik zadania z matematyki). Wagi zmieniają się tak, żeby rosła średnia nagroda:

$$\max_\theta \; \mathbb{E}_{y \sim \pi_\theta(\cdot \mid x)}\big[r(x, y)\big]$$

Słownie: model uczy się generować odpowiedzi, które oceniający lubi.

W Qwen3 największe modele przeszły kilkuetapowy post-trening (myślenie krok po kroku, RL na rozumowaniu, łączenie trybów), a **małe modele, w tym 0.6B–8B, dostały te umiejętności głównie przez destylację z dużych** (uczeń naśladuje rozkłady nauczyciela). Po tym etapie model:
- rozumie **format czatu** (role `system` / `user` / `assistant`);
- **wykonuje polecenia**;
- ma **tryb myślenia** `<think>…</think>`, który włącza się i wyłącza w szablonie czatu (`enable_thinking=False`).

Nazwy na Hugging Face: `Qwen/Qwen3-0.6B-Base` (Base) i `Qwen/Qwen3-0.6B` (instrukcyjny z trybem myślenia). Tak samo dla 1.7B, 4B i 8B.

## 2. Jak to wpływa na nasze pomiary

| Pomiar | Base | Instrukcyjny | Uwagi |
|---|---|---|---|
| Perplexity (WikiText-2, C4) | naturalna | działa, ale wyższa | post-trening przesuwa model w stronę czatu, więc „zwykły” tekst jest dla niego mniej typowy; porównujemy tylko z jego własnym BF16 |
| KL względem BF16 | tak | tak | zawsze porównujemy z tym samym modelem przed kompresją |
| lm-eval: ARC, HellaSwag, PIQA | tak (standard w artykułach) | tak | zadania wyboru odpowiedzi działają na obu |
| IFEval, evalplus, sędzia | **nie** | tak | Base nie wykonuje poleceń, więc wyniki byłyby bez sensu |

## 3. Dlaczego warto mieć oba (opcja A)

- **Porównywalność:** artykuły o kompresji podają perplexity i lm-eval głównie dla modeli Base, więc tak możemy sprawdzić, czy nasze wyniki są rozsądne.
- **Realne użycie:** ludzie korzystają z wersji instrukcyjnej, więc to ją trzeba ocenić IFEval, evalplus i sędzią.
- **Ciekawe pytanie badawcze:** czy kompresja psuje bardziej „wiedzę” (widoczną w Base), czy „zachowania” z post-treningu (wykonywanie poleceń, myślenie)? Ta sama metoda na obu wersjach daje odpowiedź za darmo.
- **Koszt:** dwa modele na każdy rozmiar to 2× pobieranie i liczenie. Przy 0.6B i 1.7B to minuty. Przy 8B to już godziny, więc tam można ograniczyć się do jednej wersji (o tym zdecydujemy, gdy dojdziemy do 8B).

Z wyborem wiąże się też format danych kalibracyjnych dla wersji instrukcyjnej (@A3, punkt 3e; pytanie @phase-0:K32).
