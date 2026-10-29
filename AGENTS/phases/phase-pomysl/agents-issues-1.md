# Główny pomysł — pytania (runda 1)

*2026-10-29 20:50 — Claude Opus 5.5*

## Co masz zrobić

Decyzje potrzebne, żeby z Twojego pomysłu (@T009) zrobić plan. Opis matematyczny: `AGENTS/phases/phase-pomysl/raport-1-opis-matematyczny.md`, moja opinia: `AGENTS/phases/phase-pomysl/raport-2-opinia.md`. Numery K odpowiadają oznaczeniom **[wybór → K…]** w raporcie 1. Każde pytanie ma rekomendację, więc wystarczy „rek” albo litera. Jeśli wolisz najpierw przeczytać raporty i porozmawiać, napisz w @T009.

---

### K1. 🔴 Co nazywamy neuronem

- **Problem:** od tego zależy cała reszta. Tylko neurony MLP da się „wyciąć” z jednej warstwy (z 3072 do np. 2458).
- **Opcje:**
  - **A** — neuron MLP: jedna z 3072 ścieżek w środku MLP każdej warstwy (86 016 w modelu);
  - **B** — wymiar strumienia rezydualnego (1024, wspólne dla wszystkich warstw, więc nie da się ich zmniejszyć w jednej warstwie);
  - **C** — głowa atencji (16 na warstwę, 448 w modelu);
  - **D** — A + C (najpierw A, potem głowy).
- **Rekomendacja:** A. Pasuje do C („z 1000 do 800”), a MLP to 44% parametrów. Głowy (C) można dodać później.
- **Decyzja:** A

### K2. 🟡 Jak zaburzamy neuron (wartości −1, −0,5, 0,5, 1)

- **Problem:** to samo $\delta$ może znaczyć różne rzeczy. Wzory: raport 1, część A.
- **Opcje:**
  - **A** — mnożąco: $a \to (1+\delta)\,a$. Wtedy −1 wyłącza neuron, −0,5 go osłabia, +0,5 i +1 wzmacniają (×1,5, ×2);
  - **B** — dodając w skali neuronu: $a \to a + \delta\,\sigma$ ($\sigma$ = typowa wielkość aktywacji tego neuronu);
  - **C** — dodając wprost: $a \to a + \delta$ (dla neuronów o różnej skali wynik jest nieporównywalny);
  - **D** — A i B (2× koszt).
- **Rekomendacja:** A. Jest czytelne („wyłącz, osłab, wzmocnij”), a −1 to dokładnie to, co robi przycinanie w części C.
- **Decyzja:** A

### K3. 🟡 Jak mierzymy „sensowność” w części A

- **Problem:** dla 344 tys. zaburzeń nie da się generować i oceniać odpowiedzi klasyfikatorem. Potrzebna jest tania miara.
- **Opcje:**
  - **A** — KL względem oryginału na stałym zbiorze tokenów (+ zmiana straty). Dla ~100 neuronów o największym wpływie dodatkowo generacja i ocena;
  - **B** — tylko zmiana perplexity;
  - **C** — generacja i model nagrody dla każdego zaburzenia (najwierniej, ale miesiące liczenia).
- **Rekomendacja:** A. KL jest najczulsza i liczy się jednym przebiegiem. Generację zostawiamy dla ciekawych przypadków.
- **Decyzja:** ⏳ w toku → @A11 (wstępnie: Rozwiń czym jest KL, poza tym także składaniam się do A - Przy czym, czy nie możemy po prostu użyć szybszego klasyfikatora?)

### K4. 🟡 Jak liczyć część A: wszystko czy z przesiewem

- **Problem:** 86 016 neuronów × 4 zaburzenia. Szacunek czasu: raport 2, punkt 2.
- **Opcje:**
  - **A** — wszystko dokładnie (najpewniej, ale dziesiątki godzin GPU);
  - **B** — przesiew gradientem (wszystkie neurony naraz, minuty), a dokładnie tylko ~10% najważniejszych + losowa próbka do sprawdzenia przybliżenia;
  - **C** — pilot: dokładnie 2–3 warstwy, porównanie z przesiewem, potem decyzja A czy B dla reszty.
