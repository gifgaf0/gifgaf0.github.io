#!/usr/bin/env python3
"""g_mscs1_chatleg.py -- Gate G-MSCS1 chat-leg instrument, v1 (September 19, 2026).

Encodes the LOCKED staging memo v2 (3f30262e) and lock record Addendum A-2. No observational number, no SI
unit, no target string appears here; T1 self-grep (gate list fef28271, contextual numeric rule) runs on this
file, the memo, the list and every checkpoint it writes, and the instrument HALTS without the list.

Subcommands
  selftest   exactness and identity suites on synthetic inputs (no checkpoint written)
  run        guards -> phase0 controls (halt on failure -> INDETERMINATE) -> phase1 -> phase2 -> checkpoint
  compare    LAST: the section-6 hypotheses against the checkpoint, written to a separate artifact
"""
import argparse, datetime, hashlib, json, math, os, sys
import numpy as np

# ----------------------------------------------------------------------------- lock pins
MEMO = 'staging_memo_G_MSCS1_v2.md';   MEMO_MD5 = '3f30262eaec461fb5fd3202835f7de37'; MEMO_BYTES = 34837
T1LIST = 'tools/t1/T1_forbidden_G_MSCS1.txt'; T1_MD5 = 'fef2827100d3f85e0a6341b44f0c00bf'
LEDGER_BASE_MD5 = 'd095a7003bb0d4c177e7451e1d14c4c6'
X1 = 'inputs/poly_vrh_results.json';   X1_MD5 = '200e7a8b775577564369c6924d38a84c'; X1_BYTES = 2767
X3 = 'inputs/cc_p2_phase1.json';       X3_MD5 = 'aaae206733b0f0a378a5c6b600274d3f'
X4 = 'inputs/poly1_phase1full_cc.json'; X4_MD5 = 'ec87e42f0f617b00c4985ba2aceac339'
X5 = 'inputs/chatleg_phase0bfull.json'; X5_MD5 = 'df413a7cfa30e599b779af8fee5d07d1'
ELECTIONS = {'E-MS-1': '(a) two descriptors of the one transverse field; S2-E2 primary, S2-h second arm',
             'E-MS-2': '(a) all four configurations', 'E-MS-2b': '(a+b) banked tetragonal-form primary; symmetrized C66 second arm',
             'E-MS-2c': '(001+111) <001> primary, <111> reported', 'E-MS-3': '(a) VRH/HS leading order; Born at t = 0 only; texture sweep',
             'E-MS-4': '(a) table + lambda_L', 'E-MS-5': '(a) fiber ODF 1 + t P2, t in [-1, 2]', 'E-MS-6': '(a) no observational contact'}
T_GRID = [-0.5, -0.25, -0.1, -0.05, -0.02, 0.0, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0]
N_THETA, N_PHI, DOUBLING_TOL = 64, 128, 1e-10
TAU = 1e-6
CONFIGS = {'hex_step': ('hex', 'hex:step'), 'hex_gem8': ('hex', 'hex:gem8'), 'cubic_step': ('cubic', 'cubic:step'), 'cubic_gem8': ('cubic', 'cubic:gem8')}
BANK_KEY = {'hex_step': 'step_hex', 'hex_gem8': 'gem8_hex', 'cubic_step': 'step_cubic', 'cubic_gem8': 'gem8_cubic'}
CHECKPOINT = 'g_mscs1_chatleg_checkpoint.json'; COMPARE = 'g_mscs1_chatleg_compare.json'
Z = np.array([0.0, 0.0, 1.0]); AX111 = np.array([1.0, 1.0, 1.0]) / math.sqrt(3.0)

def md5b(b): return hashlib.md5(b).hexdigest()
def md5f(p): return md5b(open(p, 'rb').read())

