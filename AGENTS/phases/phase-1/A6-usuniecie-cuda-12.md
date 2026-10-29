# A6 — usunięcie CUDA 12.8 i 12.9

*2026-10-29 15:00 — Claude Opus 5.5*

## Co masz zrobić

Uruchom polecenia z kroków 1–4 po kolei. W kroku 1 **przejrzyj listę, zanim potwierdzisz** (`y`). Na koniec wklej w raporcie pod @A6 wynik kroku 4 (albo napisz „zrobione, zostały tylko xorg-x11-drv-nvidia-cuda*”). Zwolni się ~34 GB.

## Co sprawdziłem na Twoim systemie

- Zainstalowane są dwa komplety CUDA (12.8 i 12.9) z lokalnych repozytoriów dla Fedory 41: 75 pakietów `cuda-*`, a do tego **42 pakiety bez „cuda” w nazwie** (`libcublas-12-8`, `libcufft-12-9`, `libnpp…`, `libnvjpeg…`, `gds-tools-12-8`…). Polecenie z `local-llm-conversation.md` by je pominęło, więc dodałem je niżej.
- Katalogi: `/usr/local/cuda-12.8` (6,8 GB), `/usr/local/cuda-12.9` (15 GB), `/var/cuda-repo-fedora41-12-8-local` (5,6 GB), `/var/cuda-repo-fedora41-12-9-local` (6,4 GB).
- Dowiązania `/usr/local/cuda` i `/usr/local/cuda-12` prowadzą przez `/etc/alternatives` do 12.9.
- `~/.bashrc` (linie 13 i 27) dopisuje CUDA 12.8 do `PATH` i `LD_LIBRARY_PATH`. Działa to tylko w bashu (używasz zsh), ale po usunięciu CUDA te linie wskazują donikąd.
- Sterownik (`xorg-x11-drv-nvidia-cuda*` z RPM Fusion) **zostaje**. Żaden wzorzec niżej do niego nie pasuje.

## Kroki

**1. Usunięcie pakietów.** dnf pokaże listę i zapyta o zgodę. Sprawdziłem wzorce na Twojej liście pakietów: obejmują dokładnie **117 pakietów**, wszystkie z CUDA 12, i nic poza nimi. Na liście mają być tylko pakiety z `12-8` albo `12-9` w nazwie, `cuda-toolkit-config-common` i `cuda-toolkit-12-config-common`. Jeśli zobaczysz cokolwiek z `nvidia` albo `xorg`, przerwij (`N`) i napisz w raporcie.

**Dopisane 2026-10-29 19:46 (po @T008):** dnf pokaże **123 pakiety**, nie 117. Doliczy 6 „nieużywanych zależności”: `nsight-compute-2025.1.0`, `nsight-compute-2025.2.1`, `nsight-systems-2025.1.3` (profilery z CUDA 12), `java-25-openjdk` (graficzna Java, którą zainstalowały narzędzia CUDA) oraz `xorg-x11-fonts-Type1` i `ttmkfdir` (czcionki tej Javy). To w porządku. `java-25-openjdk-headless` zostaje. `xorg-x11-fonts-Type1` to czcionki, nie sterownik, więc mimo „xorg” w nazwie można kontynuować.

```bash
sudo dnf remove 'cuda-*-12-8*' 'cuda-*-12-9*' 'libcu*-12-[89]' 'libnpp*-12-[89]' 'libnv*-12-[89]' 'gds-tools-12-[89]' cuda-toolkit-config-common cuda-toolkit-12-config-common
```

**2. Usunięcie pozostałych katalogów i dowiązań** (dnf nie usuwa plików, które nie należą do pakietów).

```bash
sudo rm -rf /usr/local/cuda-12.8 /usr/local/cuda-12.9 /var/cuda-repo-fedora41-12-8-local /var/cuda-repo-fedora41-12-9-local
sudo rm -f /usr/local/cuda /usr/local/cuda-12
sudo ldconfig
```

**3. Sprzątanie `~/.bashrc`** (opcjonalnie, dotyczy tylko basha). Polecenie usuwa dwie linie z CUDA 12.8 i zostawia kopię `~/.bashrc.bak`:

```bash
sed -i.bak -e '\|^export PATH=/usr/local/cuda-12.8/bin|d' -e '\|^export LD_LIBRARY_PATH=/usr/local/cuda/lib64|d' ~/.bashrc
```

**4. Sprawdzenie.** Wynik wklej w raporcie:

```bash
rpm -qa | grep -i -E 'cuda|-12-[89]-' | sort
ls -d /usr/local/cuda* /var/cuda-repo* 2>/dev/null
nvidia-smi --query-gpu=name,driver_version --format=csv
```

Oczekiwany wynik: z `rpm` zostają tylko `xorg-x11-drv-nvidia-cuda…` i `xorg-x11-drv-nvidia-cuda-libs…` (oraz niezwiązany `texlive-barracuda`), `ls` nic nie wypisuje, a `nvidia-smi` pokazuje RTX 4070 SUPER i sterownik 615.78.08.
