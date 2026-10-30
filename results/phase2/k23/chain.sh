#!/usr/bin/env bash
set -u
cd /home/karol/Pulpit/Badania-LLM/Qwen3
for learning_rate in 5e-5 2e-4; do
  uv run --no-sync python scripts/phase2_stage4_one_layer.py --layer 13 \
    --removed-fractions 0.2 0.4 --importances perturbation --epochs 16 --learning-rate "$learning_rate" \
    --measurement-sequences 0 1 2 3 4 5 6 7 --output "results/phase2/k23/lr-$learning_rate" \
    > "results/phase2/k23/lr-$learning_rate.log" 2>&1
  echo "lr $learning_rate exit $?" >> results/phase2/k23/status.txt
done
