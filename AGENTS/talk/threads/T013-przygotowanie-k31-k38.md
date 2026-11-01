# T013 · Przygotowanie obliczeń z decyzji K31–K38

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

## Co masz zrobić

Odpowiedz na **K39** w `AGENTS/phases/phase-2/agents-issues-7.md`: czy uruchomić kolejkę obliczeń (wystarczy „A”). Poniżej jest to, co przygotowałem i sprawdziłem bez GPU. Jeśli coś jest nie tak, jak chciałeś, napisz tutaj.

### K31: punkt startu

Cztery starty dla warstwy 13 przy 40%, każdy z długim treningiem (16 epok, krok $5 \cdot 10^{-5}$, jak w @phase-2:K23):
- **mapa:** jak dotąd (mapa kodu 75/25);
- **średnia aktywacja:** średnia kwadratowa aktywacji neuronu na danych treningowych (75% Python). Biorę ją zamiast średniej |a| ze starego zbioru tekstowego, żeby oba starty widziały te same dane. Uwaga: to trochę inna miara niż „średnia |a|” z treści K31;
- **losowy:** losowe neurony oryginału (stałe ziarno);
- **połączone neurony:** opis niżej.

**Ważne przy łączeniu neuronów.** Najpierw sprawdziłem (na CPU), czy wyrzucane neurony mają „bliźniaków” wśród zostających, czyli czy ich aktywacje są podobne. Prawie nigdy nie mają:

| Zmniejszenie | największe podobieństwo aktywacji wyrzucanego neuronu do zostającego (mediana) | odsetek z podobieństwem > 0,5 |
|---|---|---|
| 20% | 0,13 | 0,3% |
| 40% | 0,13 | 0,1% |

(podobieństwo = cosinus między aktywacjami dwóch neuronów na 1 mln tokenów; 1 = identyczne, 0 = niezależne)

Słownie: każdy neuron robi coś innego niż pozostałe, więc łączenie „w pary po aktywacjach” nie ma czego łączyć. Dlatego łączenie robię znaną metodą składania wag (*model folding*): neurony grupuję metodą k-średnich według ich wag wejściowych ($W_{gate}$, $W_{up}$), na start środkami grup są neurony najważniejsze według mapy, a każda grupa staje się jednym neuronem (średnia wag wejściowych, suma kolumn $W_{down}$). Potem jak zwykle: nowe $W_{down}$ z najmniejszych kwadratów i trening. Na warstwie 13 przy 40% wychodzi: 1689 z 1843 ważnych neuronów zostaje bez zmian, a 1229 neuronów, które przy zwykłym starcie byłyby wyrzucone, łączy się z pozostałymi ~150 ważnymi w ~150 grup, w tym kilka dużych (do 247 neuronów). Moje przypuszczenie: przy tak niezależnych neuronach łączenie da niewiele ponad sam start z mapy, ale to właśnie sprawdzi K31.

### K37: trening z celem na wyjściu modelu

Zmniejszona warstwa uczy się tak, żeby rozkład następnego tokenu całego modelu był jak najbliżej oryginału:

$$
\mathcal{L} = \frac{1}{T} \sum_{t=1}^{T} \mathrm{KL}\big(p_{\text{oryginał}}(\cdot \mid x_{<t}) \,\big\Vert\, p_{\text{zmniejszony}}(\cdot \mid x_{<t})\big)
$$

Słownie: dla każdego z $T$ tokenów porównujemy, z jakim prawdopodobieństwem oryginał i model ze zmniejszoną warstwą przewidują każdy możliwy następny token, i uśredniamy rozbieżność. Uczy się tylko zmniejszona warstwa; reszta modelu jest zamrożona. KL liczę w kawałkach po 256 pozycji, żeby nie trzymać w pamięci naraz macierzy 2048 × 151 936. Test sprawdza, że wartość i gradient są identyczne jak przy liczeniu wprost; na CPU sprawdziłem też jeden krok na prawdziwym modelu.

### K38: mapa 100% kod

Mapa z samego kodu jest już policzona (z tego samego przesiewu co 75/25); warstwa 13, 20% i 40%, 6 epok, żeby porównać wprost z wynikami z raportu `AGENTS/phases/phase-2/etap-4b-kod.md`.

