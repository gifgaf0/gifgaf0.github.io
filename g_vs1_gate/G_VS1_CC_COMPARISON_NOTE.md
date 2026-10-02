# G-VS1 — CC-side two-leg comparison (frozen comparator v1.0 + the direct per-form check) — October 1, 2026

Run after the return was committed and the armor opened (`--decode-quarantined`; every quarantined md5 and byte count asserted by the dispatch extractor). Inputs: chat checkpoint `quarantine/g_vs1_chatleg_checkpoint.json` (md5 `d3d1ed074259c8924d0c29a03d320918`), CC checkpoint `g_vs1_ccleg_checkpoint.json` (md5 `05e82029d8d978661bc200b9bec1755c`); chat pre-read `quarantine/g_vs1_chatleg_prereadcheckpoint.json` (md5 `b208db869bbc0c8c80c482737d957d9d`), CC pre-read `g_vs1_ccleg_prereadcheckpoint.json` (md5 `7c4073730ddbe2b3f4ac5a13c0e24354`). Comparator `g_vs1_compare_v1_0.py` md5 `69011375d28ec8f63f3ac76383e98321` (schema md5 asserted by the comparator itself).

## 1. Full pair (chat checkpoint vs CC checkpoint) → `g_vs1_twoleg_comparison_cc.json`

**415 checks, 340 PASS, 75 MISS (0 representational, 75 exact); verdict codes ["VC-3", "VC-3"]; ALL_PASS = False** (file md5 `629b99aa0a4071b10c5656bc20f1ef73`).

