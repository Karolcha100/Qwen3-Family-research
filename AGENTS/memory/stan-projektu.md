# Stan projektu

Krótko: co już jest, co teraz robimy, co dalej i jakie decyzje czekają. Agent aktualizuje ten plik na końcu sesji, gdy coś się zmieniło.

*Szablon, 2026-10-29*

---

## Gdzie jesteśmy

- **Cel:** nauka for fun — badania nad kompresją LLM (kwantyzacja, pruning, rozkłady niskiego rzędu, destylacja) na rodzinie **Qwen3** (0.6B → 1.7B → 4B → 8B). Pełny kontekst z rozmowy 27–29.10.2026: `local-llm-conversation.md`.
- **Sprzęt:** RTX 4070 SUPER 12 GB (sm_89), Ryzen 7 9700X, 30 GiB RAM, Fedora 44, zsh z oh-my-zsh, GCC 16, sterownik NVIDIA 615.78.08 (RPM Fusion, nie ruszamy). Python systemowy 3.14.8. Miniconda w `~/miniconda3` (zsh init zrobiony, `auto_activate` wyłączone) — tylko zapas.
- **Repo:** `github.com/Karolcha100/Qwen3-Family-research` (prywatne). Commit + push po każdej sesji (@phase-0:K17 = B); pozwolenie `Bash(git push)` w `.claude/settings.json` (@A5).
- **Decyzje (phase-0):** K1 GitHub; K2 rozpisujemy tylko Phase 1, dalsze fazy autor; K3 instalacje z `sudo` jako zadania A (@A6–@A8); K4 **uv**; K5 **Python 3.14**; K6 **gotowe biblioteki, metody wybiera autor**; K10 agent pisze kod, **uruchamia na GPU tylko na „uruchom” autora**; K11 wyniki w `results/*.jsonl`; K12 pakiet `src/…` „spoko”, ale **struktura dopiero po wyborze metod**; K15 notatki do nauki przy każdej metodzie; K16 `phase-0` na pytania ogólne; K17 commit + push; K30 zapisujemy tylko wybrane checkpointy (poza repo). K32 kalibracja zawsze C4; K33 bez „uruchom” wolno instalować, budować i pobierać (po zatwierdzeniu planu), GPU tylko na „uruchom”; K34 katalog metod + propozycja (`AGENTS/phases/phase-0/katalog-metod.md`, L1); K35 szum ziaren mierzony raz na 0.6B. K7 = A (Base do perplexity/KL/lm-eval, instrukcyjny do evalplus/IFEval/klasyfikatorów); K8 = C (kalibracja: mieszanka C4 + kod), ale **autor ma główny pomysł, inny niż klasyczna kwantyzacja, jeszcze nieopisany**; K9 = A (okna 2048 bez nakładania); K14 = A (ruff, pyright, pytest).
- **Phase 1 (środowisko): ✅ skończona 2026-10-29 20:47.** CUDA 13.4.92, llama.cpp z CUDA (`~/llama.cpp`, commit `eb4e244be`), uv + Python 3.14 + torch 2.15.0+cu134. Testy: PPL WikiText-2 (okna 2048) Base 12,67, instrukcyjny 20,97; ~28 tys. tok/s przebiegu. Raport: `AGENTS/phases/phase-1/srodowisko.md`. GGUF i dane: `~/qwen3-checkpoints/`.
- **Główny pomysł autora (@T009):** A zaburzenia neuronów MLP (δ ∈ {−1, −0,5, 0,5, 1}) i pomiar skutku, B rodzaje neuronów na wykresach, C zmniejszanie warstw (wybór neuronów, rekonstrukcja lokalna, dotrenowanie). Decyzje: neuron = neuron MLP (K1 A), zaburzenie mnożące (K2 A), miara KL (+ generacja i klasyfikator dla top ~250, K3 A), pilot (K4 C), trening warstwy „przez następną” (K5 B), dane na dysk (K6), start z najmniejszych kwadratów (K7 A), dotrenowanie najpierw tylko zmniejszonych warstw, potem LoRA (K8 D). **Phase 2 = etapy 1–4** (K9): plan `AGENTS/phases/phase-2/plan-phase-2.md` **zatwierdzony 2026-10-29 21:36**; **etapy 1–4 policzone w nocy 29/30.10** (raporty `AGENTS/phases/phase-2/etap-1-pilot.md`, `etap-2-mapa.md`, `etap-3-rodzaje-neuronow.md`, `etap-4-jedna-warstwa.md`; wyniki `results/phase2/`): zaburzenia tylko w float32, $\mathrm{KL} \propto \delta^2$, mapa = przesiew Fishera na 131 tys. tokenów (zgodność z pomiarem dokładnym 0,96–0,99), ranking zależy od tekstu (tekst vs kod ≈ niezależne), krytyczne neurony głównie w warstwie 27 i 2, warstwa 13 −40% neuronów → PPL +0,5%; K10–K15 rozstrzygnięte (tekst 75% C4 + 25% kod, pilot na warstwach 2/13/25, 1 mln tokenów na dysk, stopnie −5/−10/−20/−40%, pakiet `src/qwen_compression/`). **Cel autora: zmniejszać modele, zachowując sens** (uwaga 3). **2026-10-30: autorowi najbardziej zależy, żeby model dobrze programował** (dyskusja `etap-2-mapa.md`); mapa 75% tekst / 25% kod chroni głównie tekst → pytania @phase-2:K25–K30. **2026-10-30 11:30–13:00 (@L18, raport `AGENTS/phases/phase-2/etap-4b-kod.md`):** dane Python/C4 75/25, mapa kodu (75/25 ważona); start z mapy kodu → KL na Pythonie −37% vs stara mapa (C4 +30%); warstwy 13/14 najlepsze, 2/26 ~3,5× gorsze; trening po najmniejszych kwadratach daje 1–20% (16 epok zamiast 4: −5%) → pytanie o cel treningu @phase-2:K37; waga mapy @phase-2:K38; K31–K38 = A (2026-10-30 13:59); przygotowane (@T013), kolejka czeka na @phase-2:K39. **2026-10-30 14:31–17:15 (@L20, raport `AGENTS/phases/phase-2/etap-4c-k31-k38.md`):** oryginał EvalPlus 36,9 (raport Qwen3 36,23); warstwa 13 −40% → pass@1 −2,7 pkt, warstwa 26 −40% → 0 pkt mimo 3× większej KL (KL nie przewiduje pass@1 między warstwami); start z mapy najlepszy także po 16 epokach (losowy +64%), scalanie neuronów gorsze niż usuwanie; cel na wyjściu pomaga w w. 26 (−18% KL), nie w w. 13; mapa 100% kod: Python −11–17%, C4 +25–35%. Pytania @phase-2:K40–K43 (`agents-issues-8.md`). 18:28: autor woli jeden cel (za warstwą), wybór warstw z mapy i mapę 75/25; mapa wskazuje warstwy 20–25 jako najtańsze; raport `porownanie-z-oryginalem.md` (oryginał 200 zadań „+” z 542, w. 26 −40%: 205, w. 13 −40%: 184–191); pytania K44 (pass@2/3), K45 (warstwy 20–25) w `agents-issues-9.md`. Ocena kodu: EvalPlus w kontenerze `qwen-code-sandbox` (bez sieci), klasyfikator odłożony. **2026-10-31/11-01:** K40 = C (cel za warstwą wszędzie), K41 = A (75/25), K42 = A (scalanie porzucone, wynik negatywny), K43 = A, K44 = A bez w. 26 (docelowo środkowe warstwy); K43: zgodność tokenu na odpowiedziach oryginału na zadania EvalPlus odtwarza kolejność testów kodu (w. 26 99,44% ≈ szum bf16 99,59%; w. 13 98,3–98,7%), zgodność na zwykłym kodzie nie; raport `k43-zgodnosc-tokenu.md`, pytanie K46 (`agents-issues-10.md`). Noc 1.11: K44 i warstwy 10, 15, 17, 18, 20–25.
- **Ewaluacja (@T002):** 1) perplexity + KL, 2) lm-eval (z IFEval) + evalplus, 3) **klasyfikatory, bez sędziów generatywnych**: 4 reguły (K28) + wieloatrybutowy model nagrody (K29 = B, np. ArmoRM; wybór modelu: K18 „do rozważenia”). 200 pytań po angielsku (K21, K23), mieszanka źródeł (K22), sampling 3 odpowiedzi (K24), **tryb myślenia włączony** (K25), ocena bezwzględna + parami z BF16 (K20), ręczna kalibracja ~50 odpowiedzi w HTML (K26). Lista metryk: `AGENTS/phases/phase-0/plan-metryki-oceny.md` (do opiniowania). K37 limit 8192 tokenów; K38 model nagrody widzi tylko odpowiedź końcową; K39 bez pytań IFEval w naszych 200 (@T005); K40 metryka zgodności z wzorcem. K36: porównanie z BF16 + percentyle + ranking Elo (sekcja D planu metryk). K41 = C: 80 MT-Bench + 60 Arena-Hard + 40 AlpacaEval + 20 własnych; K42 = B: obie tury MT-Bench (druga oceniana osobno).
- **Kod:** Python 3.14, z typami, po angielsku, bez komentarzy, pełne nazwy zmiennych.

