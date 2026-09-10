#!/usr/bin/env python3
# g_poly1_hexghs_chatleg_v3.py — hex G_HS bands, tetragonal-primary per PIN ADDENDA 1+2
# Addendum 1 md5 57dfd40e5f0dbb311a64b30a67a47df6; Addendum 2 md5 3d419b8f7196efd895fc5079df8760b4.
# Chat leg only; CC confirmation rides the Phase-3 dispatch.
import json, hashlib
import numpy as np

FORBIDDEN = ['Mpc','Gpc','LIGO','170817','299792458','SME']
EXTRA = [chr(51)+'.'+'19', '0.0'+'19']
src = open(__file__, encoding='utf-8').read()
body = src.split('# T1-END')[1]
for f in FORBIDDEN + EXTRA:
    assert f not in body, f'T1 HIT (source): {f}'
print('T1 self-grep (instrument source): PASS')
# T1-END

raw = open('/mnt/user-data/outputs/poly_vrh_results.json','rb').read()
assert hashlib.md5(raw).hexdigest() == '200e7a8b775577564369c6924d38a84c'
D = json.loads(raw)

def _pm_side(KV, GVeff, GReff, c_terms, G):
    """Shared (36)-(44)+(6) machinery. c_terms = [(coef, modulus), ...] for the
    non-first bracket terms of (11)/(13). Returns (mu, K_PM, diagnostics)."""
    K = KV*(GReff - G)/(GVeff - G)                                 # (44)
    if K <= 0:
        return None
    al = -1.0/(K + 4.0*G/3.0)                                      # (38)
    be = 2.0*al/15.0 - 1.0/(5.0*G)
    ze = (G/6.0)*(9.0*K + 8.0*G)/(K + 2.0*G)                       # (3)
    id2 = abs(1.0 + 2.0*be*G + 2.0*be*ze)/abs(2.0*be*ze)           # (2)
    rhs = (1.0 - al*(KV - K)) / (GVeff + ze + (al/(2.0*be))*(KV - K))
    for coef, m in c_terms:
        rhs += coef/(m + ze)
    rhs /= 5.0                                                     # (11)/(13)
    mu_a = 1.0/rhs - ze
    D_ = 1.0 - 2.0*be*(GVeff - G) - al*(KV - K)                    # (41)
    B2 = (GVeff - G)/D_
    for coef, m in c_terms:
        B2 += coef*(m - G)/(1.0 - 2.0*be*(m - G))
    B2 /= 5.0                                                      # (39)/(43)
    mu_b = G + B2/(1.0 + 2.0*be*B2)                                # (37)
    route = abs(mu_b - mu_a)/abs(mu_a)
    K6 = KV*(GReff + ze)/(GVeff + ze)                              # (6)
    K36 = K + (KV - K)/(1.0 + 2.0*be*(G - GVeff))                  # (36)
    kroute = abs(K6 - K36)/abs(K6)
    return dict(mu=mu_a, K_PM=K6, K_comp=K, zeta=ze, id2=id2,
                mu_route=route, K_route=kroute)

