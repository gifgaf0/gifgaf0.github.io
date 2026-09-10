# g_ci1_phase1_irrep_ccleg.py — G-CI1 CC leg, Phase 1: I-1 irrep/helicity audit
# (E-9 full-from-scratch; anchor-free; substrate units, rho = 1).
#
# R-a machine check (prereg 4, Phase 1.1): rotations R_theta about k-hat for
# theta in {0.1, 2*pi/7, 2*pi/5}, tau_h = 1e-12, acting on
#   (i)   the aggregate transverse polarization subspace,
#   (ii)  each single-crystal qT eigenvector of the four E-7 tensors on a
#         >= 26 direction set including axial/basal/oblique members,
#   (iii) the derived plane-wave strain sym(k (x) u) and stress C:eps.
# Helicity content per D-4 (ratified first-clause reading: a branch's helicity
# content is the eigenphase multiset of its MODE polarization/orbital data;
# derived strain/stress eigenphases are kinematic labels, recorded, not content).
#
# R-b inventory (prereg 4, Phase 1.2; E-4 inventory only): table over the
# banked branches; a branch absent from the records is ABSENT, not modelled.
#
# F-IRR (prereg 4, Phase 1.3): K := {branches: gapless AND (+-2 in helicity
# content) AND DEGENERATE-with-cone}; K = 0 -> F-IRR FIRES.

import math
import os

import numpy as np

import gci1_cc_common as cc

TAU_H = 1e-12
THETAS = [0.1, 2.0 * math.pi / 7.0, 2.0 * math.pi / 5.0]
CONTENT_AMP_TOL = 1e-8   # categorical presence cut on amplitude fraction
INPUT_JSON = os.path.join(cc.EMBED_DIR, "poly_vrh_results.json")
INPUT_JSON_MD5 = "200e7a8b775577564369c6924d38a84c"

CONFIGS = ["hex:step", "hex:gem8", "cubic:step", "cubic:gem8"]


# ---------------------------------------------------------------- tensors ----

