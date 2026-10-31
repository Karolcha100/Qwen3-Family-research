# Zasady współpracy z autorem

Skrót ustaleń. Pełne brzmienie: `AGENTS/todo/llm/INSTRUKCJA.md`, `AGENTS/README.md`, `AGENTS/talk/od-autora-dla-llmow.md`.

*Szablon z projektu economics-model-pol-vs-rus, 2026-10-29*

---

## Cykl pracy

1. Autor odpowiada w GUI (`python3 -m agents_board`) i klika **✅ Koniec**. Powstaje `AGENTS/talk/koniec/RRRR-MM-DD-GGMM.md` z listą jego działań, a do schowka trafia prompt.
2. Autor wkleja w czacie: „Odpowiedziałem w AGENTS board. Podsumowanie: AGENTS/talk/koniec/… Przeczytaj je i kontynuuj według AGENTS/todo/llm/INSTRUKCJA.md.”
3. Agent czyta plik Koniec i **tylko pliki zmienione od ostatniego briefingu** (`git status`, `git diff`). Nie czyta wszystkiego od nowa.
4. Agent odpowiada:
   - w wątkach — wpis na końcu wątku;
   - w raporcie autora — blok „🤖 ODPOWIEDŹ LLM”, jeden na zadanie;
   - w planach — wpis w sekcji `## Dyskusja`;
   - aktualizuje TODO, raport agentów, plany i pamięć.
5. Na koniec: **briefing** `AGENTS/talk/briefings/RRRR-MM-DD-GGMM.md` z tą samą treścią co odpowiedź w czacie, potem **commit**.

## Kanały, w których autor może pisać

Tylko przez GUI: Decyzja w pytaniu, odpowiedź końcowa w pytaniu 🔄, raport autora i status zadania, wątki, dyskusja planu, uwagi dla LLM, Koniec. Do tego czat. **Inne pliki są dla niego tylko do czytania** — nigdy nie pisz „odpowiedz w pliku X”. Tabela: `AGENTS/todo/llm/INSTRUKCJA.md`, sekcja „Gdzie autor może odpisywać”.

## Odpowiedź w czacie

Tylko dwie części (ta sama treść idzie do briefingu):

- **Zmiany:** linki do plików z oznaczeniem CRE / MOD / DEL;
- **Do odpowiedzi:** miejsce w drzewie GUI (np. „Co czeka na mnie → Wątki — agent odpowiedział → @T003”) i bardzo krótki opis.

Reszta treści trafia do plików w `AGENTS/`.

## Stałe reguły

