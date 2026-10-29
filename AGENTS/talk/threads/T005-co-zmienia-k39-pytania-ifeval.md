# T005 · Co zmienia K39 (pytania w stylu IFEval)

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

## Co masz zrobić

Przeczytaj. Na końcu jest jedna rzecz, która z tego wynika, i dwa nowe pytania o skład 200 pytań: @phase-0:K41 i @phase-0:K42. Jeśli wszystko jasne, możesz zamknąć wątek 🔒.

---

**Kontekst.** Prosiłeś o wyjaśnienie, co zmienia Twoja decyzja @phase-0:K39 = A („w naszych 200 pytaniach nie ma pytań w stylu IFEval”).

### Czym są pytania w stylu IFEval

IFEval (*Instruction-Following Eval*) to zbiór ~540 poleceń z **warunkami, które da się sprawdzić programem**, np.:
- „Napisz o kotach **dokładnie w 3 punktach**”;
- „Odpowiedz **w formacie JSON**”;
- „Użyj słowa *ocean* **co najmniej 2 razy**, całość **poniżej 100 słów**”.

Program sprawdza każdy warunek (0/1). Wynik to odsetek spełnionych poleceń. Mierzy więc jedną konkretną umiejętność: **czy model robi dokładnie to, o co go poproszono**.

### Przed decyzją (K22 = C, K28 = A) — sprzeczność

- część naszych 200 pytań miała być w stylu IFEval (~20 pytań);
- ale usunęliśmy metrykę regułową „format zgodny z poleceniem”, więc **nikt by nie sprawdził, czy te warunki są spełnione**. Model nagrody tego nie potrafi: nie policzy, czy jest dokładnie 3 punkty.

### Po decyzji K39 = A — co się zmienia

| | Przed | Po |
|---|---|---|
| Gdzie mierzymy wykonywanie poleceń | ~20 naszych pytań (bez sprawdzania) | **IFEval w lm-eval**: ~540 poleceń, sprawdzane programem (poziom 2) |
| Skład naszych 200 pytań | IFEval + MT-Bench + własne | **MT-Bench + inne źródła + własne** (skład: @phase-0:K41) |
| Metryka „format zgodny” | usunięta, ale potrzebna | niepotrzebna |
| Metryka 11 „wykonanie polecenia” z modelu nagrody | — | zostaje jako **miękka** ocena (czy trzyma się tematu i prośby) |

Co zyskujemy:
- **lepsza statystyka:** ~540 poleceń zamiast ~20. Przy 20 pytaniach jedno zepsute pytanie to 5 punktów procentowych różnicy;
- **bez dublowania** i bez metryki, której nikt nie liczy;
- **porównywalność:** IFEval w lm-eval jest standardem, więc wynik zestawimy z innymi publikacjami.

Co tracimy: nic istotnego. Jedyna różnica jest taka, że wykonywanie poleceń mierzymy na pytaniach IFEval, a nie na naszych.

### Co z tego wynika: skąd wziąć 200 pytań

**MT-Bench ma tylko 80 pytań** (8 kategorii po 10). Do tego każde ma dwie tury: pytanie i dopytanie. Żeby mieć 200 (@phase-0:K23 = C), potrzeba innych źródeł. Najbardziej znane:
- **Arena-Hard** (500 trudnych pytań z prawdziwych rozmów na Chatbot Arenie, dużo technicznych i programistycznych);
- **AlpacaEval** (805 różnorodnych, raczej prostszych poleceń).

Dwie decyzje:
- skład 200 pytań: @phase-0:K41;
- co z drugą turą MT-Bench: @phase-0:K42.

*2026-10-29 16:21 — Claude Opus 5.5*

---
---
---

🔒 Wątek zamknięty.

*2026-10-29 16:48 — Autor*

---
---
---
