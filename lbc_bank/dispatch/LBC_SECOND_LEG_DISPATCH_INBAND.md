# LBC SECOND-LEG DISPATCH (single file, in-band) — the numbers the supersolid-vacuum paper cites

**Plain-language summary.** A short paper argues that a supersolid "vacuum" cannot give matter and light one speed limit, because the medium's second sound is slower than its shear wave and couples to the knots. Every number it cites was computed once, by one route, with internal cross-checks. This dispatch asks for an independent, blind recomputation of exactly those numbers from the model definitions below. The first leg's results travel sealed inside this file. They are opened only after your own results are committed, then compared by the embedded comparator. This is not a gate: no lock, no fold, and no ledger edit rides on it. It is the two-leg check the author asked for on the paper's numbers.

**Activation.** Do not start until the author's message contains this exact line:
`ACTIVATE: LBC-2LEG-1`
On any other message, hold and say so.

## 1. Independence rules (binding)

1. Build from scratch. Do not import, copy or read the first leg's scripts (the `lbc_*.py`, `step3_*.py`, `paper_*.py` files; the earlier instruments `g_tsh1_chatleg.py`, `tsh4_core.py`, `tsh4_routeD.py`). The sealed embed E6 contains them for diagnosis only, after comparison.
2. Use a different method wherever you reasonably can. Examples: a Newton or preconditioned-gradient ground-state solver instead of split-step imaginary time; a real-space or finite-difference BdG, or your own plane-wave construction with a different basis cut; a different quadrature for the γ6 kernel transform; an independent derivation of the drag prefactor.
3. Do not decode embeds E5 or E6 until your checkpoint (Sec. 4) is written, scanned (Sec. 5) and committed on your branch. Record the commit hash.
4. Report every number at full precision. Do not round to match anything.
5. Work from `main`. Do not open, list or read anything under `lbc_bank/` except the `lbc_bank/second_leg/` folder you create, and do not check out or read the branch `claude/lbc-bank-v489` or its pull request. They hold the first leg's numbers and the paper draft in plain text. If `lbc_bank/` is already on `main` when you start, treat everything in it outside `second_leg/` as sealed, exactly like E5 and E6.

## 2. Model definitions (exact)

Units ħ = m = 1. Mean density ρ̄ = 1. Core radius R = 1.

**2D.** E[ψ] = ∫ ½|∇ψ|² d²r + ½ ∬ ρ(r) U(r − r′) ρ(r′) d²r d²r′, with ρ = |ψ|².
- Step kernel U(r) = g θ(R − r), Fourier transform Û(k) = 2πgR² J₁(kR)/(kR), Û(0) = πgR².
- γ6 kernel U(r) = g exp(−(r/R)⁶), Û(k) = 2πg ∫₀^∞ e^(−r⁶) J₀(kr) r dr.
- Crystal: triangular lattice, one droplet per primitive cell, a₁ = (a, 0), a₂ = (a/2, √3a/2). The lattice constant a is optimized at fixed ρ̄ (minimize energy per area).
- Uniform reference: energy per area πg/2, chemical potential πg (step kernel).

**3D.** e = ⟨½|∇ψ|²⟩ + (Λ/2)⟨n (Û ∗ n)⟩ with n = |ψ|² and ⟨n⟩ = 1; step kernel Û(k) = 4πR³[sin(kR) − kR cos(kR)]/(kR)³.
- Λ_c = min over k with Û(k) < 0 of [−k²/(4Û(k))] (expect Λ_c ≈ 21.71); use Λ = 2Λ_c.
- Structure: AB (hcp-type) stack in the orthorhombic cell (a, √3a, c) with sites at fractional (0,0,0), (½,½,0), (½,⅙,½), (0,⅔,½).
- Lattice parameters: a = 1.3859646002819213, c = 2.2595969088482843 (from an earlier optimization). Report results there, and optionally at your own optimum.

**Excitations.** Linearize the time-dependent GP equation about the ground state ψ₀ (Bogoliubov–de Gennes), Bloch wavevector q.
- Density matrix element of mode ν: ρ_ν(q) = ∫_cell e^(−iq·r) ψ₀ (u_ν + v_ν), with normalization ∫_cell (|u_ν|² − |v_ν|²) = 1.
- Spectral weight: Z_ν = |ρ_ν|² per cell.
- f-sum share: F_ν = ω_ν Z_ν / (N_cell q²/2), N_cell = ρ̄ × cell area (volume).
- Static share: S_ν = (2Z_ν/ω_ν) / Σ_μ(2Z_μ/ω_μ).
- Both sum rules are checks: Σ_ν ω_ν Z_ν = N_cell q²/2, and Σ_ν 2Z_ν/ω_ν must equal the directly solved static response (equivalently Σ_ν F_ν/c_ν² = 1/c_κ²).
- Identify modes by polarization, not frequency order. In 2D the transverse mode has zero density weight along mirror directions; the two remaining gapless modes are longitudinal, labelled 2 (lower) and 1 (upper). Detect and report c₂ > c_T if it occurs.

