# Phase 1 — plan: środowisko

*2026-10-29 13:30 — Claude Opus 5.5*

**Status planu:** zatwierdzony (2026-10-29 19:39, Autor)
## Co masz zrobić

Phase 1 ma dać działające środowisko: Qwen3-0.6B działa na GPU w PyTorchu i w llama.cpp, a my znamy wersje wszystkich narzędzi. Przeczytaj plan i zatwierdź (✅ Zatwierdzam plan) albo napisz w dyskusji, co zmienić. Szczegóły zależą od otwartych pytań @phase-0:K3 (zadania A na instalację), @phase-0:K4 (uv czy conda), @phase-0:K5 (Python), @phase-0:K10 (kto uruchamia GPU), @phase-0:K12 (struktura kodu) i @phase-0:K14 (narzędzia jakości). Plan działa przy każdej odpowiedzi, a w krokach zaznaczyłem, co się wtedy zmienia.

## Cel

Środowisko, w którym Phase 2 (pomiary baseline) może ruszyć bez dalszych instalacji.

## Czego nie robimy

Żadnych metod kompresji ani protokołu ewaluacji; to Phase 2 i dalsze fazy, które rozpiszesz Ty (@phase-0:K2). Nie zmieniamy sterownika NVIDIA ani konfiguracji pulpitu.

## Kroki

| # | Krok | Kto | Wynik do sprawdzenia |
|---|---|---|---|
| 1 | Usunięcie CUDA 12.8 / 12.9 — @A6 | Ty (`sudo`) | `rpm -qa \| grep -i cuda` pokazuje tylko `xorg-x11-drv-nvidia-cuda*` |
| 2 | CUDA 13.4: runfile, tylko toolkit, `PATH` w `~/.zshrc`, `ldconfig` — @A7 | Ty (`sudo`) | `nvcc --version` → 13.4 |
| 3 | Pakiety do budowy + `uv`: `git cmake gcc-c++ openssl-devel libcurl-devel uv` — @A8 | Ty (`sudo dnf`) | `uv --version` |
| 4 | Budowa llama.cpp w `~/llama.cpp` (CUDA, `sm_89`); przy błędzie GCC 16 → `gcc15-c++` | ja (bez `sudo`) | `llama-cli --version`, `llama-bench` na GPU |
| 5 | Środowisko Pythona: **uv** (`pyproject.toml` + `uv.lock`), **Python 3.14** (@phase-0:K4, K5 = A); PyTorch z wheelem CUDA zgodnym ze sterownikiem 615 | ja | `torch.cuda.is_available()`, mnożenie BF16 na GPU |
| 6 | Biblioteki: `transformers`, `accelerate`, `datasets`, `safetensors`, `lm-eval`; narzędzia jakości według K14 | ja | import bez błędów |
| 7 | Test dymny PyTorch: Qwen3-0.6B (Base i/lub instrukcyjny według @A2) → generacja + szybka perplexity na fragmencie WikiText-2 | ja, **po Twoim „uruchom”** (@phase-0:K10) | sensowny tekst, perplexity w rozsądnym zakresie |
| 8 | Test dymny llama.cpp: konwersja Qwen3-0.6B do GGUF (BF16 i Q4_K_M) → `llama-bench`, `llama-perplexity` | ja, **po Twoim „uruchom”** | tokeny/s, perplexity Q4 nieco wyższa niż BF16 |
| 9 | Raport środowiska `AGENTS/phases/phase-1/srodowisko.md`: wersje (sterownik, CUDA, GCC, Python, torch, transformers, llama.cpp commit), zajętość VRAM, polecenia do odtworzenia | ja | raport w GUI |

Kroki 5–7 nie zależą od 1–4, bo PyTorch ma własne biblioteki CUDA (@T003). Kroki 5–6 zrobię po zatwierdzeniu planu i po @A8 (potrzebne `uv`), niezależnie od CUDA. Czy instalacje i pobieranie modeli wymagają Twojego „uruchom”, rozstrzyga @phase-0:K33. Kroki 7–8 (GPU) uruchamiam tylko na Twoje polecenie.

Modele i dane trafiają do domyślnego cache Hugging Face (`~/.cache/huggingface`); nic dużego nie trafia do repozytorium.

## Koniec fazy, gdy

- `nvcc --version` → 13.4, a stara CUDA usunięta;
- llama.cpp z CUDA działa na Qwen3-0.6B (GGUF);
- PyTorch na GPU generuje tekst z Qwen3-0.6B i liczy perplexity;
- środowisko da się odtworzyć z plików w repo;
- jest raport środowiska.

## Dyskusja

---
---
---

Zmiany w planie po Twoich decyzjach z 14:58:
- kroki 1–3 mają zadania @A6, @A7, @A8 z poleceniami (@phase-0:K3 = A). W @A6 dodałem 42 pakiety CUDA 12 (`libcublas-12-8`…), które pomijało polecenie z `local-llm-conversation.md`;
- krok 3: doszło `uv`; krok 5: uv + Python 3.14 (@phase-0:K4, K5);
- kroki 7–8 (GPU) tylko po Twoim „uruchom” (@phase-0:K10); co z instalacjami i pobieraniem: @phase-0:K33.

Plan nadal czeka na zatwierdzenie (✅ Zatwierdzam plan) albo uwagi.

*2026-10-29 15:03 — Claude Opus 5.5*

---
---
---

✅ Plan zatwierdzony. Zgoda

*2026-10-29 19:39 — Autor*

---
---
---

**Phase 1 skończona.** Wszystkie warunki końca fazy spełnione, raport: `AGENTS/phases/phase-1/srodowisko.md`. Kroki 1–3: @A6, @A7, @A8; 4: @L3; 5–6: @L2; 7–8: @L4; 9: @L5.

*2026-10-29 20:48 — Claude Opus 5.5*

---
---
---
