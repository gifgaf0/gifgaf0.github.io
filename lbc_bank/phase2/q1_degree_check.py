#!/usr/bin/env python3
"""q1_degree_check.py - Phase 2, question 1 (exploration mode; no gate, no fold).

Question: in the standard two-component knot-soliton class (two complex fields z1, z2 with the normalized pair
n = (z1, z2)/|(z1, z2)| on S^3; the BEC-Skyrme / Skyrme-Faddeev class), does the conserved topological charge
(the S^3 degree = Skyrme baryon number B) see Borromean linking of three vortex loops of ONE component?

Method (two independent routes per configuration):
  1. Degree integral  B = (1/2 pi^2) Int det[Z, dZ/dx, dZ/dy, dZ/dz] / |Z|^4 d^3x   (Z = (Re z1, Im z1, Re z2, Im z2)),
     with analytic derivatives, midpoint rule on a cell-centred grid over [-L, L]^3, processed in z-slabs.
     (det[n, dn...] = det[Z, dZ...]/|Z|^4 because the radial part of dn is parallel to n.)
  2. Gauss linking integrals of the explicit zero curves, oriented as zero sets (tangent along grad Re f x grad Im f).
Expectation files (written before computing): Q1_EXPECTATION_pre_compute.md, Q1_EXPECTATION_ADDENDUM_pre_compute.md.

Configurations (z1 zero set | z2 zero set):
  a   identity map (inverse stereographic projection): z-axis | unit circle                           expect |B| = 1 minus box tail
  a1  ring A alone | loop D1 linking A once                                                              expect |B| = 1 (sign s0)
  b   Borromean rings A, B, C | none (z2 nowhere zero)                                                   expect B = 0
  c   Borromean rings A, B, C | loop D1 linking A only                                                   expect B = s0
  d   Borromean rings A, B, C | loop D' linking none                                                     expect B = 0
  e   three UNLINKED rings (same shapes, B and C moved apart) | loop D1 linking A only                   expect B = s0 (= c)
  f   Borromean rings A, B, C | loops D1, D2, D3, one linking each ring (C3-symmetric)                  expect B = 3 s0
Usage: python3 q1_degree_check.py [N ...]   (default N = 128 192)
"""
import json, sys, time, hashlib
import numpy as np

AE, BE, KE = 2.0, 1.0, 1.0      # Borromean ellipses: long semi-axis a, short semi-axis b, imaginary slope k
RD = 0.5                         # radius of the z2 loops
ELL = 0.25                       # z1 amplitude is set per configuration so that, at the point where ring A pierces the
                                 # disk of loop D1, |z2| / |grad z1| = ELL (topologically irrelevant; keeps the integrand
                                 # resolved: with a fixed amplitude the peak there is ~0.05 wide and under-resolved)
WG = 2.5                         # Gaussian damping width on z1 (makes n -> (0, 1) at infinity fast)
L = 6.5                          # half-width of the integration box


# ---------- factors: each returns (f, [df/dx, df/dy, df/dz]) ----------
def ellipse(kind, c=(0.0, 0.0, 0.0)):
    """kind A: in the plane z=cz, long along x; B: plane x=cx, long along y; C: plane y=cy, long along z (cyclic)."""
    def fn(X, Y, Z):
        u, v, w = X - c[0], Y - c[1], Z - c[2]
        one = np.ones_like(u)
        if kind == "A":
            f = u**2 / AE**2 + v**2 / BE**2 - 1 + 1j * KE * w
            g = [2 * u / AE**2 + 0j, 2 * v / BE**2 + 0j, 1j * KE * one]
        elif kind == "B":
            f = v**2 / AE**2 + w**2 / BE**2 - 1 + 1j * KE * u
            g = [1j * KE * one, 2 * v / AE**2 + 0j, 2 * w / BE**2 + 0j]
        else:
            f = w**2 / AE**2 + u**2 / BE**2 - 1 + 1j * KE * v
            g = [2 * u / BE**2 + 0j, 1j * KE * one, 2 * w / AE**2 + 0j]
        return f, g
    return fn


