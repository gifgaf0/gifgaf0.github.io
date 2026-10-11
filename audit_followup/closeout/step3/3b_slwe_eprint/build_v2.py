#!/usr/bin/env python3
"""The revised SLWE negative-result note (October 10, 2026), built from the first version as deposited. Not deposited.

Plain-language summary: the first version (Zenodo 10.5281/zenodo.23270249) is mathematically sound, but an independent
audit found four statements that are wrong, all of them about other documents or about a side remark:
  1. the abstract cites a failure rate of 2^(-6.4e15) as "reported earlier", which reads as a claim of the proposing
     paper (Fluid Lattice Topology); it comes from the project's own ledger (section 2.66.1);
  2. Section 4 says the working specification [6] "kept version 1's parameters"; [6] targets q of about 3329, and its
     security table labels q = 911 "L5" and q = 3329 "L3";
  3. Section 2 presents the prime 4 294 977 961 and the secret weight 64 as version 1's own; version 1 gives only
     q of about 2^32 with q = 1 (mod 455) and sparse ternary secrets, so these are our instantiation;
  4. Section 5 says decryption "never fails for any q > 1032"; it fails at q = 1033 (a prime). The first prime at which
     it never fails is 1039.
The first version also described Table 1 as having three seed sets and a uniform control for every k; that held only
for k >= 8. This revision corrects all of these, runs the missing k <= 7 cases (same values), gives the failure rate at
q = 911 next to the tail, and adds what the first version left out: version 2's parameters after the rank collapse
(2^40.4) and with a uniform matrix (2^167.2; every lattice attack in the estimator's default set below the 2^272 of
Category 5), and [6]'s q = 3329 row. ("Version 1/2" means the proposing paper's versions, as in the note.)
Where the errors came from: error 2's sentence was written in the October 9 edits of build_final.py. Errors 1 and 3
became errors in those edits, which tied sentences of the Phase C draft to the proposing paper; in the draft, "reported
earlier" and "the proposed parameters" referred to the project's own documents. Error 4 was in the Phase C draft.

Mechanics: the source is slwe_negative_result_final.tex (the first version, md5 below). Each edit replaces a unique
string; applying the edits in reverse recovers the first version byte for byte. Section 7 cites the commit that holds
the new runs (v2_runs/). The PDF is built with latexmk/pdflatex and a fixed SOURCE_DATE_EPOCH.
"""
import hashlib, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "slwe_negative_result_final.tex")
SRC_MD5 = "b470bae54a389b5aa2f9a8b52c5bd279"
t = open(SRC, encoding="utf-8").read()
assert hashlib.md5(t.encode()).hexdigest() == SRC_MD5
OLD_COMMIT = "b09929ada97cc3c5bfc0f5f327518cd82e342fea"
REF_COMMIT = "d96d1f7451ffca96468ce1918f595370154558af"   # the commit that adds v2_runs/ and [6]'s v2.4 addendum
ACK_OLD = ("\\paragraph{Acknowledgements.} AI agents (Anthropic's Claude) drafted this note and wrote and ran all of its "
           "computations, including both independent rank implementations; the author directed the work, reviewed the "
           "text, and takes responsibility for it.")
ACK_NEW = ("\\paragraph{Acknowledgements.} AI agents (Anthropic's Claude) drafted this note and wrote and ran all of its "
           "computations, including both independent rank implementations. A separate Claude agent audited the first "
           "version of this note and found the errors corrected here. The author directed the work, reviewed the text, "
           "and takes responsibility for it.")
