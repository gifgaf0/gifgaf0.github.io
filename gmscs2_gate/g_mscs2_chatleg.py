#!/usr/bin/env python3
"""g_mscs2_chatleg.py -- Gate G-MSCS2 chat-leg instrument, v1 (September 26, 2026).

Encodes the LOCKED staging memo v2 (efdcabdc) and lock record Addendum A-2 (49232d4c). No observational number,
no SI unit, no target string appears here; the pinned scanner (T1 gate list be921b8c) runs on this file and the memo
at every invocation and the instrument HALTS on any hit and without the list (no override path).

Machinery inherited from the G-MSCS1 chat instrument (db5f51dd; the chat leg may reuse its own prior code — the CC
leg is the blind one): tensors, SO(3) product quadrature, Voigt/Reuss/Hill and Walpole-HS with references optimized
at t = 0, k-sphere Christoffel, the descriptors, the fits. New: the l = 4 ODF families (cubic K4-tilde, hex P4, the hex
(t2, t4) form), the marginal descriptor-weight averages, the exhaustion / affinity / closed-form / marginal controls,
the continuity pins against X-6, the birefringence coefficient, the quadratic form.

Subcommands
  selftest          exactness and identity suites on synthetic inputs (no checkpoint written)
  run [--phase0-only]  guards -> phase0 pins+controls (halt on failure -> INDETERMINATE) [-> phase2 -> phase3] -> checkpoint
  compare           LAST: the memo section-6 hypotheses against the full checkpoint, written to a separate artifact
"""
import argparse, datetime, hashlib, importlib.util, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ME = os.path.abspath(__file__)
# ----------------------------------------------------------------------------- lock pins (lock record §1)
MEMO = os.path.join(HERE, 'staging_memo_G_MSCS2_v2.md'); MEMO_MD5 = 'efdcabdcd937cda4acb64f941dc4bb2b'; MEMO_BYTES = 46053
T1LIST = os.path.join(HERE, 'tools/t1/T1_forbidden_G_MSCS2.txt'); T1_MD5 = 'be921b8c29f7578e85ed92f1450c1956'
SCANNER = os.path.join(HERE, 'tools/t1/t1_scan.py'); SCANNER_MD5 = '6b86290090a8c84f1b1a0a99ec0bf697'
LEDGER_BASE_MD5 = 'f36bbdb04104008783f2763f70fb916f'
X1 = os.path.join(HERE, 'inputs/poly_vrh_results.json'); X1_MD5 = '200e7a8b775577564369c6924d38a84c'; X1_BYTES = 2767
X6C = os.path.join(HERE, 'inputs/g_mscs1_chatleg_checkpoint.json'); X6C_MD5 = 'c04c0b8ea34cfe60f231aa06828e6ce4'
X6CC = os.path.join(HERE, 'inputs/g_mscs1_ccleg_checkpoint.json'); X6CC_MD5 = '249e11dd53c4cb82f302b15d3c94c337'
ELECTIONS = {"E-MS2-1": "a+b", "E-MS2-2": "a", "E-MS2-2b": "a+b", "E-MS2-2c": "001+111", "E-MS2-3": "a", "E-MS2-4": "a", "E-MS2-5": "a", "E-MS2-6": "a", "E-MS2-7": "05302210+MSCS1stratum", "E-MS2-8": "a"}
T4_GRID = [-0.5, -0.25, -0.1, -0.05, -0.02, 0.0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0]
T2T4 = [-0.25, -0.125, 0.0, 0.125, 0.25]
N_THETA, N_PHI = 64, 128
TAU, KFLOOR = 1e-6, 1e-6
CONFIGS = {'hex_step': ('hex', 'hex:step'), 'hex_gem8': ('hex', 'hex:gem8'), 'cubic_step': ('cubic', 'cubic:step'), 'cubic_gem8': ('cubic', 'cubic:gem8')}
BANK_KEY = {'hex_step': 'step_hex', 'hex_gem8': 'gem8_hex', 'cubic_step': 'step_cubic', 'cubic_gem8': 'gem8_cubic'}
KEYS = ['hex_step|a', 'hex_step|b', 'hex_gem8|a', 'hex_gem8|b', 'cubic_step|001', 'cubic_step|111', 'cubic_gem8|001', 'cubic_gem8|111']
Z = np.array([0.0, 0.0, 1.0]); X = np.array([1.0, 0.0, 0.0]); Y = np.array([0.0, 1.0, 0.0]); AX111 = np.array([1.0, 1.0, 1.0]) / math.sqrt(3.0)
CHECKPOINT = os.path.join(HERE, 'g_mscs2_chatleg_checkpoint.json'); CHECKPOINT_P0 = os.path.join(HERE, 'g_mscs2_chatleg_phase0_checkpoint.json'); COMPARE = os.path.join(HERE, 'g_mscs2_chatleg_compare.json')

def md5b(b): return hashlib.md5(b).hexdigest()
def md5f(p): return md5b(open(p, 'rb').read())
def rel(a, b): return abs(a - b) / max(abs(a), abs(b), 1e-300)

# ----------------------------------------------------------------------------- guards + T1
def t1_gate(paths):
    if not os.path.exists(T1LIST): sys.exit('HALT: T1 gate list absent -- this gate has no LIST_ABSENT path')
    if md5f(T1LIST) != T1_MD5: sys.exit('HALT: T1 gate list md5 != lock')
    if md5f(SCANNER) != SCANNER_MD5: sys.exit('HALT: scanner md5 != lock')
    spec = importlib.util.spec_from_file_location('t1_scan', SCANNER); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    pats = mod.load(T1LIST); out = {'list_md5': T1_MD5, 'scanner_md5': SCANNER_MD5}
    for tag, p in paths.items():
        hits, coll = mod.scan_text(open(p, 'rb').read().decode('utf-8', 'replace'), pats)
        if hits: sys.exit(f'HALT: T1 HIT in {tag}: pattern indices {sorted(set(i for i, _ in hits))}')
        out[tag] = 'CLEAN'
    return out
def guards():
    for p, m, nb in ((MEMO, MEMO_MD5, MEMO_BYTES), (X1, X1_MD5, X1_BYTES)):
        raw = open(p, 'rb').read()
        if md5b(raw) != m or len(raw) != nb: sys.exit(f'HALT: {os.path.basename(p)} does not match the lock ({md5b(raw)}, {len(raw)} B)')
    for p, m in ((X6C, X6C_MD5), (X6CC, X6CC_MD5)):
        if md5f(p) != m: sys.exit(f'HALT: pin source {os.path.basename(p)} md5 != lock')
    return t1_gate({'instrument': ME, 'memo': MEMO})

# ----------------------------------------------------------------------------- tensors (inherited)
VOIGT = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
def c4_from_constants(sym, c, symmetrize_hex=False):
    M = np.zeros((6, 6))
    if sym == 'hex':
        C11, C12, C13, C33, C44 = (c[k] for k in ('C11', 'C12', 'C13', 'C33', 'C44'))
        C66 = 0.5 * (C11 - C12) if symmetrize_hex else c['C66']
        M[:3, :3] = [[C11, C12, C13], [C12, C11, C13], [C13, C13, C33]]; M[3, 3] = M[4, 4] = C44; M[5, 5] = C66
    else:
        C11, C12, C44 = c['C11'], c['C12'], c['C44']
        M[:3, :3] = [[C11, C12, C12], [C12, C11, C12], [C12, C12, C11]]; M[3, 3] = M[4, 4] = M[5, 5] = C44
    return voigt66_to_c4(M)
