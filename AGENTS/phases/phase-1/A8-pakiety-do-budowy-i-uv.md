# A8 — pakiety do budowy llama.cpp i uv

*2026-10-29 15:00 — Claude Opus 5.5*

## Co masz zrobić

Uruchom dwa polecenia niżej (można przed @A6 i @A7, kolejność nie ma znaczenia) i wklej w raporcie pod @A8 wynik drugiego. Budowę llama.cpp zrobię ja po @A7, bez `sudo`. Pythona 3.14 masz już w systemie (decyzja @phase-0:K5 = A).

**Dopisane 2026-10-29 20:12:** `git`, `cmake`, `gcc-c++`, `openssl-devel` i `libcurl-devel` są już w systemie (sprawdziłem). Wystarczy:

```bash
sudo dnf install uv
uv --version
```

Pełne polecenie niżej też zadziała (dnf pominie to, co już jest).

## Kroki

**1. Instalacja** (`uv` 0.12.24 jest w repo Fedory 44 — decyzja @phase-0:K4 = A):

```bash
sudo dnf install git cmake gcc-c++ openssl-devel libcurl-devel uv
```

**2. Sprawdzenie:**

```bash
uv --version && cmake --version | head -1 && g++ --version | head -1 && python3.14 --version
```

Oczekiwany wynik: wersje czterech narzędzi, bez błędów.
