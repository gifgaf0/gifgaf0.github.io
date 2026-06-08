# op_psl3_family_sweep.g — OP-PSL.3: PSL(2,p) family generalization of the n1 characterization
# ============================================================================================
# Deliverable 1 of the CC BRIEF (OP-PSL.3). Computes, for each prime p:
#   - PSL(2,p) (as DerivedSubgroup(PGL(2,p)) so PGL is on hand for the Out-action),
#   - character table + irreducible degrees,
#   - conjugacy classes of maximal subgroups (index, order, structure),
#   - the full n1(H; rho) matrix  n1 = <chi_rho, Ind^G_H 1_H> = ScalarProduct(chi, PermChar),
#   - trinity (p in {5,7,11}): the index-p subgroup H_p, the decomposition of pi_{H_p},
#     and rho_{p-1} := the nontrivial constituent (degree p-1; for p=11, WHICH deg-10 irr),
#   - PR-3: the n1(.; rho_{p-1}) column over all maximal classes + uniqueness verdict,
#   - PR-4: number of index-p classes and whether the outer automorphism (PGL-conjugation)
#           fixes or swaps them,
#   - PR-5: Borel (index p+1), n1(Borel; St) with St the degree-p Steinberg, and whether
#           the Borel is the unique maximal class with n1(.; St)=1.
# All computed numbers are R1. No structural/family-theorem prose here (out of scope, brief s9).
#
# Run:  gap -q -b < op_psl3_family_sweep.g     (AtlasRep remote access disabled; offline-safe)

SetUserPreference("AtlasRep", "AtlasRepAccessRemoteFiles", false);

primes := [5, 7, 11, 13, 17, 19, 23];;
trinity := [5, 7, 11];;

for p in primes do
  Print("########## p = ", p, "  (", "trinity", "=", p in trinity, ") ##########\n");
  PG := PGL(2, p);;
  G  := DerivedSubgroup(PG);;            # = PSL(2,p) for p >= 5, index 2 in PGL
  Print("Size(G) = ", Size(G), "   expected p(p^2-1)/2 = ", p*(p^2-1)/2,
        "   OK=", Size(G) = p*(p^2-1)/2, "\n");

  tbl := CharacterTable(G);;
  irr := Irr(tbl);;
  degs := List(irr, Degree);;
  Print("irr degrees = ", degs, "\n");

  mx    := ConjugacyClassesMaximalSubgroups(G);;
  maxes := List(mx, Representative);;
  info  := List(maxes, H -> [Index(G,H), Size(H), StructureDescription(H)]);;
  pis   := List(maxes, H -> PermutationCharacter(G, H));;
  n1    := List(pis, pi -> List(irr, chi -> ScalarProduct(tbl, chi, pi)));;

  Print("--- maximal-subgroup classes & full n1 matrix (cols = irr degrees ", degs, ") ---\n");
  for i in [1..Length(maxes)] do
    Print("  [class ", i, "] index=", info[i][1], " order=", info[i][2],
          " type=", info[i][3], "  n1=", n1[i], "\n");
  od;

  # ---- Steinberg (degree p) and the Borel (index p+1): PR-5 ----
  stPos := Filtered([1..Length(irr)], i -> degs[i] = p);;
  Print("Steinberg: irr positions with degree p=", p, " -> ", stPos, "\n");
  borelIdx := Filtered([1..Length(maxes)], i -> info[i][1] = p+1);;
  Print("Borel: maximal classes of index p+1=", p+1, " -> classes ", borelIdx, "\n");
  if Length(stPos) >= 1 then
    st := stPos[1];;
    n1St := List([1..Length(maxes)], i -> n1[i][st]);;
    Print("PR-5: n1(.; St[deg ", p, "]) over maximal classes = ", n1St, "\n");
    uniqueSt := Filtered([1..Length(maxes)], i -> n1[i][st] = 1);;
    Print("PR-5: classes with n1(.;St)=1 -> ", uniqueSt,
          "  (Borel-unique-for-St = ", uniqueSt = borelIdx, ")\n");
  fi;

  # ---- index-p analysis (trinity) : PR-1, PR-2, PR-3, PR-4 ----
  mpIdx := Filtered([1..Length(maxes)], i -> info[i][1] = p);;
  Print("PR-1: # index-p (=", p, ") maximal classes = ", Length(mpIdx),
        " -> classes ", mpIdx, "\n");
  if Length(mpIdx) >= 1 then
    hp := maxes[mpIdx[1]];;
    piHp := pis[mpIdx[1]];;
    decomp := List(irr, chi -> ScalarProduct(tbl, chi, piHp));;
    Print("PR-2: pi_{H_p} decomposition (mult per irr) = ", decomp,
          "  rank=", Sum(decomp), "  multfree=", ForAll(decomp, x -> x <= 1), "\n");
    # rho_{p-1}: nontrivial constituent (degree p-1) appearing in pi_{H_p}
    rhoPos := Filtered([1..Length(irr)],
                       i -> degs[i] = p-1 and decomp[i] >= 1);;
    Print("PR-(rule): rho_{p-1} candidate irr positions (deg ", p-1,
          ", appearing in pi_Hp) = ", rhoPos, "   (#deg-(p-1) irrs total = ",
          Length(Filtered(degs, d -> d = p-1)), ")\n");
    if Length(rhoPos) = 1 then
      rp := rhoPos[1];;
      n1rho := List([1..Length(maxes)], i -> n1[i][rp]);;
      Print("PR-3: n1(.; rho_{p-1} = irr#", rp, " deg ", degs[rp],
            ") over maximal classes = ", n1rho, "\n");
      ones := Filtered([1..Length(maxes)], i -> n1[i][rp] = 1);;
      Print("PR-3: classes with n1(.;rho_{p-1})=1 -> ", ones,
            "  (== the index-p classes? ", Set(ones) = Set(mpIdx),
            " ; #such classes = ", Length(ones), ")\n");
    fi;
    # PR-4: Out-action via PGL conjugation
    delta := First(PG, x -> not (x in G));;
    Print("PR-4: outer rep delta in PGL\\PSL found = ", delta <> fail, "\n");
    for i in mpIdx do
      H := maxes[i];;
      Print("  PR-4: index-p class ", i, " conjugate to H^delta? ",
            IsConjugate(G, H, H^delta),
            "  (false => moved/swapped by Out)\n");
    od;
  else
    Print("PR-1: NO index-p maximal class (expected for control primes p NOT in {5,7,11}).\n");
  fi;
  Print("\n");
od;
QUIT;