| check | name | kind | chat | cc |
|---|---|---|---|---|
| C-VS-1 | phase0.0a.rank | EXACT | 14 | 2 |
| C-VS-1 | phase0.0a.index_su2_long | EXACT | 1 | 1 |
| C-VS-1 | phase0.0a.index_su2_short | EXACT | 3 | 3 |
| C-VS-1 | phase0.0d.spin1_polar.elementary_winding | EXACT | 2pi/2 | pi |
| C-VS-1 | phase0.0d.weyl_spin1_invariant_dims | EXACT | {"2": 1, "4": 2, "6": 2} | [1, 2, 2] |
| C-VS-1 | phase0.0f.annihilated | EXACT | {"N_minus_rho7": true, "rho0": true, "rho7": true} | true |
| C-VS-2 | phase1.weyl | EXACT | {"G2xU1_R14": {"2": 1, "4": 2, "6": 2}, "G2xU1_R16": {"2": 2, "4": 6, "6": 10}, "SO7xU1_R14": {"2": 1, "4": 2, "6": 2}, "SO7xU1_R16": {"2": 2, "4": 6, "6": 10}} | {"G2xU1_R14": {"deg2": 1, "deg4": 2, "deg6": 2}, "G2xU1_R16": {"deg2": 2, "deg4": 6, "deg6": 10}, "SO7xU1_R14": {"deg2": 1, "deg4": 2, "deg6": 2}, "SO7xU1_R16": {"deg2": 2, "deg4": 6, "deg6": 10}} |
| C-VS-2 | phase1.T_parity | EXACT | {"N": 1, "N^2": 1, "Q = psi0^2 Sbar - c.c. (imaginary-valued)": -1, "Re(psi0^2 Sbar)": 1, "rho0": 1, "rho0*N": 1, "rho0^2": 1, "\|S\|^2": 1} | {"deg2": {"N": 1, "rho0": 1}, "deg4": {"N^2": 1, "Q": -1, "Re(psi0^2 Sbar)": 1, "rho0 N": 1, "rho0^2": 1, "\|S\|^2": 1}} |
| C-VS-2 | phase1.locality_g2_equals_so7 | EXACT | {"R14": {"2": true, "4": true, "6": true}, "R16": {"2": true, "4": true, "6": true}} | true |
| C-VS-2 | phase1.F_VS_1 | EXACT | SILENT | false |
| C-VS-2 | phase1.F_VS_2 | EXACT | SILENT | false |
| C-VS-2 | phase1.RUS.deg4.flags | EXACT | {"N^2": true, "Q = psi0^2 Sbar - c.c. (imaginary-valued)": true, "Re(psi0^2 Sbar)": true, "rho0*N": true, "rho0^2": true, "\|S\|^2": true} | {"N^2": true, "Q": true, "Re(psi0^2 Sbar)": true, "rho0 N": true, "rho0^2": true, "\|S\|^2": true} |
| C-VS-2 | phase1.RUS.singlet_blind | EXACT | {"N": true, "N^2": true, "Q = psi0^2 Sbar - c.c. (imaginary-valued)": false, "Re(psi0^2 Sbar)": false, "rho0": false, "rho0*N": false, "rho0^2": false, "\|S\|^2": true} | {"N": true, "N^2": true, "Q": false, "Re(psi0^2 Sbar)": false, "rho0": false, "rho0 N": false, "rho0^2": false, "\|S\|^2": true} |
| C-VS-2 | phase1.point_of_record.quartic_coefficients | EXACT | {"N^2": "1", "Re(psi0^2 Sbar)": "0", "rho0*N": "2", "rho0^2": "1", "\|S\|^2": "0"} | ["1", "2", "1", "0", "0"] |
| C-VS-2 | phase1.basis_deg4 | EXACT | ["rho0^2", "rho0*N", "N^2", "\|S\|^2", "Re(psi0^2 Sbar)", "Q = psi0^2 Sbar - c.c. (imaginary-valued)"] | ["rho0^2", "rho0 N", "N^2", "\|S\|^2", "Re(psi0^2 Sbar)"] |
| C-VS-3 | phase2.strata.R.P_kind | EXACT | finite | trivial |
| C-VS-3 | phase2.strata.R.dynkin_index | EXACT | 1 | 1 |
| C-VS-3 | phase2.strata.R.pi0_K | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.R.pi0_H | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.P7.P_kind | EXACT | finite | Z2 |
| C-VS-3 | phase2.strata.P7.dynkin_index | EXACT | 1 | 1 |
| C-VS-3 | phase2.strata.P7.orbit | EXACT | S6 = G2/SU(3) | S6 |
| C-VS-3 | phase2.strata.P7.pi0_K | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.P7.elementary_winding | EXACT | 2pi/2 | pi |
| C-VS-3 | phase2.strata.F7.P_kind | EXACT | U1 | U(1) |
| C-VS-3 | phase2.strata.F7.dynkin_index | EXACT | 1 | 1 |
| C-VS-3 | phase2.strata.F7.orbit | EXACT | V2(R7) = G2/SU(2) | V2(R7) |
| C-VS-3 | phase2.strata.F7.pi0_K | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.F7.pi0_H | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.F7.elementary_winding | EXACT | none | null |
| C-VS-3 | phase2.strata.I7.P_kind | EXACT | finite | Z2 |
| C-VS-3 | phase2.strata.I7.dynkin_index | EXACT | 1 | 1 |
| C-VS-3 | phase2.strata.I7.orbit | EXACT | V2(R7) = G2/SU(2) | V2(R7) |
| C-VS-3 | phase2.strata.I7.pi0_K | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.I7.elementary_winding | EXACT | 2pi/2 | pi |
| C-VS-3 | phase2.strata.MP+.P_kind | EXACT | finite | trivial |
| C-VS-3 | phase2.strata.MP+.dynkin_index | EXACT | 1 | 1 |
| C-VS-3 | phase2.strata.MP+.orbit | EXACT | S6 = G2/SU(3) | S6 |
| C-VS-3 | phase2.strata.MP+.pi0_K | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MP+.pi0_H | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MP-.P_kind | EXACT | finite | trivial |
| C-VS-3 | phase2.strata.MP-.dynkin_index | EXACT | 1 | 1 |
| C-VS-3 | phase2.strata.MP-.orbit | EXACT | S6 = G2/SU(3) | S6 |
| C-VS-3 | phase2.strata.MP-.pi0_K | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MP-.pi0_H | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MP0.P_kind | EXACT | finite | trivial |
| C-VS-3 | phase2.strata.MP0.dynkin_index | EXACT | 1 | 1 |
| C-VS-3 | phase2.strata.MP0.orbit | EXACT | S6 = G2/SU(3) | S6 |
| C-VS-3 | phase2.strata.MP0.pi0_K | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MP0.pi0_H | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MF.P_kind | EXACT | finite | trivial |
| C-VS-3 | phase2.strata.MF.dynkin_index | EXACT | 1 | 1 |
| C-VS-3 | phase2.strata.MF.orbit | EXACT | V2(R7) = G2/SU(2) | V2(R7) |
| C-VS-3 | phase2.strata.MF.pi0_K | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MF.pi0_H | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MI+.P_kind | EXACT | finite | trivial |
| C-VS-3 | phase2.strata.MI+.dynkin_index | EXACT | 1 | 1 |
| C-VS-3 | phase2.strata.MI+.orbit | EXACT | V2(R7) = G2/SU(2) | V2(R7) |
| C-VS-3 | phase2.strata.MI+.pi0_K | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MI+.pi0_H | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MI-.P_kind | EXACT | finite | trivial |
| C-VS-3 | phase2.strata.MI-.dynkin_index | EXACT | 1 | 1 |
| C-VS-3 | phase2.strata.MI-.orbit | EXACT | V2(R7) = G2/SU(2) | V2(R7) |
| C-VS-3 | phase2.strata.MI-.pi0_K | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MI-.pi0_H | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MI0.P_kind | EXACT | finite | trivial |
| C-VS-3 | phase2.strata.MI0.dynkin_index | EXACT | 1 | 1 |
| C-VS-3 | phase2.strata.MI0.orbit | EXACT | V2(R7) = G2/SU(2) | V2(R7) |
| C-VS-3 | phase2.strata.MI0.pi0_K | EXACT | 1 | 0 |
| C-VS-3 | phase2.strata.MI0.pi0_H | EXACT | 1 | 0 |
| C-VS-3 | phase2.criterion_pi1_zero_iff_rho0_zero_and_S_zero | EXACT | {"F7": true, "I7": true, "MF": true, "MI+": true, "MI-": true, "MI0": true, "MP+": true, "MP-": true, "MP0": true, "P7": true, "R": true} | true |
| C-VS-3 | phase2.sampling.tally | EXACT | {"DEGENERATE: edge rho=0: P7, I7, F7 \| points: F7,P7": 82, "DEGENERATE: edge rho=0: P7, I7, F7 \| points: F7,P7,R": 9, "DEGENERATE: edge rho=0: P7, I7, F7; edge s=1-rho: R, MP, P7 \| points: F7,P7,R": 6, "DEGENERATE: edge s=0: R, MF, F7 \| points: F7,R": 3, "DEGENERATE: edge s=1-rho: R, MP, P7 \| points: P7,R": 12, "DEGENERATE: interior segment from (0,0) to (1/2,1/2): strata F7, MI+, MP+ \| points: F7,MP+": 2, "DEGENERATE: interior segment from (0,0) to (1/2,1/2): strata F7, MI-, MP- \| points: F7,MP-": 2, "DEGENERATE: interior segment from (0,0) to (1/3,2/3): strata F7, MI+, MP+ \| points: F7,MP+": 1, "DEGENERATE: interior segment from (0,0) to (1/3,2/3): strata F7, MI-, MP- \| points: F7,MP-": 1, "DEGENERATE: interior segment from (0,0) to (2/3,1/3): strata F7, MI+, MP+ \| points: F7,MP+": 1, "DEGENERATE: interior segment from (0,0) to (2/3,1/3): strata F7, MI-, MP- \| points: F7,MP-": 1, "DEGENERATE: interior segment from (1/2,0) to (1/2,1/2): strata MF, MI0, MP0 \| points: MF,MP0": 3, "DEGENERATE: interior segment from (1/4,0) to (1/4,3/4): strata MF, MI0, MP0 \| points: MF,MP0": 2, "DEGENERATE: interior segment from (1/8,0) to (1/8,7/8): strata MF, MI0, MP0 \| points: MF,MP0": 1, "DEGENERATE: whole orbit space: P0 \| points: F7,P7,R": 1, "F7": 356, "F7,MP+": 1, "F7,MP-": 1, "F7,R": 45, "MF": 18, "MI+": 33, "MI-": 33, "MP+": 196, "MP-": 196, "MP0": 1, "P7": 638, "P7,R": 48, "R": 708} | {"F7": 356, "F7,I7,MF,MI+,MI-,MI0,MP+,MP-,MP0,P7,R \| P0": 1, "F7,I7,MP+,P7,R \| edge_rho=0,edge_s=1-rho": 3, "F7,I7,MP-,P7,R \| edge_rho=0,edge_s=1-rho": 3, "F7,I7,P7 \| edge_rho=0": 82, "F7,I7,P7,R \| edge_rho=0": 9, "F7,MF,R \| edge_s=0": 3, "F7,MI+,MP+ \| interior_segment": 4, "F7,MI-,MP- \| interior_segment": 4, "F7,MP+": 1, "F7,MP-": 1, "F7,R": 45, "MF": 18, "MF,MI+,MI-,MI0,MP+,MP-,MP0 \| interior_segment": 6, "MI+": 33, "MI-": 33, "MP+": 196, "MP+,MP-,MP0": 1, "MP+,MP-,MP0,P7,R \| edge_s=1-rho": 2, "MP+,P7,R \| edge_s=1-rho": 5, "MP-": 196, "MP-,P7,R \| edge_s=1-rho": 5, "P7": 638, "P7,R": 48, "R": 708} |
| C-VS-3 | phase2.sampling.strata_realized_as_minimizers | EXACT | ["F7", "MF", "MI+", "MI-", "MP+", "MP-", "MP0", "P7", "R"] | ["F7", "I7", "MF", "MI+", "MI-", "MI0", "MP+", "MP-", "MP0", "P7", "R"] |
| C-VS-3 | phase2.F_VS_3 | EXACT | SILENT | false |
| C-VS-4 | phase3.F_VS_4 | EXACT | SILENT | false |

