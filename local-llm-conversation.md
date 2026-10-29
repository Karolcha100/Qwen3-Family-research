# Badania nad kompresją LLM na rodzinie Qwen3

Podsumowanie rozmowy z 27–29.10.2026. Plik służy jako kontekst do kontynuacji pracy w Claude Code. Cel: nauka for fun.

## Stan projektu

- [x] Diagnoza systemu
- [ ] Usunięcie CUDA 12.8 / 12.9
- [ ] Instalacja CUDA 13.4
- [ ] Kompilacja llama.cpp

## Sprzęt i system (zdiagnozowane)

| Element | Stan | Uwagi |
|---|---|---|
| GPU | RTX 4070 SUPER 12 GB (AD104, compute capability 8.9) | pulpit zajmuje ~730 MiB VRAM, monitor zostaje na NVIDII (dużo grania) |
| iGPU | Radeon 610M, aktywne | nie przenosimy na nie pulpitu |
| CPU | Ryzen 7 9700X (8C/16T, Zen 5, 1 CCD) | realny odczyt RAM ~60–65 GB/s |
| RAM | 30 GiB DDR5-6000, EXPO aktywne | w spoczynku ~8,8 GiB zajęte (Brave ~2 GB, Steam ~1,5 GB, DiscoverNotifier 0,4 GB) |
| Swap | 255 GiB | |
| Dysk | 184 GB wolne (+~34 GB po usunięciu CUDA 12.x) | modele w domyślnych katalogach cache |
| OS | Fedora 44, KDE Plasma (Wayland), powłoka **zsh** | zmienne środowiskowe do `~/.zshrc` |
| Kompilator | GCC 16.2.1, glibc 2.43 | CUDA 12.x tego nie obsłuży → potrzebna CUDA 13.4 |
| Sterownik | NVIDIA 615.78.08 z RPM Fusion | OK, obsługuje CUDA ≤ 13.4, nie ruszamy |
| CUDA | 12.8 i 12.9 z lokalnych repo dla Fedory 41, nieaktywne (brak `nvcc` w PATH) | do usunięcia, nic innego z nich nie korzysta |

## Instalacja (plan, jeszcze niewykonany)

### 1. Usunięcie CUDA 12.8 / 12.9

```bash
sudo dnf remove 'cuda-*-12-8*' 'cuda-*-12-9*' cuda-toolkit-config-common cuda-toolkit-12-config-common
sudo rm -rf /usr/local/cuda-12.8 /usr/local/cuda-12.9 /var/cuda-repo-fedora41-12-8-local /var/cuda-repo-fedora41-12-9-local
sudo rm -f /usr/local/cuda /usr/local/cuda-12
rpm -qa | grep -i cuda
```

Po usunięciu na liście mają zostać tylko `xorg-x11-drv-nvidia-cuda*` (sterownik z RPM Fusion).

### 2. CUDA 13.4

CUDA 13.4 oficjalnie wspiera Fedorę 44 i GCC 16. Pobrać runfile (local) z developer.nvidia.com/cuda-downloads (Linux → x86_64 → Fedora → 44) i zainstalować **tylko toolkit**:

```bash
sudo sh cuda_13.4.1_*_linux.run --silent --toolkit
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.zshrc
echo /usr/local/cuda/lib64 | sudo tee /etc/ld.so.conf.d/cuda.conf && sudo ldconfig
exec zsh
nvcc --version
```

Uwaga: CUDA 13.2 ma błąd dający bełkot na niskobitowych kwantach. Nie używać.

### 3. Kompilacja llama.cpp

```bash
sudo dnf install git cmake gcc-c++ openssl-devel libcurl-devel
git clone https://github.com/ggml-org/llama.cpp ~/llama.cpp && cd ~/llama.cpp
cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=89 -DGGML_NATIVE=ON
cmake --build build --config Release -j 16
```

Jeśli nvcc odrzuci GCC 16, użyj pakietu kompatybilności GCC 15 (nazwę binarki sprawdź przez `ls /usr/bin/g++*`):

```bash
sudo dnf install gcc15-c++
cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=89 -DGGML_NATIVE=ON -DCMAKE_CUDA_HOST_COMPILER=g++-15
```

Aktualizacja: `git pull && cmake --build build --config Release -j 16`.

