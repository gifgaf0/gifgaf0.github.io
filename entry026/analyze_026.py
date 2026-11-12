"""analyze_026.py -- Entry 026 analysis. Runs once on the built data.
Usage:  analyze_026.py MANIFEST BEACON_JSON E_BIN R64_DIR R128_DIR
        analyze_026.py --dry PRED_JSON E_BIN R64_DIR R128_DIR        (synthetic dry runs only)
Before anything else it refuses to run unless (1) every file listed in manifest26.json matches its
SHA-256 (paths relative to the manifest), this script included; (2) the beacon round file is
self-consistent (randomness = sha256(signature)); (3) every R64/R128 chunk was generated with that
randomness as its seed; (4) the run counts equal the manifest's. The predictions are read from the
manifest-hashed pred_026.json. Then it evaluates every decisive and report-only statistic of the entry.
"""
import sys, os, glob, json, math, hashlib
import numpy as np
from scipy import stats

U = np.array([1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59])
def chi_vec(q):
    if q == 3: return np.where(U % 3 == 1, 1, -1)
    if q == 4: return np.where(U % 4 == 1, 1, -1)
    if q == 5: return np.where(np.isin(U % 5, (1, 4)), 1, -1)
CHAR = {3: 'chi_-3', 4: 'chi_-4', 5: '(./5)'}
ARMS = ['E', 'R64', 'R128']

def load_E(fn):
    h = np.fromfile(fn, np.uint64)
    assert int(h[0]) == 0x3032364547454e45, 'bad magic'
    nb = int(h[4]); blk = h[8:].reshape(nb, 3 + 512).astype(np.int64)
    return blk[:, 3:259].reshape(nb, 16, 16), blk[:, 259:].reshape(nb, 16, 16)

def load_R(d, bits):
    L1, L2, runs, seeds = [], [], [], set()
    for fn in sorted(glob.glob(os.path.join(d, f'R{bits}_*.npz'))):
        z = np.load(fn); L1.append(z['lag1'].astype(np.int64)); L2.append(z['lag2'].astype(np.int64)); runs.append(z['runs'])
        seeds.add(str(z['seed']))
    return np.concatenate(L1), np.concatenate(L2), np.concatenate(runs), seeds

def refuse(msg):
    sys.exit(f"REFUSED: {msg}")

def check_manifest(mfn):
    m = json.load(open(mfn)); base = os.path.dirname(os.path.abspath(mfn)); bad = []
    for f, h in m['sha256'].items():
        p = os.path.join(base, f)
        if not os.path.exists(p) or hashlib.sha256(open(p, 'rb').read()).hexdigest() != h: bad.append(f)
    me = os.path.abspath(__file__)
    if os.path.join(base, 'analyze_026.py') != me: bad.append('analyze_026.py is not the manifest copy being run')
    if bad: refuse('manifest mismatch: ' + ', '.join(bad))
    print(f"manifest {os.path.basename(mfn)} sha256 {hashlib.sha256(open(mfn, 'rb').read()).hexdigest()}: "
          f"{len(m['sha256'])} files verified")
    return m, base

def check_beacon(bfn):
    r = json.load(open(bfn))
    if hashlib.sha256(bytes.fromhex(r['signature'])).hexdigest() != r['randomness']:
        refuse('beacon round file: randomness != sha256(signature)')
    print(f"beacon round {r['round']}: randomness {r['randomness']} (= sha256(signature))")
    return r

def corr_units(T, q):
    """T: (units, 16, 16) counts. Ratio estimator over independent units (blocks or runs)."""
    v = chi_vec(q)
    n = T.sum(axis=(1, 2)).astype(float)
    S = np.einsum('kij,i,j->k', T, v, v).astype(float)
    N = n.sum(); c = S.sum() / N
    m = len(n)
    se = math.sqrt(((S - c * n) ** 2).sum() * m / (m - 1)) / N
    se_bin = math.sqrt((1 - c * c) / N)
    return c, se, se_bin, N, m

