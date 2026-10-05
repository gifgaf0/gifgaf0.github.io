"""Gauss linking numbers between z1 zero loops (A,B,C) and z2 zero loops (D circles), all oriented by vorticity
t ~ grad Re f x grad Im f of their own complex factor."""
import numpy as np
from borromean import curves, orient_by_vorticity, grads_A, grads_B, grads_C, gauss_lk

def circle(c, m, R, n=4000):
    c = np.array(c, float); m = np.array(m, float)
    tmp = np.array([1.0, 0, 0]) if abs(m[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(m, tmp); e1 /= np.linalg.norm(e1); e2 = np.cross(m, e1)
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    return c + R*(np.cos(t)[:, None]*e1 + np.sin(t)[:, None]*e2)

def grads_D(c, m, R):
    c = np.array(c, float); m = np.array(m, float)
    return lambda P: (2*(P - c), np.tile(2*R*m, (len(P), 1)))

Ds = {'D1': ((2, 0, 0), (0, 1, 0), 0.5), 'D2': ((0, 2, 0), (0, 0, 1), 0.5), 'D3': ((0, 0, 2), (1, 0, 0), 0.5)}
Dcurves = {k: orient_by_vorticity(circle(*v), grads_D(*v)) for k, v in Ds.items()}
for shift in (False, True):
    A, B, C = curves(shift)
    dz = 2.5 if shift else 0.0
    rings = {'A': orient_by_vorticity(A, grads_A), 'B': orient_by_vorticity(B, lambda P: grads_B(P, dz)),
             'C': orient_by_vorticity(C, lambda P: grads_C(P, -dz))}
    tag = "translated (e)" if shift else "original"
    for dn, Dc in Dcurves.items():
        print(tag, dn, {rn: round(gauss_lk(R, Dc), 4) for rn, R in rings.items()})
