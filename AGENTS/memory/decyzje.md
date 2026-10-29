# Indeks decyzji autora

Wszystkie pytania z `AGENTS/phases/*/agents-issues-*.md` w jednej tabeli: tytuł i decyzja dosłownie z pola **Decyzja**. Plik jest **generowany** poleceniem z `AGENTS/memory/procedury.md` (sekcja „Indeks decyzji”), więc nie edytuje się go ręcznie. Odświeżany na końcu każdej sesji. Gdy indeks i plik źródłowy się różnią, wygrywa plik źródłowy.

*Wygenerowano: 2026-10-29 16:56 — Claude Opus 5.5*

---

| Pytanie | Tytuł | Decyzja |
|---|---|---|
| @phase-0:K1 | 🔴 Repozytorium git | Wybieram opcje B, prywatne repozytorium pod nazwą "Qwen3-Family-research", dodaj do .gitignore, pycache i te inne rzeczy. Pushujesz po każdej mojej odpowiedzi w chacie do ciebie (o ile coś się zmieniło) |
| @phase-0:K2 | 🔴 Plan faz do zatwierdzenia | Opcja C, jeszcze nie i najpierw sama Phase 1 (potem rozpiszę co chcę w następnych fazach robić) |
| @phase-0:K3 | 🟡 Instalacja z `sudo` jako zadania autora | A |
| @phase-0:K4 | 🟡 Menedżer środowiska Pythona | A |
| @phase-0:K5 | 🟡 Wersja Pythona | Opcja A |
| @phase-0:K6 | 🔴 Własne implementacje czy gotowe biblioteki | Opcja B, aczkolwiek pragnę zaznaczyć ze sam wybiorę metody. |
| @phase-0:K7 | 🟡 Qwen3 Base czy wersja instrukcyjna | ⏳ w toku → @A2 (wstępnie: Potrzebuję raportu o tym czym jest base, perplexity, jak to wpływa na rzeczy, czym jest wersja bez sufiksu etc.) |
| @phase-0:K8 | 🟡 Dane kalibracyjne | ⏳ w toku → @A3 (wstępnie: W jaki sposób wybór wpływa na wyniki, o co tutaj chodzi, potrzebuję raportu) |
| @phase-0:K9 | 🟡 Protokół perplexity | ⏳ w toku → @A4 (wstępnie: Nie wiem co to perplexity, nie wiem co zmieniają odpowiedzi, proszę o raport) |
| @phase-0:K10 | 🟡 Kto i kiedy uruchamia obliczenia na GPU | Generalnie wolę B, z zastrzeżeniem że raczej ja powiem kiedy Agent ma uruchomić a nie że wpisuję sam komendy. |
| @phase-0:K11 | 🟢 Zapis wyników | A |
| @phase-0:K12 | 🟢 Struktura kodu | Dobra, ale chwilka, ja jeszcze nie napisałem tobie jakie rzeczy będziemy robić. Generalnie pomysł A jest spoko, ale zauważ że jeszcze nie wiesz jakie metody będziemy robić. |
| @phase-0:K13 | 🟡 Model-sędzia do oceny odpowiedzi Qwen3 (z @T002) | Myślę że pójdziemy w opcję C, przy czym to trzeba jeszcze dopracować. |
| @phase-0:K14 | 🟢 Narzędzia jakości kodu | ⏳ w toku → @A9 (wstępnie: Czy to potrzebne jeżeli będziemy stosować tamte benchmarki? - Jeżeli benchmarki tego nie uwzględniają to A) |
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
| @phase-0:K36 | 🟡 (ponowione K19) Jak zamienić wynik modelu nagrody na 0–100 | ⏳ w toku → @A10 (wstępnie: A co sądzisz o użyciu czegoś w rodzaju ELO Score? Poza tym podoba mi się twoja rekomendacja) |
| @phase-0:K37 | 🟡 Limit długości odpowiedzi z myśleniem | B |
| @phase-0:K38 | 🟢 Czy klasyfikator widzi myślenie modelu | A |
| @phase-0:K39 | 🟡 Pytania w stylu IFEval w naszych 200 pytaniach a K28 | A, chociaż proszę o jakiś wątek wyjaśniający mi co to zmienia |
| @phase-0:K40 | 🟢 Zgodność z odpowiedzią wzorcową | A |
| @phase-0:K41 | 🟡 Skąd wziąć 200 pytań | C |
| @phase-0:K42 | 🟢 Druga tura pytań MT-Bench | B |
| @phase-0:K43 | 🟢 Polecenia agenta: notatki czy mały skrypt | — (czeka) |