## Następny krok

1. Autor: odpowiedzi na K16–K24 (`AGENTS/phases/phase-2/agents-issues-3.md`), najważniejsze K17 (mapa z przesiewu) i K21 (warstwy w etapie 4).
2. Agent: według odpowiedzi (np. inne warstwy w etapie 4, dłuższy trening K23, zmiana nazwy folderu K19, poprawka GUI K22/@L14).

## Otwarte decyzje autora

- K16–K24 w `AGENTS/phases/phase-2/agents-issues-3.md`.
- Plan do opinii: `AGENTS/phases/phase-0/katalog-metod.md`.

*Zmiana: 2026-10-29 15:03 — decyzje K3–K17, zadania A5–A8, raporty A2–A4 — Claude Opus 5.5*
*Zmiana: 2026-10-29 15:45 — decyzje K11–K31, ocena klasyfikatorami — Claude Opus 5.5*
*Zmiana: 2026-10-29 16:23 — decyzje K32–K40, katalog metod, push skonfigurowany — Claude Opus 5.5*
*Zmiana: 2026-10-29 16:56 — K41/K42, notatniki agenta (@T006) — Claude Opus 5.5*
*Zmiana: 2026-10-29 19:33 — K7/K8/K9/K14/K36 zamknięte, główny pomysł autora — Claude Opus 5.5*
*Zmiana: 2026-10-29 19:49 — plan Phase 1 zatwierdzony, llama.cpp sklonowane, raport ASVD/SVD-LLM — Claude Opus 5.5*
*Zmiana: 2026-10-29 20:17 — CUDA 13.4 i llama.cpp gotowe — Claude Opus 5.5*
*Zmiana: 2026-10-29 20:22 — środowisko Pythona gotowe (L2) — Claude Opus 5.5*
*Zmiana: 2026-10-29 20:48 — Phase 1 skończona, główny pomysł autora — Claude Opus 5.5*
*Zmiana: 2026-10-29 21:13 — decyzje K1–K9 pomysłu, plan Phase 2 — Claude Opus 5.5*
*Zmiana: 2026-10-29 21:34 — K3, K10–K15 rozstrzygnięte — Claude Opus 5.5*
*Zmiana: 2026-10-29 21:49 — plan Phase 2 zatwierdzony, kod etapu 1 gotowy — Claude Opus 5.5*
*Zmiana: 2026-10-30 04:32 — Phase 2 etapy 1–4 policzone, pytania K16–K24 — Claude Opus 5.5*
