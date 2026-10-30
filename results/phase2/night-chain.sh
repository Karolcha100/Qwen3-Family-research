#!/usr/bin/env bash
cd /home/karol/Pulpit/Badania-LLM/Qwen3
export HF_HUB_DOWNLOAD_TIMEOUT=60
.venv/bin/python scripts/phase2_stage4_one_layer.py --layer 13 --measurement-sequences 0 1 2 3 4 5 6 7 >> results/phase2/stage4/stdout.log 2>&1
echo "stage4 exit $?" >> results/phase2/night-chain.log
.venv/bin/python scripts/phase2_stage2_full_map.py --mode screened >> results/phase2/stage2/stdout.log 2>&1
echo "stage2 exit $?" >> results/phase2/night-chain.log