# "version 1/2" means the proposing paper's versions everywhere else in the note, so this note's versions are named plainly
CHANGES = r"""\paragraph{Changes in this revision.} The first version of this note (doi:10.5281/zenodo.23270249) contained four
errors, corrected here. Its abstract cited a failure rate of $2^{-6.4\times10^{15}}$ as ``reported earlier'', which reads
as a claim of~\cite{Gif26a}; the figure comes from the project's ledger~\cite{Led}. It said that~\cite{Gif26b} kept
version~1's parameters; that document targets $q\approx3329$. It presented the prime $4\,294\,977\,961$ and the weight 64
as version~1's own; they are our instantiation. And it said that decryption never fails for any $q>1032$, which is false
at $q=1033$. It also described Table~\ref{tab:rank} as having three seed sets and a uniform control for every $k$, which
held only for $k\ge8$; the runs for $k\le7$ are now made, with the same values. This revision also gives the failure
rate at $q=911$ next to the tail, adds estimates for version~2's parameters and for the $q=3329$ row of~\cite{Gif26b},
and compares both rows of~\cite{Gif26b} with their claims.

"""
E = [
    # typographic only: version 1's abstract overran its first line by 5.8 pt at "sixteen-dimensional"
    (r"""a Module-LWE variant over the sixteen-dimensional sedenion algebra that the""",
     r"""a Module-LWE variant over the 16-dimensional sedenion algebra that the"""),
    (r"\date{\small October 2026}", r"\date{\small October 2026 (revised)}"),
    # ---- abstract: version 2's figures; the ledger's Gaussian-tail figure leaves the abstract (it is attributed in §5)
    (r"""$2^{39}$ operations at the first set ($n=512$, $q\approx2^{32}$). Second, replacing the matrix by a uniform one does not
help at that set (centred binomial noise with $\eta=2$, ternary secrets of weight 64): the estimator gives about
$2^{51}$. Third, decryption at those parameters is deterministic: the noise is
bounded by 258, far below $q/4$; a failure rate of $2^{-6.4\times10^{15}}$ reported earlier came from a Gaussian tail
evaluated outside the support of a bounded sum. All computations are reproducible from public scripts.""",
     r"""$2^{39}$ operations at the first set ($n=512$, $q\approx2^{32}$) and $2^{40}$ at the second ($n=1024$, $q=911$). Second,
replacing the matrix by a uniform one does not restore the claim (centred binomial noise with $\eta=2$, ternary secrets
of weight 64): the estimator gives about $2^{51}$ at the first set and about $2^{167}$ at the second, against roughly
$2^{272}$ for Category~5. Third, decryption at the first set never fails: the noise is bounded by 258, far below $q/4$.
All computations are reproducible from public scripts."""),
    # ---- introduction: say where version 2's open attacks are checked
    (r"""moved to $k=64$ and $q=911$ ($n=1024$), and claimed Category~5 from a primal estimate, leaving the dual and hybrid
attacks to be checked. It kept""",
     r"""moved to $k=64$ and $q=911$ ($n=1024$), and claimed Category~5 from a primal estimate, leaving the dual and hybrid
attacks to be checked; Section~\ref{sec:uniform} checks them. It kept"""),
    (r"\section{The scheme}", r"\section{The scheme}\label{sec:scheme}"),
    (r"""e_2+m\lfloor q/2\rceil$.""",
     r"""e_2+m\lfloor q/2\rceil$.\footnote{For odd $q$, $\lfloor q/2\rceil$ stands for $\lfloor q/2\rfloor$ or $\lceil q/2\rceil$; the
  reference code uses $\lfloor q/2\rfloor$. Section~\ref{sec:correct} treats both.}"""),
    # ---- §2: what version 1 specifies, and what is our instantiation (audit item 3)
    (r"""Version~1's parameters are $k=32$ (so $n=16k=512$), $q=4\,294\,977\,961$ (the least prime $\equiv1\pmod{455}$ above
$2^{32}$), $h_s=h_r=64$, and noise CBD$(\eta=2)$. Version~2's are $k=64$ ($n=1024$) and $q=911$ (the least prime
$\equiv1\pmod{455}$), with the same weights and noise.""",
     r"""Version~1 specifies $n=512$ (so $k=32$), a modulus $q\approx2^{32}$ with $q\equiv1\pmod{455}$, and sparse ternary
secrets. We instantiate it with the least prime above $2^{32}$ that is $\equiv1\pmod{455}$, $q=4\,294\,977\,961$, and
with $h_s=h_r=64$ and CBD$(\eta=2)$ noise, the values of version~2 and of the project's ledger~\cite{Led}. Version~2
specifies $k=64$ ($n=1024$), $q=911$ (the least prime $\equiv1\pmod{455}$), $h_s=h_r=64$ and CBD$(2)$ noise."""),
    # ---- Table 1: the k <= 7 columns now have three seed sets and a control at both primes (v2_runs/table1_k1to7.py)
    (r"""\caption{Exact ranks over $\F_{911}$ (the values for $k\in\{8,16,32,64\}$ are identical over $\F_q$ with
$q=4\,294\,977\,961$, for three seed sets each, in both implementations).}\label{tab:rank}""",
     r"""\caption{Exact ranks over $\F_{911}$ and over $\F_q$ with $q=4\,294\,977\,961$, identical at both primes for three seed
sets each, in both implementations.}\label{tab:rank}"""),
    # ---- §3: version 2 after the collapse, now estimated
    (r"""reduction gives dimension 76 with 948 samples; we did not run the estimator there.""",
     r"""reduction gives dimension 76 with 948 samples, and the estimator reports $2^{40.4}$ (BDD hybrid, again at $\beta=40$)."""),
    # ---- §4: right sources for the uniform matrix and for the q = 2^32 setting (audit item 2); version 2 and [6]'s rows
    (r"\section{A uniform matrix does not repair version~1's parameters}\label{sec:uniform}",
     r"\section{A uniform matrix does not restore the claimed security}\label{sec:uniform}"),
    (r"""The working specification~\cite{Gif26b} replaced the Singer matrix by a uniform one and kept version~1's parameters.
Table~\ref{tab:est} shows the estimator's default attack set at those parameters with a uniform matrix. The cheapest
attack costs about $2^{51}$. An""",
     r"""After the rank deficiency was found, the project replaced the Singer matrix by a uniform one. Brief~06~\cite{Brief06}
adds a uniform perturbation to it, which at the strength chosen there ($\delta=1$) makes the matrix uniform, and puts it
into the key generation of the project's hybrid-KEM wrapper, whose target is $k=32$ with $q\approx2^{32}$~\cite{KEM}.
The working specification~\cite{Gif26b} states that its security table applies with this matrix. Table~\ref{tab:est}
shows the estimator's default attack set with a uniform matrix at version~1's setting as instantiated in
Section~\ref{sec:scheme}, at the two SLWE rows of the security table of~\cite{Gif26b}, at $q=2731$, and at version~2's
parameters. At version~1's setting the cheapest attack costs about $2^{51}$. An"""),
    # the cross-check is for weight 64; say what a dense secret does after it
    (r"""a block size near 70 already exposes the short vector in
dimension about 940.""",
     r"""a block size near 70 already exposes the short vector in
dimension about 940. A dense ternary secret instead of weight 64 changes little: about $2^{53}$."""),
    (r"""\begin{tabular}{lll}\toprule
$q$ & cheapest attack ($\log_2$ rop) & uSVP ($\log_2$ rop, $\beta$)\\\midrule
$4\,294\,977\,961$ (version~1) & 51.0 (BDD) & 52.1, $\beta=72$\\
$2731$ & 114.4 (dual hybrid) & 122.5, $\beta=330$\\
$911$ & 122.2 (BKW); 127.4 without BKW & 136.9, $\beta=383$\\\bottomrule
\end{tabular}
\caption{Lattice estimator~\cite{estimator}, commit \texttt{53da598}, default attacks and cost model~\cite{MATZOV}, at $n=512$, $m=512$, ternary
secret of weight 64 and CBD$(2)$ noise, with a uniform public matrix. The columns $q=911$ and $q=2731$ (the two smallest
primes $\equiv1\pmod{455}$) are for orientation only; version~2 pairs $q=911$ with $n=1024$.}\label{tab:est}""",
     r"""\begin{tabular}{rllll}\toprule
$n$ & $q$ & claimed & cheapest attack ($\log_2$ rop) & uSVP ($\log_2$ rop, $\beta$)\\\midrule
512 & $4\,294\,977\,961$ & Cat.~5 (v.~1) & 51.0 (BDD) & 52.1, $\beta=72$\\
512 & $3329$ & L3~\cite{Gif26b} & 112.2 (dual hybrid) & 120.3, $\beta=322$\\
512 & $2731$ & --- & 114.4 (dual hybrid) & 122.5, $\beta=330$\\
512 & $911$ & L5~\cite{Gif26b} & 122.2 (BKW)$^{a}$ & 136.9, $\beta=383$\\
1024 & $911$ & Cat.~5 (v.~2) & 167.2 (MITM hybrid)$^{b}$ & 253.9, $\beta=800$\\\bottomrule
\end{tabular}
\caption{Lattice estimator~\cite{estimator}, commit \texttt{53da598}, default attacks and cost model~\cite{MATZOV}, with a
uniform public matrix, $m=n$ samples, ternary secrets of weight 64 and CBD$(2)$ noise. ``Claimed'' is NIST Category~5
for the rows of versions~1 and~2 of~\cite{Gif26a}, and the level label of the security table of~\cite{Gif26b} for its
rows. Version~1's row uses the instantiation of Section~\ref{sec:scheme}; 2731 is the second-smallest prime
$\equiv1\pmod{455}$. $^{a}$BKW needs about $2^{110.7}$ samples, and a public key gives 512; the cheapest other attack
costs $2^{127.4}$. $^{b}$Without its meet-in-the-middle step the hybrid costs $2^{181.1}$.}\label{tab:est}"""),
    (r"""Even the smallest admissible prime falls short of $2^{128}$ at $n=512$ with these distributions, so a secure instance
would need a larger dimension or wider noise. We have not searched that space. Version~2's parameters ($n=1024$,
$q=911$) are not in the table: with the Singer matrix they fall to Section~\ref{sec:rank}, and with a uniform matrix the
scheme becomes generic Module-LWE with sparse secrets, which we did not estimate.""",
     r"""The working specification~\cite{Gif26b} targets $n=512$ with ``$\sim$3329 (mod-455 prime)''. Its security table
labels $q=911$ ``L5'' (408 bits classical) and $q=3329$ ``L3'' (341 bits), from a formula calibrated on Kyber that
assumes a full-rank matrix. With weight-64 secrets neither row reaches $2^{128}$: $q=911$ gives at most about $2^{127}$
and $q=3329$ about $2^{112}$. A dense ternary secret lifts $q=911$ only to about $2^{149}$. The ML-KEM modulus 3329 is
not $\equiv1\pmod{455}$; the nearest prime below it that is, 2731, gives about $2^{114}$. At $n=512$, then, even the
smallest admissible prime gives at most about $2^{127}$ with weight-64 secrets and CBD$(2)$ noise.

Version~2 took a larger dimension. With a uniform matrix, the estimator's cheapest attack on its parameters is the
primal hybrid with a meet-in-the-middle step, at about $2^{167}$; without that step the hybrid costs $2^{181}$. The other
lattice attacks cost $2^{239}$ (dual hybrid), $2^{249}$ (BDD), $2^{254}$ (primal uSVP, the attack version~2 used, at
$\beta=800$ against its claimed $\beta\approx942$) and $2^{268}$ (dual). NIST's thresholds are about $2^{143}$ classical
gates for Category~1, $2^{207}$ for Category~3 and $2^{272}$ for Category~5~\cite{NIST16}; version~2 measured its own
gate count against the last. Reading the estimator's operation counts as gate counts, every lattice attack in the
default set is below $2^{272}$, so version~2's Category~5 claim fails even with a uniform matrix, and the primal hybrid
attacks put its parameters below Category~3. We have not searched the space of $q$, $\eta$ and secret weight further."""),
    # ---- §5: the false threshold (audit item 4), and the failure rate next to the tail
    (r"\section{Correctness}", r"\section{Correctness}\label{sec:correct}"),
    (r"""and decryption never fails at version~1's parameters. It never fails for any $q>1032$; at version~2's $q=911$ it can
fail, though rarely. For CBD noise the distribution
is in fact exact: given $r$ and $s$, $N$ is a sum of $2(h_r+h_s+1)$ independent symmetric binomial draws, i.e.\
$N\sim\mathrm{CBD}(258)$. At $q=911$ this gives $\Pr[|N|>227]=2^{-353.5}$ exactly, consistent with version~2's
Gaussian bound of $2^{-295}$.""",
     r"""and decryption never fails at version~1's setting. The bound $258<q/4$ alone would suggest the same for every $q>1032$,
but at the boundary the half unit lost in rounding $q/2$ matters: at $q=1033$, a prime, the worst case $|N|=258$ decodes
wrongly with either rounding of $q/2$ and under every decoding rule we tried (thresholds at $q/4$ and $3q/4$, the
nearest point, rounding $2v/q$, and the reference code's branchless rounding). From $q=1036$ on it never fails under any
of them, so the first prime at which decryption never fails is 1039. At version~2's $q=911$ it can fail, though rarely.
For CBD noise the distribution is in fact exact: given $r$ and $s$, $N$ is a sum of $2(h_r+h_s+1)$ independent symmetric
binomial draws, i.e.\ $N\sim\mathrm{CBD}(258)$. At $q=911$ the tail is $\Pr[|N|>227]=2^{-353.5}$. The failure rate
itself, for a uniform message bit, depends on the rounding at the boundary: it is $2^{-353.9}$ for every rule and
rounding above except the reference code's decoder with its encoding $m\lfloor q/2\rfloor$, which gives $2^{-351.4}$.
Both are consistent with version~2's Gaussian bound of $2^{-295}$."""),
    (r"""An earlier analysis reported $\log_2\mathrm{DFR}\approx-6.4\times10^{15}$. That number is the Gaussian tail at""",
     r"""The project's working ledger~\cite{Led} reported $\log_2\mathrm{DFR}\approx-6.4\times10^{15}$ for version~1's setting.
That number is the Gaussian tail at"""),
    # ---- conclusion
    (r"""uniform matrix does not rescue version~1's parameters, which reach about $2^{51}$. The scheme's correctness was never in question. The general lesson is""",
     r"""uniform matrix does not restore the claimed security: version~1's setting reaches about $2^{51}$, and version~2's
parameters about $2^{167}$, below Category~5 under every lattice attack in the estimator's default set. The scheme's correctness
was never in question. The general lesson is"""),
    # ---- §7: the new commit, and the new runs
    (r"\begin{center}\texttt{" + OLD_COMMIT + r"}\end{center}",
     r"\par\nopagebreak\smallskip{\centering\texttt{" + REF_COMMIT + r"}\par}\smallskip"),
    (r"""\item the noise bounds and exact tails: \texttt{c1\_checks.py}.
\end{itemize}
Exact ranks were computed with python-flint.""",
     r"""\item the noise bounds and exact tails: \texttt{c1\_checks.py}.
\end{itemize}
The runs added in this revision are in the directory\par\nopagebreak\smallskip
{\centering\texttt{audit\_followup/closeout/step3/3b\_slwe\_eprint/v2\_runs/}:\par}\smallskip
\begin{itemize}
\item Table~\ref{tab:rank} for $k\le7$, with three seed sets and a uniform control at both primes in both
  implementations: \texttt{table1\_k1to7.py};
\item the estimator at version~2's parameters, at the $q=3329$ row of~\cite{Gif26b} and with dense ternary secrets:
  \texttt{v2\_estimator\_run.py};
\item the exact failure rates and the decoder scan of Section~\ref{sec:correct}: \texttt{dfr\_exact.py}.
\end{itemize}
Exact ranks were computed with python-flint."""),
    # ---- changes paragraph and acknowledgements
    (ACK_OLD, CHANGES + ACK_NEW),
    # ---- bibliography
    (r"""\bibitem{Gif26b} M.~Gifford. Sedenion Module-LWE and $\Phi$-modular prime project: master reference document, v2.1
  (May 10, 2026). File \texttt{tools/SLWE\_Prime\_Master\_v2.md} in the repository of Section~\ref{sec:repro}.""",
     r"""\bibitem{Gif26b} M.~Gifford. Sedenion Module-LWE and $\Phi$-modular prime project: master reference document, v2.0
  (May 10, 2026), with notes to v2.4 (October 10, 2026). File \texttt{tools/SLWE\_Prime\_Master\_v2.md} in the
  repository of Section~\ref{sec:repro}.
\bibitem{Brief06} Brief 06: Singer $A$ matrix rank restoration (OP-G). Project brief, May 2026. In the repository of
  Section~\ref{sec:repro}, file \texttt{tools/BRIEF\_06\_OP\_G.md}.
\bibitem{KEM} M.~Gifford. Hybrid PQC testbed: architectural specification, version 0.1. May 2026. File
  \texttt{hybrid\_kem/SPEC.md} in the repository of Section~\ref{sec:repro}.
\bibitem{Led} M.~Gifford. SQT master ledger, version 4.99 (October 2026), section 2.66.1 (May 20, 2026). File
  \texttt{SQT\_Master\_Ledger\_v4\_99\_CANONICAL.md} in the repository of Section~\ref{sec:repro}."""),
    (r"""\bibitem{Regev} O.~Regev.""",
     r"""\bibitem{NIST16} NIST. Submission requirements and evaluation criteria for the post-quantum cryptography
  standardization process. December 2016.
\bibitem{Regev} O.~Regev."""),
]
out = t
for old, new in E:
    assert t.count(old) == 1, old[:70]
    out = out.replace(old, new, 1)
