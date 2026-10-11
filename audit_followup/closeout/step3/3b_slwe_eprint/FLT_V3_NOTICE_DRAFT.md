# Notice for *Fluid Lattice Topology*, version 3 (draft)

**Plain-language summary.** This is text to put at the top of a version 3 of the Zenodo record 10.5281/zenodo.20078312, so that anyone who opens the old paper learns that its cryptosystem is broken.
- The same lines can go in the record's description without a new version.
- The notice cites the SLWE note through its "all versions" DOI, so readers land on the note's latest version. Zenodo shows that DOI on the note's record page, under "Cite all versions".
- Updated October 10, 2026, for the revised note (`ZENODO_V2_DRAFT.md`): the notice now says that a uniform matrix restores neither version's claimed security. Before, it said this only of version 1's parameters.
- Nothing here is deposited.

## For the first page of the PDF and the top of the Zenodo description

> **Notice (October 2026).** The cryptographic scheme in Section IV, Sedenion Module-LWE, is insecure at both parameter sets this paper published: version 1 (n = 512, q ≈ 2³²) and version 2 (k = 64, q = 911). Its Singer-orbit public matrix has rank at most 76 at every module rank. So the public key can be told apart from random, and recovering the noise reduces to a 76-dimensional problem. Replacing the matrix with a uniform one does not restore the claimed security either: version 1's parameters reach only about 2⁵¹ operations with weight-64 secrets and 2⁵³ with dense ones, and version 2's about 2¹⁶⁷, short of the roughly 2²⁷² that Category 5 requires. The NIST Category 5 claims in both versions are withdrawn. Details: M. Gifford, "A rank collapse in a sedenion Module-LWE proposal, and why a uniform matrix does not repair it", Zenodo, 2026, doi:[the note's all-versions DOI].
>
> *[Optional, your call:]* The physics sections belong to a research programme the author closed in October 2026. They are kept as a record and are not current claims.

## Zenodo settings

- **Version note:** "Version 3 adds a notice withdrawing the security claims of Section IV. The text of version 2 is otherwise unchanged."
- **Related identifier:** the note's all-versions DOI, with the relation "is referenced by". The relation "is obsoleted by" would mark the whole record as replaced, including the physics half, which the note does not address.
- **On the note's own record:**
  - **the revised note (its version 2):** the related identifiers are in `ZENODO_V2_DRAFT.md`. They are doi:10.5281/zenodo.20078312 ("references") and the repository at commit `d96d1f7451ffca96468ce1918f595370154558af` ("is supplemented by"), which its Section 7 cites;
  - **the first version (doi:10.5281/zenodo.23270249):** it lists no related identifiers. Adding the same two is optional; its Section 7 cites commit `b09929ada97cc3c5bfc0f5f327518cd82e342fea` (`https://github.com/gifgaf0/gifgaf0.github.io/tree/b09929ada97cc3c5bfc0f5f327518cd82e342fea`).

  Adding related identifiers edits metadata only, so it needs no new version.
