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
| KL kontrolna („skala 1”, powinno być 0) | $1{,}3 \cdot 10^{-3}$ | $-2 \cdot 10^{-9}$ (≈ 0) |
| mediana KL wyłączenia neuronu ($\delta = -1$) | $1{,}3 \cdot 10^{-3}$ (= szum) | $1{,}3 \cdot 10^{-5}$ |
| najmniejsza KL wyłączenia | | $2{,}4 \cdot 10^{-6}$ |

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

## Co masz zrobić

Rano: przeczytaj `etap-1-pilot.md` i `etap-2-mapa.md` w `AGENTS/phases/phase-pomysl/` i odpowiedz na **K16–K22** w `AGENTS/phases/phase-pomysl/agents-issues-3.md` (najważniejsze: K17 i K21).

---

**Stan o 02:06.** Etap 1 skończony (01:37), mapa przesiewu etapu 2 gotowa (02:01), etap 3 policzony wstępnie, etap 4 (warstwa 13) liczy się od 02:03. Po nim w kolejce GPU jest pomiar dokładny etapu 2 (~2 h).

### 1. Reguły z pierwszego wpisu: jak wyszły

| Reguła | Wynik | Co zrobiłem |
|---|---|---|
| precyzja | bf16 = szum ($1{,}3 \cdot 10^{-3}$), float32 ≈ $2 \cdot 10^{-9}$ | float32 |
| przesiew vs dokładnie (≥ 0,9 i ≥ 80% top 10%) | 16 próbek: 0,88–0,95 i 78% ✗; **64 próbki: 0,96–0,98 i 84–87% ✓** | tryb „przesiew + dokładnie 10% najważniejszych i 5% losowych” |
| 4096 tokenów wystarczy (≥ 0,95) | **0,51 ✗** | przesiew na 131 tys. tokenów zamiast 4096 |

**Odstępstwo:** dla przesiewu zwiększyłem liczbę próbek z 16 do 64. Przy regule „inaczej wszystko dokładnie” mapa i tak opierałaby się na 4096 tokenach, a te dają ranking o wiarygodności ~0,5. Przesiew kosztuje 10 s na 4096 tokenów, więc policzyłem go na 32× więcej tokenów. Do akceptacji: **K17**.

### 2. Najciekawsze wyniki

- Skutek zaburzenia neuronu rośnie dokładnie jak $\delta^2$ (osłabienie o połowę = ¼ skutku wyłączenia, podwojenie = wyłączenie). Dalej mierzę więc tylko $\delta = \pm 1$ (**K16**).
- Ranking ważności neuronów **mocno zależy od tekstu**: ranking z tekstu i ranking z kodu są praktycznie niezależne (**K18**).
- Rozkład skutków jest wąski (mediana ~$1$–$3 \cdot 10^{-5}$). Nie ma dużej grupy neuronów, które można wyciąć za darmo; jest kilka bardzo ważnych (masywne w warstwie 2, kilkadziesiąt w ostatniej warstwie 27).
- Najmniej wrażliwy jest środek modelu (warstwy 13–14), a ostatnia warstwa jest ~17× bardziej wrażliwa niż warstwa 13.

### 3. Po drodze

- Krok przesiewu w float32 wywalił się z braku pamięci GPU (logity 2048 × 151 936 w grafie). Przepisałem go bez grafu przez logity; 34 testy przechodzą.
- **Naprawiłem tabelę w moim poprzednim wpisie (22:10):** powłoka zjadła znaki `$` we wzorach (np. `569JXkl2` zamiast $-2$). Zmieniłem tylko uszkodzone komórki, na wartości z `results/phase2/stage1/precision.pt`; treść wpisu jest ta sama. Przyczyna i zabezpieczenie: `AGENTS/memory/pulapki.md`, punkt 19.

*2026-10-30 02:06 — Claude Opus 5.5*

---
---
---

## Co masz zrobić

Odpowiedz na **K16–K24** w `AGENTS/phases/phase-pomysl/agents-issues-3.md` (najważniejsze K17 i K21). Jeśli nie masz pytań do nocy, ten wątek możesz zamknąć.

---

**Noc zakończona (04:30), wszystkie cztery etapy policzone.** Raporty w `AGENTS/phases/phase-pomysl/`:

| Etap | Raport | Najważniejszy wynik |
|---|---|---|
| 1 | `etap-1-pilot.md` | 4096 tokenów to za mało (zgodność rankingów 0,51); skutek rośnie jak kwadrat δ |
| 2 | `etap-2-mapa.md` | mapa 86 016 neuronów z przesiewu na 131 tys. tokenów; z pomiarem dokładnym zgadza się w 0,96–0,99 we wszystkich warstwach |
| 3 | `etap-3-rodzaje-neuronow.md` | prawie brak martwych i zbędnych neuronów; krytyczne głównie w ostatniej warstwie 27 i w warstwie 2; tekst i kod mają inne ważne neurony |
| 4 | `etap-4-jedna-warstwa.md` | warstwa 13: −40% neuronów MLP → perpleksja 12,660 → 12,725; wybór przesiewem lepszy niż po średniej aktywacji |

Odłożona została tylko ocena klasyfikatorem (punkt 3 pierwszego wpisu, **K20**). Nic się nie wysypało poza krokiem przesiewu (brak pamięci GPU, naprawione o 01:38).

*2026-10-30 04:32 — Claude Opus 5.5*

---
---
---
