# T009 · Główny Pomysł

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Generalnie, mój pomysł dzieli się na 3 części.

A. Przeanalizować jak zmiany w (np. [-1, -0.5, 0.5, 1]) wartości na każdym neuronie w modelu Qwen3-0.6B wpływają na sensowność odpowiedzi modelu lub na brak sensowności (różnie mierzonej, generalnie chodzi o to by sprawdzić czy pozbawiają one zdolności Qwena do sensownego użycia, czy nie).
B. Zrobić wykresy ile jest neuronów jakiego rodzaju (jeden neuron może mieć kilka rodzajów, ustalamy jeszcze metrywki w planie) w na przestrzenii każdej z layer (warstwy).
C. Wybrać najbardziej optymalne warstwy do zmniejszenia (np. z 1000 neuronów do 800 neuronów).

Co do punktu C:

Chodzi o to aby przepuścić przez Qwen bardzo dużą liczbę (N_{tokens}) przewidywań (niekoniecznie przewidywania, ale także obliczania etc) tokenów, zliczając jak poprzednia i następna warstwa względem podmienianej, aktywuje się.

Następnie do takich danych, dotrenowywujemy tę zmniejszoną (trenując tylko tą zmniejszoną warstwę, tak aby zgadzał się wynik z następnej warstwy, na podstawie poprzedniej, gdzie zmniejszona jest w środku).

Wkładamy taką wytrenowaną zmniejszoną do modelu w miejsce tej oryginalnej, a następnie dotrenowywujemy cały model - Tak aby jako tako działał.

Zrób proszę z tego raport ze wzorkami matematycznymi i drugi, w którym piszesz co o tym sądzisz.

*2026-10-29 20:35 — Autor*

---
---
---

## Co masz zrobić

Przeczytaj dwa raporty i odpowiedz na pytania:
- **raport 1 (opis matematyczny):** `AGENTS/phases/phase-pomysl/raport-1-opis-matematyczny.md`. Sprawdź, czy dobrze zrozumiałem Twój pomysł;
- **raport 2 (moja opinia):** `AGENTS/phases/phase-pomysl/raport-2-opinia.md`;
- **pytania K1–K9:** `AGENTS/phases/phase-pomysl/agents-issues-1.md`. Najważniejsze jest **K1** (co nazywamy neuronem). Wystarczy „rek” albo litera.

---

**Kontekst.** Opisałeś swój główny pomysł (A: zaburzanie neuronów, B: rodzaje neuronów na wykresach, C: zmniejszenie warstw + trening lokalny + dotrenowanie) i poprosiłeś o raport ze wzorami oraz o opinię.

**Opinia w trzech zdaniach.** Pomysł jest dobry, wykonalny na Twoim sprzęcie i uczy naraz interpretowalności i kompresji. Jest bliski znanym, działającym metodom (ablacja neuronów, kategorie neuronów, przycinanie z destylacją jak w Minitronie), co daje punkt odniesienia. Polecam go robić etapami, z pilotem na 2–3 warstwach, przesiewem gradientowym zamiast liczenia wszystkich 344 tys. zaburzeń (~56 h → minuty + dokładnie dla wybranych), pomiarem szumu i usuwaniem neuronów grupami.

**Zrozumiałem tak** (szczegóły i wzory w raporcie 1):
- **neuron** = jedna z 3072 ścieżek w MLP każdej warstwy (86 016 w modelu); tylko takie da się „wyciąć” z jednej warstwy (K1);
- **zaburzenie** $a \to (1+\delta)\,a$, gdzie $\delta = -1$ wyłącza neuron (K2);
- **skutek** = KL między rozkładami następnego tokenu modelu oryginalnego i zaburzonego (K3);
- **C:** zostawiamy najważniejsze neurony, liczymy nowe $W_{\text{down}}$ metodą najmniejszych kwadratów, trenujemy warstwę lokalnie albo „przez następną warstwę” (K5), wkładamy z powrotem i destylujemy cały model (K8).

Liczby w raportach (czasy, rozmiary) pochodzą z dzisiejszych testów na Twoim GPU (`AGENTS/phases/phase-1/srodowisko.md`).

*2026-10-29 20:48 — Claude Opus 5.5*

---
---
---