### K32, K34, K35, K36: testy kodu

- **Kontener** `qwen-code-sandbox` (podman): `python:3.12-slim` + EvalPlus 0.3.1 z zadaniami pobranymi przy budowie (obraz 891 MB, bo EvalPlus ciągnie sporo bibliotek). Uruchamiany bez sieci, z systemem plików tylko do odczytu, z limitami pamięci (8 GB), procesora (8 rdzeni) i liczby procesów; zapisywać może tylko do folderu z wynikami. Plik: `sandbox/Containerfile`.
- **Generowanie** (GPU, poza kontenerem): tak samo jak EvalPlus dla modeli bazowych: polecenie = treść zadania, model dopisuje kod, dekodowanie zachłanne, do 768 tokenów, te same teksty kończące. Różnica: generuję po 16 zadań naraz (EvalPlus po jednym), co może minimalnie zmienić pojedyncze wyniki.
- **Sprawdzenie bez modelu:** rozwiązania wzorcowe z samego zestawu (napisane przez autorów zestawu, nie przez model) przechodzą: HumanEval 163/164, MBPP 99,7% (testy podstawowe) i 99,5% (z dodatkowymi). Jedyny błąd w HumanEval (zadanie 32) to znana cecha zestawu: wzorcowe rozwiązanie liczy z mniejszą dokładnością, niż wymaga test.
- **Analiza statyczna** (bez uruchamiania): ruff (błędy nazw, składni, typowe pomyłki), pyright (błędy typów), radon (złożoność), długość. Dla rozwiązań wzorcowych średnio: HumanEval 0,03 uwagi ruff, 0,03 błędu pyright, złożoność 3,1, 16 linii; MBPP 0,09 / 0,01 / 2,2 / 4 linie. To punkt odniesienia dla modelu.
- **Sprawność modelu:** liczba parametrów, szczytowa pamięć GPU i tokeny/s przy generowaniu.

Kod: `scripts/phase2_stage4_one_layer.py` (nowe starty, `--objective output`, `--save-mlps`), `src/qwen_compression/reconstruction.py` (łączenie), `src/qwen_compression/training.py` (cel na wyjściu), `scripts/phase2_code_generate.py`, `scripts/phase2_code_evaluate.py`, kolejka `results/phase2/code/queue.sh`.

*2026-10-30 14:13 — Claude Opus 5.5*

---
---
---

Napisz mi tutaj przewidywany czas obliczeń tych rzeczy

*2026-10-30 14:20 — Autor*

---
---
---

## Co masz zrobić

Jeśli czasy Ci pasują, odpowiedz „A” w **K39** (`AGENTS/phases/phase-2/agents-issues-7.md`). Postęp na żywo zobaczysz na pasku w GUI (@T014).

### Przewidywany czas obliczeń

Razem **ok. 2 h 50 min** (moim zdaniem realnie 2,5–3,5 h). Szacunki opierają się na czasach dzisiejszych przebiegów na tej karcie: ocena modelu po podmianie warstwy ~55 s, epoka treningu „za następną warstwą” ~14 s, pełne przejście modelu ~0,25 s na sekwencję 2048 tokenów.

| Krok | Szacunek | Na czym opieram szacunek | Pewność |
|---|---|---|---|
| oryginał: HumanEval i MBPP (generowanie + testy w kontenerze) | 13 min | ~25 ms na token, po 16 zadań naraz; testy rozwiązań wzorcowych trwały 30–50 s | średnia (zależy od tego, jak długie odpowiedzi pisze model) |
| K38: mapa 100% kod, warstwa 13, 20% i 40% | 10 min | 2 × (3 oceny po ~55 s + 6 epok po ~14 s) | duża |
| K31: 4 punkty startu, 40%, po 16 epok | 28 min | 4 × (3 oceny + 16 epok po ~14 s), plus ~1 min na łączenie neuronów | duża |
| K37: cel na wyjściu modelu, warstwa 13, 40% i 20% | 76 min | każda sekwencja przechodzi przez 15 warstw i warstwę wyjściową w przód i wstecz, ~0,7 s; 480 sekwencji × 6 epok × 2 stopnie | **mała**: nie mierzyłem tego na GPU, może wyjść 45–120 min |
| K37: warstwa 26, 40% | 14 min | tylko 2 warstwy za zmniejszaną, większość czasu to warstwa wyjściowa | mała |
| HumanEval i MBPP dla dwóch wersji warstwy 13 (−40%) | 26 min | jak dla oryginału, 2 razy | średnia |