- **Rekomendacja:** C. Pilot pokaże, czy przybliżenie gradientowe się sprawdza. Samo porównanie „przybliżenie vs dokładnie” to też ciekawy wynik.
- **Decyzja:** C

### K5. 🟡 Cel treningu zmniejszonej warstwy (C2–C3)

- **Problem:** napisałeś „żeby zgadzał się wynik z następnej warstwy na podstawie poprzedniej”. Można to odczytać na dwa sposoby. Wzory: raport 1, C2.
- **Opcje:**
  - **A** — lokalnie: zmniejszony MLP ma odtworzyć wyjście oryginalnego MLP tej samej warstwy;
  - **B** — przez następną warstwę: wejście z warstwy $\ell-1$, cel na wyjściu zamrożonej warstwy $\ell+1$;
  - **C** — oba i porównanie.
- **Rekomendacja:** C. A jest prostsze i ma dokładne rozwiązanie startowe (najmniejsze kwadraty), a B to Twoja wersja. Porównanie odpowie, czy „przez następną warstwę” daje coś więcej.
- **Decyzja:** wolę B

### K6. 🟢 Dane do treningu warstwy: zapis na dysk czy w locie

- **Problem:** $N_{\text{tokens}}$ par (wejście, cel). Przy 1 mln tokenów to ok. 4 GB na warstwę.
- **Opcje:**
  - **A** — w locie: oryginalny model (1,2 GB) liczy cele na bieżąco, nic nie trafia na dysk;
  - **B** — zapis na dysk (szybsze kolejne eksperymenty na tych samych danych, ale GB na warstwę).
- **Rekomendacja:** A. Model 0.6B jest szybki. Przy 4B/8B wrócimy do tego pytania.
- **Decyzja:** Zapis na dysk, ewentualnie zmniejszymy liczbę N_{tokens}

### K7. 🟢 Start zmniejszonej warstwy

- **Problem:** od czego zaczyna trening zmniejszona warstwa.
- **Opcje:**
  - **A** — wagi zachowanych neuronów + $W_{\text{down}}$ policzone dokładnie metodą najmniejszych kwadratów (sekundy), potem trening;
  - **B** — tylko wagi zachowanych neuronów, potem trening;
  - **C** — losowe wagi (najwolniej, najgorzej).
- **Rekomendacja:** A. Najmniejsze kwadraty często same dają wynik bliski wytrenowanemu, a jeśli nie, trening startuje z dobrego punktu.
- **Decyzja:** A

### K8. 🟡 Dotrenowanie całego modelu (C4)

- **Problem:** pełny trening 0.6B z optymalizatorem Adam to ok. 10 GB samej pamięci na wagi i stany optymalizatora, więc na 12 GB jest ciasno.
- **Opcje:**
  - **A** — wszystkie wagi, z 8-bitowym Adamem i gradient checkpointingiem (mieści się, ale ciasno);
  - **B** — LoRA na całym modelu (mało pamięci, nieco słabiej);
  - **C** — trenujemy tylko zmniejszone warstwy (najtaniej);
  - **D** — C, a jeśli nie wystarczy, B.
- **Rekomendacja:** D. Najpierw sprawdzamy, ile da najtańszy wariant.
- **Decyzja:** D

### K9. 🟡 Plan faz z pomysłu

- **Problem:** w @phase-0:K2 zdecydowałeś, że fazy po Phase 1 rozpiszesz Ty. Mam w raporcie 2 propozycję etapów.
- **Opcje:**
  - **A** — rozpisz fazy według etapów z raportu 2 jako plan do zatwierdzenia;
  - **B** — rozpiszę je sam (napiszę w @T009);
  - **C** — najpierw rozmowa w @T009, potem plan.
- **Rekomendacja:** A, bo plan i tak przechodzi przez Twoje zatwierdzenie i dyskusję.
- **Decyzja:** Podane przez ciebie propozycje etapów Phase 1 są dobre, aczkolwiek chciałbym w phase 1 realizować tylko etapy 1, 2, 3, 4.
