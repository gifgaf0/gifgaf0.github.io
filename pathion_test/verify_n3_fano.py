"""
n=3 instance certificate (A_3 -> A_4, octonions -> sedenions): the bridge realizes
PG(2,2) = Fano as genuine ZERO DIVISORS. Resolves audit item B2 (Fano is a real ZD
instance, not an analogy) and extends the brute==pruned method anchor down to 16D.
"""
from pathion128_pg52 import (build_cd_table, zd_pairs_pruned, zd_pairs_brute,
                             pg_lines, bridge_witnessed_lines, verify_xor_property)
if __name__=="__main__":
    p=911
    M16=build_cd_table(4)                  # A_4 = sedenions = 16D
    print("XOR property holds at 16D:", verify_xor_property(M16,16))
    brute=zd_pairs_brute(M16,16,p); pruned=zd_pairs_pruned(M16,16)
    print(f"sedenion two-term canonical ZD pairs: brute={len(brute)} pruned={len(pruned)} "
          f"identical={brute==pruned}  (lit: 84; method anchor at 16D)")
    gen=8; lo=up=cross=0
    for fs in pruned:
        idx=[k for pr in fs for k in pr]
        L=all(1<=k<=7 for k in idx); U=all(8<=k<=15 for k in idx)
        if L: lo+=1
        elif U: up+=1
        else: cross+=1
    print(f"decomposition (A_3->A_4): lower octonion={lo} upper={up} bridge={cross} "
          f"(octonions have NO ZDs -> 0,0,84)")
    pts,lines=pg_lines(3)
    wl=bridge_witnessed_lines(pruned,16)
    print(f"PG(2,2) ground truth: {len(pts)} points {len(lines)} lines (expect 7,7)")
    print(f"bridge-witnessed: {len(wl)}/{len(lines)}  all genuine: {wl<=lines}  missing: {len(lines-wl)}")
    up_used=set(k-8 for fs in pruned for pr in fs for k in pr if k>=8); up_used.discard(0)
    print(f"distinct nonzero upper reductions used: {len(up_used)} (expect 7; generator e_8 excluded)")
