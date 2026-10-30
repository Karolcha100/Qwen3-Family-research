# Główny pomysł — pytania (runda 4): model, który ma dobrze programować

*2026-10-30 10:41 — Claude Opus 5.5*

## Co masz zrobić

Pytania wynikają z Twojego wpisu w dyskusji raportu `AGENTS/phases/phase-pomysl/etap-2-mapa.md` (najbardziej zależy Ci na tym, żeby Qwen dobrze programował) i z mojej odpowiedzi tamże. Najważniejsze są **K25** (co ma najlepiej przetrwać zmniejszanie) i **K26** (na jakich danych liczymy mapę i naprawę). Odpowiedź na K26 rozstrzyga też wcześniejsze **K18** (`agents-issues-3.md`): możesz tam wpisać „patrz K26”. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek” albo litera.

---

### K25. 🔴 Co ma najlepiej przetrwać zmniejszanie

- **Problem:** do tej pory chroniliśmy „sens modelu” mierzony na mieszance 75% zwykłego tekstu i 25% kodu (@phase-pomysl:K11). Neurony ważne dla kodu to jednak w dużej mierze inne neurony niż ważne dla tekstu. Każdy wybór proporcji jest więc wyborem, co model straci mniej.
- **Opcje:**
  - **A** — przede wszystkim programowanie; zwykły tekst tylko w takim stopniu, żeby model rozumiał polecenia, komentarze i opisy w kodzie;
  - **B** — programowanie i zwykły tekst po równo;
  - **C** — jak dotąd: model ogólny, głównie zwykły tekst.
- **Rekomendacja:** A, jeśli dobrze rozumiem Twój wpis. To Twój cel, więc decyzja jest Twoja.
- **Decyzja:**

### K26. 🔴 Na jakich danych liczymy mapę ważności i naprawę warstw

- **Problem:** to samo zestawienie danych wybiera, które neurony wyciąć (mapa z etapu 2), i uczy pozostałe neurony przejmować ich pracę (najmniejsze kwadraty i trening z etapu 4). Sprawdziłem na gotowych wynikach (wykres i liczby w dyskusji `etap-2-mapa.md`): obecna mieszanka przy wycinaniu 20% neuronów szkodzi kodowi ~1,75× bardziej, niż to konieczne. Liczby to przewidywana szkoda; mapa liczona z połowy sekwencji, szkoda sprawdzona na drugiej połowie.

| Mapa | szkoda dla kodu | szkoda dla tekstu |
|---|---|---|
| obecna: 75% tekst / 25% kod | 1,75× | 1,23× |
| pół na pół | 1,23× | 1,48× |
| 75% kod / 25% tekst | 1,07× | 1,79× |
| tylko kod | 1,00× | 3,89× |

(1,00× = najmniejsza możliwa szkoda dla danego rodzaju tekstu; wycięte 20% neuronów w każdej warstwie)
- **Opcje:**
  - **A** — 75% kodu + 25% zwykłego tekstu (dla K25 = A);
  - **B** — pół na pół (dla K25 = B);
  - **C** — tylko kod;
  - **D** — dwie osobne mapy, a chronimy neurony ważne dla **którejkolwiek** z nich (K18 B); tego jeszcze nie policzyłem, wymaga tylko analizy na CPU.
- **Rekomendacja:** A, jeśli w K25 wybierzesz A. Sam kod (C) uszkadza zwykły tekst prawie 4×, a model do programowania musi rozumieć polecenia napisane zwykłym językiem.
- **Decyzja:**

### K27. 🟡 Jak mierzymy, czy model dalej dobrze programuje

