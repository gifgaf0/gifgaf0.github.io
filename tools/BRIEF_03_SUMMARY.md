# Brief 03 — Implementation summary

The four-line ring audit (commit `2017c4a`, narrative in
`tools/BRIEF_03_RING_AUDIT_SUMMARY.md`) and the three Cl(6)
naturality obstructions (commit `42fb7bc`, narrative in
`tools/clifford_embedding_check.md`) are now reproducible
**programmatically** through `tools/ring_audit.py`,
`tools/clifford_check.py`, and seven exact-assertion tests in
`hybrid_kem/tests/test_ring_audit.py`. Full suite is **66 passing,
0 xfailed, 0 skipped**, audit tests run in 0.75 s.

What is now verified by the test suite (i.e. fails CI if it
regresses): the structural factorisation of `R_3329` into 128
irreducible quadratics with a polynomial-product cross-check, the
arithmetic identity `7 ∤ 3328` ruling out a Z₇ subgroup of F_3329×,
the chain of implications "irreducible quadratics → factor fields →
ZD graph = K_128 → Aut = Sym(128)", the parity argument for zero
(2,3,7)-proportional triples among primitive 256-th roots, the
1-dim spinor commutant of Cl(6) (Schur on the irreducible 8-dim
representation) implying a 16-dim multiplicity space and a 256-dim
ambient commutant on F_q^128, the count of 1 element of order 2 in
Z/128 (vs the 63 needed to embed (Z/2)⁶), and the commutativity of
arbitrary diagonal involutions ruling out a "natural" diagonal
Cl(6) embedding. What remains in documentation only: the prose
narrative of *why* these matter for the cryptosystem (in
`BRIEF_03_RING_AUDIT_SUMMARY.md` and `clifford_embedding_check.md`),
the comparison to other primes that *do* admit a Z₇ subgroup
(candidates listed but not exercised), and the connection between
the Cl(6) obstructions and any concrete cryptographic claim — that
remains a paper-side discussion, not a unit test. Brief 04 not
started.
