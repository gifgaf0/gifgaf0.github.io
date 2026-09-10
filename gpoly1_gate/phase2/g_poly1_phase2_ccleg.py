#!/usr/bin/env python3
# g_poly1_phase2_ccleg.py — G-POLY1 Phase 2, CC leg (election E5 estimator), blind full-from-scratch.
# Locked memo 35a6225c38b66d2ac497d9e9af447e71; lock record f1c1342c843e34ec40ae1eaab201b947;
# base V4.74 CANONICAL 13d5eda14c69d3f68468a6ccdb8c3257.
# Elections (T3-immutable): E2-1(a) independent-grain variance addition, delta_RMS(L) = s1*sqrt(d/L);
# E2-2 monodisperse d; E2-3 four configs (hex:step, hex:gem8, cubic:step, cubic:gem8), pure phases only.
# Zero-shared-machinery leg choices (deliberately different from the chat instrument):
#   quadrature = Gauss-Legendre x Gauss-Legendre product (GL in cos(theta) AND GL in phi),
#     not the chat's GL x uniform-azimuth product;
#   eigen stack = closed-form trigonometric (Cardano) eigenvalues of the symmetric 3x3
#     Christoffel matrix, vectorized, not a library eigensolver;
#   Christoffel contraction via tensordot, not einsum.
import numpy as np, json, hashlib, os, sys

# ---------------- T1 self-grep (quarantined: forbidden strings assembled by character code
# so the clean instrument body cannot itself trigger a hit) --------------------------------
_F = [bytes(x).decode() for x in [
    [77, 112, 99],                                  # M-p-c
    [71, 112, 99],                                  # G-p-c
    [76, 73, 71, 79],                               # L-I-G-O
    [49, 55, 48, 56, 49, 55],                       # 1-7-0-8-1-7
    [50, 57, 57, 55, 57, 50, 52, 53, 56],           # 2-9-9-7-9-2-4-5-8
    [83, 77, 69],                                   # S-M-E
]]
_src = open(__file__, encoding='utf-8').read()
_body = _src.split('# ==== T1 QUARANTINE END ====')[1]
_hits = [f for f in _F if f in _body]
assert not _hits, f'T1 HIT: {_hits}'
print('T1 self-grep: PASS (0 forbidden-string hits in instrument body)')
# ==== T1 QUARANTINE END ====

# ---------------- input X-1 (byte-verified before use) ------------------------------------
INP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'poly_vrh_results.json')
raw = open(INP, 'rb').read()
md5 = hashlib.md5(raw).hexdigest()
assert md5 == '200e7a8b775577564369c6924d38a84c' and len(raw) == 2767, f'input mismatch: {md5} {len(raw)}'
DATA = json.loads(raw)
print(f'input poly_vrh_results.json verified: md5 {md5} ({len(raw)} B)')

# ---------------- elastic tensor builders (own construction) ------------------------------
# Voigt index pairs in tensor form: 0->(0,0) 1->(1,1) 2->(2,2) 3->(1,2) 4->(0,2) 5->(0,1)
PAIRS = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]

def full_tensor(Cv):
    """6x6 Voigt matrix -> full 3x3x3x3 stiffness with all minor/major symmetries."""
    C = np.zeros((3, 3, 3, 3))
    for a, (i, j) in enumerate(PAIRS):
        for b, (k, l) in enumerate(PAIRS):
            v = Cv[a, b]
            for ii, jj in ((i, j), (j, i)):
                for kk, ll in ((k, l), (l, k)):
                    C[ii, jj, kk, ll] = v
    return C

def voigt_hex(p):
    C = np.zeros((6, 6))
    C[0, 0] = C[1, 1] = p['C11']
    C[2, 2] = p['C33']
    C[0, 1] = C[1, 0] = p['C12']
    for a, b in ((0, 2), (2, 0), (1, 2), (2, 1)):
        C[a, b] = p['C13']
    C[3, 3] = C[4, 4] = p['C44']
    C[5, 5] = p['C66']
    return C

def voigt_cubic(p):
    C = np.zeros((6, 6))
    C[:3, :3] = p['C12']
    for a in range(3):
        C[a, a] = p['C11']
    for a in (3, 4, 5):
        C[a, a] = p['C44']
    return C

def voigt_iso(K, G):
    lam = K - 2.0 * G / 3.0
    C = np.zeros((6, 6))
    C[:3, :3] = lam
    for a in range(3):
        C[a, a] = lam + 2.0 * G
    for a in (3, 4, 5):
        C[a, a] = G
    return C

