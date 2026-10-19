"""
make_crosscheck2_json.py -- build crosscheck.json (round 2) from xc2_checks.json (this cross-check)
and ../results.json (the original E0).  Agreement flags are computed by comparing the two files.

Run after xc2_e0.py:   python3 make_crosscheck2_json.py
"""
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
xc = json.load(open(os.path.join(HERE, "xc2_checks.json")))
orig = json.load(open(os.path.join(HERE, "..", "results.json")))
X, O = xc["values"], orig["values"]
xok = {c["name"]: c["ok"] for c in xc["checks"]}
ook = {c["name"]: c["ok"] for c in orig["checks"]}


def xpass(prefix):
    hits = [ok for n, ok in xok.items() if n.startswith(prefix)]
    assert hits, prefix
    return all(hits)


def opass(prefix):
    hits = [ok for n, ok in ook.items() if n.startswith(prefix)]
    assert hits, prefix
    return all(hits)


rows = []


def row(q, o, r, agree, note=""):
    rows.append({"quantity": q, "original": o, "recomputed": r, "agree": bool(agree), "note": note})


row("hexagon_check.py printed lines reproduced", f"{O['replica']['identical']}/{O['replica']['lines_original']} identical",
    f"{X['replica']['identical']}/{X['replica']['lines_xc2']} identical",
    O["replica"]["identical"] == X["replica"]["identical"] == 25,
    "lines rebuilt from my own exact values, compared with a fresh run of seed/hexagon_check.py")
row("120 deg Weyl turn on the seven points", "x -> 4x (C^-1 D C = D^4)", "x -> 4x (C^-1 D C = D^4; the 240 deg turn gives x -> 2x)",
    xpass("the 120 deg turn theta -> roll(theta) sends point 1 to point 4") and xpass("C^-1 D C = D^4")
    and O["weyl"]["SU(3)"]["turns"] == X["weyl"]["SU(3)"]["turns"], "")
row("finer lattice Lambda + Zp", "hexagonal, Gram (1/7)[[2,-1],[-1,2]], index 7, 6 shortest vectors",
    "minimal norm^2 2/7 attained by exactly 6 vectors; covolume 1/7 (index 7); reduced Gram (1/7)[[2,1],[1,2]] = hexagonal",
    xpass("Lambda + Zp: minimal norm^2 2/7") and xpass("Lambda + Zp = Z p + Z (0,1)") and xpass("a reduced basis (a, c)"),
    "Gram computed in integer Lambda coordinates by enumeration, not from the original's basis (p, tp)")
t_o, t_x = O["triangulation"], X["triangulation"]
row("torus triangulation V - E + F", f"{t_o['V']} - {t_o['E']} + {t_o['F']} = {t_o['chi']}",
    f"{t_x['V']} - {t_x['E']} + {t_x['F']} = {t_x['chi']}; 6-cycle links; orientable",
    all(t_o[k] == t_x[k] for k in ("V", "E", "F", "chi")) and xpass("every vertex link") and xpass("orientable: with the plane"), "")
row("K7, two Fano families, octonion lines", f"K7; 2 Fano families; '{t_o['octonion_family']}' family = {{i,i+1,i+3}}",
    f"K7; 2 Fano families; '{t_x['octonion_family']}' family = {{i,i+1,i+3}}, other = {{i,i+2,i+3}}",
    xpass("the six shortest vectors carry labels 1..6") and xpass("both families are Fano planes"),
    "'up'/'down' naming is a convention; my reduced basis has labels (4,6) where the original uses (1,5), and both make 'down' the octonion family")
row("Fano planes on Z7 fixed by x -> x+1", f"{O['fano']['cyclic']} of {O['fano']['total']}; = the two torus families",
    f"{X['fano']['cyclic']} of {X['fano']['total']} (Steiner-triple-system backtracking); = the two torus families",
    O["fano"] == X["fano"], "collineation groups 168, 168, intersection 21 in both")
g = X["group_orders"]
row("order of <D, 120 deg turn> in SU(3)", "21 (BFS closure; exact unitary, det 1)",
    f"{g['F21']} (projective orbit-stabiliser chain, orbit sizes {g['orbit_sizes']['F21']}); enumeration also 21, all in SU(3)",
    g["F21"] == 21 and opass("|<D, C>| = 21"), "")
