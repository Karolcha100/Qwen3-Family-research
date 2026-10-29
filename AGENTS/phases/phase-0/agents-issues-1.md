# Phase 0 — pytania startowe (runda 1)

*2026-10-29 13:05 — Claude Opus 5.5*

## Co masz zrobić

To decyzje na start projektu: organizacja, środowisko, sposób pracy i protokół pomiarów. Każde pytanie ma rekomendację, więc jeśli się zgadzasz, wystarczy wpisać w polu Decyzja „rek” albo literę opcji. 🔴 blokuje start, 🟡 ważne, 🟢 drobne. Pytania K1–K3 pochodzą z @T001, K13 z @T002.

---

### K1. 🔴 Repozytorium git

- **Problem:** katalog projektu nie jest repozytorium git. Instrukcja wymaga commita po każdej sesji, a agent czyta zmiany przez `git status` i `git diff`. Bez gita tego nie zrobię.
- **Opcje:**
  - **A** — `git init` lokalnie, bez remote, `.gitignore` (modele, cache, `__pycache__`, duże wyniki), pierwszy commit z obecnym stanem;
  - **B** — A plus prywatne repozytorium na GitHubie (push robisz Ty albo ja na Twoje polecenie);
  - **C** — bez gita (wtedy pomijam commity, a zmiany śledzę po datach plików — mniej pewne).
- **Rekomendacja:** A. Remote można dodać w każdej chwili.
- **Decyzja:** Wybieram opcje B, prywatne repozytorium pod nazwą "Qwen3-Family-research", dodaj do .gitignore, pycache i te inne rzeczy.

  Pushujesz po każdej mojej odpowiedzi w chacie do ciebie (o ile coś się zmieniło)

### K2. 🔴 Plan faz do zatwierdzenia