## 2. Pre-read pair → `g_vs1_twoleg_comparison_preread_cc.json`

**71 checks, 65 PASS, 6 MISS (0 representational, 6 exact); verdict codes [["<MISSING>"], ["<MISSING>"]]; ALL_PASS = False** (file md5 `707bbb72db288a697dedb979481b7f3d`).

| check | name | kind | chat | cc |
|---|---|---|---|---|
| C-VS-1 | phase0.0a.rank | EXACT | 14 | 2 |
| C-VS-1 | phase0.0a.index_su2_long | EXACT | 1 | 1 |
| C-VS-1 | phase0.0a.index_su2_short | EXACT | 3 | 3 |
| C-VS-1 | phase0.0d.spin1_polar.elementary_winding | EXACT | 2pi/2 | pi |
| C-VS-1 | phase0.0d.weyl_spin1_invariant_dims | EXACT | {"2": 1, "4": 2, "6": 2} | [1, 2, 2] |
| C-VS-1 | phase0.0f.annihilated | EXACT | {"N_minus_rho7": true, "rho0": true, "rho7": true} | true |

## 3. The per-form checks the frozen comparator cannot address (H-CC-1) → `g_vs1_twoleg_forms_direct_cc.json`

The schema's form names contain ".", so the comparator's dotted-path lookup returns `<MISSING>` for every `phase3.F_a.<form>.<key>` on both legs (those 48 rows PASS trivially above). Re-run here with the form name as a single key and the schema's own key lists (degree-4 list for degree-4 forms, degree-2 list for the D-a forms): **78 checks, 54 PASS, 24 MISS** (file md5 `9f19862fc85f9e16ba972e593df3e455`). Forms present — chat: 8, CC: 8.

