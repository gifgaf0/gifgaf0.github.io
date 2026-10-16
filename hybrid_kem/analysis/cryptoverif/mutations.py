#!/usr/bin/env python3
"""Mutation tests for the CryptoVerif models of HYBRID-AKE.

Each mutation weakens one design element of the protocol or one assumption,
re-runs CryptoVerif with the same proof, and checks that the affected query
is no longer proved (and, where noted, that the others still are). A proof
that survives a mutation it should not survive would mean the model does not
depend on that element; a failure here is therefore a finding, not noise.

Failing to prove is not by itself an attack: CryptoVerif is sound but not
complete. Each entry says what the mutation removes and why a proof should
need it. Entries marked "control" are expected to stay proved; the
fresh_* entries remove the twelve freshness and RevealKey guards of the
protocol model one at a time, checking that each is load-bearing (so the
reveal oracles have effect and no guard is dead code).

Usage (normally via `make mutations`):
    python3 mutations.py --cryptoverif PATH --libdir DIR [--m4 m4]
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))

AUTH_ONLY_PROOF = """proof {
   crypto uf_cma_corrupt(sign) rK;
   success;
   simplify;
   success
}
"""

TH_IN_DECL = "fun th_in(bitstring, idname, pkey, kempkey, ciphertext): hashinput [data]."
TH_DISEQ = (
    "equation forall a: bitstring, b: idname, c: pkey, d: kempkey, e: ciphertext,\n"
    "                x: hashoutput, s: signature;\n"
    "   th_in(a, b, c, d, e) <> th2_in(x, s)."
)
TH_USES = [
    ("th_in(iidI, idRI, vkRI, pkE, ctI)", "I"),
    ("th_in(iidR, myid, myvk, pkER, ctR)", "R"),
    ("th_in(iidA, myid, myvk, pkEA, ctA)", "A"),
]
CTX_DECL = (
    "fun msgI(hashoutput): sigmsg [data].\n"
    "equation forall x: hashoutput, y: hashoutput; msgR(x) <> msgI(y)."
)


def _drop_arg(use: str, idx: int) -> str:
    head, args = use.split("(", 1)
    parts = [p.strip() for p in args.rstrip(")").split(",")]
    del parts[idx]
    return f"{head}({', '.join(parts)})"


def replace_proof(text: str, proof: str) -> str:
    a = text.index("proof {")
    b = text.index("\n}\n", a) + 3
    return text[:a] + proof + text[b:]


@dataclass
class Mutation:
    name: str
    source: str                      # model file (an .m4.ocv needs `variant`)
    removes: str                     # what the mutation takes away
    why: str                         # why a proof should need it
    edits: list = field(default_factory=list)   # (old, new) pairs, each must match
    variant: str | None = None
    lib: str = "pq"
    proof: str | None = None         # replacement proof block, if any
    drop_queries: list = field(default_factory=list)
    expect: dict = field(default_factory=dict)  # query key -> True (proved) / False
    expect_error: str | None = None  # substring of the expected CryptoVerif error


def mutations() -> list[Mutation]:
    no_ct = [(TH_IN_DECL, TH_IN_DECL.replace(", ciphertext)", ")")),
             (TH_DISEQ, TH_DISEQ.replace(", e: ciphertext", "").replace("th_in(a, b, c, d, e)", "th_in(a, b, c, d)"))]
    no_ct += [(u, _drop_arg(u, 4)) for u, _ in TH_USES]
    no_vk = [(TH_IN_DECL, TH_IN_DECL.replace("idname, pkey, kempkey", "idname, kempkey")),
             (TH_DISEQ, TH_DISEQ.replace(" c: pkey,", "").replace("th_in(a, b, c, d, e)", "th_in(a, b, d, e)"))]
    no_vk += [(u, _drop_arg(u, 2)) for u, _ in TH_USES]
    no_ctx = [(CTX_DECL, "letfun msgI(x: hashoutput) = msgR(x).")]
    secrecy = ["query secret keyI.\n", "query secret keyR.\n"]
    all_ake = {"inj-event(endR": True, "inj-event(endI": True,
               "secrecy of keyI": True, "secrecy of keyR": True,
               "event(endI(iid1": True}          # key uniqueness

    def guard(name, old, new, query, why):
        return Mutation(
            name=f"fresh_{name}", source="hybrid_ake.ocv",
            removes=f"freshness guard: {why}",
            why="each freshness/RevealKey guard must be load-bearing, or the "
                "reveal oracles would be ineffective (a vacuity check)",
            edits=[(old, new)],
            expect={query: False})

    xwing_c2pri = re.search(
        r"proba Pbind\.\n.*?2-proj-mpair\(mencap_r\(mpkgen\(s\), r\)\)\)\.",
        open(os.path.join(HERE, "kem_xwing.m4.ocv")).read(), re.S).group(0)
    bb_no_ctm = [
        ("fun bb_input(msec, G, mct, G, mpkey, G): comb_in [data].",
         "fun bb_input(msec, G, G, mpkey, G): comb_in [data]."),
        ("bb_input(ssM, ssX, ctM, ctX, pkM, pkX)", "bb_input(ssM, ssX, ctX, pkM, pkX)"),
        ("bb_input(ssMd, exp(ctXd, xs), ctMd, ctXd, pkMd, pkXd)",
         "bb_input(ssMd, exp(ctXd, xs), ctXd, pkMd, pkXd)"),
        ("let bb_input(ssM0: msec, dh0: G, ctM0: mct, ctX0: G, pkM0: mpkey, pkX0: G) = x1 in",
         "let bb_input(ssM0: msec, dh0: G, ctX0: G, pkM0: mpkey, pkX0: G) = x1 in"),
        ("let bb_input(ssM0: msec, dh0: G, ctM0: mct, ctX0: G, pkM0: mpkey, pkX0: G) = x1_1 in",
         "let bb_input(ssM0: msec, dh0: G, ctX0: G, pkM0: mpkey, pkX0: G) = x1_1 in"),
    ]
    return [
        Mutation(
            name="ake_auth_only_baseline",
            source="hybrid_ake.ocv",
            removes="nothing (control for the two authentication-only mutants)",
            why="the signature step alone proves both agreement queries on the "
                "real model, so their failure below is due to the mutation",
            proof=AUTH_ONLY_PROOF, drop_queries=secrecy,
            expect={"inj-event(endR": True, "inj-event(endI": True},
        ),
        Mutation(
            name="ake_no_ct_in_transcript",
            source="hybrid_ake.ocv",
            removes="the KEM ciphertext ct from the transcript hash TH",
            why="the responder's signature must bind ct, or a man in the middle "
                "can replace it with its own encapsulation to pk_e",
            edits=no_ct, proof=AUTH_ONLY_PROOF, drop_queries=secrecy,
            expect={"inj-event(endR": False, "inj-event(endI": False},
        ),
        Mutation(
            name="ake_no_ct_in_transcript_full_proof",
            source="hybrid_ake.ocv",
            removes="ct from TH, with the full proof",
            why="the KEM-correctness step (the initiator decapsulated the "
                "honest responder's ciphertext) can no longer be justified",
            edits=no_ct,
            expect_error="I cannot prove that the term you want to put is equal",
        ),
        Mutation(
            name="ake_no_vkR_in_transcript",
            source="hybrid_ake.ocv",
            removes="the responder's verification key vk_R from TH",
            why="without it the initiator's msg3 does not commit to which "
                "responder it accepted (unknown key share under plain UF-CMA)",
            edits=no_vk,
            expect={"inj-event(endR": False, "inj-event(endI": True,
                    "secrecy of keyI": True, "secrecy of keyR": True},
        ),
        Mutation(
            name="ake_no_context_strings",
            source="hybrid_ake.ocv",
            removes="the separation between CTX_R and CTX_I",
            why="(control) still proved: the two signed hash inputs LP(7 "
                "fields) and LP(2 fields) can never coincide, so the context "
                "strings are a second, redundant layer of role separation",
            edits=no_ctx,
            expect=dict(all_ake),
        ),
        Mutation(
            name="ake_no_context_strings_no_encoding_separation",
            source="hybrid_ake.ocv",
            removes="both the CTX_R/CTX_I separation and the disjointness of "
                    "the two LP encodings",
            why="with neither, a responder's signature on TH could be reused "
                "as an initiator's msg3 signature",
            edits=no_ctx + [(TH_DISEQ, "")],
            proof=AUTH_ONLY_PROOF, drop_queries=secrecy,
            expect={"inj-event(endR": False},
        ),
        # Initiator freshness (testI): honest peer, uncorrupted peer, no
        # revealed mutual-responder partner, no revealed responder-only partner.
        guard("test_I_dishonest_peer",
              "          else false);\n      return(sigI);",
              "          else (keyI: sesskey <- kI; true));\n      return(sigI);",
              "secrecy of keyI",
              "an initiator is tested even if its peer is not an honest party"),
        guard("test_I_corrupted_peer",
              "             (if defined(corruptK[jP]) then false\n",
              "             (if false then false\n",
              "secrecy of keyI",
              "an initiator is tested even if its peer was corrupted before it accepted"),
        guard("test_I_despite_revealed_R",
              "                find jR1 <= NR, jRK1 <= NK suchthat defined(thR[jR1, jRK1], revR[jR1, jRK1]) && thI = thR[jR1, jRK1] then false\n"
              "                orfind jA1",
              "                find jA1", "secrecy of keyI",
              "an initiator is tested even if its mutual-responder partner's key was revealed"),
        guard("test_I_despite_revealed_A",
              "                orfind jA1 <= NRa, jAK1 <= NK suchthat defined(thA[jA1, jAK1], revA[jA1, jAK1]) && thI = thA[jA1, jAK1] then false\n",
              "", "secrecy of keyI",
              "an initiator is tested even if its responder-only partner's key was revealed"),
        guard("reveal_I_despite_tested_R",
              "      find jR2 <= NR, jRK2 <= NK suchthat defined(thR[jR2, jRK2], keyR[jR2, jRK2]) && thI = thR[jR2, jRK2] then\n"
              "         return(NoLeak)\n"
              "      else\n",
              "", "secrecy of keyR",
              "an initiator's key is revealed even if its partner's is tested"),
        # Mutual-responder freshness (testR): honest peer, uncorrupted peer,
        # no revealed initiator partner.
        guard("test_R_dishonest_peer",
              "          else false);\n      return();",
              "          else (keyR: sesskey <- kR; true));\n      return();",
              "secrecy of keyR",
              "a mutual responder is tested even if its peer is not an honest party"),
        guard("test_R_corrupted_peer",
              "             (if defined(corruptK[jP2]) then false\n",
              "             (if false then false\n",
              "secrecy of keyR",
              "a mutual responder is tested even if its peer was corrupted before it accepted"),
        guard("test_R_despite_revealed_I",
              "                find jI1 <= NI, jIK1 <= NK suchthat defined(thI[jI1, jIK1], revI[jI1, jIK1]) && thR = thI[jI1, jIK1] then false\n"
              "                else\n",
              "", "secrecy of keyR",
              "a responder is tested even if its partner's key was revealed"),
        guard("reveal_R_despite_tested_I",
              "      find jI2 <= NI, jIK2 <= NK suchthat defined(thI[jI2, jIK2], keyI[jI2, jIK2]) && thR = thI[jI2, jIK2] then\n"
              "         return(NoLeak)\n"
              "      else\n",
              "", "secrecy of keyI",
              "a responder's key is revealed even if its partner's is tested"),
        guard("reveal_A_despite_tested_I",
              "      find jI3 <= NI, jIK3 <= NK suchthat defined(thI[jI3, jIK3], keyI[jI3, jIK3]) && thA = thI[jI3, jIK3] then\n"
              "         return(NoLeak)\n"
              "      else\n",
              "", "secrecy of keyI",
              "a responder-only key is revealed even if its partner's is tested"),
        guard("reveal_tested_I",
              "      if testI then return(NoLeak) else",
              "      if false then return(NoLeak) else", "secrecy of keyI",
              "RevealKey also answers for a tested initiator"),
        guard("reveal_tested_R",
              "      if testR then return(NoLeak) else",
              "      if false then return(NoLeak) else", "secrecy of keyR",
              "RevealKey also answers for a tested mutual responder"),
        Mutation(
            name="ephleak_test_revealed_sessions",
            source="hybrid_ake_ephleak.ocv",
            removes="the freshness condition excluding responder sessions that "
                    "encapsulated to a revealed ephemeral key",
            why="the adversary can decapsulate under a revealed ephemeral, so "
                "such keys are not secret (cf. eph_reveal_breaks_session in "
                "../hybrid_ake_ext.spthy)",
            edits=[(
                "                find jL <= NL, jLK <= NK suchthat defined(pkEL[jL, jLK]) && pkER = pkEL[jL, jLK] then false\n"
                "                orfind jI1 <= NI,",
                "                find jI1 <= NI,")],
            expect={"secrecy of keyR": False, "secrecy of keyI": True,
                    "inj-event(endR": True, "inj-event(endI": True},
        ),
        Mutation(
            name="composite_no_prehash_collision_resistance",
            source="composite_sig.m4.ocv", variant="MLDSA_SECURE",
            removes="collision resistance of the composite pre-hash PH",
            why="components sign M' = ... || PH(M); a PH collision transfers a "
                "signature from M to M'",
            edits=[("expand CollisionResistant_hash(hashkey, bitstring, phout, PH, PHoracle, Phash).",
                    "fun PH(hashkey, bitstring): phout.\nlet PHoracle(k: hashkey) = OH() := return(k).")],
            expect={"event(accepted": False},
        ),
        Mutation(
            name="xwing_x25519_branch_no_c2pri",
            source="kem_xwing.m4.ocv", variant="X25519_SECURE", lib="default",
            removes="C2PRI of ML-KEM in the X25519-only branch of X-Wing",
            why="X-Wing does not hash ct_M; with ML-KEM broken, a second "
                "ciphertext with the same ss_M would decapsulate to the "
                "challenge key",
            edits=[(xwing_c2pri, "")],
            expect={"indistinguishability": False},
        ),
        Mutation(
            name="bbfgs_rom_no_ctM_in_combiner",
            source="kem_bbfgs_x25519_rom.ocv", lib="default",
            removes="ct_M from the inputs of the ML-KEM-1024 profile's combiner",
            why="(contrast with X-Wing) this profile needs no C2PRI only "
                "because its combiner hashes ct_M",
            edits=bb_no_ctm,
            expect={"indistinguishability": False},
        ),
    ]


def run(m: Mutation, cv: str, libdir: str, m4: str, work: str) -> tuple[bool, str]:
    path = os.path.join(HERE, m.source)
    if m.variant:
        text = subprocess.run([m4, "-D", m.variant, path], check=True,
                              capture_output=True, text=True).stdout
    else:
        with open(path) as f:
            text = f.read()
    for old, new in m.edits:
        if old not in text:
            return False, f"edit did not apply: {old[:60]!r}"
        text = text.replace(old, new)
    for q in m.drop_queries:
        if q not in text:
            return False, f"query not found: {q!r}"
        text = text.replace(q, "")
    if m.proof:
        text = replace_proof(text, m.proof)
    model = os.path.join(work, f"{m.name}.ocv")
    with open(model, "w") as f:
        f.write(text)
    out = subprocess.run([cv, "-lib", os.path.join(libdir, m.lib), "-o", work, model],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, timeout=1800).stdout
    with open(os.path.join(work, f"{m.name}.log"), "w") as f:
        f.write(out)
    if m.expect_error:
        ok = m.expect_error in out
        return ok, ("aborted as expected: " if ok else "expected error not seen: ") + m.expect_error
    proved = [ln for ln in out.splitlines() if ln.startswith("RESULT Proved")]
    unproved = " ".join(ln for ln in out.splitlines() if ln.startswith("RESULT Could not prove"))
    notes, ok = [], True
    for key, want in m.expect.items():
        got_p = any(key in ln for ln in proved)
        got_u = key in unproved
        if want and not got_p:
            ok = False; notes.append(f"{key}: expected proved, was not")
        elif not want and not got_u:
            ok = False; notes.append(f"{key}: expected NOT proved, but it was")
        else:
            notes.append(f"{key}: {'proved' if want else 'not proved'} (as expected)")
    return ok, "; ".join(notes)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cryptoverif", required=True)
    ap.add_argument("--libdir", required=True)
    ap.add_argument("--m4", default="m4")
    ap.add_argument("--keep", help="directory to keep mutants and logs in")
    args = ap.parse_args()
    work = args.keep or tempfile.mkdtemp(prefix="cv-mutations-")
    os.makedirs(work, exist_ok=True)
    failures = 0
    for m in mutations():
        ok, note = run(m, args.cryptoverif, args.libdir, args.m4, work)
        failures += not ok
        print(f"{'OK  ' if ok else 'FAIL'} {m.name}\n     removes: {m.removes}\n     {note}")
    print(f"\n{len(mutations()) - failures}/{len(mutations())} mutation tests behaved as expected"
          f" (mutants and logs in {work})")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
