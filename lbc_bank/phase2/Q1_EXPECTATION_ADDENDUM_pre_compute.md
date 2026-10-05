# Phase 2, question 1 — addendum to the expectation, written before computing (2026-10-04 UTC)

The original expectation file (Q1_EXPECTATION_pre_compute.md, md5 8502c2337ceb1bd179ee3ff85b98621c) is unchanged.
This addendum adds three checks that were decided after it was written but before any degree integral was run.

 (a') same-family calibration: one ring A in z1, one z2 loop linking A once:                       |B| = 1, sign = s0
 (f)  Borromean rings in z1, three z2 loops, one linking each ring once (C3-symmetric):            B = 3*s0
 (g)  pairwise check: Gauss linking integrals of the explicit zero curves give lk(A,B) = lk(B,C) = lk(C,A) = 0
      for the Borromean configuration, and B(x) = s0 * sum_i lk(ring_i, z2 loops) for every configuration x.

Reason for (f): it tests additivity over pairwise cross-component links. Reason for (a'): configuration (a), the
inverse stereographic map, decays only as r^-6, so its box value is short of 1 by a known tail; (a') decays fast and
calibrates the sign s0 within the same family as (b)-(f).

Analytic argument behind all of these (to be checked, not assumed): take the target point p = (z1, z2) = (0, -1).
Its preimages are the points on the zero curves of z1 where z2 is real and negative. Along ring i, arg z2 winds
lk(ring_i, zero set of z2) times, so the signed count of preimages, which is the degree, is s0 * sum_i lk(ring_i, D).
The triple (Milnor) linking of the rings among themselves never enters.