row("orders of Klein's copy and flipped copy of PSL(2,7) in SU(3)", "168, 168",
    f"{g['Klein_copy']}, {g['flipped_copy']} (orbit sizes {g['orbit_sizes']['Klein_copy']}); explicit isomorphisms onto PSL(2,F7)",
    g["Klein_copy"] == g["flipped_copy"] == 168, "flipped copy = flip (Klein) flip^-1 = LNR's <A,B> as sets in both")
row("quartic invariants (exact)", "Klein copy keeps x^3y+y^3z+z^3x; flipped copy keeps xy^3+yz^3+zx^3 (all 168)",
    "same, exact polynomial identities under the generators and all 168 elements",
    xpass("Klein quartic x^3y+y^3z+z^3x is invariant") and xpass("mirror quartic xy^3+yz^3+zx^3 is invariant"), "")
mo = sorted([m["order"], m["conjugates"]] for m in O["PSL27_subgroups"]["maximal_classes"])
mx = X["PSL27_subgroups"]["maximal_classes"]
row("maximal subgroups of PSL(2,7) (order x conjugates)", ", ".join(f"{b} x {a}" for a, b in mo),
    ", ".join(f"{b} x {a}" for a, b in mx) + f"; {X['PSL27_subgroups']['total']} subgroups in {X['PSL27_subgroups']['conjugacy_classes']} classes (completeness proven by join closure)",
    mo == mx and O["PSL27_subgroups"]["by_order"] == X["PSL27_subgroups"]["by_order"]
    and O["PSL27_subgroups"]["total"] == X["PSL27_subgroups"]["total"], "")
row("PSL(2,7) triplet character on 1A,2A,3A,4A,7A,7B", f"{', '.join(O['PSL27_triplet_character']['chi'])}; FS {O['PSL27_triplet_character']['frobenius_schur']}",
    f"{', '.join(X['PSL27_triplet_character']['chi'])}; FS {X['PSL27_triplet_character']['frobenius_schur']} (both copies; classes via the PSL(2,F7) image)",
    O["PSL27_triplet_character"] == X["PSL27_triplet_character"], "")
row("F21 triplet character on 1A,3A,3B,7A,7B", f"{', '.join(O['F21_triplet_character']['chi'])}; FS {O['F21_triplet_character']['frobenius_schur']}",
    f"{', '.join(X['F21_triplet_character']['chi'])}; FS {X['F21_triplet_character']['frobenius_schur']}",
    O["F21_triplet_character"] == X["F21_triplet_character"], "chi(D) = b7 exactly in both")
row("A5 triplet characters on 1A,2A,3A,5A,5B", f"{', '.join(O['A5_triplet_character']['chi'])}; FS +{O['A5_triplet_character']['frobenius_schur']}",
    f"{', '.join(X['A5_triplet_character']['chi'])}; FS +{X['A5_triplet_character']['frobenius_schur']} for both triplets (icosahedral group found by brute force)",
    O["A5_triplet_character"] == X["A5_triplet_character"], "")
wo, wx = O["weyl"], X["weyl"]
row("Weyl(SU(3)) and Weyl(G2) on the seven points",
    f"orders {wo['SU(3)']['order']}, {wo['G2']['order']}; mirrors keeping points {wo['SU(3)']['mirrors_keeping_points']}/{wo['SU(3)']['mirrors']}, {wo['G2']['mirrors_keeping_points']}/{wo['G2']['mirrors']}",
    f"orders {wx['SU(3)']['order']}, {wx['G2']['order']}; mirrors keeping points {wx['SU(3)']['mirrors_keeping_points']}/{wx['SU(3)']['mirrors']}, {wx['G2']['mirrors_keeping_points']}/{wx['G2']['mirrors']}; W(G2) = Aut(Lambda)",
    all(wo[k][f] == wx[k][f] for k in ("SU(3)", "G2") for f in ("order", "mirrors", "mirrors_keeping_points", "turns")),
    "turn list identical: 60/180/300 deg = x -> 5x, 6x, 3x, swap the families")
ao = Counter((c["rotation_order"], c["mirrors_through"]) for c in O["affine_weyl"]["G2"]["site_pattern"])
ax_ = Counter()
for k, v in X["affine_weyl"]["G2"]["site_pattern"].items():
    r, m, _ = eval(k)
    ax_[(r, m)] += v
ao3 = Counter((c["rotation_order"], c["mirrors_through"]) for c in O["affine_weyl"]["SU3"]["site_pattern"])
ax3 = Counter()
for k, v in X["affine_weyl"]["SU3"]["site_pattern"].items():
    r, m, _ = eval(k)
    ax3[(r, m)] += v