Pasek w GUI na bieżąco poprawia czas „do końca”: bierze pod uwagę, o ile szybciej lub wolniej szły już skończone kroki i jaką część bieżącego kroku zgłosił skrypt. Po pierwszych epokach K37 zobaczysz więc dokładniejszy czas.

Zmiana techniczna: kolejka jest teraz w pliku `results/phase2/code/queue.json` (te same kroki co w `queue.sh` z treści K39, plus szacowany czas każdego kroku) i uruchamia ją `scripts/run_queue.py`, który zapisuje postęp dla paska.

*2026-10-30 14:26 — Claude Opus 5.5*

---
---
---

## Co masz zrobić

Nic. Kolejka liczy się od 14:31 (@phase-2:K39 = A), postęp widać na pasku w GUI. Wyniki opiszę w raporcie, gdy wszystko się skończy.

### Pierwszy wynik: oryginał odtwarza liczbę z raportu Qwen3

| Zestaw | pass@1 (oryginał, u nas) |
|---|---|
| HumanEval | 29,9% (49 z 164) |
| HumanEval+ | 23,2% |
| MBPP (EvalPlus) | 51,6% |
| MBPP+ | 42,9% |
| **średnia (EvalPlus)** | **36,9** (raport Qwen3: **36,23**) |

Różnica 0,6 punktu mieści się w niepewności (przy 164 zadaniach HumanEval to ±3,7 punktu), więc sposób zadawania pytań i ocena działają jak u Qwen. Przejrzałem kilka nieudanych rozwiązań: to prawdziwe błędy modelu (np. zła logika), a nie ucięty kod.

Sprawność oryginału przy generowaniu (po 16 zadań naraz, bf16): 124–134 tokeny/s, szczytowo 3,4 GB pamięci GPU, 596 mln parametrów. Generowanie zajęło 2 min 20 s (HumanEval) i 3 min 30 s (MBPP), testy w kontenerze 30 s i 50 s, czyli tyle, ile szacowałem.

*2026-10-30 14:38 — Claude Opus 5.5*

---
---
---

Dobra, jak to wygląda względem oryginalnego Qwen3? - Zrób porównanie i uwzględnij dodatkową kolejkę do 17:30

*2026-10-30 18:02 — Autor*

---
---
---

## Co masz zrobić

Przeczytaj raport `AGENTS/phases/phase-2/porownanie-z-oryginalem.md`. Jest w nim pełne porównanie z oryginałem, razem z dodatkową kolejką do 17:13. Tę samą prośbę napisałeś też w @T016, więc obie dostały jeden raport.

### W skrócie (liczba rozwiązanych zadań)

| Model | HumanEval (z 164) | HumanEval+ | MBPP (z 378) | MBPP+ |
|---|---|---|---|---|
| **oryginał** | **49** | **38** | **195** | **162** |
| w. 13 −40%, cel za warstwą | 44 | 34 | 186 | 152 |
| w. 13 −40%, cel na wyjściu | 45 | 34 | 182 | 150 |
| w. 13 −40%, mapa 100% kod (dodatkowa kolejka) | 42 | 32 | 190 | 159 |
| w. 26 −40%, cel na wyjściu (dodatkowa kolejka) | **50** | **40** | **196** | **165** |

Każdy wariant to oryginał z jedną warstwą zmniejszoną o 40% neuronów (−0,6% parametrów):
- **warstwa 13** traci od 9 do 16 zadań z 542 w testach „+”; na MBPP+ to strata prawdziwa, a nie przypadek;
- **warstwa 26** nie traci nic.

Pamięć i szybkość się nie zmieniają, bo zmiana jest za mała. Jakość kodu (ruff, pyright, złożoność) też się nie zmienia.

*2026-10-30 18:39 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-11-01 14:21 — Autor*

---
---
---
