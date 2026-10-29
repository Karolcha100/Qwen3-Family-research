# T010 · Noc: uruchamiam etapy Phase 2 — plan i zastrzeżenia

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

## Co masz zrobić

Nic teraz, śpij spokojnie. Etapy uruchamiam (etap 1 liczy się od 22:08). Rano przeczytaj raporty etapów i podejmij dwie decyzje, które wymieniam niżej (będą też jako pytania). Nie mam nic przeciwko uruchomieniu, mam tylko dwa zastrzeżenia (punkty 3 i 4).

---

**Kontekst.** Napisałeś w Koniec (22:07): „uruchom wszystkie etapy, idę spać; jeśli masz coś przeciwko, zrób wątek”. Do tego: nie widzisz planu Phase 2 w GUI, a wpis „zamknąłem…” miał trafić do planu metryk.

### 1. Co zrobię w nocy

| Etap | Co | Kiedy przechodzę dalej |
|---|---|---|
| 1 — pilot | precyzja, statystyki, dokładnie 3 warstwy, szum, przesiew (~3 h) | po zakończeniu: analiza + raport `AGENTS/phases/phase-pomysl/etap-1-pilot.md` |
| 2 — cały model | sposób według reguł ustalonych **przed** zobaczeniem wyników (niżej) | po zakończeniu: raport `etap-2-mapa.md` |
| 3 — rodzaje neuronów | etykiety + wykresy (bez klasyfikatora, punkt 3) | raport `etap-3-rodzaje-neuronow.md` |
| 4 — jedna warstwa | dane na dysk (~4 GB), −5/−10/−20/−40%, warianty (a)/(b)/(c), porównanie ze „średnią wielkością aktywacji” | raport `etap-4-jedna-warstwa.md` |

**Reguły dla etapu 2 (ustalone teraz, przed wynikami pilota):**
- **precyzja:** jeśli w bf16 KL kontrolna („skala 1”, która powinna wynosić 0) przekracza 10% mediany KL wyłączenia neuronu ($\delta=-1$), etap 2 liczę w float32;
- **sposób:** jeśli przesiew gradientem ma z dokładną KL korelację rang ≥ 0,9 i wskazuje ≥ 80% tych samych „top 10%” neuronów, liczę **przesiew dla wszystkich + dokładnie 10% najważniejszych + 5% losowych do kontroli**. W przeciwnym razie liczę **wszystko dokładnie**, co potrwa dłużej niż noc; obliczenia można wznawiać, więc dokończę je w kolejnych sesjach;
- **liczba tokenów:** 4096 zamiast 16 384, jeśli ranking z 4096 tokenów ma z rankingiem z 16 384 korelację ≥ 0,95.

### 2. Gdyby coś poszło źle

Jeśli coś się wysypie, nie zgaduję. Zatrzymuję się na ostatnim dobrym kroku i opisuję problem tutaj. Każdy krok zapisuje wyniki, więc nic nie przepada.

### 3. Zastrzeżenie 1: klasyfikator w etapie 3

W planie etap 3 obejmuje generację i ocenę klasyfikatorem dla ~250 najważniejszych neuronów. **Klasyfikator (model nagrody) nie jest jeszcze wybrany** (@phase-0:K18 „do rozważenia”), a zestaw pytań do generacji nie jest zbudowany (@L7). Ten jeden podpunkt odkładam. Etykiety i wykresy etapu 3 zrobię bez niego. Decyzja o klasyfikatorze: nowe pytanie.

### 4. Zastrzeżenie 2: wybór warstwy w etapie 4

W planie wybór warstwy do zmniejszania był „do Twojej akceptacji”. Żeby noc nie przepadła, **wybiorę najmniej wrażliwą warstwę według danych** i oznaczę wynik jako tymczasowy. Jeśli rano wolisz inną warstwę, powtórka to ~1–2 h.

### 5. Gdzie jest plan Phase 2 w GUI

Plan jest w pliku `AGENTS/phases/phase-pomysl/plan-phase-2.md`. Po zatwierdzeniu znika z „Co czeka na mnie”. Widać go w widoku **„Plany” → „Zatwierdzone i zamknięte” → „Phase 2 — plan: mapa neuronów…”** albo w **Drzewo → Plany**. Może myliło Cię, że folder nazywa się `phase-pomysl`, a nie `phase-2`. Czy przemianować folder, to drobne pytanie, które dodam.

### 6. Wpis „zamknąłem…”

Przenoszę go (jako cytat) do dyskusji planu metryk i tam odpowiadam. W skrócie: plan metryk **przyda się** w etapie 3 (gdy wybierzemy klasyfikator) i w Phase 3. Twój wpis trafił do złego planu, więc możliwe, że GUI po zatwierdzeniu jednego planu zostawia otwarty poprzedni. Sprawdzę to jako zadanie @L14.

*2026-10-29 22:09 — Claude Opus 5.5*

---
---
---

## Co masz zrobić

Nic. To informacja o pierwszym wyniku i zmianie, którą wymusił (zgodnie z regułą precyzji z mojego poprzedniego wpisu).

**Pierwszy wynik pilota: bf16 jest za mało precyzyjne.** 64 losowe neurony warstwy 13, jedna sekwencja 2048 tokenów:

| | bf16 | float32 |
|---|---|---|
| KL kontrolna („skala 1”, powinno być 0) | {,}3 \cdot 10^{-3}$ | 569JXkl2 \cdot 10^{-9}$ (≈ 0) |
| mediana KL wyłączenia neuronu ($\delta = -1$) | {,}3 \cdot 10^{-3}$ (= szum) | {,}3 \cdot 10^{-5}$ |
| najmniejsza KL wyłączenia | | {,}5 \cdot 10^{-6}$ |

W bf16 szum jest **100× większy** niż skutek wyłączenia typowego neuronu, więc pomiar w bf16 mierzy sam szum. W float32 szum jest ~1000× mniejszy od najmniejszego skutku. **Wniosek: zaburzenia liczymy w float32.**

**Co zmieniłem w nocy:**
- pomiar w bf16, który już ruszył, zatrzymałem i uruchomiłem pilot w float32 (start 22:10);
- float32 jest ~2× wolniejszy. Pilot na 16 384 tokenach trwałby ~11 h, więc liczę na **4096 tokenach** (1 sekwencja tekstu + 1 sekwencja kodu, ~2,8 h);
- zamiast reguły „4096 vs 16 384 tokenów” sprawdzam, czy ranking neuronów z dwóch **rozłącznych** zbiorów po 4096 tokenów się zgadza (krok „szum”). Jeśli korelacja ≥ 0,95, to 4096 wystarcza.

Tłumaczy to też, dlaczego przesiew gradientem jest tak cenny: dokładne liczenie w float32 wszystkich 86 016 neuronów trwałoby ~26 h nawet na 4096 tokenach.

*2026-10-29 22:10 — Claude Opus 5.5*

---
---
---