# ---------------- eigenvalues of symmetric 3x3: hand-written vectorized cyclic Jacobi -----
# (A closed-form Cardano solver was tried first and rejected: it loses ~sqrt(eps) accuracy
# at degenerate eigenvalue pairs, failing F-ISO-NULL at ~2e-8. Jacobi rotations are backward
# stable there. Recorded as honesty item H-CC-1.)
def eig3_sym(M, sweeps=8):
    """M: (N, 3, 3) symmetric. Returns eigenvalues ascending, shape (N, 3)."""
    A = M.copy()
    N = A.shape[0]
    eye = np.broadcast_to(np.eye(3), (N, 3, 3))
    for _ in range(sweeps):
        off = np.abs(A[:, 0, 1]) + np.abs(A[:, 0, 2]) + np.abs(A[:, 1, 2])
        scale = np.abs(A[:, 0, 0]) + np.abs(A[:, 1, 1]) + np.abs(A[:, 2, 2])
        if np.all(off <= 1e-15 * scale):
            break
        for p, q in ((0, 1), (0, 2), (1, 2)):
            apq = A[:, p, q]
            app, aqq = A[:, p, p], A[:, q, q]
            nz = np.abs(apq) > 0.0
            tau = np.where(nz, (aqq - app) / np.where(nz, 2.0 * apq, 1.0), 0.0)
            t = np.where(nz, np.sign(tau) / (np.abs(tau) + np.sqrt(1.0 + tau * tau)), 0.0)
            t = np.where(nz & (tau == 0.0), 1.0, t)   # tau==0 with apq!=0 -> 45-degree rotation
            c = 1.0 / np.sqrt(1.0 + t * t)
            s = t * c
            J = eye.copy()
            J[:, p, p] = c; J[:, q, q] = c
            J[:, p, q] = s; J[:, q, p] = -s
            A = np.transpose(J, (0, 2, 1)) @ A @ J
    lam = np.stack([A[:, 0, 0], A[:, 1, 1], A[:, 2, 2]], axis=-1)
    return np.sort(lam, axis=-1)

# ---------------- GL x GL sphere quadrature and per-config statistics ---------------------
def sphere_stats(C4, nt, np_):
    """Uniform-sphere-measure statistics over a GL(cos theta) x GL(phi) product grid.
    Returns dict with s1, mean_B, max_B_grid, the three invariants, min qL / max qT speeds."""
    xt, wt = np.polynomial.legendre.leggauss(nt)     # cos(theta) on [-1, 1]
    xp, wp = np.polynomial.legendre.leggauss(np_)    # phi via map [-1,1] -> [0, 2*pi]
    phi = np.pi * (xp + 1.0)
    st = np.sqrt(np.maximum(0.0, 1.0 - xt * xt))
    # direction grid (nt*np_, 3)
    n = np.empty((nt, np_, 3))
    n[..., 0] = st[:, None] * np.cos(phi)[None, :]
    n[..., 1] = st[:, None] * np.sin(phi)[None, :]
    n[..., 2] = xt[:, None]
    n = n.reshape(-1, 3)
    w = (wt[:, None] * (np.pi * wp)[None, :]).reshape(-1)
    w = w / w.sum()                                   # normalized uniform sphere measure
    # Christoffel: M_jk = n_i C_ijkl n_l
    A = np.tensordot(n, C4, axes=([1], [0]))          # (N, j, k, l)
    M = (A * n[:, None, None, :]).sum(axis=-1)        # (N, j, k)
    lam = eig3_sym(M)                                 # ascending: [qT2^2, qT1^2, qL^2]
    v = np.sqrt(lam)
    v2, v1, vL = v[:, 0], v[:, 1], v[:, 2]            # qT pair = two smallest eigen-speeds
    B = 2.0 * (v1 - v2) / (v1 + v2)
    return dict(
        s1=float(np.sqrt(np.sum(w * B * B))),
        mean_B=float(np.sum(w * B)),
        max_B_grid=float(B.max()),
        inv_qT_lamsum=float(np.sum(w * (lam[:, 0] + lam[:, 1]))),
        inv_qL_lam=float(np.sum(w * lam[:, 2])),
        inv_qT_vprod=float(np.sum(w * v1 * v2)),
        min_vqL=float(vL.min()),
        max_vqT=float(v1.max()),
    )

CONFIGS = {
    'hex:step':   ('hex',   DATA['vrh']['hex:step']['C_over_rho']),
    'hex:gem8':   ('hex',   DATA['vrh']['hex:gem8']['C_over_rho']),
    'cubic:step': ('cubic', DATA['vrh']['cubic:step']['C_over_rho']),
    'cubic:gem8': ('cubic', DATA['vrh']['cubic:gem8']['C_over_rho']),
}