## Model bazowy: rodzina Qwen3

Dlaczego Qwen3, a nie Qwen3.5:
- Qwen3 to standardowy transformer. Wszystkie metody (GPTQ, AWQ, SparseGPT, Wanda, HQQ, QuIP#) działają od ręki, łatwo o baseline'y i porównanie z literaturą.
- Qwen3.5 (hybryda z Gated DeltaNet) jest trudniejszy: warstw DeltaNet nie należy kwantyzować, SpinQuant jest niekompatybilny, potrzebne są osobne kernele. To słabo zbadany temat, więc potencjalnie ciekawy na później.

| Model | BF16 | Zastosowanie |
|---|---|---|
| Qwen3-0.6B | ~1,2 GB | szybka iteracja (minuty na eksperyment) |
| Qwen3-1.7B | ~3,4 GB | sprawdzenie, czy efekt się utrzymuje |
| Qwen3-4B | ~8 GB | mieści się w VRAM |
| Qwen3-8B | ~16 GB | nie mieści się w VRAM: kompresja warstwa po warstwie (model w RAM), ewaluacja z offloadem przez `accelerate` |

## Ewaluacja

- Perplexity: WikiText-2, C4
- KL divergence względem modelu BF16 (czulsza niż perplexity)
- lm-evaluation-harness (ARC, HellaSwag, PIQA, zero-shot)
- evalplus (HumanEval+, MBPP+) do sprawdzania zdolności programowania

## Rodzaje kompresji

**Kwantyzacja** (mniej bitów na wagę). Główny problem to outliery.
- RTN: skala z min/max w grupie, zaokrąglenie. Baseline.
- GPTQ: kwantyzuje kolumny po kolei i kompensuje błąd w pozostałych (Hessian z danych kalibracyjnych).
- AWQ: chroni kanały mnożone przez duże aktywacje, skalując je przed kwantyzacją.
- HQQ: bez kalibracji, optymalizuje skale i zera pod błąd rekonstrukcji.
- Rotacje (QuIP#, SpinQuant): mnożenie przez macierz ortogonalną (np. Hadamarda) rozmazuje outliery.
- SmoothQuant: W8A8, przenosi trudność z aktywacji na wagi.
- Kwantyzacja wektorowa (AQLM, QuIP#): indeksy do książki kodowej, ~2 bity na wagę.

**Pruning** (zerowanie wag)
- Niestrukturalny: najlepsza jakość, brak przyspieszenia na GPU.
- 2:4 półstrukturalny: sprzętowe wsparcie na RTX 4070S.
- Strukturalny (neurony, głowy, warstwy): pewne przyspieszenie, największa strata.
- Kryteria: magnitude (słabe w LLM), Wanda (|W| × ‖X‖), SparseGPT (kompensacja błędu jak w GPTQ).

**Rozkłady niskiego rzędu**: W ≈ A·B (SVD). Opłaca się, gdy r < mn/(m+n). Naiwne SVD szybko psuje model. ASVD i SVD-LLM ważą rozkład statystykami aktywacji.

**Destylacja**: uczeń naśladuje nauczyciela (KL na wyjściach). Na 12 GB głównie do „leczenia” po kompresji (LoRA). Pokrewne: QAT.

## Preferencje dot. kodu

- Python w najnowszej wersji i najnowszej składni, z typami.
- Kod po angielsku, bez komentarzy, krótki, pełne nazwy zmiennych (bez skrótów).

## Źródła

- https://docs.nvidia.com/cuda/archive/13.4.1/cuda-toolkit-release-notes/index.html (CUDA 13.4, GCC 16)
- https://docs.nvidia.com/cuda/cuda-installation-guide-linux/ (Fedora 44 wspierana)
- https://forums.developer.nvidia.com/t/nvcc-13-4-rejects-conforming-libstdc-string-with-g-16/382852 (bug tylko w C++23)
- https://packages.fedoraproject.org/pkgs/gcc15/gcc15-c++/fedora-44.html (gcc15-c++)
- https://allthings.how/?p=800 (błąd CUDA 13.2)
- https://huggingface.co/88plug/Qwen3.6-35B-A3B-W4A16 (problemy z kwantyzacją warstw Gated DeltaNet)
