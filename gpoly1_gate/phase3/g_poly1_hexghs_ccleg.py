#!/usr/bin/env python3
# g_poly1_hexghs_ccleg.py — CC-leg confirmation of the hex G_HS completion.
# Independent implementation (zero-shared-machinery) from the verbatim pins:
#   PIN ADDENDUM 1 (57dfd40e...) — hexagonal branch, eqs (2),(3),(6),(11),
#     (20)-(24),(36)-(41),(44),(45),(48), delta-shift prescription;
#   PIN ADDENDUM 2 (3d419b8f...) — tetragonal branch, eqs (31)-(35),(13),(43),
#     (47),(50); tetragonal-primary convention for the framework tensors.
# Five controls + two framework tensors; the CC checkpoint is hashed BEFORE the
# embedded chat G_HS checkpoint is consulted (dispatch S2(g)).
# Pure python (no third-party deps); grids + golden-section refinement.
import hashlib, json, math, os

T1 = ['M'+'pc', 'G'+'pc', 'H'+'z', 'G'+'W', 'LI'+'GO', '17'+'0817',
      chr(51)+'.'+'19', '0.0'+'19', '2997'+'92458', 'S'+'ME']
_me = open(__file__, encoding='utf-8').read()
_body = _me.split('# T1'+'-WALL-END')[1].lower()
for _t in T1:
    assert _t.lower() not in _body, 'T1 HIT in CC G_HS source: ' + _t.lower()
print('T1 self-grep (CC G_HS instrument source, case-insensitive): PASS')
# T1-WALL-END

HERE = os.path.dirname(os.path.abspath(__file__))
VRH = os.path.join(HERE, 'embeds', 'poly_vrh_results.json')
CKPATH = os.path.join(HERE, 'poly1_hexghs_cc.json')

raw = open(VRH, 'rb').read()
assert hashlib.md5(raw).hexdigest() == '200e7a8b775577564369c6924d38a84c'
D = json.loads(raw)

# ---- shared Peselnick-Meister/Watt machinery ---------------------------------------
def pm_side(KV, GV, GR, terms, G):
    """One comparison-modulus evaluation. terms = [(count, modulus), ...] for the
    non-first bracket entries of (11)/(13). Returns None when inadmissible."""
    if G <= 0.0 or abs(GV - G) < 1e-300:
        return None
    K = KV * (GR - G) / (GV - G)                                   # (44)
    if K <= 0.0:
        return None
    al = -1.0 / (K + 4.0 * G / 3.0)                                # (38)
    be = 2.0 * al / 15.0 - 1.0 / (5.0 * G)
    ze = (G / 6.0) * (9.0 * K + 8.0 * G) / (K + 2.0 * G)           # (3)
    id2 = abs(1.0 + 2.0 * be * G + 2.0 * be * ze) / abs(2.0 * be * ze)   # (2)
    s = (1.0 - al * (KV - K)) / (GV + ze + (al / (2.0 * be)) * (KV - K))
    for c, mod in terms:
        s += c / (mod + ze)
    mu = 5.0 / s - ze                                              # (11)/(13)
    Dp = 1.0 - 2.0 * be * (GV - G) - al * (KV - K)                 # (41)
    B2 = (GV - G) / Dp
    for c, mod in terms:
        B2 += c * (mod - G) / (1.0 - 2.0 * be * (mod - G))
    B2 /= 5.0                                                      # (39)/(43)
    mu_b = G + B2 / (1.0 + 2.0 * be * B2)                          # (37)
    K6 = KV * (GR + ze) / (GV + ze)                                # (6)
    K36 = K + (KV - K) / (1.0 + 2.0 * be * (G - GV))               # (36)
    return dict(mu=mu, K_PM=K6, K_comp=K, zeta=ze, id2=id2,
                mu_route=abs(mu_b - mu) / abs(mu),
                K_route=abs(K6 - K36) / abs(K6))

def _ok(r):
    return r is not None and r['id2'] < 1e-10 and r['mu_route'] < 1e-9 \
        and r['K_route'] < 1e-9

def loggrid(lo, hi, n):
    la, lb = math.log10(lo), math.log10(hi)
    return [10.0 ** (la + (lb - la) * i / (n - 1)) for i in range(n)]

def golden_min(f, a, b, iters=90):
    """Golden-section minimum of f over [a, b] in log10-delta space."""
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    fc, fd = f(c), f(d)
    for _ in range(iters):
        if fc <= fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = f(d)
    return (c if fc <= fd else d)