def circle(c, nrm, R=RD):
    """f = |p|^2 - R^2 + 2iR p.n  (p = x - c): zero set = circle of radius R about c in the plane normal to n."""
    c = np.asarray(c, float); nrm = np.asarray(nrm, float); nrm = nrm / np.linalg.norm(nrm)
    def fn(X, Y, Z):
        p = [X - c[0], Y - c[1], Z - c[2]]
        pn = p[0] * nrm[0] + p[1] * nrm[1] + p[2] * nrm[2]
        f = p[0]**2 + p[1]**2 + p[2]**2 - R**2 + 2j * R * pn
        g = [2 * p[i] + 2j * R * nrm[i] for i in range(3)]
        return f, g
    return fn


def poly_id1(X, Y, Z):           # 2x + 2iy
    one = np.ones_like(X)
    return 2 * X + 2j * Y, [2 * one + 0j, 2j * one, 0j * one]


def poly_id2(X, Y, Z):           # 2z + i(r^2 - 1)
    one = np.ones_like(X)
    return 2 * Z + 1j * (X**2 + Y**2 + Z**2 - 1), [2j * X, 2j * Y, 2 * one + 2j * Z]


def poly_nozero(X, Y, Z):        # 1 + r^2 + 2iz : real part >= 1, never zero
    return 1 + X**2 + Y**2 + Z**2 + 2j * Z, [2 * X + 0j, 2 * Y + 0j, 2 * Z + 2j]


def product(factors, X, Y, Z):
    vals = [fn(X, Y, Z) for fn in factors]
    F = np.ones_like(X, dtype=complex)
    for f, _ in vals:
        F = F * f
    G = [np.zeros_like(X, dtype=complex) for _ in range(3)]
    for i, (fi, gi) in enumerate(vals):
        rest = np.ones_like(X, dtype=complex)
        for j, (fj, _) in enumerate(vals):
            if j != i:
                rest = rest * fj
        for a in range(3):
            G[a] = G[a] + gi[a] * rest
    return F, G


def field(spec, X, Y, Z):
    """spec = dict(factors=[...], amp=float, m=int, gauss=width or None): z = amp * prod(factors) * (1+r^2)^-m * exp(-r^2/w^2)."""
    F, G = product(spec["factors"], X, Y, Z)
    r2 = X**2 + Y**2 + Z**2
    W = spec.get("amp", 1.0) * (1 + r2) ** (-spec["m"])
    dlogW = [-2 * spec["m"] * q / (1 + r2) for q in (X, Y, Z)]
    if spec.get("gauss"):
        W = W * np.exp(-r2 / spec["gauss"]**2)
        dlogW = [dlogW[i] - 2 * q / spec["gauss"]**2 for i, q in enumerate((X, Y, Z))]
    return F * W, [G[a] * W + F * W * dlogW[a] for a in range(3)]


def degree(z1spec, z2spec, N, Lbox=L, nslab=8, want_pointwise_identity=False):
    h = 2 * Lbox / N
    xs = -Lbox + (np.arange(N) + 0.5) * h
    total, maxdev = 0.0, 0.0
    absint = 0.0
    for k0 in range(0, N, nslab):
        X, Y, Zc = np.meshgrid(xs, xs, xs[k0:k0 + nslab], indexing="ij")
        a, ga = field(z1spec, X, Y, Zc)
        b, gb = field(z2spec, X, Y, Zc)
        M = np.empty(X.shape + (4, 4))
        for j, (u, v) in enumerate([(a, b)] + [(ga[i], gb[i]) for i in range(3)]):
            M[..., 0, j], M[..., 1, j], M[..., 2, j], M[..., 3, j] = u.real, u.imag, v.real, v.imag
        dens = np.linalg.det(M) / (np.abs(a)**2 + np.abs(b)**2) ** 2
        total += dens.sum()
        absint += np.abs(dens).sum()
        if want_pointwise_identity:
            ref = 8.0 / (1 + X**2 + Y**2 + Zc**2) ** 3
            maxdev = max(maxdev, float(np.max(np.abs(np.abs(dens) - ref) / ref)))
    out = {"B": float(total * h**3 / (2 * np.pi**2)), "abs_integral": float(absint * h**3 / (2 * np.pi**2)), "h": h}
    if want_pointwise_identity:
        out["pointwise_max_rel_dev_vs_8_over_(1+r2)^3"] = maxdev
    return out