def main():
    dry = sys.argv[1] == '--dry'
    if dry:
        pred = json.load(open(sys.argv[2]))
    else:
        m, base = check_manifest(sys.argv[1])
        beacon = check_beacon(sys.argv[2])
        pred = json.load(open(os.path.join(base, 'pred_026.json')))
    E1, E2 = load_E(sys.argv[3])
    R64 = load_R(sys.argv[4], 64); R128 = load_R(sys.argv[5], 128)
    if not dry:
        for bits, R in ((64, R64), (128, R128)):
            n = m['runs'][f'R{bits}']
            if R[3] != {beacon['randomness']}: refuse(f'R{bits} chunks were not all generated with the beacon seed: {sorted(R[3])}')
            if sorted(R[2].tolist()) != list(range(n)): refuse(f'R{bits} run indices are not exactly 0..{n - 1}')
        print("seed and run counts verified against the beacon and the manifest")
    data = {'E': (E1, E2), 'R64': R64[:2], 'R128': R128[:2]}
    A = pred['alpha_prime']; z1 = stats.norm.isf(A); z2 = stats.norm.isf(A / 2)
    print(f"Entry 026 analysis{' (DRY RUN)' if dry else ''}. alpha' = {A:.3e}; one-sided z {z1:.3f}, two-sided z {z2:.3f}")
    for a in ARMS:
        T = data[a][0]
        print(f"arm {a}: units {T.shape[0]}, lag-1 pairs {int(T.sum()):,}")
    res = {}
    print("\nPer cell: observed, s.e. (units), s.e. (binomial), (2.16), full HL, tau")
    for a in ARMS:
        for q in (3, 4, 5):
            c, se, seb, N, m = corr_units(data[a][0], q)
            p = pred['cells'][f'{a}_{q}']
            res[(a, q)] = dict(c=c, se=se, seb=seb, N=N, c216=p['c216'], cfull=p['cfull'], tau=p['tau'])
            print(f"  {a:4s} {CHAR[q]:7s} {c:+.6f}  {se:.2e}  {seb:.2e}  {p['c216']:+.6f}  {p['cfull']:+.6f}  {p['tau']:.1e}")
    verdicts = []
    print("\nT-216: observed more negative than (2.16) (one-sided, decisive where listed)")
    for a in ARMS:
        for q in (3, 4, 5):
            r = res[(a, q)]; z = (r['c'] - r['c216']) / r['se']
            dec = f'{a}_{q}' in pred['decisive']['T216']
            ok = z < -z1
            print(f"  T216 {a:4s} {CHAR[q]:7s} z {z:+8.2f}  {'PASS' if ok else 'FAIL'}{'' if dec else ' (report-only)'}")
            if dec: verdicts.append((f'T216 {a} {CHAR[q]}', ok))
    print("\nT-full: |observed - full HL| <= tau + z2 * s.e. (consistency)")
    for a in ARMS:
        for q in (3, 4, 5):
            r = res[(a, q)]; d = r['c'] - r['cfull']; band = r['tau'] + z2 * r['se']
            dec = f'{a}_{q}' in pred['decisive']['Tfull']
            ok = abs(d) <= band
            print(f"  Tfull {a:4s} {CHAR[q]:7s} obs-full {d:+.2e}  band {band:.2e}  z(no tau) {d/r['se']:+6.2f}  "
                  f"obs/full {r['c']/r['cfull']:.4f}  {'PASS' if ok else 'FAIL'}{'' if dec else ' (report-only)'}")
            if dec: verdicts.append((f'Tfull {a} {CHAR[q]}', ok))
    print("\nT-height: ratio to (2.16) falls from E to R128, D = R_E - R_128 > 0 (one-sided)")
    for q in (3, 4, 5):
        e, h = res[('E', q)], res[('R128', q)]
        RE, RH = e['c'] / e['c216'], h['c'] / h['c216']
        se = math.hypot(e['se'] / abs(e['c216']), h['se'] / abs(h['c216']))
        Dp = e['cfull'] / e['c216'] - h['cfull'] / h['c216']
        z = (RE - RH) / se; ok = z > z1
        print(f"  Theight {CHAR[q]:7s} R_E {RE:.4f}  R_64 {res[('R64', q)]['c']/res[('R64', q)]['c216']:.4f}  R_128 {RH:.4f}  "
              f"D {RE-RH:+.4f} (pred {Dp:+.4f})  z {z:+.2f}  {'PASS' if ok else 'FAIL'}")
        verdicts.append((f'Theight {CHAR[q]}', ok))
    zs = []
    print("\nReport-only:")
    for a in ARMS:
        for q in (3, 4, 5):
            r = res[(a, q)]; zs.append((r['c'] - r['cfull']) / math.hypot(r['se'], r['tau']))
    print(f"  chi^2 of (obs - full HL)/sqrt(se^2 + tau^2) over 9 cells: {sum(z*z for z in zs):.2f} on 9 df, p = {stats.chi2.sf(sum(z*z for z in zs), 9):.3f}")
    for a in ARMS:
        lad = pred['cells'][f'{a}_3']['ladder']
        for q in (3, 4, 5):
            r = res[(a, q)]; lad = pred['cells'][f'{a}_{q}']['ladder']
            near = min(lad, key=lambda k: abs(lad[k] - r['c']))
            print(f"  {a:4s} {CHAR[q]:7s} ladder value nearest the data: through {near} ({lad[near]:+.6f}); obs {r['c']:+.6f}")
    for a in ARMS:
        line = []
        for q in (3, 4, 5):
            c, se, _, _, _ = corr_units(data[a][1], q); line.append(f"{CHAR[q]} {c:+.6f} ± {se:.1e}")
        print(f"  lag 2, {a}: " + ";  ".join(line))
    for a in ARMS:
        T = data[a][0].sum(axis=0).astype(float)
        for q in (3, 4, 5):
            k = sorted(set(int(u % q) for u in U)); M = np.zeros((len(k), len(k)))
            for i, u in enumerate(U):
                for j, w in enumerate(U):
                    M[k.index(u % q), k.index(w % q)] += T[i, j]
            print(f"  {a:4s} pair shares mod {q}: " + " ".join(f"{x:.6f}" for x in (M / M.sum()).ravel()))
    nfail = sum(1 for _, ok in verdicts if not ok)
    print(f"\nDecisive tests: {len(verdicts)}; failures: {nfail}" + (": " + ", ".join(n for n, ok in verdicts if not ok) if nfail else ""))

if __name__ == '__main__':
    main()
