"""
analysis_lib.py -- extra diagnostics for the E8 configuration-type identification
(kept separate from fs_lib.py so that running relaxations are not affected).

  * slice_degree: degree m of the field restricted to a half-plane bounded by the
    symmetry axis (the winding of the 2D soliton that is swept round the ring);
    for an axial A_{n,m} field the half-plane boundary (axis + infinity) maps to e3,
    so the restricted field is a map S^2 -> S^2 and m = (1/4pi) Int phi.(d_s phi x d_t phi).
  * loop_shape: planarity / circularity of a closed polygon.
  * classify_curves: Sutcliffe-type label from position/linking curves.
"""
import numpy as np
from scipy.ndimage import map_coordinates


def _solid_angle(a, b, c):
    det = np.einsum('...i,...i->...', a, np.cross(b, c))
    den = 1.0 + np.einsum('...i,...i->...', a, b) + np.einsum('...i,...i->...', b, c) + np.einsum('...i,...i->...', c, a)
    return 2.0 * np.arctan2(det, den)


def sample_field(phi, h, L, pts):
    """Trilinear interpolation of phi at physical points pts (..., 3); outside the box the
    boundary value e3 is used (mode='nearest' on a grid whose boundary is e3)."""
    idx = (pts + L) / h
    coords = np.moveaxis(idx, -1, 0).reshape(3, -1)
    out = np.empty((coords.shape[1], 3))
    for c in range(3):
        out[:, c] = map_coordinates(phi[..., c], coords, order=1, mode='nearest')
    out /= np.linalg.norm(out, axis=-1, keepdims=True)
    return out.reshape(pts.shape)


def slice_degree(phi, h, L, centre, u, e, thetas, res=None, ext=None):
    """Degree of phi on the half-planes {centre + s u + t e_theta, t >= 0}, e_theta = cos(th) e + sin(th) (u x e)."""
    u = np.asarray(u, float); u /= np.linalg.norm(u)
    e = np.asarray(e, float); e -= (e @ u) * u; e /= np.linalg.norm(e)
    w = np.cross(u, e)
    if res is None:
        res = h / 2
    if ext is None:
        ext = 0.95 * L
    s = np.arange(-ext, ext + 1e-9, res)
    t = np.arange(0.0, ext + 1e-9, res)
    S, T = np.meshgrid(s, t, indexing='ij')
    degs = []
    for th in thetas:
        et = np.cos(th) * e + np.sin(th) * w
        pts = centre[None, None, :] + S[..., None] * u[None, None, :] + T[..., None] * et[None, None, :]
        P = sample_field(phi, h, L, pts)
        a = P[:-1, :-1]; b = P[1:, :-1]; c = P[1:, 1:]; d = P[:-1, 1:]
        om = _solid_angle(a, b, c) + _solid_angle(a, c, d)
        # boundary check: field on the axis (t=0) and the far edges should be close to e3
        edge = np.concatenate([P[:, 0, 2], P[0, :, 2], P[-1, :, 2], P[:, -1, 2]])
        degs.append(dict(theta=float(th), degree=float(om.sum() / (4 * np.pi)), min_phi3_on_edges=float(edge.min())))
    return degs


def loop_shape(c):
    """Planarity and circularity of a closed polygon c (n,3)."""
    m = c.mean(0)
    X = c - m
    U, sv, Vt = np.linalg.svd(X, full_matrices=False)
    normal = Vt[2]
    z = X @ normal
    inplane = X - np.outer(z, normal)
    rad = np.linalg.norm(inplane, axis=1)
    return dict(centre=m.tolist(), normal=normal.tolist(), mean_radius=float(rad.mean()),
                out_of_plane_rms_over_radius=float(np.sqrt((z ** 2).mean()) / rad.mean()),
                radius_std_over_mean=float(rad.std() / rad.mean()),
                length=float(np.sum(np.linalg.norm(np.diff(np.vstack([c, c[:1]]), axis=0), axis=1))))
