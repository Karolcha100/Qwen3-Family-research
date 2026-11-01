# Porównanie z oryginalnym Qwen3 — stan po obliczeniach z 30.10 (do 17:13)

*2026-10-30 18:38 — Claude Opus 5.5*

**Status raportu:** zamknięty (2026-11-01 14:28, Claude Opus 5.5 na prośbę autora @T018)
## Co masz zrobić

Przeczytaj. Odpowiada na @T013 i @T016. Jedyna decyzja z tego raportu to **K44** (pass@2 i pass@3) w `AGENTS/phases/phase-2/agents-issues-9.md`. Uwagi możesz pisać pod raportem.

W skrócie (liczby zadań rozwiązanych z testami „+”, razem w HumanEval+ i MBPP+, z 542 zadań):
- **oryginał rozwiązuje 200 zadań**;
- **warstwa 26 zmniejszona o 40%: 205** (+5; w granicach przypadku);
- **warstwa 13 zmniejszona o 40%: 184–191** (od 9 do 16 mniej), zależnie od wariantu.

---

## 1. Co porównuję

**Oryginał** to Qwen3-0.6B-Base (596 mln parametrów), bez zmian.

**„Nasz model”** to ten sam model, w którym **jedna warstwa MLP** ma usunięte 40% neuronów (1229 z 3072). Zostałe neurony są poprawione najmniejszymi kwadratami i treningiem. Usuwamy tym samym 3,8 mln parametrów, czyli **0,6% modelu**. To jeszcze nie jest model zmniejszony do praktycznego użytku, tylko test metody na jednej warstwie.

| Wariant | Która warstwa | Start | Trening |
|---|---|---|---|
| w. 13, cel za warstwą | 13 | mapa kodu 75/25 | 16 epok, cel za następną warstwą |
| w. 13, cel na wyjściu | 13 | mapa kodu 75/25 | 6 epok, cel na wyjściu modelu |
| w. 13, mapa 100% kod | 13 | mapa tylko z kodu | 6 epok, cel za następną warstwą |
| w. 26, cel na wyjściu | 26 | mapa kodu 75/25 | 6 epok, cel na wyjściu modelu |

Szczegóły, jak powstał każdy wariant: raport `AGENTS/phases/phase-2/etap-4c-k31-k38.md`.

## 2. Testy kodu: liczba rozwiązanych zadań

![Liczba zadań](AGENTS/phases/phase-2/figures/porownanie-liczba-zadan.png)

Lewy wykres: HumanEval (164 zadania), prawy: MBPP (378 zadań). W każdej grupie pięć słupków: oryginał i cztery warianty; liczba nad słupkiem to liczba rozwiązanych zadań. „+” to te same zadania z dużo większą liczbą testów (@T015).

| Model | HumanEval (z 164) | HumanEval+ | MBPP (z 378) | MBPP+ | razem (z 1084) |
|---|---|---|---|---|---|
| **oryginał** | **49** | **38** | **195** | **162** | **444** |
| w. 13, cel za warstwą | 44 (−5) | 34 (−4) | 186 (−9) | 152 (−10) | 416 (−28) |
| w. 13, cel na wyjściu | 45 (−4) | 34 (−4) | 182 (−13) | 150 (−12) | 411 (−33) |
| w. 13, mapa 100% kod | 42 (−7) | 32 (−6) | 190 (−5) | 159 (−3) | 423 (−21) |
| w. 26, cel na wyjściu | **50 (+1)** | **40 (+2)** | **196 (+1)** | **165 (+3)** | **451 (+7)** |

(w nawiasach: różnica w liczbie zadań względem oryginału; „razem” to suma czterech kolumn)

## 3. Które zadania się zmieniły

![Zyski i straty](AGENTS/phases/phase-2/figures/porownanie-zyski-straty.png)

Dla każdego wariantu: ile zadań, których oryginał **nie** rozwiązał, wariant rozwiązuje (zielone, w prawo), i ile zadań rozwiązanych przez oryginał wariant **traci** (czerwone, w lewo). Liczone na testach „+”.

| Model | HumanEval: zysk / strata | HumanEval+ | MBPP | MBPP+ |
|---|---|---|---|---|
| w. 13, cel za warstwą | +7 / −12 (p 0,36) | +6 / −10 (p 0,45) | +6 / −15 (p 0,08) | +5 / −15 (**p 0,04**) |
| w. 13, cel na wyjściu | +6 / −10 (p 0,45) | +5 / −9 (p 0,42) | +6 / −19 (**p 0,01**) | +4 / −16 (**p 0,01**) |
| w. 13, mapa 100% kod | +5 / −12 (p 0,14) | +5 / −11 (p 0,21) | +8 / −13 (p 0,38) | +11 / −14 (p 0,69) |
| w. 26, cel na wyjściu | +4 / −3 (p 1,0) | +4 / −2 (p 0,69) | +7 / −6 (p 1,0) | +6 / −3 (p 0,51) |

p (dokładny test McNemara) mówi, jak łatwo taka przewaga strat nad zyskami (lub odwrotnie) zdarzyłaby się przypadkiem, gdyby zmiana w modelu nie zmieniała jego umiejętności. Poniżej 0,05 traktuję różnicę jako prawdziwą.