def _bounds(KV, GVeff, GReff, c_terms, Gm, Gp_raw, hard=True):
    """Lower at Gm (delta-free); upper minimized over the ADMISSIBLE delta family
    when singular (G+_raw == GVeff), else at Gp_raw."""
    lo = _pm_side(KV, GVeff, GReff, c_terms, Gm)
    assert lo and lo['id2'] < 1e-10 and lo['mu_route'] < 1e-9 and lo['K_route'] < 1e-9
    singular = abs(Gp_raw - GVeff) < 1e-12*GVeff
    if not singular:
        hi = _pm_side(KV, GVeff, GReff, c_terms, Gp_raw)
        assert hi and hi['id2'] < 1e-10 and hi['mu_route'] < 1e-9 and hi['K_route'] < 1e-9
        return lo, hi, dict(singular=False, dstar=None, excluded_sliver=None)
    # admissible delta family: K+ > 0  <=>  G+ > GReff when GReff > GVeff
    d_adm = max(0.0, (GReff - GVeff)/GVeff)
    grid = np.logspace(np.log10(max(d_adm*1.5, 1e-9)), 1, 241)
    mus, kps, ok = [], [], []
    for df in grid:
        r = _pm_side(KV, GVeff, GReff, c_terms, GVeff*(1.0 + df))
        if r is None or r['mu'] <= lo['mu'] - 1e-9*abs(lo['mu']):
            mus.append(np.inf); kps.append(np.inf); ok.append(False)
        else:
            mus.append(r['mu']); kps.append(r['K_PM']); ok.append(True)
    mus = np.array(mus); kps = np.array(kps)
    assert np.isfinite(mus).any(), 'no admissible delta found'
    imu, ikp = int(np.nanargmin(mus)), int(np.nanargmin(kps))
    hi = _pm_side(KV, GVeff, GReff, c_terms, GVeff*(1.0 + grid[imu]))
    hk = _pm_side(KV, GVeff, GReff, c_terms, GVeff*(1.0 + grid[ikp]))
    assert hi['id2'] < 1e-10 and hi['mu_route'] < 1e-9
    out = dict(hi); out['K_PM'] = hk['K_PM']
    sens = []
    for f in (grid[imu]/3, grid[imu]*3):
        if f > d_adm:
            r = _pm_side(KV, GVeff, GReff, c_terms, GVeff*(1.0 + f))
            if r: sens.append(r['mu'] - out['mu'])
    return lo, out, dict(singular=True, dstar=float(grid[imu]),
                         excluded_sliver=(float(d_adm) if d_adm > 0 else None),
                         dsens_mu_x3=sens)

def hs_hex(c11, c12, c13, c33, c44, c66):
    KV = (2*(c11+c12) + 4*c13 + c33)/9.0                           # (20)
    GVeff = (c11 + c33 - 2*c13 - c66)/3.0                          # (22)
    KR = c13 + 1.0/(1.0/(c11 - c66 - c13) + 1.0/(c33 - c13))       # (23)
    GReff = KR*GVeff/KV                                            # formal definition
    prod = abs(3*KR*GVeff - (c33*(c11-c66) - c13*c13))/abs(c33*(c11-c66) - c13*c13)
    muV = (GVeff + 2*c44 + 2*c66)/5.0                              # (21)
    muR = 5.0/(1.0/GReff + 2.0/c44 + 2.0/c66)                      # (24)
    lo, hi, meta = _bounds(KV, GVeff, GReff, [(2.0, c44), (2.0, c66)],
                           min(c44, GReff, c66), max(c44, GVeff, c66))
    return dict(branch='hex', KV=KV, KR=KR, GVeff=GVeff, GReff=GReff,
                muV=muV, muR=muR, product_resid=prod, lo=lo, hi=hi, **meta)

def hs_tet(c11, c12, c13, c33, c44, c66):
    KV = (2*(c11+c12) + 4*c13 + c33)/9.0                           # (20)
    GVeff = (c11 + c12 - 4*c13 + 2*c33)/6.0                        # (32)
    KR = c13 + 1.0/(2.0/(c11 + c12 - 2*c13) + 1.0/(c33 - c13))     # (33)
    om = (c11 + c12)*c33 - 2*c13*c13
    GReff = om/(6.0*KV)                                            # (35)
    mu3 = (c11 - c12)/2.0
    prod = abs(3*KR*GVeff - om/2.0)/abs(om/2.0)                    # exact algebra
    assert prod < 1e-10, f'tetragonal product identity fails: {prod}'
    muV = (GVeff + mu3 + 2*c44 + c66)/5.0                          # (31)
    muR = 5.0/(1.0/GReff + 1.0/mu3 + 2.0/c44 + 1.0/c66)            # (34)
    lo, hi, meta = _bounds(KV, GVeff, GReff,
                           [(1.0, mu3), (2.0, c44), (1.0, c66)],
                           min(c44, mu3, GReff, c66), max(c44, mu3, GVeff, c66))
    return dict(branch='tet', KV=KV, KR=KR, GVeff=GVeff, GReff=GReff, mu3=mu3,
                muV=muV, muR=muR, product_resid=prod, lo=lo, hi=hi, **meta)

# ---------------- controls -----------------------------------------------------------
# Hex (Addendum 1, Tables 1-2): Co (singular), Mg (singular), Graphite B (non-singular).
# Tetragonal (Addendum 2, Tables 5-6): TiO2 (non-singular), Sn (singular).
# Spec (H-10 respecified): lower delta-free +/-0.1 (0.2 extreme); non-singular upper
# direct; singular upper: validity mine <= table + 0.1 AND family containment <= 0.15.
def fam_contain(fn, c, table_hi):
    best = 1e9
    for df in np.logspace(-8, 1, 181):
        # containment probes the unconstrained-but-admissible family
        r = fn(*c)  # bounds recomputed; cheap enough to probe via _pm_side directly
        break
    return None  # containment handled inline below via direct family probe