def voigt66_to_c4(M):
    T = np.zeros((3, 3, 3, 3))
    for I, (i, j) in enumerate(VOIGT):
        for J, (k, l) in enumerate(VOIGT):
            for a, b in ((i, j), (j, i)):
                for cc, d in ((k, l), (l, k)):
                    T[a, b, cc, d] = M[I, J]
    return T
def c4_to_voigt66(T):
    return np.array([[T[i, j, k, l] for (k, l) in VOIGT] for (i, j) in VOIGT])
_MF = np.array([1, 1, 1, math.sqrt(2), math.sqrt(2), math.sqrt(2)])
def c4_to_mandel(T):
    return np.array([[T[i, j, k, l] * _MF[I] * _MF[J] for J, (k, l) in enumerate(VOIGT)] for I, (i, j) in enumerate(VOIGT)])
def mandel_to_c4(M): return voigt66_to_c4(M / np.outer(_MF, _MF))
E6 = np.array([1.0, 1, 1, 0, 0, 0]); J6 = np.outer(E6, E6) / 3.0; K6M = np.eye(6) - J6
def iso_mandel(K, G): return 3 * K * J6 + 2 * G * K6M
def iso_KG_of_c4(T):
    K = np.einsum('iijj->', T) / 9.0; G = (np.einsum('ijij->', T) - np.einsum('iijj->', T) / 3.0) / 10.0; return K, G
def zener_H(c): return c['C11'] - c['C12'] - 2.0 * c['C44']

# ----------------------------------------------------------------------------- SO(3) product quadrature + ODF families
def so3_grid(na, nb, ng):
    al = 2 * np.pi * np.arange(na) / na; ga = 2 * np.pi * np.arange(ng) / ng
    xb, wb = np.polynomial.legendre.leggauss(nb); sb = np.sqrt(1 - xb**2)
    Rs, ws = [], []
    for a in al:
        Ra = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
        for ib in range(nb):
            Rb = np.array([[xb[ib], 0, sb[ib]], [0, 1, 0], [-sb[ib], 0, xb[ib]]])
            for g in ga:
                Rg = np.array([[math.cos(g), -math.sin(g), 0], [math.sin(g), math.cos(g), 0], [0, 0, 1]])
                Rs.append(Ra @ Rb @ Rg); ws.append(wb[ib] / (2.0 * na * ng))
    return np.array(Rs), np.array(ws)
SO3 = so3_grid(16, 10, 16)
SO3_DOUBLE = None
def rotate_all(c4, Rs):
    t = np.einsum('gia,abcd->gibcd', Rs, c4, optimize=True); t = np.einsum('gjb,gibcd->gijcd', Rs, t, optimize=True)
    t = np.einsum('gkc,gijcd->gijkd', Rs, t, optimize=True); return np.einsum('gld,gijkd->gijkl', Rs, t, optimize=True)
def P2(x): return 0.5 * (3 * x * x - 1)
def P4(x): return (35 * x**4 - 30 * x**2 + 3) / 8.0
def P6(x): return (231 * x**6 - 315 * x**4 + 105 * x**2 - 5) / 16.0
def K4tilde(Rs):
    """(5/2)(sum_i (e_i . z)^4 - 3/5) with e_i = R e_i the crystal axes in the lab: (e_i . z) = R[2, i]."""
    return 2.5 * (np.sum(Rs[:, 2, :]**4, axis=1) - 0.6)
def K6tilde(Rs):
    """20 x the pure l = 6 cubic harmonic (sum x^6 - (15/11) sum x^4 + 30/77) of the fiber axis in the crystal frame; |K6t| < 1."""
    z = Rs[:, 2, :]; return 20.0 * (np.sum(z**6, axis=1) - (15.0 / 11.0) * np.sum(z**4, axis=1) + 30.0 / 77.0)
class ODF:
    """Fiber-texture weight on SO(3). kind: 'l2' (G-MSCS1: 1 + t P2((g axis_c).z)), 'K4' (cubic: 1 + t4 K4t(g) [+ t6 K6t]),
    'P4' (hex: 1 + t2 P2 + t4 P4 + t6 P6 of the c-axis angle), 'iso'. Also provides the descriptor-axis MARGINAL on S^2."""
    def __init__(self, kind, axis_c=Z, t=0.0, t2=0.0, t4=0.0, t6=0.0, cmarg=1.0):
        self.kind, self.axis_c, self.t, self.t2, self.t4, self.t6, self.cmarg = kind, np.asarray(axis_c, float), t, t2, t4, t6, cmarg
    def w_so3(self, Rs):
        if self.kind == 'iso': return np.ones(len(Rs))
        if self.kind == 'l2': return 1.0 + self.t * P2((Rs @ self.axis_c)[:, 2])
        if self.kind == 'K4': return 1.0 + self.t4 * K4tilde(Rs) + self.t6 * K6tilde(Rs)
        if self.kind == 'P4':
            x = (Rs @ Z)[:, 2]; return 1.0 + self.t2 * P2(x) + self.t4 * P4(x) + self.t6 * P6(x)
        raise ValueError(self.kind)
    def w_marg(self, n):
        """Marginal weight on the descriptor axis n (S^2): l2 -> 1 + t P2(n_z); K4 -> 1 + c t4 P4(n_z) (+ t6 term has zero P6-moment
        against a degree-4 weight, so the exhaustion probe is carried as c6 t6 P6 with c6 immaterial: kept for the tensor path only);
        P4 -> 1 + t2 P2 + t4 P4 + t6 P6."""
        x = n[:, 2]
        if self.kind == 'iso': return np.ones(len(n))
        if self.kind == 'l2': return 1.0 + self.t * P2(x)
        if self.kind == 'K4': return 1.0 + self.cmarg * self.t4 * P4(x) + self.t6 * P6(x)
        if self.kind == 'P4': return 1.0 + self.t2 * P2(x) + self.t4 * P4(x) + self.t6 * P6(x)
        raise ValueError(self.kind)
def odf_avg_c4(c4, odf, grid=None):
    Rs, ws = grid if grid is not None else SO3; w = ws * odf.w_so3(Rs)
    return np.einsum('g,gijkl->ijkl', w, rotate_all(c4, Rs), optimize=True)

# ----------------------------------------------------------------------------- aggregate schemes (inherited)
def cstar(K0, G0):
    Ks = 4.0 * G0 / 3.0; Gs = G0 * (9 * K0 + 8 * G0) / (6.0 * (K0 + 2 * G0)); return iso_mandel(Ks, Gs)
def aggregate_tensors(c4, odf, hs_ref, grid=None):
    CV = odf_avg_c4(c4, odf, grid); S4 = mandel_to_c4(np.linalg.inv(c4_to_mandel(c4)))
    CR = mandel_to_c4(np.linalg.inv(c4_to_mandel(odf_avg_c4(S4, odf, grid)))); out = {'V': CV, 'R': CR, 'H': 0.5 * (CV + CR)}
    if hs_ref is not None:
        hs = {}
        for tag, (K0, G0) in hs_ref.items():
            Cs = cstar(K0, G0); inv = mandel_to_c4(np.linalg.inv(c4_to_mandel(c4) + Cs))
            hs[tag] = mandel_to_c4(np.linalg.inv(c4_to_mandel(odf_avg_c4(inv, odf, grid))) - Cs)
        out['HSlo'], out['HShi'] = hs['lo'], hs['hi']; out['HS'] = 0.5 * (hs['lo'] + hs['hi'])
    return out
