# T008 · A.6 krok 1

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

```❯ sudo dnf remove 'cuda-*-12-8*' 'cuda-*-12-9*' 'libcu*-12-[89]' 'libnpp*-12-[89]' 'libnv*-12-[89]' 'gds-tools-12-[89]' cuda-toolkit-config-common cuda-toolkit-12-config-common
[sudo] hasło użytkownika karol: 
Pakiet                                                                           Arch              Wersja                                                                           Repozytorium                                     Rozmiar
Usuwanie:
 cuda-cccl-12-8                                                                  x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                        11.2 MiB
 cuda-cccl-12-9                                                                  x86_64            0:12.9.27-1                                                                      cuda-fedora41-12-9-local                        12.7 MiB
 cuda-command-line-tools-12-8                                                    x86_64            0:12.8.0-1                                                                       cuda-fedora41-12-8-local                         0.0   B
 cuda-command-line-tools-12-9                                                    x86_64            0:12.9.1-1                                                                       cuda-fedora41-12-9-local                         0.0   B
 cuda-compiler-12-8                                                              x86_64            0:12.8.0-1                                                                       cuda-fedora41-12-8-local                         0.0   B
 cuda-compiler-12-9                                                              x86_64            0:12.9.1-1                                                                       cuda-fedora41-12-9-local                         0.0   B
 cuda-crt-12-8                                                                   x86_64            0:12.8.61-1                                                                      cuda-fedora41-12-8-local                       922.5 KiB
 cuda-crt-12-9                                                                   x86_64            0:12.9.86-1                                                                      cuda-fedora41-12-9-local                       928.8 KiB
 cuda-cudart-12-8                                                                x86_64            0:12.8.57-1                                                                      cuda-fedora41-12-8-local                       773.3 KiB
 cuda-cudart-12-9                                                                x86_64            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                       785.8 KiB
 cuda-cudart-devel-12-8                                                          x86_64            0:12.8.57-1                                                                      cuda-fedora41-12-8-local                         7.7 MiB
 cuda-cudart-devel-12-9                                                          x86_64            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                         8.5 MiB
 cuda-cuobjdump-12-8                                                             x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                       617.2 KiB
 cuda-cuobjdump-12-9                                                             x86_64            0:12.9.82-1                                                                      cuda-fedora41-12-9-local                       665.7 KiB
 cuda-cupti-12-8                                                                 x86_64            0:12.8.57-1                                                                      cuda-fedora41-12-8-local                       134.4 MiB
 cuda-cupti-12-9                                                                 x86_64            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                       143.2 MiB
 cuda-cuxxfilt-12-8                                                              x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                         1.0 MiB
 cuda-cuxxfilt-12-9                                                              x86_64            0:12.9.82-1                                                                      cuda-fedora41-12-9-local                         1.0 MiB
 cuda-documentation-12-8                                                         x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                       524.1 KiB
 cuda-documentation-12-9                                                         x86_64            0:12.9.88-1                                                                      cuda-fedora41-12-9-local                       538.3 KiB
 cuda-driver-devel-12-8                                                          x86_64            0:12.8.57-1                                                                      cuda-fedora41-12-8-local                       126.5 KiB
 cuda-driver-devel-12-9                                                          x86_64            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                       131.0 KiB
 cuda-gdb-12-8                                                                   x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                        85.8 MiB
 cuda-gdb-12-9                                                                   x86_64            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                        89.7 MiB
 cuda-libraries-12-8                                                             x86_64            0:12.8.0-1                                                                       cuda-fedora41-12-8-local                         0.0   B
 cuda-libraries-12-9                                                             x86_64            0:12.9.1-1                                                                       cuda-fedora41-12-9-local                         0.0   B
 cuda-libraries-devel-12-8                                                       x86_64            0:12.8.0-1                                                                       cuda-fedora41-12-8-local                         0.0   B
 cuda-libraries-devel-12-9                                                       x86_64            0:12.9.1-1                                                                       cuda-fedora41-12-9-local                         0.0   B
 cuda-nsight-12-8                                                                x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                       113.2 MiB
 cuda-nsight-12-9                                                                x86_64            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                       113.2 MiB
 cuda-nsight-compute-12-8                                                        x86_64            0:12.8.0-1                                                                       cuda-fedora41-12-8-local                         7.3 KiB
 cuda-nsight-compute-12-9                                                        x86_64            0:12.9.1-1                                                                       cuda-fedora41-12-9-local                         7.3 KiB
 cuda-nsight-systems-12-8                                                        x86_64            0:12.8.0-1                                                                       cuda-fedora41-12-8-local                         1.7 KiB
 cuda-nsight-systems-12-9                                                        x86_64            0:12.9.1-1                                                                       cuda-fedora41-12-9-local                         1.7 KiB
 cuda-nvcc-12-8                                                                  x86_64            0:12.8.61-1                                                                      cuda-fedora41-12-8-local                       306.5 MiB
 cuda-nvcc-12-9                                                                  x86_64            0:12.9.86-1                                                                      cuda-fedora41-12-9-local                       317.8 MiB
 cuda-nvdisasm-12-8                                                              x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                         5.7 MiB
 cuda-nvdisasm-12-9                                                              x86_64            0:12.9.88-1                                                                      cuda-fedora41-12-9-local                         6.1 MiB
 cuda-nvml-devel-12-8                                                            x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                         1.3 MiB
 cuda-nvml-devel-12-9                                                            x86_64            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                         1.4 MiB
 cuda-nvprof-12-8                                                                x86_64            0:12.8.57-1                                                                      cuda-fedora41-12-8-local                        10.6 MiB
 cuda-nvprof-12-9                                                                x86_64            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                        10.6 MiB
 cuda-nvprune-12-8                                                               x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                       176.5 KiB
 cuda-nvprune-12-9                                                               x86_64            0:12.9.82-1                                                                      cuda-fedora41-12-9-local                       181.0 KiB
 cuda-nvrtc-12-8                                                                 x86_64            0:12.8.61-1                                                                      cuda-fedora41-12-8-local                       211.8 MiB
 cuda-nvrtc-12-9                                                                 x86_64            0:12.9.86-1                                                                      cuda-fedora41-12-9-local                       216.9 MiB
 cuda-nvrtc-devel-12-8                                                           x86_64            0:12.8.61-1                                                                      cuda-fedora41-12-8-local                       248.2 MiB
 cuda-nvrtc-devel-12-9                                                           x86_64            0:12.9.86-1                                                                      cuda-fedora41-12-9-local                       248.0 MiB
 cuda-nvtx-12-8                                                                  x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                       403.7 KiB
 cuda-nvtx-12-9                                                                  x86_64            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                       415.0 KiB
 cuda-nvvm-12-8                                                                  x86_64            0:12.8.61-1                                                                      cuda-fedora41-12-8-local                       135.9 MiB
 cuda-nvvm-12-9                                                                  x86_64            0:12.9.86-1                                                                      cuda-fedora41-12-9-local                       132.6 MiB
 cuda-nvvp-12-8                                                                  x86_64            0:12.8.57-1                                                                      cuda-fedora41-12-8-local                       127.7 MiB
 cuda-nvvp-12-9                                                                  x86_64            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                       127.7 MiB
 cuda-opencl-12-8                                                                x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                        91.7 KiB
 cuda-opencl-12-9                                                                x86_64            0:12.9.19-1                                                                      cuda-fedora41-12-9-local                        91.7 KiB
 cuda-opencl-devel-12-8                                                          x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                       741.1 KiB
 cuda-opencl-devel-12-9                                                          x86_64            0:12.9.19-1                                                                      cuda-fedora41-12-9-local                       741.1 KiB
 cuda-profiler-api-12-8                                                          x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                        72.9 KiB
 cuda-profiler-api-12-9                                                          x86_64            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                        73.4 KiB
 cuda-repo-fedora41-12-8-local                                                   x86_64            0:12.8.0_570.86.10-1                                                             <nieznane>                                       5.5 GiB
 cuda-repo-fedora41-12-9-local                                                   x86_64            0:12.9.1_575.57.08-1                                                             <nieznane>                                       6.3 GiB
 cuda-sandbox-devel-12-9                                                         x86_64            0:12.9.19-1                                                                      cuda-fedora41-12-9-local                       146.3 KiB
 cuda-sanitizer-12-8                                                             x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                        38.7 MiB
 cuda-sanitizer-12-9                                                             x86_64            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                        37.3 MiB
 cuda-toolkit-12-8                                                               x86_64            0:12.8.0-1                                                                       cuda-fedora41-12-8-local                         3.2 KiB
 cuda-toolkit-12-8-config-common                                                 noarch            0:12.8.57-1                                                                      cuda-fedora41-12-8-local                         0.0   B
 cuda-toolkit-12-9                                                               x86_64            0:12.9.1-1                                                                       cuda-fedora41-12-9-local                         3.2 KiB
 cuda-toolkit-12-9-config-common                                                 noarch            0:12.9.79-1                                                                      cuda-fedora41-12-9-local                         0.0   B
 cuda-toolkit-12-config-common                                                   noarch            0:12.8.57-1                                                                      cuda-fedora41-12-8-local                        44.0   B
 cuda-toolkit-config-common                                                      noarch            0:12.8.57-1                                                                      cuda-fedora41-12-8-local                        41.0   B
 cuda-tools-12-8                                                                 x86_64            0:12.8.0-1                                                                       cuda-fedora41-12-8-local                         0.0   B
 cuda-tools-12-9                                                                 x86_64            0:12.9.1-1                                                                       cuda-fedora41-12-9-local                         0.0   B
 cuda-visual-tools-12-8                                                          x86_64            0:12.8.0-1                                                                       cuda-fedora41-12-8-local                         0.0   B
 cuda-visual-tools-12-9                                                          x86_64            0:12.9.1-1                                                                       cuda-fedora41-12-9-local                         0.0   B
 gds-tools-12-8                                                                  x86_64            0:1.13.0.11-1                                                                    cuda-fedora41-12-8-local                        59.9 MiB
 gds-tools-12-9                                                                  x86_64            0:1.14.1.1-1                                                                     cuda-fedora41-12-9-local                        59.9 MiB
 libcublas-12-8                                                                  x86_64            0:12.8.3.14-1                                                                    cuda-fedora41-12-8-local                       856.6 MiB
 libcublas-12-9                                                                  x86_64            0:12.9.1.4-1                                                                     cuda-fedora41-12-9-local                       815.6 MiB
 libcublas-devel-12-8                                                            x86_64            0:12.8.3.14-1                                                                    cuda-fedora41-12-8-local                         1.2 GiB
 libcublas-devel-12-9                                                            x86_64            0:12.9.1.4-1                                                                     cuda-fedora41-12-9-local                         1.2 GiB
 libcufft-12-8                                                                   x86_64            0:11.3.3.41-1                                                                    cuda-fedora41-12-8-local                       266.8 MiB
 libcufft-12-9                                                                   x86_64            0:11.4.1.4-1                                                                     cuda-fedora41-12-9-local                       277.2 MiB
 libcufft-devel-12-8                                                             x86_64            0:11.3.3.41-1                                                                    cuda-fedora41-12-8-local                       546.3 MiB
 libcufft-devel-12-9                                                             x86_64            0:11.4.1.4-1                                                                     cuda-fedora41-12-9-local                       567.3 MiB
 libcufile-12-8                                                                  x86_64            0:1.13.0.11-1                                                                    cuda-fedora41-12-8-local                         3.2 MiB
 libcufile-12-9                                                                  x86_64            0:1.14.1.1-1                                                                     cuda-fedora41-12-9-local                         3.2 MiB
 libcufile-devel-12-8                                                            x86_64            0:1.13.0.11-1                                                                    cuda-fedora41-12-8-local                        27.6 MiB
 libcufile-devel-12-9                                                            x86_64            0:1.14.1.1-1                                                                     cuda-fedora41-12-9-local                        27.9 MiB
 libcurand-12-8                                                                  x86_64            0:10.3.9.55-1                                                                    cuda-fedora41-12-8-local                       130.5 MiB
 libcurand-12-9                                                                  x86_64            0:10.3.10.19-1                                                                   cuda-fedora41-12-9-local                       159.3 MiB
 libcurand-devel-12-8                                                            x86_64            0:10.3.9.55-1                                                                    cuda-fedora41-12-8-local                       132.5 MiB
 libcurand-devel-12-9                                                            x86_64            0:10.3.10.19-1                                                                   cuda-fedora41-12-9-local                       161.3 MiB
 libcusolver-12-8                                                                x86_64            0:11.7.2.55-1                                                                    cuda-fedora41-12-8-local                       374.0 MiB
 libcusolver-12-9                                                                x86_64            0:11.7.5.82-1                                                                    cuda-fedora41-12-9-local                       470.6 MiB
 libcusolver-devel-12-8                                                          x86_64            0:11.7.2.55-1                                                                    cuda-fedora41-12-8-local                       267.2 MiB
 libcusolver-devel-12-9                                                          x86_64            0:11.7.5.82-1                                                                    cuda-fedora41-12-9-local                       332.5 MiB
 libcusparse-12-8                                                                x86_64            0:12.5.7.53-1                                                                    cuda-fedora41-12-8-local                       374.1 MiB
 libcusparse-12-9                                                                x86_64            0:12.5.10.65-1                                                                   cuda-fedora41-12-9-local                       463.0 MiB
 libcusparse-devel-12-8                                                          x86_64            0:12.5.7.53-1                                                                    cuda-fedora41-12-8-local                       782.3 MiB
 libcusparse-devel-12-9                                                          x86_64            0:12.5.10.65-1                                                                   cuda-fedora41-12-9-local                       960.3 MiB
 libnpp-12-8                                                                     x86_64            0:12.3.3.65-1                                                                    cuda-fedora41-12-8-local                       305.3 MiB
 libnpp-12-9                                                                     x86_64            0:12.4.1.87-1                                                                    cuda-fedora41-12-9-local                       393.0 MiB
 libnpp-devel-12-8                                                               x86_64            0:12.3.3.65-1                                                                    cuda-fedora41-12-8-local                       318.5 MiB
 libnpp-devel-12-9                                                               x86_64            0:12.4.1.87-1                                                                    cuda-fedora41-12-9-local                       406.2 MiB
 libnvfatbin-12-8                                                                x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                         2.4 MiB
 libnvfatbin-12-9                                                                x86_64            0:12.9.82-1                                                                      cuda-fedora41-12-9-local                         2.4 MiB
 libnvfatbin-devel-12-8                                                          x86_64            0:12.8.55-1                                                                      cuda-fedora41-12-8-local                         2.3 MiB
 libnvfatbin-devel-12-9                                                          x86_64            0:12.9.82-1                                                                      cuda-fedora41-12-9-local                         2.3 MiB
 libnvjitlink-12-8                                                               x86_64            0:12.8.61-1                                                                      cuda-fedora41-12-8-local                        89.8 MiB
 libnvjitlink-12-9                                                               x86_64            0:12.9.86-1                                                                      cuda-fedora41-12-9-local                        91.6 MiB
 libnvjitlink-devel-12-8                                                         x86_64            0:12.8.61-1                                                                      cuda-fedora41-12-8-local                       127.1 MiB
 libnvjitlink-devel-12-9                                                         x86_64            0:12.9.86-1                                                                      cuda-fedora41-12-9-local                       127.6 MiB
 libnvjpeg-12-8                                                                  x86_64            0:12.3.5.57-1                                                                    cuda-fedora41-12-8-local                         7.5 MiB
 libnvjpeg-12-9                                                                  x86_64            0:12.4.0.76-1                                                                    cuda-fedora41-12-9-local                         9.0 MiB
 libnvjpeg-devel-12-8                                                            x86_64            0:12.3.5.57-1                                                                    cuda-fedora41-12-8-local                         7.9 MiB
 libnvjpeg-devel-12-9                                                            x86_64            0:12.4.0.76-1                                                                    cuda-fedora41-12-9-local                         9.4 MiB
Usuwanie nieużywanych zależności:
 java-25-openjdk                                                                 x86_64            1:25.0.4.1.1-1.1.fc44                                                            updates                                        961.0 KiB
 nsight-compute-2025.1.0                                                         x86_64            0:2025.1.0.14-1                                                                  cuda-fedora41-12-8-local                         1.1 GiB
 nsight-compute-2025.2.1                                                         x86_64            0:2025.2.1.3-1                                                                   cuda-fedora41-12-9-local                         1.1 GiB
 nsight-systems-2025.1.3                                                         x86_64            0:2025.1.3.140_251335620677v0-0                                                  cuda-fedora41-12-9-local                       976.8 MiB
 ttmkfdir                                                                        x86_64            0:3.0.9-74.fc44                                                                  fedora                                         142.2 KiB
 xorg-x11-fonts-Type1                                                            noarch            0:7.5-42.fc44                                                                    fedora                                         863.3 KiB

Podsumowanie transakcji:
 Usuwanie:                            123 pakietów

Po tej operacji 30 GiB zostanie zwolniony (zainstaluje 0 B, usunie 30 GiB).
Kontynuować? [t/N]: n
Operacja przerwana przez użytkownika.

~ via 🐍 v3.14.8 took 30s 
❯ ```

