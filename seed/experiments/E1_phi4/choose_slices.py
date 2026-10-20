"""Rule (fixed before the coarse scan finished): the (A,k) slice is taken at the
coarse sigma with the most producing runs, the (A,sigma) slice at the coarse k
with the most producing runs; ties go to the smaller value. Prints 'sigma k'."""
import json
from collections import Counter
r = json.load(open("e1d_coarse.json"))["runs"]
cs = Counter(x["sigma"] for x in r if x["produced"])
ck = Counter(x["k"] for x in r if x["produced"])
s = sorted(cs.items(), key=lambda t: (-t[1], t[0]))[0][0]
k = sorted(ck.items(), key=lambda t: (-t[1], t[0]))[0][0]
print(s, k)
