"""Check that the zero sets A,B,C of fA,fB,fC form the Borromean rings and that the translated triple of (e)
is the 3-component unlink: build a PD code from a generic planar projection of the 3D curves, feed to
SnapPy/spherogram (identify, volume, Jones), and compute Gauss linking numbers independently."""
import numpy as np

def curves(shift=False, n=4000):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    c, s = np.cos(t), np.sin(t)
    A = np.stack([2*c, s, 0*t], 1)
    B = np.stack([0*t, 2*c, s], 1)
    C = np.stack([s, 0*t, 2*c], 1)
    if shift:
        B = B + [0, 0, 2.5]; C = C + [0, 0, -2.5]
    return [A, B, C]

def orient_by_vorticity(P, f_grads):
    """Orient the polyline P along grad Re f x grad Im f (vortex orientation of the complex zero line)."""
    T = np.roll(P, -1, 0) - P
    gr, gi = f_grads(P)
    t_vort = np.cross(gr, gi)
    if np.sum(np.einsum('ij,ij->i', T, t_vort)) < 0:
        P = P[::-1].copy()
    return P

def grads_A(P):  # fA = x^2/4 + y^2 - 1 + i z
    x, y, z = P.T; return np.stack([x/2, 2*y, 0*x], 1), np.stack([0*x, 0*x, 1+0*x], 1)
def grads_B(P, dz=0.0):  # fB = y^2/4 + (z-dz)^2 - 1 + i x
    x, y, z = P.T; return np.stack([0*x, y/2, 2*(z-dz)], 1), np.stack([1+0*x, 0*x, 0*x], 1)
def grads_C(P, dz=0.0):  # fC = (z-dz)^2/4 + x^2 - 1 + i y
    x, y, z = P.T; return np.stack([2*x, 0*x, (z-dz)/2], 1), np.stack([0*x, 1+0*x, 0*x], 1)

def gauss_lk(P, Q):
    """Discrete Gauss linking integral between closed polylines P and Q (midpoint rule)."""
    dP = np.roll(P, -1, 0) - P; mP = P + dP/2
    dQ = np.roll(Q, -1, 0) - Q; mQ = Q + dQ/2
    tot = 0.0
    for i in range(0, len(mP), 500):
        r = mP[i:i+500, None, :] - mQ[None, :, :]
        cr = np.cross(dP[i:i+500, None, :], dQ[None, :, :])
        tot += np.sum(np.einsum('ijk,ijk->ij', cr, r)/np.linalg.norm(r, axis=2)**3)
    return tot/(4*np.pi)

def pd_code(comps, d):
    d = np.asarray(d, float); d /= np.linalg.norm(d)
    u = np.cross(d, [0.0, 0.0, 1.0]);
    if np.linalg.norm(u) < 1e-6: u = np.cross(d, [0.0, 1.0, 0.0])
    u /= np.linalg.norm(u); v = np.cross(d, u)          # (u, v, d) right-handed
    proj = [np.stack([P @ u, P @ v], 1) for P in comps]
    height = [P @ d for P in comps]
    # segment list
    segs = []
    for ci, Q in enumerate(proj):
        n = len(Q)
        for i in range(n):
            segs.append((ci, i, Q[i], Q[(i+1) % n]))
    S0 = np.array([s[2] for s in segs]); S1 = np.array([s[3] for s in segs])
    comp = np.array([s[0] for s in segs]); idx = np.array([s[1] for s in segs])
    crossings = []
    def cross2(a, b): return a[..., 0]*b[..., 1] - a[..., 1]*b[..., 0]
    for k in range(len(segs)):
        p, r = S0[k], S1[k] - S0[k]
        q, sv = S0[k+1:], S1[k+1:] - S0[k+1:]
        den = cross2(r[None, :], sv)
        with np.errstate(divide='ignore', invalid='ignore'):
            tt = cross2(q - p, sv)/den
            uu = cross2(q - p, r[None, :])/den
        hit = np.where((np.abs(den) > 1e-14) & (tt > 0) & (tt < 1) & (uu > 0) & (uu < 1))[0]
        for h in hit:
            m = k + 1 + h
            if comp[m] == comp[k] and abs(idx[m] - idx[k]) <= 1: continue
            ck, cm = comp[k], comp[m]
            nk, nm = len(proj[ck]), len(proj[cm])
            hk = height[ck][idx[k]]*(1-tt[h]) + height[ck][(idx[k]+1) % nk]*tt[h]
            hm = height[cm][idx[m]]*(1-uu[h]) + height[cm][(idx[m]+1) % nm]*uu[h]
            crossings.append(dict(a=(ck, idx[k] + tt[h]), b=(cm, idx[m] + uu[h]),
                                  ta=r, tb=sv[h], a_over=hk > hm, gap=abs(hk - hm)))
    # passages along each component, sorted by parameter
    passages = {ci: [] for ci in range(len(comps))}
    for xi, X in enumerate(crossings):
        passages[X['a'][0]].append((X['a'][1], xi, 'a'))
        passages[X['b'][0]].append((X['b'][1], xi, 'b'))
    edge_out = {}  # (xi, role) -> outgoing edge label;  edge_in similarly
    edge_in = {}
    label = 0
    for ci in passages:
        L = sorted(passages[ci])
        first = label
        for j, (_, xi, role) in enumerate(L):
            edge_out[(xi, role)] = label + j
        for j, (_, xi, role) in enumerate(L):
            edge_in[(xi, role)] = (label + j - 1) if j > 0 else (label + len(L) - 1)
        label += len(L)
    pd = []
    signs = []
    for xi, X in enumerate(crossings):
        under, over = ('b', 'a') if X['a_over'] else ('a', 'b')
        tu = X['t' + under]; to = X['t' + over]
        e_in, e_out = edge_in[(xi, under)], edge_out[(xi, under)]
        o_in, o_out = edge_in[(xi, over)], edge_out[(xi, over)]
        if cross2(tu, to) < 0:     # +t_o is CCW-next after -t_u
            pd.append([e_in, o_out, e_out, o_in])
        else:
            pd.append([e_in, o_in, e_out, o_out])
        # crossing sign (right-handed = +1): over x under . d > 0 convention
        signs.append(int(np.sign(cross2(to, tu))))
    return pd, crossings, signs