Czy to jest okej?

*2026-10-29 19:45 — Autor*

---
---
---

## Co masz zrobić

**Tak, w porządku.** Dobrze, że przerwałeś i zapytałeś. Uruchom to samo polecenie jeszcze raz i tym razem odpowiedz `t`:

```bash
sudo dnf remove 'cuda-*-12-8*' 'cuda-*-12-9*' 'libcu*-12-[89]' 'libnpp*-12-[89]' 'libnv*-12-[89]' 'gds-tools-12-[89]' cuda-toolkit-config-common cuda-toolkit-12-config-common
```

Potem kroki 2–4 z `AGENTS/phases/phase-1/A6-usuniecie-cuda-12.md`. Wynik kroku 4 wklej tutaj albo w raporcie pod @A6.

Wyjątek: jeśli używasz programów z okienkami w Javie uruchamianych systemową Javą (nie IDE i nie gier z własną Javą), najpierw zachowaj Javę:

```bash
sudo dnf mark user java-25-openjdk
```

---

**Kontekst.** Pytasz, czy lista z `dnf remove` (123 pakiety, 30 GiB) jest w porządku, skoro w @A6 pisałem o 117.

**Skąd różnica 123 vs 117.** Sprawdzałem tylko, które pakiety pasują do wzorców (117, wszystkie z CUDA 12). dnf dodatkowo usuwa **„nieużywane zależności”**: pakiety, które kiedyś zainstalowały się *tylko dlatego*, że potrzebowała ich CUDA, i teraz nikt ich nie potrzebuje. W Twojej liście jest ich 6:

