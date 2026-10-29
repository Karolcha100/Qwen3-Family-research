# T003 · Uwagi do planu instalacji

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

## Co masz zrobić

Nic do decyzji, to tylko informacja. Uwaga przeniesiona z @T001. Decyzje o instalacji: @phase-0:K3 (zadania A), @phase-0:K4 (uv), @phase-0:K5 (Python).

**Systemowa CUDA a PyTorch.** PyTorch z pip ma własne biblioteki CUDA (wheel `cu13x`). Potrzebuje tylko sterownika, a sterownik 615.78.08 obsługuje CUDA do 13.4. Dlatego:
- systemowa CUDA 13.4 (`nvcc`) jest potrzebna tylko do budowy llama.cpp i do kompilowania własnych kerneli (np. niektórych implementacji AWQ albo QuIP#);
- eksperymenty w Pythonie (RTN, GPTQ, Wanda, SparseGPT, SVD, perplexity, KL) mogą ruszyć równolegle z instalacją CUDA albo nawet przed nią;
- wersję wheela PyTorcha dobiorę w Phase 1 do sterownika 615; nie może wymagać CUDA nowszej niż 13.4.

**GCC 16 i nvcc 13.4.** Błąd z wątku na forum NVIDII dotyczy tylko kompilacji w C++23. llama.cpp kompiluje się w C++17, więc nie powinno go to dotyczyć. Pakiet `gcc15-c++` jest planem awaryjnym, gdyby `nvcc` mimo to odrzucił GCC 16.

**CUDA 13.2** omijamy (bełkot na niskobitowych kwantach). Po instalacji sprawdzimy `nvcc --version`, czy to na pewno 13.4.

*2026-10-29 13:05 — Claude Opus 5.5*

---
---
---

A co sądzisz o użyciu condy do tego?

*2026-10-29 13:22 — Autor*

---
---
---

## Co masz zrobić

To opinia, decyzja jest w @phase-0:K4. Conda to tam opcja **C**. Jeśli wybierasz condę, wpisz w K4 „C — miniconda, env z conda-forge, torch z pip”. Jeśli zostajesz przy mojej rekomendacji, wpisz „A”.

Sprawdziłem: masz **Minicondę 26.3.2** w `~/miniconda3` (solver libmamba, kanał `defaults`, środowiska `datascience`, `kinesinquest`, `r_env`). Jak włączyć ją w zsh: @T004.

**Plusy condy w tym projekcie:**
- **masz ją już** i ją znasz;
- **potrafi zainstalować CUDA toolkit bez `sudo`**, w środowisku (`conda install -c conda-forge cuda-nvcc cuda-toolkit`). To realna alternatywa dla systemowej CUDA 13.4 przy budowie llama.cpp i kompilacji kerneli; środowisko można skasować bez śladu w systemie;
- łatwo mieć kilka wersji Pythona obok siebie.

**Minusy:**
- **PyTorch nie wydaje już paczek conda** (od wersji 2.6 tylko pip). W środowisku conda i tak instalujemy `torch`, `transformers` i `lm-eval` przez `pip`, a mieszanie conda i pip to klasyczne źródło trudnych błędów (dwie kopie tej samej biblioteki);
- **brak lockfile w praktyce:** `conda env export` zapisuje wersje, ale odtworzenie środowiska po miesiącach bywa zawodne. `uv.lock` odtwarza je dokładnie, co przy porównywaniu wyników z różnych tygodni ma znaczenie;
- kanał `defaults` (repo.anaconda.com) ma warunki licencyjne Anaconda. Dla Ciebie prywatnie to zwykle bez znaczenia, ale lepiej używać `conda-forge`;
- wolniejsza i cięższa niż uv (Twoja `~/miniconda3` zajmuje 20 GB).

**Rekomendacja:** **uv** do pakietów Pythona (K4 = A). Condę warto zostawić jako **zapas na CUDA toolkit bez `sudo`**, gdyby instalacja systemowej CUDA 13.4 sprawiała problemy. Jeśli wolisz jedno narzędzie, które znasz, conda też zadziała: env z Pythonem z conda-forge, a wszystko inne przez `pip` w tym środowisku. Wtedy pilnuję, żeby nie mieszać źródeł paczek.

*2026-10-29 13:30 — Claude Opus 5.5*

---
---
---

Okej, zostańmy przy twojej rekomendacji (uv + systemowa CUDA 13.4).

Masz coś do dodania?

*2026-10-29 14:08 — Autor*

---
---
---

## Co masz zrobić

Wpisz w @phase-0:K4 decyzję „A” (uv), bo w polu Decyzja ciągle pusto, a wolę mieć to w pytaniu niż tylko w wątku. Zostają też @phase-0:K3 (czy instalacje z `sudo` dostają zadania A) i @phase-0:K5 (wersja Pythona). Po decyzji w K3 dam polecenia w zadaniach.

Mam do dodania kilka rzeczy:

**1. Instalacja uv: z repo Fedory.** `uv` 0.12.24 jest w `updates` Fedory 44, więc nie trzeba skryptu `curl | sh`:

```bash
sudo dnf install uv
uv --version
```

Wchodzi to w zadania z K3, razem z CUDA.

**2. Conda nie będzie przeszkadzać.** Sprawdziłem: `auto_activate` jest wyłączone, więc terminal nie startuje w `(base)`. To ważne, bo uv w aktywnym środowisku conda potrafi użyć jego Pythona zamiast `.venv` projektu. Jeśli kiedyś zrobisz `conda activate`, przed pracą w tym projekcie zrób `conda deactivate`.

**3. PyTorch nie potrzebuje systemowej CUDA.** Wheel PyTorcha z CUDA 13.x działa ze sterownikiem 615. Systemowa CUDA 13.4 jest potrzebna do llama.cpp i kerneli, a nie do PyTorcha. Dlatego środowisko Pythona (kroki 5–7 planu Phase 1) mogę postawić, zanim zainstalujesz CUDA. Czeka tylko na zatwierdzenie planu i K5.

**4. Kolejność wpisów w `~/.zshrc`.** Linia `export PATH=/usr/local/cuda/bin:$PATH` z instalacji CUDA może stać przed blokiem conda albo po nim; conda nie dodaje własnego `nvcc`, dopóki go w niej nie zainstalujesz. Bez znaczenia.

**5. Miejsce na dysku.** Qwen3 0.6B–8B w BF16 to ~29 GB w cache Hugging Face (`~/.cache/huggingface`), do tego warianty GGUF i skompresowane checkpointy. Przy 184 GB wolnego (+34 GB po usunięciu CUDA 12.x) starczy. Modele zostają w domyślnym cache, tak jak ustaliliśmy w `local-llm-conversation.md`. Otwarte jest tylko to, czy zapisujemy skompresowane checkpointy, bo to one mogą zająć dużo miejsca: @phase-0:K30.

*2026-10-29 14:09 — Claude Opus 5.5*

---
---
---

Dobra, czyli mogę zamykać ten wątek czy jest coś jeszcze co uważasz za warte do przedyskutowania w nim?

*2026-10-29 15:12 — Autor*

---
---
---

## Co masz zrobić

Możesz zamknąć ten wątek 🔒. Nie mam nic więcej do dyskusji. Wszystko, co z niego wynikło, ma już swoje miejsce:
- instalacje: zadania @A6 (usunięcie CUDA 12), @A7 (CUDA 13.4), @A8 (pakiety + uv);
- uv i Python 3.14: decyzje @phase-0:K4 i @phase-0:K5, wpisane w plan Phase 1 (`AGENTS/phases/phase-1/plan.md`);
- checkpointy na dysku: @phase-0:K30 = B.

*2026-10-29 15:45 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-10-29 15:54 — Autor*

---
---
---
