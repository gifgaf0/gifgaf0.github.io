"""beacon_round_028.py PUSH_TIME_UTC -- the drand round fixed by the Entry 028 rule: the first round of the
mainnet default chain (genesis 1595431050, period 30 s; round r published at genesis + (r-1)*30) published
at least 10 minutes after the push."""
import sys, datetime
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from analyze_028 import beacon_round, GENESIS, PERIOD
R = beacon_round(sys.argv[1]); t = GENESIS + (R - 1) * PERIOD
print(R, datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
