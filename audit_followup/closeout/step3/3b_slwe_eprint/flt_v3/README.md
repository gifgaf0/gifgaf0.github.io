# *Fluid Lattice Topology* with the notice: the deposited version

**Plain-language summary.** These are the files behind the version of *Fluid Lattice Topology* that the author deposited on Zenodo on October 13, 2026, with a notice that its cryptosystem is broken.
- **What changed.** The text is version 2's. Only the editorial suggestions are taken out, and the notice is added as a framed box on page 1.
- **The deposit.** doi:10.5281/zenodo.23351706. Zenodo labels it v4, while the file calls itself version 3. Its one file is the PDF built here, md5 `6bd55206…`, which Zenodo's record shows.
- **What is still missing.** The notice quotes figures for version 2's parameters, about 2¹⁶⁷ with a uniform matrix against 2²⁶² for ML-KEM-1024. Those figures are in the SLWE note's revision, which is not yet on Zenodo (`../ZENODO_V2_DRAFT.md`). Depositing it completes the citation.

| File | md5 | What |
|---|---|---|
| `FLT_v2_source.md` | `bea51f5a512cb029ff9d0549716826fa` | The author's upload of the version 2 text (October 13, 2026) |
| `make_flt_v3.py` | | Makes `FLT_v3.md`. It takes out the suggested title, the four "[AUTHOR TO SUPPLY: …]" notes and the "(Open: … should be justified …)" note, adds the notice and sets the version line. Every edit is an exact, unique match, and putting them back gives the source byte for byte |
| `FLT_v3.md` | `ef9ccd0a5186c252d713488ded7af298` | The deposited text |
| `build_flt_v3_pdf.py` | | Builds the PDF: pandoc 3.1 → XeLaTeX, FreeSerif 11 pt, US Letter, with the notice framed. Two builds must be identical, with no missing glyph or overfull line. The PDF's text must match the Markdown's: the same characters, in the same order outside the three tables |
| `Fluid_Lattice_Topology_v3.pdf` | `6bd55206b83c817ff07c74fa7bd2340e` | 8 pages; the file on Zenodo |

**The notice.** It is the text of `../FLT_V3_NOTICE_DRAFT.md`, with the note's all-versions DOI filled in as 10.5281/zenodo.23270248. That DOI resolves to the note's record.

**Not changed: two slips in the version 2 text.** The body is the record of version 2, so these were reported to the author and left as they are:
- the Data availability section gives 10.5281/zenodo.20078013 as the scripts' DOI, which the author's records list as the ropelength paper;
- "Fᵨ", "Fᵩ" and "Sᵩ" use subscript rho and phi where F_p, F_q and S_q are meant.

**The record.**
- Concept (all versions): 10.5281/zenodo.20078311.
- Versions listed by DataCite: 20078312 (v1, May 8), 20448904 (May 29) and 23351706 (this one). DataCite also lists 23351115, which could not be read. The author reported at 13:48 PDT deleting the paper by accident.
- In the ledger this paper is the Rosetta Stone manuscript; `rosetta_stone_arxiv_v1.md` in the project store is its first version's text.