row("G2 affine Weyl group", f"Coxeter {tuple(O['affine_weyl']['G2']['coxeter'])}; sites {dict(ao)}; p6m (SU(3): p3m1)",
    f"Coxeter {tuple(X['affine_weyl']['G2']['coxeter'])} with my own base (a1 = e2 - (1,1,1)/3, theta = (1,0,-1)); sites {dict(ax_)}; p6m (SU(3): {dict(ax3)}, p3m1)",
    O["affine_weyl"]["G2"]["coxeter"] == X["affine_weyl"]["G2"]["coxeter"] and ao == ax_ and ao3 == ax3,
    "site pattern from the fixed-point equation (1 - w) x = t mod Lambda (the same idea as the original; the round-1 cross-check used a grid search)")
uo, ux = O["torus7_uniqueness"], X["torus7_uniqueness"]
row("7-vertex torus triangulations / automorphisms", f"{uo['orbit']} labelled, one orbit; |Aut| = {uo['aut_order']}, {uo['orientation_preserving']} orientation-preserving",
    f"{ux['orbit']} labelled, one orbit; |Aut| = {ux['aut_order']} = AGL(1,7), {ux['orientation_preserving']} orientation-preserving",
    uo["degree2_complexes"] == ux["complexes"] and uo["orbit"] == ux["orbit"] and uo["aut_order"] == ux["aut_order"]
    and uo["orientation_preserving"] == ux["orientation_preserving"], "the search covers chi = 0 complexes only (see issue 1)")
row("Der(O) / stabiliser of an imaginary unit", f"dim {O['octonions']['der_dim']} / dim {O['octonions']['stabiliser_dim']}",
    f"dim {X['octonions']['der_dim']} / dim {X['octonions']['stabiliser_dim']} (Cayley-Dickson model; compact, rank <= 2)",
    O["octonions"]["der_dim"] == X["octonions"]["der_dim"] and O["octonions"]["stabiliser_dim"] == X["octonions"]["stabiliser_dim"], "")
row("<PSL(2,7), complex conjugation> inside G2", f"order {O['octonions']['PGL27_in_G2_order']} = PGL(2,7); swaps S4 classes and Fano families",
    f"order {X['PGL27']['order']}; kappa transported to P^1(F7) is a Moebius map of non-square determinant, so the group IS PGL(2,F7); swaps the S4 classes; S4 classes give the families {X['PGL27']['S4_class_families']}",
    O["octonions"]["PGL27_in_G2_order"] == X["PGL27"]["order"] == 336 and X["PGL27"]["kappa_swaps_S4_classes"], "")
po, px = O["order7_points_with_hexagonal_finer_lattice"], X["order7_points_with_hexagonal_finer_lattice"]
row("order-7 torus points with a hexagonal finer lattice", f"{po['value']} of {po['of']} ({po['subgroups']} subgroups)",
    f"{px['value']} of {px['of']} ({px['subgroups']} subgroups: D's and diag(z,z^4,z^2)'s)", po == px, "")

