# Notice for *Fluid Lattice Topology*, version 3 (draft)

**Plain-language summary.** This is text to put at the top of a version 3 of the Zenodo record 10.5281/zenodo.20078312, so that anyone who opens the old paper learns that its cryptosystem is broken.
- The same lines can go in the record's description without a new version.
- Fill in the ePrint number once the note is posted.
- Nothing is deposited.

## For the first page of the PDF and the top of the Zenodo description

> **Notice (October 2026).** The cryptographic scheme in Section IV, Sedenion Module-LWE, is insecure at both parameter sets this paper published: version 1 (n = 512, q ≈ 2³²) and version 2 (k = 64, q = 911). Its Singer-orbit public matrix has rank at most 76 at every module rank. So the public key can be told apart from random, and recovering the noise reduces to a 76-dimensional problem. Replacing the matrix with a uniform one does not rescue version 1's parameters, which reach only about 2⁵¹ operations. The NIST Category 5 claims in both versions are withdrawn. Details: M. Gifford, "A rank collapse in a sedenion Module-LWE proposal, and why a uniform matrix does not repair it", IACR Cryptology ePrint Archive, 2026/[NUMBER].
>
> *[Optional, your call:]* The physics sections belong to a research programme the author closed in October 2026. They are kept as a record and are not current claims.

## Zenodo settings

- **Version note:** "Version 3 adds a notice withdrawing the security claims of Section IV. The text of version 2 is otherwise unchanged."
- **Related identifier:** the ePrint's URL, with the relation "is referenced by". The relation "is obsoleted by" would mark the whole record as replaced, including the physics half, which the note does not address.
