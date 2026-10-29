# Raport autora — odpowiedzi do zadań A…

Wpisy autora (z GUI albo ręcznie) i pod nimi bloki „🤖 ODPOWIEDŹ LLM” od agentów. Format: `AGENTS/todo/author/INSTRUKCJA.md`.

---
---
---

### [A1] Utwórz prywatne repozytorium GitHub „Qwen3-Family-research”

zrobione

*2026-10-29 13:54 — Autor*

---

> 🤖 **ODPOWIEDŹ LLM — początek** (Claude Opus 5.5)
>
> ### [A1] Re: Utwórz prywatne repozytorium GitHub „Qwen3-Family-research”
>
> **Co masz zrobić:** nic. Zostało tylko @phase-0:K17 (czy ja pushuję po sesji); do tego czasu commituję lokalnie, a push robisz Ty:
>
> ```bash
> git push
> ```
>
> Sprawdziłem: `origin` wskazuje na `github.com/Karolcha100/Qwen3-Family-research`, a `main` jest zsynchronizowany z `origin/main` (commit `49943d4`). Zadanie oznaczyłem jako `[x]`.
>
> *przeczytane i odpowiedziane: 2026-10-29 14:09 — Claude Opus 5.5*
>
> 🤖 **ODPOWIEDŹ LLM — koniec**

---

### [A2] K7: 🟡 Qwen3 Base czy wersja instrukcyjna

Potrzebuję raportu o tym czym jest base, perplexity, jak to wpływa na rzeczy, czym jest wersja bez sufiksu etc.

*2026-10-29 14:52 — Autor*

---

> 🤖 **ODPOWIEDŹ LLM — początek** (Claude Opus 5.5)
>
> ### [A2] Re: K7: 🟡 Qwen3 Base czy wersja instrukcyjna
>
> **Co masz zrobić:** przeczytaj raport `AGENTS/phases/phase-0/A2-base-czy-instrukcyjna.md` i napisz tutaj wybór: **A** (rek.), **B** albo **C**.
>
> Krótko: **Base** = model po samym pretreningu, który tylko dokańcza tekst; perplexity mierzy dokładnie to, czego go uczono. **Wersja bez sufiksu** (`Qwen3-0.6B`) = Base douczony do czatu (SFT, RL, destylacja z dużych Qwen3): wykonuje polecenia i ma tryb myślenia. Rekomenduję **A**: Base do perplexity, KL i lm-eval (porównywalność z artykułami), a wersja instrukcyjna do IFEval, evalplus i sędziego (tego Base nie umie). Przy okazji sprawdzimy, czy kompresja psuje bardziej wiedzę, czy zachowania z post-treningu.
>
> *przeczytane i odpowiedziane: 2026-10-29 15:03 — Claude Opus 5.5*
>
> 🤖 **ODPOWIEDŹ LLM — koniec**

---

### [A3] K8: 🟡 Dane kalibracyjne

W jaki sposób wybór wpływa na wyniki, o co tutaj chodzi, potrzebuję raportu

*2026-10-29 14:53 — Autor*

---

> 🤖 **ODPOWIEDŹ LLM — początek** (Claude Opus 5.5)
>
> ### [A3] Re: K8: 🟡 Dane kalibracyjne
>
> **Co masz zrobić:** przeczytaj raport `AGENTS/phases/phase-0/A3-dane-kalibracyjne.md` i napisz tutaj wybór: **A** (rek.), **B** albo **C**.
>
> Krótko: GPTQ, AWQ, Wanda i SparseGPT minimalizują błąd **wyjścia** warstwy $\|WX - \widehat{W}X\|_F^2$, a nie samych wag. Wejścia $X$ biorą z próbki tekstu, czyli danych kalibracyjnych. Metoda chroni to, co widzi w próbce, więc wybór domeny ma znaczenie, a kalibracja na WikiText-2 zawyża wynik perplexity na WikiText-2. Rekomenduję **A** (C4, 128 × 2048 tokenów, stałe ziarno), a mieszankę z kodem jako osobny eksperyment. Z raportu wyszły dwa nowe pytania: @phase-0:K31 (powtórzenia z kilkoma ziarnami) i @phase-0:K32 (format kalibracji dla modelu instrukcyjnego).
>
> *przeczytane i odpowiedziane: 2026-10-29 15:03 — Claude Opus 5.5*
>
> 🤖 **ODPOWIEDŹ LLM — koniec**