def hs_iso_bound(c4, K0, G0):
    Cs = cstar(K0, G0); inv = mandel_to_c4(np.linalg.inv(c4_to_mandel(c4) + Cs))
    C = mandel_to_c4(np.linalg.inv(c4_to_mandel(odf_avg_c4(inv, ODF('iso')))) - Cs); return iso_KG_of_c4(C)
def feasible(c4, K0, G0, upper):
    D = iso_mandel(K0, G0) - c4_to_mandel(c4); lam = np.linalg.eigvalsh(D); scale = np.abs(c4_to_mandel(c4)).max()
    return (lam.min() >= -1e-11 * scale) if upper else (lam.max() <= 1e-11 * scale)
def optimize_hs_reference(c4):
    """G-MSCS1 A-2.3 procedure, verbatim: tightest feasible Walpole references at t = 0 (grid + bisection + golden section)."""
    Kv, Gv = iso_KG_of_c4(c4); refs = {}
    for upper in (True, False):
        def K_at(G0):
            lo, hi = 0.0, 50.0 * Kv
            if not (feasible(c4, hi, G0, True) if upper else feasible(c4, lo, G0, False)): return None
            for _ in range(80):
                mid = 0.5 * (lo + hi); ok = feasible(c4, mid, G0, upper)
                if upper: hi, lo = (mid, lo) if ok else (hi, mid)
                else:     lo, hi = (mid, hi) if ok else (lo, mid)
            return hi if upper else lo
        evals = {}
        def f(G0):
            if G0 in evals: return evals[G0][0]
            K0 = K_at(G0); val = 1e300 if K0 is None else (hs_iso_bound(c4, K0, G0)[1] * (1 if upper else -1)); evals[G0] = (val, K0); return val
        grid = np.linspace(0.2 * Gv, 4.0 * Gv, 160)
        for G0 in grid: f(float(G0))
        feas = [G0 for G0 in evals if evals[G0][1] is not None]; best = min(feas, key=lambda G0: evals[G0][0])
        i = list(grid).index(min(grid, key=lambda x: abs(x - best)))
        a, b = float(grid[max(i - 1, 0)]), float(grid[min(i + 1, len(grid) - 1)]); phi = (math.sqrt(5) - 1) / 2
        x1, x2 = b - phi * (b - a), a + phi * (b - a)
        for _ in range(70):
            if f(x1) < f(x2): b, x2 = x2, x1; x1 = b - phi * (b - a)
            else: a, x1 = x1, x2; x2 = a + phi * (b - a)
        feas = [G0 for G0 in evals if evals[G0][1] is not None]; best = min(feas, key=lambda G0: evals[G0][0])
        refs['hi' if upper else 'lo'] = (float(evals[best][1]), float(best))
    return refs

# ----------------------------------------------------------------------------- k-sphere + Christoffel + descriptors (inherited)
def sphere_grid(nt, nphi):
    x, w = np.polynomial.legendre.leggauss(nt); ph = 2 * np.pi * np.arange(nphi) / nphi
    ct, cp = np.meshgrid(x, np.cos(ph), indexing='ij'); st = np.sqrt(1 - ct**2); sp = np.sin(np.meshgrid(x, ph, indexing='ij')[1])
    K = np.stack([st * cp, st * sp, ct], -1).reshape(-1, 3); W = (np.repeat(w, nphi) / (2.0 * nphi)); return K, W
def modes(c4, K):
    G = np.einsum('ijkl,nj,nl->nik', c4, K, K, optimize=True); val, vec = np.linalg.eigh(G)
    return np.sqrt(np.maximum(val, 0.0)), np.transpose(vec, (0, 2, 1))
def descriptors(K, e):
    ke = np.einsum('ni,nbi->nb', K, e); lam = ke**2; w_em = 1.0 - lam
    eperp = e - ke[..., None] * K[:, None, :]
    Sp = 0.5 * (np.einsum('ni,nbj->nbij', K, eperp) + np.einsum('nbi,nj->nbij', eperp, K))
    w_h = (1.0 - lam) / (1.0 + lam / 3.0); return lam, w_em, Sp, w_h
def frac_E2(Sp, n):
    Sn = np.einsum('...ij,mj->...mi', Sp, n); nSn = np.einsum('...mi,mi->...m', Sn, n); Sn2 = np.einsum('...mi,...mi->...m', Sn, Sn)
    norm = np.einsum('...ij,...ij->...', Sp, Sp)[..., None]
    with np.errstate(divide='ignore', invalid='ignore'):
        f = 1.0 - 2.0 * Sn2 / norm + 0.5 * nSn**2 / norm
    return np.where(norm > 1e-300, f, 0.0)
NGRID = sphere_grid(12, 24)
def odf_avg_fracE2(Sp, odf):
    n, wn = NGRID; f = frac_E2(Sp, n); w = wn * odf.w_marg(n); return np.einsum('...m,m->...', f, w) / np.sum(w)
def so3_direct_fracE2(Sp, odf, axis_c, chunk=512):
    """SO(3)-direct ODF average of the per-grain E2 fraction: the descriptor axis n = g axis_c carried along the full orientation."""
    Rs, ws = SO3; w = ws * odf.w_so3(Rs); n_all = Rs @ axis_c; out = np.zeros(Sp.shape[:-2]); tot = 0.0
    for s in range(0, len(Rs), chunk):
        out += np.einsum('...m,m->...', frac_E2(Sp, n_all[s:s + chunk]), w[s:s + chunk]); tot += float(np.sum(w[s:s + chunk]))
    return out / tot
def label_branches(sym, K, e, lam, v):
    nk = K.shape[0]; lab = np.full((nk, 3), -1, dtype=int); iL = np.argmax(lam, axis=1)
    if sym == 'hex':
        zk = np.cross(np.broadcast_to(Z, K.shape), K); nrm = np.linalg.norm(zk, axis=1); zk = zk / np.where(nrm > 0, nrm, 1)[:, None]
        ov = np.abs(np.einsum('nbi,ni->nb', e, zk)); iSH = np.argmax(ov, axis=1)
        for n in range(nk):
            rest = [b for b in range(3) if b != iSH[n]]; l = rest[int(np.argmax(lam[n, rest]))]; s = [b for b in rest if b != l][0]
            lab[n, iSH[n]] = 0; lab[n, s] = 1; lab[n, l] = 2
    else:
        for n in range(nk):
            rest = [b for b in range(3) if b != iL[n]]; f, s = (rest if v[n, rest[0]] >= v[n, rest[1]] else rest[::-1])
            lab[n, f] = 0; lab[n, s] = 1; lab[n, iL[n]] = 2
    return lab
