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
