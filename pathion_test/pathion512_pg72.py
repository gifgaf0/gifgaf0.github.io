"""
512D PG(7,2) test -- fifth consecutive Cayley-Dickson doubling.

Continues PG(2,2)->PG(3,2)->PG(4,2)->PG(5,2)->PG(6,2). Claim: the 256D->512D
bridge realizes PG(7,2) exactly (255 points = nonzero F_2^8 vectors, 10795
lines = XOR-zero triples), generator e_256 excluded, two intact 256D copies.

Trust basis identical to the 128D/256D runs: dimension-general completeness
lemma + pruned==brute validated at 32D (in-script) and 64D (pathion64_brute_check
.py). No higher brute force is run. Pruned search is prime-free => field-class-
independent by construction. XOR property verified at every dimension. No target
value consulted (Eddington guard).
"""
from collections import defaultdict
from pathion128_pg52 import (build_cd_table, verify_xor_property,
                             zd_pairs_pruned, zd_pairs_brute,
                             pg_lines, bridge_witnessed_lines)

if __name__=="__main__":
    p=911
    print(f"p={p} (only for the 32D brute equivalence leg; pruned method is prime-free)\n")

    print("=== 32D implementation check (pruned vs brute) ===")
    M32=build_cd_table(5)
    b32=zd_pairs_brute(M32,32,p); pr32=zd_pairs_pruned(M32,32)
    print(f"  XOR@32D={verify_xor_property(M32,32)}  brute={len(b32)} pruned={len(pr32)} "
          f"identical={b32==pr32} (expect 1260, True)")
    if b32!=pr32:
        print("  !!! ABORT"); raise SystemExit
    print("  (64D pruned==brute established separately: pathion64_brute_check.py)")

    print("\n=== 256D recheck (pruned) ===")
    M256=build_cd_table(8)
    print(f"  XOR@256D={verify_xor_property(M256,256)}", flush=True)
    s256=zd_pairs_pruned(M256,256)
    print(f"  256D total pruned ZD pairs: {len(s256)}  (expect 992124)", flush=True)

    print("\n=== 512D run (sedenion-of-256D = two 256D copies + bridge) ===")
    M512=build_cd_table(9)
    print(f"  XOR property holds at 512D: {verify_xor_property(M512,512)}", flush=True)
    s512=zd_pairs_pruned(M512,512)
    print(f"  total two-term ZD pairs at 512D: {len(s512)}", flush=True)

    lower=upper=cross=0
    for fs in s512:
        idx=[k for pr in fs for k in pr]
        lo=all(1<=k<=255 for k in idx); up=all(256<=k<=511 for k in idx)
        if lo: lower+=1
        elif up: upper+=1
        else: cross+=1
    print(f"  lower copy (idx 1..255):     {lower}  (predict 992124 = full 256D structure)")
    print(f"  upper copy (idx 256..511):   {upper}  (predict 992124)")
    print(f"  bridge (crossing):           {cross}")
    print(f"  total: {lower+upper+cross} = {len(s512)}")

    allxor0 = all((lambda i: i[0]^i[1]^i[2]^i[3]==0)([k for pr in fs for k in pr]) for fs in s512)
    print(f"  every ZD quadruple has index-XOR = 0: {allxor0}", flush=True)

    print("\n=== PG(7,2) realization test ===")
    pts7, lines7 = pg_lines(8)   # F_2^8 -> 255 points
    deg=defaultdict(int)
    for L in lines7:
        for x in L: deg[x]+=1
    print(f"  PG(7,2) ground truth: {len(pts7)} points, {len(lines7)} lines "
          f"(expect 255, 10795); each point on {set(deg.values())} lines (expect {{127}})")
    wl = bridge_witnessed_lines(s512, 512)
    print(f"  bridge-witnessed upper triples: {len(wl)} of {len(lines7)}")
    print(f"  all witnessed are genuine PG(7,2) lines: {wl <= lines7}")
    print(f"  PG(7,2) lines NOT witnessed: {len(lines7 - wl)}")
    if wl==lines7:
        print("  >>> EXACT: the 512D bridge witnesses all 10795 PG(7,2) lines and nothing else.")
    elif wl<=lines7 and wl:
        print(f"  >>> SUBSET: {len(wl)}/10795 genuine lines, none spurious.")
    else:
        print("  >>> does NOT match PG(7,2).")

    up_used=set()
    for fs in s512:
        for pr in fs:
            for k in pr:
                if k>=256: up_used.add(k-256)
    up_used.discard(0)
    print(f"  distinct nonzero upper reductions used: {len(up_used)} (expect 255; e_256 generator excluded)")