claim_audit = [
    {"claim": "All 102 exact checks pass; 25/25 hexagon_check.py lines reproduced exactly", "verdict": "supported",
     "note": "Rerun of e0_exact.py in a scratch copy: 102/102, exit 0, 4.1 s. results.json identical apart from runtimes; replica files and the figure byte-identical. My own 25 lines also match."},
    {"claim": "Group orders 21, 168, 168 (exact)", "verdict": "supported",
     "note": "Recomputed by a projective orbit-stabiliser chain (orbit sizes 3x7 and 24x7), with no full enumeration, and confirmed by enumeration."},
    {"claim": "Characters: PSL(2,7) (3,-1,0,1,b7,b7bar), F21 (3,0,0,b7,b7bar) with FS 0; A5 (3,-1,0,(1±sqrt5)/2) with FS +1", "verdict": "supported",
     "note": "Recomputed exactly. Classes come from an explicit isomorphism onto PSL(2,F7); A5 comes from a brute-force icosahedral group."},
    {"claim": "Maximal subgroups 8 x 21, 7 x 24, 7 x 24; 179 subgroups in 15 classes", "verdict": "supported",
     "note": "Recomputed. The original assumes 'all subgroups are 2-generated' (stated only in a code comment); my join-closure check proves that the list of 179 is complete."},
    {"claim": "Weyl groups: orders 6, 12; turns x->4x, 2x keep the families; 60/180/300 deg = 5x, 6x, 3x swap them; no mirror keeps the seven points", "verdict": "supported",
     "note": "Recomputed in integer Lambda coordinates; also W(G2) = Aut(Lambda)."},
    {"claim": "G2 affine Weyl group = p6m (sites 1a 6mm, 2b 3m, 3c 2mm); SU(3)'s = p3m1", "verdict": "supported",
     "note": "Recomputed with an independent G2 base. The Coxeter (2,3,6) relations hold, W_aff = Lambda x| W(G2), and the site pattern matches."},
    {"claim": "Finding 6: the 7-vertex torus triangulation is unique (120 labelled, one orbit) and chiral (Aut = AGL(1,7), all 42 orientation-preserving)", "verdict": "supported",
     "note": "Recomputed. Wording slip: the check title says 'every 7-vertex triangulated closed surface is an orientable torus', which is false (issue 1)."},
    {"claim": "Finding 7: only 12 of the 48 order-7 torus points give a hexagonal finer lattice", "verdict": "supported", "note": "Recomputed with Gauss reduction."},
    {"claim": "Finding 8: <flipped PSL(2,7), kappa> = PGL(2,7) of order 336 inside G2; kappa swaps the S4 classes and the families; S4 classes = Fano families", "verdict": "supported",
     "note": "Recomputed. I identified the group explicitly with PGL(2,F7) on P^1(F7), which removes the citation |Aut PSL(2,7)| = 336."},
    {"claim": "Finding 8: the PSL(2,7) in U(3) containing <D,C> is unique", "verdict": "supported",
     "note": "The report gives only a sketch and uses LNR for 'the only triplets are 3 and 3bar'. I computed the missing pieces (|Aut F21| = 42, all induced by N_PGL(F21); the degree equation forces irrep degrees 1,3,3,6,7,8) and the argument closes; see CROSSCHECK.md."},
    {"claim": "Finding 9 / extra: Der(O) = g2 (dim 14), stabiliser of e = su(3) (dim 8); D, C, Rf, Dk, R, kappa are octonion automorphisms", "verdict": "supported",
     "note": "Recomputed in the Cayley-Dickson model, and the report's C + C^3 model was rechecked over Q(i). The original's real basis uses G = i sqrt7 rather than i; that is legitimate."},
    {"claim": "Calibration rows marked CALIBRATED for targets sourced to SEED §3", "verdict": "overstated",
     "note": "PLAN §1 reserves CALIBRATED for literature targets; these are seed claims and should read CONFIRMED (issue 2). The numbers are right."},
    {"claim": "AMENDED: 'they don't stack into one clean tower'", "verdict": "overstated",
     "note": "The math of the amendment is right, but every factual clause of the seed sentence holds, and kappa, hence PGL(2,7), swaps the families exactly as the seed says G2's turns do. This is an interpretive refinement, not a correction (issue 3)."},
    {"claim": "Maximal-subgroup target sourced 'ATLAS; LNR §5 [read]'", "verdict": "overstated",
     "note": "LNR §5 names only the two isomorphism types (S4, Z7 x| Z3). The two S4 classes come from ATLAS, which was not read (issue 4). The computation itself establishes the two classes."},
    {"claim": "Background claims ('SU(3) is the color group', 'model-builders used both groups') marked CONFIRMED in results.json", "verdict": "overstated",
     "note": "Not tested by E0. The REPORT body already says 'CONFIRMED with a cited part' (issue 5)."},
    {"claim": "LNR citations [read]: eq. 13 (b7), eqs. 16/22/23 (A = Rf, AB = D), eq. 78 (mirror quartic), §2 (A5: five real irreps, two triplets), §5 (F21 table)", "verdict": "supported",
     "note": "I checked each in the arXiv:0709.1447v2 text and rebuilt A and B from eqs. 22-23 myself."},
    {"claim": "Figure fig_torus_p6m.png shows the two families and the p6m pattern", "verdict": "supported",
     "note": "The file exists (163,640 bytes) and reproduces byte for byte. Point labels sit at (j/7, 3j/7) and the blue triangles are {i,i+1,i+3}."},
]

