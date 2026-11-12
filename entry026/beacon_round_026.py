"""beacon_round_026.py -- Entry 026 beacon rule.
drand mainnet default chain (League of Entropy): chain hash 8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce,
genesis 1595431050, period 30 s; round r is published at genesis + (r - 1) * 30.
R = the first round whose publication time is at least 10 minutes after the push of the freeze commit.
Usage: beacon_round_026.py PUSH_TIME_UTC   (ISO 8601, e.g. 2026-11-04T05:34:50Z)
"""
import sys, math, datetime as dt
GENESIS, PERIOD, DELAY = 1595431050, 30, 600
CHAIN = "8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce"
def round_for(push_epoch):
    return math.ceil((push_epoch + DELAY - GENESIS) / PERIOD) + 1
def t(r):
    return dt.datetime.fromtimestamp(GENESIS + (r - 1) * PERIOD, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
if __name__ == '__main__':
    push = dt.datetime.fromisoformat(sys.argv[1].replace('Z', '+00:00')).timestamp()
    R = round_for(push)
    print(f"push {sys.argv[1]}; push + 10 min = {dt.datetime.fromtimestamp(push + DELAY, dt.timezone.utc):%Y-%m-%dT%H:%M:%SZ}")
    print(f"round {R - 1} published {t(R - 1)} (too early); round {R} published {t(R)}  ->  R = {R} (chain {CHAIN[:8]}...)")
