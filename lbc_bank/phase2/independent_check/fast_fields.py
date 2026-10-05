"""Hand-coded (product rule) fields + gradients for speed; cross-validated against the sympy version."""
import numpy as np

a2, b2, k = 4.0, 1.0, 1.0

def quad_field(U, V, Wc, iu, iv, iw):
    """f = U^2/a^2 + V^2/b^2 - 1 + i k Wc; returns f and grad (wrt x,y,z) given which coordinate index each arg is."""
    f = U**2/a2 + V**2/b2 - 1 + 1j*k*Wc
    g = np.zeros(U.shape + (3,), complex)
    g[..., iu] += 2*U/a2
    g[..., iv] += 2*V/b2
    g[..., iw] += 1j*k
    return f, g

def fA(X, Y, Z):  # x^2/a^2 + y^2/b^2 - 1 + ikz
    return quad_field(X, Y, Z, 0, 1, 2)

def fB(X, Y, Z):  # y^2/a^2 + z^2/b^2 - 1 + ikx
    return quad_field(Y, Z, X, 1, 2, 0)

def fC(X, Y, Z):  # z^2/a^2 + x^2/b^2 - 1 + iky
    return quad_field(Z, X, Y, 2, 0, 1)

def fD(X, Y, Z, c, m, R):
    d = np.stack([X - c[0], Y - c[1], Z - c[2]], -1)
    f = (d**2).sum(-1) - R**2 + 2j*R*(d @ np.array(m, float))
    g = 2*d + 2j*R*np.array(m, float)
    return f, g

def Wfun(X, Y, Z, A0):
    r2 = X**2 + Y**2 + Z**2
    W = A0*(1 + r2)**(-3)*np.exp(-r2/6.25)
    dWdr2 = W*(-3/(1 + r2) - 1/6.25)
    g = 2*np.stack([X, Y, Z], -1)*dWdr2[..., None]
    return W, g

def prod(*fg):
    f = np.ones_like(fg[0][0], dtype=complex)
    for fi, _ in fg:
        f = f*fi
    g = np.zeros(f.shape + (3,), complex)
    for i, (fi, gi) in enumerate(fg):
        other = np.ones_like(f)
        for j, (fj, _) in enumerate(fg):
            if j != i:
                other = other*fj
        g = g + gi*other[..., None]
    return f, g

D1 = dict(c=(2, 0, 0), m=(0, 1, 0), R=0.5)
D2 = dict(c=(0, 2, 0), m=(0, 0, 1), R=0.5)
D3 = dict(c=(0, 0, 2), m=(1, 0, 0), R=0.5)

def inv_pow(X, Y, Z, n):
    """(1+r^2)^(-n) and its gradient"""
    r2 = X**2 + Y**2 + Z**2
    f = (1 + r2)**(-n)
    g = -n*(1 + r2)**(-n - 1)
    return f.astype(complex), (2*np.stack([X, Y, Z], -1)*g[..., None]).astype(complex)

def make_fast(name):
    def ev(X, Y, Z, A0):
        X = np.asarray(X, float); Y = np.asarray(Y, float); Z = np.asarray(Z, float)
        Wv = Wfun(X, Y, Z, A0)
        if name == 'e':
            z1 = prod(fA(X, Y, Z), fB(X, Y, Z - 2.5), fC(X, Y, Z + 2.5), Wv)
        else:
            z1 = prod(fA(X, Y, Z), fB(X, Y, Z), fC(X, Y, Z), Wv)
        if name in ('c', 'e'):
            z2 = prod(fD(X, Y, Z, **D1), inv_pow(X, Y, Z, 1))
        elif name == 'f':
            z2 = prod(fD(X, Y, Z, **D1), fD(X, Y, Z, **D2), fD(X, Y, Z, **D3), inv_pow(X, Y, Z, 3))
        elif name == 'b':
            r2 = X**2 + Y**2 + Z**2
            num = (1 + r2 + 2j*Z, np.stack([2*X, 2*Y, 2*Z + 2j], -1).astype(complex))
            z2 = prod(num, inv_pow(X, Y, Z, 1))
        return z1[0], z2[0], z1[1], z2[1]
    return ev

if __name__ == '__main__':
    from fields import make_numeric
    rng = np.random.default_rng(5)
    P = rng.uniform(-4, 4, (2000, 3))
    for name in 'cebf':
        for A0 in (1.0, 250.0):
            s = make_numeric(name)(P[:, 0], P[:, 1], P[:, 2], A0)
            f = make_fast(name)(P[:, 0], P[:, 1], P[:, 2], A0)
            err = max(np.max(np.abs(s[i] - f[i])/(1e-300 + np.max(np.abs(s[i])))) for i in range(4))
            print(name, A0, 'max rel err fast vs sympy:', err)
