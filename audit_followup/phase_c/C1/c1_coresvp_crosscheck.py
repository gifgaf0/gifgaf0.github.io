#!/usr/bin/env python3
"""C1 DR-C1-2 cross-check: primal-uSVP core-SVP estimate (the 2016 estimate), written independently of the lattice
estimator's code (pre-registration C1_PREREG.md §3).

Model (Alkim–Ducas–Pöppelmann–Schwabe 2016, Kannan embedding with the secret rescaled to the error's width):
  lattice dimension d = n + m + 1, volume q^m · ν^n with ν = σ_e/σ_s;
  success when σ_e·sqrt(β) ≤ δ_β^(2β − d − 1) · Vol^(1/d),
  δ_β = ((π β)^(1/β) · β / (2π e))^(1/(2(β − 1)));
  cost 2^(0.292 β) classical (BDGL16 sieve), 2^(0.265 β) quantum. Minimised over m ≤ m_max.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
Q = 4294977961


def delta(beta):
    return ((math.pi * beta) ** (1 / beta) * beta / (2 * math.pi * math.e)) ** (1 / (2 * (beta - 1)))


def min_beta(n, q, sig_s, sig_e, m_max):
    nu = sig_e / sig_s
    best = None
    for m in range(1, m_max + 1):
        d = n + m + 1
        log_vol = m * math.log(q) + n * math.log(nu)
        for beta in range(40, d + 1):
            lhs = math.log(sig_e) + 0.5 * math.log(beta)
            rhs = (2 * beta - d - 1) * math.log(delta(beta)) + log_vol / d
            if lhs <= rhs:
                if best is None or beta < best[0]:
                    best = (beta, m, d)
                break
    return best


def report(label, n, q, sig_s, sig_e, m_max):
    beta, m, d = min_beta(n, q, sig_s, sig_e, m_max)
    r = {"label": label, "n": n, "q": q, "sigma_s": round(sig_s, 4), "sigma_e": sig_e, "m_max": m_max,
         "beta": beta, "m_used": m, "d": d, "log2_classical_coreSVP": round(0.292 * beta, 1),
         "log2_quantum_coreSVP": round(0.265 * beta, 1)}
    print(r)
    return r


if __name__ == "__main__":
    out = []
    # spec, uniform public matrix: n = 512, sparse ternary h = 64 (variance 64/512), CBD(2) error (variance 1), m <= 512
    out.append(report("spec n=512, uniform A, m<=512", 512, Q, math.sqrt(64 / 512), 1.0, 512))
    out.append(report("spec n=512, uniform A, m<=1024", 512, Q, math.sqrt(64 / 512), 1.0, 1024))
    # the reduced instance after the rank collapse: secret = the noise on 76 coordinates (CBD(2)), 436 samples
    out.append(report("rank-collapse reduction, n=76, m<=436", 76, Q, 1.0, 1.0, 436))
    # toy prime, for orientation
    out.append(report("toy q=911, n=512, uniform A, m<=512", 512, 911, math.sqrt(64 / 512), 1.0, 512))
    json.dump(out, open(os.path.join(HERE, "c1_coresvp_crosscheck.json"), "w"), indent=1)
