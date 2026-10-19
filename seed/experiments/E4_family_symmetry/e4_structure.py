"""
e4_structure.py -- E4 part 4b: generic rank / degeneracy scan of every texture class of e4_fits.py.

Why: the least-squares fits work in floating point, so a mass matrix whose smallest singular value
is EXACTLY zero (e.g. a Z7-aligned familon (0,0,1) in a Dirac product makes two rows or two columns
parallel) can show up at the best fit as a tiny non-zero mass ratio (1e-7 .. 1e-4, set by rounding
noise times the hierarchy the optimizer chose).  The fit verdict ("excluded") is unaffected, but
the reason must be stated correctly.  This script decides the structure exactly enough:
  * parameters are drawn with O(1) moduli (generic rank is reached on an open dense set, so no
    hierarchy is needed and rounding noise stays ~1e-16 relative);
  * generic rank = max over 40 random points of #(singular values > 1e-9 * largest);
  * structural degeneracy = smallest relative gap between singular values < 1e-9 at every point.
It also re-derives, symbolically, the rank-2 statement for a (0,0,1) familon in the 5-invariant
Dirac matrix (sympy, generic symbols).
Writes out/structure.json.  Run: python3 e4_structure.py   (about 10 s)
"""
import json
import os

import numpy as np
import sympy as sp

import e4_fits as F

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
TOL = 1e-9
NPTS = 40


def gen_point(c, rng):
    lay = F.layout(c)
    p = np.empty(len(lay))
    for k, t in enumerate(lay):
        if t == "phase":
            p[k] = rng.uniform(0, 2 * np.pi)
        elif t == "logmod":
            p[k] = rng.uniform(-1.0, 0.5)
        else:
            p[k] = rng.normal()
    return p


def matrices(c, p):
    """Rebuild the class's mass matrices exactly as e4_fits.lepton_obs / quark_obs do."""
    idx = 0
    code = F.CODES
    if c["sector"] == "lepton":
        u10, idx = F.flavon(p, idx, code[c["phi10"]] if c["variant"] != "LNR exact" else 3)
        if c["variant"] == "LNR exact":
            u5 = np.array([-1.0 + 0j, 1.0, 1.0])
            u1 = np.array([1.0 + 0j, 1.0, 1.0])
            ce = np.zeros(5, complex); ce[0] = 1
            cD = np.array([1, -1, -1, -1, -1], dtype=complex)
            alpha = p[idx] + 0j
        else:
            v = 0 if c["variant"] == "min" else 1
            u5, idx = F.flavon(p, idx, code[c["phi5"]])
            u1, idx = F.flavon(p, idx, code[c["phi1"]])
            ce, idx = F.coupl(p, idx, v, 0)
            cD, idx = F.coupl(p, idx, v, 1)
            alpha = p[idx] + 1j * p[idx + 1]
        Me = F.dirac(u5, u10, ce)
        MD = F.dirac(u5, u1, cD)
        MR = F.majorana(u1, alpha)
        out = {"M_e": Me, "M_D": MD, "M_R": MR}
        if abs(np.linalg.det(MR)) > 1e-12 * max(1.0, np.abs(MR).max()) ** 3:
            out["M_nu"] = -(MD @ np.linalg.inv(MR) @ MD.T)
        return out
    v = 0 if c["variant"] == "min" else 1
    u10, idx = F.flavon(p, idx, code[c["phi10"]])
    u5, idx = F.flavon(p, idx, code[c["phi5"]])
    if v == 0:
        alu = 0j
        cd = np.zeros(5, complex); cd[0] = 1
    else:
        alu = p[idx] + 1j * p[idx + 1]
        idx += 2
        cd, idx = F.coupl(p, idx, 1, 0)
    return {"M_u": F.majorana(u10, alu), "M_d": F.dirac(u10, u5, cd)}


