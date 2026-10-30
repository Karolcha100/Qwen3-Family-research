#!/usr/bin/env bash
cd "$(dirname "$0")/../../.."
status=results/phase2/code/queue-status.txt
data="$HOME/qwen3-checkpoints/phase2-code"
mlps="$HOME/qwen3-checkpoints/phase2-code/mlps"
evaluation=results/phase2/code-eval
common=(--measurement-sequences 0 1 2 3 --data-directory "$data" --stage2 results/phase2/code/stage2
  --evaluation-set "$data/evaluation-set.pt" --learning-rate 5e-5 --save-mlps "$mlps")
note() { echo "$1 $(date '+%H:%M')" >> "$status"; }
code_tests() {
  local name=$1; shift
  for dataset in humaneval mbpp; do
    uv run --no-sync python scripts/phase2_code_generate.py --dataset "$dataset" \
      --output "$evaluation/$name/$dataset.jsonl" "$@" > "$evaluation/$name-$dataset-generate.log" 2>&1
    note "generate $name $dataset exit $?"
    uv run --no-sync python scripts/phase2_code_evaluate.py --dataset "$dataset" \
      --samples "$evaluation/$name/$dataset.jsonl" > "$evaluation/$name-$dataset-evaluate.log" 2>&1
    note "evaluate $name $dataset exit $?"
  done
}
note "start"
code_tests original
uv run --no-sync python scripts/phase2_stage4_one_layer.py --layer 13 --importances code-only \
  --removed-fractions 0.2 0.4 --epochs 6 "${common[@]}" --output results/phase2/code/stage4 \
  > results/phase2/code/k38.log 2>&1
note "k38 exit $?"
uv run --no-sync python scripts/phase2_stage4_one_layer.py --layer 13 \
  --importances perturbation activation-rms random merged --removed-fractions 0.4 --epochs 16 "${common[@]}" \
  --output results/phase2/code/k31 > results/phase2/code/k31.log 2>&1
note "k31 exit $?"
uv run --no-sync python scripts/phase2_stage4_one_layer.py --layer 13 --importances perturbation \
  --removed-fractions 0.4 0.2 --epochs 6 --objective output "${common[@]}" \
  --output results/phase2/code/k37 > results/phase2/code/k37-13.log 2>&1
note "k37 layer 13 exit $?"
uv run --no-sync python scripts/phase2_stage4_one_layer.py --layer 26 --importances perturbation \
  --removed-fractions 0.4 --epochs 6 --objective output "${common[@]}" \
  --output results/phase2/code/k37 > results/phase2/code/k37-26.log 2>&1
note "k37 layer 26 exit $?"
code_tests layer13-40-window --mlps "$mlps/layer-13-perturbation-40-trained.pt"
code_tests layer13-40-output --mlps "$mlps/layer-13-perturbation-40-trained_output.pt"
note "all done"
