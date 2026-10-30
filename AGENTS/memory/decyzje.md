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
| @phase-2:K1 | 🔴 Co nazywamy neuronem | A |
| @phase-2:K2 | 🟡 Jak zaburzamy neuron (wartości −1, −0,5, 0,5, 1) | A |
| @phase-2:K3 | 🟡 Jak mierzymy „sensowność” w części A | ✅ Okej, to odpowiedź A, ale generalnie zamiast 100 neuronów o największym wpływie, widziałbym jakieś 250. (po @A11) |
| @phase-2:K4 | 🟡 Jak liczyć część A: wszystko czy z przesiewem | C |
| @phase-2:K5 | 🟡 Cel treningu zmniejszonej warstwy (C2–C3) | wolę B |
| @phase-2:K6 | 🟢 Dane do treningu warstwy: zapis na dysk czy w locie | Zapis na dysk, ewentualnie zmniejszymy liczbę N_{tokens} |
| @phase-2:K7 | 🟢 Start zmniejszonej warstwy | A |
| @phase-2:K8 | 🟡 Dotrenowanie całego modelu (C4) | D |
| @phase-2:K9 | 🟡 Plan faz z pomysłu | Podane przez ciebie propozycje etapów Phase 1 są dobre, aczkolwiek chciałbym w phase 1 realizować tylko etapy 1, 2, 3, 4. |
| @phase-2:K10 | 🟢 Numer fazy | A, wcześniej się pomyliłem z numerami sorry xD |
| @phase-2:K11 | 🟡 Tekst, na którym mierzymy zaburzenia | A |
| @phase-2:K12 | 🟢 Które warstwy w pilocie (etap 1) | A |
| @phase-2:K13 | 🟢 Ile tokenów zapisać do treningu warstwy (etap 4) | A |
| @phase-2:K14 | 🟡 Jak mocno zmniejszamy warstwę w etapie 4 | B aczkolwiek proponuje -5%, -10%, -20%, -40% |
| @phase-2:K15 | 🟢 Układ kodu | A |
| @phase-2:K16 | 🟢 Które δ mierzyć dalej | A (tylko δ = ±1) |
| @phase-2:K17 | 🔴 Etap 2 policzony przesiewem na dużej liczbie tokenów | A (mapa = przesiew, pomiar dokładny do kontroli) |
| @phase-2:K18 | 🟡 Mapa osobno dla tekstu i dla kodu? | C: mapa tylko kodu — doprecyzowane w K26: 75% kodu + 25% tekstu |
| @phase-2:K19 | 🟢 Nazwa folderu `phase-pomysl` | A (→ `phase-2`, zrobione 2026-10-30) |
| @phase-2:K20 | 🟡 Klasyfikator do oceny generacji w etapie 3 | C: skupiamy się na kodzie; raport, czy i jakie klasyfikatory mają sens; pamiętać o metrykach jakości i sprawności kodu → `raport-3-ocena-kodu.md`, K32–K36 |
| @phase-2:K21 | 🔴 Warstwa do zmniejszania w etapie 4 | C: kolejna mało ważna + jedna z początku + jedna z końca → 14, 2, 26 |
| @phase-2:K22 | 🟢 GUI: zatwierdzenie planu a następny plan (@L14) | „chyba B” (wpis pod planem metryk zapisał się w innym planie) |
| @phase-2:K23 | 🟡 Dłuższy trening zmniejszonej warstwy | A (16 epok; lr 5e-5 i 2e-4) |
| @phase-2:K24 | 🟢 Progi rodzajów neuronów w etapie 3 | A |
| @phase-2:K25 | 🔴 Co ma najlepiej przetrwać zmniejszanie | A (programowanie) |
| @phase-2:K26 | 🔴 Na jakich danych liczymy mapę ważności i naprawę warstw | A (75% kodu + 25% tekstu) |
| @phase-2:K27 | 🟡 Jak mierzymy, czy model dalej dobrze programuje | A (KL/perpleksja na kodzie + HumanEval/MBPP w kluczowych punktach) |
| @phase-2:K28 | 🟡 Które języki programowania | B (tylko Python) |
| @phase-2:K29 | 🟢 Model, który zmniejszamy | B (Qwen3-0.6B-Base + model do kodu ~0,5B jako odniesienie) |
| @phase-2:K30 | 🔴 Następny krok na GPU w sprawie kodu | A (uruchomione 2026-10-30 po zgodzie autora w czacie, @T012) |