Co widać:
- **każda zmiana „przerzuca” zadania w obie strony**, nawet gdy wynik prawie się nie zmienia. Dlatego sama różnica 1–3 zadań nic nie znaczy;
- **warstwa 13**: wyraźnie więcej strat niż zysków; na MBPP+ różnica jest prawdziwa (p 0,01–0,04) dla obu wariantów z mapą 75/25. Wariant z mapą 100% kod traci mniej na MBPP (−3 zadania na MBPP+), ale więcej na HumanEval (−6 na HumanEval+); w sumie −21 zadań wobec −28 i −33. Ta różnica między wariantami jest w granicach przypadku;
- **warstwa 26**: zysków jest tyle samo co strat albo więcej; **nie ma śladu pogorszenia**.

## 4. Inne miary jakości

| Model | KL na Pythonie | KL na tekście C4 | perpleksja WikiText-2 |
|---|---|---|---|
| oryginał | 0 | 0 | 12,66 |
| w. 13, cel za warstwą | 0,0031 | 0,0078 | 12,75 (+0,7%) |
| w. 13, cel na wyjściu | 0,0038 | 0,0087 | 12,76 (+0,8%) |
| w. 13, mapa 100% kod | 0,0028 | 0,0101 | 12,79 (+1,0%) |
| w. 26, cel na wyjściu | 0,0094 | 0,0209 | 13,21 (+4,3%) |

KL mówi, o ile rozkład następnego tokenu odbiega od oryginału (średnio na token); perpleksja mówi, jak dobrze model przewiduje zwykły tekst (mniej = lepiej).

Co widać: **miary „rozkładowe” i testy kodu mówią co innego.** Warstwa 26 odbiega od oryginału najbardziej (KL 3× większa, perpleksja +4,3%), a w testach kodu wypada najlepiej. Możliwe wyjaśnienie (niesprawdzone): przy jednej odpowiedzi bez losowania liczy się tylko, czy najbardziej prawdopodobny token zostaje ten sam, a zmiany w końcowej warstwie raczej „rozmywają” rozkład, niż zmieniają ten token. To jest pytanie K43 (`agents-issues-8.md`).

## 5. Sprawność

| Model | parametry | pamięć GPU (szczyt) | szybkość generowania |
|---|---|---|---|
| oryginał | 596,0 mln | 3,4 GB | 124 / 134 tokeny/s |
| warianty | 592,3 mln (−0,6%) | 3,4 GB | 101–132 / 118–141 tokenów/s |

(szybkość: HumanEval / MBPP; generowanie po 16 zadań naraz, bf16, RTX 4070 SUPER)

Co widać: przy −0,6% parametrów zysku w pamięci i szybkości nie da się zmierzyć. Rozrzut szybkości (101–141) to szum pomiaru (zależy od długości odpowiedzi w każdej paczce), a nie efekt zmniejszenia. Zysk w sprawności pojawi się dopiero, gdy zmniejszymy wiele warstw.

## 6. Jakość kodu bez uruchamiania

| Model | uwagi ruff na rozwiązanie | błędy pyright na rozwiązanie | złożoność (HumanEval / MBPP) | niepuste linie (HumanEval / MBPP) |
|---|---|---|---|---|
| oryginał | 0,07 / 0,04 | 0,02 / 0,03 | 6,0 / 3,5 | 20,2 / 7,2 |
| warianty | 0,07–0,09 / 0,04–0,05 | 0,01–0,03 / 0,02–0,04 | 5,0–5,6 / 3,5–3,9 | 19,6–21,6 / 6,8–7,5 |

(złożoność cyklomatyczna: liczba niezależnych ścieżek w najbardziej złożonej funkcji rozwiązania)

Co widać: styl i poprawność kodu (bez uruchamiania) **nie zmieniają się**; rozwiązania mają podobną długość i złożoność.

## 7. Wnioski

1. **Ocena jest zgodna z Qwen:** oryginał ma u nas średnią 36,9, raport Qwen3 podaje 36,23 (różnica ~1 zadanie HumanEval).
2. **Jedna warstwa w środku modelu (13) zmniejszona o 40% kosztuje ~9–16 zadań z 542** (testy „+”). To mało w liczbach bezwzględnych, ale jest to tylko 0,6% parametrów, więc przy zmniejszaniu wielu warstw straty będą się sumować.
3. **Końcowa warstwa (26) zmniejszona o 40% nie kosztuje nic** w testach kodu, choć KL i perpleksja pogarszają się bardziej niż w warstwie 13. Mapa (wizualizacja w dyskusji raportu `etap-4c-k31-k38.md`) też wskazuje końcowe warstwy jako najtańsze: 20–25, a zaraz za nimi 26. To sugeruje, gdzie zmniejszać w pierwszej kolejności (pytanie K45 w `agents-issues-9.md`).
4. **Testy na jednej odpowiedzi są „zaszumione”:** każda zmiana przerzuca kilka–kilkanaście zadań w obie strony. pass@2 i pass@3 z kilku losowanych odpowiedzi (Twoja prośba z @T015) dadzą pełniejszy obraz (pytanie K44).

## 8. Pliki

- skrypt: `scripts/phase2_code_comparison.py` (tabele i wykresy tego raportu);
- dane: `results/phase2/code-eval/comparison.json`, rozwiązania i wyniki testów każdego modelu w `results/phase2/code-eval/<model>/`.

*2026-10-30 18:38 — Claude Opus 5.5*

## Dyskusja

---
---
---

🔒 Dyskusja zakończona na prośbę autora (@T018). Podsumowanie wszystkich raportów Phase 2: `AGENTS/phases/phase-2/raport-zbiorczy-phase-2.md`.

*2026-11-01 14:28 — Claude Opus 5.5*

---
---
---