- **Commit i push po każdym prompcie autora:** sensowny opis, potem `git push` (@phase-0:K17 = B).
- **Obliczenia na GPU (@phase-0:K10 = B z zastrzeżeniem):** agent pisze kod i polecenia, ale **uruchamia je dopiero, gdy autor powie „uruchom”** (w GUI albo w czacie). Autor nie wpisuje poleceń sam. Bez takiego polecenia nic na GPU. Instalacje pakietów, budowę (CPU) i pobieranie modeli/danych agent robi sam, gdy plan jest zatwierdzony (@phase-0:K33 = A).
- **Wzory w TeX z opisem słownym** przy sprawach technicznych i matematycznych (uwaga 2 w `AGENTS/talk/od-autora-dla-llmow.md`).
- **Decyzje zawsze jako pytania w `AGENTS/phases/<faza>/agents-issues-N.md`, każda osobno** (`### K1. …` z opcjami, rekomendacją i polem Decyzja), a nie jako lista pytań w wątku. Autor **chce dużo pytań**, także o drobne decyzje, które teraz nie mają znaczenia, ale mogą mieć 200 decyzji dalej. Lepiej zapytać niż przyjąć coś po cichu. Wątek służy do rozmowy i opinii (źródło: @T001, 2026-10-29). Pytania organizacyjne, niezwiązane z jedną fazą, trafiają do `AGENTS/phases/phase-0/`.
- **Polecenia dla autora zawsze w blokach kodu** (` ```bash … ``` `, każde w osobnej linii), nigdy w tekście w pojedynczych backtickach (uwaga 1 w `AGENTS/talk/od-autora-dla-llmow.md`).
- **Nie zakładaj z góry, co będziemy robić.** Metody i dalsze fazy wybiera i rozpisuje autor (@phase-0:K2, K6). Przy K12 i K30 autor zwrócił uwagę: „jeszcze nie wiesz, jakie metody będziemy robić”. Nie projektuj struktury kodu, katalogów ani przepływu pod metody, których autor nie wybrał. Pytania zależne od metod oznaczaj jako warunkowe albo odłóż do czasu, aż autor opisze fazy. **Kierunek badań wyznacza główny pomysł autora (@T009, 2026-10-29): A — zaburzanie neuronów i pomiar skutku, B — rodzaje neuronów na wykresach, C — zmniejszanie warstw z rekonstrukcją i dotrenowaniem.** Klasyczna kwantyzacja nie jest głównym kierunkiem (@phase-0:K8). Metody z katalogu to materiał poboczny i punkty odniesienia.
- **Cel autora: zmniejszać modele tak, żeby zachowały sens** (uwaga 3 w `AGENTS/talk/od-autora-dla-llmow.md`). Nie pisz „czego to uczy” ani wątków edukacyjnych przy metodach, chyba że autor o to poprosi. Raporty wyjaśniające pisz tylko na prośbę.
- **Odpowiedzi w wątkach mają być uporządkowane:** najpierw kontekst (na jakie pytanie autora odpowiadam), potem nagłówki, które go powtarzają. Żadnych „punktów 1, 2” bez powiązania z pytaniem (uwaga autora w @T002, 15:11).
- **„Co ty na to?”, „co sądzisz?”, „jak widzisz?”** to pytanie o opinię: plusy, minusy, rekomendacja — **nic nie uruchamiasz**. Działasz dopiero po „zgoda”, „robimy”, „start”.
- **Każdy plik dla autora zaczyna się od „## Co masz zrobić”:** problem prostymi słowami i pytanie z gotowymi opcjami (np. „wystarczy: zgoda, B”).
- **Jeden plik na zadanie** (plan, raport, propozycja), podlinkowany w zadaniu. Plik zbiorczy tylko jako spis.
- **Podpis:** `*RRRR-MM-DD GG:MM — <model>*`, godzina zawsze z `date "+%Y-%m-%d %H:%M"` tuż przed podpisem, nigdy szacowana.
- **Wątki:** wpisy rozdzielone **trzema** liniami `---`; każdy wpis kończy się podpisem, a po nim są trzy linie `---`.
- **Nie edytujemy cudzych ani wcześniejszych wpisów** (wątki, raporty, decyzje). Wyjątek: naprawa ewidentnych uszkodzeń, z adnotacją.
- **Wzory w TeX:** w tekście `$…$`, osobno `$$…$$`, nie w blokach kodu. Kwoty pisz „0,5 $” (spacja przed `$`).
- **Język:** komunikacja i pliki w `AGENTS/` po polsku; kod, nazwy plików i `README.md` projektu po angielsku (chyba że autor zdecyduje inaczej). Nazwy plików bez polskich znaków.
- **Pliki tymczasowe agentów** tylko w katalogu tymczasowym sesji (scratchpad), nigdy w repozytorium.

## Styl autora

- Krótkie odpowiedzi w GUI („zgoda”, „tak”, „B”). Gdy pisze ogólnie („rozpisz mi…”), agent proponuje opcje z rekomendacją.
- Ceni, gdy agent przyznaje się do błędu i od razu go naprawia.
- Nie lubi szukać, na co ma odpowiedzieć — pytanie zawsze na górze, z opcjami.
- **Wyniki testów kodu podawaj jako liczby zadań** (oryginał vs nasz model, np. „38 → 34 z 164”, ile zyskane / stracone), procenty najwyżej obok; interesuje go też pass@2 i pass@3, nie tylko pass@1 (@T015).
- Woli **jedną metodę zamiast wielu**: cel treningu za warstwą i wybór warstw pełnych mało ważnych neuronów według mapy, mapa 75/25 (dyskusja `etap-4c-k31-k38.md`, 2026-10-30 18:28).
- **Docelowo zmniejszamy środkowe warstwy**, nie początkowe i końcowe (@phase-2:K44, 2026-10-31). Przepis domyślny (@T017): mapa 75/25 → najmniejsze kwadraty → 6 epok celem za warstwą, krok $5 \cdot 10^{-5}$.

*Zmiana: 2026-10-29 — reguła: decyzje jako osobne pytania w agents-issues, pytamy dużo (@T001) — Claude Opus 5.5*
*Zmiana: 2026-10-29 — polecenia dla autora w blokach kodu (uwaga 1) — Claude Opus 5.5*
*Zmiana: 2026-10-29 15:45 — nie zakładać metod z góry; porządek odpowiedzi w wątkach — Claude Opus 5.5*
*Zmiana: 2026-10-29 16:23 — co wolno bez „uruchom” (K33) — Claude Opus 5.5*
*Zmiana: 2026-10-29 19:33 — główny pomysł autora jeszcze nieznany (K8) — Claude Opus 5.5*
*Zmiana: 2026-10-29 20:48 — główny pomysł autora znany (@T009) — Claude Opus 5.5*
*Zmiana: 2026-10-29 21:12 — cel autora, bez „czego to uczy” (uwaga 3) — Claude Opus 5.5*
*Zmiana: 2026-10-30 18:39 — liczby zadań zamiast punktów, jedna metoda (@T015, dyskusja etapu 4c) — Claude Opus 5.5*
*Zmiana: 2026-11-01 00:04 — środkowe warstwy, przepis domyślny (@phase-2:K44, @T017) — Claude Opus 5.5*
