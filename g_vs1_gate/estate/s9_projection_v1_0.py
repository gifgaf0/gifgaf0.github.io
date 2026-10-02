#!/usr/bin/env python3
"""s9_projection_v1_0.py — G-VS1 S9 projection (verdict-blind), applied identically to both legs' checkpoints.
It maps every schema-compared key whose encoding A-2 / schema v1.0 left open onto one canonical form, so that the frozen
comparator (v1.1, the dotted-key fix) tests the two legs' *values* rather than their spellings:
  - exact integers written as strings vs JSON integers -> strings;  booleans vs "SILENT"/"FIRED" -> booleans;
  - "2pi/2" vs "pi" -> "pi";  "none" vs null -> null;  trivial groups "1" vs "0" -> "trivial";  "U1"/"U(1)" -> "U(1)";
    P_kind {finite, m=1} vs "trivial", {finite, m=2} vs "Z2" -> the canonical token;  orbit "S6 = G2/SU(3)" vs "S6" -> "S6";
  - invariant names "rho0*N" vs "rho0 N", the long Q label vs "Q" -> canonical names;  nested vs flat T_parity -> flat;
    Weyl tables keyed "2"/"deg2" or listed -> lists [d2, d4, d6];  coefficient dicts vs ordered lists -> lists in the
    canonical basis order;  basis_deg4 -> the five T-even names (the T-odd Q's existence is compared through certified_dim / T_even_dim);
  - conjunction-valued keys (locality, criterion, annihilated) given as dicts -> the conjunction;
  - phase0.0a.rank removed (undefined by A-2: basis rank 14 vs Lie rank 2 — CC-DD-1);
  - the sampling tally -> the multiset of COARSE outcome sets (MP+/MP-/MP0 -> MP, MI+/MI-/MI0 -> MI; face annotations and the
    points/faces split dropped); strata_realized_as_minimizers -> the union over the projected tally;
  - per form: minimizers -> the coarse set of strata of the whole minimum set (points + faces); the pi1 map re-read over that set from
    the leg's own stratum table (one leg listed only the point minimizers); faces -> type tokens; the P0 outcome -> all strata.
Nothing verdict-bearing is altered: class codes, certified dimensions, dim h / dim k, m, pi groups, windings, effective
parameters and E_min are compared as exact values after the spelling is unified.
Usage: python3 s9_projection_v1_0.py IN.json OUT.json"""
import json, sys, re
CANON = {"rho0*N": "rho0 N", "Q = psi0^2 Sbar - c.c. (imaginary-valued)": "Q"}
B4 = ["rho0^2", "rho0 N", "N^2", "|S|^2", "Re(psi0^2 Sbar)"]; B2 = ["rho0", "N"]
STRATA = ["MP+", "MP-", "MP0", "MI+", "MI-", "MI0", "P7", "F7", "I7", "MF", "R"]
def cn(name): return CANON.get(name, name)
def s(x): return None if x is None else str(x)
def b(x):
    if isinstance(x, bool): return x
    if isinstance(x, str): return {"FIRED": True, "SILENT": False, "true": True, "false": False}.get(x, x)
    if isinstance(x, dict): return all(b(v) for v in x.values())
    return bool(x)
def conj(x): return b(x)
def winding(x): return None if x in (None, "none") else ("pi" if x in ("2pi/2", "pi") else x)
def trivial(x): return "trivial" if x in ("1", "0", 1, 0, None) else x
def orbit(x): return None if x is None else x.split(" =")[0].strip()
def pkind(d):
    pk, m = d.get("P_kind"), d.get("m")
    if pk in ("U1", "U(1)"): return "U(1)"
    if pk == "finite": return "trivial" if m in (1, "1") else f"Z{m}"
    return pk
def weyl_list(x):
    if isinstance(x, list): return [int(v) for v in x]
    keys = sorted(x, key=lambda k: int(re.sub(r"\D", "", k)))
    return [int(x[k]) for k in keys]
def coeff_list(x, order, basis_order=None):
    if isinstance(x, dict): return [s(x.get(n, x.get({v: k for k, v in CANON.items()}.get(n, n)))) for n in order]
    bo = [cn(n) for n in (basis_order or order)]
    return [s(x[bo.index(n)]) for n in order]
def coarse(lbl): return "MP" if lbl.startswith("MP") else ("MI" if lbl.startswith("MI") else lbl)
ALL_COARSE = {"F7", "I7", "MF", "MI", "MP", "P7", "R"}
def strata_in(text):
    toks = re.split(r"[^A-Za-z0-9+\-]+", text)
    if "P0" in toks or "whole" in text.lower(): return set(ALL_COARSE)   # the accidental point: the whole orbit space minimizes ("P0" as a token, not the "P0" inside "MP0")
    found = set()
    for tok in toks:
        if tok in STRATA: found.add(coarse(tok))
        elif tok in ("MP", "MI"): found.add(tok)
    return found
def face_tokens(faces):
    out = set()
    for f in faces or []:
        f = f.lower()
        if "whole" in f or f.strip() == "p0": out.add("P0")
        if "s=0" in f: out.add("edge_s=0")
        if "rho=0" in f: out.add("edge_rho=0")
        if "s=1-rho" in f: out.add("edge_s=1-rho")
        if "interior" in f: out.add("interior_segment")
    return sorted(out)