issues = [
    {"severity": "minor",
     "description": "results.json check B ('exhaustive search: every 7-vertex triangulated closed surface is an orientable torus ...') and REPORT Method item 3 overstate the search. It covers only complexes in which each vertex pair lies in exactly 2 triangles, i.e. chi = 0. 7-vertex triangulations of the sphere (pentagonal bipyramid) and of RP^2 exist (xc2_e0.py builds both). The numbers 120, one orbit and |Aut| = 42 are correct. The round-1 cross-check reported the same issue, and the rerun left it unfixed.",
     "suggested_fix": "Reword as 'every 7-vertex triangulated surface with chi = 0 is an orientable torus (so no 7-vertex Klein bottle exists), and all are relabellings of ours'."},
    {"severity": "minor",
     "description": "The calibration table and headline list use CALIBRATED for rows whose target source is 'SEED §3' (x -> 4x, |<D,C>| = 21, the Weyl turns, and others). PLAN §1 defines CALIBRATED as reproducing a literature target; these are seed claims, and seed_claims already lists them as CONFIRMED. Unfixed since round 1.",
     "suggested_fix": "Mark seed-sourced rows CONFIRMED. Keep CALIBRATED for rows with a literature target (LNR characters, ATLAS maxima, A5 reality, p6m)."},
    {"severity": "minor",
     "description": "The AMENDED verdict on 'they don't stack into one clean tower' amends an interpretation, not a fact. Every factual clause of the seed sentence is confirmed. The proposed chain G2 ⊃ SU(3)⋊Z2 ⊃ PGL(2,7) ⊃ PSL(2,7) ⊃ F21 is correct and verified here, but its top steps (kappa, PGL(2,7)) swap the Fano families, which is the seed's point.",
     "suggested_fix": "Record it as 'facts CONFIRMED; suggested wording refinement'. Keep the chain and state that the family split survives only up to PSL(2,7)."},
    {"severity": "minor",
     "description": "Citation: the maximal-subgroup target 'S4, S4, 7:3' is sourced as 'ATLAS; LNR §5 [read]'. LNR §5 gives only the isomorphism types. The two conjugacy classes of S4 rest on ATLAS, which was not read (results.json says 'via SEED §9').",
     "suggested_fix": "Source the two-class statement to ATLAS [summary/via SEED] and to the computation itself."},
    {"severity": "minor",
     "description": "results.json gives a plain CONFIRMED to background and literature claims that E0 does not test ('SU(3) is the color group', 'model-builders used both groups'). The REPORT body correctly says 'CONFIRMED with a cited part'.",
     "suggested_fix": "Use 'not tested (cited)' or 'CONFIRMED (cited)' consistently in results.json."},
    {"severity": "minor",
     "description": "Unstated assumptions in the original code, none of which changes a result: the subgroup lattice enumerates only 2-generated subgroups (completeness assumed in a comment); PSL(2,7) is identified by 'simple of order 168'; Aut(PSL(2,7)) = PGL(2,7) by the order 336; and the Finding 8 uniqueness relies on LNR's character table. This cross-check supplies each one by computation (join closure, explicit isomorphisms onto PSL(2,F7) and PGL(2,F7), |Aut F21| = 42 and the degree equation).",
     "suggested_fix": "Optional: cite the cross-check, or add a short completeness argument to the Limitations section."},
]

out = {
    "experiment": "E0_hexagon_exact",
    "round": 2,
    "crosscheck_script": "xc2_e0.py",
    "n_checks": xc["n_checks"], "n_pass": xc["n_pass"], "runtime_seconds": xc["runtime_seconds"],
    "original_rerun": {"n_checks": 102, "n_pass": 102, "runtime_seconds": 4.1,
                       "results_json_identical_except_runtime": True, "replica_files_identical": True, "figure_byte_identical": True},
    "round1_crosscheck_rerun": {"script": "xc_e0.py", "n_checks": 81, "n_pass": 81},
    "independent_values": rows,
    "all_agree": all(r["agree"] for r in rows),
    "claim_audit": claim_audit,
    "issues": issues,
    "overall": "confirmed_with_corrections",
    "summary": "All 19 headline quantities agree exactly; no headline number or seed verdict is wrong. The six issues are minor: wording, verdict vocabulary, one citation and undocumented assumptions.",
}
with open(os.path.join(HERE, "crosscheck.json"), "w") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
print("wrote crosscheck.json;", len(rows), "quantities; all agree:", out["all_agree"])
for r in rows:
    print(("  ok  " if r["agree"] else "  XX  ") + r["quantity"])