- **Problem:** KL na kodzie mówi, jak bardzo zmieniły się przewidywania następnego tokenu. Nie mówi wprost, czy model nadal pisze **działający** kod. Do tego służą zestawy zadań z testami: model pisze funkcję, a testy sprawdzają, czy działa. Najczęściej używa się HumanEval (164 zadania w Pythonie) i MBPP (500 zadań testowych w Pythonie). Wynik to odsetek zadań rozwiązanych za pierwszym razem. Uwaga: to oznacza uruchamianie kodu napisanego przez model, więc trzeba to robić w odizolowanym środowisku (np. kontener bez sieci).
- **Opcje:**
  - **A** — przy każdym kroku KL i perpleksja na odłożonym kodzie (tanie), a HumanEval i MBPP w kluczowych punktach (oryginał, wybrane stopnie zmniejszenia);
  - **B** — tylko KL i perpleksja na kodzie;
  - **C** — tylko HumanEval i MBPP.
- **Rekomendacja:** A. KL jest czuła i tania, a zestawy zadań mówią, co naprawdę zostało z umiejętności. Model 0,6B rozwiązuje tylko część zadań, więc małe różnice w tych zestawach będą szumem. Dlatego oba sposoby razem.
- **Decyzja:**

### K28. 🟡 Które języki programowania

- **Problem:** obecny kod w danych to 7 języków z GitHuba (zbiór codeparrot/github-code-clean): Python, JavaScript, Java, C++, C, C#, PHP, wymieszane po równo. Mapa ważności chroni to, na czym ją liczymy. Jeśli używasz głównie jednego-dwóch języków, mapa z tych języków ochroni je lepiej, kosztem pozostałych.
- **Opcje:**
  - **A** — zostaje 7 języków po równo;
  - **B** — tylko Python (HumanEval i MBPP też są w Pythonie);
  - **C** — wybrane języki (wpisz, w czym programujesz).
- **Rekomendacja:** C: napisz, w czym programujesz. Bez tego A.
- **Decyzja:**

### K29. 🟢 Model, który zmniejszamy

- **Problem:** Qwen3-0.6B-Base to model ogólny, a cała Phase 2 jest policzona na nim. Istnieją też małe modele Qwen trenowane głównie na kodzie (np. Qwen2.5-Coder-0.5B). Jeśli celem jest jak najlepsze programowanie, warto przynajmniej wiedzieć, jak wypada model do kodu podobnej wielkości.
- **Opcje:**
  - **A** — zostajemy przy Qwen3-0.6B-Base;
  - **B** — zostajemy przy Qwen3-0.6B-Base, a model do kodu ~0,5B mierzymy tylko jako punkt odniesienia (te same testy z K27, bez zmniejszania; pobranie ~1 GB);
  - **C** — przechodzimy na model do kodu i powtarzamy na nim etapy.
- **Rekomendacja:** B. Metoda i wyniki zostają, a porównanie pokaże, czy zmniejszony Qwen3 dorównuje modelowi zrobionemu od początku do kodu.
- **Decyzja:**

### K30. 🔴 Następny krok na GPU w sprawie kodu

- **Problem:** po decyzjach K25–K28 można sprawdzić, czy wycinanie według mapy „pod kod” rzeczywiście chroni kod przy prawdziwym zmniejszaniu warstwy, a nie tylko w przewidywaniu.
- **Opcje:**
  - **A** — (1) mapa z kodu na 48 nowych sekwencjach kodu (~15–20 min GPU, plus pobranie kodu); (2) nowy zbiór do naprawy według K26 (1 mln tokenów); (3) powtórka etapu 4 dla warstwy 13 z wyborem według starej i nowej mapy, ocena osobno na kodzie i na tekście (~30 min GPU);
  - **B** — tylko krok (3) ze starą mapą: osobna ocena na kodzie i tekście istniejących wariantów etapu 4 (~30 min GPU); pokaże, ile kod traci dziś;
  - **C** — poczekać, aż rozstrzygniemy K16–K24.
- **Rekomendacja:** A, po Twoim „uruchom”. Część CPU (wybór danych, kod skryptów) mogę przygotować od razu po decyzjach.
- **Decyzja:**