def kauffman_jones(pd, writhe):
    """Own state-sum: <X[a,b,c,d]> = A*P[a,b]P[c,d] + A^-1*P[a,d]P[b,c]; V(t) = (-A^3)^(-w) <D>/(-A^2-A^-2), A=t^(-1/4).
    Returned as a polynomial in A (and in t via A=t^(-1/4))."""
    import sympy as sp, itertools
    A = sp.Symbol('A')
    n = len(pd)
    total = 0
    for state in itertools.product((0, 1), repeat=n):
        parent = {}
        def find(x):
            parent.setdefault(x, x)
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        def union(x, y): parent[find(x)] = find(y)
        na = 0
        for (a, b, c, d), s in zip(pd, state):
            if s == 0: union(a, b); union(c, d); na += 1
            else: union(a, d); union(b, c)
        edges = {e for X in pd for e in X}
        loops = len({find(e) for e in edges})
        total += A**(na - (n - na)) * (-A**2 - A**-2)**(loops - 1)
    V = sp.expand((-A**3)**(-writhe) * total)
    t = sp.Symbol('t')
    Vt = sp.expand(V.subs(A, t**sp.Rational(-1, 4)))
    return Vt

if __name__ == '__main__':
    import snappy, spherogram
    for shift in (False, True):
        A, B, C = curves(shift)
        dz = 2.5 if shift else 0.0
        A = orient_by_vorticity(A, grads_A)
        B = orient_by_vorticity(B, lambda P: grads_B(P, dz))
        C = orient_by_vorticity(C, lambda P: grads_C(P, -dz))
        comps = [A, B, C]
        print("=== shifted (config e)" if shift else "=== original A,B,C (configs c,b,f)")
        print(" Gauss lk(A,B), lk(B,C), lk(A,C):", [round(gauss_lk(P, Q), 4) for P, Q in [(A, B), (B, C), (A, C)]])
        for dvec in ([0.31, 0.47, 0.83], [-0.62, 0.21, 0.75], [0.55, -0.66, 0.51]):
            pd, X, sg = pd_code(comps, dvec)
            L = spherogram.Link(pd)
            info = f" dir={dvec}: #crossings={len(pd)}, min height gap={min(x['gap'] for x in X):.3f}, comps={len(L.link_components)}"
            info += f", linking matrix={L.linking_matrix()}"
            info += f", writhe={sum(sg)}, own-Jones={kauffman_jones(pd, sum(sg))}"
            Ls = L.copy(); Ls.simplify('global')
            info += f", simplified crossings={len(Ls.crossings)}, split diagram pieces={len(L.split_link_diagram())}"
            print(info)
            if not shift:
                E = L.exterior()
                print("   SnapPy: volume=%.6f identify=%s" % (float(E.volume()), E.identify()))
    ref = spherogram.Link('L6a4')
    print("reference: SnapPy L6a4 volume =", float(snappy.Manifold('L6a4').volume()),
          "; own-Jones of spherogram's L6a4 PD (writhe from spherogram) =", kauffman_jones(ref.PD_code(), sum(c.sign for c in ref.crossings)))
    tre = spherogram.Link('K3a1')
    print("sanity: own-Jones of spherogram K3a1 (trefoil) =", kauffman_jones(tre.PD_code(), sum(c.sign for c in tre.crossings)),
          "writhe", sum(c.sign for c in tre.crossings))
