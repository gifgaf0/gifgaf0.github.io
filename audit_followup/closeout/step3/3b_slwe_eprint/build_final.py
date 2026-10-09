#!/usr/bin/env python3
"""Step 3b: the SLWE negative-result note for IACR ePrint, final form for the author's approval. Not submitted.

Plain-language summary: this takes the Phase C draft and changes three things.
  - The byline and contact follow F5: "Matthew Gifford", independent researcher, Hollister, California, USA. The email
    placeholder is dropped, because the repository is public; ePrint's submission form asks for an email separately.
  - The acknowledgement becomes one sentence on AI assistance, for the author to approve.
  - The red DRAFT date line becomes "October 2026".
  - Added October 8, 2026, on the author's directive ("ePrint Commit Hash: Use the latest commit hash from the
    claude/audit-followup-oct6 branch as the reference"): Section 7 cites the repository at a fixed commit, the branch
    head b09929a when the note was finalized, instead of the branch name, so the reference survives the branch.
  - Added October 9, 2026, on the author's word: the note cites the paper that proposed SLWE (Fluid Lattice Topology,
    Zenodo 10.5281/zenodo.20078312) and the project's working specification, says what each version claimed, credits
    version 2's own correction of version 1's modulus, says the rank collapse breaks version 2 too, and labels which
    parameter set each number belongs to (edits 5-23).
Everything else is the Phase C text, unchanged. The PDF is built with latexmk/pdflatex, as before.
"""
import hashlib, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../../../phase_c/C1/eprint_draft/slwe_negative_result.tex")
SRC_MD5 = "70ea6610a6df829894c3235e9f91c845"
t = open(SRC, encoding="utf-8").read()
assert hashlib.md5(t.encode()).hexdigest() == SRC_MD5
REF_COMMIT = "b09929ada97cc3c5bfc0f5f327518cd82e342fea"   # branch head when the note was finalized (Oct 8, 2026)
ACK = ("AI agents (Anthropic's Claude) drafted this note and wrote and ran all of its computations, including both "
       "independent rank implementations; the author directed the work, reviewed the text, and takes responsibility "
       "for it.")
