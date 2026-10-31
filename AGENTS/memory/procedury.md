# Procedury agenta — jak robię typowe rzeczy

Sprawdzone sposoby na powtarzalne czynności, żeby kolejna sesja (albo inny agent) nie wymyślała ich od nowa i nie popełniała tych samych błędów (`AGENTS/memory/pulapki.md`). Pełne zasady: `AGENTS/todo/llm/INSTRUKCJA.md`. Polecenia uruchamia się z katalogu projektu.

*2026-10-29 16:54 — Claude Opus 5.5*

---

## Co masz zrobić

Nic do decyzji. To notatnik agenta. Jeśli coś tu jest niezgodne z tym, jak chcesz pracować, napisz w @T006.

## 1. Start sesji (skrót)

1. `AGENTS/memory/w-toku.md`: czy poprzednia sesja nie została przerwana w połowie zadania. Jeśli tak, zaczynam od niego.
2. Plik Koniec z promptu autora + zmiany od ostatniego commitu:
   ```bash
   git status --short && git diff -U0 | grep -v '^@@\|^index\|^diff'
   ```
3. `AGENTS/memory/decyzje.md` (indeks decyzji) i `AGENTS/todo/llm/TODO-dla-LLM.md` (moje zadania).
4. Reszta według INSTRUKCJA.md (uwagi autora, raport, wątki, plany).

## 2. Czy GUI widzi to, co napisałem

Po każdej zmianie wątków, pytań, zadań albo planów:

```bash
python3 -c "
import pathlib
from agents_board.model import Board
b = Board(pathlib.Path('AGENTS'))
print('wątki:', [(t.extra['id'], t.owner, t.extra['closed']) for t in b.threads()])
print('pytania otwarte:', [i.extra['id'] for i in b.issues() if i.status == 'open'])
print('plany:', [(p.path, p.owner) for p in b.plans()])
print('zadania:', [(t.extra.get('id'), t.status) for t in b.todos()])
"
```

`owner == 'llm'` przy wątku albo planie znaczy, że czeka na autora.

## 3. Dopisanie wpisu do wątku lub dyskusji planu

Zawsze najpierw odczyt, potem osobny zapis (pułapka 1). Treść wpisu przygotowuję w pliku w scratchpadzie, a dopisuję tak:

```bash
python3 - <<'EOF'
import pathlib
path = pathlib.Path("AGENTS/talk/threads/T00X-....md")
entry = pathlib.Path("/ścieżka/do/wpisu.md").read_text()
content = path.read_text().rstrip()
path.write_text(content + "\n\n" + entry.strip() + "\n\n---\n---\n---\n")
EOF
```

Wpis zaczyna się od `## Co masz zrobić`, a kończy podpisem `*RRRR-MM-DD GG:MM — Claude …*` z godziną z `date "+%Y-%m-%d %H:%M"`.

## 4. Nowy wątek od agenta

```bash
python3 - <<'EOF'
import pathlib
from agents_board.model import thread_header
path = pathlib.Path("AGENTS/talk/threads/T00N-tytul-ascii.md")
assert not path.exists()
entry = "…"
path.write_text(thread_header("T00N", "Tytuł") + "\n\n---\n---\n---\n\n" + entry + "\n\n---\n---\n---\n")
EOF
```

Numer: następny po najwyższym w `AGENTS/talk/threads/`.

## 5. Blok odpowiedzi w raporcie autora (pod wpisem `### [A…]`)

```bash
python3 - <<'EOF'
import pathlib, re
path = pathlib.Path("AGENTS/todo/author/raport-TODO-autora.md")
task_id, title, body = "A10", "tytuł zadania", "**Co masz zrobić:** …\n\ntreść…"
signature = "*przeczytane i odpowiedziane: RRRR-MM-DD GG:MM — Claude …*"
lines = ["🤖 **ODPOWIEDŹ LLM — początek** (Claude …)", "", f"### [{task_id}] Re: {title}", ""] + body.split("\n") + ["", signature, "", "🤖 **ODPOWIEDŹ LLM — koniec**"]
block = "\n" + "\n".join(("> " + line) if line else ">" for line in lines) + "\n\n---\n"
text = path.read_text()
match = re.search(rf"^### \[{task_id}\] .*?^---\n", text, flags=re.S | re.M)
path.write_text(text[:match.end()] + block + text[match.end():])
EOF
```

Uwaga: wzór TeX w `body` w zwykłym stringu Pythona wymaga podwójnych `\\`.

## 6. Indeks decyzji (`AGENTS/memory/decyzje.md`)

Odświeżam na końcu sesji, gdy autor coś zdecydował:

```bash
python3 - <<'EOF'
import pathlib, re
from agents_board.model import Board
board = Board(pathlib.Path("AGENTS"))
rows = []
for issue in board.issues():
    phase = issue.path.split("/")[1]
    title = re.sub(r"^K\d+\.\s*", "", issue.title)
    decision = issue.extra["decision"].replace("\n", " ").replace("|", "/") or "— (czeka)"
    rows.append(((phase != "phase-0", phase, int(re.search(r"\d+", issue.extra["id"]).group())), f"| @{phase}:{issue.extra['id']} | {title} | {decision} |"))
path = pathlib.Path("AGENTS/memory/decyzje.md")
head = path.read_text().split("| Pytanie |")[0]
path.write_text(head + "| Pytanie | Tytuł | Decyzja |\n|---|---|---|\n" + "\n".join(row for _, row in sorted(rows)) + "\n")
EOF
```