LABELS = {'hex': ['qSH', 'qSV', 'qL'], 'cubic': ['qT1', 'qT2', 'qL']}
def species_stats(sym, c4, K, W, odf=None, axis_lab=None, want_labels=True):
    """Single crystal (odf None): S2-E2 about the fixed lab axis axis_lab; aggregate (odf given): marginal-ODF-averaged E2 weight."""
    v, e = modes(c4, K); lam, w_em, Sp, w_h = descriptors(K, e)
    f = frac_E2(Sp, axis_lab[None, :])[..., 0] if odf is None else odf_avg_fracE2(Sp, odf)
    w_e2 = w_em * f; Wb = W[:, None]
    def mean(w): return float(np.sum(Wb * w * v) / np.sum(Wb * w))
    vEM, vE2, vH = mean(w_em), mean(w_e2), mean(w_h)
    out = {'v_EM': vEM, 'v_S2E2': vE2, 'v_S2h': vH, 'r_xtal_E2': vE2 / vEM - 1.0, 'r_xtal_h': vH / vEM - 1.0}
    if want_labels:
        lab = label_branches(sym, K, e, lam, v); qT = lab < 2; lamT = np.where(qT, lam, np.nan)
        out['lambda_mean'] = float(np.nansum(Wb * lamT) / np.sum(Wb * qT))
        im = np.unravel_index(np.nanargmax(np.where(qT, lam, -1.0)), lam.shape); out['lambda_max'] = float(lam[im]); out['lambda_max_branch'] = LABELS[sym][lab[im]]
    return out

# ----------------------------------------------------------------------------- fits
def fit_r(t, r, basis=(1, 2, 3)):
    A = np.stack([np.array(t)**k for k in basis], 1); coef, *_ = np.linalg.lstsq(A, np.array(r), rcond=None)
    return coef, float(np.sqrt(np.mean((A @ coef - np.array(r))**2)))
def fit_quadform(t2s, t4s, r):
    A = np.stack([t2s**2, t2s * t4s, t4s**2, t2s**3, t2s**2 * t4s, t2s * t4s**2, t4s**3], 1); coef, *_ = np.linalg.lstsq(A, r, rcond=None)
    return {'kappa22': float(coef[0]), 'kappa24': float(coef[1]), 'kappa44': float(coef[2]), 'residual': float(np.sqrt(np.mean((A @ coef - r)**2)))}

# ----------------------------------------------------------------------------- configuration helpers
def config_keys(cfg):
    return [(cfg + '|a', False, Z, 1.0), (cfg + '|b', True, Z, 1.0)] if cfg.startswith('hex') else [(cfg + '|001', False, Z, 1.0), (cfg + '|111', False, AX111, -2.0 / 3.0)]
def family(sym, axis_c, cmarg, **kw):
    return ODF('K4', axis_c=axis_c, cmarg=cmarg, **kw) if sym == 'cubic' else ODF('P4', axis_c=axis_c, **kw)
def r_agg_of(sym, c4, odf, K, W, hs_ref, schemes=('H',)):
    ag = aggregate_tensors(c4, odf, hs_ref); return {s: species_stats(sym, ag[s], K, W, odf, want_labels=False) for s in schemes}, ag

