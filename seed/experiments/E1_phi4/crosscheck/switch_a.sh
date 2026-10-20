#!/bin/bash
# wait until the first DSV case is written, then stop worker A (by PID) and start stage 2
cd "$(dirname "$0")"
until [ -s xc2_dsv.jsonl ]; do sleep 5; done
kill 14382 14386
sleep 1
nohup ./run_xc2_a2.sh > logs/xc2_a2.log 2>&1 &
echo switched