| form | key | chat | cc |
|---|---|---|---|
| F-a.1 \|<psi,psi>\|^2 (the complex bilinear norm, modulus squared) | coefficients | {"N^2": "0", "Re(psi0^2 Sbar)": "2", "rho0*N": "0", "rho0^2": "1", "\|S\|^2": "1"} | ["1", "0", "0", "1", "2"] |
| F-a.1 \|<psi,psi>\|^2 (the complex bilinear norm, modulus squared) | minimizers | [{"rho": "0", "s": "0", "stratum": "F7", "t": "0", "t_free": false}, {"rho": "1/2", "s": "1/2", "stratum": "MP-", "t": "-1/4", "t_free": false}] | ["F7", "MI-", "MP-"] |
| F-a.1 \|<psi,psi>\|^2 (the complex bilinear norm, modulus squared) | degenerate_faces | ["interior segment from (0,0) to (1/2,1/2): strata F7, MI-, MP-"] | ["interior_segment"] |
| F-a.1 \|<psi,psi>\|^2 (the complex bilinear norm, modulus squared) | pi1_of_minimizing_strata | {"F7": "0", "MP-": "Z"} | {"F7": "0", "MI-": "Z", "MP-": "Z"} |
| F-a.2 \|\|psi psibar^dag\|\|^2_H | coefficients | {"N^2": "2", "Re(psi0^2 Sbar)": "-2", "rho0*N": "4", "rho0^2": "1", "\|S\|^2": "-1"} | ["1", "4", "2", "-1", "-2"] |
| F-a.2 \|\|psi psibar^dag\|\|^2_H | minimizers | [{"rho": "0", "s": "1", "stratum": "P7", "t": "0", "t_free": false}, {"rho": "1", "s": "0", "stratum": "R", "t": "0", "t_free": false}] | ["MP+", "P7", "R"] |
| F-a.2 \|\|psi psibar^dag\|\|^2_H | degenerate_faces | ["edge s=1-rho: R, MP, P7"] | ["edge_s=1-rho"] |
| F-a.2 \|\|psi psibar^dag\|\|^2_H | pi1_of_minimizing_strata | {"P7": "Z", "R": "Z"} | {"MP+": "Z", "P7": "Z", "R": "Z"} |
| F-a.3 \|\|psibar^dag psi\|\|^2_H | coefficients | {"N^2": "2", "Re(psi0^2 Sbar)": "-2", "rho0*N": "4", "rho0^2": "1", "\|S\|^2": "-1"} | ["1", "4", "2", "-1", "-2"] |
| F-a.3 \|\|psibar^dag psi\|\|^2_H | minimizers | [{"rho": "0", "s": "1", "stratum": "P7", "t": "0", "t_free": false}, {"rho": "1", "s": "0", "stratum": "R", "t": "0", "t_free": false}] | ["MP+", "P7", "R"] |
| F-a.3 \|\|psibar^dag psi\|\|^2_H | degenerate_faces | ["edge s=1-rho: R, MP, P7"] | ["edge_s=1-rho"] |
| F-a.3 \|\|psibar^dag psi\|\|^2_H | pi1_of_minimizing_strata | {"P7": "Z", "R": "Z"} | {"MP+": "Z", "P7": "Z", "R": "Z"} |
| F-a.4 \|\|psi^2\|\|^2_H | coefficients | {"N^2": "0", "Re(psi0^2 Sbar)": "-2", "rho0*N": "4", "rho0^2": "1", "\|S\|^2": "1"} | ["1", "4", "0", "1", "-2"] |
| F-a.4 \|\|psi^2\|\|^2_H | minimizers | [{"rho": "0", "s": "0", "stratum": "F7", "t": "0", "t_free": false}] | ["F7"] |
| F-a.5 N_O(psi psibar^dag) = sum_k P_k^2 | coefficients | {"N^2": "0", "Re(psi0^2 Sbar)": "2", "rho0*N": "0", "rho0^2": "1", "\|S\|^2": "1"} | ["1", "0", "0", "1", "2"] |
| F-a.5 N_O(psi psibar^dag) = sum_k P_k^2 | minimizers | [{"rho": "0", "s": "0", "stratum": "F7", "t": "0", "t_free": false}, {"rho": "1/2", "s": "1/2", "stratum": "MP-", "t": "-1/4", "t_free": false}] | ["F7", "MI-", "MP-"] |
| F-a.5 N_O(psi psibar^dag) = sum_k P_k^2 | degenerate_faces | ["interior segment from (0,0) to (1/2,1/2): strata F7, MI-, MP-"] | ["interior_segment"] |
| F-a.5 N_O(psi psibar^dag) = sum_k P_k^2 | pi1_of_minimizing_strata | {"F7": "0", "MP-": "Z"} | {"F7": "0", "MI-": "Z", "MP-": "Z"} |
| F-a.6 \|\|Im_O(psi psibar^dag)\|\|^2_H | coefficients | {"N^2": "1", "Re(psi0^2 Sbar)": "-2", "rho0*N": "2", "rho0^2": "0", "\|S\|^2": "-1"} | ["0", "2", "1", "-1", "-2"] |
| F-a.6 \|\|Im_O(psi psibar^dag)\|\|^2_H | minimizers | [{"rho": "0", "s": "1", "stratum": "P7", "t": "0", "t_free": false}, {"rho": "1", "s": "0", "stratum": "R", "t": "0", "t_free": false}] | ["MP+", "P7", "R"] |
| F-a.6 \|\|Im_O(psi psibar^dag)\|\|^2_H | degenerate_faces | ["edge s=1-rho: R, MP, P7"] | ["edge_s=1-rho"] |
| F-a.6 \|\|Im_O(psi psibar^dag)\|\|^2_H | pi1_of_minimizing_strata | {"P7": "Z", "R": "Z"} | {"MP+": "Z", "P7": "Z", "R": "Z"} |
| D-a.1 Re_O(psi psibar^dag) (degree 2) | coefficients | {"N": "1", "rho0": "1"} | ["1", "1"] |
| D-a.2 Re_O(psibar^dag psi) (degree 2) | coefficients | {"N": "1", "rho0": "1"} | ["1", "1"] |