# ----------------------------------------------------------------------------- Phase 0
def phase0(vrh, x6, K, W):
    C = {}; hs_refs = {}
    x6p1, x6p2, x6pins = x6['phase1'], x6['phase2'], x6['pins_vrh0']
    # PIN-XTAL
    worst = 0.0; xtal = {}
    for cfg, (sym, vk) in CONFIGS.items():
        for key, symm, axis, cm in config_keys(cfg):
            c4 = c4_from_constants(sym, vrh[vk]['C_over_rho'], symm); st = species_stats(sym, c4, K, W, None, axis); xtal[key] = st
            for f in ('r_xtal_E2', 'r_xtal_h', 'lambda_mean', 'lambda_max'): worst = max(worst, rel(st[f], x6p1[key][f]))
    C['PIN-XTAL'] = {'worst_rel': worst, 'passed': bool(worst <= 1e-8)}
    # PIN-VRH0 / PIN-HS0
    wv = whs = 0.0; vt0 = {}
    for cfg, (sym, vk) in CONFIGS.items():
        c4 = c4_from_constants(sym, vrh[vk]['C_over_rho']); refs = optimize_hs_reference(c4); hs_refs[cfg] = refs
        for key, symm, axis, cm in config_keys(cfg):
            c4k = c4_from_constants(sym, vrh[vk]['C_over_rho'], symm); ag = aggregate_tensors(c4k, ODF('iso'), refs)
            vT = {k: math.sqrt(iso_KG_of_c4(ag[k])[1]) for k in ('V', 'R', 'H', 'HSlo', 'HShi')}; vt0[key] = vT
            wv = max(wv, rel(vT['H'], x6p2[key]['vT_VRH']), rel(vT['V'], x6p2[key]['vT_V']), rel(vT['R'], x6p2[key]['vT_R']))
            whs = max(whs, rel(vT['HSlo'], x6p2[key]['vT_HS_lo']), rel(vT['HShi'], x6p2[key]['vT_HS_hi']))
        Glo = hs_iso_bound(c4, *refs['lo'])[1]; Ghi = hs_iso_bound(c4, *refs['hi'])[1]; b = x6pins[cfg]['G_HS']; whs = max(whs, rel(Glo, b[0]), rel(Ghi, b[1]))
    C['PIN-VRH0'] = {'worst_rel': wv, 'passed': bool(wv <= 1e-8)}; C['PIN-HS0'] = {'worst_rel': whs, 'passed': bool(whs <= 1e-6)}
    # PIN-K2: the l = 2 family with G-MSCS1's grid/window/fit reproduces kappa2 (hex rel <= 1e-4; cubic abs <= 1e-12)
    T_GRID1 = [-0.5, -0.25, -0.1, -0.05, -0.02, 0.0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0]; whex = 0.0; wcub = 0.0; k2 = {}
    for cfg, (sym, vk) in CONFIGS.items():
        for key, symm, axis, cm in config_keys(cfg):
            c4 = c4_from_constants(sym, vrh[vk]['C_over_rho'], symm); rE2 = []
            for t in T_GRID1:
                rs, _ = r_agg_of(sym, c4, ODF('l2', axis_c=axis, t=t), K, W, None, ('H',)); rE2.append(rs['H']['r_xtal_E2'])
            idx = [i for i, t in enumerate(T_GRID1) if abs(t) <= 0.25 + 1e-12]; cE, _ = fit_r([T_GRID1[i] for i in idx], [rE2[i] for i in idx]); k2[key] = float(cE[1])
            if sym == 'hex': whex = max(whex, rel(k2[key], x6p2[key]['kappa2_E2']))
            else: wcub = max(wcub, abs(k2[key]))
            print(f'  PIN-K2 {key:16} kappa2={k2[key]:+.9e}  X-6 {x6p2[key]["kappa2_E2"]:+.9e}', flush=True)
    C['PIN-K2'] = {'worst_rel_hex_kappa2': whex, 'worst_abs_cubic_kappa2': wcub, 'kappa2_E2_recomputed': k2, 'passed': bool(whex <= 1e-4 and wcub <= 1e-12)}
    # F-CTRL-ISO
    Kiso, Giso = 134.609, 70.881; c_iso = c4_from_constants('cubic', {'C11': Kiso + 4 * Giso / 3, 'C12': Kiso - 2 * Giso / 3, 'C44': Giso})
    st = species_stats('cubic', c_iso, K, W, None, Z); worst = max(abs(st['r_xtal_E2']), abs(st['r_xtal_h']), st['lambda_max'])
    for t4 in T4_GRID:
        for odf in (ODF('K4', t4=t4), ODF('P4', t4=t4)):
            rs, _ = r_agg_of('cubic', c_iso, odf, K, W, None); worst = max(worst, abs(rs['H']['r_xtal_E2']), abs(rs['H']['r_xtal_h']))
    C['F-CTRL-ISO'] = {'worst_abs': float(worst), 'passed': bool(worst <= 1e-10)}
    # F-CTRL-SO3
    c4 = c4_from_constants('hex', vrh['hex:step']['C_over_rho']); ag = aggregate_tensors(c4, ODF('iso'), None); v, e = modes(ag['H'], K); lam, w_em, Sp, _ = descriptors(K, e)
    f = odf_avg_fracE2(Sp, ODF('iso')); dev = float(np.max(np.abs(f[w_em > 1e-6] - 0.4))); r0 = species_stats('hex', ag['H'], K, W, ODF('P4', t4=0.0), want_labels=False)['r_xtal_E2']
    C['F-CTRL-SO3'] = {'dev_from_0p4': dev, 'r_agg_0_abs': abs(r0), 'passed': bool(dev <= 1e-10 and abs(r0) <= TAU)}
    # F-CTRL-POS
    Rs, ws = SO3; wmin = min([float(np.min(ODF('K4', t4=t4).w_so3(Rs))) for t4 in T4_GRID] + [float(np.min(ODF('P4', t4=t4).w_so3(Rs))) for t4 in T4_GRID]
                         + [float(np.min(ODF('P4', t2=a, t4=b).w_so3(Rs))) for a in T2T4 for b in T2T4] + [float(np.min(ODF('K4', t4=0.3, t6=0.3).w_so3(Rs))), float(np.min(ODF('P4', t4=0.3, t6=0.3).w_so3(Rs)))])
    C['F-CTRL-POS'] = {'min_odf_weight': wmin, 'passed': bool(wmin >= 0.0)}
    # F-CTRL-L2NULL (cubic): l2 at t = 1 and the mixed (t2, t4) leave tensors and r_agg unchanged
    worst = 0.0
    for cfg in ('cubic_step', 'cubic_gem8'):
        sym, vk = CONFIGS[cfg]; refs = hs_refs[cfg]
        for key, symm, axis, cm in config_keys(cfg):
            c4 = c4_from_constants(sym, vrh[vk]['C_over_rho']); scale = np.abs(c4).max()
            a0 = aggregate_tensors(c4, ODF('iso'), refs); a1 = aggregate_tensors(c4, ODF('l2', axis_c=axis, t=1.0), refs)
            for s in ('V', 'R', 'HS'): worst = max(worst, float(np.abs(a1[s] - a0[s]).max()) / scale)
            r0 = species_stats(sym, a0['H'], K, W, ODF('iso'), want_labels=False)['r_xtal_E2']; r1 = species_stats(sym, a1['H'], K, W, ODF('iso'), want_labels=False)['r_xtal_E2']
            worst = max(worst, abs(r1 - r0))
            # mixed: a P2 term on the cubic descriptor axis added to the K4 family must change nothing on the tensor side
            b0 = aggregate_tensors(c4, ODF('K4', axis_c=axis, cmarg=cm, t4=0.25), refs)
            mixed = ODF('K4', axis_c=axis, cmarg=cm, t4=0.25); wmix = lambda Rs, m=mixed: m.w_so3(Rs) + 0.25 * P2((Rs @ axis)[:, 2])
            class _M(ODF):
                def w_so3(self, Rs): return mixed.w_so3(Rs) + 0.25 * P2((Rs @ axis)[:, 2])
            b1 = aggregate_tensors(c4, _M('K4', axis_c=axis, cmarg=cm, t4=0.25), refs)
            for s in ('V', 'R', 'HS'): worst = max(worst, float(np.abs(b1[s] - b0[s]).max()) / scale)
    C['F-CTRL-L2NULL'] = {'worst_abs': float(worst), 'passed': bool(worst <= 1e-12)}
    # F-CTRL-L4EXHAUST: an l = 6 term changes nothing (tensors, weights, r_agg) — hex P6 at t6 = 0.3 on top of t4 = 0.3; cubic K6t likewise
    wt = wr = 0.0
    for cfg, (sym, vk) in CONFIGS.items():
        refs = hs_refs[cfg]
        for key, symm, axis, cm in config_keys(cfg):
            c4 = c4_from_constants(sym, vrh[vk]['C_over_rho'], symm); scale = np.abs(c4).max()
            o0 = family(sym, axis, cm, t4=0.3); o6 = family(sym, axis, cm, t4=0.3, t6=0.3)
            a0 = aggregate_tensors(c4, o0, refs); a6 = aggregate_tensors(c4, o6, refs)
            for s in ('V', 'R', 'HS'): wt = max(wt, float(np.abs(a6[s] - a0[s]).max()) / scale)
            r0 = species_stats(sym, a0['H'], K, W, o0, want_labels=False)['r_xtal_E2']; r6 = species_stats(sym, a6['H'], K, W, o6, want_labels=False)['r_xtal_E2']; wr = max(wr, abs(r6 - r0))
    C['F-CTRL-L4EXHAUST'] = {'worst_rel_tensor': float(wt), 'worst_abs_r_agg': float(wr), 'passed': bool(wt <= 1e-12 and wr <= 1e-12)}
    # F-CTRL-C4: the exact closed form (Voigt and Reuss), affinity, and the H = 0 tensor
    T4V = np.zeros((6, 6)); T4V[0, 0] = T4V[1, 1] = 3; T4V[2, 2] = 8; T4V[0, 1] = T4V[1, 0] = 1; T4V[0, 2] = T4V[2, 0] = T4V[1, 2] = T4V[2, 1] = -4; T4V[3, 3] = T4V[4, 4] = -4; T4V[5, 5] = 1
    T4V = T4V / 105.0
    wcf = waf = 0.0
    for cfg in ('cubic_step', 'cubic_gem8'):
        sym, vk = CONFIGS[cfg]; c = vrh[vk]['C_over_rho']; c4 = c4_from_constants(sym, c); H = zener_H(c); scale = np.abs(c4).max()
        V0 = c4_to_voigt66(odf_avg_c4(c4, ODF('iso'))); V3 = c4_to_voigt66(odf_avg_c4(c4, ODF('K4', t4=0.3))); V6 = c4_to_voigt66(odf_avg_c4(c4, ODF('K4', t4=0.6)))
        wcf = max(wcf, float(np.abs((V3 - V0) - 0.3 * H * T4V).max()) / scale); waf = max(waf, float(np.abs((V6 - V0) - 2 * (V3 - V0)).max()) / scale)
        S4 = mandel_to_c4(np.linalg.inv(c4_to_mandel(c4))); Sv = c4_to_voigt66(S4); HS_ = Sv[0, 0] - Sv[0, 1] - 0.5 * (4 * Sv[3, 3])   # Voigt-notation S44 = 4 S_2323 -> tensor H_S = S11 - S12 - 2 S_2323
        R0 = c4_to_voigt66(odf_avg_c4(S4, ODF('iso'))); R3 = c4_to_voigt66(odf_avg_c4(S4, ODF('K4', t4=0.3)))
        # Voigt-notation compliance entries: the tensor law holds on the tensor; in Voigt notation the shear rows carry factors 4 (44) and the mixed rows 2 — compare on tensors instead
        S3t = odf_avg_c4(S4, ODF('K4', t4=0.3)); S0t = odf_avg_c4(S4, ODF('iso')); Ht = HS_ / 1.0
        Tt = voigt66_to_c4(T4V); Tt_full = Tt.copy()   # T4V in Voigt notation encodes the tensor 𝒯⁴/105 entries directly (all entries symmetric)
        wcf = max(wcf, float(np.abs((S3t - S0t) - 0.3 * Ht * Tt_full).max()) / np.abs(S4).max())
    c_h0 = c4_from_constants('cubic', {'C11': 200.0, 'C12': 100.0, 'C44': 50.0}); V0 = odf_avg_c4(c_h0, ODF('iso')); V3 = odf_avg_c4(c_h0, ODF('K4', t4=0.3))
    h0 = float(np.abs(V3 - V0).max()) / np.abs(c_h0).max()
    C['F-CTRL-C4'] = {'worst_rel_closed_form': float(wcf), 'worst_rel_affine': float(waf), 'h0_effect_rel': h0, 'passed': bool(wcf <= 1e-12 and waf <= 1e-12 and h0 <= 1e-12)}
    # F-CTRL-MARG (cubic keys): SO(3)-direct weight average == marginal form at t4 = 0.3
    worst = 0.0
    for cfg in ('cubic_step', 'cubic_gem8'):
        sym, vk = CONFIGS[cfg]; c4 = c4_from_constants(sym, vrh[vk]['C_over_rho'])
        for key, symm, axis, cm in config_keys(cfg):
            odf = ODF('K4', axis_c=axis, cmarg=cm, t4=0.3); ag = aggregate_tensors(c4, odf, None); v, e = modes(ag['H'], K); lam, w_em, Sp, _ = descriptors(K, e)
            fm = odf_avg_fracE2(Sp, odf); fd = so3_direct_fracE2(Sp, odf, axis); worst = max(worst, float(np.max(np.abs(fm - fd)[w_em > 1e-6])))
    C['F-CTRL-MARG'] = {'worst_abs': float(worst), 'passed': bool(worst <= 1e-12)}
    # F-CTRL-TEX4
    c_tex = c4_from_constants('cubic', {'C11': 300.0, 'C12': 100.0, 'C44': 40.0}); rs, _ = r_agg_of('cubic', c_tex, ODF('K4', t4=1.0), K, W, None)
    C['F-CTRL-TEX4'] = {'r_agg_t1_abs': abs(rs['H']['r_xtal_E2']), 'passed': bool(abs(rs['H']['r_xtal_E2']) > TAU)}
    # F-CTRL-QUAD: k-sphere doubling on r_agg at t4 = 0.25 per key; SO(3) doubling on the Voigt tensor at t4 = 0.3
    global SO3_DOUBLE
    K2, W2 = sphere_grid(2 * N_THETA, 2 * N_PHI); wd = 0.0; wso3 = 0.0
    if SO3_DOUBLE is None: SO3_DOUBLE = so3_grid(32, 20, 32)
    for cfg, (sym, vk) in CONFIGS.items():
        for key, symm, axis, cm in config_keys(cfg):
            c4 = c4_from_constants(sym, vrh[vk]['C_over_rho'], symm); odf = family(sym, axis, cm, t4=0.25); ag = aggregate_tensors(c4, odf, None)
            r1 = species_stats(sym, ag['H'], K, W, odf, want_labels=False)['r_xtal_E2']; r2 = species_stats(sym, ag['H'], K2, W2, odf, want_labels=False)['r_xtal_E2']; wd = max(wd, abs(r1 - r2))
            V1 = odf_avg_c4(c4, family(sym, axis, cm, t4=0.3)); V2 = odf_avg_c4(c4, family(sym, axis, cm, t4=0.3), SO3_DOUBLE); wso3 = max(wso3, float(np.abs(V1 - V2).max()) / np.abs(c4).max())
    C['F-CTRL-QUAD'] = {'doubling_residual': float(max(wd, wso3)), 'k_sphere_doubling': float(wd), 'so3_doubling': float(wso3), 'passed': bool(max(wd, wso3) <= 1e-10)}
    return C, hs_refs, xtal, vt0

