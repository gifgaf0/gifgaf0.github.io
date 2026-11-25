"""analyze_028.py -- Entry 028 analysis. Runs once on the built data.
Usage:  analyze_028.py MANIFEST MANIFEST_SHA256 INFO_JSON ROUND_JSON PREV_ROUND_JSON PUSH_TIME_UTC DATADIR
        analyze_028.py --dry PRED_JSON DATADIR                       (synthetic dry runs only)
Startup refusal checks (production), in order:
 (1) the manifest file's own SHA-256 equals MANIFEST_SHA256 (recorded in the run log at the freeze), and
     every file it lists matches its SHA-256, this running copy of analyze_028.py included;
 (2) drand: /info is the frozen chain (hash, genesis, period); the round is the one fixed by the rule
     (first round published >= 10 min after PUSH_TIME_UTC); its BLS signature verifies against the PINNED
     public key; randomness =
     sha256(signature); previous_signature = the signature of round R - 1;
 (3) every data chunk was generated with SEED = that randomness;
 (4) the stratum indices are exactly 0..1999, each once, with n = 12,500,000 lag-1 and n - 1 lag-2 pairs each.
Predictions are read only from the manifest-hashed pred_028.json."""
import sys, os, glob, json, math, hashlib, datetime
import numpy as np
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from read_028 import read, MAGIC

CHAIN_HASH = "8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce"   # drand mainnet default chain
# pinned: the public key of that chain, as fetched and BLS-verified for Entry 026 (entry026/provenance/drand_info.json)
PUBLIC_KEY = "868f005eb8e6e4ca0a47c8a77ceaa5309a47978a7c71bc5cce96366b5d7a569937c529eeda66c7293784a9402801af31"
GENESIS, PERIOD = 1595431050, 30
M_STRATA, N_PER = 2000, 12_500_000
U = np.array([1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59])
CHARS = {"chi-3": np.where(U % 3 == 1, 1, -1), "chi-4": np.where(U % 4 == 1, 1, -1),
         "leg5": np.where(np.isin(U % 5, (1, 4)), 1, -1)}
LABEL = {"chi-3": "chi_-3", "chi-4": "chi_-4", "leg5": "(./5)"}

def refuse(msg): sys.exit(f"REFUSED: {msg}")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def check_manifest(mfn, msha):
    if sha(mfn) != msha: refuse(f"manifest sha256 {sha(mfn)} != recorded {msha}")
    m = json.load(open(mfn)); base = os.path.dirname(os.path.abspath(mfn)); bad = []
    for f, h in m["sha256"].items():
        p = os.path.join(base, f)
        if not os.path.exists(p) or sha(p) != h: bad.append(f)
    if os.path.join(base, "analyze_028.py") != os.path.abspath(__file__): bad.append("analyze_028.py is not the manifest copy being run")
    if bad: refuse("manifest mismatch: " + ", ".join(bad))
    print(f"manifest {os.path.basename(mfn)} sha256 {msha}: {len(m['sha256'])} files verified")
    return m, base

def beacon_round(push_iso):
    t = datetime.datetime.fromisoformat(push_iso.replace("Z", "+00:00")).timestamp() + 600
    return max(1, math.ceil((t - GENESIS) / PERIOD) + 1)          # first r with genesis + (r-1)*30 >= t

def check_beacon(info_fn, round_fn, prev_fn, push_iso):
    from py_ecc.bls import G2Basic
    info, r, prev = (json.load(open(f)) for f in (info_fn, round_fn, prev_fn))
    if not (info.get("hash") == CHAIN_HASH and info.get("genesis_time") == GENESIS and info.get("period") == PERIOD
            and info.get("public_key") == PUBLIC_KEY):
        refuse("beacon /info is not the frozen drand chain (hash, genesis, period, pinned public key)")
    R = beacon_round(push_iso)
    if r.get("round") != R: refuse(f"beacon round {r.get('round')} is not the rule's round {R}")
    sig, ps = bytes.fromhex(r["signature"]), bytes.fromhex(r["previous_signature"])
    if not G2Basic.Verify(bytes.fromhex(PUBLIC_KEY), hashlib.sha256(ps + R.to_bytes(8, "big")).digest(), sig):
        refuse("beacon BLS signature does not verify")
    if hashlib.sha256(sig).hexdigest() != r["randomness"]: refuse("beacon randomness != sha256(signature)")
    if not (prev.get("round") == R - 1 and prev.get("signature") == r["previous_signature"]):
        refuse("beacon previous_signature is not the signature of round R - 1")
    print(f"beacon round {R}: BLS valid, chain link to {R-1} valid, randomness {r['randomness']} (= sha256(signature))")
    return r["randomness"]

def load(datadir):
    metas = sorted(glob.glob(os.path.join(datadir, "chunk_*.json")))
    seeds = {json.load(open(m))["seed"] for m in metas}
    R = np.concatenate([read(m[:-5] + ".bin") for m in metas]) if metas else np.zeros(0)
    return R, seeds

def check_data(R, seeds, seed):
    if seeds != {seed}: refuse(f"data chunks not all generated with the beacon seed: {sorted(seeds)}")
    r = sorted(R["r"].astype(int).tolist())
    if r != list(range(M_STRATA)): refuse(f"stratum indices are not exactly 0..{M_STRATA - 1} ({len(r)} records)")
    if not ((R["magic"] == MAGIC).all() and (R["flags"] == 0).all() and (R["lag1"].sum(1) == N_PER).all()
            and (R["lag2"].sum(1) == N_PER - 1).all()):
        refuse("a stratum has wrong magic, flags or pair counts")
    print(f"seed and strata verified: {len(r)} strata, seed = beacon randomness")

