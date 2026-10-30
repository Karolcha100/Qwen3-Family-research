# Główny pomysł — pytania (runda 7): uruchomienie obliczeń z decyzji K31–K38

*2026-10-30 14:12 — Claude Opus 5.5*

## Co masz zrobić

Wszystko z decyzji K31–K38 jest przygotowane i sprawdzone bez GPU (szczegóły: @T013). Według @phase-0:K10 GPU uruchamiam dopiero na Twoje „uruchom”, więc pytam o to wprost. Wystarczy „A”.

---

### K39. 🔴 Uruchomić kolejkę obliczeń K31–K38?

- **Problem:** kolejka `results/phase2/code/queue.sh` robi po kolei:
  1. HumanEval(+) i MBPP(+) dla oryginalnego modelu (K32, K34, K35): czy odtwarzamy ~36% z raportu Qwen3;
  2. mapa 100% kod na warstwie 13 (K38);
  3. punkt startu przy długim treningu, warstwa 13, 40%: mapa, średnia aktywacja, losowy, połączone neurony (K31);
  4. trening z celem na wyjściu modelu: warstwa 13 (40%, 20%) i 26 (40%) (K37);
  5. HumanEval(+) i MBPP(+) dla modelu ze zmniejszoną warstwą 13 (40%): trening za następną warstwą vs trening na wyjściu modelu.

  Czas według mojego szacunku: 3–3,5 h GPU (najdłuższy jest krok 4, którego jeszcze nie mierzyłem na GPU). Kod napisany przez model uruchamia się tylko w kontenerze bez sieci (K36).
- **Opcje:**
  - **A** — uruchom całą kolejkę;
  - **B** — uruchom tylko kroki 1–3 (~1,5 h), krok 4 po obejrzeniu wyników;
  - **C** — jeszcze nie uruchamiaj.
- **Rekomendacja:** A. Kroki są niezależne, a wyniki trafią do jednego raportu.
- **Decyzja:** A, uruchom teraz

*2026-10-30 14:12 — Claude Opus 5.5*
