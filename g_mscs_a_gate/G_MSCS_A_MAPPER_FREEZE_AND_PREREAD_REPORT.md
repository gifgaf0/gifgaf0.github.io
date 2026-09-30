# G-MSCS-A — chat mapper freeze and pre-read report (September 29, 2026; 02:16 UTC September 30)

**Lock record:** `G_MSCS_A_LOCK_RECORD.md` md5 `8116cc622279b5d4e73214178ae97cd8` (17,923 B). Locked artifacts as its §1. **Chat mapper FROZEN:** `g_mscs_a_chatleg.py` md5 **`0d0e5ecf610b34f21e8c22dd3938ce40`** (51,490 B). It embeds and asserts, at every invocation, the md5s of the memo (`6ea16b95`), the pinned file (`2d44ec01`), the lock record (`8116cc62`), the T1 gate list (`e274e58e`), the base list (`05302210`), the scanner (`6b862900`), the schema (`5323e11f`) and the comparator (`c5b4a7aa`).

## Pre-read run (Phase 0 + Phase 2), the frozen instrument, `main` = `e1fa071`

Checkpoint `g_mscs_a_chatleg_prereadcheckpoint.json` md5 `ccbb32077996833cdac2339938193ec1` (13,842 B; `phase3` = null; post-write T1 scan 0 hits, 1 collision).

| Control | Result | Observed (limit) |
|---|---|---|
| F-CTRL-SA-PIN | PASS | 335 raw values equal their sources by pointer; two-leg κ ≤ 1.11×10⁻⁹, κ₃ ≤ 2.08×10⁻⁷, b₁ ≤ 6.48×10⁻¹³ relative (1×10⁻⁴); S ≤ 2.76×10⁻¹⁵ absolute (1×10⁻⁶) |
| F-CTRL-SA-PIN-DERIVED | PASS | 1,042 leaves re-derived with the mapper's own code; worst scaled deviation 3.4×10⁻⁵ of the tolerance; 0 mismatches |
| F-CTRL-SA-ZERO | PASS | ≤ 3.34×10⁻¹⁶ (1×10⁻¹²) |
| F-CTRL-SA-RECON | PASS | 6.85×10⁻¹⁰ absolute on S2-E₂ Hill (1×10⁻⁸); 7.27×10⁻⁴ relative on the robustness arms (1×10⁻³) |
| F-CTRL-SA-S | PASS | bi ≤ 2.18×10⁻¹², fit ≤ 4.27×10⁻¹¹ (1×10⁻⁶) |
| F-CTRL-SA-K24 | PASS | every basis-independent estimator ≤ 9.43×10⁻¹¹; fit7 ≤ 3.48×10⁻⁷ (1×10⁻⁶) |
| F-CTRL-SA-L2NULL | PASS | κ₂ ≤ 1.23×10⁻¹³, κ₂₂ ≤ 7.97×10⁻⁹ (1×10⁻⁶); t₂ alone at t₂ = 1 ≤ 3.34×10⁻¹⁶ (1×10⁻¹²) |
| F-CTRL-SA-SIGN | PASS | 0 binding-end mismatches over 36 cells |
| F-CTRL-SA-GRID | PASS | counts from the generators: 12; 9 / 7; 7 / 5; 5; 25; 40,401 |
| F-CTRL-SA-MONO | PASS | worst √10 scaling deviation 2.2×10⁻¹⁶ (1×10⁻¹⁴); 0 monotonicity violations |
| F-CTRL-SA-MASK | PASS | 0 sealed opens before Phase 3 |
| F-CTRL-SA-T1 | PASS | 0 hits under the 36 patterns over the instrument, memo, pinned file, lock record, schema and comparator; 13 collisions, all in the pinned file |

Phase 2: **C-SYN-1 … C-SYN-14 all PASS** (fourteen of fourteen). Among the details: C-SYN-3 gives KILL-IN-D / KILL-IN-D / TUNED / TUNED(robustness only); C-SYN-6 aborted all fifteen malformed files with reason codes and leaked none of the four synthetic values; C-SYN-12 fires the NULL-FLOOR flag on 16 of 36 cells at t_syn = 10⁻⁹ and not on the other 20; C-SYN-13 gives MARGIN-ONLY on both pinned band intervals; C-SYN-14 snaps the noisy hull end to 0 and classes SIGN.

**Comparator** `c5b4a7aa`: 22/22 adversarial self-test suites; on the pre-read checkpoint against a pseudo-CC copy (leg label and instrument md5 changed) 0 misses.

## Synthetic end-to-end read (disclosed; not a gate result; deleted after the test)

The full `read` path was exercised with synthetic sealed files whose values resemble no observation (budgets of order 10⁻⁶ … 10⁻⁴), base64-armored, with a synthetic T1-A1 built by `sa_t1a1_build.py`: every gate class was produced by construction (WINDOW-DELIVERED, INERT-IN-D, TUNED, MARGIN-ONLY, KILL-IN-D, VOID), OOM robustness and the row-level MONO check ran, the two-parameter region was computed (the hex S2-E₂ region non-compact along the null rays, as ST-2 predicts), the checkpoint carried none of the synthetic values or the synthetic `src` text (fixed-string search), the masked aborts fired on a CRLF file and on a wrong stated md5, and `census` mode printed md5, bytes and census only.

## D-SA-1 (a pre-freeze collision, found by the synthetic run; for the author before T1-A1 is frozen)

`sa_t1a1_build.py` writes, for every anchor number, renderings at precisions p ∈ {n−2, n−1, n, n+1} significant digits. When a number has one or two significant digits, that set includes a **one-significant-digit** rendering — for a synthetic value it produced the house forms `1×10⁻³` and `1×10⁻⁴` and the e-form `1e-4` — which are also the tolerance literals of the locked memo, the lock record and the pinned file (the κ floor, τ_agg, the two-leg κ tolerance, the RECON tolerance). Under the union list the Phase-0 T1 scan then halts on the locked artifacts themselves, exactly the S-SA-10 hazard. This is what the pre-freeze collision scan (memo §4.6) exists for, and the memo already sets the disposition: a colliding pattern is too generic for this gate and is removed from A1 before the freeze, logged as a D-item. **Recommendation:** after building A1, delete from it every rendering with fewer than two significant digits (or, equivalently, run `t1_scan.py` with A1 alone over the locked artifacts and the mapper, and delete each hit's pattern line); the chat leg repeats that scan on receipt and reports any hit by index before the A1 freeze. No locked artifact changes.

## What remains (lock record §4)

1. **The author supplies the sealed file + T1-A1** (memo §4.6): armored (zip or base64 with markers), the unarmored md5 and byte count, the census, and A1 after the collision resolution above.
2. The chat leg confirms md5, bytes and census (`census` mode; nothing else read), runs the A1 pre-freeze collision scan, freezes A1.
3. Dispatch (P-4; the sealed file armored in P-4.b; P-4.c delivered alone) → CC blind read from scratch → chat read → two-leg comparison → S9 on misses → fold authorization → V4.87 with H-MS2-9, H-SA-3 and H-SA-4.

*Chat leg, September 29, 2026. Nothing has been mapped against any anchor.*