---

### [A4] K9: 🟡 Protokół perplexity

Nie wiem co to perplexity, nie wiem co zmieniają odpowiedzi, proszę o raport

*2026-10-29 14:54 — Autor*

---

> 🤖 **ODPOWIEDŹ LLM — początek** (Claude Opus 5.5)
>
> ### [A4] Re: K9: 🟡 Protokół perplexity
>
> **Co masz zrobić:** przeczytaj raport `AGENTS/phases/phase-0/A4-perplexity.md` i napisz tutaj wybór: **A** (rek.), **B** albo **C**.
>
> Krótko: perplexity $\mathrm{PPL} = \exp\big(-\tfrac{1}{N}\sum_i \log p_\theta(x_i \mid x_{<i})\big)$ to średnia geometryczna z „1 / prawdopodobieństwo prawidłowego tokenu”. PPL = 10 znaczy, że model jest tak niepewny, jakby losował spośród 10 tokenów. Im niżej, tym lepiej, a kompresja ją podnosi. Protokół (długość okna, cięcie tekstu, wycinek zbioru) zmienia same liczby, więc musi być stały. Rekomenduję **A** (okna 2048 bez nakładania, standard GPTQ/Wanda), bo daje porównywalność z literaturą.
>
> *przeczytane i odpowiedziane: 2026-10-29 15:03 — Claude Opus 5.5*
>
> 🤖 **ODPOWIEDŹ LLM — koniec**

---

### [A9] K14: 🟢 Narzędzia jakości kodu

Czy to potrzebne jeżeli będziemy stosować tamte benchmarki? - Jeżeli benchmarki tego nie uwzględniają to A

*2026-10-29 15:38 — Autor*

---

> 🤖 **ODPOWIEDŹ LLM — początek** (Claude Opus 5.5)
>
> ### [A9] Re: K14: 🟢 Narzędzia jakości kodu
>
> **Co masz zrobić:** jeśli zgadzasz się z wyjaśnieniem, wpisz w @phase-0:K14 odpowiedź końcową „A”. Wystarczy: „A”.
>
> To nieporozumienie z mojej strony, bo za mało wyjaśniłem pytanie. **Benchmarki i narzędzia jakości sprawdzają dwie zupełnie różne rzeczy:**
> - **benchmarki** (lm-eval, evalplus) sprawdzają **model Qwen3**: czy dobrze odpowiada;
> - **`ruff`, `pyright`, `pytest`** sprawdzają **nasz kod w Pythonie**, czyli skrypty, które kompresują i mierzą:
>   - `ruff`: styl i proste błędy (np. nieużywana zmienna, literówka w nazwie);
>   - `pyright`: zgodność typów (chciałeś kod z typami; pyright pilnuje, żeby się zgadzały);
>   - `pytest`: małe testy, np. że funkcja liczenia perplexity daje 4 na przykładzie z `AGENTS/phases/phase-0/A4-perplexity.md`.
>
> Benchmarki tego nie uwzględniają, więc według Twojej reguły wychodzi **A**. Koszt jest pomijalny: trzy narzędzia w środowisku uv, uruchamiane w kilka sekund. Kiedy kod ma błąd, dowiadujemy się o nim od razu, a nie po godzinie liczenia z błędnym wynikiem.
>
> *przeczytane i odpowiedziane: 2026-10-29 15:45 — Claude Opus 5.5*
>
> 🤖 **ODPOWIEDŹ LLM — koniec**

---
