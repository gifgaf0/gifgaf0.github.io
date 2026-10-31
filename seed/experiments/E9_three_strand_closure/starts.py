"""
Starting configurations for E9, as fixed by PREREG.md Amendment B. Used by run_N1.py and trace_N1.py.

A vortex of unit winding along a closed curve C is built from the solid-angle phase: at a point x the
phase is Omega_C(x)/2, where Omega_C is the solid angle subtended by a surface bounded by C (a fan of
triangles from the curve's first point). Omega jumps by 4*pi across that surface, so the phase jumps
by 2*pi and the field is single-valued. The amplitude is tanh(distance to C / core).
"""
import numpy as np

def _tri_solid_angle(P, a, b, c):
    """Signed solid angle of triangle (a,b,c) seen from points P (..., 3). Van Oosterom & Strackee (1983)."""
    A = a - P; B = b - P; C = c - P
    la, lb, lc = (np.linalg.norm(X, axis=-1) for X in (A, B, C))
    num = np.einsum('...i,...i->...', A, np.cross(B, C))
    den = (la * lb * lc + np.einsum('...i,...i->...', A, B) * lc
           + np.einsum('...i,...i->...', A, C) * lb + np.einsum('...i,...i->...', B, C) * la)
    return 2 * np.arctan2(num, den)

def curve_field(g, curve, core=1.0):
    """Unit-winding vortex along the closed polyline `curve` (M, 3) on the grid of GL3 instance g."""
    # Grid points exactly coplanar with a fan triangle make the arctan2 branch ambiguous (spurious 2*pi
    # jumps). Shift the curve by a fixed, tiny, generic offset so no grid point is ever coplanar.
    curve = np.asarray(curve, float) + np.array([1.3e-3, 2.9e-3, 4.7e-3]) * g.h
    P = np.stack([g.x, g.y, g.z], -1)
    p0 = curve[0]; omega = np.zeros(g.x.shape)
    for i in range(1, len(curve) - 1):
        omega += _tri_solid_angle(P, p0, curve[i], curve[i + 1])
    phase = omega / 2
    # distance to the curve (segment-wise)
    d = np.full(g.x.shape, np.inf)
    for i in range(len(curve) - 1):
        a, b = curve[i], curve[i + 1]; ab = b - a
        t = np.clip(((P - a) @ ab) / (ab @ ab), 0, 1)
        d = np.minimum(d, np.linalg.norm(P - (a + t[..., None] * ab), axis=-1))
    return np.tanh(d / core) * np.exp(1j * phase)

def circle(center, u, v, r, M=240):
    t = np.linspace(0, 2 * np.pi, M + 1)
    c = np.asarray(center, float); u = np.asarray(u, float); v = np.asarray(v, float)
    return c + r * (np.cos(t)[:, None] * u + np.sin(t)[:, None] * v)

def helix_on_ring(R, a, turns=1, M=480):
    """(1, turns) helix of minor radius a around the circle of radius R in the z=0 plane."""
    t = np.linspace(0, 2 * np.pi, M + 1)
    rr = R + a * np.cos(turns * t)
    return np.stack([rr * np.cos(t), rr * np.sin(t), a * np.sin(turns * t)], -1)

def start_fields(g, start, R0):
    """Returns psi (3, N, N, N): strand 1 = psi[0]; strands 2, 3 = the composite ring of radius R0."""
    f23 = curve_field(g, circle((0, 0, 0), (1, 0, 0), (0, 1, 0), R0))
    if start == 'A':      # Hopf link: strand 1 on a circle of radius R0 in the x-z plane, centred at (R0, 0, 0)
        f1 = curve_field(g, circle((R0, 0, 0), (1, 0, 0), (0, 0, 1), R0))
    elif start == 'B':    # PREREG §9: (1,1) helix of minor radius 2 around the ring core
        f1 = curve_field(g, helix_on_ring(R0, 2.0, 1))
    else:
        raise ValueError(start)
    return np.stack([f1, f23, f23])