def probe_family(builder, c, table_hi):
    # rebuild the family for containment: use branch internals
    if builder is hs_hex:
        c11,c12,c13,c33,c44,c66 = c
        KV=(2*(c11+c12)+4*c13+c33)/9.0; GV=(c11+c33-2*c13-c66)/3.0
        KR=c13+1.0/(1.0/(c11-c66-c13)+1.0/(c33-c13)); GR=KR*GV/KV
        terms=[(2.0,c44),(2.0,c66)]
    else:
        c11,c12,c13,c33,c44,c66 = c
        KV=(2*(c11+c12)+4*c13+c33)/9.0; GV=(c11+c12-4*c13+2*c33)/6.0
        KR=c13+1.0/(2.0/(c11+c12-2*c13)+1.0/(c33-c13)); GR=((c11+c12)*c33-2*c13*c13)/(6.0*KV)
        terms=[(1.0,(c11-c12)/2.0),(2.0,c44),(1.0,c66)]
    best=1e9
    d_adm = max(0.0,(GR-GV)/GV)
    for df in np.logspace(np.log10(max(d_adm*1.5,1e-9)),1,181):
        r=_pm_side(KV,GV,GR,terms,GV*(1.0+df))
        if r: best=min(best,abs(r['mu']-table_hi))
    return best

ctrl = {
 'Co (hex)':       (hs_hex, (295.,159.,111.,335.,71.,(295.-159.)/2), 76.6, 77.0),
 'Mg (hex)':       (hs_hex, (59.3,25.7,21.4,61.5,16.4,(59.3-25.7)/2), 17.3, 17.3),
 'GraphB (hex)':   (hs_hex, (1060.,180.,15.0,36.5,4.0,(1060.-180.)/2), 14.8, 148.9),
 'TiO2 (tet)':     (hs_tet, (270.,176.,147.,480.,124.,193.), 110.0, 117.0),
 'Sn (tet)':       (hs_tet, (73.2,59.8,39.1,90.6,21.9,23.8), 17.7, 19.0),
}
print('\n== CONTROLS ==')
ctrl_out = {}
for name, (fn, c, tlo, thi) in ctrl.items():
    r = fn(*c)
    lo, hi = r['lo']['mu'], r['hi']['mu']
    tol_lo = 0.2 if 'Graph' in name else 0.1
    ok_lo = abs(lo - tlo) <= tol_lo
    if r['singular']:
        cont = probe_family(fn, c, thi)
        ok_hi = (hi <= thi + 0.1) and cont <= 0.15
    else:
        cont = abs(hi - thi); ok_hi = cont <= 0.2
    ok = ok_lo and ok_hi
    print(f"{name:14s} mu-HS = [{lo:.3f}, {hi:.3f}]  table [{tlo}, {thi}]  "
          f"singular {r['singular']}  containment {cont:.3f}  -> {'PASS' if ok else 'FAIL'}")
    assert ok, f'control {name}'
    ctrl_out[name] = dict(mu=[lo, hi], table=[tlo, thi], singular=r['singular'],
                          containment=cont, dstar=r.get('dstar'))