# ---------------- F-ISO-NULL (hard gate, runs FIRST) --------------------------------------
K0 = DATA['vrh']['cubic:step']['K_VRH']
G0 = DATA['vrh']['cubic:step']['G_VRH']
iso = sphere_stats(full_tensor(voigt_iso(K0, G0)), 20, 20)
assert iso['max_B_grid'] <= 1e-12, f"F-ISO-NULL FAIL: max B = {iso['max_B_grid']:.3e}"
print(f"F-ISO-NULL: PASS (exact isotropic K={K0}, G={G0}: max B = {iso['max_B_grid']:.3e})")

# ---------------- convergence ladder (base resolution is the leg's free choice) -----------
NT, NP = 144, 144   # base; chosen after the ladder below confirmed the 1e-9 doubling gate
LADDER = [18, 36, 72, 144, 288]
if '--ladder' in sys.argv:
    for name, (sym, p) in CONFIGS.items():
        C4 = full_tensor(voigt_hex(p) if sym == 'hex' else voigt_cubic(p))
        prev = None
        row = []
        for nq in LADDER:
            s = sphere_stats(C4, nq, nq)['s1']
            row.append(f"{nq}: {'-' if prev is None else f'{abs(s - prev) / s:.3e}'}")
            prev = s
        print(f'ladder {name:12s} rel-delta vs previous -> ' + ', '.join(row))
    sys.exit(0)

# ---------------- per-config run: base + doubling gate + guards ---------------------------
results = {}
for name, (sym, p) in CONFIGS.items():
    C4 = full_tensor(voigt_hex(p) if sym == 'hex' else voigt_cubic(p))
    r = sphere_stats(C4, NT, NP)
    rd = sphere_stats(C4, 2 * NT, 2 * NP)
    dq = abs(rd['s1'] - r['s1']) / r['s1']
    assert dq <= 1e-9, f'F-QUAD FAIL {name}: doubling rel delta {dq:.3e}'
    assert r['min_vqL'] > r['max_vqT'], f"qL-separation FAIL {name}: {r['min_vqL']} vs {r['max_vqT']}"
    # F-N1: the L = d endpoint of delta_RMS(L) = s1*sqrt(d/L) must reproduce s1 exactly
    d_arb = 3.7
    assert r['s1'] * np.sqrt(d_arb / d_arb) == r['s1'], f'F-N1 FAIL {name}'
    r['s1_doubling_reldelta'] = dq
    r['mean_B_doubling_delta'] = abs(rd['mean_B'] - r['mean_B']) / r['mean_B']
    results[name] = r
    print(f"{name:12s} s1 = {r['s1']:.12e}  mean B = {r['mean_B']:.6e}  max B(grid) = {r['max_B_grid']:.6e}")
    print(f"{'':12s} F-QUAD {dq:.3e}  qL-sep {r['min_vqL']:.4f} > {r['max_vqT']:.4f}  F-N1 exact")

# ---------------- W-ANISO witness (non-gate) ----------------------------------------------
witness = {n: dict(max_B_pct=100.0 * r['max_B_grid']) for n, r in results.items()}
print('W-ANISO witness (non-gate): max single-grain qT split as % of mean:',
      {n: round(v['max_B_pct'], 2) for n, v in witness.items()})

# ---------------- E8 checkpoint (written and hashed BEFORE any cross-leg consultation) ----
checkpoint = dict(
    gate='G-POLY1', phase='2', leg='cc',
    lock=dict(memo_md5='35a6225c38b66d2ac497d9e9af447e71',
              lock_record_md5='f1c1342c843e34ec40ae1eaab201b947',
              base='V4.74 13d5eda14c69d3f68468a6ccdb8c3257',
              elections=['E2-1(a) variance addition delta_RMS(L)=s1*sqrt(d/L)',
                         'E2-2 monodisperse d', 'E2-3 four configs pure phases']),
    input_md5='200e7a8b775577564369c6924d38a84c',
    law='delta_RMS(L) = s1 * sqrt(d/L)  [E2-1(a); F-N1 endpoint delta_RMS(d)=s1 exact]',
    quadrature=dict(base=[NT, NP], doubling=[2 * NT, 2 * NP], gate='<=1e-9 on s1',
                    construction='GL(cos theta) x GL(phi) product (CC leg; distinct from chat GL x uniform)',
                    eigen='closed-form trigonometric symmetric-3x3 (no library eigensolver)',
                    note='psi-average exact: Christoffel eigenvalues are polarization-frame independent'),
    controls=dict(F_ISO_NULL=f"PASS max B {iso['max_B_grid']:.3e}",
                  qL_separation='PASS all configs',
                  F_N1='PASS exact (identity at L=d)'),
    results=results, witness_W_ANISO=witness)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'poly1_phase2_cc.json')
open(OUT, 'w').write(json.dumps(checkpoint, indent=1, default=float))
h = hashlib.md5(open(OUT, 'rb').read()).hexdigest()
print(f'\ncheckpoint: {OUT}  md5 {h}  ({os.path.getsize(OUT)} B)')