# ---------- explicit zero curves for the Gauss linking integrals ----------
def curve_ellipse(kind, c=(0.0, 0.0, 0.0), M=800):
    t = 2 * np.pi * np.arange(M) / M
    c = np.asarray(c, float)
    if kind == "A":
        P = np.stack([AE * np.cos(t), BE * np.sin(t), 0 * t], 1)
    elif kind == "B":
        P = np.stack([0 * t, AE * np.cos(t), BE * np.sin(t)], 1)
    else:
        P = np.stack([BE * np.sin(t), 0 * t, AE * np.cos(t)], 1)
    return P + c


def curve_circle(c, nrm, R=RD, M=800):
    nrm = np.asarray(nrm, float); nrm = nrm / np.linalg.norm(nrm)
    e1 = np.cross(nrm, [1.0, 0, 0]) if abs(nrm[0]) < 0.9 else np.cross(nrm, [0, 1.0, 0])
    e1 /= np.linalg.norm(e1); e2 = np.cross(nrm, e1)
    t = 2 * np.pi * np.arange(M) / M
    return np.asarray(c, float) + R * (np.outer(np.cos(t), e1) + np.outer(np.sin(t), e2))


def orient(P, fn):
    """Orient the closed polygon P as the zero set of fn: tangent along grad Re f x grad Im f. Also report max |f| on P."""
    T = np.roll(P, -1, 0) - np.roll(P, 1, 0)
    f, g = fn(P[:, 0], P[:, 1], P[:, 2])
    gr = np.stack([gi.real for gi in g], 1); gi_ = np.stack([gi.imag for gi in g], 1)
    s = np.sign(np.einsum("ij,ij->i", T, np.cross(gr, gi_)))
    assert np.all(s == s[0]), "orientation not constant along the curve"
    return (P if s[0] > 0 else P[::-1].copy()), float(np.max(np.abs(f)))


def gauss_link(P, Q):
    dP = np.roll(P, -1, 0) - P; mP = P + 0.5 * dP
    dQ = np.roll(Q, -1, 0) - Q; mQ = Q + 0.5 * dQ
    R = mP[:, None, :] - mQ[None, :, :]
    cr = np.cross(dP[:, None, :], dQ[None, :, :])
    return float(np.sum(np.einsum("ijk,ijk->ij", R, cr) / np.linalg.norm(R, axis=2) ** 3) / (4 * np.pi))


# ---------- link type of the z1 rings: Kauffman bracket of a generic planar projection ----------
def _padd(p, q, c=1):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, 0) + c * v
    return {k: v for k, v in out.items() if v != 0}


def _pmul(p, q):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            out[a + b] = out.get(a + b, 0) + x * y
    return {k: v for k, v in out.items() if v != 0}


