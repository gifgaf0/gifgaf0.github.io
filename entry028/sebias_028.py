"""sebias_028.py -- is the paired-strata s.e. unbiased under realistic height drift?
Replicates: c_hat_r ~ Normal(c(y_r), (1 - c(y_r)^2)/n) with the band's (2.16)-shaped drift (x1, and x100
as a stress case).  Compares E[se_pair] and E[se_pair^2] with the true s.e. of c_hat."""
import os as _os; PRED = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "pred")
import json, math, numpy as np
d = json.load(open(PRED + "/drift_216.json")); rng = np.random.default_rng(28); n = 12_500_000; P = 1000; reps = 20000
print("drift | char | E[se_pair]/se_true - 1 | E[se_pair^2]/var_true - 1 | MC precision (1 sd)")
for mult in (1, 100):
    for q in ("3", "4", "5"):
        c = np.array(d[q]); c = c.mean() + mult * (c - c.mean()); sd = np.sqrt((1 - c ** 2) / n)
        true = math.sqrt((sd ** 2).sum()) / len(c)
        x = c[None, :] + sd[None, :] * rng.standard_normal((reps, len(c)))
        dd = x[:, 1::2] - x[:, 0::2]; sp = np.sqrt((dd ** 2).sum(1)) / (2 * P)
        b1 = sp.mean() / true - 1; b2 = (sp ** 2).mean() / true ** 2 - 1
        print(f"x{mult:<4d} | q={q} | {b1:+.4%} | {b2:+.4%} | {sp.std()/true/math.sqrt(reps):.3%}")
