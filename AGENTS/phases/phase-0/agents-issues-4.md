# Phase 0 — pytania (runda 4): uruchamianie, wybór metod, kalibracja

*2026-10-29 15:03 — Claude Opus 5.5*

## Co masz zrobić

Cztery nowe decyzje po Twoich odpowiedziach z 14:58. K33 doprecyzowuje @phase-0:K10, K34 dotyczy @phase-0:K6, a K31 i K32 wynikają z raportu `AGENTS/phases/phase-0/A3-dane-kalibracyjne.md`. Wystarczy „rek” albo litera.

---

### K31. 🟢 Powtórzenia z kilkoma ziarnami

- **Problem:** inne losowe dane kalibracyjne (inne ziarno) dają nieco inny wynik. Gdy dwie metody różnią się o ułamek punktu perplexity, z jednego pomiaru nie wiadomo, czy to różnica metod, czy przypadek.
- **Opcje:**
  - **A** — zawsze 1 ziarno (najtaniej, ale bez wiedzy o szumie);
  - **B** — 3 ziarna dla każdego wariantu, wynik jako średnia ± odchylenie (3× dłużej);
  - **C** — na początku (Qwen3-0.6B) raz mierzymy szum na 3–5 ziarnach dla kilku metod, a potem 1 ziarno. Różnice mniejsze niż zmierzony szum oznaczamy jako „nierozstrzygnięte”.
- **Rekomendacja:** C. Raz poznajemy wielkość szumu i nie płacimy za nią przy każdym wariancie.
- **Decyzja:** Już chyba na to odpowiedziałem że B w innym pytaniu, ale ponów je jeśli nie.

### K32. 🟢 Format kalibracji dla modelu instrukcyjnego

- **Problem:** jeśli kompresujemy wersję instrukcyjną (zależy od @A2), można ją kalibrować na zwykłym tekście (C4) albo na dialogach w formacie czatu. Kalibracja na dialogach może lepiej chronić wykonywanie poleceń i tryb myślenia.
- **Opcje:**
  - **A** — zawsze C4 (prosto, tak jak Base);
  - **B** — dla wersji instrukcyjnej dialogi w szablonie czatu Qwen3 (np. z otwartego zbioru rozmów);
  - **C** — A jako standard, a B jako osobny eksperyment („czy kalibracja czatowa chroni IFEval i sędziego?”).
- **Rekomendacja:** C.
- **Decyzja:** A

### K33. 🟡 Co mogę robić bez Twojego „uruchom”

- **Problem:** w @phase-0:K10 zdecydowałeś, że uruchamiam obliczenia dopiero na Twoje polecenie. Nie wiem, czy to dotyczy też rzeczy, które nie zajmują GPU: instalacji pakietów Pythona, budowy llama.cpp (kilka minut CPU) i pobierania modeli (GB z internetu).
- **Opcje:**
  - **A** — „uruchom” potrzebne tylko do wszystkiego, co używa **GPU**; instalacje, budowę i pobieranie modeli robię sam, kiedy plan jest zatwierdzony;
  - **B** — „uruchom” potrzebne do GPU **i** do pobierania modeli/danych (bo zajmują łącze i dysk); instalacje i budowę robię sam;
  - **C** — „uruchom” potrzebne do wszystkiego poza edycją plików.
- **Rekomendacja:** A. Instalacje i budowa nie przeszkadzają w grze, a dzięki temu po Twoim „uruchom” od razu liczymy, zamiast czekać na pobieranie.
- **Decyzja:** A

### K34. 🟡 Jak chcesz wybierać metody

- **Problem:** w @phase-0:K6 zdecydowałeś: gotowe biblioteki, a metody wybierasz Ty. Żeby wybór był łatwy, mogę przygotować materiał.
- **Opcje:**
  - **A** — katalog metod: jeden plik z tabelą (metoda, rodzaj, idea w 2 zdaniach + wzór, biblioteka, czy działa z Qwen3, koszt na 12 GB, czego można się nauczyć); wybierasz z niego przy rozpisywaniu faz;
  - **B** — A plus mój proponowany zestaw startowy z uzasadnieniem (wybór zostaje przy Tobie);
  - **C** — nic nie przygotowuję; sam podajesz metody, a ja sprawdzam, czy są wykonalne.
- **Rekomendacja:** B. Najpierw Phase 1, więc katalog przygotuję w trakcie, a będzie gotowy, zanim zaczniesz rozpisywać Phase 2.
- **Decyzja:** B
