#!/bin/bash
# E10 QB: after a container restart, relaunch the chain (runs resume from checkpoints / skip if done) and autocommit.
cd "$(dirname "$0")"
pip install -q scipy==1.18.1 numba==0.68.1 2>/dev/null
grep -q "CHAIN DONE" log_qb_chain.txt 2>/dev/null || pgrep -f "[q]b_chain.sh" >/dev/null || (setsid nohup ./qb_chain.sh >> log_qb_chain.txt 2>&1 < /dev/null &)
pgrep -f "[q]b_autocommit.sh" >/dev/null || (setsid nohup ./qb_autocommit.sh > /dev/null 2>&1 < /dev/null &)