# ----------------------------------------------------------------------------- Phase 2 / 3
def phase2(vrh, K, W, hs_refs):
    out = {}
    for cfg, (sym, vk) in CONFIGS.items():
        refs = hs_refs[cfg]
        for key, symm, axis, cm in config_keys(cfg):
            c4 = c4_from_constants(sym, vrh[vk]['C_over_rho'], symm); rE2, rh, rHS, rV, rR, lamt = [], [], [], [], [], []
            for t4 in T4_GRID:
                odf = family(sym, axis, cm, t4=t4); ag = aggregate_tensors(c4, odf, refs)
                sH = species_stats(sym, ag['H'], K, W, odf); rE2.append(sH['r_xtal_E2']); rh.append(sH['r_xtal_h']); lamt.append(sH['lambda_mean'])
                for tag, lst in (('HS', rHS), ('V', rV), ('R', rR)): lst.append(species_stats(sym, ag[tag], K, W, odf, want_labels=False)['r_xtal_E2'])
            idx = [i for i, t in enumerate(T4_GRID) if abs(t) <= 0.25 + 1e-12]; idx2 = [i for i, t in enumerate(T4_GRID) if abs(t) <= 0.1 + 1e-12]
            tt = [T4_GRID[i] for i in idx]; tt2 = [T4_GRID[i] for i in idx2]
            cE, resE = fit_r(tt, [rE2[i] for i in idx]); cE2, _ = fit_r(tt2, [rE2[i] for i in idx2]); ch, _ = fit_r(tt, [rh[i] for i in idx]); cHS, _ = fit_r(tt, [rHS[i] for i in idx])
            # birefringence b1 on Hill: propagation along x (perpendicular to the fiber), polarizations y (qSH) and z (qSV)
            def biref(t4):
                ag = aggregate_tensors(c4, family(sym, axis, cm, t4=t4), None); M = c4_to_voigt66(ag['H'])
                return (math.sqrt(M[5, 5]) - math.sqrt(M[3, 3]))   # v_SH^2 = C66, v_SV^2 = C44 for k along x in a TI medium about z
            vT0 = math.sqrt(iso_KG_of_c4(aggregate_tensors(c4, ODF('iso'), None)['H'])[1]); b1 = (biref(0.05) - biref(-0.05)) / 0.1 / vT0
            # quadratic form on the 5x5 grid (hex: P2+P4; cubic: P2 on the descriptor axis + K4 -> must reduce to kappa44 alone)
            t2s, t4s, rq = [], [], []
            for a in T2T4:
                for b in T2T4:
                    if sym == 'hex': odf = ODF('P4', t2=a, t4=b)
                    else:
                        base = ODF('K4', axis_c=axis, cmarg=cm, t4=b)
                        class _M(ODF):
                            def w_so3(self, Rs): return base.w_so3(Rs) + a * P2((Rs @ axis)[:, 2])
                            def w_marg(self, n): return base.w_marg(n) + a * P2(n[:, 2])
                        odf = _M('K4', axis_c=axis, cmarg=cm, t4=b)
                    ag = aggregate_tensors(c4, odf, None); rq.append(species_stats(sym, ag['H'], K, W, odf, want_labels=False)['r_xtal_E2']); t2s.append(a); t4s.append(b)
            qf = fit_quadform(np.array(t2s), np.array(t4s), np.array(rq))
            ag0 = aggregate_tensors(c4, ODF('iso'), refs); vT = {k: math.sqrt(iso_KG_of_c4(ag0[k])[1]) for k in ('H', 'HSlo', 'HShi')}
            out[key] = {'r_agg_E2_VRH': rE2, 'r_agg_h_VRH': rh, 'r_agg_E2_HS': rHS, 'r_agg_E2_V': rV, 'r_agg_E2_R': rR, 'lambda_mean_t4': lamt,
                        'S4_E2': float(cE[0]), 'S4_h': float(ch[0]), 'kappa44_E2': float(cE[1]), 'kappa44_h': float(ch[1]), 'kappa444_E2': float(cE[2]), 'kappa44_E2_HS': float(cHS[1]),
                        'halving_dev_kappa44': float(abs(cE[1] - cE2[1])), 'kappa44_E2_window0p1': float(cE2[1]), 'fit_residual': resE, 'biref_b1_VRH': float(b1),
                        'vT_VRH': vT['H'], 'vT_HS_lo': vT['HSlo'], 'vT_HS_hi': vT['HShi'], 'quadform': qf, 'hs_ref': refs}
            print(f'  phase2 {key:16} S4={cE[0]:+.3e} k44={cE[1]:+.6e} (win0.1 {cE2[1]:+.6e}) k44_HS={cHS[1]:+.6e} k44_h={ch[1]:+.3e} b1={b1:+.4e} qf k22={qf["kappa22"]:+.3e} k24={qf["kappa24"]:+.3e} k44={qf["kappa44"]:+.6e}', flush=True)
    return out