E = [
    (r"\author{Matt Gifford\\ \small independent researcher \quad \textit{[contact email to be added by the author]}}",
     r"\author{Matthew Gifford\\ \small Independent researcher, Hollister, California, USA}"),
    (r"\date{\small \textcolor{red}{DRAFT, October 7, 2026 --- not submitted; for the author's review}}",
     r"\date{\small October 2026}"),
    ("\\paragraph{Acknowledgements.} The computations and both rank implementations were carried out by AI agents, not by\nhuman referees.",
     "\\paragraph{Acknowledgements.} " + ACK),
    ("All scripts, outputs and checksums are on the public repository \\texttt{gifgaf0/gifgaf0.github.io}, branch\n"
     "\\texttt{claude/audit-followup-oct6}, directory \\texttt{audit\\_followup/phase\\_c/C1/}:",
     "All scripts, outputs and checksums are in the public repository \\texttt{gifgaf0/gifgaf0.github.io} at commit\n"
     "\\begin{center}\\texttt{" + REF_COMMIT + "}\\end{center}\n"
     "\\noindent in the directory \\texttt{audit\\_followup/phase\\_c/C1/}:"),
    # ---- Added October 9, 2026, on the author's word ("Yes", 13:06 PDT): cite the paper that proposed SLWE and say what
    # each version claimed (edit 1); credit version 2's own correction of version 1's modulus (edit 2); say that the rank
    # collapse breaks version 2 too (edit 3); say which parameter set each number belongs to (edit 4).
    (r"""We report a negative result on SLWE, a Module-LWE variant over the sixteen-dimensional sedenion algebra proposed in the
author's own research programme.""",
     r"""We report a negative result on SLWE, a Module-LWE variant over the sixteen-dimensional sedenion algebra that the
author proposed in an earlier paper with a claim of NIST Category~5 security."""),
    (r"""uniform matrix of the same shape has rank $16k$. Recovering the noise then reduces to an LWE instance of dimension 76,
which the lattice estimator places at about $2^{39}$ operations. Second, replacing the matrix by a uniform one does not
help at the proposed parameters ($n=512$, $q\approx2^{32}$, centred binomial noise with $\eta=2$, ternary secrets of
weight 64): the estimator gives about $2^{51}$. Third, decryption at those parameters is deterministic: the noise is""",
     r"""uniform matrix of the same shape has rank $16k$. This invalidates the security claim at both published parameter sets.
Recovering the noise then reduces to an LWE instance of dimension 76, which the lattice estimator places at about
$2^{39}$ operations at the first set ($n=512$, $q\approx2^{32}$). Second, replacing the matrix by a uniform one does not
help at that set (centred binomial noise with $\eta=2$, ternary secrets of weight 64): the estimator gives about
$2^{51}$. Third, decryption at those parameters is deterministic: the noise is"""),
    (r"""rather than the (non-associative) algebra product. The scheme was never published as secure; its documentation listed
the hardness of its structured matrix as open.

This note settles the question negatively and records three facts that may be useful beyond this proposal.""",
     r"""rather than the (non-associative) algebra product.

Both versions of the paper that proposed SLWE~\cite{Gif26a} claimed NIST Category~5 security. Version~1 used $n=512$
and $q\approx2^{32}$. Version~2 found that modulus far too large (its primal estimate put version~1 below Category~1),
moved to $k=64$ and $q=911$ ($n=1024$), and claimed Category~5 from a primal estimate, leaving the dual and hybrid
attacks to be checked. It kept the Singer-orbit matrix, whose rank it had tested only at $k=4$. The project's working
specification~\cite{Gif26b} recorded on May~10, 2026 that this matrix is rank-deficient at $k=32$, and replaced it by a
uniform one.

This note shows that neither version is secure and records three facts that may be useful beyond this proposal."""),
    (r"""\item At $q\approx2^{32}$ with noise of standard deviation about 1, LWE in dimension 512 is easy whatever the matrix
  (Section~\ref{sec:uniform}). The modulus-to-noise ratio, not the algebra, governs security.""",
     r"""\item At $q\approx2^{32}$ with noise of standard deviation about 1, LWE in dimension 512 is easy whatever the matrix
  (Section~\ref{sec:uniform}). The modulus-to-noise ratio, not the algebra, governs security. Version~2
  of~\cite{Gif26a} reached the same conclusion with a primal estimate; Section~\ref{sec:uniform} confirms it with the
  standard estimator."""),
    (r"""The proposed parameters are $k=32$ (so $n=16k=512$), $q=4\,294\,977\,961$ (the least prime $\equiv1\pmod{455}$ above
$2^{32}$), $h_s=h_r=64$, and noise CBD$(\eta=2)$.""",
     r"""Version~1's parameters are $k=32$ (so $n=16k=512$), $q=4\,294\,977\,961$ (the least prime $\equiv1\pmod{455}$ above
$2^{32}$), $h_s=h_r=64$, and noise CBD$(\eta=2)$. Version~2's are $k=64$ ($n=1024$) and $q=911$ (the least prime
$\equiv1\pmod{455}$), with the same weights and noise."""),
    (r"""uniform control. The collapse starts at $k=5$; from $k=7$ on the rank is 76 for every seed set tried.""",
     r"""uniform control. The collapse starts at $k=5$; from $k=7$ on the rank is 76 for every seed set tried. Version~2's
parameters, $k=64$ over $\F_{911}$, are in the table: the rank is 76, not 1024. Its own rank test used $k=4$, where the
matrix has 64 columns, below the cap of 76, so the collapse could not show there."""),
    (r"""still: it needs only Gaussian elimination, because $A$ itself is rank-deficient.""",
     r"""still: it needs only Gaussian elimination, because $A$ itself is rank-deficient. At version~2's parameters the same
reduction gives dimension 76 with 948 samples; we did not run the estimator there."""),
    (r"""\section{A uniform matrix does not repair the parameters}\label{sec:uniform}""",
     r"""\section{A uniform matrix does not repair version~1's parameters}\label{sec:uniform}"""),
    (r"""A later revision of the proposal replaced the Singer matrix by a uniform one. Table~\ref{tab:est} shows the estimator's
default attack set at the proposed parameters with a uniform matrix. The cheapest attack costs about $2^{51}$. An""",
     r"""The working specification~\cite{Gif26b} replaced the Singer matrix by a uniform one and kept version~1's parameters.
Table~\ref{tab:est} shows the estimator's default attack set at those parameters with a uniform matrix. The cheapest
attack costs about $2^{51}$. An"""),
    (r"""$4\,294\,977\,961$ (proposal) & 51.0 (BDD)""",
     r"""$4\,294\,977\,961$ (version~1) & 51.0 (BDD)"""),
    (r"""primes $\equiv1\pmod{455}$) are for orientation only.}\label{tab:est}""",
     r"""primes $\equiv1\pmod{455}$) are for orientation only; version~2 pairs $q=911$ with $n=1024$.}\label{tab:est}"""),
    (r"""would need a larger dimension or wider noise. We have not searched that space.""",
     r"""would need a larger dimension or wider noise. We have not searched that space. Version~2's parameters ($n=1024$,
$q=911$) are not in the table: with the Singer matrix they fall to Section~\ref{sec:rank}, and with a uniform matrix the
scheme becomes generic Module-LWE with sparse secrets, which we did not estimate."""),
    (r"""\section{Correctness is deterministic}""",
     r"""\section{Correctness}"""),
    (r"""and decryption never fails at the proposed parameters. It never fails for any $q>1032$. For CBD noise the distribution""",
     r"""and decryption never fails at version~1's parameters. It never fails for any $q>1032$; at version~2's $q=911$ it can
fail, though rarely. For CBD noise the distribution"""),
    (r"""$N\sim\mathrm{CBD}(258)$. At $q=911$ this gives $\Pr[|N|>227]=2^{-353.5}$ exactly.""",
     r"""$N\sim\mathrm{CBD}(258)$. At $q=911$ this gives $\Pr[|N|>227]=2^{-353.5}$ exactly, consistent with version~2's
Gaussian bound of $2^{-295}$."""),
    (r"""beyond the largest value $N$ can take. The correct statement is $\mathrm{DFR}=0$.""",
     r"""beyond the largest value $N$ can take. At that modulus the correct statement is $\mathrm{DFR}=0$."""),
    (r"""The Singer-orbit public matrix makes SLWE insecure at every module rank. A uniform matrix does not rescue the proposed
parameters, which reach about $2^{51}$.""",
     r"""The Singer-orbit public matrix makes SLWE insecure at every module rank, including both published parameter sets. A
uniform matrix does not rescue version~1's parameters, which reach about $2^{51}$."""),
    (r"""\begin{thebibliography}{9}\small""",
     r"""\begin{thebibliography}{99}\small"""),
    (r"""\bibitem{LS15} A.~Langlois""",
     r"""\bibitem{Gif26a} M.~Gifford. Fluid Lattice Topology: bridging PSL(2,7) vacuum geometry and non-associative
  post-quantum cryptography. Zenodo, 2026, versions 1 and 2. doi:10.5281/zenodo.20078312.
\bibitem{Gif26b} M.~Gifford. Sedenion Module-LWE and $\Phi$-modular prime project: master reference document, v2.1
  (May 10, 2026). File \texttt{tools/SLWE\_Prime\_Master\_v2.md} in the repository of Section~\ref{sec:repro}.
\bibitem{LS15} A.~Langlois"""),
]
out = t
for old, new in E:
    assert t.count(old) == 1, old[:60]
    out = out.replace(old, new, 1)
