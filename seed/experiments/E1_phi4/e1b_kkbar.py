"""E1b: kink-antikink collisions. Critical velocity and two-bounce windows.

Initial condition (PLAN.md E1b, task notes):
  phi = tanh(g(x+x0)/sqrt2) - tanh(g(x-x0)/sqrt2) - 1, g = 1/sqrt(1-v^2),
  phi_t = -(g v/sqrt2)[sech^2(g(x+x0)/sqrt2) + sech^2(g(x-x0)/sqrt2)];
  kink at -x0 moving right, antikink at +x0 moving left, each with speed v.
Bounce counting: number of down-crossings (phi(0,t) going from > 0 to < 0).
Outcome:
  escape  - after the last bounce phi(0,t) stays > 0 and the kinks separate:
            early stop when the half-separation z (outermost zero of phi)
            exceeds x0 while increasing and phi(0) > 0 for the last 50 time
            units; otherwise at t_max = x0/v + t_post escape if phi(0) > 0
            over the last 150, z > 6 and z grew by > 0.1 over the last 100;
  capture - anything else (bion).
Label: n = number of bounces for an escape, 0 for capture.

Usage: python e1b_kkbar.py <dx> <x0> <tag> [t_post] [vmin vmax step] [nproc]
Writes e1b_<tag>.json.
"""
import sys
import json
import time
import numpy as np
from multiprocessing import Pool
from phi4core import grid, Sim, kk_initial, outer_zero

LPHYS = 40.0     # physical half-width; absorbing layer beyond
WSP = 30.0
GMAX = 1.0
CFL = 0.4


def collide(v, x0, dx, t_post=600.0, return_series=False):
    x = grid(LPHYS + WSP, dx)
    phi, pi = kk_initial(x, v, x0)
    dt = CFL * dx
    sim = Sim(x, phi, pi, dt, Lphys=LPHYS, W=WSP, gmax=GMAX)
    t_coll = x0 / v
    t_max = t_coll + t_post
    chunk_t = 2.0
    nchunk = int(round(chunk_t / dt))
    c_series = [np.array([sim.phi[sim.ic]])]
    z_t, z_v = [0.0], [outer_zero(x[x >= 0], sim.phi[x >= 0])]
    escaped = False
    early = False
    while sim.t < t_max - 1e-9:
        rec = sim.run(nchunk)
        c_series.append(rec)
        z_t.append(sim.t)
        z_v.append(outer_zero(x[x >= 0], sim.phi[x >= 0]))
        if sim.t > t_coll + 10.0:
            c = np.concatenate(c_series)
            nlast = int(round(50.0 / dt))
            zv = np.array(z_v)
            k10 = int(round(10.0 / chunk_t))
            if (np.all(c[-nlast:] > 0) and zv[-1] > x0 and len(zv) > k10
                    and zv[-1] - zv[-1 - k10] > 0.0 and np.min(c) < 0):
                escaped = True
                early = True
                break
    c = np.concatenate(c_series)
    tt = dt * np.arange(c.size)
    down = np.where((c[:-1] > 0) & (c[1:] <= 0))[0]
    nb = int(down.size)
    zv = np.array(z_v)
    if not escaped:
        n150 = int(round(150.0 / dt))
        k100 = int(round(100.0 / chunk_t))
        if (np.all(c[-n150:] > 0) and zv[-1] > 6.0 and zv[-1] - zv[-1 - k100] > 0.1
                and nb > 0):
            escaped = True
    out = {"v": v, "nb": nb, "escaped": escaped, "early": early,
           "label": nb if escaped else 0, "t_end": sim.t,
           "z_end": float(zv[-1]),
           "t_bounces": [float(tt[i]) for i in down[:12]]}
    if escaped and len(zv) > 6:
        # outgoing half-separation speed from the last 10 time units
        k = min(5, len(zv) - 1)
        out["v_out"] = float((zv[-1] - zv[-1 - k]) / (z_t[-1] - z_t[-1 - k]))
    if return_series:
        out["series"] = (tt, c, np.array(z_t), zv)
    return out


def _job(args):
    v, x0, dx, t_post = args
    r = collide(v, x0, dx, t_post)
    return r


def scan(vs, x0, dx, t_post, pool):
    res = pool.map(_job, [(float(v), x0, dx, t_post) for v in vs], chunksize=1)
    return res


