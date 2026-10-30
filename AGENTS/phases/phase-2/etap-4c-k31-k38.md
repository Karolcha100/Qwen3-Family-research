# Etap 4c — punkt startu, cel treningu, waga kodu i pierwsze testy kodu (K31–K38)

*2026-10-30 17:13 — Claude Opus 5.5*

**Status raportu:** do przeczytania

## Co masz zrobić

Przeczytaj raport i odpowiedz na pytania **K40–K43** w `AGENTS/phases/phase-2/agents-issues-8.md`. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”. Uwagi do raportu możesz pisać pod nim w GUI.

W skrócie:
- **oryginalny model odtwarza raport Qwen3:** średnia EvalPlus 36,9 u nas, 36,23 w raporcie;
- **zmniejszenie warstwy 13 o 40% kosztuje ~2,5–2,9 punktu pass@1, a warstwy 26 o 40% nic** (każde to −0,6% parametrów), choć KL warstwy 26 jest 3× większa: **KL nie przewiduje pass@1 między warstwami**;
- **punkt startu ma znaczenie także po 16 epokach:** mapa kodu jest najlepsza, start losowy o 64% gorszy (KL na Pythonie); **scalanie neuronów jest gorsze niż ich zwykłe usunięcie**;
- **cel na wyjściu modelu** pomaga tam, gdzie stary cel zawodzi (warstwa 26: −17% KL), ale w warstwie 13 nie jest lepszy, a jest ~18× wolniejszy;
- **mapa 100% kod** daje na Pythonie o 11–17% mniejszą KL niż 75/25, za to na tekście o 25–35% większą.

---

## 1. Co zrobiono

Kolejka z decyzji @phase-2:K31–K38 (uruchomienie: @phase-2:K39), 14:31–16:38, i dodatkowa kolejka 16:38–17:13 (Twoja zgoda z 16:30: „możesz dodać trochę więcej obliczeń, tak abyś się uwinął do 17:30”).

Wszędzie jak w etapie 4b: dane 75% Python + 25% C4, zmniejszenie jednej warstwy (start z wybranych neuronów → najmniejsze kwadraty dla $W_{down}$ → trening), ocena całego modelu przez KL do oryginału na odłożonym Pythonie i odłożonym C4. KL to średnia na token różnica między rozkładem następnego tokenu oryginału i zmniejszonego modelu; im mniej, tym bliżej oryginału.

Testy kodu (@phase-2:K32, K34–K36): HumanEval i MBPP z rozszerzonymi testami EvalPlus (HumanEval+, MBPP+), jedna odpowiedź na zadanie, dekodowanie zachłanne (bez losowania), maks. 768 nowych tokenów. Kod napisany przez model uruchamia się tylko w kontenerze bez sieci (@phase-2:K36). pass@1 to odsetek zadań, w których ta jedna odpowiedź przechodzi wszystkie testy.

## 2. Oryginalny model: odtworzenie raportu Qwen3

| Zestaw | pass@1 |
|---|---|
| HumanEval | 29,9% |
| HumanEval+ | 23,2% |
| MBPP | 51,6% |
| MBPP+ | 42,9% |
| **średnia (jak w raporcie Qwen3)** | **36,9** (raport: 36,23) |

Różnica 0,7 punktu to mniej niż jedno zadanie w HumanEval (1 zadanie = 0,6 punktu), więc sposób zadawania pytań i oceny jest zgodny z tym, którego używa Qwen. Rozwiązania wzorcowe przechodzą testy w 99,4–100% (jedno zadanie HumanEval ma w EvalPlus zbyt ciasną tolerancję liczbową), więc kontener i testy działają.

## 3. K31: od czego zacząć, gdy trening jest długi

![K31](AGENTS/phases/phase-2/figures/kod-k31-punkty-startu.png)

Warstwa 13, zmniejszenie o 40%, 16 epok treningu (cel za następną warstwą). Każda grupa słupków to jeden punkt startu; trzy słupki to kolejne kroki: samo wycięcie, najmniejsze kwadraty, trening. Lewy wykres: KL na Pythonie, prawy: na tekście C4.

