"""
make_crosscheck_json.py -- assemble crosscheck.json from this cross-check's own
results (xc_checks.json, written by xc_e0.py) and the original E0 results.json.
Run after xc_e0.py:  python3 make_crosscheck_json.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
xc = json.load(open(os.path.join(HERE, "xc_checks.json")))
orig = json.load(open(os.path.join(HERE, "..", "results.json")))
V = xc["values"]
OH = {h["quantity"]: h for h in orig["headline"]}


def ov(q):
    return OH[q]["value"]


rows = [
    ("hexagon_check.py printed lines reproduced exactly", ov("hexagon_check.py printed lines reproduced exactly"),
     f"{V['replica']['identical']}/{V['replica']['lines_original']} identical (lines rebuilt from the cross-check's own exact values; hexagon_check.py rerun)",
     V["replica"]["identical"] == 25, "independent rebuild; original scripts also rerun in a scratch copy: 102/102, results.json identical up to runtimes"),
    ("120 deg Weyl turn on the seven points", ov("120 deg Weyl turn on the seven points"),
     "x -> 4x (integer matrix [[0,-1],[1,-1]] on Lambda; C^-1 D C = D^4 exactly); 240 deg gives x -> 2x", True, ""),
    ("finer lattice Lambda + Z p", ov("finer lattice Lambda + Z p"),
     f"min norm^2 {V['finer_lattice']['min_norm2']} on {V['finer_lattice']['n_shortest']} vectors, two at 60 deg span L', index 7: hexagonal",
     V["finer_lattice"]["n_shortest"] == 6, "found by lattice enumeration, not from a chosen basis"),
    ("torus triangulation V - E + F", ov("torus triangulation V - E + F"),
     f"{V['triangulation']['V']} - {V['triangulation']['E']} + {V['triangulation']['F']} = {V['triangulation']['chi']}; 6-cycle links; orientable",
     V["triangulation"]["chi"] == 0, ""),
    ("K7, two Fano families, octonion lines", ov("K7, two Fano families, octonion lines"),
     "K7; both families Fano; one = {i,i+1,i+3}, the other {i,i+2,i+3}", True, "family names differ by convention only"),
    ("Fano planes on Z7 fixed by x -> x+1", ov("Fano planes on Z7 fixed by x -> x+1"),
     f"{V['fano']['cyclic']} of {V['fano']['total']} (backtracking; 7!/168 = 30), = the two torus families", V["fano"]["cyclic"] == 2, ""),
    ("|<D, 120 deg turn>| in SU(3)", ov("|<D, 120 deg turn>| in SU(3)"),
     "21: relations exact + Todd-Coxeter on <d,c|d^7,c^3,c^-1dcd^-4> = 21; Schreier-Sims mod 29 and mod 43 = 21",
     True, "different method (presentation + Schreier-Sims vs BFS closure)"),
    ("|Klein's copy| and |flipped copy| in SU(3)", ov("|Klein's copy| and |flipped copy| in SU(3)"),
     "168, 168: LNR relations A^2=B^3=(AB)^7=[A,B]^4=1 exact, Todd-Coxeter = 168, simple quotient; Schreier-Sims mod 29/43 = 168 for <Dk,C,R>, <D,C,Rf>, <A,B>",
     True, "different method"),
    ("quartic invariants (exact polynomial identities)", ov("quartic invariants (exact polynomial identities)"),
     "Klein quartic invariant under Dk, C, R; mirror quartic under D, C, Rf, LNR B (exact expansion; generators suffice)", True, ""),
    ("maximal subgroups of PSL(2,7) (class size x order)", ov("maximal subgroups of PSL(2,7) (class size x order)"),
     f"{V['PSL27_subgroups']['maximal']} (as (order, conjugates)); {V['PSL27_subgroups']['total']} subgroups in {V['PSL27_subgroups']['classes']} classes; F21 maximal also by 2-transitivity on its 8 cosets",
     V["PSL27_subgroups"]["maximal"] == [[21, 8], [24, 7], [24, 7]] or V["PSL27_subgroups"]["maximal"] == [(21, 8), (24, 7), (24, 7)],
     "lattice computed in the faithful degree-8 coset action"),
    ("PSL(2,7) triplet character on 1A,2A,3A,4A,7A,7B", ov("PSL(2,7) triplet character on 1A,2A,3A,4A,7A,7B"),
     "3, -1, 0, 1, b7, b7bar on classes 1, 21, 56, 42, 24, 24; FS 0 (both copies)", True, "classes from mod-29 permutation image, traces exact"),
    ("F21 triplet character on 1A,3A,3B,7A,7B", ov("F21 triplet character on 1A,3A,3B,7A,7B"),
     "3, 0, 0, b7, b7bar on classes 1, 7, 7, 3, 3; FS 0", True, ""),
    ("A5 triplet characters on 1A,2A,3A,5A,5B", ov("A5 triplet characters on 1A,2A,3A,5A,5B"),
     "3, -1, 0, (1 +- sqrt5)/2; FS +1 for both triplets; other degrees forced (4,5)", True,
     "different generators (72 deg about a vertex + 2-fold about z)"),
    ("Weyl(SU(3)) and Weyl(G2) on the seven points", ov("Weyl(SU(3)) and Weyl(G2) on the seven points"),
     "; ".join(V["weyl"]["SU(3)"]["turns"] + V["weyl"]["G2"]["turns"][1::2]) + f"; mirrors keeping points {V['weyl']['SU(3)']['mirrors_keeping']}/{V['weyl']['SU(3)']['mirrors']}, {V['weyl']['G2']['mirrors_keeping']}/{V['weyl']['G2']['mirrors']}",
     True, "integer 2x2 matrices on Lambda"),
    ("G2 affine Weyl group", ov("G2 affine Weyl group"),
     f"Coxeter {V['affine_weyl']['G2']['coxeter']} = (6,3,2); Lambda x| W(G2); sites {V['affine_weyl']['G2']['sites']} ((rot, mirrors): count) = 1x6mm, 2x3m, 3x2mm: p6m; SU(3): 3x3m = p3m1",
     True, "own base (alpha1 = (-2,1,1)/3, theta = (0,-1,1)); exhaustive 1/12-grid site search"),
    ("7-vertex torus triangulations (labelled) / automorphisms", ov("7-vertex torus triangulations (labelled) / automorphisms"),
     f"{V['torus7']['designs']} simple 2-(7,3,2) designs, all surfaces, all orientable, one orbit; |Aut| {V['torus7']['aut']}, {V['torus7']['aut_orientation_preserving']} orientation-preserving",
     V["torus7"]["designs"] == 120 and V["torus7"]["aut"] == 42, "the check TITLE in results.json over-generalises (see issues)"),
    ("Der(O) / stabiliser of an imaginary unit", ov("Der(O) / stabiliser of an imaginary unit"),
     f"dim {V['octonions']['der_dim']} / dim {V['octonions']['stab_dim']}", V["octonions"]["der_dim"] == 14 and V["octonions"]["stab_dim"] == 8,
     "Fano-table (Cayley-Graves) octonions, a different model from the original's C + C^3"),
    ("<PSL(2,7), complex conjugation> inside G2", ov("<PSL(2,7), complex conjugation> inside G2"),
     "kappa in Aut(O) (exact); conj(B) in flipped copy; conj(D) = D^6 not conjugate to D (outer) -> PSL(2,7) x| Z2 = PGL(2,7), order 336; kappa swaps the S4 classes",
     True, "order from the outer-automorphism argument, not by closure"),
    ("order-7 torus points with a hexagonal finer lattice", ov("order-7 torus points with a hexagonal finer lattice"),
     f"{V['order7_hex']['points']} of {V['order7_hex']['of']} ({V['order7_hex']['subgroups']} subgroups: those of D and of diag(z,z^4,z^2))",
     V["order7_hex"]["points"] == 12, "Lagrange-Gauss reduction"),
]
independent_values = [dict(quantity=q, original=o, recomputed=r, agree=bool(a), note=n) for q, o, r, a, n in rows]

issues = [
    dict(severity="minor",
         description="results.json check title (and REPORT Method item 3) says 'every 7-vertex triangulated closed surface is an orientable torus'. "
                     "That is false as worded: a pentagonal bipyramid (sphere, chi 2) and a 7-vertex RP^2 (chi 1) exist (checked in xc_e0.py). "
                     "The search only covered complexes with every pair in exactly two triangles, i.e. chi = 0 / K7 1-skeleton. The numbers (120, one orbit, |Aut| 42) are right.",
         suggested_fix="Reword to 'every 7-vertex triangulated surface with chi = 0 (equivalently, every vertex pair in exactly two triangles) is the torus, unique up to relabelling (120 labelled copies)'."),
    dict(severity="minor",
         description="The AMENDED verdict on the closing tower sentence amends an interpretive judgment ('they don't stack into one clean tower'), not a fact. Every factual clause of that sentence holds as written: "
                     "the Fano split belongs to the SU(3) rung, and the G2 turns that complete p6m swap the families (kappa, and hence PGL(2,7), swaps them too). "
                     "The PGL(2,7) chain behind the amendment is verified correct.",
         suggested_fix="Record it as 'facts CONFIRMED; wording AMENDED (interpretive)'. Keep the suggested chain G2 > SU(3):2 > PGL(2,7) > PSL(2,7) > F21 and state that the family split survives only up to PSL(2,7)."),
    dict(severity="minor",
         description="The calibration table and results.json headlines mark seed-sourced items CALIBRATED (target source 'SEED §3', e.g. |<D,C>| = 21, x -> 4x, the Weyl turns). "
                     "PLAN §1 reserves CALIBRATED for literature targets; reproducing a seed claim is CONFIRMED. The same facts already appear as CONFIRMED in seed_claims, so each is labelled twice.",
         suggested_fix="Keep CALIBRATED only for rows with a literature target (LNR characters and quartic, ATLAS maximal subgroups, the p6m classification). Relabel the SEED §3 rows CONFIRMED."),
    dict(severity="minor",
         description="The maximal-subgroup target 'S4, S4, 7:3' is attributed to 'ATLAS p.3 (via SEED §9); LNR §5 [read]'. LNR §5 gives only the two isomorphism types "
                     "('two maximal subgroups, S4 ... and ... Z7 x| Z3'), not the two conjugacy classes of S4. The two-class statement rests on ATLAS, which was not read. "
                     "The computation itself establishes the two classes, so no result is affected.",
         suggested_fix="Cite as 'ATLAS (not read; via SEED §9); LNR §5 [read] for the isomorphism types'."),
    dict(severity="minor",
         description="In results.json seed_claims, background and literature-only statements ('SU(3) is the color group...', 'flavor model-builders have used both groups') are marked CONFIRMED although nothing was tested. "
                     "The REPORT body separates them correctly as 'CONFIRMED with a cited part'.",
         suggested_fix="Mark them 'CONFIRMED (cited, not computed)' or 'not tested' in results.json to match the report."),
]

claim_audit = [
    dict(claim="All 102 exact checks pass; hexagon_check.py's 25 lines reproduce identically", verdict="supported",
         note="Original rerun in a scratch copy: 102/102, results.json identical except runtimes. The cross-check independently rebuilds the 25 lines: 25/25."),
    dict(claim="|<D,C>| = 21, |Klein's copy| = |flipped copy| = 168, all in SU(3)", verdict="supported",
         note="Todd-Coxeter + exact relations, and Schreier-Sims mod 29 and 43. Generators exactly unitary with det 1."),
    dict(claim="Quartics invariant as exact polynomial identities", verdict="supported", note="Exact expansion for the generators, which is sufficient."),
    dict(claim="PSL(2,7)/F21 triplets complex (FS 0, b7 = (-1+i sqrt7)/2); A5 triplets real (FS +1)", verdict="supported",
         note="Recomputed from mod-p classes and exact traces; A5 rebuilt from different generators."),
    dict(claim="Flipped copy = LNR's published basis (A = Rf, AB = D, same 168 matrices)", verdict="supported",
         note="The cross-checker read LNR eqs. (16), (22), (23) from arXiv:0709.1447v2: the relations hold exactly, A = Rf, AB = D, and C is a word in A, B."),
    dict(claim="Klein's own matrices contain diag(z^4,z^2,z), not D (labelling convention)", verdict="supported",
         note="Every group keeping x^3y+y^3z+z^3x has only powers of Dk among its diagonal elements, and D does not keep it. "
              "The one assumption left is that Klein's quartic is x^3y+y^3z+z^3x in Klein's coordinates; his 1878 paper was not read. "
              "LNR also call their A (= Rf) 'Klein's involution', which supports the labelling-convention reading."),
    dict(claim="Maximal subgroups 7 S4 + 7 S4 + 8 (7:3); F21 maximal; N(F21) = F21; 179 subgroups in 15 classes", verdict="supported",
         note="Subgroup lattice in the degree-8 action; maximality also via 2-transitivity. The citation nuance is listed in the issues."),
    dict(claim="G2 affine Weyl group = p6m (sites 6mm + 2x3m + 3x2mm); SU(3)'s = p3m1", verdict="supported",
         note="Own base, Coxeter orders, translation lattice argument, exhaustive site search."),
    dict(claim="Weyl orders 6, 12; turns x->4x,2x keep the families; 60/180/300 = x->5x,6x,3x swap them; no mirror keeps the seven points", verdict="supported",
         note="Integer matrices on Lambda."),
    dict(claim="The 7-vertex torus triangulation is unique (120 labelled) and chiral (|Aut| = 42, all orientation-preserving)", verdict="supported",
         note="Independent backtracking gives the same numbers."),
    dict(claim="Check title: 'every 7-vertex triangulated closed surface is an orientable torus'", verdict="wrong",
         note="Wording only: 7-vertex triangulations of S^2 and RP^2 exist. The search was restricted to chi = 0."),
    dict(claim="12 of 48 order-7 torus points give a hexagonal finer lattice (2 subgroups, swapped by SU(3) mirrors)", verdict="supported", note=""),
    dict(claim="Der(O) dim 14 (g2), stabiliser of e dim 8 (su(3)); D, C, R, Rf, Dk and kappa are octonion automorphisms", verdict="supported",
         note="Der recomputed in the Fano-table model. The C + C^3 product was checked symbolically to be a unital composition algebra."),
    dict(claim="<flipped PSL(2,7), kappa> = PGL(2,7) of order 336 inside G2; kappa swaps the S4 classes and the Fano families", verdict="supported", note=""),
    dict(claim="Seed's closing tower sentence: AMENDED", verdict="overstated",
         note="The facts in the seed sentence hold as written. The amendment concerns the interpretive phrase 'clean tower'."),
    dict(claim="Calibration-table rows sourced to SEED §3 are CALIBRATED", verdict="overstated",
         note="By PLAN §1's definitions these are CONFIRMED seed claims, not literature calibrations."),
    dict(claim="make_figures.py output byte-identical; figure 164 KB", verdict="supported",
         note="Reran in a scratch copy: cmp-identical, 163640 bytes. The figure exists and its labels match the computed point positions."),
]

out = dict(experiment="E0_hexagon_exact", role="independent cross-check (second agent)",
           method="Todd-Coxeter + Schreier-Sims over mod-p permutation images; exact Q[Z7]/(1+..+x^6) arithmetic for relations, traces and quartics; "
                  "integer lattice/Weyl/affine computations; exhaustive combinatorics; Fano-table octonions; sympy for the C + C^3 product",
           n_checks=xc["n_checks"], n_pass=xc["n_pass"], all_pass=xc["all_pass"], runtime_seconds=xc["runtime_seconds"],
           independent_values=independent_values, all_agree=all(r["agree"] for r in independent_values),
           claim_audit=claim_audit, issues=issues, overall="confirmed_with_corrections",
           summary="Every headline number of E0 reproduces with independent code and different methods (81/81 cross-check checks). No blocking or major issue. "
                   "Five minor wording, verdict-label and citation issues; the most concrete is an over-general check title about 7-vertex surfaces.")
with open(os.path.join(HERE, "crosscheck.json"), "w") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
print("wrote crosscheck.json;", len(independent_values), "quantities, all agree:", out["all_agree"])
