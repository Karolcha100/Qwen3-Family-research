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

### [L18] Obliczenia pod nieobecność autora (Python)

- @phase-2:K23: 16 epok zamiast 4 zmniejsza KL warstwy 13 tylko o ~5% (wpis 11:30 w @T012, wykres `AGENTS/phases/phase-2/figures/k23-dlugi-trening-13.png`);
- dane Python + C4 (75/25, rozłączne), mapa kodu, etap 4 dla warstw 13 (start z mapy kodu i ze starej mapy), 2, 14, 26: raport `AGENTS/phases/phase-2/etap-4b-kod.md`;
- poprawiony błąd celu treningu dla warstwy 26 (końcowa normalizacja w `hidden_states`), warstwa 26 policzona ponownie;
- pytania K37 (cel treningu) i K38 (waga kodu w mapie): `AGENTS/phases/phase-2/agents-issues-6.md`.

*2026-10-30 13:01 — Claude Opus 5.5*

### [L19] Przygotowanie obliczeń K31–K38

- starty: `activation-rms`, `random`, `merged` (k-średnie na wagach + nowe $W_{down}$), `code-only` (K38); cel na wyjściu modelu `--objective output` (`src/qwen_compression/training.py`); testy (40 przechodzi);
- aktywacje neuronów warstwy 13 prawie niezależne (mediana największego podobieństwa 0,13), stąd łączenie przez wagi;
- kontener `qwen-code-sandbox` (EvalPlus 0.3.1), rozwiązania wzorcowe: HumanEval 163/164, MBPP 99,7% / 99,5%;
- pytanie K39 (uruchomienie kolejki): `AGENTS/phases/phase-2/agents-issues-7.md`; opis: @T013.

*2026-10-30 14:14 — Claude Opus 5.5*

### [L21] Pasek postępu obliczeń

- `scripts/run_queue.py` uruchamia kroki z `queue.json` i zapisuje `AGENTS/postep-obliczen.json` (poza gitem); skrypty zgłaszają postęp przez `qwen_compression.progress.report_progress`;
- `agents_board/model.py`: `progress_summary` (procent według czasu, tempo skończonych kroków, ułamek bieżącego kroku, brak sygnału > 3 min), `/api/progress`, pasek w nagłówku odświeżany co 15 s; 4 testy;
- kolejka K31–K38 przeniesiona do `results/phase2/code/queue.json` z szacunkami (razem 167 min); szacunki w @T013.

*2026-10-30 14:27 — Claude Opus 5.5*

### [L20] Kolejka obliczeń K31–K38 + dodatkowa kolejka

- kolejka K31–K38 14:31–16:38 (~127 min wobec szacunku 167), dodatkowa 16:38–17:13 (testy kodu dla mapy 100% kod i warstwy 26, cel na wyjściu z krokiem $1 \cdot 10^{-5}$);
- oryginał EvalPlus 36,9 (raport Qwen3 36,23); warstwa 13 −40% → −2,7 pkt, warstwa 26 −40% → 0 pkt mimo 3× większej KL;
- start z mapy najlepszy także po 16 epokach (losowy +64% KL), scalanie neuronów gorsze niż usuwanie; cel na wyjściu: warstwa 26 −18% KL, warstwa 13 słabszy od starego celu;
- raport `AGENTS/phases/phase-2/etap-4c-k31-k38.md`, pytania K40–K43 `AGENTS/phases/phase-2/agents-issues-8.md`; zmierzone czasy w `procedury.md`, sekcja 10.

*2026-10-30 17:13 — Claude Opus 5.5*

### [L22] Porównanie z oryginałem, mapa, pass@k

- raport `AGENTS/phases/phase-2/porownanie-z-oryginalem.md` (liczby zadań, zyski/straty z testem McNemara, KL, perpleksja, sprawność, analiza statyczna; `scripts/phase2_code_comparison.py`);
- wizualizacja mapy i przewidywany koszt warstw (`scripts/phase2_code_map_figures.py`): najtańsze 20–25; wykres kroku uczenia K37; oba w dyskusji `etap-4c-k31-k38.md`;
- pass@k: `--samples-per-task` w `scripts/phase2_code_generate.py`, pass@1–3 w `scripts/phase2_code_evaluate.py`, `src/qwen_compression/code_metrics.py` + test; sprawdzone w kontenerze na dwóch zestawach odpowiedzi; pytania K44, K45 (`agents-issues-9.md`).

*2026-10-30 18:39 — Claude Opus 5.5*

### [L23] K43, K44 (część; kolejka warstw czeka na K47)

- K43: raport `AGENTS/phases/phase-2/k43-zgodnosc-tokenu.md` (zgodność tokenu na odpowiedziach oryginału na zadania EvalPlus odtwarza kolejność testów kodu), pytanie K46;
- K44: raport `AGENTS/phases/phase-2/k44-pass-at-k.md` (`scripts/phase2_code_pass_at_k_analysis.py`): w. 13 −40% w 1 próbie 133,4 wobec 134,0 zadań „+”, w 3 próbach 217,1 wobec 225,5, różnice w granicach przypadku;
- noc: testy MBPP w kontenerze zawiesiły się (brak pamięci przy 8 testach naraz), kolejka warstw nie ruszyła; testy powtórzone z `--parallel 2`, w kolejce warstw `timeout 1800` i `--parallel 4`, pułapka 25; pytanie K47.

*2026-11-01 13:09 — Claude Opus 5.5*

### [L25] Zamknięcie raportów Phase 2 i raport zbiorczy

- 12 raportów Phase 2 zamkniętych (status „zamknięty … na prośbę autora @T018” + wpis 🔒, jak przycisk w GUI); sprawdzone w `agents_board.model`: 12 zamkniętych, 1 otwarty;
- `AGENTS/phases/phase-2/raport-zbiorczy-phase-2.md`: chronologia etapów, metoda plan → teraz ze wzorami, najważniejsze wyniki z wykresami, co dalej (kolejka warstw K47 = B, pytania o wiele warstw i koniec Phase 2).

*2026-11-01 14:28 — Claude Opus 5.5*

### [L23] [L24] Kolejka warstw, K46 B, K44 (koniec)

- kolejka 14:59–17:51 (zgoda @T019): warstwy 10, 15, 17, 18, 20–25 przy −20/−40% przepisem @T017; testy kodu −40%: w. 24 200 zadań „+” (= oryginał), w. 17 194, w. 20 192, w. 10 189;
- K46 B: odpowiedzi oryginału na 510 zadań spoza testów; zgodność na nich przewiduje testy tak samo dobrze jak na zadaniach testowych (korelacja rang 0,86 na 8 modelach; KL na Pythonie 0,48); przewidywanie zapisane przed testami (commit 626e771) trafiło poza zamianą w. 17/20 (2 zadania);
- raport `AGENTS/phases/phase-2/warstwy-10-25.md`, pytania K48–K50 `AGENTS/phases/phase-2/agents-issues-11.md`; wykres zgodności z dwoma panelami (`scripts/phase2_code_layers_analysis.py`).

*2026-11-01 17:55 — Claude Opus 5.5*
