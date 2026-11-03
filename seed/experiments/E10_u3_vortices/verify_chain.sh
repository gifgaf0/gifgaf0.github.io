#!/bin/bash
# Amendment A verification: run order after verify_orig.py (each step resumable; re-run this script after a restart).
cd "$(dirname "$0")"
until grep -q regenerated log_verify_orig.txt; do sleep 30; done
grep -q "solve done" log_verify_V1a.txt 2>/dev/null || python3 verify_v1.py solve V1a >> log_verify_V1a.txt 2>&1
grep -q "solve done" log_verify_V1b.txt 2>/dev/null || python3 verify_v1.py solve V1b >> log_verify_V1b.txt 2>&1
[ -f verify_V1a.json ] || python3 verify_v1.py analyse V1a >> log_verify_V1a.txt 2>&1
[ -f verify_V1b.json ] || python3 verify_v1.py analyse V1b >> log_verify_V1b.txt 2>&1
python3 verify_v2.py solve >> log_verify_V2.txt 2>&1 &
grep -q "solve done" log_verify_V1c.txt 2>/dev/null || python3 verify_v1.py solve V1c >> log_verify_V1c.txt 2>&1
[ -f verify_V1c.json ] || python3 verify_v1.py analyse V1c >> log_verify_V1c.txt 2>&1
wait
python3 verify_v2.py analyse >> log_verify_V2.txt 2>&1
echo "chain done" >> log_verify_V1c.txt
