# T004 · Dodanie aliasu condy do zsh

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Hej, wydaje mi się że mam conde, ale nie mam chyba jej aliasu w .zsh (czy gdzie tam to jest), jak sprawdzić czy ją mam oraz dodać alias?

*2026-10-29 13:23 — Autor*

---
---
---

## Co masz zrobić

Uruchom dwa polecenia z punktu 2 i napisz tutaj, czy `conda --version` działa. Wystarczy: „działa”.

**1. Czy masz condę: tak.** Sprawdziłem za Ciebie:
- Miniconda **26.3.2** w `~/miniconda3`;
- `conda init` był zrobiony **tylko dla basha** (blok `# >>> conda initialize >>>` w `~/.bashrc`, linie 48–61). W `~/.zshrc` takiego bloku nie ma, dlatego zsh nie zna polecenia `conda`.

Sam możesz to sprawdzić tak:
```bash
ls ~/miniconda3/bin/conda
grep -n "conda initialize" ~/.bashrc ~/.zshrc
```

**2. Jak dodać condę do zsh.** Lepiej użyć `conda init` niż aliasu: alias nie zadziała dla `conda activate`, bo ono musi zmieniać zmienne bieżącej powłoki.
```bash
~/miniconda3/bin/conda init zsh
exec zsh
conda --version
```
`conda init zsh` dopisze do `~/.zshrc` taki sam blok jak w `~/.bashrc`. Z oh-my-zsh działa bez dodatkowych zmian.

**3. Opcjonalnie:** jeśli nie chcesz, żeby każdy terminal startował w środowisku `(base)`:
```bash
conda config --set auto_activate_base false
```
Wtedy środowisko włączasz ręcznie: `conda activate datascience`.

Jak cofnąć: `conda init --reverse zsh`.

Nie zmieniałem Twojego `~/.zshrc`, bo pytałeś, jak to zrobić. Jeśli wolisz, żebym zrobił to ja, napisz „zrób”.

*2026-10-29 13:30 — Claude Opus 5.5*

---
---
---

działa

*2026-10-29 14:04 — Autor*

---
---
---

🔒 Wątek zamknięty.

*2026-10-29 14:04 — Autor*

---
---
---
