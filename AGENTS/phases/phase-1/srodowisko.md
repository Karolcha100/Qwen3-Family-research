# Phase 1 — raport środowiska

*2026-10-29 20:47 — Claude Opus 5.5*

## Co masz zrobić

Nic. Phase 1 jest skończona: wszystkie warunki z sekcji „Koniec fazy, gdy” w `AGENTS/phases/phase-1/plan.md` są spełnione (tabela niżej). Ten plik to ściągawka: wersje, gdzie co leży, jak odtworzyć.

## Warunki końca fazy

| Warunek | Stan |
|---|---|
| `nvcc --version` → 13.4, stara CUDA usunięta | ✅ 13.4.92; CUDA 12 usunięta (@A6, @A7) |
| llama.cpp z CUDA działa na Qwen3-0.6B (GGUF) | ✅ `llama-bench`, `llama-perplexity` na GPU |
| PyTorch na GPU generuje tekst i liczy perplexity | ✅ |
| środowisko da się odtworzyć z plików w repo | ✅ `pyproject.toml`, `uv.lock`, `.python-version` |
| raport środowiska | ✅ ten plik |

## Wersje

| Składnik | Wersja |
|---|---|
| GPU / sterownik | RTX 4070 SUPER 12 GB (sm_89) / NVIDIA 615.78.08 (RPM Fusion) |
| CUDA toolkit | 13.4.92, `/usr/local/cuda-13.4`, dowiązanie `/usr/local/cuda` |
| GCC | 16.2.1 (nvcc 13.4 go akceptuje) |
| Python | 3.14.8 (systemowy, `.python-version`) |
| uv | 0.12.24 |
| PyTorch | 2.15.0+cu134 (indeks `download.pytorch.org/whl/cu134`) |
| transformers / accelerate / datasets / safetensors / lm-eval | 5.22.0 / 1.15.0 / 5.1.0 / 0.8.0 / 0.4.13 |
| ruff / pyright / pytest | 0.17.3 / 1.1.414 / 9.2.0 |
| llama.cpp | commit `eb4e244be` (2026-10-29), build 12001, `~/llama.cpp/build/bin` |

## Wyniki testów dymnych (@L4)

Pliki: `results/phase1-smoke-test.jsonl` (PyTorch, skrypt `scripts/smoke_test_torch.py`), `results/phase1-smoke-test-llamacpp.jsonl`.

| Test | Wynik |
|---|---|
| mnożenie macierzy BF16 4096×4096 | 67,6 TFLOPS |
| generacja Qwen3-0.6B (instrukcyjny, bez myślenia, greedy) | sensowna odpowiedź, 96 tok/s (transformers, jeden strumień) |
| perplexity WikiText-2, PyTorch, okna 2048 bez nakładania (@phase-0:K9 = A) | **Base 12,67**, instrukcyjny 20,97 (146 okien, 299 078 tokenów, 10,6 s, szczyt VRAM 4,2 GiB) |
| llama.cpp, Base BF16 (1,11 GiB) | przetwarzanie 32 690 tok/s, generacja 306 tok/s, perplexity 11,20 ± 0,08 |
| llama.cpp, Base Q4_K_M (373 MiB) | przetwarzanie 38 195 tok/s, generacja 566 tok/s, perplexity 12,17 ± 0,09 (+8,6% względem BF16) |

Uwagi:
- wersja instrukcyjna ma wyższą perplexity niż Base, tak jak przewidywał raport `AGENTS/phases/phase-0/A2-base-czy-instrukcyjna.md`: post-trening odsuwa model od „zwykłego” tekstu;
- perplexity z llama.cpp (11,20) jest niższa niż z PyTorcha (12,67) dla tego samego modelu, bo `llama-perplexity` liczy tylko drugą połowę każdego okna (więcej kontekstu na token). **Liczb z tych dwóch narzędzi nie porównujemy ze sobą**;
- generacja w transformers (96 tok/s) jest ~3× wolniejsza niż w llama.cpp (306 tok/s). Przy masowym generowaniu odpowiedzi do oceny trzeba będzie wybrać szybszy silnik.

## Gdzie co leży

| Co | Gdzie |
|---|---|
| środowisko Pythona | `.venv/` w projekcie (6 GB, poza gitem) |
| modele Hugging Face | `~/.cache/huggingface/hub/` (Qwen3-0.6B-Base, Qwen3-0.6B) |
| pliki GGUF, dane tekstowe | `~/qwen3-checkpoints/gguf/`, `~/qwen3-checkpoints/data/` (poza repo, @phase-0:K30 = B) |

## Jak odtworzyć

```bash
uv sync
uv run python scripts/smoke_test_torch.py
git -C ~/llama.cpp checkout eb4e244be && cmake -B ~/llama.cpp/build -S ~/llama.cpp -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=89 -DGGML_NATIVE=ON && cmake --build ~/llama.cpp/build --config Release -j 16
```

Konwersja do GGUF wymaga dodatkowo `sentencepiece`: `uv run --with sentencepiece python ~/llama.cpp/convert_hf_to_gguf.py <katalog modelu> --outtype bf16 --outfile <plik>.gguf`.

## Przygody

Przerwa w Wi-Fi autora w trakcie pobierania zawiesiła pierwszy test (połączenie wisiało bez błędu, a wagi modelu Base nie pobrały się do końca). Ponowne uruchomienie z `HF_HUB_DOWNLOAD_TIMEOUT=60` przeszło bez problemu.
