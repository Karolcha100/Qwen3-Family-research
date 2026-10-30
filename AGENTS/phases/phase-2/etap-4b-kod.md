# Etap 4b — zmniejszanie warstw z myślą o kodzie (warstwy 2, 13, 14, 26)

*2026-10-30 12:59 — Claude Opus 5.5*

**Status raportu:** do przeczytania

## Co masz zrobić

Przeczytaj i odpowiedz na **K37** (co trenować) i **K38** (waga kodu w mapie) w `AGENTS/phases/phase-2/agents-issues-6.md`. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”. Uwagi do raportu możesz pisać pod nim w GUI; przyciskiem „🔒 Zakończ dyskusję” zamykasz raport.

W skrócie:
- start z mapy kodu daje na Pythonie o ~37% mniejszą KL niż start ze starej mapy, kosztem ~30% większej KL na tekście;
- z czterech warstw najlepiej znoszą zmniejszenie 13 i 14, a 2 i 26 są ~3,5× gorsze;
- trening po najmniejszych kwadratach daje mało (od 1% do 20%), a w warstwie 26 prawie nic; stąd pytanie K37.

---

## 1. Co zrobiono

Liczone 11:30–12:59 pod Twoją nieobecność (@T012), według decyzji @phase-2:K18, K21, K24–K28.

1. **Nowe dane**, rozłączne: Python z The Stack i tekst C4, w proporcji 75/25 (@phase-2:K26). Osobne porcje do pomiaru mapy (48 sekwencji Python + 16 C4), do treningu (366 + 122, ok. 1 mln tokenów) i do oceny (16 + 16, nigdy niewidziane przy pomiarze ani treningu). Każda sekwencja ma 2048 tokenów.
2. **Mapa kodu:** przesiew Fishera (jak w etapie 2) na nowej porcji pomiarowej, potem mapa ważona:

$$
m_{\ell} = 0{,}75 \cdot \frac{m^{\text{kod}}_{\ell}}{\sum_j m^{\text{kod}}_{\ell,j}} + 0{,}25 \cdot \frac{m^{\text{tekst}}_{\ell}}{\sum_j m^{\text{tekst}}_{\ell,j}}
$$

   Słownie: w każdej warstwie $\ell$ mapę z kodu i mapę z tekstu dzielimy przez ich sumę (żeby obie miały tę samą skalę) i bierzemy 75% pierwszej i 25% drugiej.
3. **Zmniejszanie warstw** jak w etapie 4: start z najważniejszych neuronów według mapy, potem nowe $W_{down}$ z najmniejszych kwadratów, potem 6 epok treningu z krokiem $5 \cdot 10^{-5}$ (wybór kroku: @T012). Warstwy według @phase-2:K21: 13 i 14 (najmniej wrażliwe na kod), 2 (z początku), 26 (z końca; 27 jest ostatnia i nie ma za nią warstwy do treningu).
4. **Ocena** całego modelu po podmianie warstwy: KL do oryginału osobno na odłożonym Pythonie i odłożonym C4, oraz perpleksja WikiText-2.

## 2. Mapa kodu

| | warstwy 0–27 | średnio |
|---|---|---|
| zgodność dwóch połówek mapy kodu (po 24 sekwencje) | 0,62–0,92 | 0,83 |
| mapa kodu vs mapa tekstu (ta sama porcja pomiarowa) | od −0,22 do 0,29 | 0,00 |
| nowa mapa (75/25) vs stara mapa (z tekstu) | 0,50–0,78 | 0,63 |

(liczby to korelacje Spearmana rankingów neuronów)

Co z tego wynika:
- mapa kodu jest powtarzalna: dwie połówki zgadzają się w 0,83, więc cała mapa z 48 sekwencji ma wiarygodność ok. 0,9 (wzór Spearmana–Browna z etapu 2);
- przy 3× większej porcji kodu niż w etapie 2 nadal wychodzi, że **dla kodu ważne są inne neurony niż dla tekstu** (korelacja wokół zera); to potwierdza sekcję 4 raportu etapu 2;
- nowa mapa jest wyraźnie inna od starej, więc ma sens porównywać, od której zaczynać.

## 3. Warstwa 13: od której mapy zacząć

![Nowa i stara mapa](AGENTS/phases/phase-2/figures/kod-mapa-nowa-vs-stara-13.png)

Oba wykresy pokazują KL całego modelu po zmniejszeniu i treningu warstwy 13; im niżej, tym bliżej oryginału. Niebieskie słupki: start z nowej mapy kodu, pomarańczowe: start ze starej mapy z tekstu. Trening i dane są w obu przypadkach te same; różni się tylko to, które neurony zostają na starcie.

| Zmniejszenie | Start | KL Python | KL C4 | Perpleksja WikiText-2 |
|---|---|---|---|---|
| 20% | mapa kodu | **0,00133** (−38%) | 0,00340 (+33%) | 12,693 |
| 20% | stara mapa | 0,00215 | **0,00255** | 12,685 |
| 40% | mapa kodu | **0,00321** (−36%) | 0,00813 (+26%) | 12,752 |
| 40% | stara mapa | 0,00504 | **0,00643** | 12,735 |

