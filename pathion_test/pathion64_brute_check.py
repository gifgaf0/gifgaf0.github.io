"""
Extra-leg: validate the pruned method against full brute force at 64D.

pathion64_pg42.py established pruned==brute at 32D. This pushes the implementation
check one level higher (64D brute force, ~10 min) so the 128D pruned result rests
on implementation validation at TWO levels, not one. The lemma proving pruning is
complete is dimension-general; this confirms the code realizes it correctly at 64D.
"""
from pathion128_pg52 import build_cd_table, zd_pairs_pruned, zd_pairs_brute, verify_xor_property

if __name__=="__main__":
    p=911
    M64=build_cd_table(6)
    print(f"64D XOR property: {verify_xor_property(M64,64)}")
    print("running 64D pruned...", flush=True)
    pr=zd_pairs_pruned(M64,64)
    print(f"  pruned 64D ZD pairs: {len(pr)}", flush=True)
    print("running 64D BRUTE (slow)...", flush=True)
    br=zd_pairs_brute(M64,64,p)
    print(f"  brute  64D ZD pairs: {len(br)}", flush=True)
    print(f"  identical sets at 64D: {pr==br}   (expect 13020, True)")
    if pr!=br:
        only_pr=pr-br; only_br=br-pr
        print(f"  pruned-only: {len(only_pr)}  brute-only: {len(only_br)}")
