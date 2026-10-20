#!/usr/bin/env python3
"""Diagnosis of the hopfion rms-radius disagreement (step 4 of the cross-check: reads the original code).

Feeds the exact ansatz profile (f(r) = F_Skyrme(sqrt2 r), from cc_hedgehog) into the ORIGINAL
e7_hopfion.py quadrature and spline machinery, and measures how the energy-rms radius depends on
the far tail of the 24-node cubic spline in t = r/(1+r).  Prints its findings; writes
cc_diag_hopfion_rms.json.
"""
import json
import os
import sys
sys.dont_write_bytecode = True        # do not create __pycache__ in the original E7 directory
import numpy as np
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))           # original E7 directory (read-only use)
import e7_hopfion as orig                             # noqa: E402
from cc_hedgehog import Hedgehog, basis               # noqa: E402

h = Hedgehog(N=60, L=2.0, Nq=1200); h.solve()


def F(x):
    x = np.atleast_1d(x).astype(float)
    t = x / (h.L + x)
    Phi, _, F0, _ = basis(t, h.N)
    return F0 + h.c @ Phi


out = {}
for lam in [1.0, 1.1575874188209163]:   # original code's Derrick scale factor for its own profile
    # profile in the original's unscaled coordinate r0 such that the Derrick-optimal configuration is f(r0 * lam ...)
    # we simply evaluate the exact optimal profile at scale lam: f(r0) = F(sqrt2 r0 / lam)
    rn = orig.tnodes[1:-1] / (1 - orig.tnodes[1:-1])
    vals = F(np.sqrt(2) * rn / lam)
    E2, E4, d2, d4, nn = orig.energies(vals)
    L = np.sqrt(E4 / E2)
    eps_s = L * d2 + d4 / L
    rms_s = np.sqrt(np.sum(orig.W * eps_s * orig.R ** 2) / np.sum(orig.W * eps_s)) * L
    # same, but drop the far tail r > 50 (in rescaled units) from the rms integrals
    mask = (orig.R * L) < 50
    rms_cut = np.sqrt(np.sum((orig.W * eps_s * orig.R ** 2)[mask]) / np.sum((orig.W * eps_s)[mask])) * L
    # spline tail: slope df/dt at t = 1 (nonzero slope <=> f ~ a/r tail, a = -df/dt(1))
    fv = np.concatenate([[np.pi], vals, [0.0]])
    cs = CubicSpline(orig.tnodes, fv, bc_type='not-a-knot')
    a_tail = -float(cs(1.0, 1))
    out[f"lam_in={lam:.4f}"] = dict(E=2 * np.sqrt(E2 * E4), rms_original_method=rms_s, rms_r_lt_50=rms_cut,
                                    spline_tail_coefficient_a=a_tail, r_max_quadrature=float(orig.rq.max() * L))
    print(f"input scale {lam:.4f}: E_W = {2*np.sqrt(E2*E4):.8f}, rms (original formula) = {rms_s:.5f}, "
          f"rms with r<50 = {rms_cut:.5f}, spline slope at t=1 -> f ~ {a_tail:.2e}/r tail, r_max = {orig.rq.max()*L:.3g}")
# exact answer for comparison
print("exact (analytic mapping, cc_hopfion): R_rms = x_E/sqrt2 = 2.06082")
with open(os.path.join(HERE, "cc_diag_hopfion_rms.json"), "w") as fh:
    json.dump(out, fh, indent=1, default=float)