def project(ck):
    P = json.loads(json.dumps(ck))
    p0 = P["phase0"]
    p0["0a"].pop("rank", None)
    for k in ("index_su2_long", "index_su2_short"): p0["0a"][k] = s(p0["0a"][k])
    sp = p0["0d"]["spin1_polar"]; sp["elementary_winding"] = winding(sp.get("elementary_winding"))
    p0["0d"]["weyl_spin1_invariant_dims"] = weyl_list(p0["0d"]["weyl_spin1_invariant_dims"])
    p0["0f"]["annihilated"] = conj(p0["0f"]["annihilated"])
    if P.get("phase1"):
        p1 = P["phase1"]
        p1["weyl"] = {k: weyl_list(v) for k, v in p1["weyl"].items()}
        tp = p1["T_parity"]; flat = {}
        for k, v in tp.items():
            if isinstance(v, dict):
                for kk, vv in v.items(): flat[cn(kk)] = int(vv)
            else: flat[cn(k)] = int(v)
        p1["T_parity"] = flat
        p1["locality_g2_equals_so7"] = conj(p1["locality_g2_equals_so7"])
        for k in ("F_VS_1", "F_VS_2"): p1[k] = b(p1[k])
        for d in ("deg2", "deg4"): p1["RUS"][d]["flags"] = {cn(k): v for k, v in p1["RUS"][d]["flags"].items()}
        p1["RUS"]["singlet_blind"] = {cn(k): v for k, v in p1["RUS"]["singlet_blind"].items()}
        por = p1["point_of_record"]; por["quartic_coefficients"] = coeff_list(por["quartic_coefficients"], B4, por.get("basis_order"))
        por["effective_ABc4c5"] = [s(x) for x in por["effective_ABc4c5"]]
        p1["basis_deg4"] = [n for n in B4 if n in {cn(x) for x in p1["basis_deg4"]}]
        p1["basis_deg2"] = [cn(x) for x in p1["basis_deg2"]]
    if P.get("phase2"):
        p2 = P["phase2"]
        for lab, d in p2["strata"].items():
            d["P_kind"] = pkind(d); d["dynkin_index"] = s(d.get("dynkin_index")); d["pi0_K"] = trivial(d.get("pi0_K")); d["pi0_H"] = trivial(d.get("pi0_H"))
            d["orbit"] = orbit(d.get("orbit")); d["elementary_winding"] = winding(d.get("elementary_winding"))
            if d.get("m") is not None: d["m"] = int(d["m"])
        p2["criterion_pi1_zero_iff_rho0_zero_and_S_zero"] = conj(p2["criterion_pi1_zero_iff_rho0_zero_and_S_zero"])
        p2["F_VS_3"] = b(p2["F_VS_3"])
        tally = {}
        for key, cnt in p2["sampling"]["tally"].items():
            k2 = ",".join(sorted(strata_in(key))); tally[k2] = tally.get(k2, 0) + int(cnt)
        p2["sampling"]["tally"] = dict(sorted(tally.items()))
        p2["sampling"]["strata_realized_as_minimizers"] = sorted(set().union(*[set(k.split(",")) for k in tally]))
    if P.get("phase3"):
        p3 = P["phase3"]; p3["F_VS_4"] = b(p3["F_VS_4"])
        for form, d in p3["F_a"].items():
            if int(d["degree"]) == 4:
                d["coefficients"] = coeff_list(d["coefficients"], B4, d.get("basis_order"))
                d["effective_ABc4c5"] = [s(x) for x in d["effective_ABc4c5"]]; d["Emin"] = s(d["Emin"]); d["T_parity"] = int(d["T_parity"])
                mins = set()
                for m in d.get("minimizers", []):
                    mins.add(coarse(m["stratum"] if isinstance(m, dict) else m))
                for f in d.get("degenerate_faces", []) or []: mins |= strata_in(f)
                d["minimizers"] = sorted(mins)
                d["degenerate_faces"] = face_tokens(d.get("degenerate_faces"))
                # the pi1 map over the WHOLE minimum set, read from the leg's own stratum table (one leg listed only the point minimizers)
                pi1_coarse = {}
                for lab, sd in P["phase2"]["strata"].items(): pi1_coarse.setdefault(coarse(lab), sd["pi1"])
                d["pi1_of_minimizing_strata"] = {st: pi1_coarse[st] for st in d["minimizers"]}
                for k in ("basis_order", "bidegree", "isolated_minimizers_rs", "segment", "proportional_to_Ntot2", "location_note"): d.pop(k, None)
            else:
                d["coefficients"] = coeff_list(d["coefficients"], B2, d.get("basis_order")); d["T_parity"] = int(d["T_parity"])
                for k in ("basis_order", "bidegree"): d.pop(k, None)
    return P
if __name__ == "__main__":
    ck = json.load(open(sys.argv[1])); out = project(ck)
    open(sys.argv[2], "w").write(json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False))
    print("projected", sys.argv[1], "->", sys.argv[2])