def bounds(KV, GV, GR, terms, Gm, Gp):
    """Lower at Gm (delta-free). Upper: direct at Gp when non-singular; when
    Gp == GV (singular case) minimized over the ADMISSIBLE delta family
    G = GV*(1+delta) with comparison moduli positive (K+ > 0, G+ > 0); the
    K+ < 0 sliver is excluded as non-variational (Addendum 2 convention)."""
    lo = pm_side(KV, GV, GR, terms, Gm)
    assert _ok(lo), 'lower-bound evaluation failed cross-route checks'
    singular = abs(Gp - GV) < 1e-12 * GV
    if not singular:
        hi = pm_side(KV, GV, GR, terms, Gp)
        assert _ok(hi), 'upper-bound evaluation failed cross-route checks'
        return lo, dict(hi), dict(singular=False, dstar=None, excluded_sliver=None,
                                  dsens_mu_x3=None)
    d_adm = max(0.0, (GR - GV) / GV)
    d_lo = max(d_adm * 1.5, 1e-9)
    grid = loggrid(d_lo, 10.0, 601)
    best = None
    for df in grid:
        r = pm_side(KV, GV, GR, terms, GV * (1.0 + df))
        if r is None or r['mu'] < lo['mu'] - 1e-9 * abs(lo['mu']):
            continue
        if best is None or r['mu'] < best[1]['mu']:
            best = (df, r)
    assert best is not None, 'no admissible delta found'
    i = grid.index(best[0])
    a = math.log10(grid[max(0, i - 1)])
    b = math.log10(grid[min(len(grid) - 1, i + 1)])

    def f_mu(ld):
        r = pm_side(KV, GV, GR, terms, GV * (1.0 + 10.0 ** ld))
        return r['mu'] if (r is not None and r['mu'] >= lo['mu'] - 1e-9 * abs(lo['mu'])) \
            else float('inf')
    ld_star = golden_min(f_mu, a, b)
    dstar = 10.0 ** ld_star
    hi = pm_side(KV, GV, GR, terms, GV * (1.0 + dstar))
    assert _ok(hi)
    # K_PM upper minimized over the same admissible family (separate minimizer)
    kbest = None
    for df in grid:
        r = pm_side(KV, GV, GR, terms, GV * (1.0 + df))
        if r is None:
            continue
        if kbest is None or r['K_PM'] < kbest:
            kbest = r['K_PM']
    out = dict(hi)
    out['K_PM'] = min(kbest, hi['K_PM'])
    sens = []
    for df in (dstar / 3.0, dstar * 3.0):
        if df > d_adm:
            r = pm_side(KV, GV, GR, terms, GV * (1.0 + df))
            if r is not None:
                sens.append(r['mu'] - hi['mu'])
    return lo, out, dict(singular=True, dstar=dstar,
                         excluded_sliver=(d_adm if d_adm > 0.0 else None),
                         dsens_mu_x3=sens)

# ---- branch builders ----------------------------------------------------------------
def hs_hex(c11, c12, c13, c33, c44, c66):
    KV = (2.0 * (c11 + c12) + 4.0 * c13 + c33) / 9.0               # (20)
    GV = (c11 + c33 - 2.0 * c13 - c66) / 3.0                       # (22)
    KR = c13 + 1.0 / (1.0 / (c11 - c66 - c13) + 1.0 / (c33 - c13)) # (23)
    GR = KR * GV / KV                                              # formal definition
    om = c33 * (c11 - c66) - c13 * c13
    prod = abs(3.0 * KR * GV - om) / abs(om)                       # product identity
    muV = (GV + 2.0 * c44 + 2.0 * c66) / 5.0                       # (21)
    muR = 5.0 / (1.0 / GR + 2.0 / c44 + 2.0 / c66)                 # (24)
    terms = [(2.0, c44), (2.0, c66)]
    lo, hi, meta = bounds(KV, GV, GR, terms,
                          min(c44, GR, c66),                       # (45) Watt-Peselnick
                          max(c44, GV, c66))                       # (48)
    return dict(branch='hex', KV=KV, KR=KR, GVeff=GV, GReff=GR, muV=muV, muR=muR,
                product_resid=prod, lo=lo, hi=hi, **meta)

def hs_tet(c11, c12, c13, c33, c44, c66):
    KV = (2.0 * (c11 + c12) + 4.0 * c13 + c33) / 9.0               # (20)
    GV = (c11 + c12 - 4.0 * c13 + 2.0 * c33) / 6.0                 # (32)
    KR = c13 + 1.0 / (2.0 / (c11 + c12 - 2.0 * c13) + 1.0 / (c33 - c13))  # (33)
    om = (c11 + c12) * c33 - 2.0 * c13 * c13
    GR = om / (6.0 * KV)                                           # (35)
    mu3 = (c11 - c12) / 2.0
    prod = abs(3.0 * KR * GV - om / 2.0) / abs(om / 2.0)
    assert prod < 1e-10, 'tetragonal product identity broken: {}'.format(prod)
    muV = (GV + mu3 + 2.0 * c44 + c66) / 5.0                       # (31)
    muR = 5.0 / (1.0 / GR + 1.0 / mu3 + 2.0 / c44 + 1.0 / c66)     # (34)
    terms = [(1.0, mu3), (2.0, c44), (1.0, c66)]
    lo, hi, meta = bounds(KV, GV, GR, terms,
                          min(c44, mu3, GR, c66),                  # (47)
                          max(c44, mu3, GV, c66))                  # (50)
    return dict(branch='tet', KV=KV, KR=KR, GVeff=GV, GReff=GR, mu3=mu3, muV=muV,
                muR=muR, product_resid=prod, lo=lo, hi=hi, **meta)

