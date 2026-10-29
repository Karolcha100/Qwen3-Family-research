# Indeks decyzji autora

Wszystkie pytania z `AGENTS/phases/*/agents-issues-*.md` w jednej tabeli: tytuł i decyzja dosłownie z pola **Decyzja**. Plik jest **generowany** poleceniem z `AGENTS/memory/procedury.md` (sekcja „Indeks decyzji”), więc nie edytuje się go ręcznie. Odświeżany na końcu każdej sesji. Gdy indeks i plik źródłowy się różnią, wygrywa plik źródłowy.

*Wygenerowano: 2026-10-29 21:34 — Claude Opus 5.5*

---

| Pytanie | Tytuł | Decyzja |
|---|---|---|
| @phase-0:K1 | 🔴 Repozytorium git | Wybieram opcje B, prywatne repozytorium pod nazwą "Qwen3-Family-research", dodaj do .gitignore, pycache i te inne rzeczy. Pushujesz po każdej mojej odpowiedzi w chacie do ciebie (o ile coś się zmieniło) |
| @phase-0:K2 | 🔴 Plan faz do zatwierdzenia | Opcja C, jeszcze nie i najpierw sama Phase 1 (potem rozpiszę co chcę w następnych fazach robić) |
| @phase-0:K3 | 🟡 Instalacja z `sudo` jako zadania autora | A |
| @phase-0:K4 | 🟡 Menedżer środowiska Pythona | A |
| @phase-0:K5 | 🟡 Wersja Pythona | Opcja A |
| @phase-0:K6 | 🔴 Własne implementacje czy gotowe biblioteki | Opcja B, aczkolwiek pragnę zaznaczyć ze sam wybiorę metody. |
| @phase-0:K7 | 🟡 Qwen3 Base czy wersja instrukcyjna | ✅ Zgadzam się na opcje A (po @A2) |
| @phase-0:K8 | 🟡 Dane kalibracyjne | ✅ Wybieram C, przy czym ja nie chcę kwantyzować modelu w klasyczny sposób (nie mówię że tego nie zrobimy, ale generalnie nie napisałem jeszcze tobie mojego głównego pomysłu) (po @A3) |
| @phase-0:K9 | 🟡 Protokół perplexity | ✅ Niech będzie A (po @A4) |
| @phase-0:K10 | 🟡 Kto i kiedy uruchamia obliczenia na GPU | Generalnie wolę B, z zastrzeżeniem że raczej ja powiem kiedy Agent ma uruchomić a nie że wpisuję sam komendy. |
| @phase-0:K11 | 🟢 Zapis wyników | A |
| @phase-0:K12 | 🟢 Struktura kodu | Dobra, ale chwilka, ja jeszcze nie napisałem tobie jakie rzeczy będziemy robić. Generalnie pomysł A jest spoko, ale zauważ że jeszcze nie wiesz jakie metody będziemy robić. |
| @phase-0:K13 | 🟡 Model-sędzia do oceny odpowiedzi Qwen3 (z @T002) | Myślę że pójdziemy w opcję C, przy czym to trzeba jeszcze dopracować. |
| @phase-0:K14 | 🟢 Narzędzia jakości kodu | ✅ To zgadzam się na A (po @A9) |
| @phase-0:K15 | 🟢 Notatki do nauki | A |
| @phase-0:K16 | 🟢 Folder na pytania startowe | A |
| @phase-0:K17 | 🟡 Push do GitHuba po sesji | Opcja B - Po każdym commicie rób też git push. |
| @phase-0:K18 | 🟡 Z czego składa się sędzia | Opcja B jest spoko, ale tutaj należy to jeszcze rozważyć. |
| @phase-0:K19 | 🟡 Skala metryk 0–100 | Nie będziemy stosować sędziów, tylko klasyfikatory (modele nagrody), tak więc zadaj to pytanie jeszcze raz, biorąc pod uwagę ten kontekst. |
| @phase-0:K20 | 🟡 Ocena bezwzględna czy względem BF16 | C |
| @phase-0:K21 | 🟡 Język pytań | A |
| @phase-0:K22 | 🟡 Skąd wziąć 50 pytań | C |
| @phase-0:K23 | 🟢 Liczba pytań | C |
| @phase-0:K24 | 🟡 Jak generować odpowiedzi do oceny | B |
| @phase-0:K25 | 🟡 Tryb myślenia Qwen3 przy ocenie | B |
| @phase-0:K26 | 🟢 Ręczna kalibracja sędziego | A |
| @phase-0:K27 | 🟡 Lista 16 metryk | C |
| @phase-0:K28 | 🟢 Które metryki regułowe zostają | A |
| @phase-0:K29 | 🟡 Czy jeden model nagrody da kilka metryk | B |
| @phase-0:K30 | 🟢 Czy zapisujemy skompresowane modele | B, aczkolwiek zauważ znowu że jeszcze nie wiesz co będziemy tak naprawdę robić!!! |
| @phase-0:K31 | 🟢 Powtórzenia z kilkoma ziarnami | Już chyba na to odpowiedziałem że B w innym pytaniu, ale ponów je jeśli nie. |
| @phase-0:K32 | 🟢 Format kalibracji dla modelu instrukcyjnego | A |
| @phase-0:K33 | 🟡 Co mogę robić bez Twojego „uruchom” | A |
| @phase-0:K34 | 🟡 Jak chcesz wybierać metody | B |
| @phase-0:K35 | 🟢 (ponowione K31) Ziarna przy wyborze danych kalibracyjnych | C |
| @phase-0:K36 | 🟡 (ponowione K19) Jak zamienić wynik modelu nagrody na 0–100 | ✅ Zgadzam się na twoją propozycję (po @A10) |
| @phase-0:K37 | 🟡 Limit długości odpowiedzi z myśleniem | B |
| @phase-0:K38 | 🟢 Czy klasyfikator widzi myślenie modelu | A |
| @phase-0:K39 | 🟡 Pytania w stylu IFEval w naszych 200 pytaniach a K28 | A, chociaż proszę o jakiś wątek wyjaśniający mi co to zmienia |
| @phase-0:K40 | 🟢 Zgodność z odpowiedzią wzorcową | A |
| @phase-0:K41 | 🟡 Skąd wziąć 200 pytań | C |
| @phase-0:K42 | 🟢 Druga tura pytań MT-Bench | B |
| @phase-0:K43 | 🟢 Polecenia agenta: notatki czy mały skrypt | C |
| @phase-pomysl:K1 | 🔴 Co nazywamy neuronem | A |
| @phase-pomysl:K2 | 🟡 Jak zaburzamy neuron (wartości −1, −0,5, 0,5, 1) | A |
| @phase-pomysl:K3 | 🟡 Jak mierzymy „sensowność” w części A | ✅ Okej, to odpowiedź A, ale generalnie zamiast 100 neuronów o największym wpływie, widziałbym jakieś 250. (po @A11) |
| @phase-pomysl:K4 | 🟡 Jak liczyć część A: wszystko czy z przesiewem | C |
| @phase-pomysl:K5 | 🟡 Cel treningu zmniejszonej warstwy (C2–C3) | wolę B |
| @phase-pomysl:K6 | 🟢 Dane do treningu warstwy: zapis na dysk czy w locie | Zapis na dysk, ewentualnie zmniejszymy liczbę N_{tokens} |
| @phase-pomysl:K7 | 🟢 Start zmniejszonej warstwy | A |
| @phase-pomysl:K8 | 🟡 Dotrenowanie całego modelu (C4) | D |
| @phase-pomysl:K9 | 🟡 Plan faz z pomysłu | Podane przez ciebie propozycje etapów Phase 1 są dobre, aczkolwiek chciałbym w phase 1 realizować tylko etapy 1, 2, 3, 4. |
| @phase-pomysl:K10 | 🟢 Numer fazy | A, wcześniej się pomyliłem z numerami sorry xD |
| @phase-pomysl:K11 | 🟡 Tekst, na którym mierzymy zaburzenia | A |
| @phase-pomysl:K12 | 🟢 Które warstwy w pilocie (etap 1) | A |
| @phase-pomysl:K13 | 🟢 Ile tokenów zapisać do treningu warstwy (etap 4) | A |
| @phase-pomysl:K14 | 🟡 Jak mocno zmniejszamy warstwę w etapie 4 | B aczkolwiek proponuje -5%, -10%, -20%, -40% |
| @phase-pomysl:K15 | 🟢 Układ kodu | A |
