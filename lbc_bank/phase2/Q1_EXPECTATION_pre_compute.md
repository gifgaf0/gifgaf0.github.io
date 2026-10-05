# Phase 2, question 1 — expectation, written before computing (2026-10-04 UTC)

Question: in the standard two-component realization of a knot soliton (two complex fields with |z1|^2 + |z2|^2 = 1,
target S^3; the "BEC-Skyrme" / Faddeev-Skyrme class), is the conserved topological charge (the S^3 degree = Skyrme
baryon number) able to see the Borromean linking of three vortex loops in ONE component, as the program's
"Borromean linking = baryon number" survivor requires?

Expectation: NO. The degree counts the signed linking of the zero set of z1 with the zero set of z2 (cross-component,
pairwise). Triple (Milnor) linking among loops of the same component is invisible to it. Concretely I expect:
 (a) calibration, the standard identity map (z1 zeros = z-axis, z2 zeros = unit circle):        |B| = 1
 (b) Borromean rings in z1, z2 without zeros:                                                    B = 0
 (c) Borromean rings in z1, one z2 loop linking ring A only:                                     |B| = 1
 (d) Borromean rings in z1, one z2 loop linking none:                                            B = 0
 (e) three UNLINKED rings in z1 (same shapes, separated), one z2 loop linking ring A only:       |B| = 1  (= c)
So B cannot distinguish Borromean from trivially unlinked loops. Consequence: in this class baryon number is
cross-component pairwise linking (as in the published identification "linking number of vortices as baryon number"),
and same-component Borromean linking is unprotected (vortex reconnection can undo it) -> no topological reason for
proton stability if baryon number were Borromean linking.
Falsifier of the expectation: B(b) or B(d) nonzero, or B(c) != B(e).