## 4. Reading of the misses

**Both legs reach class code `VC-3`; every compared number agrees; all 75 exact misses of the frozen comparator (and the 6 of the pre-read pair, which are a subset) are representational or definitional — the S9 classification CC proposes, row by row:**

| Miss (count) | chat | cc | Reading |
|---|---|---|---|
| `phase0.0a.rank` (1) | 14 | 2 | **definitional** — chat: the rank of the 14 basis matrices (= g2_dim); CC: the Lie-algebra rank (generic ad-nullity). A-2 defines neither; both are correct for their definition (CC-DD-1). |
| `phase0.0a.index_su2_long` / `index_su2_short` (2) | `"1"`, `"3"` | 1, 3 | **representational** — strings vs JSON integers; the schema allows both. Same values. |
| `phase0.0d.spin1_polar.elementary_winding`, `phase2.strata.{P7,I7}.elementary_winding` (3) | `"2pi/2"` | `"pi"` | **representational** — the same angle. |
| `phase0.0d.weyl_spin1_invariant_dims` (1) | `{"2":1,"4":2,"6":2}` | `[1,2,2]` | **representational** — same counts. |
| `phase0.0f.annihilated` (1) | `{rho0: true, rho7: true, N_minus_rho7: true}` | `true` | **representational** — the per-candidate dict vs its conjunction. |
| `phase1.weyl` (1) | degree keys `"2"/"4"/"6"` | `"deg2"/"deg4"/"deg6"` | **representational** — identical counts 2/6/10 and 1/2/2 for both algebras. |
| `phase1.T_parity`, `RUS.deg4.flags`, `RUS.singlet_blind` (3) | flat dict; names `rho0*N`, `Q = psi0^2 Sbar - c.c. (imaginary-valued)` | nested by degree; names `rho0 N`, `Q` | **representational** — identical parities and flags under the candidate-name map rho0*N ↔ rho0 N, Q-long-name ↔ Q. |
| `phase1.locality_g2_equals_so7` (1) | per-space, per-degree dict, all true | `true` | **representational** — its conjunction. |
| `phase1.F_VS_1`, `F_VS_2`, `phase2.F_VS_3`, `phase3.F_VS_4` (4) | `"SILENT"` | `false` | **representational** — "did not fire" in two encodings. |
| `phase1.point_of_record.quartic_coefficients` (1) | dict by basis name | list in basis order | **representational** — (1, 2, 1, 0, 0) on both legs. |
| `phase1.basis_deg4` (1) | the six degree-4 invariants (Q included) | the five T-even ones | **definitional** — chat records the full degree-4 basis, CC the T-even basis A-2.8 names; same five T-even names modulo `rho0*N`/`rho0 N`. |
| `phase2.strata.*.P_kind` (11) | `"finite"` / `"U1"` | `"trivial"` or `"Z2"` / `"U(1)"` | **representational** — `m` agrees on every stratum (PASS), which carries the finite order. |
| `phase2.strata.*.dynkin_index` (11) | `"1"` | 1 | **representational** — string vs integer. |
| `phase2.strata.*.orbit` (10) | `"S6 = G2/SU(3)"`, `"V2(R7) = G2/SU(2)"` | `"S6"`, `"V2(R7)"` | **representational** — the same orbit with the coset written out. |
| `phase2.strata.*.pi0_K` (11), `pi0_H` on the m = 1 strata and F7 (9) | `"1"` | `"0"` | **representational** — the trivial group written as its order (chat) vs as a homotopy group (CC); `K_connected` PASS on all eleven, `pi0_H` = `Z2` PASS on P7 and I7. |
| `phase2.strata.F7.elementary_winding` (1) | `"none"` | `null` | **representational**. |
| `phase2.criterion_pi1_zero_iff_rho0_zero_and_S_zero` (1) | per-stratum dict, all true | `true` | **representational** — its conjunction (CC's per-stratum table is in the non-compared `criterion_table`). |
| `phase2.sampling.tally` (1) | 28 prose keys | 25 token keys | **representational** — reconciled mechanically by stratum family: 708 R, 638 P7, 356 F7, 393 MP, 66 MI, 48 P7+R, 45 F7+R, 18 MF, 2 F7+MP (point ties), and the degenerate families 82 / 9 / 6 (edge ρ = 0 with and without R, with the edge s = 1 − ρ), 12 (edge s = 1 − ρ), 3 (edge s = 0), 8 (F7–MI–MP interior segments), 6 (MF–MI–MP interior segments), 1 (P0) — every count equal; 127 degenerate outcomes on both legs (the chat report's prose "128" is a slip against its own tally). The chat splits interior segments by their endpoints and labels a free-t point by t = 0 (`MP0`: 1); CC aggregates segments and labels a free-t point with all its t-labels (`MP+,MP-,MP0`: 1). |
| `phase2.sampling.strata_realized_as_minimizers` (1) | nine strata (no I7, no MI0) | all eleven | **definitional** — chat counts the strata of point minimizers; CC counts every stratum appearing in a minimizer set, so I7 (inside the degenerate edge ρ = 0, 97 grid points) and MI0 (inside the MF–MI–MP interior segments and the free-t intervals) are included. The underlying tallies are identical. |

**The per-form keys (direct check, 78 rows, 54 PASS, 24 MISS):** every `degree`, `g2_u1_invariant`, `T_parity`, `in_T_even_basis`/`in_basis`, `effective_ABc4c5`, `is_O16_point`/`is_O16` and `Emin` agrees exactly on all eight forms. The 24 misses: `coefficients` (8 forms) — dict by basis name vs list in basis order, identical values; `minimizers` (6 forms) — chat lists the point minimizers as (ρ, s, t, stratum, t_free) records, CC lists the stratum labels of the whole minimizer set; `degenerate_faces` (5 forms) — prose vs tokens naming the same edge or segment with the same endpoints; `pi1_of_minimizing_strata` (5 forms) — chat over the point minimizers, CC over every stratum of the minimizer set (the extra entries are MI− on F-a.1/F-a.5 and MP+ on F-a.2/F-a.3/F-a.6, with π₁ = Z, agreeing with the chat's own stratum table). All representational / definitional.

**Independence witness:** instrument md5s differ (`cb2e2230` chat, 55,958 B, Fractions / sympy rationals with numpy mod p; `0ba1abe4` CC, 80,852 B, Fractions only with a weight-coordinate GF(p) elimination); primes differ in one of two (chat 1,048,573 and 999,983; CC 1,048,573 and 1,000,037); the structures differ throughout. Neither checkpoint was edited at any point.

