#!/bin/sh
# smoke_028.sh -- generator benchmark + integrity suite on 10 smoke strata at 5e11 and a boundary smoke of
# 20 strata at 2.1e12 (just above the band, lower prime density than any band stratum; both outside the band).
# Seed 'smoke-028'. No character statistic is computed on these primes (build_028 compares tables only).
set -u
S=${SMOKE_DIR:-/home/claude/smoke028}; rm -rf $S; mkdir -p $S
echo "== generate 10 smoke strata at y0 = 5e11 (one process)"
T0=$(date +%s.%N); python3 gen_028.py smoke-028 $S/data 0 10 --y0 5e11 --chunk 5; T1=$(date +%s.%N); python3 -c "print('wall %.1f s for 10 strata' % ($T1 - $T0))"
echo "== build (expect 0 failures)"
python3 build_028.py smoke-028 $S/data --y0 5e11 --M 10 --nverify 10 --write-hashes $S/hashes.json; echo "exit $?"
echo "== build again against the recorded hashes (expect 0 failures)"
python3 build_028.py smoke-028 $S/data --y0 5e11 --M 10 --nverify 0 --hashes $S/hashes.json; echo "exit $?"
echo "== NEGATIVE: wrong seed (expect failures)"
python3 build_028.py smoke-028-wrong $S/data --y0 5e11 --M 10 --nverify 0; echo "exit $?"
echo "== NEGATIVE: missing data directory (expect failure)"
python3 build_028.py smoke-028 $S/nonexistent --y0 5e11 --M 10 --nverify 0; echo "exit $?"
echo "== NEGATIVE: wrong range (decisive band y0 = 1.05e12, M = 2000) (expect failures)"
python3 build_028.py smoke-028 $S/data --y0 1.05e12 --M 2000 --nverify 0; echo "exit $?"
echo "== NEGATIVE: corrupted chunk vs recorded hashes (expect failures)"
cp -r $S/data $S/corrupt
python3 -c "
f='$S/corrupt/chunk_0005.bin'; b=bytearray(open(f,'rb').read()); b[200]^=1; open(f,'wb').write(b)"
python3 build_028.py smoke-028 $S/corrupt --y0 5e11 --M 10 --nverify 10 --hashes $S/hashes.json; echo "exit $?"
echo "== BOUNDARY smoke: 20 strata at y0 = 2.1e12 (above the band; worst-case density), two processes"
T0=$(date +%s.%N); (python3 gen_028.py smoke-028-top $S/top 0 10 --y0 2.1e12 --chunk 10 & python3 gen_028.py smoke-028-top $S/top 10 20 --y0 2.1e12 --chunk 10 & wait); T1=$(date +%s.%N)
python3 -c "print('boundary smoke wall %.1f s for 2 x 10 strata (%.3f s per stratum per process)' % ($T1 - $T0, ($T1 - $T0) / 10))"
python3 build_028.py smoke-028-top $S/top --y0 2.1e12 --M 20 --nverify 3; echo "exit $?"
