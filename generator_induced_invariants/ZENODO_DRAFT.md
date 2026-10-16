# Generator-induced invariants: what to deposit on Zenodo (draft)

**Plain-language summary.** This is a new record, not a new version of an existing one. It holds the note and the
diagnostic the note describes. Nothing here is deposited.
- The note generalizes the SLWE rank collapse: a public key built by applying fixed linear maps to random seeds is the
  image of a fixed design matrix, so its rank can never exceed that matrix's rank, and a rank check run on an instance
  smaller than the ceiling cannot see the ceiling.
- To publish it: on Zenodo choose **New upload**, add the two files below, fill in the settings, and paste
  `ZENODO_DESCRIPTION.txt` as the description. That file has one line per paragraph, because the SLWE note's
  hard-wrapped description lost words at every wrap point when DataCite harvested it ("authorproposed", "anorder-7").
- The note's Section 7 says that a copy of the diagnostic accompanies it on Zenodo, so upload both files.
- **Deposit only after the pull request is merged.** The note's Section 7 says the file with the printed SHA-256 is in
  the public repository, and until the merge `main` still holds the previous version (SHA-256 `bb22d680…0f401b94`).
  The repository link under "Related identifiers" should also point at a commit on `main`.

## Files

| File | md5 | |
|---|---|---|
| `generator_induced_invariants_v1.pdf` | `a2a1f2d0496743d43d5217fe1f6159c7` | 12 pages. `build_pdf.py` builds it and rebuilds it byte-identical |
| `design_matrix_rank.py` | `7da8ea561cb2a7e4329f4802cd6ff8d1` | from `diagnostics/`; SHA-256 `24a0d4c6…ba54e876`, as printed in the note's Section 7 |

Zenodo shows each uploaded file's md5 on the record page; it should match the table.

## Record settings

- **Resource type:** Publication / Preprint.
- **Title:** "Generator-induced invariants in lattice public keys: a pre-standardization rank diagnostic".
- **Creator:** Gifford, Matthew (Independent researcher, Hollister, California, USA).
- **Version:** v1. **Publication date:** the day you deposit.
- **Licence:** CC BY 4.0, as for the SLWE note. It will cover the script as well. Creative Commons advises against its
  licences for software; if you would rather the script carry an open-source licence such as MIT, that is your call,
  and a licence line in the file's header would change its checksum, so the note's Section 7 would need the new one
  (`build_pdf.py` refuses to build until they match).
- **Keywords:** post-quantum cryptography; lattice-based cryptography; Module-LWE; structured public keys; design
  matrix; rank deficiency; cryptanalysis; negative result; evaluation methodology; sedenions.
- **Related identifiers:**
  - doi:10.5281/zenodo.23270248 (the SLWE negative-result note, all versions), relation "references". The note's
    bibliography cites version 2 (doi:10.5281/zenodo.23352161) because its figures come from that version. The record
    link uses the all-versions DOI, as the *Fluid Lattice Topology* notice does, so that readers land on the latest
    version.
  - doi:10.5281/zenodo.20078312 (*Fluid Lattice Topology*), relation "references".
  - After the merge: `https://github.com/gifgaf0/gifgaf0.github.io/tree/<merge commit>/generator_induced_invariants`,
    relation "is supplemented by".

## Description

Paste `ZENODO_DESCRIPTION.txt` as it is. Its first paragraph is the note's abstract, checked word for word against the
PDF (319 words); the second points to the full break; the third describes the accompanying script.

## IACR ePrint (optional)

The PDF is suitable for ePrint as it stands. Suggested category: "Attacks and cryptanalysis". If you post it, post the
same PDF as on Zenodo.
