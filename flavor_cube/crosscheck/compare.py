"""
compare.py -- diff the first computation (../geometry.json, ../mixing.json) against the independent
second leg (crosscheck_geometry.json, crosscheck_mixing.json) at full precision.

Geometry: every field the page uses must be identical, up to the two legs' stated conventions
(cyclic orders may start elsewhere or run the other way; the stabilizer list may be sorted differently,
so it is compared as a set of (matrix, class) pairs).
Mixing: every preset's angles, |U|^2, J, chi2 and cube delta must agree to 1e-9 (absolute or relative).
Exit status 0 when everything agrees.
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    with open(path) as f:
        return json.loads(re.sub(r"\bNaN\b", "null", f.read()))


def same_cycle(a, b):
    """True if the cyclic sequences a and b agree up to rotation and reversal."""
    if len(a) != len(b) or sorted(a) != sorted(b):
        return False
    n = len(a)
    for seq in (b, b[::-1]):
        for s in range(n):
            if all(a[i] == seq[(i + s) % n] for i in range(n)):
                return True
    return False


def close(x, y, tol=1e-9):
    if x is None or y is None:
        return x is None and y is None
    return abs(x - y) <= tol * max(1.0, abs(x), abs(y))


fails = []

A = load(os.path.join(HERE, "..", "geometry.json"))
B = load(os.path.join(HERE, "crosscheck_geometry.json"))
for k in ("phi", "fano_plus", "fano_minus", "pairings", "fano_diagram", "mismatch", "orbits"):
    if A[k] != B[k]:
        fails.append(("geometry", k, A[k], B[k]))
for k in ("link_order", "corner_view_order"):
    if not same_cycle(A[k], B[k]):
        fails.append(("geometry", k, A[k], B[k]))
for k in A["hexagons"]:
    if not same_cycle(A["hexagons"][k], B["hexagons"][k]):
        fails.append(("geometry", "hexagons." + k, A["hexagons"][k], B["hexagons"][k]))
sa = sorted((json.dumps(e["matrix"]), e["class"], e["det"]) for e in A["stabilizer"])
sb = sorted((json.dumps(e["matrix"]), e["class"], e["det"]) for e in B["stabilizer"])
if sa != sb:
    fails.append(("geometry", "stabilizer", len(sa), len(sb)))
ca = sorted((tuple(c["signs"]), tuple(c["faces"]), c["tetra"], c["fano_plus_line"], c["fano_minus_line"]) for c in A["corners"])
cb = sorted((tuple(c["signs"]), tuple(c["faces"]), c["tetra"], c["fano_plus_line"], c["fano_minus_line"]) for c in B["corners"])
if ca != cb:
    fails.append(("geometry", "corners", ca, cb))
for k in A["invariants"]:
    if json.dumps(A["invariants"][k], sort_keys=True) != json.dumps(B["invariants"].get(k), sort_keys=True):
        fails.append(("geometry", "invariants." + k, A["invariants"][k], B["invariants"].get(k)))
print("geometry: %d differences" % sum(1 for f in fails if f[0] == "geometry"))

MA = {p["id"]: p for p in load(os.path.join(HERE, "..", "mixing.json"))["presets"]}
MB = {p["id"]: p for p in load(os.path.join(HERE, "crosscheck_mixing.json"))["presets"]}
if set(MA) != set(MB):
    fails.append(("mixing", "preset ids", sorted(MA), sorted(MB)))
nmix = 0
for pid in sorted(set(MA) & set(MB)):
    a, b = MA[pid], MB[pid]
    for k in ("s12sq", "s13sq", "s23sq", "delta_deg", "J", "cube_delta_deg"):
        if not close(a.get(k), b.get(k)) and not (k == "delta_deg" and (a.get(k) or 0) < 1e-9 and (b.get(k) or 0) < 1e-9):
            fails.append(("mixing", pid + "." + k, a.get(k), b.get(k)))
            nmix += 1
    chia = a.get("chi2", a.get("chi2_pmns")) if a.get("chi2") is not None else a.get("chi2_pmns")
    chib = b.get("chi2", b.get("chi2_pmns")) if b.get("chi2") is not None else b.get("chi2_pmns")
    if not (close(chia, chib, 1e-8) or (chia is not None and chib is not None and max(abs(chia), abs(chib)) < 1e-20)):
        fails.append(("mixing", pid + ".chi2", chia, chib))
        nmix += 1
    for i in range(3):
        for j in range(3):
            if abs(a["absU2"][i][j] - b["absU2"][i][j]) > 1e-12:
                fails.append(("mixing", "%s.absU2[%d][%d]" % (pid, i, j), a["absU2"][i][j], b["absU2"][i][j]))
                nmix += 1
print("mixing: %d differences over %d presets" % (nmix, len(set(MA) & set(MB))))
for f in fails:
    print("DIFF", *f)
sys.exit(1 if fails else 0)