(oryginał: perpleksja 12,660; procenty względem startu ze starej mapy)

Co widać: start z mapy kodu wyraźnie lepiej zachowuje Pythona, a gorzej tekst. Różnica nie znika po treningu, więc **start ma znaczenie także po treningu** (przynajmniej po 6 epokach; dłuższy trening sprawdza @phase-2:K31). Perpleksja WikiText-2 prawie się nie zmienia, bo jedna warstwa to mała zmiana.

## 4. Cztery warstwy

![Cztery warstwy](AGENTS/phases/phase-2/figures/kod-etap4-warstwy.png)

Lewy wykres: KL na odłożonym Pythonie po treningu, prawy: na odłożonym C4. Niebieskie słupki: zmniejszenie o 20%, pomarańczowe: o 40%. Wszędzie start z mapy kodu.

KL na Pythonie dla trzech kroków (samo wycięcie → najmniejsze kwadraty → trening):

| Warstwa | Zmniejszenie | wycięcie | najmn. kwadraty | trening | zysk z treningu | KL C4 po treningu |
|---|---|---|---|---|---|---|
| 2 | 20% | 0,00568 | 0,00423 | 0,00390 | −8% | 0,0100 |
| 2 | 40% | 0,0148 | 0,0119 | 0,0107 | −11% | 0,0261 |
| 13 | 20% | 0,00241 | 0,00163 | 0,00133 | −18% | 0,0034 |
| 13 | 40% | 0,00586 | 0,00403 | 0,00321 | −20% | 0,0081 |
| 14 | 20% | 0,00223 | 0,00144 | 0,00119 | −18% | 0,0037 |
| 14 | 40% | 0,00537 | 0,00364 | 0,00295 | −19% | 0,0085 |
| 26 | 20% | 0,00365 | 0,00340 | 0,00337 | −1% | 0,0087 |
| 26 | 40% | 0,0122 | 0,0114 | 0,0113 | −1% | 0,0233 |

Co widać:
- **13 i 14** znoszą zmniejszenie najlepiej i podobnie; **2 i 26** są przy 40% ok. 3,5× gorsze. Zgadza się to z mapą (etap 2, sekcja 5): w warstwie 2 i na końcu modelu są pojedyncze bardzo ważne neurony;
- KL na C4 jest wszędzie 2–3× większa niż na Pythonie. Częściowo to skutek mapy kodu, a częściowo tego, że kod jest dla modelu łatwiej przewidywalny (etap 2, sekcja 5);
- **trening daje mało:** 18–20% w warstwach 13 i 14, 8–11% w warstwie 2, 1% w warstwie 26. Najmniejsze kwadraty dają więcej niż trening (od 7% w warstwie 26 do 35% w 14).

## 5. Warstwa 26: trening prawie nic nie daje

W warstwie 26 trening ma cel „zgodność za warstwą 27”, czyli za ostatnią warstwą modelu. Błąd za warstwą 27 jest już po najmniejszych kwadratach bardzo mały względem wielkości sygnału (0,2–0,6% wariancji), a mimo to KL całego modelu jest duża. Najlepsza była 1. epoka, potem błąd na walidacji rośnie i wraca.

**Moje przypuszczenie (niesprawdzone):** po warstwie 27 w sygnale dominuje kilka bardzo dużych wymiarów, a końcowa normalizacja przed wyjściem je ścina. Cel „za warstwą 27” patrzy głównie na te duże wymiary, a KL zależy od reszty. To kolejny argument, żeby sprawdzić cel na wyjściu modelu (pytanie **K37**).

## 6. Błąd w pierwszym przebiegu (poprawiony)

W pierwszym przebiegu warstwa 26 po treningu dawała KL ~1,1 (model zepsuty). Przyczyna: skrypt brał cel treningu jako `hidden_states[ℓ+2]` z biblioteki transformers, a dla ostatniej warstwy ten element ma już nałożoną końcową normalizację. Warstwa uczyła się więc złego celu. Teraz cel jest przechwytywany bezpośrednio z wyjścia następnej warstwy. Sprawdziłem, że dla warstwy 13 nowy sposób daje dokładnie to samo co stary, więc wcześniejsze wyniki (etap 4, @phase-2:K23) są poprawne. Błędny przebieg zostawiłem w `results/phase2/code/stage4-invalid-target/`.

## 7. Pliki

- dane: `~/qwen3-checkpoints/phase2-code/` (`measurement-set.pt`, `training-set.pt`, `evaluation-set.pt`);
- mapa: `results/phase2/code/stage2/fisher-map.pt`, `code-map-summary.json`;
- wyniki: `results/phase2/code/stage4/layer-*/results.jsonl`, `summary.json`;
- kod: `scripts/phase2_code_sets.py`, `scripts/phase2_code_map.py`, `scripts/phase2_stage4_one_layer.py`, `scripts/phase2_code_stage4_analysis.py`.

*2026-10-30 12:59 — Claude Opus 5.5*