def bracket(curves, angles=(0.37, 0.81, 0.23)):
    """Kauffman bracket <D> (polynomial in A, dict exponent -> coeff) of the projection of closed polygons onto a
    generically rotated plane. Returns (bracket, number of crossings). Convention-independent use: compare up to a
    unit +-A^k and A <-> 1/A (the rings and the unlink are amphichiral)."""
    a, b, c = angles
    Rz = lambda t: np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1]])
    Rx = lambda t: np.array([[1, 0, 0], [0, np.cos(t), -np.sin(t)], [0, np.sin(t), np.cos(t)]])
    Rm = Rz(a) @ Rx(b) @ Rz(c)
    P = [np.asarray(q) @ Rm.T for q in curves]
    segs = []                      # (component, index, start, end)
    for j, q in enumerate(P):
        for i in range(len(q)):
            segs.append((j, i, q[i], q[(i + 1) % len(q)]))
    S0 = np.array([s_[2] for s_ in segs]); S1 = np.array([s_[3] for s_ in segs])
    comp = np.array([s_[0] for s_ in segs]); idx = np.array([s_[1] for s_ in segs])
    n_by = [len(q) for q in P]
    crossings = []
    d = S1[:, :2] - S0[:, :2]
    for u in range(len(segs)):
        v = np.arange(u + 1, len(segs))
        r = S0[v, :2] - S0[u, :2]
        den = d[u, 0] * d[v, 1] - d[u, 1] * d[v, 0]
        with np.errstate(divide="ignore", invalid="ignore"):
            su = (r[:, 0] * d[v, 1] - r[:, 1] * d[v, 0]) / den
            sv = (r[:, 0] * d[u, 1] - r[:, 1] * d[u, 0]) / den
        same = comp[v] == comp[u]
        adj = same & ((np.abs(idx[v] - idx[u]) <= 1) | (np.abs(idx[v] - idx[u]) >= np.array(n_by)[comp[v]] - 1))
        hit = (np.abs(den) > 1e-14) & (su >= 0) & (su < 1) & (sv >= 0) & (sv < 1) & ~adj
        for w in v[hit]:
            k = np.where(v == w)[0][0]
            zu = S0[u, 2] + su[k] * (S1[u, 2] - S0[u, 2]); zw = S0[w, 2] + sv[k] * (S1[w, 2] - S0[w, 2])
            over, under = ((u, su[k]), (w, sv[k])) if zu > zw else ((w, sv[k]), (u, su[k]))
            crossings.append((over, under))
    # passages along each component
    passages = {j: [] for j in range(len(P))}
    for ci, (ov, un) in enumerate(crossings):
        for role, (sg, frac) in (("o", ov), ("u", un)):
            passages[comp[sg]].append((idx[sg] + frac, ci, role))
    edge_in, edge_out, ne, free = {}, {}, 0, 0
    for j in range(len(P)):
        lst = sorted(passages[j])
        if not lst:
            free += 1; continue
        m = len(lst)
        for k, (_, ci, role) in enumerate(lst):
            edge_out[(ci, role)] = ne + k
            edge_in[(ci, role)] = ne + (k - 1) % m
        ne += m
    # smoothings
    smooth = []
    for ci, (ov, un) in enumerate(crossings):
        to = d[ov[0]] / np.linalg.norm(d[ov[0]]); tu = d[un[0]] / np.linalg.norm(d[un[0]])
        ang = lambda vec: np.arctan2(vec[1], vec[0])
        base = ang(-to)
        rel = lambda vec: (ang(vec) - base) % (2 * np.pi)
        ports_u = [("u_in", -tu), ("u_out", tu)]
        p1, p3 = (ports_u[0], ports_u[1]) if rel(ports_u[0][1]) < np.pi else (ports_u[1], ports_u[0])
        E = {"o_in": edge_in[(ci, "o")], "o_out": edge_out[(ci, "o")], "u_in": edge_in[(ci, "u")], "u_out": edge_out[(ci, "u")]}
        A_pairs = [(E[p1[0]], E["o_out"]), (E[p3[0]], E["o_in"])]
        B_pairs = [(E["o_in"], E[p1[0]]), (E["o_out"], E[p3[0]])]
        smooth.append((A_pairs, B_pairs))
    dpoly = {2: -1, -2: -1}
    total = {}
    nc = len(crossings)
    for state in range(2 ** nc):
        parent = list(range(ne))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        nA = 0
        for ci in range(nc):
            isA = (state >> ci) & 1
            nA += isA
            for (x, y) in (smooth[ci][0] if isA else smooth[ci][1]):
                rx, ry = find(x), find(y)
                if rx != ry:
                    parent[rx] = ry
        loops = len({find(x) for x in range(ne)}) + free
        term = {nA - (nc - nA): 1}
        for _ in range(loops - 1):
            term = _pmul(term, dpoly)
        total = _padd(total, term)
    return total, nc


def jones_like(br):
    """Map a bracket to its coefficient sequence in steps of A^4, normalized up to unit and mirror (lexicographic min)."""
    ks = sorted(br)
    assert all((k - ks[0]) % 4 == 0 for k in ks), "bracket exponents not congruent mod 4"
    seq = [br.get(k, 0) for k in range(ks[0], ks[-1] + 1, 4)]
    cands = [seq, seq[::-1], [-x for x in seq], [-x for x in seq[::-1]]]
    return min(cands)