def phase3(C, P2):
    if not all(v['passed'] for v in C.values()): return {'verdict_class': 'INDETERMINATE', 'F-MS2-3': 'NOT-EVALUATED', 'F-MS2-4': 'NOT-EVALUATED', 'F-MS2-2': 'REGISTERED_NOT_EXECUTED', 'worst_S4': None}
    worst = max(max(abs(p['S4_E2']), abs(p['S4_h'])) for p in P2.values())
    fm3 = 'FIRES' if worst > TAU else 'SILENT'
    null = all(abs(P2[k]['kappa44_E2']) <= KFLOOR for k in ('cubic_step|001', 'cubic_gem8|001')); fm4 = 'FIRES' if null else 'SILENT'
    verdict = 'PROTECTION-BREACH' if fm3 == 'FIRES' else ('L4-NULL' if null else 'IDENTITY-DELIVERED-L4')
    return {'verdict_class': verdict, 'F-MS2-3': fm3, 'F-MS2-4': fm4, 'F-MS2-2': 'REGISTERED_NOT_EXECUTED', 'worst_S4': float(worst)}

# ----------------------------------------------------------------------------- commands
def base_checkpoint(T1):
    return {'gate': 'G-MSCS2', 'leg': 'chat', 'instrument': os.path.basename(__file__), 'instrument_md5': md5f(ME), 'memo_lock_md5': MEMO_MD5, 'memo_lock_bytes': MEMO_BYTES,
            'ledger_base_md5': LEDGER_BASE_MD5, 't1_list_md5': T1_MD5, 'x1_md5': X1_MD5, 'x6_chat_md5': X6C_MD5, 'x6_cc_md5': X6CC_MD5,
            'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'elections': ELECTIONS, 't1_scan': {'instrument': T1['instrument'], 'memo': T1['memo']},
            'quadrature': {'n_theta': N_THETA, 'n_phi': N_PHI, 'so3_grid': [16, 10, 16], 'n_grid': [12, 24]}, 't4_grid': T4_GRID, 't2t4_grid': T2T4}
def cmd_run(a):
    T1 = guards(); vrh = json.load(open(X1))['vrh']; x6 = json.load(open(X6C)); K, W = sphere_grid(N_THETA, N_PHI)
    print('phase0 ...', flush=True); C, hs_refs, xtal, vt0 = phase0(vrh, x6, K, W)
    for k, v in C.items(): print(f'  {k:16} passed={v["passed"]}  ' + ' '.join(f'{kk}={vv:.3e}' for kk, vv in v.items() if isinstance(vv, float)), flush=True)
    ck = base_checkpoint(T1); ck['phase0'] = C; ck['phase0_witness'] = {'single_crystal': xtal, 'vT_t0': vt0, 'hs_ref': hs_refs}
    ok = all(v['passed'] for v in C.values())
    if a.phase0_only or not ok:
        ck['phase2'] = {}; ck['phase3'] = phase3(C, {}) if not ok else {'verdict_class': 'NOT-ASSEMBLED (phase0-only run)', 'note': 'Phases 2-3 not executed on this run by the author\'s directive'}
        json.dump(ck, open(CHECKPOINT_P0, 'w'), indent=1); post = t1_gate({'checkpoint': CHECKPOINT_P0}); ck['T1_post_write'] = post; json.dump(ck, open(CHECKPOINT_P0, 'w'), indent=1)
        print(f'{"HALT: a Phase-0 pin/control failed -> INDETERMINATE" if not ok else "phase0 complete (phase0-only run)"}; checkpoint {os.path.basename(CHECKPOINT_P0)} {md5f(CHECKPOINT_P0)} ({os.path.getsize(CHECKPOINT_P0):,} B)  T1 post {post["checkpoint"]}')
        return
    print('phase2 ...', flush=True); ck['phase2'] = phase2(vrh, K, W, hs_refs); ck['phase3'] = phase3(C, ck['phase2'])
    json.dump(ck, open(CHECKPOINT, 'w'), indent=1); post = t1_gate({'checkpoint': CHECKPOINT}); ck['T1_post_write'] = post; json.dump(ck, open(CHECKPOINT, 'w'), indent=1)
    print(f'verdict_class {ck["phase3"]["verdict_class"]}  F-MS2-3 {ck["phase3"]["F-MS2-3"]}  F-MS2-4 {ck["phase3"]["F-MS2-4"]}  T1 post {post["checkpoint"]}')
    print(f'checkpoint {os.path.basename(CHECKPOINT)} {md5f(CHECKPOINT)} ({os.path.getsize(CHECKPOINT):,} B)')