- **Problem:** `AGENTS/plan/phases-plans.md` i `AGENTS/plan/phases-description.md` są puste. Czy mam je rozpisać jako plan do zatwierdzenia, według szkicu niżej?
- **Szkic:**
  - **Phase 1 — środowisko:** CUDA 13.4, llama.cpp, środowisko Pythona (PyTorch, transformers, lm-eval), test na Qwen3-0.6B;
  - **Phase 2 — baseline ewaluacji:** BF16 i RTN na 0.6B: perplexity (WikiText-2, C4), KL względem BF16, kilka zadań lm-eval; jeden wspólny skrypt do pomiarów;
  - **Phase 3 — kwantyzacja:** GPTQ, AWQ, HQQ, potem rotacje (QuIP#, SpinQuant);
  - **Phase 4 — pruning:** magnitude, Wanda, SparseGPT, 2:4;
  - **Phase 5 — niskie rzędy i leczenie:** SVD, ASVD/SVD-LLM, LoRA z destylacją; potem skalowanie na 1.7B, 4B i 8B.
- **Opcje:**
  - **A** — rozpisz według szkicu;
  - **B** — rozpisz, ale ze zmianą kolejności (napisz jaką, np. pruning przed kwantyzacją);
  - **C** — jeszcze nie, najpierw sama Phase 1.
- **Rekomendacja:** A. Kwantyzacja jest najlepiej opisana w literaturze, więc łatwo sprawdzić, czy wyniki się zgadzają, a GPTQ uczy mechanizmu (Hessian, kompensacja błędu), z którego korzysta potem SparseGPT.
- **Decyzja:** Opcja C, jeszcze nie i najpierw sama Phase 1 (potem rozpiszę co chcę w następnych fazach robić)

### K3. 🟡 Instalacja z `sudo` jako zadania autora

- **Problem:** usunięcie CUDA 12.x, instalację CUDA 13.4 i budowę llama.cpp robisz Ty, bo wymagają `sudo`.
- **Opcje:**
  - **A** — dodam je jako zadania A w WAŻNE, z poleceniami z `local-llm-conversation.md`; po każdym kroku wklejasz wynik w raporcie (np. `nvcc --version`), a ja go sprawdzam;
  - **B** — robisz je bez zadań i dajesz znać w wątku, gdy skończysz.
- **Rekomendacja:** A, bo każdy krok ma wynik do sprawdzenia (`rpm -qa | grep -i cuda`, `nvcc --version`, `llama-cli --version`).
- **Decyzja:** A

### K4. 🟡 Menedżer środowiska Pythona

- **Problem:** jak instalować pakiety (PyTorch, transformers, lm-eval…). Obecnie w systemie nie ma ani `uv`, ani `conda`.
- **Opcje:**
  - **A** — `uv` (`pyproject.toml` + `uv.lock`): szybki, zapisuje dokładne wersje, sam pobiera wybraną wersję Pythona;
  - **B** — `python -m venv` + `pip` + `requirements.txt`: nic nowego do instalowania, ale bez lockfile;
  - **C** — conda/mamba: wygodna dla CUDA, ale ciężka i miesza się z pip.
- **Rekomendacja:** A. Lockfile pozwala odtworzyć dokładnie te same wersje bibliotek po miesiącach, co przy porównywaniu wyników jest ważne.
- **Decyzja:** A

### K5. 🟡 Wersja Pythona

- **Problem:** chcesz najnowszą wersję. Fedora ma Pythona 3.14.8. Python 3.15 wyszedł niedawno, a PyTorch i biblioteki z kernelami CUDA zwykle dostają wheele dla nowej wersji z kilkumiesięcznym opóźnieniem.
- **Opcje:**
  - **A** — 3.14 (pewne wheele dla wszystkiego);
  - **B** — 3.15, jeśli PyTorch, transformers i lm-eval mają już wheele (sprawdzę przed instalacją); jeśli nie, wracam do 3.14;
  - **C** — 3.15 i kompilujemy brakujące pakiety ze źródeł.
- **Rekomendacja:** B. Dostajesz najnowszą wersję, kiedy tylko się da, bez kompilowania PyTorcha.
- **Decyzja:** Opcja A

### K6. 🔴 Własne implementacje czy gotowe biblioteki

- **Problem:** projekt jest do nauki. Metody (RTN, GPTQ, AWQ, Wanda, SparseGPT, SVD) można napisać samemu albo wziąć z bibliotek (GPTQModel, llm-compressor, AutoAWQ, HQQ).
- **Opcje:**
  - **A** — wszystko samemu: najwięcej nauki, ale trudno być pewnym, że implementacja jest poprawna;
  - **B** — tylko biblioteki: szybko, ale mniej się uczymy;
  - **C** — główne metody piszemy sami (krótko, bez optymalizacji), a wynik każdej porównujemy z biblioteką albo z liczbami z artykułu; metody trudne inżynieryjnie (QuIP#, AQLM, kernele) bierzemy z bibliotek.
- **Rekomendacja:** C. Własny kod uczy, a biblioteka sprawdza, czy działa poprawnie.
- **Decyzja:** Opcja B, aczkolwiek pragnę zaznaczyć ze sam wybiorę metody.

### K7. 🟡 Qwen3 Base czy wersja instrukcyjna

- **Problem:** każdy rozmiar Qwen3 ma wersję `-Base` (sam pretrening) i wersję bez sufiksu (po post-treningu, z trybem myślenia). Perplexity i lm-eval liczy się zwykle na Base, a evalplus i ocena odpowiedzi czatu wymagają wersji instrukcyjnej.
- **Opcje:**
  - **A** — Base do perplexity, KL i lm-eval, instrukcyjna (z wyłączonym myśleniem) do evalplus i oceny odpowiedzi;
  - **B** — wszędzie instrukcyjna (prościej, jeden model, ale perplexity mniej porównywalne z literaturą);
  - **C** — wszędzie Base (bez evalplus i oceny czatu).
- **Rekomendacja:** A. Koszt jest mały, bo kompresja tą samą metodą to drugie uruchomienie tego samego skryptu.
- **Decyzja:** ⏳ w toku → @A2 (wstępnie: Potrzebuję raportu o tym czym jest base, perplexity, jak to wpływa na rzeczy, czym jest wersja bez sufiksu etc.)

### K8. 🟡 Dane kalibracyjne

- **Problem:** GPTQ, AWQ, Wanda, SparseGPT i ASVD potrzebują próbki tekstu, żeby zmierzyć aktywacje. Wybór wpływa na wyniki, więc ustalamy go raz dla wszystkich metod.
- **Opcje:**
  - **A** — C4: 128 sekwencji po 2048 tokenów, stałe ziarno (standard z artykułów GPTQ i Wanda, łatwe porównanie);
  - **B** — WikiText-2 (ryzyko zawyżenia wyniku perplexity na WikiText-2);
  - **C** — mieszanka C4 i kodu (lepiej chroni programowanie, ale trudniej porównać z literaturą).
- **Rekomendacja:** A jako domyślne; C później jako osobny eksperyment („czy kalibracja na kodzie chroni evalplus?”).
- **Decyzja:** ⏳ w toku → @A3 (wstępnie: W jaki sposób wybór wpływa na wyniki, o co tutaj chodzi, potrzebuję raportu)

### K9. 🟡 Protokół perplexity

- **Problem:** perplexity zależy od długości kontekstu i podziału danych. Bez stałego protokołu liczby z różnych dni nie będą porównywalne.
- **Opcje:**
  - **A** — kontekst 2048, okna bez nakładania; WikiText-2 cały test, C4 256 sekwencji z walidacji (standard GPTQ/Wanda);
  - **B** — kontekst 4096 (bliżej realnego użycia Qwen3, ale dłużej i mniej porównywalne);
  - **C** — A plus dodatkowy pomiar na 4096 dla najlepszych konfiguracji.
- **Rekomendacja:** A, a C dopiero przy wynikach końcowych.
- **Decyzja:** ⏳ w toku → @A4 (wstępnie: Nie wiem co to perplexity, nie wiem co zmieniają odpowiedzi, proszę o raport)

### K10. 🟡 Kto i kiedy uruchamia obliczenia na GPU

- **Problem:** dużo grasz, a GPU jest jedno. Eksperyment na 0.6B trwa minuty, a na 8B z offloadem nawet godziny i zajmuje VRAM oraz RAM.
- **Opcje:**
  - **A** — krótkie zadania (do ~15 min) agent uruchamia sam, dłuższe tylko po Twojej zgodzie w zadaniu A albo w pytaniu;
  - **B** — agent pisze kod i polecenia, a uruchamiasz zawsze Ty;
  - **C** — agent uruchamia wszystko sam, kiedy pracuje.
- **Rekomendacja:** A. Przed każdym uruchomieniem sprawdzam `nvidia-smi` i nie startuję, jeśli GPU jest zajęte przez grę.
- **Decyzja:** Generalnie wolę B, z zastrzeżeniem że raczej ja powiem kiedy Agent ma uruchomić a nie że wpisuję sam komendy.

### K11. 🟢 Zapis wyników

- **Problem:** gdzie i jak zapisywać wyniki eksperymentów (metoda, bity, rozmiar, metryki, czas, wersje bibliotek).
- **Opcje:**
  - **A** — jeden wiersz JSON na eksperyment w `results/*.jsonl` (w gicie) plus wykresy `.png` w folderze fazy;
  - **B** — MLflow lokalnie (UI w przeglądarce, ale więcej narzędzi);
  - **C** — Weights & Biases (chmura).
- **Rekomendacja:** A. Prosto, wersjonowane w gicie, a skrypt łatwo z tego robi tabele i wykresy dla GUI.
- **Decyzja:**

### K12. 🟢 Struktura kodu

- **Problem:** jak ułożyć kod badawczy w repozytorium.
- **Opcje:**
  - **A** — pakiet `src/qwen_compression/` (`quantization/`, `pruning/`, `low_rank/`, `evaluation/`, `data/`), cienkie skrypty CLI w `scripts/`, testy w `tests/` obok testów GUI;
  - **B** — płaskie skrypty w `experiments/`, jeden plik na eksperyment;
  - **C** — notebooki Jupyter.
- **Rekomendacja:** A. Metody korzystają ze wspólnych części (ładowanie modelu, kalibracja, pomiar), więc płaskie skrypty szybko by się powtarzały. Jeśli wolisz inną nazwę pakietu, wpisz ją w decyzji.
- **Decyzja:**

### K13. 🟡 Model-sędzia do oceny odpowiedzi Qwen3 (z @T002)

- **Problem:** chcesz lokalny model, który ocenia, czy odpowiedź Qwen3 (np. po kompresji) jest dobra. Moja opinia jest w @T002; tu jest sama decyzja.
- **Opcje:**
  - **A** — jeszcze nie: najpierw metryki automatyczne (KL, lm-eval, testy evalplus), a sędziego dodajemy przy ocenie generowania tekstu (po Phase 2);
  - **B** — generatywny sędzia z rubryką, np. Prometheus 2 (7B), przez llama.cpp w GGUF Q8 (~8 GB): daje ocenę 1–5 z uzasadnieniem;
  - **C** — model nagrody, np. Skywork-Reward-V2 (warianty od 0.6B do 8B): daje jedną liczbę, jest szybki, ale bez uzasadnienia;
  - **D** — duży ogólny model jako sędzia (np. 14B w Q4): elastyczny, ale wolniejszy i z ryzykiem, że model z rodziny Qwen faworyzuje odpowiedzi Qwen.
- **Rekomendacja:** A, a potem porównanie B i C na ~50 parach odpowiedzi, które ocenisz ręcznie. Wybieramy sędziego, który najbardziej zgadza się z Tobą.
- **Decyzja:** Myślę że pójdziemy w opcję C, przy czym to trzeba jeszcze dopracować.

### K14. 🟢 Narzędzia jakości kodu

- **Problem:** kod ma być typowany, krótki i bez komentarzy. Narzędzia mogą to sprawdzać automatycznie.
- **Opcje:**
  - **A** — `ruff` (lint + format) + `pyright` (typy) + `pytest` z małymi testami (np. błąd kwantyzacji/dekwantyzacji w znanych granicach);
  - **B** — A, ale `mypy` zamiast `pyright`;
  - **C** — bez narzędzi.
- **Rekomendacja:** A. Pyright lepiej rozumie najnowszą składnię typów.
- **Decyzja:**

### K15. 🟢 Notatki do nauki

- **Problem:** projekt jest do nauki, więc wyniki to nie wszystko. Pytanie, czy ma być też wyjaśnienie, jak działa każda metoda.
- **Opcje:**
  - **A** — każda metoda dostaje krótką notatkę w folderze fazy (idea, wzór w TeX, co mierzymy, co wyszło i dlaczego), widoczną w GUI;
  - **B** — tylko raporty z wynikami;
  - **C** — notatki tylko na Twoją prośbę.
- **Rekomendacja:** A.
- **Decyzja:**

### K16. 🟢 Folder na pytania startowe

- **Problem:** pytania organizacyjne nie należą do żadnej fazy badań, więc dałem je do `AGENTS/phases/phase-0/` (Phase 0 = start i organizacja).
- **Opcje:**
  - **A** — zostaje `phase-0` na pytania ogólne/organizacyjne;
  - **B** — przenieś do `phase-1` (środowisko).
- **Rekomendacja:** A.
- **Decyzja:**