rev = out
for old, new in reversed(E):
    assert rev.count(new) == 1, new[:70]
    rev = rev.replace(new, old, 1)
assert rev == t, "reverse check failed"
# the four audit items are gone, and nothing of version 1's wording that they flagged survives
for bad in ("reported earlier came", "kept version~1's parameters", "Version~1's parameters are",
            "It never fails for any $q>1032$", "we did not run the estimator there", "which we did not estimate",
            "for orientation only", "as written", "version~2)}", OLD_COMMIT):
    assert bad not in out, bad
assert out.count(REF_COMMIT) == 1 and out.count("\\cite{Led}") == 3 and out.count("\\cite{Brief06}") == 1
assert out.count("\\cite{NIST16}") == 1 and out.count("\\cite{KEM}") == 1 and "mg1388484" not in out
base = os.path.join(HERE, "slwe_negative_result_v2")
open(base + ".tex", "w", encoding="utf-8").write(out)
env = dict(os.environ, SOURCE_DATE_EPOCH="1791644400", FORCE_SOURCE_DATE="1")    # 2026-10-10 15:00 UTC
subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "-quiet", os.path.basename(base) + ".tex"],
               cwd=HERE, check=True, stdout=subprocess.DEVNULL, env=env)
log = open(base + ".log", encoding="utf-8", errors="replace").read()
assert "Overfull" not in log, "overfull box in the v2 build"
assert "There were undefined references" not in log and "Citation `" not in log and "Reference `" not in log, \
    "undefined reference or citation"
for ext in (".aux", ".fls", ".fdb_latexmk", ".out", ".log"):
    if os.path.exists(base + ext):
        os.remove(base + ext)
for ext in (".tex", ".pdf"):
    b = open(base + ext, "rb").read()
    print(f"revised{ext}: md5 {hashlib.md5(b).hexdigest()} ({len(b)} B)")
print(f"{len(E)} edits; reverse to version 1 byte-identical; no overfull boxes or undefined references — PASS")