| Start | wycięcie | najmn. kwadraty | po treningu | względem mapy |
|---|---|---|---|---|
| mapa kodu 75/25 | 0,00586 | 0,00403 | **0,00306** | — |
| scalanie neuronów | 0,00938 | 0,00504 | 0,00339 | +11% |
| aktywacje (RMS) | 0,00631 | 0,00450 | 0,00344 | +12% |
| losowo | 0,0128 | 0,00733 | 0,00503 | +64% |

(KL na odłożonym Pythonie; na C4 mapa też jest najlepsza, ale różnice są mniejsze: 0,0078 dla mapy, 0,0084–0,0085 dla pozostałych trzech)

Co widać:
- **trening zmniejsza różnice między startami, ale ich nie znosi:** losowy start jest po wycięciu 2,2× gorszy od mapy, po 16 epokach nadal 1,6× gorszy. Mapa jest więc potrzebna także przy długim treningu;
- aktywacje (RMS) są niewiele gorsze od mapy (+12%), więc tanią miarę można traktować jako przybliżenie mapy;
- 16 epok zamiast 6 (ten sam start z mapy) zmniejsza KL tylko o 5% (0,00321 → 0,00306), jak w @phase-2:K23.

**Scalanie neuronów.** Pary podobnych neuronów praktycznie nie istnieją (mediana największego podobieństwa aktywacji usuwanego neuronu do zostającego: 0,13), więc scalałem według wag: 1229 usuwanych neuronów dołączyłem do ~150 grup wokół neuronów z mapy (średnia wag wejściowych, suma wag wyjściowych), potem najmniejsze kwadraty i trening. Wynik: **scalanie jest gorsze niż samo usunięcie tych neuronów** na każdym kroku (0,00938 vs 0,00586 po wycięciu, 0,00339 vs 0,00306 po treningu). Uśrednianie wag psuje neurony, które zostają, bo usuwane neurony robią co innego.

## 4. K37: cel treningu na wyjściu modelu

![K37](AGENTS/phases/phase-2/figures/kod-k37-cel-treningu.png)

Trzy przypadki (grupy słupków), w każdym trzy warianty: same najmniejsze kwadraty (przed treningiem), trening z dotychczasowym celem (zgodność za następną warstwą) i trening z celem na wyjściu modelu (KL rozkładu następnego tokenu; reszta modelu zamrożona). Oba treningi: 6 epok, krok $5 \cdot 10^{-5}$.

| Przypadek | najmn. kwadraty | cel za warstwą | cel na wyjściu | czas treningu (za warstwą / na wyjściu) |
|---|---|---|---|---|
| warstwa 13, −40% | 0,00403 | **0,00321** (−20%) | 0,00375 (−7%) | 1,4 / 24,7 min |
| warstwa 13, −20% | 0,00163 | **0,00133** (−18%) | 0,00163 (0%) | 1,4 / 25,0 min |
| warstwa 26, −40% | 0,0114 | 0,0113 (−1%) | **0,00940** (−18%) | 1,4 / 9,7 min |

(KL na odłożonym Pythonie; w nawiasach zmiana względem najmniejszych kwadratów)

Co widać:
- **w warstwie 26 cel na wyjściu działa, a stary nie:** −18% zamiast −1% (na C4: −12% zamiast −2%). Potwierdza to przypuszczenie z etapu 4b: za ostatnią warstwą sygnał „za warstwą” źle oddaje to, co widzi wyjście;
- **w warstwie 13 cel na wyjściu jest gorszy** niż stary, a przy 20% nie poprawił niczego: najlepsza była epoka 0 (stan po najmniejszych kwadratach), a błąd na walidacji rósł od pierwszej epoki. To wygląda na **za duży krok uczenia** dla tego celu: jego gradient jest bardziej „zaszumiony”, bo przechodzi przez całą resztę modelu. Sprawdzenie z mniejszym krokiem: sekcja 5;
- cel na wyjściu jest **~18× wolniejszy** w warstwie 13 (każdy krok przechodzi przez całą resztę modelu i liczy rozkład na 152 tys. tokenów słownika) i ~7× w warstwie 26 (mniej warstw za nią).

## 5. K37: mniejszy krok uczenia (dodatkowa kolejka)

Warstwa 13, zmniejszenie o 20%, cel na wyjściu, krok $1 \cdot 10^{-5}$ (5× mniejszy), 4 epoki.