def se_pair(cr):
    P = len(cr) // 2; d = cr[1:2 * P:2] - cr[0:2 * P:2]
    return math.sqrt((d ** 2).sum()) / (2 * P)

def main(argv):
    dry = argv[1] == "--dry"
    if dry:
        pred = json.load(open(argv[2])); datadir = argv[3]
    else:
        if len(argv) != 8: refuse("usage: MANIFEST MANIFEST_SHA256 INFO ROUND PREV PUSH_TIME DATADIR")
        m, base = check_manifest(argv[1], argv[2])
        seed = check_beacon(argv[3], argv[4], argv[5], argv[6])
        pred = json.load(open(os.path.join(base, "pred_028.json"))); datadir = argv[7]
    R, seeds = load(datadir)
    if not dry: check_data(R, seeds, seed)
    R = R[np.argsort(R["r"])]
    z1, z2 = pred["z1"], pred["z2"]
    L1 = R["lag1"].reshape(-1, 16, 16).astype(np.int64); L2 = R["lag2"].reshape(-1, 16, 16).astype(np.int64)
    n = L1.sum(axis=(1, 2)).astype(float); N = n.sum()
    print(f"Entry 028 analysis{' (DRY RUN)' if dry else ''}: {len(R)} strata, {int(N):,} lag-1 pairs; "
          f"alpha' = {pred['alpha_prime']:.3e}, z1 = {z1}, z2 = {z2}")
    res, verdicts = {}, []
    print("\nPer character: c_hat, se_pair, se_binomial, se_units, se_pair/se_binomial | c_216, c_full, c_hyb, tau_hyb")
    for c in ("chi-3", "chi-4", "leg5"):
        v = CHARS[c]; S = np.einsum("kij,i,j->k", L1, v, v).astype(float); cr = S / n
        ch = cr.mean(); sp = se_pair(cr); sb = math.sqrt((1 - ch * ch) / N)
        su = math.sqrt(((S - ch * n) ** 2).sum() * len(n) / (len(n) - 1)) / N
        p = pred["cells"][c]; res[c] = dict(c=ch, sp=sp, sb=sb)
        print(f"  {LABEL[c]:7s} {ch:+.7f}  {sp:.3e}  {sb:.3e}  {su:.3e}  {sp/sb:.4f} | {p['c216']:+.7f}  {p['cfull']:+.7f}  {p['chyb']:+.7f}  {p['tau_hyb']:.2e}")
    print(f"\nT-lad: (c_hat - c_full)/se_pair > {z1} (one-sided; data above the inflated-lambda ladder)")
    for c in ("chi-3", "chi-4", "leg5"):
        r = res[c]; p = pred["cells"][c]; z = (r["c"] - p["cfull"]) / r["sp"]; ok = z > z1
        print(f"  T-lad {LABEL[c]:7s} c_hat - c_full {r['c']-p['cfull']:+.3e}  z {z:+7.2f}  {'PASS' if ok else 'FAIL'}")
        verdicts.append((f"T-lad {LABEL[c]}", ok))
    print(f"\nT-hyb: |c_hat - c_hyb| <= tau_hyb + {z2} * se_pair (consistency with the fixed-lambda hybrid)")
    for c in ("chi-3", "chi-4", "leg5"):
        r = res[c]; p = pred["cells"][c]; d = r["c"] - p["chyb"]; band = p["tau_hyb"] + z2 * r["sp"]; ok = abs(d) <= band
        print(f"  T-hyb {LABEL[c]:7s} c_hat - c_hyb {d:+.3e}  band {band:.3e}  z(no tau) {d/r['sp']:+6.2f}  {'PASS' if ok else 'FAIL'}")
        verdicts.append((f"T-hyb {LABEL[c]}", ok))
    print("\nReport-only:")
    for c in ("chi-3", "chi-4", "leg5"):
        r = res[c]; p = pred["cells"][c]
        line = f"  {LABEL[c]:7s} (c_hat - c_216)/se {(r['c']-p['c216'])/r['sp']:+8.2f};  c_hat/c_hyb {r['c']/p['chyb']:.5f};  c_hat/c_full {r['c']/p['cfull']:.5f}"
        if p.get("cr23") is not None: line += f";  (c_hat - c_r23)/se {(r['c']-p['cr23'])/r['sp']:+.2f}"
        print(line)
    for c in ("chi-3", "chi-4", "leg5"):
        v = CHARS[c]; S2 = np.einsum("kij,i,j->k", L2, v, v).astype(float); n2 = L2.sum(axis=(1, 2)).astype(float)
        cr2 = S2 / n2; print(f"  lag 2 {LABEL[c]:7s} {cr2.mean():+.6f} ± {se_pair(cr2):.1e}")
    half = len(R) // 2
    for c in ("chi-3", "chi-4", "leg5"):
        v = CHARS[c]; S = np.einsum("kij,i,j->k", L1, v, v).astype(float) / n
        print(f"  {LABEL[c]:7s} lower half {S[:half].mean():+.6f}, upper half {S[half:].mean():+.6f} "
              f"(pred {pred['cells'][c]['chyb_lower']:+.6f}, {pred['cells'][c]['chyb_upper']:+.6f})")
    nf = sum(1 for _, ok in verdicts if not ok)
    print(f"\nDecisive tests: {len(verdicts)}; failures: {nf}" + (": " + ", ".join(k for k, ok in verdicts if not ok) if nf else ""))
    return verdicts

if __name__ == "__main__":
    main(sys.argv)