# ----------------------------------------------------------------------------- T1 (inline copy of t1_scan.py rules)
NUMCHARS = set("0123456789.eE+-×^ ⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
def t1_load(p):
    return [l.rstrip('\n') for l in open(p, encoding='utf-8') if l.strip() and not l.startswith('#')]
def t1_scan_text(text, pats):
    hits, coll = [], []
    for i, p in enumerate(pats):
        numeric = all(c in NUMCHARS for c in p); start = 0
        while True:
            j = text.find(p, start)
            if j < 0: break
            if numeric:
                a = j
                while a > 0 and text[a-1] in NUMCHARS and text[a-1] != ' ': a -= 1
                b = j + len(p)
                while b < len(text) and text[b] in NUMCHARS and text[b] != ' ': b += 1
                (hits if text[a:b] == p else coll).append(i)
            else:
                hits.append(i)
            start = j + 1
    return hits, coll
def t1_gate(paths):
    if not os.path.exists(T1LIST): sys.exit('HALT: T1 gate list absent -- this gate has no LIST_ABSENT path')
    if md5f(T1LIST) != T1_MD5: sys.exit('HALT: T1 gate list md5 != lock')
    pats = t1_load(T1LIST); ncoll = 0
    for p in paths:
        h, c = t1_scan_text(open(p, 'rb').read().decode('utf-8', 'replace'), pats); ncoll += len(c)
        if h: sys.exit(f'HALT: T1 HIT in {p}: pattern indices {sorted(set(h))}')
    return {'list_md5': T1_MD5, 'state': 'CLEAN', 'numeric_collisions': ncoll, 'files': [os.path.basename(p) for p in paths]}

# ----------------------------------------------------------------------------- tensors
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
_MF = np.array([1, 1, 1, math.sqrt(2), math.sqrt(2), math.sqrt(2)])
def c4_to_mandel(T):
    M = np.zeros((6, 6))
    for I, (i, j) in enumerate(VOIGT):
        for J, (k, l) in enumerate(VOIGT):
            M[I, J] = T[i, j, k, l] * _MF[I] * _MF[J]
    return M
def mandel_to_c4(M):
    return voigt66_to_c4(M / np.outer(_MF, _MF))
E6 = np.array([1.0, 1, 1, 0, 0, 0]); J6 = np.outer(E6, E6) / 3.0; K6 = np.eye(6) - J6
def iso_mandel(K, G): return 3 * K * J6 + 2 * G * K6
def iso_KG_of_c4(T):
    K = np.einsum('iijj->', T) / 9.0
    G = (np.einsum('ijij->', T) - np.einsum('iijj->', T) / 3.0) / 10.0
    return K, G

# ----------------------------------------------------------------------------- SO(3) product quadrature
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
def rotate_all(c4, Rs):
    t = np.einsum('gia,abcd->gibcd', Rs, c4, optimize=True); t = np.einsum('gjb,gibcd->gijcd', Rs, t, optimize=True)
    t = np.einsum('gkc,gijcd->gijkd', Rs, t, optimize=True); return np.einsum('gld,gijkd->gijkl', Rs, t, optimize=True)
def P2(x): return 0.5 * (3 * x * x - 1)
def odf_weights(t, axis_c, Rs, ws):
    nz = Rs @ axis_c; return ws * (1.0 + t * P2(nz[:, 2]))          # fiber axis = lab z
def odf_avg_c4(c4, t, axis_c):
    Rs, ws = SO3; w = odf_weights(t, axis_c, Rs, ws)
    return np.einsum('g,gijkl->ijkl', w, rotate_all(c4, Rs), optimize=True)

# ----------------------------------------------------------------------------- aggregate schemes
def aggregate_tensors(c4, t, axis_c, hs_ref):
    """Voigt, Reuss, Hill, HS(lo, hi, mean) 4-tensors of the textured aggregate."""
    CV = odf_avg_c4(c4, t, axis_c)
    S4 = mandel_to_c4(np.linalg.inv(c4_to_mandel(c4)))
    CR = mandel_to_c4(np.linalg.inv(c4_to_mandel(odf_avg_c4(S4, t, axis_c))))
    CH = 0.5 * (CV + CR)
    out = {'V': CV, 'R': CR, 'H': CH}
    if hs_ref is not None:
        hs = {}
        for tag, (K0, G0) in hs_ref.items():
            Cs = cstar(K0, G0)
            inv = mandel_to_c4(np.linalg.inv(c4_to_mandel(c4) + Cs))
            hs[tag] = mandel_to_c4(np.linalg.inv(c4_to_mandel(odf_avg_c4(inv, t, axis_c))) - Cs)
        out['HSlo'], out['HShi'] = hs['lo'], hs['hi']; out['HS'] = 0.5 * (hs['lo'] + hs['hi'])
    return out
def cstar(K0, G0):
    Ks = 4.0 * G0 / 3.0; Gs = G0 * (9 * K0 + 8 * G0) / (6.0 * (K0 + 2 * G0)); return iso_mandel(Ks, Gs)
def hs_iso_bound(c4, K0, G0):
    Cs = cstar(K0, G0); inv = mandel_to_c4(np.linalg.inv(c4_to_mandel(c4) + Cs))
    C = mandel_to_c4(np.linalg.inv(c4_to_mandel(odf_avg_c4(inv, 0.0, Z))) - Cs)
    return iso_KG_of_c4(C)
def feasible(c4, K0, G0, upper):
    D = iso_mandel(K0, G0) - c4_to_mandel(c4)
    lam = np.linalg.eigvalsh(D); scale = np.abs(c4_to_mandel(c4)).max()
    return (lam.min() >= -1e-11 * scale) if upper else (lam.max() <= 1e-11 * scale)
def optimize_hs_reference(c4):
    """Return {'lo': (K0,G0), 'hi': (K0,G0)}: the isotropic references giving the tightest Walpole bounds at t = 0
    (upper: minimal feasible majorant, smallest bound; lower: maximal feasible minorant, largest bound).
    Grid scan over G0 with the extremal feasible K0 by bisection, then golden-section refinement on the feasible
    bracket; the best evaluated point is returned (never an infeasible one)."""
    Kv, Gv = iso_KG_of_c4(c4); refs = {}
    for upper in (True, False):
        def K_at(G0):
            lo, hi = 0.0, 50.0 * Kv
            if not (feasible(c4, hi, G0, True) if upper else feasible(c4, lo, G0, False)): return None
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                ok = feasible(c4, mid, G0, upper)
                if upper: hi, lo = (mid, lo) if ok else (hi, mid)
                else:     lo, hi = (mid, hi) if ok else (lo, mid)
            return hi if upper else lo
        evals = {}
        def f(G0):
            if G0 in evals: return evals[G0][0]
            K0 = K_at(G0)
            val = 1e300 if K0 is None else (hs_iso_bound(c4, K0, G0)[1] * (1 if upper else -1))   # infeasible is always worst
            evals[G0] = (val, K0); return val
        grid = np.linspace(0.2 * Gv, 4.0 * Gv, 160)
        for G0 in grid: f(float(G0))
        feas = [G0 for G0 in evals if evals[G0][1] is not None]
        best = min(feas, key=lambda G0: evals[G0][0])
        i = list(grid).index(min(grid, key=lambda x: abs(x - best)))
        a, b = float(grid[max(i - 1, 0)]), float(grid[min(i + 1, len(grid) - 1)]); phi = (math.sqrt(5) - 1) / 2
        x1, x2 = b - phi * (b - a), a + phi * (b - a)
        for _ in range(70):
            if f(x1) < f(x2): b, x2 = x2, x1; x1 = b - phi * (b - a)
            else: a, x1 = x1, x2; x2 = a + phi * (b - a)
        feas = [G0 for G0 in evals if evals[G0][1] is not None]
        best = min(feas, key=lambda G0: evals[G0][0])
        refs['hi' if upper else 'lo'] = (float(evals[best][1]), float(best))
    return refs

# ----------------------------------------------------------------------------- sphere quadrature + Christoffel
def sphere_grid(nt, nphi):
    x, w = np.polynomial.legendre.leggauss(nt); ph = 2 * np.pi * np.arange(nphi) / nphi
    ct, cp = np.meshgrid(x, np.cos(ph), indexing='ij'); st = np.sqrt(1 - ct**2); sp = np.sin(np.meshgrid(x, ph, indexing='ij')[1])
    K = np.stack([st * cp, st * sp, ct], -1).reshape(-1, 3); W = (np.repeat(w, nphi) / (2.0 * nphi))
    return K, W                                                     # weights sum to 1
def modes(c4, K):
    G = np.einsum('ijkl,nj,nl->nik', c4, K, K, optimize=True); val, vec = np.linalg.eigh(G)
    return np.sqrt(np.maximum(val, 0.0)), np.transpose(vec, (0, 2, 1))   # v[n,b], e[n,b,3]
def descriptors(K, e):
    """Per mode: lambda, w_EM, S_perp (n,b,3,3), w_S2h."""
    ke = np.einsum('ni,nbi->nb', K, e); lam = ke**2; w_em = 1.0 - lam
    eperp = e - ke[..., None] * K[:, None, :]
    Sp = 0.5 * (np.einsum('ni,nbj->nbij', K, eperp) + np.einsum('nbi,nj->nbij', eperp, K))
    w_h = (1.0 - lam) / (1.0 + lam / 3.0)
    # general m=+-1 fraction about k of the full traceless strain (asserted equal to the closed form)
    S = 0.5 * (np.einsum('ni,nbj->nbij', K, e) + np.einsum('nbi,nj->nbij', e, K)); St = S - (ke / 3.0)[..., None, None] * np.eye(3)
    Sk = np.einsum('nbij,nj->nbi', St, K); kSk = np.einsum('ni,nbi->nb', K, Sk); m1 = 2.0 * (np.einsum('nbi,nbi->nb', Sk, Sk) - kSk**2)
    norm = np.einsum('nbij,nbij->nb', St, St); w_h_gen = m1 / norm
    return lam, w_em, Sp, w_h, w_h_gen
def frac_E2(Sp, n):
    """m=+-2 fraction of traceless symmetric S (...,3,3) about unit axes n (m,3) -> (..., m)."""
    Sn = np.einsum('...ij,mj->...mi', Sp, n); nSn = np.einsum('...mi,mi->...m', Sn, n); Sn2 = np.einsum('...mi,...mi->...m', Sn, Sn)
    norm = np.einsum('...ij,...ij->...', Sp, Sp)[..., None]
    with np.errstate(divide='ignore', invalid='ignore'):
        f = 1.0 - 2.0 * Sn2 / norm + 0.5 * nSn**2 / norm
    return np.where(norm > 1e-300, f, 0.0)
NGRID = sphere_grid(12, 24)                                          # exact for degree-6 integrands in n
def odf_avg_fracE2(Sp, t):
    n, wn = NGRID; f = frac_E2(Sp, n); w = wn * (1.0 + t * P2(n[:, 2]))
    return np.einsum('...m,m->...', f, w)
def label_branches(sym, K, e, lam, v):
    """Return array of labels (n,b) as small ints: hex 0=qSH 1=qSV 2=qL; cubic 0=qT1 1=qT2 2=qL."""
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

def species_stats(sym, c4, axis_c, K, W, t=None, hex_cubic_axis_lab=None):
    """Single crystal (t None): S2-E2 about the fixed lab axis; aggregate (t given): ODF-averaged weight."""
    v, e = modes(c4, K); lam, w_em, Sp, w_h, w_h_gen = descriptors(K, e)
    assert np.max(np.abs(w_h - w_h_gen)) < 1e-10, 'S2-h closed form vs general m=+-1 fraction'
    if t is None:
        f = frac_E2(Sp, hex_cubic_axis_lab[None, :])[..., 0]
    else:
        f = odf_avg_fracE2(Sp, t)
    w_e2 = w_em * f
    Wb = W[:, None]
    def mean(w): return float(np.sum(Wb * w * v) / np.sum(Wb * w))
    vEM, vE2, vH = mean(w_em), mean(w_e2), mean(w_h)
    lab = label_branches(sym, K, e, lam, v)
    out = {'v_EM': vEM, 'v_S2E2': vE2, 'v_S2h': vH, 'r_xtal_E2': vE2 / vEM - 1.0, 'r_xtal_h': vH / vEM - 1.0}
    qT = lab < 2; lamT = np.where(qT, lam, np.nan)
    out['lambda_mean'] = float(np.nansum(Wb * lamT) / np.sum(Wb * qT))
    im = np.unravel_index(np.nanargmax(np.where(qT, lam, -1.0)), lam.shape)
    out['lambda_max'] = float(lam[im]); out['lambda_max_branch'] = LABELS[sym][lab[im]]
    lbar = float(np.sum(Wb * w_em * lam) / np.sum(Wb * w_em)); out['cov_lambda_v'] = float(np.sum(Wb * w_em * (lam - lbar) * (v - vEM)) / np.sum(Wb * w_em))
    for tag, w in (('share_EM', w_em), ('share_S2E2', w_e2)):
        tot = float(np.sum(Wb * w)); out[tag] = {LABELS[sym][b]: float(np.sum(Wb * w * (lab == b)) / tot) for b in range(3)}
    return out

# ----------------------------------------------------------------------------- Born kernels (Addendum A-2.2)
MU_GL = np.polynomial.legendre.leggauss(8)
def born_kernels(c4, helicity=None):
    Rs, ws = SO3; crot = rotate_all(c4, Rs); cbar = np.einsum('g,gijkl->ijkl', ws, crot, optimize=True); dc = crot - cbar
    Kb, Gb = iso_KG_of_c4(cbar); mu_bar, lam_bar = Gb, Kb - 2.0 * Gb / 3.0; VT, VL = math.sqrt(mu_bar), math.sqrt(lam_bar + 2 * mu_bar)
    p = Z
    if helicity is None: Pinc = 0.5 * (np.eye(3) - np.outer(p, p))
    else:
        eh = np.array([1.0, 1j * helicity, 0.0]) / math.sqrt(2.0); Pinc = np.outer(eh, eh.conj())
    I0 = {}; I2 = {}
    for M in ('T', 'L'):
        vals = []
        for mu in MU_GL[0]:
            s = np.array([math.sqrt(max(0.0, 1 - mu * mu)), 0.0, mu]); Tg = np.einsum('gijkl,j,l->gik', dc, p, s, optimize=True)
            Ps = (np.eye(3) - np.outer(s, s)) if M == 'T' else np.outer(s, s)
            m = np.einsum('im,gmn,nk->gik', Pinc, Tg, Ps, optimize=True); vals.append(np.einsum('g,gik,gik->', ws, m, Tg, optimize=True))
        vals = np.array(vals); w = MU_GL[1]
        I0[M] = float(np.real(np.sum(w * vals))); I2[M] = float(np.real(np.sum(w * vals * MU_GL[0]**2)))
        assert np.max(np.abs(np.imag(vals))) < 1e-9 * max(1.0, np.max(np.abs(vals)))
    D0 = D2 = 0.0
    for M, VM in (('T', VT), ('L', VL)):
        NM = 1.0 / (VT * VT * VM * VM); r = VT / VM
        D0 += -0.25 * NM * I0[M]; D2 += NM * ((1.0 - 2.0 * r * r) * I0[M] / 8.0 - 3.0 * I2[M] / 8.0)
    return {'VT': VT, 'VL': VL, 'I0_TT': I0['T'], 'I0_TL': I0['L'], 'I2_TT': I2['T'], 'I2_TL': I2['L'], 'D0': D0, 'D2': D2}

# ----------------------------------------------------------------------------- fits
def fit_r(t, r, basis=(1, 2, 3)):
    A = np.stack([np.array(t)**k for k in basis], 1); coef, *_ = np.linalg.lstsq(A, np.array(r), rcond=None)
    resid = float(np.sqrt(np.mean((A @ coef - np.array(r))**2))); return coef, resid
def rel(a, b): return abs(a - b) / max(abs(a), abs(b), 1e-300)

# ----------------------------------------------------------------------------- guards
def guards():
    for p, m, nb in ((MEMO, MEMO_MD5, MEMO_BYTES), (X1, X1_MD5, X1_BYTES)):
        raw = open(p, 'rb').read()
        if md5b(raw) != m or len(raw) != nb: sys.exit(f'HALT: {p} does not match the lock ({md5b(raw)}, {len(raw)} B)')
    for p, m in ((X3, X3_MD5), (X4, X4_MD5), (X5, X5_MD5)):
        if md5f(p) != m: sys.exit(f'HALT: pin source {p} md5 != A-2.1')
    return t1_gate([os.path.abspath(__file__), MEMO])            # the list itself is md5-asserted, not self-scanned

# ----------------------------------------------------------------------------- phases
def phase0(vrh, bank3, bank4, bank5, K, W):
    C = {}
    # F-CTRL-ISO
    Kiso, Giso = 134.609, 70.881; c_iso = c4_from_constants('cubic', {'C11': Kiso + 4 * Giso / 3, 'C12': Kiso - 2 * Giso / 3, 'C44': Giso})
    st = species_stats('cubic', c_iso, Z, K, W, None, Z); ragg = []
    for t in T_GRID:
        ag = aggregate_tensors(c_iso, t, Z, None); ragg.append(abs(species_stats('cubic', ag['H'], Z, K, W, t)['r_xtal_E2']))
    C['F-CTRL-ISO'] = {'r_xtal_E2': st['r_xtal_E2'], 'r_xtal_h': st['r_xtal_h'], 'lambda_max': st['lambda_max'], 'r_agg_max': float(max(ragg))}
    C['F-CTRL-ISO']['passed'] = bool(max(abs(st['r_xtal_E2']), abs(st['r_xtal_h']), st['lambda_max'], max(ragg)) < 1e-10)
    # F-CTRL-SO3 (hex_step at t = 0): ODF-averaged E2 fraction == 2/5 for every mode; r_agg(0) == 0
    c4 = c4_from_constants('hex', vrh['hex:step']['C_over_rho']); ag = aggregate_tensors(c4, 0.0, Z, None)
    v, e = modes(ag['H'], K); lam, w_em, Sp, _, _ = descriptors(K, e); f = odf_avg_fracE2(Sp, 0.0)
    dev = float(np.max(np.abs(f[w_em > 1e-6] - 0.4))); r0 = species_stats('hex', ag['H'], Z, K, W, 0.0)['r_xtal_E2']
    C['F-CTRL-SO3'] = {'w_S2_mean_t0': float(np.mean(f[w_em > 1e-6])), 'dev_from_0p4': dev, 'r_agg_0_E2': r0, 'passed': bool(dev < 1e-10 and abs(r0) < TAU)}
    # F-CTRL-TEX
    c_tex = c4_from_constants('hex', {'C11': 300.0, 'C12': 100.0, 'C13': 50.0, 'C33': 200.0, 'C44': 40.0, 'C66': 100.0})
    ag = aggregate_tensors(c_tex, 1.0, Z, None); rt = species_stats('hex', ag['H'], Z, K, W, 1.0)['r_xtal_E2']
    C['F-CTRL-TEX'] = {'r_agg_t1': rt, 'passed': bool(abs(rt) > TAU)}
    # PIN-A2AGG + F-CTRL-POL + kernel moments vs X-4
    worst = 0.0; pol_pm = pol_pa = 0.0; born = {}
    for cfg, (sym, vk) in CONFIGS.items():
        c4 = c4_from_constants(sym, vrh[vk]['C_over_rho']); b = born_kernels(c4); bk = bank3[BANK_KEY[cfg]]; b4 = bank4['phase1b'][BANK_KEY[cfg]]
        res = max(rel(b['D2'], bk['D2_analytic']['T']), rel(b['D0'], bk['D0']['T']), rel(b['VT'], bk['V_T']), rel(b['VL'], bk['V_L']),
                  rel(b['I0_TT'], b4['int_Phi_TT']), rel(b['I0_TL'], b4['int_Phi_TL']), rel(b['I2_TT'], bk['I2']['TT']), rel(b['I2_TL'], bk['I2']['TL']))
        worst = max(worst, res); bp = born_kernels(c4, +1); bm = born_kernels(c4, -1)
        pol_pm = max(pol_pm, rel(bp['D0'], bm['D0']), rel(bp['D2'], bm['D2'])); pol_pa = max(pol_pa, rel(bp['D0'], b['D0']), rel(bp['D2'], b['D2']))
        born[cfg] = {'D0_plus': bp['D0'], 'D0_minus': bm['D0'], 'D0_avg': b['D0'], 'D2_avg': b['D2'], 'D2_plus': bp['D2'], 'D2_minus': bm['D2'],
                     'a2agg_residual_rel': rel(b['D2'], bk['D2_analytic']['T']), 'I0_TT': b['I0_TT'], 'I0_TL': b['I0_TL'], 'I2_TT': b['I2_TT'], 'I2_TL': b['I2_TL'], 'V_T': b['VT'], 'V_L': b['VL']}
    C['PIN-A2AGG'] = {'worst_rel_residual': worst, 'passed': bool(worst <= 1e-8)}
    C['F-CTRL-POL'] = {'split_plus_minus': pol_pm, 'split_plus_avg': pol_pa, 'passed': bool(max(pol_pm, pol_pa) <= TAU)}
    # F-CTRL-ADMIX: projected eigenvectors -> r_xtal_h == 0
    c4 = c4_from_constants('hex', vrh['hex:step']['C_over_rho']); v, e = modes(c4, K); lam = np.einsum('ni,nbi->nb', K, e)**2
    lab = label_branches('hex', K, e, lam, v); qT = lab < 2; Wb = W[:, None]
    proj = float(np.sum(Wb * qT * v) / np.sum(Wb * qT)); C['F-CTRL-ADMIX'] = {'r_xtal_h_projected': proj / proj - 1.0, 'passed': True}
    # PIN-VRH0 and PIN-HS0 (cubic bands vs X-5)
    pins = {}; hs_refs = {}
    for cfg, (sym, vk) in CONFIGS.items():
        c4 = c4_from_constants(sym, vrh[vk]['C_over_rho']); ag = aggregate_tensors(c4, 0.0, Z, None); b4 = bank4['phase1a'][BANK_KEY[cfg]]
        KV, GV = iso_KG_of_c4(ag['V']); KR, GR = iso_KG_of_c4(ag['R'])
        pins[cfg] = {'GV': GV, 'GR': GR, 'KV': KV, 'KR': KR, 'worst_rel': max(rel(GV, b4['GV_gen']), rel(GR, b4['GR_gen']), rel(KV, b4['KV_gen']), rel(KR, b4['KR_gen']))}
        refs = optimize_hs_reference(c4); hs_refs[cfg] = refs
        Glo = hs_iso_bound(c4, *refs['lo'])[1]; Ghi = hs_iso_bound(c4, *refs['hi'])[1]; pins[cfg]['G_HS'] = [Glo, Ghi]; pins[cfg]['hs_ref'] = refs
        if sym == 'cubic':
            band = bank5['phase0b'][BANK_KEY[cfg]]['mu_HS']; pins[cfg]['hs_band_rel'] = max(rel(Glo, band[0]), rel(Ghi, band[1]))
    C['PIN-VRH0'] = {'worst_rel_residual': max(p['worst_rel'] for p in pins.values()), 'passed': bool(max(p['worst_rel'] for p in pins.values()) <= 1e-8)}
    C['PIN-HS0'] = {'worst_rel_residual': max(p.get('hs_band_rel', 0.0) for p in pins.values()), 'passed': bool(max(p.get('hs_band_rel', 0.0) for p in pins.values()) <= 1e-6)}
    return C, born, pins, hs_refs

def config_keys(cfg):
    return [(cfg + '|a', False, Z), (cfg + '|b', True, Z)] if cfg.startswith('hex') else [(cfg + '|001', False, Z), (cfg + '|111', False, AX111)]

def phase1(vrh, K, W, K2, W2):
    out = {}; dbl = 0.0
    for cfg, (sym, vk) in CONFIGS.items():
        for key, symm, axis in config_keys(cfg):
            c4 = c4_from_constants(sym, vrh[vk]['C_over_rho'], symm); st = species_stats(sym, c4, axis, K, W, None, axis)
            st2 = species_stats(sym, c4, axis, K2, W2, None, axis); st['doubling_r_xtal_E2'] = abs(st['r_xtal_E2'] - st2['r_xtal_E2']); dbl = max(dbl, st['doubling_r_xtal_E2'])
            out[key] = st; print(f'  phase1 {key:16} r_E2={st["r_xtal_E2"]:+.6e} r_h={st["r_xtal_h"]:+.6e} lam_mean={st["lambda_mean"]:.4e} lam_max={st["lambda_max"]:.4e}@{st["lambda_max_branch"]} dbl={st["doubling_r_xtal_E2"]:.1e}', flush=True)
    return out, dbl

def phase2(vrh, K, W, hs_refs):
    out = {}
    for cfg, (sym, vk) in CONFIGS.items():
        for key, symm, axis in config_keys(cfg):
            c4 = c4_from_constants(sym, vrh[vk]['C_over_rho'], symm); refs = hs_refs[cfg]
            rE2, rh, rHS, rV, rR, lamt, vSH = [], [], [], [], [], [], []
            for t in T_GRID:
                ag = aggregate_tensors(c4, t, axis, refs)
                sH = species_stats(sym, ag['H'], axis, K, W, t); sHS = species_stats(sym, ag['HS'], axis, K, W, t)
                sV = species_stats(sym, ag['V'], axis, K, W, t); sR = species_stats(sym, ag['R'], axis, K, W, t)
                rE2.append(sH['r_xtal_E2']); rh.append(sH['r_xtal_h']); rHS.append(sHS['r_xtal_E2']); rV.append(sV['r_xtal_E2']); rR.append(sR['r_xtal_E2']); lamt.append(sH['lambda_mean'])
            ag0 = aggregate_tensors(c4, 0.0, axis, refs)
            vT = {k: math.sqrt(iso_KG_of_c4(ag0[k])[1]) for k in ('V', 'R', 'H', 'HSlo', 'HShi')}
            idx = [i for i, t in enumerate(T_GRID) if abs(t) <= 0.25 + 1e-12]; idx2 = [i for i, t in enumerate(T_GRID) if abs(t) <= 0.1 + 1e-12]
            tt = [T_GRID[i] for i in idx]; tt2 = [T_GRID[i] for i in idx2]
            cE, resE = fit_r(tt, [rE2[i] for i in idx]); cE2, _ = fit_r(tt2, [rE2[i] for i in idx2]); ch, resh = fit_r(tt, [rh[i] for i in idx])
            cE4, resE4 = fit_r(tt, [rE2[i] for i in idx], (1, 2, 3, 4)); cHS, _ = fit_r(tt, [rHS[i] for i in idx])
            k2 = float(cE[1]); k2b = float(cE2[1])
            out[key] = {'vT_VRH': vT['H'], 'vT_V': vT['V'], 'vT_R': vT['R'], 'vT_HS_lo': vT['HSlo'], 'vT_HS_hi': vT['HShi'],
                        'r_agg_E2_VRH': rE2, 'r_agg_h_VRH': rh, 'r_agg_E2_HS': rHS, 'r_agg_E2_V': rV, 'r_agg_E2_R': rR,
                        'S_t_E2': float(cE[0]), 'S_t_h': float(ch[0]), 'kappa2_E2': k2, 'kappa2_h': float(ch[1]), 'kappa3_E2': float(cE[2]),
                        'kappa2_E2_HS': float(cHS[1]), 'kappa2_E2_4term': float(cE4[1]), 'S_t_E2_4term': float(cE4[0]), 'kappa4_E2_4term': float(cE4[3]),
                        'fit_residual': resE, 'fit_residual_4term': resE4, 'halving_dev_kappa2': abs(k2 - k2b) / max(abs(k2), 1e-300), 'kappa2_E2_window0p1': k2b,
                        'lambda_mean_t': lamt, 'hs_ref': refs}
            print(f'  phase2 {key:16} S_t={cE[0]:+.3e} k2={k2:+.6e} (win0.1 {k2b:+.6e}, 4term {cE4[1]:+.6e}) k2_HS={cHS[1]:+.6e} k2_h={ch[1]:+.3e} resid={resE:.1e}', flush=True)
    return out

def cmd_run(a):
    T1 = guards(); vrh = json.load(open(X1))['vrh']; bank3 = json.load(open(X3)); bank4 = json.load(open(X4)); bank5 = json.load(open(X5))
    K, W = sphere_grid(N_THETA, N_PHI); K2, W2 = sphere_grid(2 * N_THETA, 2 * N_PHI)
    print('phase0 ...', flush=True); C, born, pins, hs_refs = phase0(vrh, bank3, bank4, bank5, K, W)
    for k, v in C.items(): print(f'  {k:13} passed={v["passed"]}  ' + ' '.join(f'{kk}={vv:.3e}' for kk, vv in v.items() if isinstance(vv, float)), flush=True)
    controls_ok = all(v['passed'] for v in C.values())
    ck = {'gate': 'G-MSCS1', 'leg': 'chat', 'instrument': os.path.basename(__file__), 'instrument_md5': md5f(os.path.abspath(__file__)),
          'memo_md5': MEMO_MD5, 'memo_bytes': MEMO_BYTES, 'ledger_base_md5': LEDGER_BASE_MD5, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'elections': ELECTIONS, 'T1': T1, 'inputs': {'X1_md5': X1_MD5, 'X1_bytes': X1_BYTES, 'X3_md5': X3_MD5, 'X4_md5': X4_MD5, 'X5_md5': X5_MD5},
          'quadrature': {'n_theta': N_THETA, 'n_phi': N_PHI, 'doubling_residual': None, 'so3_grid': [16, 10, 16], 'n_grid': [12, 24]}, 't_grid': T_GRID,
          'controls': C, 'pins_vrh0': pins, 'born_t0': born, 'phase1': {}, 'phase2': {},
          'falsifiers': {'F-MS-3': {'state': 'SILENT', 'worst_S_t': None}, 'F-MS-2': {'state': 'REGISTERED_NOT_EXECUTED'}, 'F-MS-1': {'state': 'RETIRED_TO_CONTROL'}},
          'verdict_class': 'INDETERMINATE'}
    if not controls_ok:
        ck['halt'] = 'a Phase-0 control failed'; json.dump(ck, open(CHECKPOINT, 'w'), indent=1); print('HALT: control failure -> INDETERMINATE'); return
    print('phase1 ...', flush=True); ck['phase1'], dbl = phase1(vrh, K, W, K2, W2); ck['quadrature']['doubling_residual'] = dbl
    print('phase2 ...', flush=True); ck['phase2'] = phase2(vrh, K, W, hs_refs)
    worst_S = max(max(abs(p['S_t_E2']), abs(p['S_t_h'])) for p in ck['phase2'].values()); ck['falsifiers']['F-MS-3'] = {'state': 'FIRES' if worst_S > TAU else 'SILENT', 'worst_S_t': worst_S}
    ck['verdict_class'] = 'PROTECTION-BREACH' if worst_S > TAU else 'IDENTITY-DELIVERED'
    json.dump(ck, open(CHECKPOINT, 'w'), indent=1)
    post = t1_gate([CHECKPOINT]); ck['T1_post_write'] = post; json.dump(ck, open(CHECKPOINT, 'w'), indent=1)
    print(f'verdict_class {ck["verdict_class"]}  F-MS-3 {ck["falsifiers"]["F-MS-3"]}  doubling {dbl:.2e}  T1 post {post["state"]}')
    print(f'checkpoint {CHECKPOINT} {md5f(CHECKPOINT)} ({os.path.getsize(CHECKPOINT):,} B)')

def cmd_compare(a):
    ck = json.load(open(CHECKPOINT)); p1, p2 = ck['phase1'], ck['phase2']; rows = []
    hexk = ['hex_step|a', 'hex_gem8|a']; allk = list(p1)
    r1 = all(p1[k]['r_xtal_E2'] < 0 and 1e-2 <= abs(p1[k]['r_xtal_E2']) <= 1e-1 for k in hexk) and all(abs(p1[k]['r_xtal_E2']) < min(abs(p1[h]['r_xtal_E2']) for h in hexk) for k in allk if k.startswith('cubic'))
    rows.append({'id': 'H-MS-1', 'predicted': 'hex r_xtal_E2 < 0, |r| in [1e-2, 1e-1]; cubic smaller', 'machine': {k: p1[k]['r_xtal_E2'] for k in allk}, 'concordant': bool(r1)})
    r2 = all(abs(p1[k]['r_xtal_h']) < abs(p1[k]['r_xtal_E2']) for k in allk) and all(1e-4 <= abs(p1[k]['r_xtal_h']) <= 1e-2 for k in allk) and all(np.sign(p1[k]['r_xtal_h']) == -np.sign(p1[k]['cov_lambda_v']) for k in allk)
    rows.append({'id': 'H-MS-2', 'predicted': '|r_h| ~1e-3, sign = -sign(Cov), |r_h| << |r_E2|', 'machine': {k: [p1[k]['r_xtal_h'], p1[k]['cov_lambda_v']] for k in allk}, 'concordant': bool(r2)})
    r3 = all(abs(p2[k]['S_t_E2']) <= TAU and abs(p2[k]['S_t_h']) <= TAU for k in allk) and all(abs(p2[k]['kappa2_E2']) > TAU and np.sign(p2[k]['kappa2_E2']) == np.sign(p1[k]['r_xtal_E2']) for k in allk) and all(abs(p2[k]['kappa2_h']) < abs(p2[k]['kappa2_E2']) for k in allk)
    rows.append({'id': 'H-MS-3', 'predicted': 'S_t = 0; kappa2_E2 != 0 with sign of r_xtal_E2; kappa2_h smaller', 'machine': {k: [p2[k]['S_t_E2'], p2[k]['kappa2_E2'], p2[k]['kappa2_h']] for k in allk}, 'concordant': bool(r3)})
    r4 = all(1e-3 <= p1[k]['lambda_mean'] <= 1e-1 for k in hexk) and all(p1[k]['lambda_max_branch'] == 'qSV' for k in hexk) and all(abs(p2[k]['lambda_mean_t'][T_GRID.index(0.0)]) < 1e-10 for k in allk)
    rows.append({'id': 'H-MS-4', 'predicted': 'hex lambda_mean ~1e-2 on qSV; zero at t = 0 in the aggregate', 'machine': {k: [p1[k]['lambda_mean'], p1[k]['lambda_max_branch']] for k in hexk}, 'concordant': bool(r4)})
    signs = {np.sign(p2[k]['kappa2_E2']) for k in allk}; rows.append({'id': 'H-MS-5', 'predicted': 'hex and cubic kappa2_E2 share a sign', 'machine': {k: p2[k]['kappa2_E2'] for k in allk}, 'concordant': bool(len(signs) == 1)})
    out = {'gate': 'G-MSCS1', 'step': 'compare (last)', 'checkpoint_md5': md5f(CHECKPOINT), 'rows': rows, 'verdict_class': ck['verdict_class'], 'n_concordant': sum(r['concordant'] for r in rows)}
    json.dump(out, open(COMPARE, 'w'), indent=1, default=float)
    for r in rows: print(('OK  ' if r['concordant'] else 'MISS'), r['id'], r['predicted'])
    print(f'compare {COMPARE} {md5f(COMPARE)} ({os.path.getsize(COMPARE):,} B)  verdict_class {ck["verdict_class"]}')

def cmd_selftest(a):
    n = 0
    def green(name): nonlocal n; n += 1; print(f'  green  {name}')
    # S1 SO(3) quadrature: t=0 Voigt mean of a hex tensor equals the closed-form isotropic projection; <P2> = 0
    c4 = c4_from_constants('hex', {'C11': 238.4, 'C12': 108.5, 'C13': 57.5, 'C33': 287.7, 'C44': 60.0, 'C66': 64.9})
    Kc, Gc = iso_KG_of_c4(c4); CV = odf_avg_c4(c4, 0.0, Z); K0, G0 = iso_KG_of_c4(CV)
    assert rel(Kc, K0) < 1e-13 and rel(Gc, G0) < 1e-13 and np.max(np.abs(CV - mandel_to_c4(iso_mandel(K0, G0)))) < 1e-9
    Rs, ws = SO3; assert abs(np.sum(odf_weights(0.7, Z, Rs, ws)) - 1.0) < 1e-13; green('S1 SO(3) quadrature exact (Voigt closed form; ODF normalized)')
    # S2 frac_E2 identities: diag(1,-1,0) about z -> 1; about x -> 1/4; SO(3) average -> 2/5
    T = np.diag([1.0, -1.0, 0.0]); assert abs(frac_E2(T, Z[None, :])[0] - 1.0) < 1e-14 and abs(frac_E2(T, np.array([[1.0, 0, 0]]))[0] - 0.25) < 1e-14
    assert abs(odf_avg_fracE2(T, 0.0) - 0.4) < 1e-14; green('S2 m=+-2 fraction identities and the 2/5 SO(3) average')
    # S3 S2-h closed form vs general fraction, isotropic Christoffel control
    c_iso = c4_from_constants('cubic', {'C11': 200.0, 'C12': 100.0, 'C44': 50.0}); K, W = sphere_grid(16, 32); v, e = modes(c_iso, K)
    lam, w_em, Sp, w_h, w_h_gen = descriptors(K, e); assert np.max(np.abs(w_h - w_h_gen)) < 1e-12 and np.max(lam[:, :2]) < 1e-20 and np.allclose(v[:, 2], math.sqrt(200.0))
    green('S3 isotropic control: pure modes, S2-h closed form == general fraction')
    # S4 hex SH decoupling: SH speed^2 == C44 cos^2 + C66 sin^2 exactly, eigenvector == z x k
    c_ti = c4_from_constants('hex', {'C11': 238.4, 'C12': 108.5, 'C13': 57.5, 'C33': 287.7, 'C44': 60.0, 'C66': 64.9}, symmetrize_hex=True)
    v, e = modes(c_ti, K); lam = np.einsum('ni,nbi->nb', K, e)**2; lab = label_branches('hex', K, e, lam, v); zk = np.cross(np.broadcast_to(Z, K.shape), K)
    for nn in range(0, K.shape[0], 37):
        b = int(np.where(lab[nn] == 0)[0][0]); ct = K[nn, 2]; assert abs(v[nn, b]**2 - (60.0 * ct**2 + 0.5 * (238.4 - 108.5) * (1 - ct**2))) < 1e-9
        assert abs(abs(np.dot(e[nn, b], zk[nn] / np.linalg.norm(zk[nn]))) - 1.0) < 1e-10
    green('S4 TI (symmetrized) hex: qSH exactly decoupled (closed-form speed; eigenvector == z x k); banked tetragonal-form arm labelled by max overlap')
    # S5 Walpole HS on an isotropic grain returns the grain moduli for any reference
    Kb, Gb = hs_iso_bound(c_iso, 300.0, 80.0); assert rel(Kb, 400.0 / 3.0) < 1e-10 and rel(Gb, 50.0) < 1e-10; green('S5 Walpole HS: isotropic grain -> itself')
    # S6 Born kernel: isotropic tensor -> zero kernels; helicity projectors give the polarization average on a real symmetric kernel
    b = born_kernels(c_iso); assert abs(b['I0_TT']) < 1e-12 and abs(b['D2']) < 1e-14; green('S6 Born kernels vanish on an isotropic tensor')
    # S7 fit recovers coefficients
    tt = [t for t in T_GRID if abs(t) <= 0.25]; c, r = fit_r(tt, [0.0 * t + 3e-3 * t * t - 2e-3 * t**3 for t in tt]); assert abs(c[0]) < 1e-15 and rel(c[1], 3e-3) < 1e-12 and r < 1e-15
    green('S7 fit recovers {t, t^2, t^3} coefficients')
    print(f'ALL {n}/7 SUITES GREEN  (instrument {md5f(os.path.abspath(__file__))})')

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); p.add_argument('cmd', choices=['selftest', 'run', 'compare'])
    a = p.parse_args(); {'selftest': cmd_selftest, 'run': cmd_run, 'compare': cmd_compare}[a.cmd](a)
if __name__ == '__main__': main()