# ---------------- framework tensors --------------------------------------------------
print('\n== FRAMEWORK TENSORS: tetragonal-primary (identity-exact) + hex projection ==')
res = {}
for cfg in ('hex:step', 'hex:gem8'):
    p = D['vrh'][cfg]['C_over_rho']
    c = (p['C11'], p['C12'], p['C13'], p['C33'], p['C44'], p['C66'])
    T = hs_tet(*c)
    Hm = hs_hex(*c)  # measured-C66 hex branch, admissibility-guarded (continuity check)
    c66p = (p['C11'] - p['C12'])/2.0
    Hp = hs_hex(p['C11'], p['C12'], p['C13'], p['C33'], p['C44'], c66p)
    mu_lo, mu_hi = T['lo']['mu'], T['hi']['mu']
    assert mu_hi > mu_lo, 'band order'
    vlo, vhi = mu_lo**0.5, mu_hi**0.5
    vR, vV = T['muR']**0.5, T['muV']**0.5
    hw = 100.0*(vhi - vlo)/(vhi + vlo)
    hwvr = 100.0*(vV - vR)/(vV + vR)
    print(f"{cfg:9s} TET  mu_HS = [{mu_lo:.6f}, {mu_hi:.6f}]  (VR [{T['muR']:.6f}, {T['muV']:.6f}])")
    print(f"          v_T = [{vlo:.4f}, {vhi:.4f}]  half-width {hw:.2f}% (VR {hwvr:.2f}%)  tightening x{hwvr/hw:.1f}")
    print(f"          K_PM = [{T['lo']['K_PM']:.4f}, {T['hi']['K_PM']:.4f}]  singular {T['singular']}  "
          f"dstar {T.get('dstar')}  sliver {T.get('excluded_sliver')}  prod-resid {T['product_resid']:.1e}")
    print(f"          HEX(measured, guarded): [{Hm['lo']['mu']:.6f}, {Hm['hi']['mu']:.6f}]  sliver {Hm.get('excluded_sliver')}")
    print(f"          HEX(exact-hex proj):    [{Hp['lo']['mu']:.6f}, {Hp['hi']['mu']:.6f}]")
    res[cfg] = dict(
        tet_primary=dict(mu_lo=mu_lo, mu_hi=mu_hi, vT_lo=vlo, vT_hi=vhi,
                         halfwidth_pct=hw, VR=[T['muR'], T['muV']], VR_halfwidth_pct=hwvr,
                         K_PM=[T['lo']['K_PM'], T['hi']['K_PM']], singular=T['singular'],
                         dstar=T.get('dstar'), excluded_sliver=T.get('excluded_sliver'),
                         dsens_mu_x3=T.get('dsens_mu_x3'), product_resid=T['product_resid']),
        hex_measured_guarded=dict(mu_lo=Hm['lo']['mu'], mu_hi=Hm['hi']['mu'],
                                  excluded_sliver=Hm.get('excluded_sliver')),
        hex_exact_projection=dict(mu_lo=Hp['lo']['mu'], mu_hi=Hp['hi']['mu']))

ck = dict(gate='G-POLY1',
          item='hex G_HS completion (chat leg; CC confirmation rides Phase 3 dispatch)',
          addenda=dict(A1='57dfd40e5f0dbb311a64b30a67a47df6', A2='3d419b8f7196efd895fc5079df8760b4'),
          source='UCRL-JRNL-206669 (JMPS 53, 2141 (2005)) via OSTI servlets/purl/875664',
          input_md5='200e7a8b775577564369c6924d38a84c',
          convention=('TETRAGONAL branch primary (identity-exact for the measured tensors, c66 free); '
                      'hex branch = exact-hex projection + guarded continuity check; singular-case '
                      'uppers minimized over the ADMISSIBLE delta family (K+>0); lowers delta-free'),
          honesty=dict(
            H10=('first Co control spec (fixed small delta, +/-0.1 both bounds) mis-specified against '
                 'the delta-dependent published upper; family scan showed a non-monotone family with an '
                 'interior minimum below the table point; control respecified to validity-direction + '
                 'containment; no outputs consumed'),
            H11=('v2 hex-branch minimized family produced an INVERTED band on hex:step: the C66-identity '
                 'residual direction there gives KR(23)>KV, hence GReff>GVeff, opening a K+<0 inadmissible '
                 'sliver that the unguarded minimizer entered; fixed by (a) admissibility guard K+>0 and '
                 '(b) adopting the tetragonal branch (same source, Addendum 2) as the identity-exact '
                 'primary, under which KR(33)<KV and the product identity is exact; no outputs consumed')),
          controls=ctrl_out, results=res)
out = '/mnt/user-data/outputs/poly1_hexghs_chat.json'
open(out, 'w').write(json.dumps(ck, indent=1, default=float))
b = open(out, 'rb').read()
hits = [f for f in FORBIDDEN + EXTRA if f.encode() in b]
print(f"\nT1 scan (checkpoint): {'0 hits' if not hits else 'ADJUDICATE: ' + str(hits)}")
print(f"checkpoint: {out}  md5 {hashlib.md5(b).hexdigest()}  ({len(b)} B)")