rev = out
for old, new in reversed(E):
    rev = rev.replace(new, old, 1)
assert rev == t
assert "Matt Gifford" not in out and "DRAFT" not in out and "contact email" not in out
assert "audit-followup-oct6" not in out and out.count(REF_COMMIT) == 1
assert "never published as secure" not in out and "the proposed parameters" not in out
assert out.count("\\cite{Gif26a}") == 2 and out.count("\\cite{Gif26b}") == 2
base = os.path.join(HERE, "slwe_negative_result_final")
open(base + ".tex", "w", encoding="utf-8").write(out)
env = dict(os.environ, SOURCE_DATE_EPOCH="1791212400", FORCE_SOURCE_DATE="1")
subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "-quiet", os.path.basename(base) + ".tex"],
               cwd=HERE, check=True, stdout=subprocess.DEVNULL, env=env)
for ext in (".aux", ".fls", ".fdb_latexmk", ".out", ".log"):
    if os.path.exists(base + ext):
        os.remove(base + ext)
for ext in (".tex", ".pdf"):
    b = open(base + ext, "rb").read()
    print(f"final{ext}: md5 {hashlib.md5(b).hexdigest()} ({len(b)} B)")
print(f"{len(E)} edits; reverse to the Phase C draft byte-identical — PASS")