def main():
    Ns = [int(a) for a in sys.argv[1:]] or [128, 192]
    fA, fB, fC = ellipse("A"), ellipse("B"), ellipse("C")
    fBe, fCe = ellipse("B", (0, 0, 2.5)), ellipse("C", (0, 0, -2.5))
    D1 = ((2.0, 0, 0), (0, 1.0, 0)); D2 = ((0, 2.0, 0), (0, 0, 1.0)); D3 = ((0, 0, 2.0), (1.0, 0, 0))
    Dn = ((2.5, 2.5, 0), (0, 0, 1.0))
    fD1, fD2, fD3, fDn = circle(*D1), circle(*D2), circle(*D3), circle(*Dn)
    zD1 = dict(factors=[fD1], m=1)
    def balanced(spec, z2spec=zD1, p=(2.0, 0.0, 0.0)):
        P = [np.array([v]) for v in p]
        z1, g1 = field(dict(spec, amp=1.0), *P); z2, _ = field(z2spec, *P)
        amp = float(np.abs(z2[0]) / (ELL * np.sqrt(sum(np.abs(g[0])**2 for g in g1))))
        return dict(spec, amp=amp)
    borr = balanced(dict(factors=[fA, fB, fC], m=3, gauss=WG))
    split = balanced(dict(factors=[fA, fBe, fCe], m=3, gauss=WG))
    ringA = balanced(dict(factors=[fA], m=1, gauss=WG))
    borr3 = balanced(dict(factors=[fA, fB, fC], m=3, gauss=WG), dict(factors=[fD1, fD2, fD3], m=3))
    cfg = {
        "a":  (dict(factors=[poly_id1], m=1), dict(factors=[poly_id2], m=1)),
        "a1": (ringA, zD1),
        "b":  (borr, dict(factors=[poly_nozero], m=1)),
        "c":  (borr, dict(factors=[fD1], m=1)),
        "d":  (borr, dict(factors=[fDn], m=1)),
        "e":  (split, dict(factors=[fD1], m=1)),
        "f":  (borr3, dict(factors=[fD1, fD2, fD3], m=3)),
    }
    amps = {k: v[0].get("amp", 1.0) for k, v in cfg.items()}
    # zero curves (oriented) for the linking route
    cur = {}
    for name, P, fn in [("A", curve_ellipse("A"), fA), ("B", curve_ellipse("B"), fB), ("C", curve_ellipse("C"), fC),
                        ("Bs", curve_ellipse("B", (0, 0, 2.5)), fBe), ("Cs", curve_ellipse("C", (0, 0, -2.5)), fCe),
                        ("D1", curve_circle(*D1), fD1), ("D2", curve_circle(*D2), fD2), ("D3", curve_circle(*D3), fD3),
                        ("Dn", curve_circle(*Dn), fDn)]:
        cur[name], fmax = orient(P, fn)
        assert fmax < 1e-12, (name, fmax)
    pairs = [("A", "B"), ("B", "C"), ("C", "A"), ("A", "Bs"), ("Bs", "Cs"), ("Cs", "A"),
             ("A", "D1"), ("B", "D1"), ("C", "D1"), ("A", "Dn"), ("B", "Dn"), ("C", "Dn"),
             ("Bs", "D1"), ("Cs", "D1"), ("A", "D2"), ("B", "D2"), ("C", "D2"), ("A", "D3"), ("B", "D3"), ("C", "D3"),
             ("D1", "D2"), ("D2", "D3"), ("D3", "D1")]
    lk = {f"{p}-{q}": gauss_link(cur[p], cur[q]) for p, q in pairs}
    L_ = lambda p, q: round(lk[f"{p}-{q}"])
    pred_sum = {"a1": L_("A", "D1"),
                "b": 0,
                "c": L_("A", "D1") + L_("B", "D1") + L_("C", "D1"),
                "d": L_("A", "Dn") + L_("B", "Dn") + L_("C", "Dn"),
                "e": L_("A", "D1") + L_("Bs", "D1") + L_("Cs", "D1"),
                "f": sum(L_(r, d) for r in "ABC" for d in ("D1", "D2", "D3"))}
    BORR_JONES = [-1, 3, -2, 4, -2, 3, -1]      # Borromean rings (L6a4): -t^3+3t^2-2t+4-2/t+3/t^2-1/t^3
    UNLINK3 = [1, 2, 1]                         # 3-component unlink: (t^1/2 + t^-1/2)^2 = t + 2 + 1/t
    link_type = {}
    for label, names in (("borromean_config_ABC", ("A", "B", "C")), ("split_config_A_Bs_Cs", ("A", "Bs", "Cs"))):
        sub = {"A": curve_ellipse("A", M=240), "B": curve_ellipse("B", M=240), "C": curve_ellipse("C", M=240),
               "Bs": curve_ellipse("B", (0, 0, 2.5), M=240), "Cs": curve_ellipse("C", (0, 0, -2.5), M=240)}
        link_type[label] = []
        for ang in ((0.37, 0.81, 0.23), (1.1, 0.4, 2.0), (2.2, 1.3, 0.7)):      # three generic projections
            br, nc = bracket([sub[nm] for nm in names], ang)
            seq = jones_like(br)
            link_type[label].append({"projection_euler_angles": ang, "crossings": nc, "bracket_seq_step_A4_normalized": seq,
                                     "is_borromean_jones": seq == min([BORR_JONES, BORR_JONES[::-1], [-x for x in BORR_JONES]]),
                                     "is_unlink3_jones": seq == min([UNLINK3, [-x for x in UNLINK3]])})
    print("link type:", link_type, flush=True)
    res = {"schema": "q1_degree_check_v1", "params": dict(a=AE, b=BE, k=KE, R_D=RD, ell_balance=ELL, amp_z1=amps, gauss_w=WG, L=L, N=Ns),
           "gauss_linking": lk, "link_type_kauffman_bracket": link_type, "sum_lk_rings_with_z2_loops": pred_sum, "degree": {}}
    t0 = time.time()
    for N in Ns:
        for key, (s1, s2) in cfg.items():
            r = degree(s1, s2, N, want_pointwise_identity=(key == "a"))
            res["degree"].setdefault(key, {})[str(N)] = r
            print(f"N={N:4d} {key:3s} B = {r['B']:+.6f}   |dens| integral = {r['abs_integral']:.4f}   ({time.time() - t0:.0f}s)", flush=True)
    Nmax = str(max(Ns))
    s0 = int(np.sign(res["degree"]["a1"][Nmax]["B"])) * int(np.sign(pred_sum["a1"]))
    res["s0"] = s0
    # identity-map box tail: (1/2pi^2) Int_{r>L} 32 pi r^2/(1+r^2)^3 dr is an upper bound on the box tail (box contains the ball)
    rr = np.linspace(L, 4000, 2_000_001)
    tail_ball = float(np.trapezoid(32 * np.pi * rr**2 / (1 + rr**2) ** 3, rr) / (2 * np.pi**2))
    res["identity_tail_outside_ball_L"] = tail_ball
    verdict = {}
    for key in ["a1", "b", "c", "d", "e", "f"]:
        Bv = res["degree"][key][Nmax]["B"]
        verdict[key] = {"B": Bv, "nearest_int": int(round(Bv)), "pred_s0_sum_lk": s0 * pred_sum[key],
                        "match": bool(int(round(Bv)) == s0 * pred_sum[key] and abs(Bv - round(Bv)) < 0.02)}
    verdict["a"] = {"B": res["degree"]["a"][Nmax]["B"], "expected_abs_box_value_at_least": 1 - tail_ball}
    verdict["expectation_falsifiers"] = {"B(b) != 0": bool(verdict["b"]["nearest_int"] != 0),
                                         "B(d) != 0": bool(verdict["d"]["nearest_int"] != 0),
                                         "B(c) != B(e)": bool(verdict["c"]["nearest_int"] != verdict["e"]["nearest_int"])}
    res["verdict"] = verdict
    blob = json.dumps(res, indent=1, sort_keys=True) + "\n"
    open("q1_degree_check.json", "w").write(blob)
    print(json.dumps(verdict, indent=1))
    print("pairwise Gauss linking:", {k: round(v, 6) for k, v in lk.items()})
    print("json md5", hashlib.md5(blob.encode()).hexdigest())


if __name__ == "__main__":
    main()
