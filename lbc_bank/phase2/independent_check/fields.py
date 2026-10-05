"""Field definitions for Claim 1, built independently from the task statement (sympy -> numpy)."""
import numpy as np
import sympy as sp

x, y, z = sp.symbols('x y z', real=True)
A0s = sp.Symbol('A0', positive=True)
a, b, k = 2, 1, 1
I = sp.I

def fA(X, Y, Z):
    return X**2/a**2 + Y**2/b**2 - 1 + I*k*Z

def fB(X, Y, Z):
    return Y**2/a**2 + Z**2/b**2 - 1 + I*k*X

def fC(X, Y, Z):
    return Z**2/a**2 + X**2/b**2 - 1 + I*k*Y

def fD(c, m, R):
    d = (x - c[0], y - c[1], z - c[2])
    return d[0]**2 + d[1]**2 + d[2]**2 - R**2 + 2*I*R*(d[0]*m[0] + d[1]*m[1] + d[2]*m[2])

r2 = x**2 + y**2 + z**2
Wr = A0s * (1 + r2)**(-3) * sp.exp(-r2/sp.Rational(625, 100))

R = sp.Rational(1, 2)
D1 = dict(c=(2, 0, 0), m=(0, 1, 0), R=R)
D2 = dict(c=(0, 2, 0), m=(0, 0, 1), R=R)
D3 = dict(c=(0, 0, 2), m=(1, 0, 0), R=R)
fD1, fD2, fD3 = (fD(**D) for D in (D1, D2, D3))

S = sp.Rational(5, 2)
configs = {
    'c': (fA(x, y, z)*fB(x, y, z)*fC(x, y, z)*Wr, fD1/(1 + r2)),
    'e': (fA(x, y, z)*fB(x, y, z - S)*fC(x, y, z + S)*Wr, fD1/(1 + r2)),
    'b': (fA(x, y, z)*fB(x, y, z)*fC(x, y, z)*Wr, (1 + r2 + 2*I*z)/(1 + r2)),
    'f': (fA(x, y, z)*fB(x, y, z)*fC(x, y, z)*Wr, fD1*fD2*fD3/(1 + r2)**3),
}
D_circles = {'c': [D1], 'e': [D1], 'b': [], 'f': [D1, D2, D3]}

def make_numeric(name):
    z1, z2 = configs[name]
    exprs = [z1, z2] + [sp.diff(z1, v) for v in (x, y, z)] + [sp.diff(z2, v) for v in (x, y, z)]
    fn = sp.lambdify((x, y, z, A0s), exprs, 'numpy')
    def ev(X, Y, Zc, A0):
        X = np.asarray(X, dtype=float); Y = np.asarray(Y, dtype=float); Zc = np.asarray(Zc, dtype=float)
        out = fn(X, Y, Zc, A0)
        out = [np.broadcast_to(np.asarray(o, dtype=complex), X.shape) for o in out]
        z1v, z2v = out[0], out[1]
        dz1 = np.stack(out[2:5], axis=-1)   # (...,3)
        dz2 = np.stack(out[5:8], axis=-1)
        return z1v, z2v, dz1, dz2
    return ev

def local_sign(z1v, z2v, dz1, dz2):
    """sign det[F, dF/dx, dF/dy, dF/dz], F=(Re z1, Im z1, Re z2, Im z2): local degree of n=F/|F|
    with S^3 oriented as boundary of B^4 (outward normal first)."""
    F = np.stack([z1v.real, z1v.imag, z2v.real, z2v.imag], axis=-1)            # (...,4)
    dF = np.stack([dz1.real, dz1.imag, dz2.real, dz2.imag], axis=-2)           # (...,4,3)
    M = np.concatenate([F[..., :, None], dF], axis=-1)                         # (...,4,4)
    return np.sign(np.linalg.det(M)), np.linalg.det(M)

def circle_param(D, t):
    c = np.array(D['c'], float); m = np.array(D['m'], float); Rv = float(D['R'])
    # orthonormal basis of plane perpendicular to m
    tmp = np.array([1.0, 0, 0]) if abs(m[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(m, tmp); e1 /= np.linalg.norm(e1)
    e2 = np.cross(m, e1)
    return c[None, :] + Rv*(np.cos(t)[:, None]*e1[None, :] + np.sin(t)[:, None]*e2[None, :])
