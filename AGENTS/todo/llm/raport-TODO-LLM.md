# Raport agentów — wykonanie zadań L…

Jeden wpis na zadanie: co zrobiono, gdzie są pliki, jak sprawdzono, co zostało. Format: `AGENTS/todo/llm/INSTRUKCJA.md`.

---

### [L1] Katalog metod kompresji

- plik `AGENTS/phases/phase-0/katalog-metod.md` (plan do opiniowania): 6 grup (kwantyzacja wag, rotacje i aktywacje, pruning, niskie rzędy, leczenie, KV cache), dla każdej metody idea + wzór, dane kalibracyjne, biblioteka, obsługa Qwen3, wykonalność na 12 GB, czego uczy; na końcu propozycja zestawu startowego (decyzja autora);
- obsługa Qwen3 oznaczona ✅/⚠️ według wiedzy agenta (do połowy 2026), więc przed wyborem metody trzeba ją potwierdzić przy instalacji;
- niczego nie uruchamiano.

*2026-10-29 16:23 — Claude Opus 5.5*

---

### [L6] Ranking Elo w planie metryk

- dodałem sekcję D w `AGENTS/phases/phase-0/plan-metryki-oceny.md`: ranking Bradleya–Terry'ego na skali Elo, BF16 = 1000, wzór z opisem słownym, przeliczenie metryki 16 na $\Delta R$; wpis w dyskusji planu;
- sprawdzone, że GUI dalej widzi plan; niczego nie uruchamiano.

*2026-10-29 19:33 — Claude Opus 5.5*

---

### [L3] Budowa llama.cpp z CUDA

- kod: `~/llama.cpp`, commit `eb4e244be` (2026-10-29), build 12001, wersja `0.8.0-dev`;
- konfiguracja: `cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=89 -DGGML_NATIVE=ON`, kompilacja `-j 16` z `nice -n 19`, ok. 4 min, kod wyjścia 0;
- **nvcc 13.4.92 przyjął GCC 16.2.1** bez kompilatora pomocniczego, więc `gcc15-c++` jest niepotrzebne;
- `libggml-cuda.so` linkuje `libcudart.so.13`, `libcublas.so.13` i `libcublasLt.so.13` z `/usr/local/cuda-13.4`;
- 90 ostrzeżeń kompilatora, nieszkodliwych: operacje bitowe na różnych typach wyliczeniowych (64) i przestarzałe `std::filesystem::u8path` w GCC 16 (22);
- interfejs webowy `llama-server`: pobranie z wydania b12001 nie powiodło się, cmake przełączył się na „latest”. Nie używamy go w badaniach;
- **GPU jeszcze nie testowane** (`llama-bench`, `--list-devices`): to część @L4, po „uruchom” autora;
- aktualizacja: `git -C ~/llama.cpp pull && cmake --build ~/llama.cpp/build --config Release -j 16`.

*2026-10-29 20:17 — Claude Opus 5.5*

---

### [L2] Środowisko Pythona (Phase 1 kroki 5–6)

- `pyproject.toml` (bez pakietu i struktury pod metody, `package = false`; @phase-0:K12), `.python-version` = 3.14, `uv.lock` (116 pakietów), środowisko w `.venv` (6 GB, w `.gitignore`);
- PyTorch z indeksu `download.pytorch.org/whl/cu134`: **torch 2.15.0+cu134**. Dostępne były cu130, cu132 i cu134; cu132 pominięte przez błąd CUDA 13.2, a cu134 pasuje do sterownika 615 (CUDA ≤ 13.4);
- wersje: transformers 5.22.0, accelerate 1.15.0, datasets 5.1.0, safetensors 0.8.0, lm-eval 0.4.13, ruff 0.17.3, pyright 1.1.414 (z `pyright[nodejs]`, bo zwykły nie mógł pobrać node.js), pytest 9.2.0;
- PyTorch widzi GPU: 1 urządzenie, compute capability (8, 9). Wheel nie ma osobnego kodu `sm_89`, ale kod `sm_86` działa na Adzie (ta sama generacja 8.x);
- bez obliczeń na GPU: mnożenie BF16 i testy modelu to @L4 po „uruchom”.

*2026-10-29 20:22 — Claude Opus 5.5*

---

### [L4] Testy dymne na GPU (Phase 1 kroki 7–8)

- „uruchom” od autora: raport pod @A8, 2026-10-29 20:26;
- PyTorch: `scripts/smoke_test_torch.py` → `results/phase1-smoke-test.jsonl`: matmul BF16 67,6 TFLOPS; generacja (Qwen3-0.6B, bez myślenia) poprawna, 96 tok/s; perplexity WikiText-2 (okna 2048 bez nakładania): Base **12,67**, instrukcyjny **20,97**, 10,6 s na 299 tys. tokenów (~28 tys. tok/s), szczyt VRAM 4,2 GiB; kod przechodzi `ruff` i `pyright`;
- llama.cpp: Base → GGUF BF16 (`--with sentencepiece`) i Q4_K_M w `~/qwen3-checkpoints/gguf/` → `results/phase1-smoke-test-llamacpp.jsonl`: generacja 306 / 566 tok/s, perplexity 11,20 / 12,17 (llama-perplexity liczy drugą połowę okna, więc liczby nieporównywalne z PyTorchem);
- problem: przerwa w Wi-Fi autora zawiesiła pierwsze pobieranie (wiszące połączenie, niepełne wagi modelu Base, GGUF bez tensorów). Proces zatrzymany i ponowiony z `HF_HUB_DOWNLOAD_TIMEOUT=60`. Pułapka 14.

*2026-10-29 20:48 — Claude Opus 5.5*

---

### [L5] Raport środowiska (Phase 1 krok 9)

- `AGENTS/phases/phase-1/srodowisko.md`: warunki końca fazy (wszystkie spełnione), wersje, wyniki testów, gdzie co leży, jak odtworzyć.

*2026-10-29 20:48 — Claude Opus 5.5*

---

### [L12] Plan etapów głównego pomysłu

- `AGENTS/phases/phase-pomysl/plan-phase-2.md` (do zatwierdzenia): etapy 1–4 według @phase-pomysl:K9 (pilot A, A dla całego modelu, B rodzaje neuronów i wykresy, C na jednej warstwie), z decyzjami K1–K9;
- nowe pytania K10–K15 (`AGENTS/phases/phase-pomysl/agents-issues-2.md`): numer fazy, tekst pomiarowy, warstwy pilota, liczba tokenów, stopnie zmniejszenia, układ kodu.

*2026-10-29 21:13 — Claude Opus 5.5*

---
