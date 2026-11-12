"""reconcile_026.py -- Entry 026 pre-freeze check: predict_026.py against the archived scripts.
archive/los216.py   = run020/predict/los216.py from the 017-021 archive (10.5281/zenodo.23843120), SHA-256 6bfd6a69...5214
archive/pair_absorb.py = from exploratory_mod4.zip (10.5281/zenodo.23843225), SHA-256 c6c39225...236d
Both were extracted in Matthew's Chrome on 2026-11-11 and rebuilt here byte-identically (hashes checked below).
Part A: the nine frozen (2.16) values, recomputed with los216.density under the entry's conventions.
Part B: the mod-4 absorption ladder, pair_absorb.py (archived code) against predict_026.py, and against the
        archived mod4_result.json values.
Part C: absorbed q = 3 and q = 5 cells: los216.density evaluated directly at the composite modulus
        Q = q * prod(P) and marginalised to q (what absorption means), against predict_026.py.
"""
import sys, os, math, json, hashlib, time
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
ARCH = os.path.join(here, 'archive')
for f, h in (('los216.py', '6bfd6a69b9c434614ff9bc9e6185f6889fc3429d9feb5fea3c9349a342405214'),
             ('pair_absorb.py', 'c6c39225c0ce6a9e6923557c723c946650dd96e599222d931d3b26da5698236d')):
    got = hashlib.sha256(open(os.path.join(ARCH, f), 'rb').read()).hexdigest()
    print(f"{f}: sha256 {got} {'== archived' if got == h else 'MISMATCH'}"); assert got == h
sys.path.insert(0, ARCH)
import los216
sys.argv = [sys.argv[0], ARCH, '/dev/null']
exec(open(os.path.join(ARCH, 'pair_absorb.py')).read().split('if __name__')[0])   # defines deficit_local / deficit_range
import predict_026 as P26
ln2 = math.log(2)
CHI = P26.CHI
pred = json.load(open(os.path.join(here, 'pred_026.json')))

def los_table(Q, q, y):
    units, tab = los216.pair_density_table(Q, y)
    rq = [a for a in range(1, q + 1) if math.gcd(a, q) == 1]; ix = {a % q: i for i, a in enumerate(rq)}
    M = np.zeros((len(rq), len(rq)))
    for (a, b), d in tab.items(): M[ix[a % q], ix[b % q]] += d
    return rq, M

def los_corr(q, absorb, mode, *args):
    Q = q * math.prod(absorb)
    v = lambda rq: np.array([CHI[q][a] for a in rq])
    if mode == 'local':
        rq, M = los_table(Q, q, args[0]); M = M / M.sum()
    else:
        (y0, y1), nodes, uniform = args
        x, wt = np.polynomial.legendre.leggauss(nodes); lo, hi = math.log(y0), math.log(y1)
        M = 0
        for xi, wi in zip(x, wt):
            Ly = 0.5 * (hi - lo) * xi + 0.5 * (hi + lo); rq, Mi = los_table(Q, q, math.exp(Ly))
            M = M + (Mi / Mi.sum() if uniform else Mi) * math.exp(Ly) * wi
        M = M / M.sum()
    return float(v(rq) @ M @ v(rq))

print("\nPart A. Frozen (2.16) values: predict_026 (pred_026.json) vs archived los216, same conventions")
CONV = {'E': ('range', (1e12, 1.02e12), 2, False), 'R64': ('range', (2.0**63, 2.0**64), 4, True), 'R128': ('range', (2.0**127, 2.0**128), 4, True)}
worstA = 0
for arm, (mode, rng, nodes, uni) in CONV.items():
    for q in (3, 4, 5):
        c_ours = pred['cells'][f'{arm}_{q}']['c216']; c_los = los_corr(q, [], mode, rng, nodes, uni)
        worstA = max(worstA, abs(c_ours - c_los))
        print(f"  {arm:4s} q={q}: predict_026 {c_ours:+.10f}  los216 {c_los:+.10f}  diff {c_ours - c_los:+.2e}  rel {(c_ours - c_los)/c_los:+.1e}")
print(f"  max |diff| = {worstA:.2e}")

print("\nPart B. Mod-4 absorption ladder (same-residue deficit eps): archived pair_absorb vs predict_026 vs archived mod4_result.json")
arch = {"024-A": {"none": 0.022728542120242945, "3": 0.02364876901426438, "3x5": 0.02403121425906951, "3x5x7": 0.02408832545856371, "3x5x7x11": 0.024094689802651947},
        "2^64": {"none": 0.012643665644489849, "3": 0.012927757702880793, "3x5": 0.013035926156587024, "3x5x7": 0.013064677315091894, "3x5x7x11": 0.013074318124470546},
        "2^128": {"none": 0.007163684475480603, "3": 0.007256762231239916, "3x5": 0.007286947728049914, "3x5x7": 0.0072940918477206185, "3x5x7x11": 0.0072977717448778345}}
worstB = worstB_arch = 0
for name, kind in (("024-A", ('range', 1e9, 2e9, 6)), ("2^64", ('local', 2**63.5)), ("2^128", ('local', 2**127.5))):
    for P in ((), (3,), (3, 5), (3, 5, 7), (3, 5, 7, 11)):
        key = "x".join(map(str, P)) or "none"
        e_pa = deficit_range(P, *kind[1:]) if kind[0] == 'range' else deficit_local(P, kind[1])
        if kind[0] == 'range':
            rq, M = P26.table(4, list(P), rng=(kind[1], kind[2]), nodes=kind[3])
        else:
            rq, M = P26.table(4, list(P), L=math.log(kind[1]))
        e_26 = 0.25 - M[0, 0]
        worstB = max(worstB, abs(e_pa - e_26)); worstB_arch = max(worstB_arch, abs(e_pa - arch[name][key]))
        print(f"  {name:6s} P={key:9s} pair_absorb {e_pa:.10f}  predict_026 {e_26:.10f}  diff {e_26 - e_pa:+.2e}  | archived json {arch[name][key]:.10f} (pair_absorb rerun - json {e_pa - arch[name][key]:+.1e})")
print(f"  max |predict_026 - pair_absorb| = {worstB:.2e};  max |pair_absorb rerun - archived json| = {worstB_arch:.2e}")

print("\nPart C. Absorbed q = 3, 5 cells: archived los216 at composite modulus vs predict_026 (local density, single node)")
worstC = 0
for lab, L in (('1.01e12', math.log(1.01e12)), ('2^63.5', 63.5 * ln2), ('2^127.5', 127.5 * ln2)):
    for q, Ps in ((3, ([2], [2, 5], [2, 5, 7], [2, 5, 7, 11])), (5, ([2], [2, 3], [2, 3, 7], [2, 3, 7, 11]))):
        for absorb in Ps:
            t = time.time()
            c_los = los_corr(q, absorb, 'local', math.exp(L)); c_26 = P26.corr_at(q, absorb, L=L)
            worstC = max(worstC, abs(c_los - c_26))
            print(f"  {lab:8s} q={q} absorb {str(absorb):14s} los216 {c_los:+.10f}  predict_026 {c_26:+.10f}  diff {c_26 - c_los:+.2e}  [{time.time()-t:.0f}s]", flush=True)
print(f"  max |diff| = {worstC:.2e}")
