# Phase 0 — pytania (runda 5): ocena klasyfikatorami, ponowione K19 i K31

*2026-10-29 15:45 — Claude Opus 5.5*

## Co masz zrobić

Sześć decyzji. Wszystkie dotyczą **oceny** (nie metod kompresji, które wybierzesz Ty). Nie blokują Phase 1, więc możesz je odłożyć. K35 i K36 to ponowione pytania (prosiłeś o to przy K31 i K19). K37–K40 wynikają z Twoich decyzji K22–K28. Wystarczy „rek” albo litera.

---

### K35. 🟢 (ponowione K31) Ziarna przy wyborze danych kalibracyjnych

- **Problem:** to **nie** jest to samo co @phase-0:K24. Tam chodziło o losowość przy **generowaniu odpowiedzi** do oceny (wybrałeś 3 odpowiedzi na pytanie). Tu chodzi o losowość przy **kompresji**: metody z kalibracją (np. GPTQ, Wanda; czym jest kalibracja: `AGENTS/phases/phase-0/A3-dane-kalibracyjne.md`) losują 128 kawałków tekstu, a inne losowanie daje nieco inny skompresowany model. Dotyczy tylko metod, które używają kalibracji.
- **Opcje:**
  - **A** — zawsze 1 ziarno (najtaniej, ale nie wiemy, ile wynosi szum);
  - **B** — 3 ziarna dla każdego wariantu: 3 skompresowane modele, wynik jako średnia ± odchylenie (3× dłużej);
  - **C** — raz, na Qwen3-0.6B, mierzymy szum na 3–5 ziarnach dla kilku metod, a potem 1 ziarno. Różnice mniejsze niż zmierzony szum oznaczamy jako „nierozstrzygnięte”.
- **Rekomendacja:** C.
- **Decyzja:** C

### K36. 🟡 (ponowione K19) Jak zamienić wynik modelu nagrody na 0–100

- **Problem:** model nagrody nie daje ani 0–100, ani 1–10, tylko **liczbę bez ustalonej skali**, np. $r = 3{,}7$ albo $r = -1{,}2$. Sama w sobie nic nie znaczy, znaczą tylko **różnice**. Model nagrody jest uczony tak, że prawdopodobieństwo, że człowiek woli odpowiedź $a$ od $b$, to

$$P(a \succ b) = \sigma(r_a - r_b) = \frac{1}{1 + e^{-(r_a - r_b)}}$$

  Słownie: im większa różnica wyników, tym pewniej $a$ jest lepsza. Przy równych wynikach to 50/50. W modelu wieloatrybutowym każdy atrybut ma do tego własną skalę.
- **Opcje:**
  - **A** — **porównanie parami z BF16:** $100 \cdot \sigma(r_{\text{po kompresji}} - r_{\text{BF16}})$ dla tego samego pytania. 50 = tak samo dobra, poniżej 50 = gorsza. Naturalne dla wyniku ogólnego (pasuje do @phase-0:K20 = C);
  - **B** — **percentyl względem odpowiedzi BF16:** „ta odpowiedź jest lepsza niż X% odpowiedzi oryginalnego modelu” (osobno dla każdego atrybutu). Działa dla każdej skali;
  - **C** — bez skali 0–100: surowe wyniki i ich różnice względem BF16.
- **Rekomendacja:** A dla wyniku ogólnego + B dla atrybutów. Obie liczby są zrozumiałe bez znajomości skali modelu.
- **Decyzja:** ⏳ w toku → @A10 (wstępnie: A co sądzisz o użyciu czegoś w rodzaju ELO Score? Poza tym podoba mi się twoja rekomendacja)

### K37. 🟡 Limit długości odpowiedzi z myśleniem

- **Problem:** wybrałeś tryb myślenia (@phase-0:K25 = B), 3 odpowiedzi na pytanie (K24 = B) i 200 pytań (K23 = C), czyli 600 odpowiedzi na każdy wariant modelu. Qwen zaleca do 32 768 tokenów na odpowiedź z myśleniem, a małe modele po kompresji często myślą w kółko aż do limitu. Przy średnio ~2 tys. tokenów to ~1,2 mln tokenów na wariant. Ile to trwa, zależy od programu do generowania, o którym zdecydujemy, gdy będą znane metody.
- **Opcje:**
  - **A** — limit 4096 tokenów (szybko, ale część poprawnych, długich rozumowań zostanie ucięta);
  - **B** — limit 8192;
  - **C** — 32 768 (zalecenie Qwen, najwierniej, najdrożej).
- **Rekomendacja:** B. Ucięcie liczymy jako metrykę „kompletna = 0”, więc i tak widzimy, jak często model się zapętla.
- **Decyzja:** B

### K38. 🟢 Czy klasyfikator widzi myślenie modelu

- **Problem:** odpowiedź z trybem myślenia ma dwie części: `<think>…</think>` i odpowiedź końcową. Modele nagrody są uczone głównie na odpowiedziach końcowych.
- **Opcje:**
  - **A** — klasyfikator dostaje tylko odpowiedź końcową; metryki regułowe (pętle, czysty tekst) sprawdzają też część myślenia;
  - **B** — klasyfikator dostaje całość;
  - **C** — obie wersje (2× ocen).
- **Rekomendacja:** A.
- **Decyzja:** A

### K39. 🟡 Pytania w stylu IFEval w naszych 200 pytaniach a K28

- **Problem:** dwie Twoje decyzje się gryzą. W @phase-0:K22 = C część naszych pytań ma być w stylu IFEval („odpowiedz w 3 punktach”), a w @phase-0:K28 = A usunęliśmy metrykę „format zgodny z poleceniem”, bo IFEval jest w lm-eval. Bez tej metryki nikt nie sprawdzi, czy te nasze pytania zostały wykonane.
- **Opcje:**
  - **A** — w naszych 200 pytaniach **nie ma** pytań IFEval (wykonywanie poleceń mierzy IFEval w lm-eval, ~500 poleceń, lepsza statystyka); ich miejsce zajmują MT-Bench i pytania własne;
  - **B** — pytania IFEval zostają i tylko dla nich przywracamy metrykę „format zgodny”;
  - **C** — zostają bez sprawdzania formatu (ocenia je tylko klasyfikator).
- **Rekomendacja:** A. Bez dublowania, a wykonywanie poleceń mierzymy na większym zbiorze.
- **Decyzja:** A, chociaż proszę o jakiś wątek wyjaśniający mi co to zmienia

### K40. 🟢 Zgodność z odpowiedzią wzorcową

- **Problem:** część pytań (matematyka i rozumowanie z MT-Bench, część własnych) ma jedną poprawną odpowiedź, np. liczbę. Modele nagrody słabo sprawdzają, czy rachunek jest poprawny: oceniają raczej, czy odpowiedź *wygląda* dobrze.
- **Opcje:**
  - **A** — dodajemy 5. metrykę regułową „wynik zgodny z wzorcem” (0/1) dla pytań z jednoznaczną odpowiedzią;
  - **B** — nie dodajemy; poprawność ocenia tylko klasyfikator.
- **Rekomendacja:** A. To tania metryka i chroni przed sytuacją, w której model nagrody daje wysoki wynik pewnej siebie, ale błędnej odpowiedzi.
- **Decyzja:** A