def scan(c):
    rng = np.random.default_rng(12345)
    rank, mingap, singular_MR = {}, {}, 0
    for _ in range(NPTS):
        Ms = matrices(c, gen_point(c, rng))
        if "M_R" in Ms and "M_nu" not in Ms:
            singular_MR += 1
        for k, M in Ms.items():
            s = np.linalg.svd(M, compute_uv=False)
            r = int(np.sum(s > TOL * max(s[0], 1e-300)))
            rank[k] = max(rank.get(k, 0), r)
            ss = np.sort(s)
            gap = min((ss[i + 1] - ss[i]) / max(ss[-1], 1e-300) for i in range(2))
            mingap[k] = max(mingap.get(k, 0.0), gap)
    reasons = []
    charged = ("M_e",) if c["sector"] == "lepton" else ("M_u", "M_d")
    for k in charged:
        if rank[k] < 3:
            reasons.append(f"{k} has rank {rank[k]} for all parameters (massless charged fermion)")
        elif mingap[k] < TOL:
            reasons.append(f"{k} has an exactly degenerate pair for all parameters")
    if c["sector"] == "lepton":
        if singular_MR == NPTS:
            reasons.append("M_R singular for all parameters (seesaw undefined)")
        elif "M_nu" in rank and mingap["M_nu"] < TOL:
            reasons.append("light neutrinos have an exactly degenerate pair for all parameters (r = 1 or 0)")
    return {"rank": rank, "max_min_rel_gap": {k: float(v) for k, v in mingap.items()},
            "M_R_singular_everywhere": singular_MR == NPTS, "structural_reasons": reasons}


def symbolic_rank_z7():
    """Dirac matrix of e4_fits.dirac with u' = (0,0,1) and generic u, c: rank <= 2 (and with u = (0,0,1))."""
    u = sp.symbols("u1:4")
    c = sp.symbols("c0:5")
    res = {}
    for label, (uu, up) in {"row familon generic, column familon (0,0,1)": (u, (0, 0, 1)),
                            "row familon (0,0,1), column familon generic": ((0, 0, 1), u)}.items():
        M = sp.zeros(3, 3)
        for i in range(3):
            M[i, i] = c[0] * uu[i] * up[i]
        for (i, j) in ((0, 2), (2, 1), (1, 0)):
            M[i, j] = c[1] * uu[i] * up[j] + c[2] * uu[j] * up[i]
        for (i, j) in ((0, 1), (1, 2), (2, 0)):
            M[i, j] = c[3] * uu[i] * up[j] + c[4] * uu[j] * up[i]
        res[label] = {"matrix": str(M.tolist()), "det": str(sp.simplify(M.det())), "rank": M.rank()}
    Mmaj = sp.Matrix(3, 3, lambda i, j: (sp.Integer([0, 0, 1][i] * [0, 0, 1][j]) * (1 if i == j else sp.Symbol("alpha"))))
    res["Majorana with (0,0,1)"] = {"rank": Mmaj.rank()}
    return res


def main():
    classes = F.class_list()
    out = {}
    for c in classes:
        out[F.cname(c)] = scan(c)
    sym = symbolic_rank_z7()
    checks = {}
    checks["symbolic: Dirac matrix with a (0,0,1) familon has det = 0 and rank 2"] = all(
        v.get("det") == "0" and v["rank"] == 2 for k, v in sym.items() if k.startswith("row"))
    checks["symbolic: Majorana matrix with (0,0,1) has rank 1"] = sym["Majorana with (0,0,1)"]["rank"] == 1
    z7_classes = [n for n, c in zip(out, classes) if c["sector"] == "lepton" and c["variant"] != "LNR exact"
                  and ("Z7" in (c["phi5"], c["phi10"]))]
    checks["numeric: every lepton class with phi5 or phi10 = Z7 has rank(M_e) <= 2 (1 if M_e is diagonal or both are Z7)"] = all(
        out[n]["rank"]["M_e"] <= 2 for n in z7_classes)
    for k, v in checks.items():
        print(f"[{'PASS' if v else 'FAIL'}] {k}")
    n_struct = sum(bool(v["structural_reasons"]) for v in out.values())
    print(f"{n_struct} of {len(out)} classes are structurally dead (massless/degenerate charged fermion, "
          f"degenerate light neutrinos, or singular M_R)")
    json.dump({"tol": TOL, "n_points": NPTS, "classes": out, "symbolic": sym, "checks": checks,
               "all_pass": all(checks.values())}, open(os.path.join(OUT, "structure.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
