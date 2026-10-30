#!/usr/bin/env bash
set -u
cd /home/karol/Pulpit/Badania-LLM/Qwen3
status=results/phase2/code/status.txt
while kill -0 "$(cat results/phase2/k23/chain.pid)" 2>/dev/null; do sleep 30; done
echo "k23 finished $(date '+%H:%M')" >> "$status"
uv run --no-sync python scripts/phase2_stage2_fisher_map.py \
  --data-path "$HOME/qwen3-checkpoints/phase2-code/measurement-set.pt" --output results/phase2/code/stage2 \
  > results/phase2/code/fisher.log 2>&1
echo "fisher exit $? $(date '+%H:%M')" >> "$status"
uv run --no-sync python scripts/phase2_code_map.py > results/phase2/code/code-map.log 2>&1
echo "code map exit $? $(date '+%H:%M')" >> "$status"
learning_rate=$(uv run --no-sync python - <<'PYTHON'
import json
from pathlib import Path
best = {}
for learning_rate in ("5e-5", "2e-4"):
    path = Path(f"results/phase2/k23/lr-{learning_rate}/layer-13/results.jsonl")
    if path.exists():
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        trained = [row["kl"] for row in rows if row["variant"] == "trained" and row["removed_fraction"] == 0.4]
        if trained:
            best[learning_rate] = trained[0]
print(min(best, key=best.get) if best else "5e-5")
PYTHON
)
echo "learning rate $learning_rate" >> "$status"
common=(--removed-fractions 0.2 0.4 --epochs 6 --learning-rate "$learning_rate"
  --measurement-sequences 0 1 2 3 --data-directory "$HOME/qwen3-checkpoints/phase2-code"
  --stage2 results/phase2/code/stage2 --evaluation-set "$HOME/qwen3-checkpoints/phase2-code/evaluation-set.pt"
  --output results/phase2/code/stage4)
uv run --no-sync python scripts/phase2_stage4_one_layer.py --layer 13 --importances perturbation previous-map \
  "${common[@]}" > results/phase2/code/stage4-layer-13.log 2>&1
echo "layer 13 exit $? $(date '+%H:%M')" >> "$status"
for layer in 2 26 14; do
  uv run --no-sync python scripts/phase2_stage4_one_layer.py --layer "$layer" --importances perturbation \
    "${common[@]}" > "results/phase2/code/stage4-layer-$layer.log" 2>&1
  echo "layer $layer exit $? $(date '+%H:%M')" >> "$status"
done
echo "all done $(date '+%H:%M')" >> "$status"