**Directions and fits.** 2D: q parallel to a₁ (the first leg's instruments call this direction "GM"; geometrically it points toward K — the labels are inherited, the direction is what counts). Also report c_T at 30° to a₁, at |q|a/2π = 0.05. Speeds are least-squares slopes ω = c q through the origin over |q|a/2π ∈ {0.03, 0.05, 0.075, 0.10}. Weights are quoted at |q|a/2π = 0.05. 3D: q parallel to the x axis (along a) with |q| = 0.15 and 0.3 (units 1/R). Report the q = 0.15 values in the schema.

## 3. Tasks

**Q-A (2D weights).** For g ∈ {44, 28, 22, 16, 14, 13.5, 13.25, 13} (step kernel) and g = 35 (γ6 kernel), compute a, c₂, c_T, c₁, F₂, Z₂/Z₁, S₂. For the step points with g ≤ 22 also compute the superfluid fraction f_s from the phase-twist energy, E(k) − E(0) = ½ N f_s k² with the lattice held fixed and k small. At g = 22 also report the maximum sum-rule residuals over your q points and c_T at 30°.

**Q-A′ (static hydrodynamic route at g = 22, no excitations).** From finite strains of the relaxed cell, compute:
- f_s;
- α = ∂²e/∂ρ² (lattice fixed);
- M = C_xxxx (density fixed);
- C_xxyy;
- μ = C_xyxy (shear);
- γ = ∂²e/∂ρ∂ε_xx.

Then evaluate, with ρ_n = (1 − f_s)ρ and ρ_s = f_s ρ:
- a = ρα − 2γ + M/ρ_n and b = (ρ_s/ρ_n)(αM − γ²);
- c_±² = [a ± √(a² − 4b)]/2;
- c_T = √(μ/ρ_n);
- F₋ = (c_*² − c₋²)/(c₊² − c₋²), with c_*² = ρ_s M/(ρ ρ_n);
- the static share of the lower branch, (F₋/c₋²)/(F₋/c₋² + F₊/c₊²).

**Q-B (3D weights).** At the AB point, report:
- c₂ and the range of transverse speeds over your directions (c_T min and max);
- c₁, F₂, Z₂/Z₁ and S₂ at q = 0.15 along x;
- the compressibility speed c_κ = (vol/χ_static)^½ per unit density.

**Q-C (approach to melting, step kernel, 2D).** Follow the crystal branch downward in g (continuation seeding is fine) and report:
- the fixed-density coexistence boundary Λ_c, defined as the root of Λ(μ_c − ε_c) = μ_c²/(2π), where ε_c is the crystal energy per particle and μ_c its chemical potential;
- Λ_u = μ_c(Λ_c)/π;
- the fixed-density energy crossing (ε_c = πg/2);
- c₂/c_T and F₂ at Λ_c;
- the maximum of c₂/c_T along the metastable continuation, and the g at which the crystal branch ends;
- the boolean "c₂ ≥ c_T at any computed state".

**Q-D (loss length and formulas).**
1. Derive the drag on a point-like density-coupled defect of vertex V(q) moving at v through a medium with χ(q, ω) = ρq² Σ_ν F_ν/(ω² − c_ν² q²) (linear branches). Report the coefficient C in F_d = C ρ F_ν v⁻² ∫ q³|V|² dq. As a check, reduce to the single Bogoliubov branch with a contact vertex and compare with Astrakharchik & Pitaevskii, Phys. Rev. A 70, 013608 (2004), Eq. (12).
2. From the inputs below, recompute the loss-length re-evaluation.
   - Closure: ℓ = γ M τ̂ ξ / 𝒫 per channel, γ = 3.1974×10¹¹, ξ = 1.616255×10⁻³⁵ m (take as given), L_prop = 3.0857×10²⁰ m, M_old = φ² (φ the golden ratio).
   - Maps at four points (Â, Ĵ, Ô, T̂ = τ̂): (15.17, 4.68, 1.82, 8.06), (9.35, 0.61, 1.6401, 2.74), (13.73, 4.43, 1.20, 7.49), (18.26, 7.41, 0.45, 11.23).
   - Report the most- and least-favourable log₁₀(ℓ/L_prop) over points and channels.
   - Main re-evaluation: multiply ℓ by [S(φ²)/S(M_new)]/F₂ with S(M) = (1 − 1/M²)^(−½), M_new = c_T/c₂ from your Q-B (take c_T = 7.68 as the dynamical mean), and F₂ over your Q-B q points.
   - Report the orders recovered (min, max), the new most-favourable headline (min, max), the band over the four readings (fixed vertex filament / fixed vertex point source / closure literal with M → c_T/c₂ / fixed dressed static deficit with the factor divided by (c_κ/c_s)⁴, where c_s = c_T/φ²), and ξ_req = L_prop 𝒫/(γ M τ̂) divided by the main factor.
3. Evaluate the paper's estimate ℓ ≈ (16πτ/ε²)(c_T/c_κ)⁴ γξ/F₂ at τ = 10 and ε = 1 with your 3D c_κ and the smaller F₂; report the coefficient of γξ. Evaluate 1/(2γ²).

## 4. Checkpoint

Write `lbc_cc_checkpoint.json` in the schema of embed E4 (schema `lbc_2leg_schema_v1.0`, leg `cc`). Fill every null; arrays have the length shown. Units as in Sec. 2. Add any extra keys you like (they are reported as CC-only and not compared).

## 5. Procedure

1. Extract E1–E4 (the extractor at the end of this file prints and checks the md5 of every embed).
2. Build, compute, write the checkpoint.
3. Scan every file you wrote with E2 using the base list E1: `python3 t1_scan.py T1_base_author_20260919.txt <files>`. All files must be CLEAN, except that a file holding only the Q-D arithmetic may be exempted if its only hits are the stated inputs. Report hits by index only. (This file itself: the plaintext scans CLEAN under E1; the sealed base64 body of E6 contains chance substrings matching base indices 1, 9 and 10 (E5's body scans CLEAN) — armor-transport collisions of random characters, not references, the known class from earlier dispatches.)
4. Commit the checkpoint and your instrument on a new branch under `lbc_bank/second_leg/` and push. Record the commit hash: this is the pre-consultation checkpoint.
5. Only now extract E5 (and E6 if needed) and run `python3 lbc_2leg_compare.py lbc_chat_checkpoint.json lbc_cc_checkpoint.json compare_out.json`.
6. Report the comparator summary. For every MISS, state which leg you believe and why. A suspected first-leg error is diagnosed from E6 and reported as such; neither checkpoint is edited after comparison.
7. Commit `compare_out.json` and a short return note; open a pull request to `main`.

## 6. Tolerances (identical to the comparator's rules)

- Speeds: 1 % relative.
- 2D lattice constant: 0.5 %.
- Z₂/Z₁: 3 %.
- F₂: 3 % relative or 0.002 absolute (3D: 5 % or 0.0003).
- Static shares: 0.02 absolute (3D: 0.03).
- f_s and the moduli: 2 %.
- Sum-rule residuals: ≤ 10⁻⁴.
- Λ_c, Λ_u, energy crossing, branch end: 0.1 absolute.
- c₂/c_T at Λ_c and its maximum: 0.02 absolute; F₂ at Λ_c: 0.03.
- Boolean: equal.
- Loss-length orders: 0.1 absolute; ξ_req: 10 %; Eq. (3) coefficient: 5 %; 1/(2γ²): 1 %; drag coefficient C: 1 %.

## 7. Embeds

- E1 `T1_base_author_20260919.txt` (plaintext; md5 05302210cc4ceb70553acbe8379e9fc3).
- E2 `t1_scan.py` (plaintext; md5 6b86290090a8c84f1b1a0a99ec0bf697).
- E3 `lbc_2leg_compare.py` (plaintext).
- E4 `lbc_2leg_schema_v1.0_skeleton.json` (plaintext).
- E5 `lbc_chat_checkpoint.json` (SEALED, base64).
- E6 `lbc_chat_instruments.tar.gz` (SEALED, base64; the first leg's scripts and outputs, for diagnosis only).

The md5 of every embed is in the manifest below. The extractor writes each embed to the current directory and checks its md5. Run it for E1–E4 first; E5 and E6 only after step 4.

## Manifest

| embed | file | bytes | md5 | form |
|---|---|---|---|---|
| E1 | `T1_base_author_20260919.txt` | 143 | `05302210cc4ceb70553acbe8379e9fc3` | plaintext |
| E2 | `t1_scan.py` | 1,967 | `6b86290090a8c84f1b1a0a99ec0bf697` | plaintext |
| E3 | `lbc_2leg_compare.py` | 3,934 | `d3fe406a65fb6586d5979b45d27a1419` | plaintext |
| E4 | `lbc_2leg_schema_v1.0_skeleton.json` | 2,310 | `d8235acc8547dac6d838f9f01f139a84` | plaintext |
| E5 | `lbc_chat_checkpoint.json` | 3,851 | `299afd1129430396fbe809913742de21` | SEALED base64 |
| E6 | `lbc_chat_instruments.tar.gz` | 66,848 | `7773283d5b3f0efdfaf259fb321c8c68` | SEALED base64 |

<!-- BEGIN E1 T1_base_author_20260919.txt PLAINTEXT md5=05302210cc4ceb70553acbe8379e9fc3 -->
````text
# T1 forbidden-string list, base stratum
# Recovered from G-2a-L1 dispatch (0c5588ee)
#
Mpc
Gpc
LIGO
170817
299792458
SME
GW1
3.19
0.019
Hz
GW
````
<!-- END E1 -->

<!-- BEGIN E2 t1_scan.py PLAINTEXT md5=6b86290090a8c84f1b1a0a99ec0bf697 -->
````text
#!/usr/bin/env python3
"""t1_scan.py — T1 forbidden-string scanner, G-MSCS1 (frozen with the gate list).
Rules: pattern lines only ('#' comment lines and blank lines ignored); case-sensitive substring;
bare numeric patterns (regex ^[0-9.e+\-×^ ⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+$) under the contextual numeric rule:
a match counts only if the maximal token of numeric characters containing it equals the pattern;
otherwise it is logged as a formatting COLLISION (not a hit). Hits are reported by pattern INDEX only.
Usage: t1_scan.py LIST FILE [FILE...]   -> exit 0 clean, 1 hit, 2 usage.
"""
import re, sys
NUMCHARS = set("0123456789.eE+-×^ ⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
def load(list_path):
    pats = [l.rstrip("\n") for l in open(list_path, encoding="utf-8")]
    return [p for p in pats if p.strip() and not p.startswith("#")]
def is_numeric(p): return all(c in NUMCHARS for c in p)
def scan_text(text, pats):
    hits, collisions = [], []
    for i, p in enumerate(pats):
        start = 0
        while True:
            j = text.find(p, start)
            if j < 0: break
            if is_numeric(p):
                a = j
                while a > 0 and text[a-1] in NUMCHARS and text[a-1] != " ": a -= 1
                b = j + len(p)
                while b < len(text) and text[b] in NUMCHARS and text[b] != " ": b += 1
                tok = text[a:b]
                (hits if tok == p else collisions).append((i, j))
            else:
                hits.append((i, j))
            start = j + 1
    return hits, collisions
def main():
    if len(sys.argv) < 3: print(__doc__); sys.exit(2)
    pats = load(sys.argv[1]); rc = 0
    for f in sys.argv[2:]:
        text = open(f, "rb").read().decode("utf-8", "replace")
        hits, coll = scan_text(text, pats)
        print(f"{f}: {'HIT' if hits else 'CLEAN'}  hits={[i for i,_ in hits]}  numeric_collisions={len(coll)}")
        if hits: rc = 1
    sys.exit(rc)
if __name__ == "__main__": main()
````
<!-- END E2 -->

<!-- BEGIN E3 lbc_2leg_compare.py PLAINTEXT md5=d3fe406a65fb6586d5979b45d27a1419 -->
````text
#!/usr/bin/env python3
"""lbc_2leg_compare.py — comparator for the second leg of the paper-cited LBC numbers (schema lbc_2leg_schema_v1.0).
Usage: python3 lbc_2leg_compare.py CHAT.json CC.json [OUT.json]
Every leaf of the chat checkpoint is compared with the CC value at the same dotted key, using the first matching
tolerance rule below (fnmatch on the dotted key). Missing on the CC side = MISS. Keys present only on the CC side are
listed as CC-ONLY (reported, not compared). Exit code 0 if no MISS, 1 otherwise. Free text is never compared.
Tolerance kinds: rel (|a-b| <= t*|a|), abs (|a-b| <= t), relabs (rel t1 OR abs t2), le (CC value <= t), bool, str.
"""
import json, sys, fnmatch, math

RULES = [
    ("2d.*.astar", ("rel", 0.005)),
    ("2d.*.c2", ("rel", 0.01)), ("2d.*.cT", ("rel", 0.01)), ("2d.*.c1", ("rel", 0.01)),
    ("2d.*.cT_30deg_kf005", ("rel", 0.01)),
    ("2d.*.F2", ("relabs", 0.03, 0.002)), ("2d.*.Z21", ("rel", 0.03)), ("2d.*.S2", ("abs", 0.02)),
    ("2d.*.f_s", ("rel", 0.02)),
    ("2d.*.fsum_resid_max", ("le", 1e-4)), ("2d.*.static_resid_max", ("le", 1e-4)),
    ("hydro_g22.static_share_minus", ("abs", 0.02)), ("hydro_g22.F_minus", ("relabs", 0.03, 0.002)),
    ("hydro_g22.*", ("rel", 0.02)),
    ("3d.F2*", ("relabs", 0.05, 0.0003)), ("3d.S2*", ("abs", 0.03)), ("3d.cT_*", ("rel", 0.03)), ("3d.*", ("rel", 0.02)),
    ("melting.any_c2_ge_cT", ("bool",)), ("melting.ratio_*", ("abs", 0.02)), ("melting.F2_at_Lambda_c", ("abs", 0.03)),
    ("melting.*", ("abs", 0.1)),
    ("loss.drag_prefactor_3d_coeff", ("rel", 0.01)), ("loss.xi_req_main_m*", ("rel", 0.10)), ("loss.eq3_coefficient", ("rel", 0.05)),
    ("loss.eq4_bound", ("rel", 0.01)), ("loss.*", ("abs", 0.1)),
]

def leaves(d, pre=""):
    for k, v in d.items():
        key = f"{pre}.{k}" if pre else k
        if isinstance(v, dict):
            yield from leaves(v, key)
        elif isinstance(v, list) and v and all(isinstance(x, (int, float)) for x in v):
            for i, x in enumerate(v):
                yield f"{key}[{i}]", x
        else:
            yield key, v

def rule_for(key):
    base = key.split("[")[0]
    for pat, r in RULES:
        if fnmatch.fnmatch(base, pat):
            return r
    return None

def norm(s): return str(s).replace(" ", "").lower()

def check(r, a, b):
    kind = r[0]
    if kind == "bool": return bool(a) == bool(b)
    if kind == "str": return norm(a) == norm(b)
    a, b = float(a), float(b)
    if not (math.isfinite(a) and math.isfinite(b)): return False
    if kind == "rel": return abs(a - b) <= r[1]*abs(a)
    if kind == "abs": return abs(a - b) <= r[1]
    if kind == "relabs": return abs(a - b) <= r[1]*abs(a) or abs(a - b) <= r[2]
    if kind == "le": return b <= r[1]
    raise ValueError(kind)

def main():
    chat = json.load(open(sys.argv[1])); cc = json.load(open(sys.argv[2]))
    assert chat.get("schema") == cc.get("schema") == "lbc_2leg_schema_v1.0", "schema mismatch"
    C = dict(leaves({k: v for k, v in chat.items() if k not in ("schema", "leg")}))
    K = dict(leaves({k: v for k, v in cc.items() if k not in ("schema", "leg")}))
    out = {"pass": [], "miss": [], "cc_only": sorted(set(K) - set(C))}
    for key, a in C.items():
        r = rule_for(key)
        if r is None:
            out["miss"].append({"key": key, "why": "no tolerance rule"}); continue
        if key not in K:
            out["miss"].append({"key": key, "why": "missing on CC side", "chat": a}); continue
        ok = check(r, a, K[key])
        (out["pass"] if ok else out["miss"]).append({"key": key, "chat": a, "cc": K[key], "rule": list(r)})
    print(f"checks: {len(C)}  PASS: {len(out['pass'])}  MISS: {len(out['miss'])}  CC-only: {len(out['cc_only'])}")
    for m in out["miss"]:
        print("  MISS", m)
    if len(sys.argv) > 3:
        json.dump(out, open(sys.argv[3], "w"), indent=1, default=str)
    sys.exit(1 if out["miss"] else 0)

if __name__ == "__main__":
    main()
````
<!-- END E3 -->

<!-- BEGIN E4 lbc_2leg_schema_v1.0_skeleton.json PLAINTEXT md5=d8235acc8547dac6d838f9f01f139a84 -->
````text
{
 "schema": "lbc_2leg_schema_v1.0",
 "leg": "cc",
 "2d": {
  "44": {
   "astar": null,
   "c2": null,
   "cT": null,
   "c1": null,
   "F2": null,
   "Z21": null,
   "S2": null
  },
  "28": {
   "astar": null,
   "c2": null,
   "cT": null,
   "c1": null,
   "F2": null,
   "Z21": null,
   "S2": null
  },
  "22": {
   "astar": null,
   "c2": null,
   "cT": null,
   "c1": null,
   "F2": null,
   "Z21": null,
   "S2": null,
   "f_s": null,
   "fsum_resid_max": null,
   "static_resid_max": null,
   "cT_30deg_kf005": null
  },
  "16": {
   "astar": null,
   "c2": null,
   "cT": null,
   "c1": null,
   "F2": null,
   "Z21": null,
   "S2": null,
   "f_s": null
  },
  "14": {
   "astar": null,
   "c2": null,
   "cT": null,
   "c1": null,
   "F2": null,
   "Z21": null,
   "S2": null,
   "f_s": null
  },
  "13.5": {
   "astar": null,
   "c2": null,
   "cT": null,
   "c1": null,
   "F2": null,
   "Z21": null,
   "S2": null,
   "f_s": null
  },
  "13": {
   "astar": null,
   "c2": null,
   "cT": null,
   "c1": null,
   "F2": null,
   "Z21": null,
   "S2": null,
   "f_s": null
  },
  "13.25": {
   "astar": null,
   "c2": null,
   "cT": null,
   "c1": null,
   "F2": null,
   "Z21": null,
   "S2": null,
   "f_s": null
  },
  "35g6": {
   "astar": null,
   "c2": null,
   "cT": null,
   "c1": null,
   "F2": null,
   "Z21": null,
   "S2": null
  }
 },
 "hydro_g22": {
  "f_s": null,
  "alpha": null,
  "M": null,
  "Cxxyy": null,
  "mu": null,
  "gamma": null,
  "F_minus": null,
  "c_minus": null,
  "c_plus": null,
  "c_T": null,
  "static_share_minus": null
 },
 "3d": {
  "c2": null,
  "cT_min": null,
  "cT_max": null,
  "c1_basal_q015": null,
  "F2_basal_q015": null,
  "Z21_basal_q015": null,
  "S2_basal_q015": null,
  "c_kappa": null
 },
 "melting": {
  "Lambda_c": null,
  "Lambda_u": null,
  "energy_crossing": null,
  "ratio_at_Lambda_c": null,
  "F2_at_Lambda_c": null,
  "ratio_max_metastable": null,
  "branch_end_g": null,
  "any_c2_ge_cT": null
 },
 "loss": {
  "v467_best_orders": null,
  "v467_worst_orders": null,
  "main_orders_recovered": [
   null,
   null
  ],
  "main_headline_orders": [
   null,
   null
  ],
  "band_orders": [
   null,
   null
  ],
  "xi_req_main_m": [
   null,
   null
  ],
  "eq3_coefficient": null,
  "eq4_bound": null,
  "drag_prefactor_3d_coeff": null
 }
}
````
<!-- END E4 -->

<!-- BEGIN E5 lbc_chat_checkpoint.json SEALED-BASE64 md5=299afd1129430396fbe809913742de21 -->
```
ewogInNjaGVtYSI6ICJsYmNfMmxlZ19zY2hlbWFfdjEuMCIsCiAibGVnIjogImNoYXQiLAogIjJkIjogewogICI0NCI6IHsKICAg
ImFzdGFyIjogMS4zOTI5ODkzMTI3MjM1NjU3LAogICAiYzIiOiAwLjU5NDgwMzA0NjIwNjQwNjcsCiAgICJjVCI6IDguNjY5MTQz
MDM2Njg1OTcyLAogICAiYzEiOiAxNi4wNjUzNjUwNjc4MzIxNDMsCiAgICJGMiI6IDAuMDAzMjI2MzU5NTk5NDk5Njk5NywKICAg
IloyMSI6IDAuMDg3MDA3NTYyMTAyNzA5NjMsCiAgICJTMiI6IDAuNzAwMzEzODQyMTA3NzQ0CiAgfSwKICAiMjgiOiB7CiAgICJh
c3RhciI6IDEuNDM0Njg1MDM3Mjg1MTk3MSwKICAgImMyIjogMS4yODYxODkxMTc2ODc0NjksCiAgICJjVCI6IDYuNjMwNDczMjI4
MjE5MTgyNSwKICAgImMxIjogMTIuNjUwOTc5OTQ0MDY2NzQ4LAogICAiRjIiOiAwLjAyMTM4NDgxMDk2MjU1NjIwNiwKICAgIloy
MSI6IDAuMjEzOTg5OTUyMTUxNTczNTQsCiAgICJTMiI6IDAuNjc2Nzg0MTg5ODM5OTg4NgogIH0sCiAgIjIyIjogewogICAiYXN0
YXIiOiAxLjQ1NzQ3MTAwODc5MDMxODIsCiAgICJjMiI6IDEuODAyNDI1Mzc0OTUyMDU1NiwKICAgImNUIjogNS43NzMxMDQ3Mzg1
MjQzNjMsCiAgICJjMSI6IDExLjE1NDMwMjA0MTc0NTM0NiwKICAgIkYyIjogMC4wNTEyODc4OTc5MDk0NDA1MzYsCiAgICJaMjEi
OiAwLjMzMzYzMDQzMzI3MzMxMTU0LAogICAiUzIiOiAwLjY3Mjg4MTYxNTI1MDE4MTQsCiAgICJmX3MiOiAwLjA5NTE3NTkyMjc5
MTI0MTQ3LAogICAiZnN1bV9yZXNpZF9tYXgiOiAzLjIyNjM2MTE3ODIyMTI4MmUtMDksCiAgICJzdGF0aWNfcmVzaWRfbWF4Ijog
OC43MTczNTQzNzE2OTAwNzhlLTA4LAogICAiY1RfMzBkZWdfa2YwMDUiOiA1Ljc0NjIxMzY4OTIzNTg0NwogIH0sCiAgIjE2Ijog
ewogICAiYXN0YXIiOiAxLjQ4ODM3NTY1NDM0NDg0NTYsCiAgICJjMiI6IDIuNjg4MzcxMjM5NDgxMDk3LAogICAiY1QiOiA0Ljg3
NjQwOTQ5MTk4MDA2NCwKICAgImMxIjogOS4zOTA3OTQ0ODEzMjc4MSwKICAgIkYyIjogMC4xNTkxMjkyNDk0NDc2Nzg2MiwKICAg
IloyMSI6IDAuNjYwOTU4Nzk5NjYyMDUxNiwKICAgIlMyIjogMC42OTcxNTg0MjY4ODQwMzE4LAogICAiZl9zIjogMC4yNzgxODU3
OTIxNTUwNDQ4CiAgfSwKICAiMTQiOiB7CiAgICJhc3RhciI6IDEuNTAxOTUxMDMwMzQ5MDU5MywKICAgImMyIjogMy4xNzE1OTg2
MzEzNzEyNjA1LAogICAiY1QiOiA0LjU3MDMzMjQ3Nzk2Mzg1MiwKICAgImMxIjogOC42MzUxOTE0MjIzMTE3MDUsCiAgICJGMiI6
IDAuMjc2OTUxNjkxNDEwMTE1MiwKICAgIloyMSI6IDEuMDUwMDA2MDAxMTE5MjI3NiwKICAgIlMyIjogMC43NDA1NDExNDM0OTM5
MDQ5LAogICAiZl9zIjogMC40MzYwODg5ODAzMzYyMzY3CiAgfSwKICAiMTMuNSI6IHsKICAgImFzdGFyIjogMS41MDU4NjYyMjQ0
MzUwMTMyLAogICAiYzIiOiAzLjMxNTQxMjcxMDQ5OTg2NywKICAgImNUIjogNC40OTE1MDcyNDcyNTA2NTA1LAogICAiYzEiOiA4
LjM5NzA0MjUwMDU2NDcxOCwKICAgIkYyIjogMC4zMzMzMzg2OTgyOTI3NzU1LAogICAiWjIxIjogMS4yODM4MTQ2ODk1NDY3MzI4
LAogICAiUzIiOiAwLjc2NDcyMjc4NzQ4ODQyMjIsCiAgICJmX3MiOiAwLjQ5NzE1MzE3MzE2NjM3NDg2CiAgfSwKICAiMTMiOiB7
CiAgICJhc3RhciI6IDEuNTEwMjEwNDE3MDY1MzU3NiwKICAgImMyIjogMy40NDk0MzMzMzQyMDIxLAogICAiY1QiOiA0LjQwODAx
MDU2Njg0NzE3NywKICAgImMxIjogOC4wOTc3NzEwMjQ5NjgzLAogICAiRjIiOiAwLjQyMTc1MjkxMjU3NDMzMjIzLAogICAiWjIx
IjogMS43NzIxNDU1MzYxNjUzMDksCiAgICJTMiI6IDAuODA2NzMxNzQ0MDk2MzEyNywKICAgImZfcyI6IDAuNTc2MzEwMTYwMTQ5
MzE3OAogIH0sCiAgIjEzLjI1IjogewogICAiYXN0YXIiOiAxLjUwNzgyODU0MjIwMTc0NTIsCiAgICJjMiI6IDMuMzg1NjYzNzgy
OTkwODY0NywKICAgImNUIjogNC40NTEyMDA4NDUzNjYwMzE0LAogICAiYzEiOiA4LjI2MjAwNjE1NzgyMTE0NCwKICAgIkYyIjog
MC4zNzEzODQyNTM1NzYwNjAxNCwKICAgIloyMSI6IDEuNDcxODE0MjE3MTQyMjI3NywKICAgIlMyIjogMC43ODIzNzAzNTc4MTg3
NDgyLAogICAiZl9zIjogMC41MzM3NDQzMDY1ODYzNjk4CiAgfSwKICAiMzVnNiI6IHsKICAgImFzdGFyIjogMS40Mzc3ODg5ODYx
NDcxNzgyLAogICAiYzIiOiAyLjE3NDA4MTczNzAyOTI5NCwKICAgImNUIjogNi42MTc0ODk1MDI4NDczOTcsCiAgICJjMSI6IDEz
LjQ5ODczMTM4MDQzMzEyLAogICAiRjIiOiAwLjA0Mjk5NDc4MDM1NDY4OTMxLAogICAiWjIxIjogMC4yNzg4MzU0MDg2MTUxMjYz
NSwKICAgIlMyIjogMC42MzM1MzIxNDc3MzIyMzIKICB9CiB9LAogImh5ZHJvX2cyMiI6IHsKICAiZl9zIjogMC4wOTUxNzU5MjI3
OTEyNDE0NywKICAiYWxwaGEiOiA0My43MzE4ODMxNDc0NjQ5OCwKICAiTSI6IDkxLjYwNjc1NjU3NDI5NzY2LAogICJDeHh5eSI6
IDMwLjUwODA2OTUzNTU1NTI5MywKICAibXUiOiAzMC41NTc2ODc0MTc4ODg0ODQsCiAgImdhbW1hIjogOC4wMTUzMDM0OTM3MjQ3
MDEsCiAgIkZfbWludXMiOiAwLjA1MTc4NjU5NzM4MDQ3MzA0NiwKICAiY19taW51cyI6IDEuODE2NjE2NDY5NjkzMDg0LAogICJj
X3BsdXMiOiAxMS4yMDkwOTQzNzYzMzY4OTYsCiAgImNfVCI6IDUuODExMzY1MTkxNDMxNTgyLAogICJzdGF0aWNfc2hhcmVfbWlu
dXMiOiAwLjY3NTI1NTI1Njg1Mjg1NDMKIH0sCiAiM2QiOiB7CiAgImMyIjogMC40NzY2NTcwOTc5NzMwMTcxLAogICJjVF9taW4i
OiA3LjMzMDUxMTc4MjIzMDY4OCwKICAiY1RfbWF4IjogOC4xNjc1MDQ3MzY2NDA2NzcsCiAgImMxX2Jhc2FsX3EwMTUiOiAxNi4w
NDU4NDMyNjg2Mjk1ODIsCiAgIkYyX2Jhc2FsX3EwMTUiOiAwLjAwMTcwNjkwNTM0MjY0Mzk1MywKICAiWjIxX2Jhc2FsX3EwMTUi
OiAwLjA1NzU1MDA5MjAyOTY2NDc5NiwKICAiUzJfYmFzYWxfcTAxNSI6IDAuNjU5MTQyMjI4MzU0MzgwNywKICAiY19rYXBwYSI6
IDkuMzgzNjQxNzM0NzA1NTIyCiB9LAogIm1lbHRpbmciOiB7CiAgIkxhbWJkYV9jIjogMTMuMDM4Mzc0Mzc1NTkxODE1LAogICJM
YW1iZGFfdSI6IDEyLjIzMzIxMzM0NTgzNDE1MywKICAiZW5lcmd5X2Nyb3NzaW5nIjogMTIuNTY5ODg5MjgwNzUxMDksCiAgInJh
dGlvX2F0X0xhbWJkYV9jIjogMC43Nzg4OTQxMDAzMTU0NDc5LAogICJGMl9hdF9MYW1iZGFfYyI6IDAuNDE0MDIxNDQ5MjIwNTA5
MywKICAicmF0aW9fbWF4X21ldGFzdGFibGUiOiAwLjc5Nzg5NDUzMzAwMzMxNzYsCiAgImJyYW5jaF9lbmRfZyI6IDEyLjQ3LAog
ICJhbnlfYzJfZ2VfY1QiOiBmYWxzZQogfSwKICJsb3NzIjogewogICJ2NDY3X2Jlc3Rfb3JkZXJzIjogLTQxLjk2MDkwNDMyNTQ4
NzM0LAogICJ2NDY3X3dvcnN0X29yZGVycyI6IC00My44OTExMzI2MTYwMjU1OSwKICAibWFpbl9vcmRlcnNfcmVjb3ZlcmVkIjog
WwogICAyLjc4MjYzMjM5MDI4Mjc3NiwKICAgMi44MDkyODM2NjYyNTUzMTI1CiAgXSwKICAibWFpbl9oZWFkbGluZV9vcmRlcnMi
OiBbCiAgIC0zOS4xNzgyNzE5MzUyMDQ1NiwKICAgLTM5LjE1MTYyMDY1OTIzMjAzCiAgXSwKICAiYmFuZF9vcmRlcnMiOiBbCiAg
IC00MS4xOTgyMTM4NDk3MTg1MywKICAgLTM4LjM5NTg0Nzg1MDQ5NzI5CiAgXSwKICAieGlfcmVxX21haW5fbSI6IFsKICAgMjI5
MTUuNTYzNDc0MTg2MzgzLAogICAyNDM2NS44NjQwNDQwMjA4MgogIF0sCiAgImVxM19jb2VmZmljaWVudCI6IDEzNDYxOC43ODM4
NjEyMDEyNiwKICAiZXE0X2JvdW5kIjogNC44OTA3NTY3NTEwNTY4MzFlLTI0LAogICJkcmFnX3ByZWZhY3Rvcl8zZF9jb2VmZiI6
IDAuMDc5NTc3NDcxNTQ1OTQ3NjcKIH0KfQo=
```
<!-- END E5 -->

<!-- BEGIN E6 lbc_chat_instruments.tar.gz SEALED-BASE64 md5=7773283d5b3f0efdfaf259fb321c8c68 -->
```
H4sIAAAAAAAAA+xbe2/bSJKfv/Up+hgclpRFSaTeynFxSc42BrP2GIkHmFlDESiqZXEkPkxStnTe3Ge/X1U3JUp2srO4mz0cdomY
Yr+q613VjzRb3/3uTxvPoNfjXzynv/zt9Nx+u9PrO33qNxi47nei9/uj9t13m7zwMyG+y5Kk+Fa/v9b+//RpttazYLrczbOkme5+
nzlIwP1u9yvydwaDzon8HdftOd+J9u+DzvHzDy7/N//S2uRZaxbGLRk/inRXLJO4UzMMo1ZVDGHbIoznMpV4xYXg+vku9qMwEEGW
5LkdLGWwEslCFEspZpkfB0vxJMP7ZZE3a7UPSZRuCpk3xFNYLMX1j+L9/BIgUdngEbdeW+SbVGZ5sg7nxxNwt1wkMfcM/DiJw8Bf
C4iukOOaEItpLvhhCIv1BhAWmR8UIcaY6dLPpV08hXkhZCyz+11DrP2iCAMpFuFWzi2A8NfoRiA8MXdla54tE1f4heqw7354TB4w
RTcbfwThqmzyxIfpFk8JSqb5dFsBhv4VCJsNDb73o+hkeqEGilefyvQ8nmbcgS787rY7YeZLCbWOkvlmvclFtLHEIsmYfWGeFFkC
kbZEML0VLLaaH8+FfPTXGzA0526/JIn9H0mWS+p4Q/Tb7/1wvQ6l/X7tr0IpMolaMDgXZrQDsln4yOWGOP/55vzD7bvb73+8FnFS
SItk5IM0oFtXjLaFq2k+E1ct1E9j8VbM0MekQq6qLEUmWGur3p9dIjaYntmfXeoLQGcif8gKE012d2ZZLRdwiDLuEG0UIAy6mNrE
XTOY1tFkowtgWC2UzyrlBo2t81jGA8iZCjuSMjF+nTzJzNYKvrDzTSTypZ9JQuzP03jTehDQQRHI9RpA0OCLOiaPN6JlugAeQ16f
NrO8yMBrsYnDIn/LKuEJp8mGF0ZpkhUi38FaEvz9mhNTizCSZVO8iSBAPxdxWltkSaQqmotFIXQPfLoNEdJPDYCaqV8sm2GcS7Cq
3RBGa5lEshWs/c1ctvKHYkqWl7bugdO0yJfOFLZ1H8b3hlXOea/qg6VfrOU9TX5bq/340y3wNlpFlGpgdrtlE2xbw571F4OhbDu2
Pwvmdm84n9uz9sy3F6NhbzSfySCQw1YegBnBMvXnFI6M2iWAum6z/Vb8cP7xmmbIk0VhvBXvPt2++8ic6vYG3YHTbg8Ho3bHGbpv
xfUHNIz6tdpcLpj99zKJphem3xAXDXEdeNcfWBGFAJN/nK3Dh40UaT9SomK3BGGt7Tz1YemPMiig/tBrGE4Eq53t2C5cWHLkF1m4
FRdNkhYB9B1MfSH+HfJo+lnm78w7zNputifWW+G7LxrbzV4dHVDButuB1tb9icWw3qF3BYzTAICJ9aoTeCOy5CnnUe+JY3WMS0N6
r8PYX99D4I/mO6t5+8ooMQPkmavo9qdhczb9lWCINATN6wJVvzJk3c8T7+/akwbezoTrI4UnNIz+Fpl8MK8Dq34dcOvVFVh+rbpE
Ml/eZ+HcjBoC/yiObKFanhH+aiiaL8lXXl3VZw7mOLu+rs9cfLwVl7t9vVPW6+nZsGBfs9w80DuXBehVMHMydmakH99Lwu0MbLda
GsFPIOuTe4IgjC1/FcGf0fGTU/cZv08QlsLvl321U1Zr9DJZbLJYzMMArsmDrH3HU7L0fBjmzPEUX70ZSpdb73KLn513CRd+6aJU
r7tnlzu8G0ypR6+G+Nn7uSF+8X5R6hxYStfJEW+noPFeNthrzfysIVbQYM+EDrIiwrGleTgN4W686yRGx3nhob4NLAp/4/XRr3ak
JinicL5kPyBzzzQdaXcboo+MzWoAWpGsPVQ57sGmvo/IZfjZziZfJS5vFGYcFCh4++I+fJSxsjcyTllkOwqLkfTBKhnnYbHbE8BQ
lXZidEpAEPLfrxO4XRXLiUJhrsJYIjaLv1yerf7y2W2BYwGSjbXcEsViJdPC2hvqdQCJ3cs74zowIL+fVijeNn+4uL4jRzMxS4uk
LpeuMQGhl0oDfuB4w/VbY3JGc0MFLEgIEUzV78p6h+vVhEVS6FgCourUj0RpKC0JF3upIC4LEsx4L4WMcCVPwdB9B9D5g9Dad5rv
0frZmNhZidMZV/2iqirosGDBFVZ7uU1Ne+4iLNXbzU4PfSyykXbvrK1MX67zCj5qXIlv08+LXSpNzWurGSCnMBViSilj+E0ztcal
LaT1krvElBbzehOxicKIU8LRqjAIhsoY7SGq1I0g7lEiDlGIQ6XqXkbSKlDUrcp+FMRVzz2M85XqT7gQt39gN0qjg1OU3orzUMtE
D/hpVXbOVqe9D4JU9J+vkBmFtQMrSxbloSKSMjRzXiAhjvMCuZ8FTyRM1JBLKkyYaWteWLA+aFyxAdfNIxut8OUHDDyImPAF2Lqi
DhHpPM3kIzqQvu3H0Oykhsh02GFqHMZHXkEhzmmFiUnqivkgwDrlPOqqXKbnZnkYDMbtBWI1Ke6+Mg/e9b2eggAAsH4zOq/zuHxg
eSD2X0Wv3RaeJ7qj0TGhSjMaSuCl5gEImIeK89WZluQJTMVZmDLSXmavoMyaGHJuc5sl/o1cZz3ytyaFA2qxYCMzsGD1EgMtqPPa
1/BRoXhDTgBIufXzEPoN83oRhNDZwx8grDwFyDunkse0NIT0TP6yWgcNRrjeeNFGh6Bq/bVHk+j4E/lhbGpFySTF3ecvXCjAW85b
m/TSzuF7rZk7abqqZoblGYtKh7FK7sb5XkN8Dz/sIIiVxkNwadSdgYK2tDQjI1kYd9QwAT3P3OMP8g+TcXO4+EK06KpoQ3V91DFh
upa+y3rzuYK2XbTHzfbiS24ZDYHFZb70brONtEqC7wwCYExo7Uaslp7CTWoOqlK0oSJPqCoUL8FDAvMGK2yssV9Zv44Fr191zPPX
SXwvtkqt+Pt0MatcSUUKZNirFRk28s62y+lAdzI+Mvy1P6OMQTkcYws6zdVKJQ5gvWnsqIZzidXKsk6cQvH0m6SnU5LVYyUVIVmq
BKRbinePFul08XRnnCOKKY7hCws2cmOqfG1M6qsVud3jkfndwngGSV+mz6vVFxbM4thvlLqyyCeasdxfrDwaMaYNBe95oXThb1WG
Ra5mVIk5bU2gsE78wuRU049NTHtnbKckDdIJKu10aWIdKwS4mlN2E2CdXfhxkbPkKehirjychWvKmbA2CWSMFeUaGrhYSHi9AIZo
slCwdiFfKH1KnEBDJaJOk4W5Txjl1mMJy536BWUk/4OsL45WJnfOmdxSL1BwxwNQsZtUcpPs22pxYVWy1b+mEdqVZWxVXLvkSNx2
VKZy8Ahl+xu9pVPdzzGPdnMUdJmCZFrMMDecsyXQUp/2UvUo4Zgytd26bJ/JyGoty+gmU5cAuAcIbr0CgwoHKK4C45ZwaAOCepTA
1K4OrXDNrtopsdU4q9U59nJcPRFL73kJfX3m4rjZI31deu6yrHJ13ccQC/dsniMNf9aT6BYT0YM3gcZiHm3UztN/iWciluhk9FTX
R9pIEkc+FNWv2cEbcXXYBTP3u16a4dt0Stp24Dlr3dY7cE1XlAK42jLbME7zbXskgC1LYFsRgR5fFUQJci+Pq62robp7qKfiuCpF
cbW10f+FEK48RSPkAIZfbTVLXVV6jfdXmu9v4ayzvLDLbbNHKcy8IJu2lDRIAkQw06qF4MovrzJbbf5pbSR1TiNSSVbsA5cbYol/
e4Zw0a6W7ZN2W3VguB9oBqW80Is0gm6k0F/CrVtfljwlm8sT4LPDozJKvduokNsRSrsTwe9OBb87CF5NuSvtbleV+xtxvMnJG2F5
SMsR1aLmzGnO/HhO8O94TlSUc0abab7kafNy2vxI3XJWt/xE3QDhVN0I6F7dGKyr4bp7wKcah25a5XiArYa9UDwdFiZa9N4zy0fp
m+K+93yly6bSUa/UT+Sw0UZtEFveM0/A9S31rbX2IzeVympUwufC0BBtNbnVcr1nExbyQZd4zKuKqnZ8X2xxc+v9lFQX74jeEX9H
Vb984iN0hV311ydd7OWRGylnN2kqm2ayaaIzmueFHiPK0nbfzqaNWqRFfMghCplFwtxvobOlauA7hf9OEbBTFOxekLA7JWH3goTd
KQm7YxKmbBU8oc3z2TzdGc92TMheYXjg5MXZApJEbtGeSpi7sa6ZKu2x/ub0R6vmIR3mcOPxu1EGOE//NsSVd4UsAm7Ru6LiB9bd
KzrJYMX+oI41WDOhsB5/cPkjfX882bQ6epgOj9+NknOe/m1wioc/uDyw+yjnOjp7Qp5FVKhzDr1Nf8igdKupqbvS8xCCPEMleyq3
+NtYKXNKOKV9f1qnOza+9/1enJPUK+ck8b6bOirJUWXV1fT1/SnJUUY8D/NA73DwOUndt7v12aE9IHcWROo45Yx6W7SHZvq2/j70
vC2PVA5oBHR8yqcleZ2OSuL6Ps7TcxHxkQt3sgP2dpiPv96Ki5SJv4gO0FZ+mvr68EWTVSGqdXW0D/6GDwAhI3MTh/429Nf7pZCt
M1/rRaqcp1KvkZTGHlbIwTSFPnv7VJ3ZBWxpBRRMozB+2RjpxtvThltqeFU1gykzw1M8QRasIV9E9M0YXKSvD/3zg+pLZzWUTh+t
I+sXEUWSE9QwhEB+ZUR6NCL9Ks6KzVM+5tLomphOyVN9nAEYQSBusBBPOaIk+1WuLMOpnuU1VFvlcO3UkE56x7bHroRee/ujAlng
wTMdTJmdExUrTtK4Y7uvGPzEUGdvzfkmSnOTGtThQFx4jvXS/fFmdZLK2Ez0gduvSRibP/502xDG4TSdQBoYbjwZFh2jLcaHWbBi
g0daHKZpkJvxN+tC8ROOKlyI6RS+SU6ntHNlTKe0/zKdGsrVqM2Y2m89/2+2Uh8cn4Y0XViEMp9yUPvfvAzy7fsf7b7rdk7uf3QH
/e4/73/8PZ6v3//4tItmyZq2Hkgf8vJmx0FRxMMmKWCJobqWwXokTDoP/upNDug27VmFxWZOB3Yi50NWBEnToWVPaD40nizl/cXD
Z1fcXdgt8+kzAgad96OGtr4vznTdma6bwHPa3EDxBOtNOpS33tZMdEcDBSB95K9P/M8OJTrvf3ncL9TtA4DoaBCq1aQQS+3sZSyM
a4k7lPGhLgnsYQOmdTTRRAj7j+I/JTxMEq93tFmsYBK7sFC60mQzZEzcfSV0bSKRbWh1g4+LVsBoOy3tcD+7e99b0nMcQD9T/ATk
Hp0rHGAD3jqMwkJvcwDJJBkDZ/oK6sxafLXRaSUxG/f67DaPLiro2wh5WntqiIeGoMQyh+dnFcpNI4nkvS8eBG0spkke0npXO06g
2UAaRJkhOe8GM6I6di8OjaDKhq5egZRrFkJEce0N+fwUWZtUC0NS0UcsthchVPZP/j0dcoR+LKCkG3VNSG6R3ZNWssI3VO/dFI4b
ztAa0x0LmfnQV14cwAwShEIq19CCqR+QodTNJ3pT9oK0wuasqP7A+RgGEH5xHT26aIIunYGkQ19K9OqUzjGgJ3WyCACQok7t+IAJ
rd3ajWKS3KbAhbIuOjD+JtDta8CsGkJ3g1LAE6Yj36G7Kqn7ks1BXkn3eBoLzE79rEACtt+1zsktkBrAUlsw0jGZd8Wy68Lckmnk
ZJDmljNC+qEkhBof1DBLNJvNGmUHpUrR+h5iMU0wvQWeWs18M8tN6F2uU40teATK4NbvZVGmkofJwCzzhtJmmgc8ovsQQEr1qH8u
8SGbpV+YMHpyaL9h+YnT1prOH0oftrUoLp/CvNE3msTYaBwRooizj9EEV1s3DKdN3IUNshJDpcP5RtKZOfGDsvZNHsb3VdQOjKyV
2Tc7oTL51t/VNLoESzddhImEg3ZiIUSaWvv7nYArHIsbdqXkou2ve0R2iHuudHxrP+zsa360pZwo0fuCQTdKwlglEme0GmsA0G7a
OqHhpM97hil57ZEl1pQxgPhTfqfU+kdxaGLNrqKnKDK1jycw6d6/E4M7yhZO8TEVQnVSNj2CpFrhPwxpuTrR6YtIkaqMksX2m2FD
SW0stzr/EwgHVe7MoMvrJIevZKWgrTwoIZ1ChHlBN0CZw+RUq8pDomOytBjYZZYpxGFIJP18Q0k8b92FwrwXdN+LrgosE8+pPfpr
Pr9CaSwcCg/4sdvN9qjnDHpDihVj0e00Bx1nOKSoMRbDZtvpddoIH2Mxcpr9dn/Q/1KjpI0g5QhTcm6qJUmm7kJm5KHA/Ztkvdcx
mhgpwdZqxjzUJDFNmZdT9pFciyr2gQocWFcZXLJwYZBpafrHnAJ4zwRKnSmR46ByWpbrqpzrMphtasZa3rNJDTaN5vuKqf7WXcu9
uYWBQUpoGKOQ2ysEI6c+n6EcY6HJSvkzdb9YJTidASnL9J5LZrYUh8dNd/HFINl+K0OpBavKIr4MN0g/ann31I+r9SNdoqGtAItX
kd9EtEIQRTwkQCvXekUEBmF4SJXsaqokTC0a2D9vZBGz8q7FhH0lQaq9OwmS714GR0Kgd6q6GPPRV/eXzFFDOHQZi3VWaav7pXZD
Yyo62NP0UE70zqqRur5DPZ/hOhLscGSXXn19jJud6nih7/se6XhPAX3XYGCneq52c15X6551vJ1ILFLbes8Eatxsyy+lkmd3bX2I
bv+x1OucK96qVBrqnJM/oqtK0LU7Z2Lz97jZkaRa/9dLon+oR/3/j86cdyV+pzm+vf7vtjtu72T97wy6g3+u//8ez3NNGL4BV9Xs
DHujfrffbrtDZ+Q6nQZaArS4Tbc3QtOoPRx2h+6wyy1/8iODY3DXHXT7I3c46PQ6vUGX2ugqLRrv4DK6Lu33DfjdH9bEhNolGvvD
ZqeL8O30O/3OqN/jgdGGMHEGzWHbRRPeo36/N6ImuGK00YXVTrvX7fUGTncw6nScwbBPzdeXNLLT6/H8waYgxF2+02rQbWeNzjN5
MeOBITk93orE2lQ3CgI/cPrugJKM7gC62XEbumHY643a3YHTGbVHTqW63+sMu2BOZzBq9wadsn406HaRrDDLOv2Rmoo2/0ej3mCA
OhDQ+W/2/ny5juvK9wf9N57iXFR0C6DAg8y9d05UoaJctqSqW5LssGhXhXhZCBA4IFHERADUcGlF9EP0m/R79EP0k/T3s3LO3AcA
Cdry/f0MW+BBnpz2sObvWiuE7nha5KVG5YpEs1LZbOjHLUOSl0UeKs1ECL5oTg9MUFLoJ3VZ5oPvj1eFnpdoUkOal83hbJno5TMd
cGma6m05/Lwe/XfDweumaRbKInGa2zwpqvY1fCoKFlFm3LsoV49d3r65L+tFLLX4Gm/ef+c0O77IvQ+az0rXB33XDmEZUj1MO4s7
l1Wlr7L2sqoostTnufNF4dIk62+pd/SZ9kbwZanp06+0mSrtmRCSkIZMN/XB+dXjpLmoWibOV04zoi0aEnv9shtZKFySOc2bBpJ6
XebT4fS8Gc6PlsznWZmkZe4CV7WDyYL4WKpp0BYoysz3o6mWLtUYqtT50hW+Gk4dW6nIxPPSQgtfDMZZaXqYNl2hjeVd0d9Ql5VZ
oiuT0mUiAp/33yVLp9kucpeVpWiqLItmurOlc6xolReaPlc6LUXSXJSj11VZUmnSslyjGq5SlodSU67Jq7ThMj3LJ4PpObaQwGgL
pUUiVsES5Oxk3020FlPbpNL8i1cUYTgiDbYUyRWp3i8fjdYvXaWR+CrVCmXZcPagoTzRlhQliWOxqs1eCEttEI1HS6GRBe+GM6Tb
5cEF3UwbpSh3+hf3hSYmLao01a1DPwWlRqFfaZZo8f1gbfWcQvtKBFqJa6Su4sWrwfRcT6dHzCwNTgugB/gyKdoV8M55cZtSd0vE
eobjLyQfK/FeUWNRVDYF3cJp/0PwmrSQuHywt7zGUyaQe16VXjvP97OTLfUUXVKRN1MMKS8RNSRiQykcWfOW5d0KOfajaCQVb9K3
g+3D6mm3pbpblafasGm/f7wGnKba4FmZhcBKTsjrWOr5/hW6sbHkqvth/ya+mcU6LtSeJiba/KSiq9Dy6E38KEcnV6vDm1pQiAxF
OqX2utcr1G+0+VLq/+pov9u3LLy4nWa20I7NsizR8tSTuPlVQqxLJ/llVmjKQhFcksCou9Fvfn9xqhOKpezSUrxe/N5pBzcP09vo
S8ChB6f7X36NnfbzzkQK+YgQ0hbRqmmaC7HiEPJuk0pC62W1LkUl0g6dtClrIZFW+r9YQr/XRe2lGKwM40q7Lm1pUcIEaa+dIRbc
CTmkjXibxJBkmvh51e7y0kkngH8XSeld1QkbLVOqBydae33bSxuxbs1Doq/EAnx3OJQ5Yl3yT0peWqwVQmLj4u1SRHJxWN/zIi2M
KFrahiRryKpyuN3FbApEc+6gxirrWbwYRS4alWwVzemMUA6/03qiYiCnC5TOIYNxnqFlInHO4rKq4xYS6ZlJG4llCeK0ZyOaQM2o
9ARNTpEXLZkUkgOZFjTIhkY2p3DSdoJ1WOsm8SnigvL0nbtNCMHXvJQdjSa07xuWpMI5salQSenI8+FQ2JeiW6lZrpKI8D2J5kst
FG4VI3tNbT87fuk1y+IxmlQJ0DQb3FKsz9kCifOI9eTDyXFS6/SOesUUzdAPeGwS8kLMXwQugawFSfJ+62Xe5eLkITOJ3N9QHLgS
62H3pXoPBzufMJGYECoRaWWZa4l8u8P9MmV1vFZM+pcUmcGIpI+Km0r31USUWc0xy5ZjSr2RJNbr6vG1oC47Hqxd4vW9RECW21Xd
DQvWW1tI216XFsM5EvMVO9eDJFUS7c1+inLnEhYROpEI990OF5NyYqUS/uIIg1dwS3hvmiBgvZbJFxMhPZdCudYuk8AVVyg65VTL
Lf4mpSFB1mmvDESNjcX2h9TcwjSoot0IWmlm2Pkg0yAZfKVth7Xg2SiFcaChzJf2l0M5ZYUO7QZUmZiuIM1PnK6Qwlzm2WAHOY1W
F+mDSzAgBpo1+pXMEW0Vlw52ZIFWpJPF73Sprp+Q11ohhLwrwx1CSC8jbSzL1gkh8TItZkANkYhZL4Uky8SWS5QQaZKNBdDLoIa1
pHon0UEQJWsj5x9JCOURISSa1+xr44qKoaRe2GjNAhJBklD6Yi+cSuk1Oadrkqt8IIRyraVmSbSHGG33TS7CyKRXiYumkjidTqWl
zdg4Uuk0xk4hzsT4JBYzFOWhVNEm9onJINlg3dYrlrbn0ANd2piXzXEtqo64YHx/xGZHLEQWlvReSRupV4W2YbuXNLGSswnajnZm
0W93qbh6TiaxLSYs1csU8257wlMkDKAFTceQAxc8TPtTd9PEasv3l5XS9QtZJWmCUaolH7IQrF3JSSwECYRu6GYiy473ZnxKqEhL
7rQxL1sDQ0j0ARfzafsciQXOLZ0eJMV4wkGmAkgTrZFKCmmhs7Qnae1dJlVDTHNJ8KGAFmGKNCUYpYtIgQnDudEO0RbTpZpoDWTI
QWSzYkvoDG38yg+/0sEyc0xZgV40YiBOFpBZGohv/TNgr8ZzZNQUqMy9FGQLSaeShSgldjA1GLiOk724jWyDcqrjx6SPJhelWHxf
qkBedlu+gmVJcmv+i8yNWKUks+M/SXZthiE7LJeZRBjiW7JCLCQdma+VjECRgCxo8e1yMEGSGOxG8UL9pzlMi+EEadlEAuL1Yk0y
vXrzWkqwpKbGK31EHLB9cynwYofitxJJTlK/117ECYNkFnwplzkRTIcq7xQ/GqoIzGPAtmPhWCUhW2A6SmAOLR0EaIla4REyI6or
Rf5oigkmSvDDTafFlFDQ3si1hiEMpZa2ucxAbatcFlfmx9JHnA8dRjpcFfIBXWU4JKRQF2hMUjK6dZWel/B28LTayOk2sDSGQmQl
IwzZGWa7Z53sqeBQd8oekbdYxDrZI/UDfwUOmqSVUDHZE6ijINbsGUjj9ZmIHs2RNLlEep1sA98+8sGSZ50TLqucmJ5IKNcydNq1
6F0zKfafoeX6jhVKQ9AYMhw4hSzV7nxtSnQvjxvRd945FkV0nMGmRXJ5PjuMt6b3YolUKkhaOjI+yd7ZpmM4VbQBpXBUbn5cjCNt
HVTYS5Kneg8WVtO0VvJIFGgLenyqrGASWiLARwXzxqnm8pFPSOOXcNWbVAVeoXTEKLUBpTSUMs7FlhI35B+a3wJlQptZxM3u9K3O
W6J7SR3MioAvsb8jTji4GF5PsWvsmu5RWq4Cq6cQJUviDZ2BeAgTvHZSkyXqfP8siTmtXCZ+BZ/P+Mr7W8SPtK2g2RGjRAHpnD74
qPBGm1MtTXuPBwTjsFWlxKNvY2D1njaxNmnCMGycm9VQMBVi+DJhJRrELRMI23WWRIWJp8k2h3Ex8L0gfSSaq6LC2VMiu9tHiW9I
9mAaYYaNfIHwBs2l+GhiM94/KpPsTKS4yqwtJQTgcBP1NWL+FBiuUn0Q1a5VoqRpmLNetCW+WNlLd1Mkmx9FDVebFO/ED19Oeloq
rVqjgUebbt1JGU1AhtIjtczVJqJrn8aCV+wd8ZTa/ummSFNX4WmRUMfP0TmaZfxV5vxFGc6ykVNPnFqcOdf/Jab5pmOyGZZPkcNk
xYD9nfZPKW0ixW8uOut8pNJDJIIJOYiLFLhm+x2KcZ2L52hvozyGMhuKGU2paE/7qkB0Z/3sZJpVrQP8VyqjOY7a2ZG2lIptBShZ
TCXLR25cn0pvFUfGzIEEO3GfwVEk0AIiekBeAT+pKEg3Qs4M310ajNRmaWQlMy5TMbuv/YN60Ojxtzjh8KYmjUIekUHSN0UBJZKo
9Uyt8cJh8WbaMtLPQ/PyIx8cUUTtTqelqMw6fR8nnKUHvJcHTltETAzHpsbQSRrJHptDbQQtQW/8sCfF9nWqBFAvfxBKWhSUtNAr
bSJ1KXKZdHZRdJgdhrkXvbsWZiqy9UWGG6olShneFe6wnFiZ1iCbH/edY0p2UirZUbCp8NGGbK30kSjDq6XdnKAedcTsk8w8qg6l
shgQppflJ2NcO0Vv6RA1Q/0HF5WepzkMiL+hW6fgVvh1RByoR0OuYnqgrBiZP5DkkDak7SH7NTaPaVR23ioMvjyDX7NuQwLFctTi
SOMV1/H5iLBLfSnrUTQo/hLucL1JGEsC5zlxFAIS7dKxK8rABGiOKj8kPr1LwBNfVaaK+15z1huH0uHf9eIbfmDcZUtuBGeVXo/X
fyjOPU59WK30MZMG7UIgeLQTcgKVMlKTfOg61RtmrKyk/CCCgfIePBoS+p/MyGrIoZgPozmzNMv7uN1wn2FCsKSV755S8mKJsXQp
EwM1o5Jw0xxUCG3plZnv944niiOGpatE8bXd0+0ddDHNtvaP2JpLx3oGrn8z5sTC3HB+NJlAyLSrCqkJVW98Ffg4ccCyRma4d3LR
ByjapakFBwrfyx0n7VVLUOHJTGVMVXfKHb2pmAp8TnMUuttIq07EQzXOIsmSyg3XQAckeKTqYBaW1WCTaKREjFEbUuLD5cDAE3ER
stBtxaySMAyhSpRJkykJkWpLisSHEyTTqkTEGhQD0dWpINK4C5sAwgMDwQN70ntI8dIWSSs/WNtCgjFHZ84xJgNLcU+/G4TvonJn
cBqhkaxhcDG5g1gVs8vxot4S/UmlT3vUTiJ5qFgx64ewvxSDksF0TtkHyp01TjfCxAGtyUmodgsjE18WTkFkBCLrDmvu4V4JZOKT
XvDIRJPFj9KPDtH51gjDS+vQMYe9ND+cOd9aiosUH5O2ZkJoEvJoj3spshIuFVgRjKV8flzr7XwvfCSPZHigPJoBvVb4gJWQduO8
mVBJp2x7EQwOUnEXTVDa77Fc5F7l5hTNCU8NQqe4+hJt1wq/SnDlQCJUy8AzfE5wUAwoH7IWXA0Ze7bCkZkNmDnzocUp8YemmJa9
gkxcJSUCV+Db6dl1CUYVH1Up7Qz1f0geGVOiN5FunJZ4x2+3eojraJja0hBiS34SA+xL4DmSf24oesB6hApxTXQnjCwi7SJRDwEh
D/IhH8oEmUNi3pUeJlUkjPESCWxS4lq7JS8NENDPjsSPTpchJeMjTzr2VuBBc4SkpPFWY3yBuAkubfFpqcL1QrjBQiA6E0xGGSTF
feyeAOoB+Aoxwj6wqW98WiGFHNibcqgAeNPANaci7lAOhKNYm88lgzDuRR7ej5R+3UuqQ0h46zwf+HqlipunM8kQP3rqaI6qCkiP
tqMWR6psL2u1eJm5YMS7Bg8ql9o0HrEkjVP2WdnPkPaWRDo+d+IbFqEcTVBE/viAzGCF2uABVik4ikS8z2OqjaRPISMb5EqmHVaO
aEHfpRLKROZQt4zwOktNooroMjJOlsdALuVLdhvqmfQbVOLh1HjmEnUnAXyQJJ1iLLrxeHYSTUIyBhFBxnp3tiSh4eG7p7JjQZA5
XCghv7/0kTla3mX14ATHB7FO+ohJ5BCdM5m4XvpogohLoRI4Iq0x4ZNZhNn86mnh3ifos1744AYZ/riIMAILh9ohQeIMiNdJHTw4
WJME53wygCHgnwLpwfvmAzMoZOAZCIWKvY/BcNrXMt5Dnvieb2mPlJmYaUlcqOMjqNHSTFBRCuarM3gAZOEwQ1XtLB6wcCX+8jw1
w7zlfJnFRyxYJL6SZOtxCEQo9dKFFLwKUFCnzMoG8ji5wDsW8LOk4wr4LqoU6QoP9ENvSIoFTOTZG1sdamQSBNKgxIXSAra6GsB/
ZHIRyijFTZAsYUgwYOESYFZ4q9P2ZsQjNZ0yUiUXa2W2lzjiIxUAMckcCbH+zbHvciA8Jmdr/9PIQzmFIARixZ54j9ajjwCJR8nW
TYE3ykqrepiQw34nQotu49n3vSIdlnojbRpwV+IOaTacADwMJXopluXQ7sQbIu3biS94gohhIDwMCKfZqTLsXVl2+YCZ5HUsKROZ
hwG3yyxcnXtMC+lZHr7da05SYJw5pUxY2RLdJYtAYGFOU504y7rdXaUZijfyhoi5758iSxoWLF6XSqanpiz0ETqPC67yaNQjIYVV
jke4wi3i0yEfBlyJIpgiJYpyOD/A4ESiUmgAfuRdeNPjzYNg8cH5wSLVEDndJ+CYEj8o0s7I119QZp5K12oQYENNJgaDw3TBLCfk
08Es8FvCN8E3lWYnDpiFuJChScCc1PTTRaAKTTYOjwyPWW74wdBKtwzzTDJXplBa20gdYjQBvQMMQhtFY86G8+Mx9XUYrUoyMO/U
TWy+BF4NJjIfCkQpEZAj2hHCvBi+fWrAuhzPFuig+f5ZJ4yAO98ZBsLsDk2gIYqDgxMkhHiTqlwvjKQ3iXdouACacX4VE3HUAOGQ
62hGWek/CAn373E/3FgiNeJ/6pfDSUZk3hxrobePMu1nEUBZgKAJvagi0pKaZ0OsovfjVYAIAnhYQgj5CBmHDkbMkP3esZqyKPJ6
WyJlekUnBTIrQ6EEXdyJHml5qcQn+EwQr53oASzqEvDVaRLSXiTJfAkEtjIpAs6tByXgR4NFy+hJQtbRDfZAlaPw6M2HAgn/AQwL
BFWqrRxGGlzmKJ4OuByHYzVw0IsTBRkNMk4wkcTvBi5/i5UXgD8MtZuPPFCobmwyMYTUXN6dlq2J1hSlNd/J+teQYMg0V7i0E4Pf
9h6g2vQW1Ur5zzJUUZ+724BxGUagTC0ppsAbO4GdSYaIChL8UgP0JvtZYlcUixaDd3AY/0pIetAXtK6R/jnCHgOOEc1h5pS1C6Vz
P0ltAHwASkvMMCmGAtsZIg44SkJAMuvuF/AcG37LgdMccKJSctOLIwcD5DtTY4fT46W2s20wA6R63SWTUiCfRCG1clnW69HajuhO
EqQBUMlQbhMiF78Td5MlkCaDHRSkkhUSsaZSEO8Mw4nILVtT06B3l8UzAg8CZtNUoPs6n65G9pG0P2KLOYbaACOiKdN8ejzjlSG6
+xA7U6dnwHlqDaHHaYo28Xj6AiVbDG44QRFggkf11Ey4AB5ruAszQoBaAhxghCraUWrw0JeUN0I55WDlvO5X4c3JQU/J3B7B2isg
AShp4ljamIPdRbzPEeiQxlFIVIwcEDK8ZSMFWV0We+1Cw1KvpR8RPADdMriEQCXB6wLHRWW+iTF5Qd+sEW+D2XovqZRjGtxpIgF+
XI/OxmMIN0B43yKUUoQwUW9ZFjn/xUwkA8ZJlUCQy7LO3h+eEJdJ+VgkpRGRJFYgZgfS2XwZWW8NZbAHWTjiPHqzLvQJkhR0gyGZ
By6+Cter2BFJH4XraUVmgYVjpPqUHfoAlTmx7BltPqKerbqD1xPYCsjuYiBhiHzrf4TmcT40xwHWiF2LLYEAScuiO463nsCX0yPL
MCSbKUyusPCAOF4m273H1xgkSYM3JFg5EjtBOimGjjktq2EmCrFN7QnCMUU5dKr4pRkUokIQSNoNI2d3CiQWTAFOrRom102rZAYR
JKwyEBlZx9+BKiIQSI/Iimz4hgYVt1QUwI5+wFIqRLj2JBEWlLw7gHIh16w4niNVN+uUbLONSNMRUaZDJIQjFCFGJ5sVh4tJnaEK
LOklfi9ZBiawGMpkqQVkWaSsfD4OBYAnDcRJZH5WbjQ5Tpa0nkRGkQnzdpCe9IBKr2ABk2L4ghiiuXEmvHIjz6lmHrxOqOO96Rzr
FEHKgf9kRNLftY06N6NmQSoSOVAAdt1Az66Wlfm82SPoDKHXdiSPWDks8IL0JzecBXIAgAy6wpjAKNqIt6HCjZoA5C6GM0TQkryf
kliKdnk73yg/KYYsZsLYaSZ+KqXBDHBpUPl4pzqGlOWWR2L75y6snFQ3fEkokmnex78IgsoCIz5We2GHTF30gaWdV3ZK0vk+pGfg
TdQFlXnShyoN2Rq4TDPMWzfcXBm5ehn5UgXQpHK0g7xnmTJcKZ5Mm1Zr0fpJjxHn0EKICYwch0CcySdNMJXS0RYioVPsyWl5C+ly
c7DlWqedJHMZlUiD04iXuvVQBdGCdDKcWK66BargsAsrnOTmmpsiFVq4XAqwEmd5UYb3CBiN5FGTMHu+Orjat4IMOgP51IinViQN
JFLS9HGZ/puxUjl4WNyiaZ70ppslt5JXILPV8BehPSxCI+PNkXLS+vPMnedKUNABtbARPTJ6CMLQupHchcZZ2B0twYwXSX9yxaZx
FuTxtsS2wr1wWTcOZ+klaFPSxswF1dG/hBzRar2TgYHKHqTqlgiUrLTED3B8vRYNZo1vcCmK0lIYQ/+VBGvAzWteJlTYxgsoe0bk
Y9E6uHHWh0/ETGRvpshssh9NQoR+eG/uGh/7azJCv250DfHGRtfQbmx0/Vfj0elNG30hNro0OjrDSyTd8MYc/pYhJgCJZYs5U3Yk
UZpXciaPM+AdKdujY6u55L80pjLJDGsS+qi1XgkNJcE3VJQ1uiE0M4YqVJZNKBwRnybNgwpNJR5gTa9hyPVV3nxlYAgg9SmoaQNz
ZN0Ir+81wrT7NwOSmACgLMiH62HvJQkKls1D9lkywIXIKJWYlxoHyAvDZbiPg42eb6oaBNdsSJxZWWoJ/GmBJdRtyJzUg9w8BwH4
XzHakBOGWi8MViKALVdPfkzFD5ZxETBwy5qBzfmprzOSpKj6mtPMmCkCCTElwU903WS5jafnpkQjHQhmUIsWJK3djut46YaY5s+/
dFGF/4N+6vofV6vrt6c313+hIiC31v9IJXLctP8rMN1f/b3+x1/hh/of9Fbcf+lcq1zcHLxEE+kO17S72VXUWGy+Xl2dt6fUXx8w
jQ1Jjxsz2tdW2SOzYEUOSg3bOK3zGzY/37civ08WHi09J5NdpiRJ/zUveHm5X5fCOjhtfQKSPwCspRHnrkFQbv5wcHW0/4Or2QbF
wlKwzBn5leRBNd7szW8oLmwvWnoZ7tIKU1CNRe0z2DQ3d/3Og7ohtVOg09G+/HqzVlg3Xx/Xr9Tova1eJkU4hUFqNBpJmyG1eXZx
tOpu2d5Ux0+4aqf9y5Q5wq+5GaAVhS5cl0fQKEm1a4R6IYZQlyxrfa2tmoEmQeY/kk8c1mVlmwg2lNS8LNJBGh7Ia3KL+wdd92cB
nAikEDjcXYM7HZ4yos2vmipkP+9ExpZOx0ZkHm0GLwFVPorR2KSrpnhPM9IGc3NHtg6OdnDY6ECuwbPiegc0lxbz4YHA9jK+ZaVI
nwolnufBede9JNItQGE3U570GsFgkE9vG6SbDlImEfE1Ys84LYvZ+okUEF4Z/mBChcVsAfGgyaSVJDY8qI+tX0VCuZGErLPC+9jq
ScdKM5ISZd3mnZ1/z9Xz44E5Z5lluLtw25fJeGNKR8GhRxhVYl1Wq2uFej+yzErK4VbHP+QAdCWRxasd3NoKGMGJtEXxBZ/Nx5ct
UYwdeG08Qy4Po0c2Y7QuWreNM0zGCbYKHz+AGRlz5XgBiyXzTaoa1r6FAtN0ukllA3sWBh9ZyilJNR8mUBUanmObJaSO9h6NyRbN
wGXl6JSJpY+kyXsPMosNUqsgDpmJbTs3WczMKg8FsvLIc3G9y6BfTMAJjshZBeR8ACUbjtKwEYCDCWgSJepdJsNRhmVmqaXSCqXR
SRctRk+MDdP+ed6wWBTalj2SfSIzo8YuFoMT9lc/HrRqancazm8yY8LwxLlb25OClreRxFY3Ns7ePhmwYV54E07kko1PHerIzZm+
IEerdS6tdWBQ7sdghM15U3XaL0XbhKUsLdeBV2s30uZXtVwsl6IiSk/VSTkGAbFAdL1Z7hJz7VBa9gSQxIOg1+ZtHTzvJ+XANssG
JbkQUIYfbT9D4eB9wHtAyCPLy4iUyywcUZI1kgNRiHISMuRwR4ntiOvEZRyuH1LHsMza6Pdg172fjAsGJ5ai4gErTUZWgFsVZ8H4
MwHdwxnakZEVVxLssTpiwezzCPfIljiRKZ4B8NEyTNNyPrqC0VXki3qKS7jRWR8k3ippVmJYAJ5yhMts5UCyANMGhI4+N1u4gphG
AahZ9r7LI4PTU7Q5LMqaoMtUEdFtQTEqc9WF6ygO91DxJvImnEBubTWWbqXWzeeWpVNor5B5MBVuVlQmpX4HCDD49YifT5OepMKF
uqiSz6so29e48U0TwJZChK85mW3NDxJupFziZiKFcbw9Kc9BLJSab1YGJxuJrmac3t4bHSfF81KO5uJ4wNETSnxo74E5WyfeKGOC
WwNL3pP+PX7kQ+SbpI54A/HZIikm40w9SCfgzF57yI1kVztMvXdmTqcAJGTg/h4P01E2KWM5yVzK4/LNgUoX863I5S9JGxs98n3k
G7m24sCg3ALVKtYJuP48PMBtuvM6+SYJ50mHvVW+GYguSw0Y3SIu4/LNzgyWnZxkawRc93ApQUWRtsbFTL6VKJ5axQCygHyruXyr
VcaMIZB87dEg0vvLt3YOG5Csk0BKdANUT5SIDxFwMsDIwQHubWjwuRVAZjo5RvgoqTkTEXBkp3hsL0ntPItoVwg4SnuQwJonaPuR
vScJV1htVWOlAOQfJuEIgGq1LJrrfRgPrVxa5bfC8C7wuRE92NByqjAkAJdycf/SnJbpfGwerwFZ014LktYBo2Q+umyJEoK6ilhy
E5H6ASKOzHly0wqwHWS2zCxw8sUy6lJQty8M7etOxJHunZOjBho1xA049BIUFwdcvowbcLKUSyuYQ9pfOecY7yviCpcRWAXHPtW6
3JL4KF4YEVtifvNkYpo6wupUacAP7IvqFgkXEqvnI5IF7pO5qP1mOawSQyURbIMEfBwJl5PS7SiKOSG8nGpylMGxQoeJARkn8o3U
UAy/QMyBRP+4eBPzkmAmo093KS0zNomMEUmTmxQK0KgzY/D9bdSYeKvENEGgiK4no9QOlvIk9TFJDM6Zza03wBPUYZEpAG9Jh+Dr
4TAdOVglEZvAcJNiEJIfy7ecZ4HSJcaShQ8138DZZrjQssSKmq4Tb915gQTfquVCa8Wbo/Zbq9uvE2851QnESsh5zManTsQbZ6Yk
PUmel+MzZw9nXrTdWv9TJBxiFVDJNSgADxiSs338UMCRxYygBH1fSTTdX8C1d6vZk7Ok1krMG7hJ0qZUvJ+Aw+qneEQglhv83M1F
/U8AtVgDOnNCZsg3MU8q7Rg+pYoRmYk3J+O2AuEKSfqICol8IySt54nG0nLgMv0A+YaLsaKUbm7ltbIwJa2K9CJLDXO4D2LyDY2W
l3GG/ExHpww0RzLcZLWnJKI5bPKBGBxwyTyrU6AaLGE6Hd37CDcrLU1FATFxUJKVm66bpV1gG2DpUHIwItyokkZdRhmfwa+x36xM
GA6rnKJxceFWWKqi1j+jCO77OZfnws0DytUOkCUIwHCybhlIZJBtVCwkkyOZsMRiCUjEEicyq05+i3QzRQqVCq5elRHG7614NmkB
1BSZPO8Bso2C4wml5IYEU3vPxY8KykIRSbeMwamJCp4dtJ9kN6jaYo3/1VM31BL3xc2paePjsq3CeU6shcKRmRUR+DiijbRZ6uZJ
7IRs6pnMLQvLkXQmtpHFLDcrs5aQ1Uld3CGwayzBiVgFKyZfAglY65qED5Cmb7WN8vxDLTfSQ2F2oilST8LIIhuItv48yo7e4ZdM
rHTbxMKayrUMsQzYE3j1xMSbCDZOlbDSO7o7BRvIc/KI1sg1EszJYSP7G2jZENU4lGuWoFNRl89bUdT7i7ViLNegX0dOdoVp1brl
30+sUV2KLHzyt6iTPRNrVH6gsg/ldqpyHrtx4GHhaJSQcTHXnXklZfFlRLEy0WPM/5PUqcHo0AAuS/cgt2RqtaK95VKRMjaNaRRU
qydKVKCEZCMdr2cd1CnOiRtUVRWXaVQk4ywgdaAnCxcXaunSTOzMgjylTAn/UMHml7k0WvEih8KV5tN1QxiX4NeCAzbk5+Y2Yr2g
SgetEPIiam1XVL3VPOF0rKoiwhTZhSRc4x7NxGmL6qE2G8UHLX/bCuW7ycoliU2ilUkM1VyquaWVrsipv2YVwMaGyhhzLwJ0hDpS
R8GbJBow5VWoRJVDHi4Lo9s9QLAZABX8ESrfNLZIYlpO3NQZxHZumVbLlNgjpcAyK/EVF23F0hwqmLiBVPQ0LtmAvnqwwWS56P/p
B1mmEckGOBa3jiy3pJhqKMQ8RDpaSwCElZ+LNq/FJIiD7Y3T260z2rSPyV3CTQMsPMSNNquRDgxPanyFcHMfKtoIBVAvkI4JIh43
OGEo2frTwC1EJduoEFmWd2UQ14k2moHASQg5+/GpE8lWn1mm7LKJcRd5eKB3il8XcqsxuHj3MvLHyszY4ly0BcveRoXKiZncW7KN
cSUTWMmHOSQpfUStxSC9PElmci0le7sCSuCsellErpU44vIEpS+r1kbbSvwcmcxdwKxrjDUQ9ZRoIafxQcaazJnK6hcHiky6ZOzR
yhtMPsUBScAf6YGNrpgBkSSWT++PyhcjSjnuVV2ITmwlWKOSZI0XBNVTE0QaD+prYlFsNx3g+4i1UEfZC+sVU04dPbiupSqiKJIZ
gBsqJtaoLx7Mwx7iFg02GBVxZTqkfUnpmbUmozABc0LcZKbov6dUQ5Aa0ofk6Gw0KipjsUk0ZlYnKUZMunHSWRkHAPtgaPIsXy/V
SHL1lQVdSJr0kdEFbH7SmGT+UWfQfSyhhtSiCCsoinLK783/TYEMq/5kdQdmwlu2lfd0LbAoU+pusUmx2CXVqDGQkqg9HyYTa3Ul
gU0j5/MPskrncs2qzpXm8c5cGAtv6iuAeZY6i1qYljGLjfp1FE2V/KiaaqwRi60gZ5haGQUF00Z1acZ2KVVlS0OuhMJSHj5Iqg0Q
IiT0jMRVL9SmOJK7zDXaLFQT+TOz17QJS8su7eIC68w1O7Ow4OlEUkaEWk6stVoXZ6t3EW5S8nfLgtVqDcuBTKPWi5UAyixh199f
qI2tNYKlWiaqYuAd/wAnJPUVClIkKQGWVMlM6QcjKQGMzwck3ZT7m1SjGgCxuCoxx1aUuDRpFP2l3gh588UaGElFdhdodZ2azKyZ
95Frvq6eFSpKRhNKnDBI0v4TUp80aAh5brCRsmGw/oTCV3XbnIhgc4QKKqtCg0PLl3EfCB1UKGngrEpJmj9UrFkuJBX+PcjL3M3U
kSzBFHO0FJK2liXzlbMQG3mfFHwp12AkqWSQ0v6HAt9xa42MNdqCWVZT8X5W9lysUfaNejZ56apkvGrU7aL3oR5HpXlXzcVaTYE0
I2DoaOUEx+P8PqO2WR7SggRf1iQ2OiNofGmAoBIKU7w/tGIu1vRaKSHLBOdtMY3/0sonya2PHVC+uVRLl2Stk7MUAsWKBjV9Z6PE
DkotsxHbMImbpJaUgnTMrVT9BwnvuVArZcJLV0ZxlCk/Xsu8jqRqfFXdgmKykJVEv3U7IiIfglsTXZPeAXY3Syxn3CXlOrWSLmyW
6lJBzPkYi3J/ieZltktlyunpJcawRqINzhJH81GJNi4LkHa8dx0wkj4nBLyBMhW3eiDbU9EDkjUeyGFuZ060rr1jVKTRtgSHBoyG
nTnHjlhjoab0OFzl/i7IMTJyDIxsudr7ibQsoReop1ACjZ/GqjESK7VK8glNUPpOhkORRpFwSjmi8RY+XSPSpEJROIdgSFIV6RqR
RgGGhHz2AvPiISKNPgjU16Y0OjCosbAW56SxDdWlSMZ1UYlGIyEAJ7jGa+01JtJoLEOXImAFgaz1LC7TpFzjrXCl5SSmiXuoUJOR
mBFvp6JbNoe00oY1s2x84L8xWCTdkqwCiPUMigs08RwaIFJJqIz7jWnS4EJFbSgJkGHE9ENEmreOSrodQPUqzP3hVBFyYFrxC0in
c7OBYYKhYFCpMQFhkq8xYcCfwCAA40r8RbekRR2opEzZAFI/y+xjxNWIrFM9Gvf4JJatrUl1GpBvldWSGceJmr1JIXRakpp8t6ql
cf+4DCUKGJNJTvhgLaiJ4GoOkpTyP6WP7c0PkGnUdsgJ/lPhYmJ2E+fKwdp6XMVlmKsnmdlfudVUT0nYukVwW3dgSvRZHCBqjpbL
DE955mqsd1bdKbjjUq0HOhJIr9Y4HydwyDudjxUN/G6100BPWA0w5iK9zU5rzzQjI13jfBwaiTnVBtqBRIVaDjjc9JPSGubNZBoJ
CzSeyUgcL8r1aMh//2sltfnUPNKkRs9QB3VSGzXxxRsTnxRz/mhZbQVeeXogl/HAGkltKb2IiSa6QfhuktOGqAk02C3SB6IhpSBK
X9EmT2l+mo5pigI8lN4sOQko2TyhjR4FBcUs6dlauGxdQluVk9JOISgzNNfls1nNs5y6MyWS23+kfDYqpYvFVV2BvuHaWUJboDue
trcb8c9BQhu+cpL33DDjbZLQBhq+btjtI1HDOqGNOrPBQNTh/RSSWxLaqOk8dULW+Wy0JaEwfrglnw0QKDVz8rvz2WpEUCgjG7NJ
ZyvBiQOhLT9uOhsVRLWG1VTvotAHlW2pBJ2W1Ri412Z6STKnOimnjM0tmV5UdyEGX1J7IF2jdwVKxJWWJImB6Me5ZQ9NaCMxgbpP
49UsgKqwyNZ41Gr9RLL2QIxYN9jMChauTdtLLFIMojCl3/ravD1q7RTWbcHq0d+ZuBcXb4NUtZKGtG4EdXxAShv2VdKV8b8lpa3u
AUFfsFsNN86EA9JJcYoymT1d+kdBS7d1oEhvFf4J1pOQUthuWpfVhkyR9EjKW7PaZnLuL5PVpomiK6DVYJqzSlQdsh0KYysjePIg
rY3mhfTCLnwEF1+H2cjCAOYEzDceZqNoDO22UguQvl+8JprVZuWb82A9eEYDo3R3TuNCc+fgdhyhOTqnD/5kMffSOki7keY7SPag
1RXFa4BNl1ZmNKIgW7VwMpUosmb9RUey9UMz20gXD1QcoXrjbPFy24tZ7XAu8jmilcw2oEf4tlwSx/5YZpu3WGse1hhwOSFaGoEQ
vkzeL0J6S14bORvleE/WiW2EryldVTsl44ltubGVwqqO3ZHXRpnTzIq+r09so64ufXOrPP8gcMWaxDZXkl4eqvEGddScB9pZ0m7W
197wiYZJNydi49jnpF+ma2CDxZKOteKulGDVQNw6jzm1bSAWSQGpbnfGoO4r5Ci0TxhCwiCbUqGYj1Qtb7EbgyZHkvdQe+m2lxAE
TMeJjAPHZLD0VDpXFZqKNTIOcBFFPVICrLl1D7wjd2+diBtYZwn5F+tE3H2S2kZWXF8t9ZacNjpo5nSPmuQHzHPagK2IrYq1T8Tm
TMBZAY50vRVXLnFpF3S+IaBW3J7VJpFBn1k6BdxfwP2l0tqo5U9uWtJ1yR0aAzTJox8LadshFnGrcvaLzCJ6ZLg4K6GZAI4l7QUr
5ht3T4KvowoY0Zs8e5B70tLaKGbgaDJLl9HRyHI9DGPbAymWQB3WXuz1ZJARCdjAnJSFLMRFHCiuSkKAhDz6Yo/NwiEoAbVbnIug
bAWU8mESzhLbPPWHrW3uNKbRJLbR7Bbz2Dq2ziUczdnpD2ulRdOoemKJbfgfqDvr1mH/2YUJGBBqIDwU+t/mtaXWVWTmWs69qf/m
UyvMrooltlGUlIwMarfclrxtMjkD9pVmRRlN2SBDhF7FVek/DDsYz2oDoEMvsmzsXNbChtRK49NWxdfd6iYjtLZQGU3R6UOQj5rn
DUdIgghYMEBg7GI3Rk0NE74se8hax1kC9+iZD0tsoy5Tmlnq7IQKYYTWBNHRFzeavqd9TbUblBCSkPO4hLPmwCEzvDhep7AmyYF2
NfgsJFtTbYsklHda5Wtk3CBjjZJ269D/90psG4o46v91KVxrE9twu3niYNlEcM0S2woyOuglW9yVt51a48tiHf5fFrW3uLPUFVIx
kwFIa57XRipRSbZMKO8v4f5CeW2FNZq24tHV3IazanWFIa7oTxVJAcjpxwvQB9hXlcZd5BllhGkKTrJYlI/UOQDkvzkKdYdypkG+
b2JbmdMzqbSi/W5qCRj8ShIAHlEX9XdT2iLmRC4oTVfSak3iNq0drIx1XevAmbYdseE8UsBZzwwqS5OO9LDMbXhXQasaNiV9A2fa
iXRGR9oeeWDalFVMwBEhBtxOx84yGjytKJqWU1u/GnvUJlkAlkJHGrIP77dya3PbPL0A3cSGs9w2SoWkyHXpi9kcc0FyG6Xc0JZk
eFa3yTfgiJWpb+TDxRLTtXLUQhZnDFlBJ5QPAxJG09sKcuvwcYfCTYZJ+xNS1LUB6bQVqdpR0BGBPg2B7LCsqOKuSmqqk31IWikd
O/I1qV9kwtU1iHJzyBZ3537dU8hJQRKzgkTIth+NUxIMIBlJKFjuho6ZJfJJ0pN9SABImyus8Tw7ctmBpEkrpZVuHpdx5ZL612Rp
eaBWHyrgBnlrNAdza+Al98lvm7SF7aLKawGT0opoTgOg4Q4BZ6dmdXrH5K5zFyltn/K1Ai4sa+cjZYvzur3T2vy2uo57YmDS+8u3
v0yCmwjXWZXh3E/CAYbvRGDj8CUYX6ZzFkm+oaNuOHkN4uDrLLiEIsCg5YEfrhNv1F+k50niHyjcSsPMiWAIKCfphKQ8nWglZbXo
RZ3pOUGXUGaPsDDV4KnAnWXxCD6NedA8Lf2X8ulxzkGUIKECDNq6S6bZ3R+Y4CaZRU1pinB0TZr7lcMEEt8DVUuSdzVXTIhCEowW
U8jCsLDJJMXNqn9raaksvka44RvCwZzi8HuocLMMtxJARzqxuwsTSBmuEnrWFJG8bZxQVtFK7Dk19+ttGW6O4icp5ce10WPxYTLc
qIgvoiYRzQobfqwMNxzLhoSpZskAmFpQFCmfknD5XLZZTVMD0VM+qi50E8UUFpZiRaondSPXgOT9ktzuUtpsQWJEmRcfS7TRckh8
uKJbySQXwNDGCUkAtG0qQxUxxQtDwMF3HRW40jWZfPnSepJb7zcrqRcXbWEZ6I1CXfWKjkI+3GmOr5Fufe4au7QNYX9IitsoG4DW
LrfLtoDzh4xS2nTdKtrsTOsUELKp13P+cHqSEL1eI9yaFDcK81OpPZO6VERgJpbihjyh9wg4+3sLt79IjlvdCYr69H5aobZOcpN1
4xM85OLhEaCCo98cPb2xQ7UH18i2hJ59lTky6Q0al22ORiCEXkjWfGiaG22lLOcJ79OY9Xt4dgASkdHJJC3n0q1apnUXLUcnuGxd
mlu2LCT8qcCKDPVratlRArcsrcR/bmX0PkKSW4rAoimALMww00m0BX2dV69zZHTFsgES3LZ0FCbHMQ4wCXlACyPHK43DS1BWLEiZ
4MctHyrYLMlNxgqp5xOfXZ2LRXGUgh6hPo/g7dAvA73NE1L76oY/t2S5pbgakDCU3VmT5UbF0LQEgptn5ccSbCWtAnN6Z7iZ6zWj
lq8sTw0xq0txTAaZL+k+TDWa3OBD67HyaaB7bkoeIwV243LN0s3g9EEaGu2iPpJYIwMvpTE1rXMnqdvFUjyQ3NAE8EVW5XOpRtl5
VAqKPoCNMbfw2kw+8cEUJR+slLhvtIBC8NSMoj16QjuoOw3wuFgbQEZw+6+ptnWfHLeRyebpy36HWKvwMQME6CuIrBFrdiZ6eVmu
sdgGDy+A23XQl7hUq6T8EjOy1egF8CTJLSUqSK9tkcv9pdpfJMkN0DvNl8u8cLMUYGqROOMlzmqozhHYYokFDbsSStsS749uPEny
Gn2XU1MiVrbDQm55ZVl1CWD1WTzqPZPc8BOIdICEZ8mUQdIzPsg4xFIpk2rOOsLS2kDkxAcBUxRxzuGWoPxpFEl7NKrAxUMaep9c
yjCWOuWJrXbJTAK8Z5YbTdXQ9zPQWdOFywymmlMFnjIv83WjNaS1JfJ0zQxrom2BJJhCs5DTlDIu18jtA5/lcUvPuf4HZLnh1Gff
5ZMUlXJJi7pAx0bX2BVr0txAdRVWnDotCr+GGdL6UWYmT3KJi4tty3IzQElS1250c5P0Q9LcaLZqfWkTMFsTg40KPlXdFhbqGu+p
FlFoLQLg/FRKSteUEC5kAJPfTT+u0hsEOJ4FBoaFpqdwgqqK7c4PSXNzno7PqPppUo3XMtDVBW0a3ks737n1nS+pgoozyIMNS8pb
5JpEGnVVPY0RMMWirkixXBIoKa1aWX+sD5JrfQ4bvgO3JifgPpluY2utuCPSBoCIjSoiK9xtKQHtmdo6lDi8U6yRolSmt6YEBBw/
wDAD0dMsUo8ESqKNKg3Q6Ud+f0/kXyTPjfbQVFkN01o4luYGVYH3tuLPsfLIpuGBNy7ZMmvckIRLRFjiMwVtQ+NpshRRBX1ekn8V
3jNYM8tzI3RCZi5o+TxMpVpGeVFsx4ogWxZx9DiKY1F/jcrkPi/XKMQpVhNNsTMjmZCtEWvWPQ71Dey81Xx/qFyrtHikg2X4CZ2f
eyIBDpDXqynwSRopkkb6bwo2LiTWjDAu2OjIaTmMopGYEgxU0knnBk1E2afi/RBA0VS3QHwJxLxPZhl8uPKpDGl+VMYWad1DwnZC
c9sU+x+jNeplxdKppJOU+L/RltcJtkAZfppMh5S0sY+BJKEzuAwQy3sM01Ai1JJgDFQJ3QtjxTqCpYLQrTCnsa5fZ69hT2hn4kug
Wfq63ektt1tzWpbaFulHste0/eivrv2ehtkgc3JVaNKea+tkLpurKCSR4oiVGWD+Sr/e8gapIY0DGEZmZSRjmiVVhhIDz5W0mr/b
pxwXa0P4Y9qXM35oqltFzabb5Bolfh1ViIDt3RZfa090INemid7R1rww3FvLbAGFzyxBPqMmY/ueo0w36Wk2JUBhaviIfj3fsM3S
NbTbPw/JZrzXnX3Fjf/v1O8u1IN8n353f7lGQLSCKWi+PmO6TScgKoXgaIo2SrBOQAWI5iqOSWz7AAFLobz9mpKbdScgPdKaSDzI
uu07ASERpIdms5BPlVH/mRIvdGUao2QaTSChMi0tNEJSWkuZWFIByB7wmFqEJND0b00zIIsyBYsdMuu+LD9aOyAbhrutHZD2MKnx
EV2gaQeUi9RBr8R1gaYdUA5eYl3eu7UDSs0LkiYP73bXtQMyi2Vq5Db9gALLk+dzjMagH1Cqf5P0No9f1w8os0fe1g9IJgh6fvHR
2wEFSi9MtYGmHZB0Vvws45S4cTugpKRqWx7GcJV5OyCp7drOk9mYtwMiwEL15rtTCu6nD/TtgDTKSf1bS2PAYAKcQZWZSOlNWuJh
zmsBqP1eR1kiql1J4N8TRKF4V+nW4AOI2XiK/ReYHqlV6HxgO6CCptahHBmxD0idIMs4cXfgbuouPwWAhGlCxC39gDpUy/oMeDET
ijut0Qu6jkBMcZaXxR0dgTIrgyrmsLFYY+/+NTsmiEuVPptUh0oGHRNIfiiySH5Z2zGBtqKyCdbUlm46JgATEc+4tWECvCQMa+U/
qGECDY8k5qbNSAj8aGx0ZQHgG+ZyLl9Sd1kGADHKzNCJ8cQJHGDUedaOclLu83jmREZnTXoqFbLDyjrz9kGZE33XBIJxFC+drl3X
NaGRGLd0TSBAOSxQHeuaAFq6WtPTtemaYNmdWXg/HeWWpgm6ZZFM8wrapglslBCrUNk1TSB1pnC3Nr3rmiakkGIe5YpN0wQKSYL/
z+50/91TyrVtExzo0PEo+8YJFeRS3No4Iaey2aQ1UqRxgsUDy3wNKKVrnGAFQbz/sET/2xongGCbhmKpAUujAz04L6zo2txh7VPi
+WS3p5gS6boKS1RdxKTIKXWfZ2Mg+JAOacllhQgBwxV3uqzXCLkOMVqwguugN++HKwVQkZYToRVtnEBvKm3Y2xsCDfsmTE+dJ054
eEhL37c0TsgtauzXJE50jROciEu28Xp37l+xvnRC7XI3ViSTrr50aqjSEM0LrOtL07/H2rWuM+PqAtMF3cgTt066WYVpK3FWzOtD
fWCFab155iagompJ32mQQJllj0eyJigzQuFVep5nJHKMUwcHVBVIfKLZr35ph4wz5EeWAL2nrNKLr+r6tg/Km+iLTOOScJmfrV5f
ZZr2gWWIiremzHRpTSLj4q0tMy3mnoQ1ocq6zDQdZcIwJvzAMtPgpWdqf1dnmmcWzkUhOE2haVL6xAruUWca/Gy2FoGDWgJMnd4z
RfaxIDhdoWkHDHgixbtC05qK1MBftxSaxjNQFsVt8JSu0HRBblyIeBq6StPAEqhT+7ELTTPSYkyKNQxOWlhqiVeRzkA1Co6IU0q6
d4g7rrNlZUnZnr56TaGKiCZmwf0AGM0XVMX50N4JA2xNVrqPVWXaMozvSHyndjR951OXdGbCPcpMT/Mr5o+XcUFRqNubJ/R1pkNH
K9Ey0zmFMnyxsYh6dcvNqEe3HHhzy/t4c0muzygVSvJlHY2pvbm5VNwEvFBO0dv6i96VW4AZyTy1mDGsq/qpM08udYB075Q0HBpV
rHHlkp1ZpAD9tMxl09J84MoFD2Lx20AuVw01Mldu7RV/kCu3yLAnYIMpFac/RAVI0UEyKrykjvjSvIIKLCMTAdO03GJbMzmSEnAJ
Ic8lceDdcW+us+6VlseOy7CM2BIW1a1b1Va0iJ9bgO/nzaWrUWE8MtDSeixKqmVp5d8y+rYXk+5Ibf61XlqMp6Cid1m38ovYuMWy
tDBtoH086NF1SgBBVt2JfG8xBsCcD60OQKPaQkKEehRTiKM5kGTYpuCsZHxrx6dzJYBuvtTOSilrEOLg6aqgyyU9lmgMHrMCLaxL
E6XcmdgN76fATZWAakmKKb0JcjpzTIA84vYZSYB4p8SRIo7cXNqRpyI3TWHzut7Xuipv1EupXGkt6tJht45hYhCFpcWfrRxB+lGq
33jJW5g0wWuKMU8kI7XscPNINyFW4/GvpLNQgxgyEPIqxx9PIfg11c98SiFGKXo02bb+TxElPNB6BWgL7MQ76yZ8R/Wze2gA3vQK
Kj85IG/TUZaG1qQ3p2PXzIsgkPRCEo733kBiVsg+skup3Yb3gWL3gA/XtHvJsJcLgjtkzckcvrMEQlwFGPhmSajrkvLu9OGOLOFY
E6MUNecWLQBgfZ3PUsG6bkkvac50GY1nw7Q77uzZOaXHsrJLGJnXBkgAWUidkTVBzy8fN3ElD+ApBp8VK8/dA1y49BwSd0vLJPRp
ze9Z/kb6T5pY02U0/DmPJMu6sMoTweAvcx5JEescCBYKnezuuJbtUuYFoJajklOMxLBzqWZCRUNZFeV7FlGZeXHpcULYnjuJQU8r
b0gromZdZsV2Kh+zc0tPMJradjiq/Ro7l2JcdYe9EqeA5SHERBxlBFLKxuYGftPEPrw+QAEvYr9besAcSW1ywNyZrijTUM5WL8cP
6CS+yDXJ4k6KirR/7lRZokJcwjnPEpOOAwCgmrnF3kfEeegzyaykJu1HxuPCRZHlgaJPYKTzSHYC5b7Q3MqKjhlFfpv1l9ckkFKX
WrsvmvtKbqgXFQATn6JGHyLiSFwme7lMJoXIxU7A2HvUkpIUFz+X4wFJH8jLo0RCsaaveykBV1mBQraxD2vkm1uaGVwQlqbDTHV3
WZh7yjc8W9rwGa09pm1fpBGWFjY0GH+Sxcr80HpMr2Mw/sTKJ0ar/FjYPbWClWCm4+AsXOOOqrAUM6LMw91FftZIuN43yyL23dXv
8OHeI9XEUa/xdhFnPm+tJa1wbhdxdqbHZeSnjZfmD5cMoJ7gOhEHCghHDzVkfI7ivEbEAeHMQDiRdS695d4SburFLeCrVM6kGUr3
Xu9XHYAWGSJvKqTkIRun0ZsGgvWZWH0mipzOcxZSQ+t6MkisClYUz4EBhwdc7A9Yc1pFNp/Jt1IqhBMtopo+0I+LWkwF4wKpU5bZ
hLbor1aRxGbJNiGSREnjm9wQNFQ/KF2IR0eCtELqw7gcP20a1hSIzCjXSIZzWbcSfnCrQPLDgd3SCMtyjqZr55PaVqY3iEhsjsRB
uCWmf3KCjyNxcP2JB1HDKosFX022JTiBHUhHnGQPlG0AexPigry5m0aXnUliyNZRrSLSVQnFhPbXiRUd9MmkZ+3YiZviSQ1IZ6rr
xtqiyJoKVkiVovbho7QKNLsGp3cOkDQL5WRvUhGXLDBvQjwiwFHP2E5Sk8kBLoq4jZpZPRselFhvibXtb03FLQzxImW//BjtbzVG
sqpTShaLEueyrQwgAUNiNfyTiPWWL/GQis2lQdvACjO46CDpQ0K2dJVb3u3IMTuSbR7wip6lm1o5hQ8RbQPPrAcPusZ2mzpw7841
wTq4rTQARXTpR4/Mcl09grhcq09EKbgbk0uf76rsKu5EvbdOOhQ50nQVpxnDXKrVmYSk4esDiPONRcx/68NmzH+rw9zS/Lc+3Md/
i2WC41TSlO7r9rX5b4tySd4tbbyMgCZg3OCX2FigzcjSqxl6zINLWTipS1QjEpOoT5s7cEuKrGrnAYkJDSEPHbi+sMZbBGyzFtH7
kRy4ZWH9NUowL0mHxnq/Nh0lBYsBJYsBliHS6kFqo6dwuZXYyqMJECBeK5p5VgWZjXE+W4FQqqqcSthpHs9+oBU2PX2xmPn9EPGv
u2nR8MnRwSYd9sGrxUhFj1KJa2JbrrA47qS8K/yLUk9FXul9Sj8B7A7REYRSHUkgOe3o19R3dUvKTJDfQxF7ehg+3IXrnFi7J61M
2rqfuyekX9I7CzC12EGSzlaPcnUWgcfVk64pXVhZqwj2MA0hYiagKQFVanZwoFbeg1y4Pl9Smwwvfm49Gkbjgt8HquDTGK+oIh7c
bAkwrbIINplLt3pwy5Qe2R5RU1UxVEtqrWhQshzdhMu7K8rcRwMolpYpasVqwrC7TQ03xg9JCxVtQTJutVMmmndFU0X9lNT51Mtl
ow4XQ2gJWTZUiCkx98do3WEfGe2RyluaUEr24eh2H6oCFDiZwXmLT5r0negAACy9hAu9kiprcjP34JLLLDZe1HzDrXPg5k1hWpN9
oQjrPLjAEvFXegMpufzBLtwa7N11jr8ThnuHIkDQofcSRhUB0gdSa0MVDKd0C1CpOZVmPnp8hzBcG8olChV6pTvmxqUcdEpHl2A9
XeY2br7EFUwvKtI3rLLy+nIKdzlxQSJSUAcgbNYZl+/pxE0NzUuSm0G6Z1ySJiZMOpWUqiqWvV6JW4PTIQYnphpvsUiGOFAYZ3kZ
PpaRQa5WhngjmTUjo/whQo5dT1EQfCJ+1F2ixkcUAAPJtKO2jbXMmHfpKHDBAGSppOvUVmlUxtEVyqScCCiUmF0xGac3yojKFI5Y
v6bioSLOLymIbkaOTEwfA5pJlad5AThTTerUiEfGpc5UE1qFOR/PPa2T2okjyaCOFy8k1u1QgQo9rwgz2/09JRyocsRJguN4wv1T
0k5payEttK7dOmOLeWa5UXSqxYfrb/PgVjRyxontyN+KtxErLRcKhwhFx91HceEWdLWWnm1WdjZpP5iJs9OsOacuPnmlsRhlAGWF
+UGp92RNh6awJHUzp0KFA7cyyZUZCnJyNkHaG36y+ii5JoyyBMRB1mhfMq1bS+umSV2IDBduGhNxlVgPGAEJr2Bg45iIK5YUrAe3
nFN6KI97cCHANBPdUxqA4lrFnd221gi43jObENFdF6J8bwcuaJBpAaCJeCOSWFrfhTzv4GZx8WanIiWsGP4dpi7V7TM0wjXSjcZn
QKoL8n10Q7fGgSspSSCrgp3kIHLvLd4mHlyEN1B0R9MH5z7IhpPVAb7QsDP0z5rbcFbrg3EFKpNGoLgJud9AixOqY6w14STxPVU3
HUXDfdQVmBOVIU+ckWXlg6QbRadTasVnYMrLSYlXWWeAq9C9CmLGfu6/FV8IdIUM5F3RiHad/9asIBpacVqermtjB/oBdQ94SFKG
h/pvcykmluCXA/4JfoaeogIjUimlGgtdsmOSjUSnJGS51T6LA3BK7Q+dQnFX8cZo8UIPeIV6WzorLx9WB0+yjTabwH7IlZzoW6kh
RaXVadPREKQoYw5cWnIk1GW0ksXJLRVenaN/BHUEcYfE/bcYrjRf81Rm+kge3IKciNRCHrhHpskX0vNzoJaBJp+WeDuHGYEvxAPK
bsqzKh6fFE9iJrwzJaauZxqJT2YgsnGuBEvdSbKPEp4s9PCqrg+tYUwlm97cyn1YwXQq0rlZGg21ykgXhp0DAIh7cNMlmTgWRscr
HlyIu3Ap5EBcO7XMARolPNyHC/9YJ9ze34er0d7mwqXRjFaIVGzpdm7aNHFiudmp9GkLZHrfYbmRlRP6enlrvLhoBESwab3eGYMD
0WZKu7X5SL0liW0sYl7cEPfihoEXN9zHiyt9nsYDUp4kmPOmVIF5cat8aQ6lJPfWQrV2l3Ze3Ix2a6ACKKTpmor6ES8uJVJTUwtZ
yGYW525c3SCjYLCnkztZq3Za78Y1Fov3hxr+tZrxkby4lTUOQu+jZXDyQTBcPH8gmS1TkaKVETcuVWQz6kSh3eejU1olIICJJiGH
gO4aW0JyAmuqJF8MhE7cxBVbp8o0kQWfPaxmoLXpIscIJQaX7ZgJFUvK/lKJjLoc0gPmJm4JANNlYKsw/2/B4VKFLGfTZWTvxA3c
aom7DrWD/MYy/xhNuqBKKolKjhH1nOtvhXWechZsKKYdpVl/rRpKREV4Jg8DIThUAyqzDIimUUA7nmuKkufAFtG8eVgs6AP0gCAS
hnrJ201lw0+zVOiALbGcYDT4ijYUU/uvLoUJciwHVmTlZGMGYLGsa80RgLeiCXH7zxHxNt8UanBhBbQ+AKMa5sPE2ioJRBUYLKNx
eq2v9bzx5I7EXZw4FCxIJHmaZiFu/1E4KafNaEJT1ioLa1yc+ZKuL5VxrKwuVfHwPl0aZO4oF1iQE5FN8qEDELhAfofEPBnvIeaT
l9KXmbsqpVvoba2zyYAsCL9RPyKPjLGSoaZJLSnMTYbK3dpOXA8YeHGdR9Y8qJjCQBMAon97ky7UxoIqrzkV/ot84pkdqQL1qZoP
D7C9nIR+I05cwBFV50OeV1OwzE9LzmBM82IKzhyvztqL5siE/GFO3IwyJ1aGsOoSDd4z1YTMIOoaeas5VcxFHBhF+gRJQyQK7WMS
LrO0ZHJIaIUQTzUhnEbLWBmy5HlWVdRgKkwWimZpQ/OefHLmxbU8DBmWGXCjwo3DXdI+qOJO1QsqJYQqYulKDOpFCS467yimEbd0
i2WWVWVGg5ayII9/Xb13ihEU0tsrvMflg5FKnmosZHdJqgAsnPeh1MrxJaYELvT52sHJ9E4Z8o904biEI5kVawMgWRqVcA6oOqjY
1LoG5zND8H0lnLcS9GL9AGgmnN/n5EMgk6xaYayYDmBGcZXEumMG7+NGoCYw0GCHfQtcrYobgbmUJetgQptD7Yjyg/ybc/lmNSPY
egTqZmK8SMiByRPKvicTxGjnh8mgTjy5VNdeZwWad9ZI2KDJa+tbgmqhhB35pi4pyo8l4awTZlWAzy4mYrzQzoF2Usoi0QUw5pO3
9l45JZdLy4W4xScPXhBnWoV9l8fDzmQf0bm3AkES8vROn/waITd00VIs9p59uu5OOiVslk2k0UzIkc9gmd1lNfH6TmUcZ+a4XSk/
fJe5S8S4TLoadPOSCqYcaJ8A2vNuXStKipJKyNH8IwVGfW8ZN/HkijglxEuQQlr7DyoX5MT8rXA5LuEhjrYPU0osURZPLDlQSDQm
4cwvTfo6ExkvGCTJVVH83VCjpG3FBRx2HlVNCDT594t2zTy5FbLN131tMEAmjNLAHqIJsDhl3a1k4hIs6ehFFUUrrV6LrohHsMTx
5gJd2milkIQ4CymX5BdZa3hKvxfj0z6o8rsTJRB2kSEmHjLDUQNZ8SRv5imh4TmMSjZnZY2ifElKZtzdWQG1kpQsySrKyogIQMKV
1pAvMzEwUAM+TMClVuw7BYCZZVMXvCtRTMhQlnGWpDGtH3BqBUqBNqTVGidnTllIGp6Ta1PWyWHRJEO4K+2r0MNzX3yQk3Mu3yxb
OKPbmLjKrNdm6ajfUhUgVUtrtTwZpKdUnDdEYm4lM0anDFgSwXOplyGQR2PV9WL1TPySvFMDleAYtqyPB7tyNUoi/QbZILUuGTus
qyVpUtQHk+kA+42VjKCPnCZDDIGE5eIWnzzaTlmQ0E7IuYoWty+Bo+BDp65ilvg7vfJx6Tby0baB9Ic7cs3fd7tko/hHRiCIKhsT
U28i2uxUVF8g23e2NKE2lzhvO5Y1LU1SnGG2JJSfjvhyk4xiCrVapuVwszq5L/P9lz7bHHtym4PcrkbjZhM/7st8XksBjA4FENkW
w8q4ZbaknDuQJjJ1s0k1BdhLRk0RHF95YxnGsLjUuS2pFyQNAT5q583BuF6zRj8rlHHYu502AONWCVXicJVWVAWxrz9WNYWAB76q
U927eofvZ+Lq9WSaAnRPMCrnjsDUYnjetDgpjXMhIqmHIgKeqZSpFxf/NMgrqZ0MLKiKgjlzy/eWNeqtq+X7yZBIJQUSLCklTdVI
N45zkmTjCcsXqCMEseYuXJxPVMMFwEP6nY+7cInQ0qw6w5UjCVHGXbilNqynZzQl9Knf93AXrng+pRCIMUtDm0GUEszugBoMeKyK
heCx72TQUASvYiNEpb9pmBUNCzS4NR5csNzkapYJ2f/FzC56r1IKlHqkzYT2NCbgrFwgzsCSAl+EcfIs0t1Rd6ASSk4NKQIoSbjF
KEI3LOixTbFzF2vWSVMwbxUNcPmnVHr8CFVxc7Q3R1kXEBmhmEasxcLEkCl9LT2gdJFKQzDBjLaUaO/05Bv3EhqaJbSJKKi2Lzs+
W9uHuiChTwohXajzSRu1Dy2nxDAph0ArJ1mwE0veWfO5FKGSACfJ5u4KwHg5WSCgBcvSai7F1DlQohgrVvSF2pXjkPuAEkkHL2g9
W6CB5Xf6K+I6wMA9q51PZvMaC/d9a+JmTiRX3RrRpQlhyAyTJdUuvw2s1J5KrxN/DxPXTOJkPRTXYK0ZKBhyh8s13ahZh4KHUjuA
NMaNxQe6cVO0Ryq6FWAxP6AJjOxkMCjOGo854tBzLK4YBQhkMu6tQVFExtH1iVhJXlrzvbiQI+YCE8yoyu7j+SbkEZKTUWAnPcjC
NSXI5RQjk1LbB3I79bq0LBJKCpN0FOlHLeFF0otohTYitFWKdaMGDp/iRKevI82T1xXilBrk8oYiJsDfDyqkUFGFN80ozZ+l1cz7
Tq8BGhxZ/XPnYiBcWfjguIHqJcOWnyMBh2EC4ov2B3mEY0jAodpZYjcFurLsQSFKBBzB7Nwy5abjqiv2k29H6oJzk+q0jV/C4bin
r3lpCPPb6uFaaCLUbVQTF3G7oOjg4aFqDemf1ceph0sglpRHk5vpBCFId7ccf6vVE0TRiok3q2RJDCK3yqdrOpuBlCDD2dSdtE43
icm3kqrvISnIvMFh9XGawBCIlQgnpZs19dPVRHUocvO8elJv59oKqUWuJD9UX9MKLR6lLOrSFBTRQREvQly8WeiXeuSeiGmV3q2s
rBFvg2IKeZcy8HAkbkk8doIrmgo3b5mLIAuK27p2dmdKvOF4WiPbBk93OexiXYjSUxKMiAqaYxKG3b5HBXFZriqziqzSqt2HF8Ql
nieRQQGrosvleS/RVlEons6MlDzNy7n1BjKDGpnmTi0itWZSHcwsb5fqnT6PwjgoBWh12dDSCJTEJRt2NUkKHr3qQfabW+qNDb9h
zWmzfKodw6iofoOIc3W3sYln2tPwkCatwYS3lUGNSTdq7+aYpdY7gBTmuHjzSxt63pTmebB4y2jhRgU66mCX6bwKhoNt0CWUpidp
BIfrMYLoIGW96eP4G9Q/AsqBUEEWTzFh3el/ROZfEWaDek/ZloFTL+ltg/d2WgyXBHZqm2ekPVZFpG+n2CElKq22KNiV29pRlzlV
4nJKWBdl1OrGvYr2gDCtko+CwhXLt7JKVraenT7bm8w10SdA8pKA8xrofmmdJ1IcAsHQbXHR5qhtXuFdcFa5Ol8j2gJzZt2ectJ3
fMhisYUPkG1WFotSyVT0KPPJYpIpAVaSHmzenChTTUU6IXUsU4fnQ8za3WaI09JVezDDgwsGaz7OggoWBOQzuhOYT+ahDakBm7S2
9wd5cEfCzRzytwo34hrkRNFyNoTbADjtqVQ8nyWkxLqZpDIDbu9yRqBZ1mUVDNESaWYCHpRQXiqJWop8Nxa993bj51+9589y9/Lg
cnW1f3Pw4nR1vbz86X1vcI+fGgAdftVMwuTflAakv6IcCKBQrc2vACD57FeL5C/wLrOft7irF4tfXV1c3Nx23l3f/x/68w//Y/ft
9dXui5Pz3dX594vLn25eXZz7jc3Nzd9cnF9fnJ4cHdysFjevVovzt2cvVlfX9tn2zOLw5GZ1vTg5v7lYXJzrJLbQYmu0n/77+uJ8
8eni7ODq9dHFD+fby41vL1ero+sni9PVwfXN4+s3b7X3uenVxduXrx5fXJ28PDlfHJ/cLC6OFxdnq5cHW2+2Fxff63Gvj/WsxTMK
mexA+cnzxdaXB2dnB4+/3v5s8cPq5OWrm+vFwQ0n7pmbQk+7eHt1uOJxLw6JHrw9vWleauulTnJucXhwfnF+cnhwurN4yc3y7R07
+fqH1epy//Tih8HpqV+Ki49OuFodn5yv7JyNrcOL85uT87fQ/Tknu2yxXC5SChg2F7366ejqornj8b69bf0ezff+qPnS/3bx6vBy
e6mF2Dg5u7y4ulnwxQ7LcPnT4uB6cX658Vtdurn7StO0e3h68PZotcs9Vj9enl4Y8znf3fxs8a2ddHN22ZzzONl9zCWPm0te5MdF
uUrSxwcvDo8eZ+XR0eMXyYuDx8d0xjh6sTo8XJW714e64eGry4MjHrG7ufFr3ZUXWp5eHBxtXVyuzrd+++nmdJY3t7Uy/7r21H42
dOLGV7/7j/mZ39ZnjlfDbvuHz7+44/TB2nD/3/q1L9JMO2cR7NF5z55vHK2OF8dXF2f7OmPr5uDlzuL4eu8b7fTtJ8aUL3Tar5/p
i+efLV6ecc3V4vjianHFNr14VoeNni9OjhdXz8zeeL7Y2zOTY3FwfmTyo1r8I1/K9niuT+zp9Lnd+w3vcH65PLi6Ovhp65nOeaNT
uru/PHu+bedBKHuL04OzF0cHi5Mni2MN7WZLF0qcbb25fjS6RW22PH928vwZ2sPkftu7/WVvrrfr+19lk3FpoBrQwYvrrea9CbBl
23p72cTV82eJJoO5uMq659mNkInN4YnQrb+/Wt28vTpfHJ0c3mydHrxYne7ZjL/c00S+3Hy+syDMqKP60wKOOmKBRg7UEUcdEUXt
HV/vLA7dniZmC0o9fGofUz6m9lGk1mgj/c8Xbu9Mr/6sVXd0r+9c2hz7bvP57tkzV3/aWXzr9rbco+FXSTOf27sMbWdh2s0e4xQP
3Ky31BJZf3601W2oPjWGzXzbKf7uU1zZbt21Z7hN27//yhi1BzZ/3GcD6qW3+41uZLN10Yyg2eazLXD31r5te6xZ7ePmPd9dPPvk
5SfPn7z8eTOy+k2y0Jql19/6h7+0AfTH4f5XZ/ta8s3n8xXXvrAznjYnsDvqSy7bI9oUbNcvdJd2Q/D3d2/swG77+bLZFPz9bXNu
vQPs9/zRq8vrfalzb6/3+fSWx/LhUJPVfHzLPV41g3+0pX/P3g6/18ftx93RR4/crnakqPfyRKvJOr02SbnpEs3VZlra78J+5/Y7
W2b1v/Y7NH8F++2bv/zm82YDTLdVvU3Erp+91nt2+3z0aJN+d9xBHHx4h8VIfm5Pb+iWlb2XW5bNv0Xzb978m3UP1Ma0y5ARbMj6
ScuXq5utzcOrn/S8081me9/n/c5WNwf9KF/mIoievhpgxIRCX+bbG/+wOLxY/XhyfbM6P1wtXly8PT86uPpp8ZVx6/1Du8fi1Vb9
9zY6y2LrVBLrADK7WV1dXpzWqsSL1Y1eqFUpGJA+JdqzQ31DitrB9sarVDsnMYp9tvlqyONNsNUUayQH/UrRaOiuXq+dbUh0x+bL
dkCzAwd/NztxcKTbkbOzRjtz46vDWoVKpBAmetqjrcevku3drVcp/2589VZfI141b6vz1dXLnxaHVxfX1yfnL6Urnfy4Olocrc6v
T25+2n7Sz4hWv54Qll9qqKmnw3nZWOU7i1UGE6vfj/3Sv/Xj2UEjvvYoW2p+bn9UJ2+8/JFx8SKfLrbs28f8ta3xrXKNTw/nw4ap
ZPsHA4H98gkyvl7rLUm7Z/Wy2lroJZ4NJrTnZbujox3/ao4a1cVO775orpACwSLt26r0b/HV4a2vUa/r9Gn10efNGja33bVl12L6
325c+YkM+a1vhYj0LL4ciILNWveVyrC63GmoBR25I5zNWsK3qs7Z6ujk4Nw0HKSwNvDuVF+68pJzQ058+FTm+fnL1d6z+jbix/Zf
e4+gMbafMwn2+Q11v0bbOjv40f57n2ufT17mbHVwvn/00/lescxLhNH89dpb5rHhjd/mjlNHD//CRR/VKkKazVufs/a80UMkO6NP
+a5bru/sdW991O0nj573bXxQ1/cc1NrztMUv3t6025UNvMevnW5rNrvyq8Pt7tjb9thbHasZ237L2JqvXv441klbTrE/uW17nPvH
rtDr7/eyam80pkO3aXN3+HSNUKh9crUiNxJ4owdpu8zf63b2MaT7uRDa2+skkE24FC4Hh7n3VTUPai+c0DmOhdVq/2jvyG9vmO13
JPt5S4u4szADcHPmrkCZ+GFTa3VyLnlzs5dub1xeaXhbm3+Wrf7nWrfTvweP9Asb/s/iRvzaf8rv1P7erf/6gi++c7vfcfRb/bHZ
3+zx48f3/m+zVoW6yahVl2OMxOPNd1fPPtF7SGle+uOfN5uJMk14cXK9OL+4MbG6WJ3qvTf/f/+v/3fteK3f41ij4ga1zv3uk8XW
//f/k29/Ut/kk1rt/kTT/cnL/JP6Dp988vOivsZm4pPn7Z+mi/MW4dgOHV+33xy65uXav59O/k77vzcHq1ePjat3I1d94QYP099i
MuMTvu0f28378eb/Ou8UMCmcZ2foDPCKc22JsZqh2X331aHd4bNFR86NhNtq77K9e3liZ75tz5xqL/ry5Y/14vSv0ewRqQPd6+g8
bcxnn8zIvxnGZ+yn2AVjouzOFuWjEfXEvHghrnj4avKgMddot1G3Uf1vn4gkOtq53hIpbW/80n7Lv/98nJ/lLmqW3z/VXt0/XZ2/
vHllXPBjPuN2/3/iQxYm/n+yA/7u//9r/LzbWGz+KeTFZoP2f7G6Jrj1OKTLilzw4B0t2tpGhRdXzdd+STMQT+MywmB1v8MfT/av
VoYLCgVhwnyZhaICcV40qQUS0TVswmDrOT306DLkDCJpwa662kxJFxpAfFVFisSGxQfRYWqwYJ6THlBUhafKF199vX+++oEn5/R8
t8qeYAkrg9zL6nktu/zAEHe+NFikD+BxLVK7ebU6OBKjvm4noRYD36+ublY/IhRkrkk8LKRKnZxvNyfprIPDm4urDgaSJ/mSolMF
2TmJb6GF2vjLjMInZM5XdfvKWlfdvLg6Wl1da8oOiW+sjrpbUQSfEhne6jMWbWa8W5ZUzLWazVnmU5cNbvZKY8B50N3ksa+WZF0U
qSbQJV27TjtOBy3yEkgL94O7WFSmv4V2QZqQ7e8cCbht/UuO00AgWJfDAhjE4B71Ltg/64fjKjxOlMjUcuddRxUHbGQJYDtQEKxG
oOIgtMj3ZBUuLySNFtcWz1m3BGIfSxqJ+JK6wHlbjlXbSE/J8hxkqPbsPZeASkyZVYmj3ppr1wCkKuU8ANoUSRnuWgNHLfEqsYaW
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
HfTlv3MEh4/sg1p9IIkYvqS3ag88/7ldzGbUe+2A+in/hz4bucG7DNztTczMQLePk+0nAJD3rAFvEYqUugBV4tNSCmiT2QxA+rGu
XXX3f22IYTKo0526WOmizaZOMvtdZHVqtf22zy7p+W+vCQ+zCp1jMtrUvNgLzVRkdOOr1o5dnY4n5eL8+8Gc9O/s+vdMb3+p/fOQ
3P/FZmv6M68Zkttf01LERmvXLBCm7eOtk+16Ba8/Y52uVo+vtbTnqyOE/Fiz/+R6cfHDea1D7nPW/YcOp3pp6XGu5OU9vdWsw9rz
MR03qum+/m8aff8wzI96hiaCspvVLjOTP15uW15mP6tDIyg+kXet98v8fVb7lpFYReK6DrFE01669Lr61Yk+FG47tl3aksaL4ZXv
OaBfOn7/0J8a/9En4v8lnnEH/pfGlHP8x9/rf/xVfsD/AtNooa9WRitdWqWiks46wdd1i+vC3Vm2LDMKhhYZTWPr+thN1e50WXo6
MVUVVR8NE2qY3+MOV9vknNcNDmn7VTlH/bvQdH7Y/OmuE+wOoTuBokeUeCpCqHtr1HeYnBAc3WDpU2Xvs5JhhXbcvNTBqUQqBZr8
0hqVUdE4UPepHrZ9vf+H/gRaUhQhD3Xb3U0YRJUuaWjn6OhKMavmG7uK7xI61QGGpOmIffebn/TTfks5Tkrv66QaZv2bH3+0b32y
zGgBWGV0Tc6agvmkW16/WlmRdc6geXOa1Z2M26WyR9uXRV4WVgWWjh72rZU5scpbSZp5XaVVdqGo217V3+7/1HxfWTHsQPXOuiqX
5RWtX59XTcW6Zqovr1bYWidoOfVsH+4TRGC3aJMlVUKLq5zWfHW9Vn1vqfH1dkpzyjFSQ5ty+s33T+vCbDTaztIqpfdmU1r+EFX6
yhnKm8adWRUoJUSBS/v+i+7e1lejoLluQRlBqkPmzSnN61ndPqqaJo4mq64ua0vCf526f7m6aurHs2Op/kbrMMpolk27Up3KvcZn
0rEx4dUpv5rXHXfaghhmhQxeUZuGBmlZXmaOMmbNGFske07TLq1uRfVQ79JmfXqLYvxkMKZgV6n7XyRV1SAaY/kfHxsFeAf/L5x3
E/7vC1/8nf//NX7W4/++1b5Y+CforqvvD07ftnWg/hS0Mxf//hu/YM8sGuBbE7BuXNNHC//bxTX+qtoRttz4t/PLtzfXi5uD16vz
HuNn6Kb6hlunq6OXqytKCqfLL3f/VQYOXj9jR4++fnRz8PbRjye7v7do2+ErdOlTMtwurxdbv975nzu/23m6vXFwYy9xfPH2anHz
w4VBC/+QNor4Yut3rw5utshNzbbtNqurq4Mbmeqfp2ZIUTh++7PFj+AtTvd//1n9bP3hl3Q+XqXpZxtf7V9eXVzasYRGXi5ZnAE0
PJWFT2Dh6wvZW4+/keV4ca57fb1/cXpkcfgTkHKyj0+YHFn4J0cdFHH/ujnjsVscGjQOx1eNL7w6ODrRTJ2/bM8+ub5tnhsrMSx+
/S+7rw4vdyyHvimeEk2l336yUSPwjPlYfuH50eKaGl1ktdr6DAokLRe/vTp4SdhimJzxZHG050cJGhuEHBdf7IbF5cnieyL4/6bv
3vyXX/z5TwThj958NkirYS3qbbS9aC503YXfbn3dXu26q3c27DCxfIt3p4/T3a919nKxmEL2sJFsPLLEiPeSdLn162+++fw/H//m
t59/8TiN1Ng6k/kfA+NdGhZnK/00e/RIsnV7122c/t7qhmlym42hfZSSnrN6jPnRbZ2dfsdsXN6YK2EL89TJkt9Ks2Va7ARS/yX1
3A6NOLd3Fs1efbJVYcpIIKQ79S7dITul96naeandCBVFN5KwQLzuFMtQtTeqn1RKteNwukNzsh2ksN/+2eJcxIS+3hGJvt1ZaFQ/
nuyd/n77SevU0SAHZFhD7/SdRn309rDlCocX2mlXOLe1ZU+1TS+ub3YNwL84PvheW8OyUBvy3YEIH9fbBvybLtneOGT/yQLc4m00
348eydp6qhfSMF4Tz6sdxK93OqrH/tWMtqEN+/rw1c7vrbrJ1uavN3d+vb2ztfk/N3f+J//+bnPnd9vbzzdOyY7dI0d2i2eKWBv8
ErAlO7JxsU82nJ0kqXh68TJNtriMKgS23LroYt9y4qYnnZz3J3Upv/UcdXN29MTmZzgz7+z26fOfm0/u+c/Sm+r3ePLp0h3/vKhz
ND6r6+dxmh7VXKBP7QX2UvUVMuybqYLN3Fw/a3fD840mL6LmUfayj363u8VK1zP/6Ol2s9Br+I1VoJs41W4vSBevtvbb1t+88QUI
nWdrC0vopOefwZnqk9bW++C8jUNG/Oy9yno0939KPQ5dTDWO3rcTFkc/nR+cmXtugODgXL23VChqRu0bj+ChX4BJY3/pw8ah+34Y
sWhqlhy6bZMSAMv3msfu6tQNivY1RWK+liq8a5urZ3Vam35bjZfkCUwcl9A7eyWLru4s3tmL2R9WHgv+o+fU6fNbTS56fWy3fg37
SgPoXm63vsr+fsLG+qxzjB9vfrtlIs5S5r9t6Ha7ebZYNdc039Wf7avNukTSGTHP65MXJ6cgz2rZ00BhGFrHz7ca57nFY5AZ34O6
Wu0saix8qt1UFz6KFo6wKmV7exi7B6f7k0plb6xQWZpt/2NXpuzQ9OyWrm3qr5Jnm3omdTSSOs7SFIN9rkU8vN4/Wh2e9stYT8Jw
leJDbTR6m337VJcs6P7s1oOjJr14zkGvR9QKxLu0eWJz4vZmW6vk3c9WPKIOdR0fHDaM8fYk1512+33xZLHVrehuu37bu19EY3rT
246yNnc4o79tuvYet2QdTu5Rv85u+3q3v9SaDLqdxZ1j3d3aahejXubtR4/C9nYTR4fwjeo1uVtGaNs77efTi9r1eGTs4ajhDgNR
cbG9M/z7VYNQJQbHij1vw5V1ft/es/phIuJpst7es/4Z60KGbUre3rNapnxaX9L9YTc2ycIZJkS6U9q/1t+9TbPbe9YLlt1XJzuL
wZ+nF8/HwJF3jPKJd9cSXD++E8Oqlqn273Kpv8Sx6r8WW5++OzJu5urv+BN+1kvEbbbIVJ5OiokMBt1IU93q3WD09dFOuA6nYHRB
PxftFeMn1QNevBvNQx0e5Aaj+agPnw1KgzRXb9X6QqMa7QwUB2Ol/U1qGAx36ON1tmdI7N+zT4xwrx4ouJ4r+8v+bVdnr7/fttU+
fFaLNNvPdUlFCYdGHuzZ79k2aFjZXk0rvHGdV7+n3bzdFtyJ15vY3JkW3fmlLeP/e/zU/v9xed2P/Yxb/T80LJrlf/oQ/l7/46/y
g//fJa13lsaeLmkaew4aeeYk9LuMJpb0Oa+/tqhbm1JNtK1pb6mPRf+x6j6SJt5+9P3H/rLQXxb6y7L+sqy/LOsvoy120v+k7eFq
fHijSQff/Hz04q5a5jmd1n2WVVlI68t1NHh6stJNype+6bamwxTCCEWglkXe9D3U0dTREpuuDknbUENHk0DPzyxNcpc3r8tREUOW
OD0voX1gf5juzKWnWXjTGMJuUaZ01dMTq7LoH+d1bU6rntL77rCjHEpSllmRp2X3btQLyYqK5nJJSLuBZK6iiEIo6Ynpurcr0pxO
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
0+bzpTj1T5errWZ028vDi8uftrb7W4v17okslqsfL7ceJ8vs0dHNI/75d9efZC+1Or+4Otu63H6ijzdvr84Xl4902fUb7bdvdrf4
+PaMfw5eXOssvdK2jWr3m0M+b09esL3d9Un/zfHF1WIfWXAFO9mq98lgGvqrjU639O6P7AN32f6s4XjtK+jYcF74+f2r/uI/vq6v
1UXb20u96GnkOfr9qJ0bzYuu377326wfJ5ukO7Oen/jL6+jr9lzesz63u0+zDu3c16v2qLnFoS2BNgmHmzM05ubbq9f29Xa/8T5H
dWDniVr19p+nzZ+v6/dunnV8enFws7X1efr482R71x75zaPXj15vS7jU3+l4wwgayfzT1tXO4k1P6H+o73RyfiRCFUM/eSq++9UZ
vy6lD5xBydB8kHD9YSXyNrG5eGtyZyyHOzK80OXf8cLPNi/ONp8/exKe7/DHd/Xn+hxkv845hTfVO8xvby/iP/+gV7ha9erAXvN3
80oSr9dnB6enizd26//9Br743bOT57tvbBefsIvtgfWzT+CyJ+c3W3bsGZ9YiKuXsga3/veb7e3n7Szr5qJeMenV0dazk8nNtNP0
1//QrZ5qfK9XP+2d1nL05ImmQI8frRUTyw2fJc+bD+nzdpXa53Z/H/xofzdLd3nBK4p5H4j98/vVifj25Y24tm9W8ob9goxd8qvh
KOaQ0vnM8c7ic+bt6dIOmjeFO26isG6KU1/s1Td/dbI3uD+/6nuZ+LjUe9tNaiVm6+myV1q3mqcNbvrN4V6VN7xGVv7O4oeL13a5
WfSmyLZiqb6kmTCjvY5ntjTWarqQYL3vdeKSqdp+bJ80idvbu/ZxdcDneqO95Qrtbs3gHnPIa+61U2MTsdfOUP3X59e1ana4Vz+H
N/l8v5YRWiKUosE3Z285OuJD+jHVrjlLe+vy5NFLSTq7eHJ4m3nt/CV7Nseaqc4zslfPXO0D2XtxcXG6pWmcP7Gdnr3OIlg0DpDm
ed1sbTff6N6Db2z26im7vGK/HW8+e7n37uXPz2Wv7L2zCXuyDMc/L7bMeHnHfnmy9Mc/P37HjrGP283EvdOsP/vEPn/y/Mky01X1
jPRfvG2/2ByM5HjzaHzt49H5n9oFtgD1WXzkPrxWNwHv2k/2St1Y6yuav7jIraYP19RrxKzAk2Wqb5n1vXdagPrkxda7AYk9vkme
LJPjn6+3N6Hbt9ev9p5evV3VUyjW0O3XfzTtrBecvEfnW3quzfkF3qVeIk9mvzUiDi9OTw8ur2Wp3FygfosZnWHSnl9g2UXeYcB8
9MiN6KOfmh+LwWvTmdAZK4zb/WUkwjy3E+wYBgA28iPbx7u2P2ryvfgBJvGs5rWwzKPzgzMZxG+ke4tPHl/DQbe2DA26eIb3nAkS
M/z3L7Q1twwht3im2x5eXNdUsptvw5CWEjrdAZ2P7ps93x7oJDytNmD1mLGqglB4ffyI1x4dRwi1GviYG+mNTUBfXR38tMXL8xJ7
3o2VjqHA3Fn876dv9EtkhoQZSdzRRRMJ2UrH0TnHqx/rM76BvYoPvnn0ZnesQYHM6thho1W4R989k178Twup99XzXQmi/q/t8Vto
pVrWeHRytdcs0+vjvdfHeuM9jQS4VsMkkGhfnUmkbnP46eDo0/bgV5fDcy/t8JRNtT8GOWxO/66/s+EMB4cvu8NP95jbdbf7Yvai
j5q7ahp1gy9mL/eoub19v+623/a3de0N24lg8nXnb/s7u/ae7fjrU9bd3JSIPVM/dEPdyj49bT9I/9LGODy93tMeAIrYKFIXZ2Hv
Wf3AH7dtx/9oKskZXz9f+7QeF7g32i8XZ4++225maYgK7ETcwc0uL9ADASPirv3pz2pFy/TKxVcDufOsBg5G9uX18uDycnV+tKXP
EyW/YY/6+M527M/s2Hevj5/8YyYhsPXV452nO199ur239U7XPvuELdyIiJ1Fe+jp7MhXl82h7ZFM6GZv89DtHj7dG95zd3KzxXe7
b3j84OG2y9tn9Yf6Z333dPfN3jvt7FrgxB/9xePmuV/0d1t82x78tjmIrKu3VH3cPn/y/GfbQs17n15zIP4UbYZmNvqtwn3z4593
6+PD7dF8ExE7JiwsMRJpwYfaNsdH9OzqB9ux+gfDEkkhSXn1wzNDR+v8PUsSqBnhm+vGBDMG/Iyz3uic/vqXZ42KzaHTgxcmV2qg
9E4NiN5pkM8DEXFxNr2rrnz+6Ja7t4PSeZ9uGq70+ZTpvrl+dHG2vdv/9eZ6ezgbE1wq19eiuIXDimfUfzcnRPUwSeC9d5Jrtv4L
nbc4dI1a096oU4aedl88HR1P+wsuh1+MFaFms9ca0/jl2wveQxkaKCEbG1rv/X3odn/flnt/H8fs/v7mk9bm0uTg4Vpqgo+2LsQF
tn73x6eyDXVl6xozt+a1HV+spDwt3v1cbzIUefbZnD/ilZOJ9/2z9Mnz59zrVDduD24jIes7/a9uIp65BN0EMMQOYVB+5/Y7W2b2
m8/BPgf77O2zt8/OPjv7nNpnaTr1uh7sS8X83nxNIatrvtt7vrRtxxD67Sqzks22+e7lk5c/94uk9+cbiAjP+/kR/z7ToefLl6ub
rTpMOXHWdI9tT33WQBaef2bK6sn5214Lvbn6aXw1NtnAEOVWj3E0tn98qj9Cb5aOr31Wv9BI42x/2reBJsaalda7Hk2rsU4GNBrU
RTea7pzVj4ery5vF5/YPHsyD68XqSVSatCT2+R/+8Ls/LN6Zk261vWx36s9PFu9WMWYXGURvaq6uri6u9q5vrnSrnQUzsGeqfn+p
eTbbLS5m9cPmNi95PH5Jo4ajt2eXW2YbHqMgoFvupcSBjg/ent7UEnVovm1++x+ff/77xW9/983nk/f+pUN2H/Wnjv/6o79I4Lf5
uSP+S4+oSfwXUNff479/jZ874r+2MbCS/W/ryGkbmqsjv108VMyBo18+fvrtv4bFr/9lsfXq8HIbhZhgK65v8dur89XpzkYTLJPp
20XSdhp/KLf4zW/au1xJ4K0e/3ZxdiAV+Hx19dPi+9XVC0nTs8XWzfWrsE+ceLG7sM928m93Nl7aXwSydnkpZOP24lLUazdvHa5n
BzdXJz9KYK0IHjOmlR5iEV78s8uNpzoZdc0iqeakWx0t/u2bb//tt5/bjS5PD85Xj384+H61OHx7c3F8vNj6bePMu7l6e36oK480
/It6Vi5Oj65vxL5Qei6uNnTLw9PVwfnixeqYIbSTSKz1anVwtJThNA4Ufrb4x/N/MoH3ASHCOwOAL0+OXx4cJ+2/y5fiqm9fLE8u
dvvZ7COB/dTr9r8ZHa0XgeO/bYNxHz06+OVv7L5OmsFni9///it99snGt77WSi2AIwViu/b8rr6XDvNk8WPjr74ihKsjRFdqnerH
xaeLrR8X/89F2lyBK6NZj60XB9cnmt3X5nfRXsX9KMNeQvr04oe9tA33ffMlLhDOXX7z5WcWy63/Ovts0X/1Za2TN8rzdeMVaTzW
teA54lKZoTuLb7RZdhZPni8e6+/mD/5u/bv7R919Dy9Wx/WbLvkCN4yk2lkjymQ7Rk/li/GpXx6dHINP2Do6e7ZcLncWSf0azx/V
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
fP/5/vP95/vP9583/vwP9iLMhgBwAwA=
```
<!-- END E6 -->

## Extractor

Save as `extract_embeds.py` next to this file and run `python3 extract_embeds.py LBC_SECOND_LEG_DISPATCH_INBAND.md E1 E2 E3 E4`
(later: `E5 E6`). Each embed is written to the current directory and its md5 checked against the BEGIN marker.

````python
import base64, hashlib, re, sys
src = open(sys.argv[1], encoding="utf-8").read()
for tag in sys.argv[2:]:
    m = re.search(r"<!-- BEGIN %s (\S+) (PLAINTEXT|SEALED-BASE64) md5=([0-9a-f]{32}) -->\n(?:````text|```)\n(.*?)\n?(?:````|```)\n<!-- END %s -->" % (tag, tag), src, re.S)
    fn, form, want, payload = m.group(1), m.group(2), m.group(3), m.group(4)
    data = base64.b64decode("".join(payload.split())) if form == "SEALED-BASE64" else (payload + ("\n" if not payload.endswith("\n") else "")).encode("utf-8")
    got = hashlib.md5(data).hexdigest()
    open(fn, "wb").write(data)
    print(tag, fn, len(data), "bytes", "md5 OK" if got == want else "MD5 MISMATCH " + got)
````
