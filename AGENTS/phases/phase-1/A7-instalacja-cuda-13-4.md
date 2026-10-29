# A7 — instalacja CUDA 13.4 (sam toolkit)

*2026-10-29 15:00 — Claude Opus 5.5*

## Co masz zrobić

Zacznij **po @A6**. Pobierz instalator, uruchom kroki 1–4 i wklej w raporcie pod @A7 wynik kroku 4. Instalujemy **tylko toolkit**; sterownik zostaje z RPM Fusion.

## Kroki

**1. Pobranie instalatora.** Na stronie https://developer.nvidia.com/cuda-downloads wybierz: Linux → x86_64 → Fedora → 44 → **runfile (local)**. Strona poda polecenie `wget` z dokładną nazwą pliku. Uruchom je w `~/Pobrane` (lub dowolnym katalogu). Plik ma kilka GB.

Uwaga: wersja musi być **13.4.x**, nie 13.2 (błąd dający bełkot na niskobitowych kwantach). Jeśli domyślnie jest nowsza wersja, napisz w raporcie, zanim zainstalujesz. Sprawdzę, czy sterownik 615 ją obsłuży.

**2. Instalacja samego toolkitu** (bez sterownika). `--toolkit` instaluje do `/usr/local/cuda-13.4` i tworzy dowiązanie `/usr/local/cuda`.

```bash
cd ~/Pobrane
sudo sh cuda_13.4.*_linux.run --silent --toolkit
```

**3. Ścieżki: `PATH` w zsh i biblioteki w systemie.**

```bash
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.zshrc
echo /usr/local/cuda/lib64 | sudo tee /etc/ld.so.conf.d/cuda.conf
sudo ldconfig
exec zsh
```

**4. Sprawdzenie.** Wynik wklej w raporcie:

```bash
nvcc --version
ls -l /usr/local/cuda
ldconfig -p | grep -c libcudart
```

Oczekiwany wynik: `nvcc` pokazuje `release 13.4`, `/usr/local/cuda` wskazuje na `cuda-13.4`, a licznik `libcudart` jest większy od 0.

Jeśli instalator odmówi przez kompilator (GCC 16), wklej komunikat w raporcie. Nie dodawaj `--override` bez konsultacji.