| Pakiet | Co to | Usunąć? |
|---|---|---|
| `nsight-compute-2025.1.0`, `nsight-compute-2025.2.1`, `nsight-systems-2025.1.3` | profilery NVIDIA z CUDA 12.8/12.9 (nazwa bez „12-8”, dlatego wzorce ich nie złapały) | **tak**, to część starej CUDA (~3 GiB) |
| `java-25-openjdk` | graficzna część Javy. Zainstalowały ją narzędzia CUDA z okienkami (nvvp, nsight) | **raczej tak**, szczegóły niżej |
| `xorg-x11-fonts-Type1`, `ttmkfdir` | czcionki dla tej Javy | tak, idą razem z nią |

**O Javie sprawdziłem:**
- żaden inny pakiet jej nie wymaga (`rpm -q --whatrequires java-25-openjdk` → brak);
- **zostaje `java-25-openjdk-headless`**, więc polecenie `java` dalej działa dla programów bez okienek;
- CLion (masz go w `~/.local/share/JetBrains`) ma własną wbudowaną Javę, więc go to nie dotyczy;
- zniknie tylko obsługa okienek w systemowej Javie. Jeśli jej nie używasz, nic nie tracisz. Jeśli używasz, zrób najpierw `sudo dnf mark user java-25-openjdk` (wtedy dnf uzna, że zainstalowałeś ją sam, i jej nie ruszy).

Mój błąd: w @A6 powinienem był uprzedzić, że dnf dołoży nieużywane zależności. Dopisałem to w pliku zadania i w pułapkach.

*2026-10-29 19:46 — Claude Opus 5.5*

---
---
---