def refine(results, x0, dx, t_post, pool, tol=2e-5):
    """Bisect every label change between consecutive scan points."""
    results = sorted(results, key=lambda r: r["v"])
    edges = []
    brackets = []
    for a, b in zip(results[:-1], results[1:]):
        if a["label"] != b["label"]:
            brackets.append([a, b])
    extra = []
    while brackets:
        mids = [0.5 * (a["v"] + b["v"]) for a, b in brackets]
        rs = pool.map(_job, [(m, x0, dx, t_post) for m in mids], chunksize=1)
        extra += rs
        nb = []
        for (a, b), r in zip(brackets, rs):
            # keep the half that still shows a change (prefer the one matching a's label boundary)
            if r["label"] != a["label"]:
                new = [a, r]
            else:
                new = [r, b]
            if r["label"] != a["label"] and r["label"] != b["label"]:
                # a third label in between: track both sub-brackets
                nb.append([r, b])
            if new[1]["v"] - new[0]["v"] <= tol:
                edges.append({"v_lo": new[0]["v"], "label_lo": new[0]["label"],
                              "v_hi": new[1]["v"], "label_hi": new[1]["label"],
                              "v_edge": 0.5 * (new[0]["v"] + new[1]["v"])})
            else:
                nb.append(new)
        brackets = []
        for br in nb:
            if br[1]["v"] - br[0]["v"] <= tol:
                if br[0]["label"] != br[1]["label"]:
                    edges.append({"v_lo": br[0]["v"], "label_lo": br[0]["label"],
                                  "v_hi": br[1]["v"], "label_hi": br[1]["label"],
                                  "v_edge": 0.5 * (br[0]["v"] + br[1]["v"])})
            else:
                brackets.append(br)
    edges = sorted(edges, key=lambda e: e["v_edge"])
    return edges, extra


def summarize(allres, edges):
    allres = sorted(allres, key=lambda r: r["v"])
    vs = np.array([r["v"] for r in allres])
    lab = np.array([r["label"] for r in allres])
    # v_c: lowest v above which every point is a 1-bounce escape
    not1 = np.where(lab != 1)[0]
    vc_lo = vs[not1[-1]] if not1.size else None
    above = vs[vs > vc_lo] if vc_lo is not None else vs
    vc_hi = above[0] if above.size else None
    vc = 0.5 * (vc_lo + vc_hi) if (vc_lo is not None and vc_hi is not None) else None
    # windows: maximal runs with label 2 below v_c, edges from bisection set
    windows = []
    i = 0
    while i < len(lab):
        if lab[i] == 2 and vs[i] < vc:
            j = i
            while j + 1 < len(lab) and lab[j + 1] == 2:
                j += 1
            lo = 0.5 * (vs[i - 1] + vs[i]) if i > 0 else vs[i]
            hi = 0.5 * (vs[j] + vs[j + 1]) if j + 1 < len(lab) else vs[j]
            windows.append({"lo": float(lo), "hi": float(hi), "width": float(hi - lo),
                            "n_points": int(j - i + 1),
                            "lo_bracket": [float(vs[i - 1]), float(vs[i])],
                            "hi_bracket": [float(vs[j]), float(vs[j + 1])]})
            i = j + 1
        else:
            i += 1
    # higher-bounce escape windows
    other = {}
    for nbv in sorted(set(lab.tolist())):
        if nbv >= 3:
            sel = vs[lab == nbv]
            other[str(nbv)] = [float(s) for s in sel]
    segs = []
    i = 0
    while i < len(lab):
        j = i
        while j + 1 < len(lab) and lab[j + 1] == lab[i]:
            j += 1
        segs.append([int(lab[i]), float(vs[i]), float(vs[j]), int(j - i + 1)])
        i = j + 1
    return {"v_c": float(vc), "v_c_bracket": [float(vc_lo), float(vc_hi)],
            "segments_label_vfirst_vlast_npts": segs,
            "two_bounce_windows": windows, "higher_bounce_escape_points": other}


if __name__ == "__main__":
    dx = float(sys.argv[1])
    x0 = float(sys.argv[2])
    tag = sys.argv[3]
    t_post = float(sys.argv[4]) if len(sys.argv) > 4 else 600.0
    if len(sys.argv) > 7:
        vmin, vmax, step = map(float, sys.argv[5:8])
    else:
        vmin, vmax, step = 0.15, 0.30, 0.0005
    nproc = int(sys.argv[8]) if len(sys.argv) > 8 else 2
    t0 = time.time()
    vs = np.round(np.arange(vmin, vmax + 0.5 * step, step), 7)
    with Pool(nproc) as pool:
        res = scan(vs, x0, dx, t_post, pool)
        t1 = time.time()
        print(f"[{tag}] coarse scan {len(vs)} runs in {t1 - t0:.0f} s", flush=True)
        edges, extra = refine(res, x0, dx, t_post, pool)
        print(f"[{tag}] refinement {len(extra)} runs in {time.time() - t1:.0f} s", flush=True)
    allres = res + extra
    summ = summarize(allres, edges)
    out = {"dx": dx, "x0": x0, "t_post": t_post, "cfl": CFL, "Lphys": LPHYS,
           "sponge_W": WSP, "gmax": GMAX, "scan": [vmin, vmax, step],
           "summary": summ, "edges": edges,
           "runs": sorted([{k: r[k] for k in ("v", "nb", "escaped", "label", "t_end", "z_end", "early")}
                           for r in allres], key=lambda r: r["v"]),
           "runtime_s": time.time() - t0}
    json.dump(out, open(f"e1b_{tag}.json", "w"), indent=1)
    print(json.dumps(summ, indent=1))
    print(f"[{tag}] total {time.time() - t0:.0f} s")
