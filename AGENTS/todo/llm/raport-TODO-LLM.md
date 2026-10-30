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

---

### [L13] Phase 2 — etapy 1–4 (noc 29/30.10)

- etap 1 (pilot, float32, warstwy 2/13/25, 4096 tokenów): `AGENTS/phases/phase-pomysl/etap-1-pilot.md`; bf16 = szum, $\mathrm{KL} \propto \delta^2$, 4096 tokenów daje ranking o zgodności tylko 0,51;
- etap 2 (mapa 86 016 neuronów): przesiew Fishera na 131 tys. tokenów (64 × 64 próbki, 21 min) + pomiar dokładny 15% neuronów w 25 warstwach (2 h); zgodność przesiewu z pomiarem dokładnym 0,96–0,99: `etap-2-mapa.md`;
- etap 3 (rodzaje neuronów, bez klasyfikatora): `etap-3-rodzaje-neuronow.md`;
- etap 4 (warstwa 13, −5…−40%): `etap-4-jedna-warstwa.md`; −40% neuronów → perpleksja 12,660 → 12,725, wybór przesiewem lepszy niż po średniej aktywacji;
- sprawdzone: 34 testy, ruff, pyright; liczby w raportach sprawdzone z plikami `results/phase2/`;
- zostało: ocena klasyfikatorem (@phase-pomysl:K20), decyzje K16–K24 (`agents-issues-3.md`).

*2026-10-30 04:32 — Claude Opus 5.5*

---

### [L15] Raporty Phase 2: wzory, tabele, wykresy, zakładka „Raporty” w GUI

- przyczyny: obrazki miały ścieżki względne (`figures/…`), więc GUI nie pokazywał żadnego wykresu; `|` we wzorach w tabelach dzielił komórki; `$$` wcięte w liście sklejały się z tekstem;
- raporty `AGENTS/phases/phase-pomysl/etap-1…4`: poprawione ścieżki i wzory, 6 nowych wykresów (`scripts/phase2_report_figures.py`, z gotowych wyników, bez GPU), linia `**Status raportu:** do przeczytania`;
- GUI: raporty z dyskusją i przyciskiem „🔒 Zakończ dyskusję” (`agents_board/model.py`, `server.py`, `static/index.html`), test `test_reports_discussion_and_closing`; komórki tabel nie dzielą się już na `|` we wzorach ani na `\|`; `$$` przerywa listę i akapit;
- sprawdzone: 19 testów GUI, ruff, pyright; zrzut ekranu GUI (Firefox bez okna); parser GUI na 4 raportach: 99 wzorów, 0 luźnych `$`, 17 tabel bez przesunięć.

*2026-10-30 09:43 — Claude Opus 5.5*

---

### [L14] GUI: wpis w dyskusji planu trafił do innego planu

- przebieg z plików: 21:36 zatwierdzony plan Phase 2, 21:37 plan metryk, 21:38 wpis w planie Phase 2; autor: „chyba B” (pisał pod planem metryk) (@phase-2:K22);
- w kodzie nie ma ścieżki, w której formularz zapisuje do innego pliku niż pozycja w oknie głównym. Najbardziej prawdopodobne: okno główne wróciło do planu Phase 2 (◀ / boczny przycisk myszy) albo plan metryk był tylko przypięty obok, a pole „Wpis w dyskusji planu” nie mówiło, do którego planu pisze;
- poprawka w `agents_board/static/index.html`: etykieta pola podaje tytuł planu lub raportu, a komunikat po zapisie podaje plik, do którego trafił wpis.

*2026-10-30 11:12 — Claude Opus 5.5*

---

### [L16] Folder `phase-pomysl` → `phase-2`

- `git mv`; odwołania zmienione w plikach fazy, planie faz, zadaniach, pamięci i skryptach. Stare wpisy (wątki, briefingi, Koniec, raporty-logi) bez zmian;
- GUI: alias `phase-pomysl` → `phase-2` dla wzmianek `@phase-pomysl:K…`, ścieżek i obrazków w starych wpisach.

*2026-10-30 11:12 — Claude Opus 5.5*

---

### [L17] Raport: jak oceniać kod

- `AGENTS/phases/phase-2/raport-3-ocena-kodu.md`: testy (HumanEval, MBPP, EvalPlus; odniesienie z raportu Qwen3: EvalPlus 36,23, MBPP 36,60), klasyfikatory (AceCodeRM-7B, model-sędzia), analiza statyczna, sprawność (model i kod, Mercury), bezpieczeństwo uruchamiania;
- pytania K31–K36: `AGENTS/phases/phase-2/agents-issues-5.md`.

*2026-10-30 11:12 — Claude Opus 5.5*