def cmd_compare(a):
    ck = json.load(open(CHECKPOINT)); p2 = ck['phase2']; rows = []; cub = [k for k in KEYS if k.startswith('cubic')]; hexk = [k for k in KEYS if k.startswith('hex')]
    r1 = all(1e-3 <= abs(p2[k]['kappa44_E2']) <= 1e-2 for k in cub) and all(abs(p2[k]['kappa44_h']) < abs(p2[k]['kappa44_E2']) for k in cub)
    rows.append({'id': 'HYP-MS2-1', 'predicted': 'cubic kappa44_E2 != 0, |.| in [1e-3, 1e-2]; kappa44_h smaller', 'machine': {k: [p2[k]['kappa44_E2'], p2[k]['kappa44_h']] for k in cub}, 'concordant': bool(r1)})
    r2 = all(p2[k]['kappa44_E2'] < 0 for k in cub if '001' in k) and all(p2[k]['kappa44_E2'] > 0 for k in cub if '111' in k)
    rows.append({'id': 'HYP-MS2-2', 'predicted': 'sign kappa44(001) < 0, sign kappa44(111) > 0', 'machine': {k: p2[k]['kappa44_E2'] for k in cub}, 'concordant': bool(r2)})
    r3 = all(abs(p2[k]['S4_E2']) <= TAU and abs(p2[k]['S4_h']) <= TAU for k in KEYS)
    rows.append({'id': 'HYP-MS2-3', 'predicted': 'S4 = 0 within tau on all keys, both arms', 'machine': {k: [p2[k]['S4_E2'], p2[k]['S4_h']] for k in KEYS}, 'concordant': bool(r3)})
    r4 = all(abs(p2[k]['quadform']['kappa44']) < abs(p2[k]['quadform']['kappa22']) and abs(p2[k]['quadform']['kappa24']) > 1e-6 and abs(p2[k]['quadform']['kappa24']) < abs(p2[k]['quadform']['kappa22']) and abs(p2[k]['quadform']['kappa24']) > abs(p2[k]['quadform']['kappa44']) for k in hexk)
    rows.append({'id': 'HYP-MS2-4', 'predicted': 'hex |kappa44| < |kappa22|; kappa24 != 0 with |kappa44| < |kappa24| < |kappa22|', 'machine': {k: p2[k]['quadform'] for k in hexk}, 'concordant': bool(r4)})
    r5 = all(abs(p2[k]['biref_b1_VRH']) >= 0.03 and abs(p2[k]['biref_b1_VRH']) * 0.25 > 100 * abs(p2[k]['kappa44_E2']) * 0.25**2 for k in cub)
    rows.append({'id': 'HYP-MS2-5', 'predicted': 'fcc birefringence coefficient of order 1e-1 per unit t4; two orders above the descriptor split at t4 ~ 0.25', 'machine': {k: [p2[k]['biref_b1_VRH'], p2[k]['kappa44_E2']] for k in cub}, 'concordant': bool(r5)})
    out = {'gate': 'G-MSCS2', 'step': 'compare (last)', 'checkpoint_md5': md5f(CHECKPOINT), 'rows': rows, 'verdict_class': ck['phase3']['verdict_class'], 'n_concordant': sum(r['concordant'] for r in rows)}
    json.dump(out, open(COMPARE, 'w'), indent=1, default=float)
    for r in rows: print(('OK  ' if r['concordant'] else 'MISS'), r['id'], r['predicted'])
    print(f'compare {os.path.basename(COMPARE)} {md5f(COMPARE)}  verdict_class {ck["phase3"]["verdict_class"]}')
def cmd_selftest(a):
    n = 0
    def green(name): nonlocal n; n += 1; print(f'  green  {name}')
    Rs, ws = SO3
    # S1 ODF normalization and sphere-mean zero of K4t, K6t, P4
    assert abs(np.sum(ws) - 1) < 1e-13 and abs(np.sum(ws * K4tilde(Rs))) < 1e-13 and abs(np.sum(ws * K6tilde(Rs))) < 1e-13 and abs(np.sum(ws * P4((Rs @ Z)[:, 2]))) < 1e-13; green('S1 SO(3) weights sum to 1; K4t, K6t, P4 have zero mean')
    # S2 K4t range and marginals: max 1 at a cube axis along z, -2/3 at a body diagonal
    assert abs(K4tilde(np.eye(3)[None]) [0] - 1.0) < 1e-14
    R111 = np.array([[1/math.sqrt(2), -1/math.sqrt(6), 1/math.sqrt(3)], [-1/math.sqrt(2), -1/math.sqrt(6), 1/math.sqrt(3)], [0, 2/math.sqrt(6), 1/math.sqrt(3)]])
    R111 = R111.T   # third ROW = (1,1,1)/sqrt3: the body diagonal is carried to lab z
    assert abs(K4tilde(R111[None])[0] + 2.0 / 3.0) < 1e-13; green('S2 K4t = 1 on a cube axis, -2/3 on a body diagonal')
    # S3 exact closed form on a generic cubic tensor (Voigt) and l6 exhaustion
    c = {'C11': 2.0, 'C12': 0.9, 'C44': 0.7}; c4 = c4_from_constants('cubic', c); H = zener_H(c)
    T4V = np.zeros((6, 6)); T4V[0, 0] = T4V[1, 1] = 3; T4V[2, 2] = 8; T4V[0, 1] = T4V[1, 0] = 1; T4V[0, 2] = T4V[2, 0] = T4V[1, 2] = T4V[2, 1] = -4; T4V[3, 3] = T4V[4, 4] = -4; T4V[5, 5] = 1; T4V /= 105.0
    V0 = c4_to_voigt66(odf_avg_c4(c4, ODF('iso'))); V3 = c4_to_voigt66(odf_avg_c4(c4, ODF('K4', t4=0.3))); V6 = c4_to_voigt66(odf_avg_c4(c4, ODF('K4', t4=0.3, t6=0.3)))
    assert np.abs((V3 - V0) - 0.3 * H * T4V).max() < 1e-13 and np.abs(V6 - V3).max() < 1e-13; green('S3 closed form (H/3) T4(z) and l = 6 exhaustion on a synthetic cubic tensor')
    # S4 marginal identity: SO(3)-direct vs marginal average of frac_E2 for a fixed traceless S, both descriptor axes
    S = np.diag([1.0, -0.4, -0.6]); S = S + 0.3 * (np.outer(X, Y) + np.outer(Y, X))
    for axis, cm in ((Z, 1.0), (AX111, -2.0 / 3.0)):
        odf = ODF('K4', axis_c=axis, cmarg=cm, t4=0.4); fm = odf_avg_fracE2(S[None, None], odf)[0, 0]; fd = so3_direct_fracE2(S[None, None], odf, axis)[0, 0]
        assert abs(fm - fd) < 1e-13, (fm, fd)
    green('S4 marginal weights c(001) = 1, c(111) = -2/3 reproduce the SO(3)-direct average')
    # S5 frac_E2 identities and the 2/5 average; S2-h isotropic control
    T = np.diag([1.0, -1.0, 0.0]); assert abs(frac_E2(T, Z[None, :])[0] - 1.0) < 1e-14 and abs(odf_avg_fracE2(T, ODF('iso')) - 0.4) < 1e-14; green('S5 m=+-2 fraction identities; 2/5 SO(3) average')
    # S6 fits
    tt = [t for t in T4_GRID if abs(t) <= 0.25]; cf, r = fit_r(tt, [3e-3 * t * t - 2e-3 * t**3 for t in tt]); assert abs(cf[0]) < 1e-15 and rel(cf[1], 3e-3) < 1e-12
    t2s = np.array([a for a in T2T4 for b in T2T4]); t4s = np.array([b for a in T2T4 for b in T2T4]); qf = fit_quadform(t2s, t4s, 1e-3 * t2s**2 - 5e-4 * t2s * t4s + 2e-3 * t4s**2)
    assert rel(qf['kappa22'], 1e-3) < 1e-10 and rel(qf['kappa24'], -5e-4) < 1e-10 and rel(qf['kappa44'], 2e-3) < 1e-10; green('S6 fits recover coefficients (1-parameter and quadratic form)')
    # S7 Voigt birefringence identity: v_SH^2 - v_SV^2 = H t4 / 21 for k along x on the Voigt tensor
    V3t = odf_avg_c4(c4, ODF('K4', t4=0.3)); M = c4_to_voigt66(V3t); assert abs((M[5, 5] - M[3, 3]) - H * 0.3 / 21.0) < 1e-13; green('S7 Voigt birefringence identity H t4 / 21')
    print(f'ALL {n}/7 SUITES GREEN  (instrument {md5f(ME)})')
def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); p.add_argument('cmd', choices=['selftest', 'run', 'compare']); p.add_argument('--phase0-only', action='store_true')
    a = p.parse_args(); {'selftest': cmd_selftest, 'run': cmd_run, 'compare': cmd_compare}[a.cmd](a)
if __name__ == '__main__': main()