def family_containment(builder_is_hex, c, table_hi):
    """min over the admissible delta family of |mu(delta) - table value|."""
    c11, c12, c13, c33, c44, c66 = c
    KV = (2.0 * (c11 + c12) + 4.0 * c13 + c33) / 9.0
    if builder_is_hex:
        GV = (c11 + c33 - 2.0 * c13 - c66) / 3.0
        KR = c13 + 1.0 / (1.0 / (c11 - c66 - c13) + 1.0 / (c33 - c13))
        GR = KR * GV / KV
        terms = [(2.0, c44), (2.0, c66)]
    else:
        GV = (c11 + c12 - 4.0 * c13 + 2.0 * c33) / 6.0
        KR = c13 + 1.0 / (2.0 / (c11 + c12 - 2.0 * c13) + 1.0 / (c33 - c13))
        GR = ((c11 + c12) * c33 - 2.0 * c13 * c13) / (6.0 * KV)
        terms = [(1.0, (c11 - c12) / 2.0), (2.0, c44), (1.0, c66)]
    d_adm = max(0.0, (GR - GV) / GV)
    best = float('inf')
    for df in loggrid(max(d_adm * 1.5, 1e-9), 10.0, 601):
        r = pm_side(KV, GV, GR, terms, GV * (1.0 + df))
        if r is not None:
            best = min(best, abs(r['mu'] - table_hi))
    return best

# ---- controls (Addendum 1 Tables 1-2 hex; Addendum 2 Tables 5-6 tetragonal) ---------
# Spec (H-10 respecified): lower delta-free within +/-0.1 (0.2 for the extreme
# graphite row); non-singular upper within 0.2; singular upper: validity direction
# (mine <= table + 0.1) AND family containment <= 0.15.
CONTROLS = {
 'Co (hex)':     (True,  (295.0, 159.0, 111.0, 335.0, 71.0, (295.0 - 159.0) / 2.0), 76.6, 77.0),
 'Mg (hex)':     (True,  (59.3, 25.7, 21.4, 61.5, 16.4, (59.3 - 25.7) / 2.0), 17.3, 17.3),
 'GraphB (hex)': (True,  (1060.0, 180.0, 15.0, 36.5, 4.0, (1060.0 - 180.0) / 2.0), 14.8, 148.9),
 'TiO2 (tet)':   (False, (270.0, 176.0, 147.0, 480.0, 124.0, 193.0), 110.0, 117.0),
 'Sn (tet)':     (False, (73.2, 59.8, 39.1, 90.6, 21.9, 23.8), 17.7, 19.0),
}
print('\n== CONTROLS (five rows, both branches, both singular classes) ==')
ctrl_out = {}
for name, (ishex, c, tlo, thi) in CONTROLS.items():
    r = (hs_hex if ishex else hs_tet)(*c)
    lo, hi = r['lo']['mu'], r['hi']['mu']
    tol_lo = 0.2 if 'Graph' in name else 0.1
    ok_lo = abs(lo - tlo) <= tol_lo
    if r['singular']:
        cont = family_containment(ishex, c, thi)
        ok_hi = (hi <= thi + 0.1) and cont <= 0.15
    else:
        cont = abs(hi - thi)
        ok_hi = cont <= 0.2
    ok = ok_lo and ok_hi
    print('{:14s} mu-HS = [{:.4f}, {:.4f}]  table [{}, {}]  singular {}  '
          'containment {:.4f}  -> {}'.format(name, lo, hi, tlo, thi, r['singular'],
                                             cont, 'PASS' if ok else 'FAIL'))
    assert ok, 'control failed: ' + name
    ctrl_out[name] = dict(mu=[lo, hi], table=[tlo, thi], singular=r['singular'],
                          containment=cont, dstar=r.get('dstar'))