Potem ręcznie poprawiam datę w linii „Wygenerowano”. Sortowanie: najpierw `phase-0`, potem pozostałe fazy alfabetycznie, w każdej według numeru K.

## 7. Praca w toku (`AGENTS/memory/w-toku.md`)

- **Przed** zadaniem dłuższym niż kilka kroków (instalacja, budowa, eksperyment): wpisuję zadanie, plan kroków i co już zrobione;
- **po każdym ukończonym kroku:** aktualizuję „Zrobione” i „Następny krok”;
- **po zakończeniu:** czyszczę sekcję „Teraz”, a wynik idzie do raportu L.

Dzięki temu po końcu kontekstu albo przerwie następna sesja wie, gdzie skończyłem.

## 8. Koniec sesji

1. Odpowiedzi we wszystkich miejscach (INSTRUKCJA.md).
2. `TODO-dla-LLM.md` (statusy L), `w-toku.md`, `decyzje.md` (sekcja 6), `stan-projektu.md`.
3. Briefing `AGENTS/talk/briefings/RRRR-MM-DD-GGMM.md` = treść odpowiedzi w czacie.
4. Commit i push:
   ```bash
   git add -A && git commit -q -m "…" && git push -q
   ```

## 9. Czego nie mogę zrobić sam

- zmienić własnych uprawnień (`.claude/settings.json`) ani utworzyć repo na GitHubie — tryb auto blokuje (pułapki 9–10). Daję autorowi polecenie w zadaniu A;
- `sudo` — zawsze zadanie A z poleceniami w blokach kodu, sprawdzonymi na żywym systemie (pułapka 11);
- GPU bez „uruchom” autora (@phase-0:K10, K33).

## 10. Kod i obliczenia (od Phase 2)

- Kod: pakiet `src/qwen_compression/`, skrypty w `scripts/`, testy w `tests/`. Przed commitem:
  ```bash
  uv run ruff format src scripts tests/test_qwen_compression.py && uv run ruff check src scripts tests/test_qwen_compression.py && uv run pyright src scripts tests/test_qwen_compression.py && CUDA_VISIBLE_DEVICES="" uv run pytest -q
  ```
- Testy liczą na CPU na małym losowym Qwen3. Porównania bardzo małych KL rób w float64 (`at_least_float32` zamiast `.float()`).
- Długie obliczenia: w tle (`run_in_background`), log w `results/<faza>/<etap>/log.jsonl`, skrypt pomija gotowe kroki (wznowienie tym samym poleceniem). Przed startem: `nvidia-smi` (czy GPU wolne) i wpis w `w-toku.md`.
- Pobieranie z Hugging Face: `HF_HUB_DOWNLOAD_TIMEOUT=60` (pułapka 14).
- **Kolejki obliczeń z paskiem postępu (@T014):** kroki z szacowanym czasem w `results/<faza>/…/queue.json` (`title`, `steps`: `name`, `estimate_minutes`, `command`, `log`), start w tle: `uv run --no-sync python scripts/run_queue.py results/…/queue.json` (zapisuje `AGENTS/postep-obliczen.json`, który GUI pokazuje jako pasek). Skrypty zgłaszają część zrobionej pracy przez `qwen_compression.progress.report_progress(ułamek)`. Szacunki czasu bierz z czasów poprzednich przebiegów (`seconds` w `results.jsonl`, czasy w `log.jsonl`). *(2026-10-30 14:26)*
- **Zmierzone czasy (RTX, 2026-10-30):** generowanie HumanEval / MBPP jednym modelem 2,3 / 3,5–3,8 min, testy w kontenerze 0,5 / 0,8–1,2 min (cały test kodu jednego modelu ~7 min); ocena jednego wariantu warstwy (KL Python + C4 + WikiText-2) ~56 s; trening celem za warstwą ~14 s/epokę; celem na wyjściu ~4,1 min/epokę w warstwie 13 i ~1,6 min/epokę w warstwie 26. Pole `seconds` wariantu `trained*` zawiera też ocenę (~56 s). *(2026-10-30 16:40)*
- **Zgodność tokenu (@phase-2:K43, 2026-11-01):** `scripts/phase2_code_token_agreement.py --mlps <katalog z .pt>` liczy KL i zgodność najbardziej prawdopodobnego tokenu na zestawie do KL oraz na odpowiedziach oryginału na zadania EvalPlus; kontrola: oryginał w bf16. Czas: ~3,5 min dla 9 wariantów + kontroli (~20 s na wariant). pass@k z 10 losowaniami: `phase2_code_generate.py --samples-per-task 10 --batch-size 30` (pamięć GPU ~9 GB). *(2026-11-01 00:04)*
