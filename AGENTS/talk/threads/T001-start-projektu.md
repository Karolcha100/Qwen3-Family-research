# T001 · Start projektu: git, plan faz, instalacja

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

## Co masz zrobić

Przeczytałem `CLAUDE.md`, `AGENTS/` (cały szablon jest jeszcze pusty) i `local-llm-conversation.md`. Zanim ruszę, potrzebuję trzech krótkich decyzji. Wystarczy np.: „1 tak, 2 tak, 3 A”.

1. **Git.** Katalog projektu nie jest repozytorium git, a instrukcja wymaga commita po każdej sesji i `git diff` od ostatniego briefingu. Czy mam zrobić `git init` (lokalnie, bez remote) i pierwszy commit z obecnym stanem? (tak / nie)
2. **Plan faz.** Czy mam rozpisać plan faz do zatwierdzenia (`AGENTS/plan/phases-plans.md`, `AGENTS/plan/phases-description.md`)? Szkic, który bym rozwinął:
   - **Phase 1 — środowisko:** CUDA 13.4, llama.cpp, środowisko Pythona (PyTorch, transformers, lm-eval), test na Qwen3-0.6B;
   - **Phase 2 — baseline ewaluacji:** BF16 i RTN na 0.6B: perplexity (WikiText-2, C4), KL względem BF16, kilka zadań lm-eval; wspólny skrypt do mierzenia;
   - **Phase 3 — kwantyzacja:** GPTQ, AWQ, HQQ, potem rotacje;
   - **Phase 4 — pruning:** Wanda, SparseGPT, 2:4;
   - **Phase 5 — niskie rzędy i leczenie:** SVD, ASVD/SVD-LLM, LoRA-distillation; potem skalowanie na 1.7B, 4B i 8B.

   (tak / nie / zmień kolejność: …)
3. **Instalacja.** Kroki z `sudo` (usunięcie CUDA 12.x, CUDA 13.4, budowa llama.cpp) robisz Ty.
   - **A** — dodam je jako zadania A w WAŻNE, z poleceniami z `local-llm-conversation.md`; po każdym kroku wklejasz wynik (np. `nvcc --version`), a ja sprawdzam.
   - **B** — robisz je sam(a) bez zadań; dasz znać w tym wątku, gdy skończysz.

   Rekomendacja: **A**, bo każdy krok ma wynik do sprawdzenia (`rpm -qa | grep -i cuda`, `nvcc --version`, `llama-cli --version`).

## Uwaga do planu instalacji

PyTorch z pip ma własne biblioteki CUDA (wheel `cu13x`), więc systemowa CUDA 13.4 jest potrzebna tylko do llama.cpp i do kompilacji własnych kerneli (np. niektórych implementacji AWQ albo QuIP#). Eksperymenty w Pythonie (RTN, GPTQ, Wanda, SVD) mogą ruszyć równolegle z instalacją CUDA. Wersję wheel dobiorę do sterownika 615 w Phase 1.

*2026-10-29 12:54 — Claude Opus 5.5*

---
---
---

Zapamiętaj że tego typu pytania powinny być w pytaniach bez decyzji (każde oddzielnie). Pamiętaj także że na luzie możesz się mnie pytać o masę rzeczy, praktycznie wszystko, w tych pytaniach. Powiedziałbym nawet że mi na tym zależy bo jednak wolę abyś zapytał o decyzję, która może w tym momencie nie ma znaczenia, ale 200 decyzji dalej - już może mieć znaczenie.

Także zrób ten wątek jako pytania. Jedynie Uwagi do planu instalacji można zostawić w nowym wątku T003 - Bo T002 zaraz zrobię sam bo mam pytanie.

*2026-10-29 13:02 — Autor*

---
---
---

## Co masz zrobić

Odpowiedz na pytania w **Co czeka na mnie → Pytania bez decyzji → phases/phase-0/agents-issues-1.md** (16 pytań, każde osobno, z rekomendacją; wystarczy wpisać „rek” albo literę opcji). Ten wątek możesz zamknąć 🔒.

Zrobione:
- pytania 1–3 z tego wątku są teraz w @phase-0:K1 (git), @phase-0:K2 (plan faz) i @phase-0:K3 (instalacja). Dodałem 13 kolejnych decyzji, które teraz niewiele kosztują, a później mogą mieć znaczenie: od @phase-0:K4 do @phase-0:K16. K13 to decyzja z @T002;
- uwagę o planie instalacji przeniosłem do @T003;
- zapamiętałem regułę: decyzje zawsze jako osobne pytania w `agents-issues-N.md`, a pytań może być dużo (`AGENTS/memory/zasady-wspolpracy.md`).

*2026-10-29 13:05 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-10-29 13:12 — Autor*

---
---
---