| Wariant | KL Python | KL C4 | błąd walidacji po kolejnych epokach |
|---|---|---|---|
| najmniejsze kwadraty (start) | 0,00163 | 0,00436 | 0,00319 |
| cel na wyjściu, krok $5 \cdot 10^{-5}$ | 0,00163 (0%) | 0,00436 (0%) | 0,00321 / 0,00334 / 0,00335 / 0,00355 / 0,00325 / 0,00325 (gorzej niż start) |
| cel na wyjściu, krok $1 \cdot 10^{-5}$ | 0,00152 (−7%) | 0,00382 (−12%) | 0,00305 / 0,00300 / 0,00300 / 0,00295 |
| cel za warstwą, krok $5 \cdot 10^{-5}$, 6 epok | **0,00133** (−18%) | **0,00340** (−22%) | — |

(błąd walidacji to KL na wyjściu modelu na odłożonej porcji danych treningowych)

Co widać: z mniejszym krokiem trening **stabilnie się poprawia** w każdej epoce, więc przyczyną porażki przy 20% był za duży krok. Mimo to w warstwie 13 cel na wyjściu (−7%) jest nadal **słabszy od starego celu** (−18%) i ~12× wolniejszy (16,4 min na 4 epoki wobec 1,4 min na 6). W środku modelu stary cel jest więc lepszym wyborem; cel na wyjściu ma sens dla ostatnich warstw (pytanie K40).

## 6. K38: mapa 100% kod

![K38](AGENTS/phases/phase-2/figures/kod-k38-waga-kodu.png)

Warstwa 13, 6 epok. Trzy mapy startowe: tylko kod, 75% kod / 25% tekst (obecna), tylko tekst (stara).

| Zmniejszenie | Mapa | KL Python | KL C4 |
|---|---|---|---|
| 20% | 100% kod | **0,00111** (−17%) | 0,00458 (+35%) |
| 20% | 75/25 | 0,00133 | 0,00340 |
| 20% | tekst | 0,00215 (+61%) | **0,00255** (−25%) |
| 40% | 100% kod | **0,00284** (−11%) | 0,0101 (+25%) |
| 40% | 75/25 | 0,00321 | 0,00813 |
| 40% | tekst | 0,00504 (+57%) | **0,00643** (−21%) |

(procenty względem mapy 75/25)

Co widać: waga kodu w mapie działa jak suwak. Przejście 75/25 → 100% kod daje na Pythonie mniej (11–17%) niż traci na tekście (25–35%); przejście 75/25 → tekst traci na Pythonie dużo więcej (57–61%), niż zyskuje na tekście (21–25%). 75/25 jest więc rozsądnym środkiem; wybór zależy od tego, jak bardzo zależy nam na tekście (pytanie K41).

## 7. Testy kodu: czy KL przekłada się na pass@1

![Testy kodu](AGENTS/phases/phase-2/figures/kod-testy-pass1.png)

Cztery grupy słupków to cztery zestawy testów; w każdej grupie kolejne modele: oryginał i cztery modele, w których jedna warstwa jest zmniejszona o 40% (każdy to −3,8 mln parametrów, czyli −0,6% modelu).

| Model | KL Python | HumanEval | HumanEval+ | MBPP | MBPP+ | średnia |
|---|---|---|---|---|---|---|
| oryginał | 0 | 29,9 | 23,2 | 51,6 | 42,9 | **36,9** |
| w. 13, cel za warstwą (16 epok) | 0,00306 | 26,8 | 20,7 | 49,2 | 40,2 | 34,2 |
| w. 13, cel na wyjściu | 0,00375 | 27,4 | 20,7 | 48,1 | 39,7 | 34,0 |
| w. 13, mapa 100% kod | 0,00284 | 25,6 | 19,5 | 50,3 | 42,1 | 34,4 |
| w. 26, cel na wyjściu | 0,00940 | 30,5 | 24,4 | 51,9 | 43,7 | **37,6** |

(pass@1 w %; średnia jak w raporcie Qwen3)

Porównanie parami z oryginałem (zadania rozwiązane z testami „+”: ile model zyskał, ile stracił; p to dokładny test McNemara, czyli prawdopodobieństwo takiej lub większej przewagi strat nad zyskami, gdyby zmiana nic nie psuła):

