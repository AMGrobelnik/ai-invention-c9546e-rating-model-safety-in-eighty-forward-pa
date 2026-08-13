#!/usr/bin/env bash
# Run every panel member in its OWN process (one model resident at a time),
# checkpointing to results/member_<key>.json so a crash costs one member, not
# the run.  The HF snapshot is deleted after each member: 19 checkpoints is
# ~47 GB and the disk holds 40 GB.
set -u
cd "$(dirname "$0")"
PY=.venv/bin/python
ORDER="${1:-l1_instruct l1_abliterated l1_base l6_instruct l6_base l3_instruct l3_abliterated l3_base l4_instruct l4_abliterated l4_base l2_instruct l2_abliterated l2_uncensored l2_base l5_instruct l5_base l7_instruct l7_base}"

for key in $ORDER; do
  if [ -f "results/member_${key}.json" ] && \
     grep -q '"status": "OK"' "results/member_${key}.json" 2>/dev/null; then
    echo "[panel] $key already done, skipping"
    continue
  fi
  echo "[panel] === $key === $(date -u +%H:%M:%S)"
  timeout 3600 $PY method.py --stage member --member "$key" --tier full \
      > "logs/member_${key}.log" 2>&1
  rc=$?
  echo "[panel] $key exit $rc  $(date -u +%H:%M:%S)"
  grep -E "alpha_50=|AMS sigma|behaviour block|up-ramp|survival:|DONE|ERROR" \
      "logs/member_${key}.log" | tail -8
  # free the disk: keep nothing but the tokenizer-sized leftovers
  rm -rf ~/.cache/huggingface/hub/models--* 2>/dev/null
  df -h / | tail -1
done
echo "[panel] all done $(date -u +%H:%M:%S)"
