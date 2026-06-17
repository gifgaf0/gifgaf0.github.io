"""
256D PG(6,2) test -- fourth consecutive Cayley-Dickson doubling.

Continues the R1 recursion PG(2,2)[octonions] -> PG(3,2)[16->32] ->
PG(4,2)[32->64] -> PG(5,2)[64->128].  Claim under test: the 128D->256D bridge
realizes PG(6,2) exactly (127 points = nonzero F_2^7 vectors, 2667 lines =
XOR-zero triples), generator e_128 excluded, two intact 128D copies embedded.

METHOD / TRUST BASIS (same as the 128D run):
  - The two-term canonical ZD completeness lemma (disjoint indices AND
    a^b^c^d=0) is dimension-general; pruning to those candidates loses nothing.
  - The pruned/sigma search uses only the CD cocycle sigma(i,j) in {+1,-1} --
    NO prime -- so the result is field-class-independent by construction.
  - Implementation already validated pruned==brute at 32D (in-script here) AND
    at 64D (pathion64_brute_check.py, full brute force). A 128D/256D brute force
    is intentionally NOT run (256D brute is ~hundreds of hours); the trust rests
    on the proven lemma + two-level implementation validation, as recorded in
    VERIFICATION_REPORT.md sec 6. The XOR property e_i*e_j=+-e_{i^j} is verified
    at every dimension before any count is trusted.

No target value consulted; counts reported as found (Eddington guard).
"""
from itertools import combinations
from collections import defaultdict
from pathion128_pg52 import (build_cd_table, verify_xor_property,
                             zd_pairs_pruned, zd_pairs_brute,
                             pg_lines, bridge_witnessed_lines)

if __name__=="__main__":
    p=911
    print(f"p={p} (only for the 32D brute equivalence leg; pruned method is prime-free)\n")

    # ---- 32D implementation check (self-contained) ----
    print("=== 32D implementation check (pruned vs brute) ===")
    M32=build_cd_table(5)
    print(f"  XOR property holds at 32D: {verify_xor_property(M32,32)}")
    b32=zd_pairs_brute(M32,32,p); pr32=zd_pairs_pruned(M32,32)
    print(f"  brute={len(b32)}  pruned={len(pr32)}  identical={b32==pr32}  (expect 1260, True)")
    if b32!=pr32:
        print("  !!! pruned != brute at 32D -- ABORT"); raise SystemExit
    print("  (64D pruned==brute equivalence established separately: pathion64_brute_check.py)")

    # ---- 128D recheck (pruned) ----
    print("\n=== 128D recheck (pruned) ===")
    M128=build_cd_table(7)
    print(f"  XOR property holds at 128D: {verify_xor_property(M128,128)}")
    s128=zd_pairs_pruned(M128,128)
    print(f"  128D total pruned ZD pairs: {len(s128)}  (expect 117180)")

    # ---- 256D run ----
    print("\n=== 256D run (sedenion-of-128D = two 128D copies + bridge) ===")
    M256=build_cd_table(8)
    print(f"  XOR property holds at 256D: {verify_xor_property(M256,256)}", flush=True)
    s256=zd_pairs_pruned(M256,256)
    print(f"  total two-term ZD pairs at 256D: {len(s256)}", flush=True)

    gen=128
    lower=upper=cross=0
    for fs in s256:
        idx=[k for pr in fs for k in pr]
        lo=all(1<=k<=127 for k in idx); up=all(128<=k<=255 for k in idx)
        if lo: lower+=1
        elif up: upper+=1
        else: cross+=1
    print(f"  lower copy (idx 1..127):     {lower}  (predict 117180 = full 128D structure)")
    print(f"  upper copy (idx 128..255):   {upper}  (predict 117180)")
    print(f"  bridge (crossing):           {cross}")
    print(f"  total: {lower+upper+cross} = {len(s256)}")

    allxor0 = all((lambda i: i[0]^i[1]^i[2]^i[3]==0)([k for pr in fs for k in pr]) for fs in s256)
    print(f"  every ZD quadruple has index-XOR = 0: {allxor0}", flush=True)

    # ---- PG(6,2) line witnessing ----
    print("\n=== PG(6,2) realization test ===")
    pts6, lines6 = pg_lines(7)   # F_2^7 -> 127 points
    deg=defaultdict(int)
    for L in lines6:
        for x in L: deg[x]+=1
    print(f"  PG(6,2) ground truth: {len(pts6)} points, {len(lines6)} lines "
          f"(expect 127, 2667); each point on {set(deg.values())} lines (expect {{63}})")
    wl = bridge_witnessed_lines(s256, 256)
    print(f"  bridge-witnessed upper triples: {len(wl)} of {len(lines6)}")
    print(f"  all witnessed are genuine PG(6,2) lines: {wl <= lines6}")
    print(f"  PG(6,2) lines NOT witnessed: {len(lines6 - wl)}")
    if wl==lines6:
        print("  >>> EXACT: the 256D bridge witnesses all 2667 PG(6,2) lines and nothing else.")
    elif wl<=lines6 and wl:
        print(f"  >>> SUBSET: {len(wl)}/2667 genuine lines, none spurious.")
    else:
        print("  >>> does NOT match PG(6,2).")

    up_used=set()
    for fs in s256:
        for pr in fs:
            for k in pr:
                if k>=128: up_used.add(k-128)
    up_used.discard(0)
    print(f"  distinct nonzero upper reductions used: {len(up_used)} (expect 127; e_128 generator excluded)")