# ---- framework tensors: tetragonal-primary + hex projection -------------------------
print('\n== FRAMEWORK TENSORS: tetragonal-primary (identity-exact) + hex checks ==')
res = {}
for cfg in ('hex:step', 'hex:gem8'):
    p = D['vrh'][cfg]['C_over_rho']
    c = (p['C11'], p['C12'], p['C13'], p['C33'], p['C44'], p['C66'])
    T = hs_tet(*c)
    Hm = hs_hex(*c)                                   # measured-C66 hex, guarded
    Hp = hs_hex(p['C11'], p['C12'], p['C13'], p['C33'], p['C44'],
                (p['C11'] - p['C12']) / 2.0)          # exact-hex projection
    mu_lo, mu_hi = T['lo']['mu'], T['hi']['mu']
    assert mu_hi > mu_lo, 'band inverted'
    vlo, vhi = math.sqrt(mu_lo), math.sqrt(mu_hi)
    vR, vV = math.sqrt(T['muR']), math.sqrt(T['muV'])
    hw = 100.0 * (vhi - vlo) / (vhi + vlo)
    hwvr = 100.0 * (vV - vR) / (vV + vR)
    print('{:9s} TET  mu_HS = [{:.6f}, {:.6f}]  (VR [{:.6f}, {:.6f}])'.format(
        cfg, mu_lo, mu_hi, T['muR'], T['muV']))
    print('          v_T = [{:.4f}, {:.4f}]  half-width {:.2f}% (VR {:.2f}%)  '
          'tightening x{:.1f}'.format(vlo, vhi, hw, hwvr, hwvr / hw))
    print('          K_PM = [{:.4f}, {:.4f}]  singular {}  dstar {}  sliver {}  '
          'prod-resid {:.1e}'.format(T['lo']['K_PM'], T['hi']['K_PM'], T['singular'],
                                     T.get('dstar'), T.get('excluded_sliver'),
                                     T['product_resid']))
    print('          HEX(measured, guarded): [{:.6f}, {:.6f}]  sliver {}'.format(
        Hm['lo']['mu'], Hm['hi']['mu'], Hm.get('excluded_sliver')))
    print('          HEX(exact-hex proj):    [{:.6f}, {:.6f}]'.format(
        Hp['lo']['mu'], Hp['hi']['mu']))
    res[cfg] = dict(
        tet_primary=dict(mu_lo=mu_lo, mu_hi=mu_hi, vT_lo=vlo, vT_hi=vhi,
                         halfwidth_pct=hw, VR=[T['muR'], T['muV']],
                         VR_halfwidth_pct=hwvr,
                         K_PM=[T['lo']['K_PM'], T['hi']['K_PM']],
                         singular=T['singular'], dstar=T.get('dstar'),
                         excluded_sliver=T.get('excluded_sliver'),
                         dsens_mu_x3=T.get('dsens_mu_x3'),
                         product_resid=T['product_resid']),
        hex_measured_guarded=dict(mu_lo=Hm['lo']['mu'], mu_hi=Hm['hi']['mu'],
                                  excluded_sliver=Hm.get('excluded_sliver')),
        hex_exact_projection=dict(mu_lo=Hp['lo']['mu'], mu_hi=Hp['hi']['mu']))

ck = dict(
    gate='G-POLY1',
    item='hex G_HS completion — CC-leg independent confirmation (rides the Phase 3 '
         'dispatch, S2(g))',
    addenda=dict(A1='57dfd40e5f0dbb311a64b30a67a47df6',
                 A2='3d419b8f7196efd895fc5079df8760b4'),
    source='UCRL-JRNL-206669 (JMPS 53, 2141 (2005)) as transcribed verbatim in the '
           'two PIN addenda (CC leg computes from the pins, not from a re-retrieval)',
    input_md5='200e7a8b775577564369c6924d38a84c',
    convention='TETRAGONAL branch primary (identity-exact, c66 free); hex branch = '
               'exact-hex projection + guarded continuity check; singular uppers '
               'minimized over the ADMISSIBLE delta family (K+>0), grid + '
               'golden-section refinement (CC method note: refined, not '
               'grid-quantized); lowers delta-free',
    method_note='pure-python instrument; 601-point log grid on delta in '
                '[max(1.5*sliver,1e-9), 10] + golden-section refinement; cross-route '
                'asserts (2),(36)/(6),(37)+(39)/(43) vs (11)/(13) at <=1e-9',
    honesty='H-10 and H-11 stand as banked (chat-leg events, acknowledged); CC leg '
            'adds none',
    controls=ctrl_out, results=res)
open(CKPATH, 'w').write(json.dumps(ck, indent=1, default=float))
b = open(CKPATH, 'rb').read()
hits = [t for t in T1 if t.lower().encode() in b.lower()]
print('\nT1 scan (CC G_HS checkpoint): {}'.format('0 hits' if not hits else
                                                  'ADJUDICATE: ' + str(hits)))
print('checkpoint (hashed BEFORE consulting the chat G_HS checkpoint):')
print('  {}  md5 {}  ({} B)'.format(CKPATH, hashlib.md5(b).hexdigest(), len(b)))
