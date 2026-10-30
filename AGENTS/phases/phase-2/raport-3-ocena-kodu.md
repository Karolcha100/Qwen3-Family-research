# Jak oceniać, czy zmniejszony model dobrze programuje (raport 3)

*2026-10-30 11:10 — Claude Opus 5.5*

**Status raportu:** do przeczytania

## Co masz zrobić

Przeczytaj i odpowiedz na pytania **K32–K36** w `AGENTS/phases/phase-2/agents-issues-5.md`. Najważniejsze są K32 (główny test poprawności) i K36 (zgoda na uruchamianie kodu napisanego przez model w odizolowanym kontenerze). Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”.

W skrócie: dla kodu **testy są lepsze niż klasyfikator**. Klasyfikator ma sens tylko do tego, czego testy nie mierzą (czytelność, styl), i to dopiero później.

---

## 1. Co chcemy mierzyć

Wynika to z @phase-2:K20 i @phase-2:K25–K28: zmniejszony model ma dalej dobrze programować w Pythonie. Są cztery różne rzeczy:

| Co | Pytanie | Jak mierzyć |
|---|---|---|
| zgodność z oryginałem | czy model przewiduje kod tak jak przed zmniejszeniem | KL i zmiana straty na odłożonym kodzie (już liczone, tanie) |
| poprawność | czy napisany kod działa | zadania z testami (rozdz. 2) |
| jakość | czy kod jest czytelny i bez błędów widocznych bez uruchamiania | analiza statyczna (rozdz. 4), ewentualnie model oceniający (rozdz. 3) |
| sprawność | czy kod działa szybko; czy zmniejszony model działa szybciej | czas działania rozwiązań (rozdz. 5); parametry, pamięć, tokeny/s modelu |

## 2. Poprawność: zadania z testami

Model dostaje opis funkcji, pisze kod, a gotowe testy sprawdzają, czy działa. Wynik **pass@1** to odsetek zadań rozwiązanych za pierwszym podejściem (dekodowanie zachłanne, bez losowania).

| Zestaw | Zadań | Uwagi |
|---|---|---|
| HumanEval | 164 | funkcje w Pythonie z opisem; najczęściej używany |
| MBPP | 500 testowych | krótkie zadania w Pythonie; Qwen podaje wynik 3-shot (3 przykłady w poleceniu) |
| HumanEval+ i MBPP+ (EvalPlus) | jak wyżej | te same zadania, ale dużo więcej testów, więc trudniej „przejść przypadkiem” |

**Punkt odniesienia z raportu technicznego Qwen3** (tabela 8, modele bazowe):

| Model | EvalPlus (średnia z HumanEval, MBPP, HumanEval+, MBPP+) | MBPP (3-shot) |
|---|---|---|
| Qwen2.5-0.5B-Base | 31,85 | 29,80 |
| **Qwen3-0.6B-Base** | **36,23** | **36,60** |
| Qwen2.5-1.5B-Base | 44,80 | 43,60 |

Pierwszy krok to więc odtworzenie ~36% dla oryginału. Jeśli wyjdzie wyraźnie inaczej, mamy błąd w sposobie zadawania pytań, a nie w modelu.

**Ile to jest warte statystycznie.** Przy ~36% rozwiązanych zadań niepewność wyniku (błąd standardowy) wynosi:

$$
\sqrt{\frac{p\,(1-p)}{n}}: \quad n = 164 \;\to\; 3{,}7 \text{ pkt proc.}, \qquad n = 500 \;\to\; 2{,}1 \text{ pkt proc.}
$$

Słownie: na samym HumanEval różnica 3–4 punktów między modelami może być przypadkiem. Pomaga to, że oryginał i zmniejszony model rozwiązują **te same** zadania. Liczymy wtedy, ile zadań zmniejszony model stracił i ile zyskał, i to jest dużo czulsze. Dlatego testy uzupełniają KL (czułą, ale pośrednią), a nie ją zastępują (@phase-2:K27 = A).

Trudniejsze zestawy (np. LiveCodeBench, BigCodeBench) są dla modelu 0,6B prawdopodobnie za trudne: rozwiąże za mało zadań, żeby porównanie coś mówiło. Tego nie sprawdzałem.

## 3. Klasyfikatory (modele oceniające kod)

Model oceniający daje liczbę „jak dobre jest to rozwiązanie” bez uruchamiania testów. Dla kodu widzę trzy możliwości:

1. **Model nagrody do kodu**, np. AceCodeRM-7B (TIGER-Lab, zbudowany na Qwen2.5-Coder-7B-Instruct, licencja MIT). Uczony odróżniać kod przechodzący testy od nieprzechodzącego. Ma 7 mld parametrów, czyli ~15 GB w bf16, więc na 12 GB tylko w 8 lub 4 bitach. Jak bardzo traci przy tym jakość, nie wiem.
2. **Model-sędzia:** większy model instrukcyjny (np. Qwen2.5-Coder-7B-Instruct w GGUF przez nasz llama.cpp, ~5 GB w 4 bitach) ocenia czytelność i styl według ustalonej listy kryteriów. Takie oceny są zaszumione i mają swoje skrzywienia (np. wolą dłuższe odpowiedzi).
3. **Bez klasyfikatora:** testy plus analiza statyczna.

**Moja opinia:** w zadaniach z testami klasyfikator przewiduje to, co testy po prostu sprawdzają, więc nic nie wnosi. Ma sens w dwóch sytuacjach:
- do oceny czytelności i stylu, których testy nie widzą;
- do oceny kodu pisanego bez testów (np. dokończenia prawdziwych plików z naszego odłożonego zbioru).

Rekomenduję zacząć bez klasyfikatora (pytanie K33), a model-sędzię dodać, jeśli testy i analiza statyczna pokażą, że zmniejszony model pisze kod „działający, ale gorszy”.

## 4. Jakość bez uruchamiania (analiza statyczna)

Tanie, deterministyczne i bez dodatkowych modeli. Dla każdego rozwiązania:
- **ruff:** liczba błędów i ostrzeżeń (np. nieużyte zmienne, błędne porównania);
- **pyright:** błędy typów i odwołania do nieistniejących nazw;
- **złożoność cyklomatyczna** (np. pakiet `radon`): liczba ścieżek w funkcji, im mniej, tym prościej;
- **długość** rozwiązania w liniach.

Porównujemy to między oryginałem a zmniejszonym modelem na tych samych zadaniach. Rozwiązania HumanEval są krótkie, więc różnice będą małe. Jeśli jednak zmniejszanie zaczyna psuć kod, zwykle najpierw widać to tutaj (więcej błędów nazw i składni).

## 5. Sprawność

„Sprawność” ma dwa znaczenia:
- **sprawność zmniejszonego modelu:** liczba parametrów, pamięć i szybkość generowania (tokeny/s). To jest właściwy zysk z kompresji i mierzymy go zawsze.
- **sprawność napisanego kodu:** jak szybko działa rozwiązanie. Służy do tego np. zestaw **Mercury** (NeurIPS 2024): 1889 zadań w Pythonie z rozwiązaniami ludzi jako punktem odniesienia czasu działania. Wynik „Beyond” łączy poprawność z szybkością. Zadania są w stylu LeetCode, więc model 0,6B rozwiąże ich mało, a szybkość da się porównać tylko na rozwiązanych.

Rekomenduję (K35): sprawność modelu od razu, a Mercury dopiero po zmierzeniu, ile zadań oryginał w ogóle rozwiązuje.

## 6. Bezpieczeństwo: uruchamianie kodu napisanego przez model

Testy wymagają uruchomienia kodu, którego nikt nie sprawdził. Proponuję:
- kontener podman (jest zainstalowany) bez sieci (`--network=none`);
- system plików tylko do odczytu, z wyjątkiem katalogu tymczasowego;
- limity pamięci, procesora i czasu (np. 10 s na zadanie);
- obraz `python:3.12-slim` (pobranie ~50 MB).

Model generuje na GPU poza kontenerem, a w kontenerze uruchamiane są tylko testy. To wymaga Twojej zgody (K36).

## 7. Źródła

- Qwen3 Technical Report, tabela 8: https://arxiv.org/abs/2505.09388
- AceCoder i AceCodeRM-7B: https://github.com/tiger-ai-lab/acecoder, https://huggingface.co/TIGER-Lab/AceCodeRM-32B
- Mercury: https://papers.nips.cc/paper_files/paper/2024/hash/1df1df43b58845650b8dada00fca9772-Abstract-Datasets_and_Benchmarks_Track.html

*2026-10-30 11:10 — Claude Opus 5.5*
