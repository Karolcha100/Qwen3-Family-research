# Główny pomysł — pytania (runda 8): po wynikach K31–K38

*2026-10-30 17:13 — Claude Opus 5.5*

## Co masz zrobić

Pytania wynikają z raportu `AGENTS/phases/phase-2/etap-4c-k31-k38.md`. Najważniejsze są K40 i K43. W K43 opcja A zawiera krótkie obliczenie GPU (~5 min); „rek” lub „A” oznacza też zgodę na nie. Jeśli zgadzasz się z rekomendacjami, wystarczy „rek”.

---

### K40. 🔴 Jakim celem trenować zmniejszone warstwy

- **Problem:** cel na wyjściu modelu (@phase-2:K37) w warstwie 26 zmniejsza KL o 18% (stary cel: o 1%), ale w warstwie 13 jest gorszy od starego celu i ~18× wolniejszy (raport, sekcje 4–5). Z mniejszym krokiem ($1 \cdot 10^{-5}$) trening na wyjściu jest stabilny, ale w warstwie 13 daje −7% KL wobec −18% starego celu (sekcja 5). Dodatkowo pass@1 warstwy 26 nie spadł nawet przed tym wyborem (sekcja 7), więc zysk z celu na wyjściu w końcowych warstwach mierzymy na razie tylko przez KL.
- **Opcje:**
  - **A** — **cel zależny od warstwy:** stary cel (za następną warstwą) tam, gdzie działa (środek modelu), cel na wyjściu dla ostatnich warstw, gdzie stary zawodzi. Granicę wyznaczę krótkim sprawdzeniem kilku warstw;
  - **B** — wszędzie cel na wyjściu (wolno: ~25 min na warstwę w środku modelu przy 6 epokach);
  - **C** — wszędzie stary cel (szybko, ale końcowe warstwy prawie nie korzystają z treningu).
- **Rekomendacja:** A. Każdy cel działa tam, gdzie drugi zawodzi; dla ostatnich warstw biorę krok $1 \cdot 10^{-5}$, który okazał się stabilny.
- **Decyzja:** C, wszędzie stary cel.

### K41. 🟡 Waga kodu w mapie

- **Problem:** mapa 100% kod daje na Pythonie o 11–17% mniejszą KL niż obecna 75/25, ale na tekście o 25–35% większą (raport, sekcja 6). W testach kodu (warstwa 13, −40%) obie mapy dają tyle samo: średnia 34,4 (100% kod) wobec 34,2 (75/25), różnica w szumie.
- **Opcje:**
  - **A** — zostajemy przy 75/25;
  - **B** — przechodzimy na 100% kod (model tylko do kodu, tekst nas nie interesuje);
  - **C** — na razie 75/25, a do pytania wracamy przy większym zmniejszeniu (kilka warstw), gdzie różnice w pass@1 będą mierzalne.
- **Rekomendacja:** C. Na Pythonie zysk z mapy 100% kod jest mniejszy niż strata na tekście, a w pass@1 nie widać go wcale; przy jednej warstwie nie da się tego rozstrzygnąć.
- **Decyzja:** A

### K42. 🟢 Scalanie neuronów

- **Problem:** scalanie usuwanych neuronów z zostającymi jest gorsze niż ich zwykłe usunięcie, na każdym kroku, także po 16 epokach treningu (raport, sekcja 3). Neurony w tym modelu robią prawie niezależne rzeczy (podobieństwo aktywacji ~0,13), więc uśrednianie psuje te, które zostają.
- **Opcje:**
  - **A** — porzucamy scalanie; zapisuję jako wynik negatywny (do pracy, z wyjaśnieniem);
  - **B** — próbujemy innego sposobu scalania (np. z wagami dobranymi najmniejszymi kwadratami zamiast średniej);
  - **C** — odkładamy do „future research”.
- **Rekomendacja:** A. Wynik jest wyraźny i ma prostą przyczynę; inna wersja scalania nie zmieni tego, że neurony są prawie niezależne.
- **Decyzja:** A

### K43. 🔴 Jak mierzyć kod w kolejnych etapach

- **Problem:** dwie rzeczy z testów kodu (raport, sekcja 7):
  1. zmniejszenie jednej warstwy zmienia wynik ~10–25 zadań w obie strony, więc różnice ~1–2 punktów pass@1 są w szumie, a testy jednego modelu trwają ~7 min;
  2. **KL nie przewiduje pass@1 między warstwami:** warstwa 26 ma 3× większą KL niż warstwa 13, a w pass@1 nie traci nic (warstwa 13: −2,7 punktu). Przypuszczam, że przy dekodowaniu zachłannym liczy się głównie, czy najbardziej prawdopodobny token zostaje ten sam.
- **Opcje:**
  - **A** — codzienne miary: **KL na Pythonie + zgodność najbardziej prawdopodobnego tokenu z oryginałem** (odsetek tokenów, w których model wybiera ten sam token; liczy się przy okazji KL, bez dodatkowego kosztu); testy EvalPlus tylko dla „kamieni milowych” (koniec etapu, model finalny), zawsze z porównaniem parami z oryginałem. Najpierw sprawdzę na 4 gotowych modelach, czy zgodność tokenu odróżnia warstwę 13 od 26 tak jak pass@1 (~5 min GPU);
  - **B** — testy EvalPlus dla każdego wariantu (wolno, a różnice między wariantami i tak często w szumie);
  - **C** — A, a dla kamieni milowych dodatkowo pass@1 z losowaniem (np. 10 odpowiedzi na zadanie), co zmniejsza szum (najwyżej ~3×), ale kosztuje ~10× więcej czasu;
  - **D** — tylko KL, jak dotąd.
- **Rekomendacja:** A. Wynik warstwy 26 pokazuje, że sama KL może prowadzić w złą stronę przy wyborze warstw (np. omijalibyśmy końcowe warstwy, które dla kodu są tanie). Zgodność tokenu jest za darmo, a jej sprawdzenie na gotowych modelach zajmuje kilka minut.
- **Decyzja:** A

*2026-10-30 17:13 — Claude Opus 5.5*
