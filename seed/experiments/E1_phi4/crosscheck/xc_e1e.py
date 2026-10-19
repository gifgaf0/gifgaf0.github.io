"""E1e cross-check: quanta counts of producing initial states, computed from my own initial data.
N*lambda/m^2 = E~/(2 sqrt2) (N = E/m) and N_lin*lambda/m^2 = N~_lin/2 with continuum dispersion
omega_q = sqrt(q^2+2) (FFT on a large box).  Derivation: phi = v Phi, x -> x/(sqrt(lambda) v) gives
E = sqrt(lambda) v^3 E~, m = sqrt(2 lambda) v, so E/m = v^2 E~/sqrt2 and v^2 = m^2/(2 lambda)."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xc_core import make_grid, energy, MKINK
from xc_e1d import init
from xc_e1c import dsv_init

def counts(phi, pi, dx):
    E = energy(phi, pi, dx)
    d = phi + 1.0
    n = len(d)
    q = 2 * np.pi * np.fft.fftfreq(n, d=dx)
    w = np.sqrt(q * q + 2.0)
    dq = np.fft.fft(d) * dx; pq = np.fft.fft(pi) * dx
    L = n * dx
    Nlin = np.sum((np.abs(pq) ** 2 + w ** 2 * np.abs(dq) ** 2) / (2 * w)) / L
    Equad = np.sum((np.abs(pq) ** 2 + w ** 2 * np.abs(dq) ** 2) / 2) / L
    return dict(E_over_2M=E / (2 * MKINK), N_E_lam_over_m2=E / (2 * np.sqrt(2)), N_lin_lam_over_m2=Nlin / 2,
                Equad_over_E=Equad / E)

out = {}
dx = 0.02
for (A, s, k) in [(0.8, 2.0, 0.5), (1.4, 1.0, 0.25), (0.275, 16.0, 0.2)]:
    x0 = 4 * s + 10
    x = make_grid(x0 + 8 * s + 200, dx)
    phi, pi = init(x, A, s, k, x0)
    out[f'gauss_{A}_{s}_{k}'] = counts(phi, pi, dx)
for (om, v) in [(0.95, 0.62), (0.90, 0.73), (0.99, 0.43)]:
    x = make_grid(700, 0.04)
    phi, pi, Nb = dsv_init(x, om, v)
    out[f'dsv_{om}_{v}'] = counts(phi, pi, 0.04)
for kk, vv in out.items():
    print(kk, {a: round(b, 4) for a, b in vv.items()})
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xc_e1e.json'), 'w'), indent=1)
