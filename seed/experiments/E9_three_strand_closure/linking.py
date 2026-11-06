"""Linking number between strand 1's vortex lines and the composite (strand 2) vortex lines.

Method: vortex lines of a component are the dual links through plaquettes on which the phase of
psi_k winds (sum of wrapped phase differences around the plaquette = 2 pi w). Each such plaquette gives a
straight dual segment of length h through its centre, along w times the plaquette normal; the segments
close into loops. The linking number of the strand-1 set with the strand-2 set is the Gauss double integral,
evaluated exactly for straight segments (signed solid-angle formula, Klenin and Langowski 2000).
The raw phase winding of psi_k on a closed loop counts the zeros it encloses, so the count does not depend on A.
usage: python3 linking.py FILE.npz [FILE.npz ...]     (also: python3 linking.py --start A|B R0)
"""
import numpy as np, sys

def vortex_segments(psi, h, ax0):
    """Return (P0, P1) arrays of dual segment endpoints for the vortex lines of psi (N^3 complex)."""
    # a tiny generic perturbation breaks exact ties (phase differences of exactly +-pi, or psi exactly 0,
    # which occur in the analytic starts centred on a site plane); it cannot change a count away from ties
    rng = np.random.default_rng(1)
    th = np.angle(psi + 1e-10 * (rng.normal(size=psi.shape) + 1j * rng.normal(size=psi.shape))); N = psi.shape[0]
    wrap = lambda d: (d + np.pi) % (2 * np.pi) - np.pi
    P0, P1 = [], []
    for mu in range(3):                       # plaquette normal
        a, b = [d for d in range(3) if d != mu]   # right-handed order (a, b, mu) up to sign
        sgn = 1 if (a, b, mu) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)] else -1
        s = [slice(None)] * 3; s[a] = slice(0, N - 1); s[b] = slice(0, N - 1)
        def sh(da, db):
            t = list(s); t[a] = slice(da, N - 1 + da); t[b] = slice(db, N - 1 + db); return th[tuple(t)]
        t00, t10, t11, t01 = sh(0, 0), sh(1, 0), sh(1, 1), sh(0, 1)
        w = np.rint((wrap(t10 - t00) + wrap(t11 - t10) + wrap(t01 - t11) + wrap(t00 - t01)) / (2 * np.pi)).astype(int) * sgn
        idx = np.argwhere(w != 0)
        for i in idx:
            ws = w[tuple(i)]
            c = np.array([ax0 + h * i[d] for d in range(3)], float)
            c[a] += h / 2; c[b] += h / 2
            e = np.zeros(3); e[mu] = h / 2
            for _ in range(abs(ws)):
                if ws > 0: P0.append(c - e); P1.append(c + e)
                else:      P0.append(c + e); P1.append(c - e)
    return np.array(P0).reshape(-1, 3), np.array(P1).reshape(-1, 3)

def _solid(a, b, c, d):
    """Signed Gauss linking contribution of segments a->b and c->d (vectorized over leading axes)."""
    r13, r14, r23, r24 = c - a, d - a, c - b, d - b
    def unit(v):
        n = np.linalg.norm(v, axis=-1, keepdims=True); return v / np.where(n == 0, 1, n)
    n1 = unit(np.cross(r13, r14)); n2 = unit(np.cross(r14, r24))
    n3 = unit(np.cross(r24, r23)); n4 = unit(np.cross(r23, r13))
    asin = lambda u, v: np.arcsin(np.clip(np.sum(u * v, -1), -1, 1))
    om = asin(n1, n2) + asin(n2, n3) + asin(n3, n4) + asin(n4, n1)
    sign = np.sign(np.sum(np.cross(d - c, b - a) * r13, -1))
    return om * sign / (4 * np.pi)

def linking(P0a, P1a, P0b, P1b):
    tot = 0.0
    for i in range(0, len(P0a), 64):
        a = P0a[i:i + 64, None]; b = P1a[i:i + 64, None]
        tot += _solid(a, b, P0b[None], P1b[None]).sum()
    return tot

def analyse(psi, h=0.5):
    N = psi.shape[1]; ax0 = -(N // 2) * h
    segs = [vortex_segments(psi[k], h, ax0) for k in range(3)]
    out = dict(nseg=[len(s[0]) for s in segs])
    out['Lk12'] = float(linking(*segs[0], *segs[1])) if len(segs[0]) and len(segs[1]) else 0.0
    out['Lk13'] = float(linking(*segs[0], *segs[2])) if len(segs[0]) and len(segs[2]) else 0.0
    out['Lk23'] = float(linking(*segs[1], *segs[2])) if len(segs[1]) and len(segs[2]) else 0.0
    return out

if __name__ == '__main__':
    if sys.argv[1] == '--start':
        from gl3 import GL3
        start, R0, N = sys.argv[2], float(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 49
        g = GL3(N=N, h=0.5, eta=0.1)
        f23 = g.ring_field((0, 0, 0), (0, 0, 1), R0)
        f1 = {'A': lambda: g.ring_field((R0, 0, 0), (0, 1, 0), R0),
              'B': lambda: g.ring_field((R0, 0, 0), (1, 0, 0), 2.0),
              'B_xz': lambda: g.ring_field((R0, 0, 0), (0, 1, 0), 2.0)}[start]()
        print(start, analyse(np.stack([f1, f23, f23])))
    else:
        for f in sys.argv[1:]:
            print(f, analyse(np.load(f)['psi']))