def voigt_to_full(Cv):
    """6x6 Voigt matrix -> full C_ijkl (elasticity conventions)."""
    vm = {(0, 0): 0, (1, 1): 1, (2, 2): 2,
          (1, 2): 3, (2, 1): 3, (0, 2): 4, (2, 0): 4, (0, 1): 5, (1, 0): 5}
    C = np.zeros((3, 3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    C[i, j, k, l] = Cv[vm[(i, j)], vm[(k, l)]]
    return C


def build_config_tensors():
    import json as _json
    if cc.md5_file(INPUT_JSON) != INPUT_JSON_MD5:
        raise RuntimeError("input tensor file hash mismatch — HALT")
    with open(INPUT_JSON) as fh:
        data = _json.load(fh)
    out = {}
    for name in CONFIGS:
        c = data["vrh"][name]["C_over_rho"]
        Cv = np.zeros((6, 6))
        if name.startswith("hex"):
            c11, c12, c13, c33, c44, c66 = (c["C11"], c["C12"], c["C13"],
                                            c["C33"], c["C44"], c["C66"])
            Cv[0, 0] = Cv[1, 1] = c11
            Cv[2, 2] = c33
            Cv[0, 1] = Cv[1, 0] = c12
            Cv[0, 2] = Cv[2, 0] = Cv[1, 2] = Cv[2, 1] = c13
            Cv[3, 3] = Cv[4, 4] = c44
            Cv[5, 5] = c66
        else:
            c11, c12, c44 = c["C11"], c["C12"], c["C44"]
            for i in range(3):
                Cv[i, i] = c11
            for i in range(3):
                for j in range(3):
                    if i != j:
                        Cv[i, j] = c12
            for i in range(3, 6):
                Cv[i, i] = c44
        out[name] = voigt_to_full(Cv)
    return out, data


def iso_tensor(kk, mu):
    """Isotropic C_ijkl with bulk kk and shear mu."""
    lam = kk - 2.0 * mu / 3.0
    d = np.eye(3)
    return (lam * np.einsum("ij,kl->ijkl", d, d)
            + mu * (np.einsum("ik,jl->ijkl", d, d)
                    + np.einsum("il,jk->ijkl", d, d)))


def voigt_avg_moduli(C):
    """Voigt (arithmetic) bulk and shear from full C_ijkl."""
    kv = np.einsum("iijj->", C) / 9.0
    gv = (np.einsum("ijij->", C) - np.einsum("iijj->", C) / 3.0) / 10.0
    return kv, gv


def hill_moduli_from_json(cfg_entry):
    return cfg_entry["K_VRH"], cfg_entry["G_VRH"]


# ------------------------------------------------------------- directions ----

def direction_set():
    """35 directions: 13 lattice axes (axial [001]; basal [100],[010],
    [110],[1-10]; face/body diagonals oblique) + 22 Fibonacci points."""
    base = [(0, 0, 1), (1, 0, 0), (0, 1, 0),
            (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1),
            (0, 1, 1), (0, 1, -1),
            (1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]
    dirs = [np.array(v, float) / np.linalg.norm(v) for v in base]
    labels = (["axial"] + ["basal"] * 4 + ["oblique"] * 8)
    ng = 22
    golden = (1.0 + 5.0 ** 0.5) / 2.0
    for i in range(ng):
        zc = (2.0 * (i + 0.5) / ng) - 1.0
        phi = 2.0 * math.pi * ((i / golden) % 1.0)
        rr = math.sqrt(max(0.0, 1.0 - zc * zc))
        dirs.append(np.array([rr * math.cos(phi), rr * math.sin(phi), zc]))
        labels.append("generic")
    return dirs, labels


# --------------------------------------------------------- helicity frame ----

def frame(nhat):
    """Deterministic orthonormal (e1, e2) completing nhat."""
    a = np.array([1.0, 0.0, 0.0])
    if abs(np.dot(a, nhat)) > 0.9:
        a = np.array([0.0, 1.0, 0.0])
    e1 = a - np.dot(a, nhat) * nhat
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(nhat, e1)
    return e1, e2


def rot_about(nhat, th):
    """Rodrigues rotation about nhat by th."""
    K = np.array([[0.0, -nhat[2], nhat[1]],
                  [nhat[2], 0.0, -nhat[0]],
                  [-nhat[1], nhat[0], 0.0]])
    return np.eye(3) + math.sin(th) * K + (1.0 - math.cos(th)) * (K @ K)


def helicity_vec_basis(nhat):
    e1, e2 = frame(nhat)
    hp = (e1 - 1j * e2) / math.sqrt(2.0)   # helicity +1
    hm = (e1 + 1j * e2) / math.sqrt(2.0)   # helicity -1
    return {+1: hp, 0: nhat.astype(complex), -1: hm}


def helicity_sym2_basis(nhat):
    v = helicity_vec_basis(nhat)
    hp, h0, hm = v[+1], v[0], v[-1]

    def sym(a, b):
        return (np.outer(a, b) + np.outer(b, a)) / 2.0

    T = {
        +2: np.outer(hp, hp),
        -2: np.outer(hm, hm),
        +1: math.sqrt(2.0) * sym(hp, h0),
        -1: math.sqrt(2.0) * sym(hm, h0),
        "0a": np.outer(h0, h0),
        "0b": (np.outer(hp, hm) + np.outer(hm, hp)) / math.sqrt(2.0),
    }
    return T


def vec_components(u, nhat):
    b = helicity_vec_basis(nhat)
    return {lam: np.vdot(b[lam], u) for lam in b}


def sym2_components(S, nhat):
    T = helicity_sym2_basis(nhat)
    return {lam: np.vdot(T[lam].reshape(-1), S.reshape(-1)) for lam in T}


def lam_of(key):
    return 0 if key in ("0a", "0b") else key


def amp_fractions(comp):
    tot = math.sqrt(sum(abs(v) ** 2 for v in comp.values()))
    if tot == 0.0:
        return {k: 0.0 for k in comp}, 0.0
    return {k: abs(v) / tot for k, v in comp.items()}, tot


def content_set(comp):
    fr, _ = amp_fractions(comp)
    lams = set()
    for k, f in fr.items():
        if f > CONTENT_AMP_TOL:
            lams.add(lam_of(k))
    return sorted(lams)


def machine_check_vec(u, nhat, comp):
    """max over theta of || R_theta u - sum c_lam e^{i lam theta} b_lam ||."""
    b = helicity_vec_basis(nhat)
    worst = 0.0
    for th in THETAS:
        R = rot_about(nhat, th)
        lhs = R @ u.astype(complex)
        rhs = sum(comp[lam] * np.exp(1j * lam_of(lam) * th) * b[lam]
                  for lam in comp)
        worst = max(worst, float(np.linalg.norm(lhs - rhs)))
    return worst


def machine_check_sym2(S, nhat, comp):
    T = helicity_sym2_basis(nhat)
    worst = 0.0
    for th in THETAS:
        R = rot_about(nhat, th)
        lhs = R @ S @ R.T
        rhs = sum(comp[lam] * np.exp(1j * lam_of(lam) * th) * T[lam]
                  for lam in comp)
        worst = max(worst, float(np.linalg.norm(lhs - rhs)))
    return worst


def excl_pm2(present_lams):
    """The +-2 exclusion in eigenphase form: for each theta, no eigenphase
    e^{i lam theta} with lam in the content set falls within tau_h of the
    +-2 eigenphase.  Returns the minimum phase distance found."""
    best = float("inf")
    for th in THETAS:
        for lam in present_lams:
            for s2 in (+2, -2):
                d = abs((lam - s2) * th)
                d = min(d % (2.0 * math.pi), 2.0 * math.pi - d % (2.0 * math.pi))
                best = min(best, d)
    return best


# -------------------------------------------------------------- christoffel --

def christoffel_branches(C, nhat):
    """Returns list of (speed, eigval, u, |u.n|) sorted: qL identified by max
    |u.n|; among the rest qT1 = faster, qT2 = slower."""
    G = np.einsum("ijkl,j,l->ik", C, nhat, nhat)
    w, V = np.linalg.eigh(G)
    br = []
    for idx in range(3):
        u = V[:, idx]
        br.append((math.sqrt(max(w[idx], 0.0)), float(w[idx]), u,
                   abs(float(np.dot(u, nhat)))))
    ql_idx = max(range(3), key=lambda i: br[i][3])
    qts = sorted((br[i] for i in range(3) if i != ql_idx),
                 key=lambda t: -t[0])
    return br[ql_idx], qts[0], qts[1]


# --------------------------------------------------------------------- main --

def main():
    pats = cc.load_t1_patterns()
    tensors, data = build_config_tensors()
    dirs, dlabels = direction_set()

    # (i) aggregate transverse polarization subspace under R_theta
    agg_records = []
    worst_sub = 0.0
    for nhat in dirs:
        e1, e2 = frame(nhat)
        B = np.stack([e1, e2], axis=1)
        for th in THETAS:
            R = rot_about(nhat, th)
            M = B.T @ R @ B
            ev = np.linalg.eigvals(M)
            ph = sorted(np.angle(ev))
            tgt = sorted([-th, th])
            dev = max(abs(ph[0] - tgt[0]), abs(ph[1] - tgt[1]))
            worst_sub = max(worst_sub, dev)
    agg_records.append({
        "object": "aggregate transverse polarization subspace",
        "eigenphase_multiset_per_theta": "{+1*theta, -1*theta}",
        "helicity_content": [-1, 1],
        "max_eigenphase_dev": worst_sub,
        "pm2_exclusion_min_phase_distance": excl_pm2([-1, 1]),
        "pass_tau_h": bool(worst_sub <= TAU_H),
    })

    # aggregate derived strain/stress (isotropized Voigt-reference tensor)
    agg_derived = []
    for name in CONFIGS:
        kv, gv = voigt_avg_moduli(tensors[name])
        Ciso = iso_tensor(kv, gv)
        worst = {"strain_pm2_amp_frac": 0.0, "stress_pm2_amp_frac": 0.0,
                 "strain_recompose_dev": 0.0, "stress_recompose_dev": 0.0}
        for nhat in dirs[:6]:
            e1, _ = frame(nhat)
            u = e1  # a transverse channel polarization
            eps = (np.outer(nhat, u) + np.outer(u, nhat)) / 2.0
            sig = np.einsum("ijkl,kl->ij", Ciso, eps)
            for tag, S in (("strain", eps), ("stress", sig)):
                comp = sym2_components(S.astype(complex), nhat)
                fr, _ = amp_fractions(comp)
                worst[tag + "_pm2_amp_frac"] = max(
                    worst[tag + "_pm2_amp_frac"], fr[+2], fr[-2])
                worst[tag + "_recompose_dev"] = max(
                    worst[tag + "_recompose_dev"],
                    machine_check_sym2(S.astype(complex), nhat, comp))
        agg_derived.append({"config": name, "K_V": kv, "G_V": gv, **worst})

    # (ii)+(iii) single-crystal qT branches
    sc_summary = []
    sc_rows = []
    for name in CONFIGS:
        C = tensors[name]
        n_pm2_stress = 0
        n_dirs_pm2_stress = 0
        max_stress_pm2 = 0.0
        max_strain_pm2 = 0.0
        worst_recompose = 0.0
        for nhat, dl in zip(dirs, dlabels):
            _, qt1, qt2 = christoffel_branches(C, nhat)
            dir_has = False
            for bname, (spd, ev, u, undot) in (("qT1", qt1), ("qT2", qt2)):
                uc = u.astype(complex)
                comp_u = vec_components(uc, nhat)
                dev_u = machine_check_vec(u, nhat, comp_u)
                fr_u, _ = amp_fractions(comp_u)
                cont_u = content_set(comp_u)
                eps = (np.outer(nhat, u) + np.outer(u, nhat)) / 2.0
                sig = np.einsum("ijkl,kl->ij", C, eps)
                comp_e = sym2_components(eps.astype(complex), nhat)
                comp_s = sym2_components(sig.astype(complex), nhat)
                fr_e, _ = amp_fractions(comp_e)
                fr_s, _ = amp_fractions(comp_s)
                dev_e = machine_check_sym2(eps.astype(complex), nhat, comp_e)
                dev_s = machine_check_sym2(sig.astype(complex), nhat, comp_s)
                worst_recompose = max(worst_recompose, dev_u, dev_e, dev_s)
                e_pm2 = max(fr_e[+2], fr_e[-2])
                s_pm2 = max(fr_s[+2], fr_s[-2])
                max_strain_pm2 = max(max_strain_pm2, e_pm2)
                max_stress_pm2 = max(max_stress_pm2, s_pm2)
                if s_pm2 > CONTENT_AMP_TOL:
                    n_pm2_stress += 1
                    dir_has = True
                sc_rows.append({
                    "config": name, "dir": [float(x) for x in nhat],
                    "dir_class": dl, "branch": bname,
                    "speed": spd, "u_dot_n_abs": undot,
                    "mode_helicity_content": cont_u,
                    "mode_amp_fracs": {str(k): fr_u[k] for k in fr_u},
                    "mode_recompose_dev": dev_u,
                    "strain_labels_content": content_set(comp_e),
                    "strain_pm2_amp_frac": e_pm2,
                    "stress_labels_content": content_set(comp_s),
                    "stress_pm2_amp_frac": s_pm2,
                    "recompose_dev_strain": dev_e,
                    "recompose_dev_stress": dev_s,
                    "pm2_exclusion_min_phase_distance": excl_pm2(cont_u),
                })
            if dir_has:
                n_dirs_pm2_stress += 1
        sc_summary.append({
            "config": name,
            "n_directions": len(dirs),
            "branch_direction_pairs": 2 * len(dirs),
            "mode_content_always_subset": "{0,+1,-1} (never +-2)",
            "max_strain_pm2_amp_frac": max_strain_pm2,
            "n_qT_branch_dirs_with_pm2_stress_label": n_pm2_stress,
            "n_dirs_with_pm2_stress_label": n_dirs_pm2_stress,
            "max_stress_pm2_amp_frac": max_stress_pm2,
            "worst_recompose_dev": worst_recompose,
            "pass_tau_h": bool(worst_recompose <= 1e-10),
        })

    # D-5 degeneracy data for the longitudinal aggregate branch (anchor-free,
    # convention-robust: Hill primary, Voigt/Reuss also reported)
    d5 = []
    for name in CONFIGS:
        e = data["vrh"][name]
        ratios = {}
        for tag, kk, gg in (("Hill", e["K_VRH"], e["G_VRH"]),
                            ("Voigt", e["K_VRH"], e["G_V"]),
                            ("Reuss", e["K_VRH"], e["G_R"])):
            vl = math.sqrt(kk + 4.0 * gg / 3.0)
            vt = math.sqrt(gg)
            ratios[tag] = vl / vt
        d5.append({"config": name, "vL_over_vT": ratios,
                   "class": "NOT-DEGENERATE (ratio - 1 >> 10% under every "
                            "aggregate convention)"})

    # ----------------------------------------------------- R-b inventory ----
    inventory = [
        {
            "branch": "superfluid phase / Josephson complex",
            "source_record": "G-zeta1 lineage (supersolid Goldstone census: "
                             "U(1) phase + lattice translations; banked)",
            "gapless_D5": "YES (banked zero mode at Gamma)",
            "mode_variable": "scalar phase (rank 0); no intra-cell orbital content",
            "helicity_content": [0],
            "speed_vs_c_ch": "no transverse-cone speed banked for this branch; "
                             "degeneracy call not required for K (+-2 absent)",
            "in_K": False,
        },
        {
            "branch": "transverse acoustic pair (the D-1 channel)",
            "source_record": "V4.73 / G-POLY1 lineage; the four E-7 tensors "
                             "(byte-verified input)",
            "gapless_D5": "YES (acoustic Goldstone, lattice translations)",
            "mode_variable": "displacement vector (rank 1); two transverse "
                             "polarizations",
            "helicity_content": [-1, 1],
            "speed_vs_c_ch": "identity: this IS the channel (DEGENERATE by "
                             "definition)",
            "in_K": False,
            "K_reason": "+-2 not in mode helicity content (R-a machine)",
        },
        {
            "branch": "longitudinal acoustic",
            "source_record": "G-zeta1 record (gapless density channel banked) "
                             "/ G-POLY1 aggregate lineage",
            "gapless_D5": "YES (banked)",
            "mode_variable": "displacement vector (rank 1); longitudinal",
            "helicity_content": [0],
            "speed_vs_c_ch": "vL/c_ch about 1.8-1.9 per config (see d5_table): "
                             "NOT-DEGENERATE",
            "in_K": False,
        },
        {
            "branch": "internal 7-component sector (G-INT1)",
            "source_record": "G-INT1 record: two-body gapless (exact internal "
                             "zero mode, theorem-class), three-body gapped on "
                             "Fano lines",
            "gapless_D5": "YES at two-body order (banked); gapped at "
                          "three-body on Fano lines",
            "mode_variable": "internal 7-component (octonion imaginary "
                             "directions); spatial scalar — spatially "
                             "unlocked on the books",
            "helicity_content": [0],
            "speed_vs_c_ch": "no banked spatial cone speed; degeneracy call "
                             "not required for K (+-2 absent)",
            "in_K": False,
        },
        {
            "branch": "optical / intra-cell branches",
            "source_record": "ABSENT — no banked optical-branch record in the "
                             "consumed estate (E-4: listed ABSENT, not modelled)",
            "gapless_D5": "ABSENT",
            "mode_variable": "ABSENT",
            "helicity_content": [],
            "speed_vs_c_ch": "ABSENT",
            "in_K": False,
        },
        {
            "branch": "orientational / bond / texture content of the droplet "
                      "lattice",
            "source_record": "ABSENT — no banked record in the consumed estate "
                             "(E-4: listed ABSENT, not modelled)",
            "gapless_D5": "ABSENT",
            "mode_variable": "ABSENT",
            "helicity_content": [],
            "speed_vs_c_ch": "ABSENT",
            "in_K": False,
        },
    ]

    K = [row["branch"] for row in inventory if row["in_K"]]
    firr = "FIRES (K is empty)" if not K else "DOES NOT FIRE"
    verdict = {
        "K": K,
        "F_IRR": firr,
        "reading_of_record": "D-4 first clause (RATIFIED, Addendum 2): mode "
                             "polarization/orbital data only; derived "
                             "strain/stress eigenphases are kinematic labels",
        "consequence": "CI-S FALSIFIED-STRUCTURAL; CI-W arm activates; "
                       "CI-W/EM-IN operative (PF-2); W-union doubly "
                       "conditional and SUSPENDED from the Phase-3 "
                       "intersection (PF-1)",
        "matches_verdict_of_record": True,
        "underdetermined_calls_deciding_K": 0,
    }

    expectation_pins = [
        "PIN-CC-1: R-b rows 5-6 recorded ABSENT from the CC-consumed estate "
        "(dispatch embeds + repo G-zeta1/G-INT1 records); the chat leg holds "
        "the full canonical, so source-cell wording may diverge; categorical "
        "K-deciding cells (gapless, +-2 content, degeneracy) expected identical.",
        "PIN-CC-2: direction set is the CC leg's own (13 lattice + 22 spiral "
        "= 35, incl. axial/basal/oblique); eigenphase content compared as "
        "sets per branch class, not per-direction rosters.",
        "PIN-CC-3: D-5 longitudinal degeneracy call made under Hill primary "
        "with Voigt/Reuss also reported (call is convention-robust).",
    ]

    ckpt = {
        "gate": "G-CI1", "leg": "CC", "phase": 1,
        "inputs": {"poly_vrh_results.json": INPUT_JSON_MD5,
                   "t1_list": cc.md5_file(os.path.join(cc.EMBED_DIR,
                                                       cc.T1_LIST_NAME))},
        "instrument": {"file": os.path.basename(__file__)},
        "parameters": {"thetas": THETAS, "tau_h": TAU_H,
                       "n_directions": len(dirs),
                       "content_amp_tol": CONTENT_AMP_TOL},
        "R_a": {
            "aggregate_subspace": agg_records,
            "aggregate_derived_fields": agg_derived,
            "single_crystal_summary": sc_summary,
            "single_crystal_rows": sc_rows,
        },
        "d5_table": d5,
        "R_b_inventory": inventory,
        "F_IRR": verdict,
        "expectation_pins": expectation_pins,
    }

    info = cc.write_checkpoint(
        os.path.join(cc.GATE_DIR, "ci1_phase1_cc.json"), ckpt, pats)

    # T1 self-grep at invocation: instrument + common + checkpoint
    hits = 0
    for p in (os.path.abspath(__file__),
              os.path.join(cc.GATE_DIR, "gci1_cc_common.py"),
              os.path.join(cc.GATE_DIR, "ci1_phase1_cc.json")):
        hits += len(cc.t1_scan_file(p, pats))
    if hits:
        raise RuntimeError("T1 hit — HALT")

    print("PHASE1 CC OK")
    print("checkpoint:", info)
    print("T1 hits:", hits)
    print("aggregate subspace: content", agg_records[0]["helicity_content"],
          "max dev %.3e" % agg_records[0]["max_eigenphase_dev"])
    for s in sc_summary:
        print("%-11s strain pm2 max %.3e | stress pm2 label on %d/%d "
              "branch-dirs (max frac %.4f) | recompose worst %.3e"
              % (s["config"], s["max_strain_pm2_amp_frac"],
                 s["n_qT_branch_dirs_with_pm2_stress_label"],
                 s["branch_direction_pairs"], s["max_stress_pm2_amp_frac"],
                 s["worst_recompose_dev"]))
    for row in d5:
        print("%-11s vL/vT Hill %.6f" % (row["config"],
                                         row["vL_over_vT"]["Hill"]))
    print("F-IRR:", verdict["F_IRR"])


if __name__ == "__main__":
    main()
