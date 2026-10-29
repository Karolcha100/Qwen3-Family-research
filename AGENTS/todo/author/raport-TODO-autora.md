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

### [A5] Pozwól agentowi na git push

zrobione sposobem 2

*2026-10-29 16:14 — Autor*

---

> 🤖 **ODPOWIEDŹ LLM — początek** (Claude Opus 5.5)
>
> ### [A5] Re: Pozwól agentowi na git push
>
> **Co masz zrobić:** nic. Dzięki!
>
> Sprawdziłem: `.claude/settings.json` zawiera regułę `Bash(git push)`. Dodaję go do repo w tym commicie, a push tej sesji idzie już z tą regułą. Zadanie oznaczyłem jako `[x]`.
>
> *przeczytane i odpowiedziane: 2026-10-29 16:21 — Claude Opus 5.5*
>
> 🤖 **ODPOWIEDŹ LLM — koniec**

---

### [A10] K36: 🟡 (ponowione K19) Jak zamienić wynik modelu nagrody na 0–100

A co sądzisz o użyciu czegoś w rodzaju ELO Score? Poza tym podoba mi się twoja rekomendacja

*2026-10-29 16:18 — Autor*

---

> 🤖 **ODPOWIEDŹ LLM — początek** (Claude Opus 5.5)
>
> ### [A10] Re: K36: 🟡 (ponowione K19) Jak zamienić wynik modelu nagrody na 0–100
>
> **Co masz zrobić:** jeśli pasuje Ci propozycja niżej, wpisz w @phase-0:K36 odpowiedź końcową: „A + B + ranking Elo”. Wystarczy: „zgoda”.
>
> **Opinia: Elo to dobry pomysł i pasuje do modeli nagrody niemal idealnie. Proponuję go jako *dodatek* do mojej rekomendacji, nie zamiast niej.**
>
> **Czym jest Elo.** To system rankingowy z szachów (a dziś też z Chatbot Areny, która porównuje modele LLM). Każdy gracz ma wynik $R$. Przewidywana szansa, że $A$ wygra z $B$:
>
> $$E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}$$
>
> Słownie: liczy się tylko **różnica** wyników. 0 punktów różnicy daje 50%, 100 punktów ≈ 64%, 200 punktów ≈ 76%, 400 punktów ≈ 91%.
>
> **Dlaczego pasuje:** to dokładnie ten sam wzór, którego uczy się model nagrody, $P(a \succ b) = \sigma(r_a - r_b)$, tylko w innych jednostkach (podstawa 10 i skala 400 zamiast $e$). Wynik modelu nagrody to w praktyce „Elo pojedynczej odpowiedzi”.
>
> **Jak by to działało u nas:**
> - każdy wariant (BF16, GPTQ-4bit, Wanda-50%…) to „gracz”;
> - „mecz” to dwie odpowiedzi różnych wariantów na **to samo pytanie**, a model nagrody wyznacza szansę wygranej;
> - z wszystkich meczów dopasowujemy ranking **Bradleya–Terry'ego**, czyli wersję Elo liczoną od razu ze wszystkich meczów, a nie mecz po meczu. Klasyczne Elo zależy od kolejności meczów, a tej wady nie ma. Tak liczy dziś Chatbot Arena;
> - BF16 dostaje stałe **1000** punktów, więc „GPTQ-4bit: 962” znaczy, że jego odpowiedź jest lepsza od odpowiedzi BF16 w ~45% przypadków.
>
> **Plusy:**
> - **jeden ranking wszystkich wariantów naraz**, także między sobą (nie tylko każdy z BF16);
> - **nic nie kosztuje:** model nagrody ocenia każdą odpowiedź raz, a wszystkie mecze to już tylko arytmetyka, bez GPU;
> - łatwo zrozumiałe różnice i łatwo dodać nowy wariant.
>
> **Minusy:**
> - skala jest **względna**: ranking zależy od tego, które warianty biorą udział. Dodanie nowego lekko przesuwa pozostałe; stałe BF16 = 1000 ogranicza ten efekt;
> - przy kilku wariantach ranking niewiele dodaje ponad metrykę 16 z planu (porównanie z BF16). Zyskuje, gdy wariantów jest dużo.
>
> **Propozycja końcowa:** **A** (porównanie z BF16, 0–100) + **B** (percentyle atrybutów) + **ranking Elo (Bradley–Terry)** wszystkich wariantów z BF16 = 1000 jako podsumowanie. Wynik A da się wprost przeliczyć na różnicę Elo: $\Delta R = 400 \log_{10}\frac{p}{1-p}$, gdzie $p$ to szansa wygranej z BF16.
>
> *przeczytane i odpowiedziane: 2026-10-29 16:21 — Claude Opus 5.5*
>
> 🤖 **ODPOWIEDŹ LLM — koniec**

---
