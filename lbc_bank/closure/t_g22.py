import sys, time, numpy as np
sys.path.insert(0, "/home/claude/sqt_persp/gate_tsh1_staging"); import g_tsh1_chatleg as T
sys.path.insert(0, "/home/claude/lbc_exploration"); from lbc_weights import bdg_full
from gsolve2d import tight, residual
t0=time.time()
st1, r1 = T.polish(T.relax_cell(1.4574710087903182, 22.0, "soft", Nc=96))
st2, rl, rn = tight(st1)
print("res first", r1, "lbfgs", rl, "nk", rn, "final", residual(st2["psi"], st2["ge"], st2["Uk"])[0], "ward", T.ward_check(st2, 22.0, "soft")[0], f"{time.time()-t0:.0f}s")
unit = 2*np.pi/1.4574710087903182
for kf in [0.005, 0.01, 0.03, 0.05, 0.1]:
    for d in ([1.0,0.0],[np.cos(np.pi/6), np.sin(np.pi/6)]):
        q = kf*unit; r = bdg_full(st2, 22.0, "soft", q*np.array(d), n=32)
        om, Z = r["om"][:3], r["Z"][:3]; it = int(np.argmin(Z/q))
        print(kf, d[1]>0, "cT=%.6f"%(om[it]/q), "others", [round(om[i]/q,5) for i in range(3) if i!=it])
