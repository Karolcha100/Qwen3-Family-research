# T015 · Punkty pass@1

*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem `*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*

---
---
---

Opisz mi tutaj czym są punkty pass@1

*2026-10-30 17:52 — Autor*

---
---
---

## Co masz zrobić

Nic, tylko przeczytać. Jeśli coś jest niejasne, dopisz pytanie tutaj.

### Czym jest pass@1

**pass@1 to odsetek zadań, w których pierwsza (jedyna) odpowiedź modelu przechodzi wszystkie testy.**

Jak to wygląda dla jednego zadania:
1. model dostaje początek programu: nagłówek funkcji i opis słowny, co ma robić, np. `def has_close_elements(numbers, threshold):` z opisem i przykładami;
2. model dopisuje treść funkcji; bierzemy jedną odpowiedź, zawsze najbardziej prawdopodobną (bez losowania);
3. gotowy kod uruchamiamy w kontenerze bez sieci razem z testami zadania;
4. zadanie jest **rozwiązane**, jeśli przejdą wszystkie testy. Każdy błąd, zły wynik albo przekroczenie czasu oznacza „nie”.

pass@1 = liczba rozwiązanych zadań / liczba wszystkich zadań.

Przykład: oryginalny model rozwiązuje 49 ze 164 zadań HumanEval, więc pass@1 = 49 / 164 = 29,9%.

„@1” oznacza, że model ma **jedną próbę**. Ogólniej pass@k to szansa, że co najmniej jedna z k prób jest dobra (np. pass@10: czy wśród 10 losowanych odpowiedzi jest choć jedna poprawna). My liczymy tylko pass@1, tak jak raport Qwen3.

### Wersje „+” (HumanEval+, MBPP+)

Te same zadania, ale z dużo większą liczbą testów, dodanych przez autorów EvalPlus. Wyłapują rozwiązania, które przechodzą kilka oryginalnych testów, ale są błędne, np. nie obsługują pustej listy. Rozwiązanie liczy się w „+” tylko wtedy, gdy przechodzi **i** testy oryginalne, **i** dodatkowe, dlatego wynik „+” jest zawsze niższy lub równy. Przykład dla oryginału: HumanEval 49 zadań (29,9%), HumanEval+ 38 zadań (23,2%).

### Co znaczą „punkty”

„Punkty” to **punkty procentowe**, czyli zwykła różnica dwóch odsetków. Przykład: HumanEval spada z 29,9% do 26,8% (z 49 do 44 rozwiązanych zadań):
- to **−3,1 punktu** (29,9 − 26,8);
- względnie to **−10%** wyniku (3,1 / 29,9).

W raportach piszę o punktach, bo tak porównuje się wyniki testów kodu w literaturze.

Ile jest wart jeden punkt:

| Zestaw | liczba zadań | 1 zadanie to |
|---|---|---|
| HumanEval (i +) | 164 | 0,61 punktu |
| MBPP (i +) | 378 | 0,26 punktu |

**„Średnia”** w raportach to średnia z czterech liczb: HumanEval, HumanEval+, MBPP, MBPP+. Tak samo liczy raport Qwen3 (36,23 dla tego modelu; u nas 36,9). Przykład: zmniejszenie warstwy 13 o 40% to średnia 34,2, czyli −2,7 punktu względem 36,9.

### Dlaczego mówię o szumie

Każde zadanie daje wynik 0 albo 1, więc mała zmiana w modelu może „przerzucić” zadania na granicy w obie strony. Model ze zmniejszoną warstwą 13 zyskał 5 zadań MBPP+, a stracił 15. Dlatego porównuję też parami (które zadania zyskał, a które stracił, względem oryginału) i liczę, czy strat jest wyraźnie więcej niż zysków (raport `AGENTS/phases/phase-2/etap-4c-k31-k38.md`, sekcja 7). Różnice 1–2 punktów między dwoma modelami są zwykle w granicach przypadku.

*2026-10-30 17:53 — Claude Opus 5.5*

---
---
---
