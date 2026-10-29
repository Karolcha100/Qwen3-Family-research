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
