## §6 Open Problems

**OP-Crypto-2 — Formal hardness reduction.** A formal reduction from Module-LWE hardness to Module-SLWE hardness. The reduction would establish: if a PPT adversary breaks Module-SLWE with non-negligible advantage, then a PPT adversary breaks Module-LWE over ℤ_q^{512} with related advantage. The second half of this argument — that a lattice adversary ignoring the algebra faces a standard Module-LWE instance — is the more tractable direction.

**OP-Crypto-1 (partial) — DFR at production parameters.** DFR has been measured at 0/5000 at toy parameters (p=8191, k=4, η=2). Production parameters (k=32) require a separate measurement campaign. A closed-form DFR bound using the noise distribution's moment generating function would be the clean solution.

**OP §2.24.5 — Aut(MultTable) = PSL(2,7) exactly.** The spot-check (5000 random samples from S₇≀ℤ₂, zero outside PSL(2,7)) is consistent with equality but not a proof. Definitive answer requires exhaustive enumeration of S₇≀ℤ₂ (approximately 5×10⁷ candidates) or a structural argument. Low priority for the cryptographic security argument.

**OP §2.24.3 — ZD structure in characteristic 2.** Whether the 84-pair structure and K₇,₇-minus-matching graph persist when p = 2 is untested. Low priority; not blocking.

**OP-Prime — Mod-455 residue distribution.** Phase B of the mod-455 prime experiment (whether primes cluster non-uniformly in residue classes mod 455) is pre-registered but not yet run. Independent of the cryptographic security argument.