| Model | HumanEval+: zysk / strata (p) | MBPP+: zysk / strata (p) |
|---|---|---|
| w. 13, cel za warstwą | 6 / 10 (0,45) | 5 / 15 (**0,04**) |
| w. 13, cel na wyjściu | 5 / 9 (0,42) | 4 / 16 (**0,01**) |
| w. 13, mapa 100% kod | 5 / 11 (0,21) | 11 / 14 (0,69) |
| w. 26, cel na wyjściu | 4 / 2 (0,69) | 6 / 3 (0,51) |

Co widać:
- **zmniejszenie warstwy 13 o 40% kosztuje ~2,5–2,9 punktu** średniej; na MBPP+ strata jest statystycznie wyraźna (p 0,01–0,04) dla obu celów treningu;
- **trzy warianty warstwy 13 są nie do odróżnienia** (34,0–34,4): różnice KL między nimi (0,0028–0,0038) nie przekładają się na mierzalną różnicę pass@1;
- **niespodzianka: warstwa 26 nie traci nic** (37,6 wobec 36,9; zyski i straty w szumie), choć jej KL na Pythonie jest 3× większa niż w warstwie 13. **KL nie przewiduje więc pass@1 między warstwami.** Moje przypuszczenie (niesprawdzone): przy dekodowaniu zachłannym liczy się tylko, czy najbardziej prawdopodobny token się nie zmienia; zmiany w końcowej warstwie mogą głównie „rozmywać” rozkład (co KL mocno karze), nie zmieniając najczęściej wybranego tokenu. Da się to sprawdzić tanio, licząc odsetek tokenów, w których zmniejszony model wybiera ten sam token co oryginał (pytanie K43);
- nawet przy braku zmiany średniej model rozwiązuje inaczej ~5–15% zadań (zyski i straty), więc pojedyncze różnice ~1–2 punktów to szum;
- **sprawność:** parametry 596,0 → 592,3 mln (−0,6%), szczyt pamięci 3,38 → 3,37 GB; szybkość generowania waha się 101–141 tokenów/s bez związku z modelem (to szum pomiaru przy małej zmianie, a nie efekt zmniejszenia);
- **jakość kodu (analiza statyczna):** bez zmian; średnio 0,04–0,09 uwag ruff i 0,01–0,04 błędów pyright na rozwiązanie, długość rozwiązań 19,6–21,6 (HumanEval) i 6,8–7,5 (MBPP) niepustych linii we wszystkich modelach.

## 8. Czasy: szacunek a rzeczywistość

| Krok | szacunek | faktycznie |
|---|---|---|
| generowanie HumanEval / MBPP (jeden model) | 4 / 6 min | 2,3 / 3,5–3,8 min |
| testy HumanEval / MBPP w kontenerze | 1,5 / 1,5 min | 0,5 / 0,8–1,2 min |
| K38 (mapa 100% kod, 2 zmniejszenia, 6 epok) | 10 min | 8,5 min |
| K31 (4 starty, 16 epok) | 28 min | 26,7 min |
| K37 warstwa 13 (2 zmniejszenia, cel na wyjściu) | 76 min | 56 min |
| K37 warstwa 26 | 14 min | 13,3 min |
| **cała kolejka K31–K38** | **167 min** | **~127 min** |

Szacunki dla treningów były trafne (±10%), poza celem na wyjściu w warstwie 13 (zawyżony o ~35%); testy kodu są ~1,6× szybsze, niż zakładałem. Nowe szacunki wpisałem do procedur (sekcja 10).

## 9. Pliki

- wyniki: `results/phase2/code/k31/`, `results/phase2/code/k37/`, `results/phase2/code/k37-lr1e-5/`, wiersze `code-only` w `results/phase2/code/stage4/layer-13/`; zbiorczo `results/phase2/code/k31-k38-summary.json`;
- testy kodu: `results/phase2/code-eval/<model>/` (rozwiązania, wyniki testów, `*-summary.json` z pass@1 i analizą statyczną, `*-efficiency.json`);
- zmniejszone warstwy: `~/qwen3-checkpoints/phase2-code/mlps/`;
- kod: `scripts/phase2_code_generate.py`, `scripts/phase2_code_evaluate.py`, `scripts/phase2_code_k31_k38_analysis.py`, `src/qwen_compression/training.py`, kontener `sandbox/`.

*2026-10-30 17:13 — Claude Opus 5.5*
