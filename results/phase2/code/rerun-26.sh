#!/usr/bin/env bash
cd "$(dirname "$0")/../../.."
status=results/phase2/code/status.txt
uv run --no-sync python scripts/phase2_stage4_one_layer.py --layer 26 --importances perturbation \
  --removed-fractions 0.2 0.4 --epochs 6 --learning-rate 5e-5 --measurement-sequences 0 1 2 3 \
  --data-directory "$HOME/qwen3-checkpoints/phase2-code" \
  --stage2 results/phase2/code/stage2 --evaluation-set "$HOME/qwen3-checkpoints/phase2-code/evaluation-set.pt" \
  --output results/phase2/code/stage4 > results/phase2/code/stage4-layer-26.log 2>&1
echo "layer 26 rerun (fixed target) exit $? $(date '+%H:%M')" >> "$status"
