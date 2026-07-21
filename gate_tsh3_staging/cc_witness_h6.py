"""Independent second-leg of chat H-6: the gem8 witness point g_w=1.5*g_c=33.03. Recorded
F-CONV drop was 1.0e-5; chat S9-lite deep fixed-a* gives 3.54e-10 (procedure noise, not
truncation). Confirm independently: certify gem8@33.03 (own a*), then deep fixed-a* F-CONV.
"""
import os,json,numpy as np
os.environ.setdefault("OMP_NUM_THREADS","1")
from tsh3_cc_solver import Kernel,Cell,solve_state,cert_state,speeds,certify
g=33.03; ker=Kernel("gem8")
c=certify("gem8",g,a_hint=1.38)   # own a* at the witness coupling
a=c["astar"]; dq=0.02*2*np.pi/a; out={}
for n in (32,40):
    cell=Cell(a,n); e_unif=0.5*g*float(np.atleast_1d(ker.Uh(0.0))[0])
    psi,e,mu,res=solve_state(cell,ker,g,seed=0,deep=True)
    cs=cert_state(cell,ker,g,psi,e,e_unif); psi=cs["psi"]
    dK=speeds(cell,ker,g,psi,mu,"K",dq); dM=speeds(cell,ker,g,psi,mu,"M",dq)
    out[n]=(0.5*(dK["cT"]+dM["cT"]),0.5*(dK["cL1"]+dM["cL1"]),res)
conv=max(abs(out[40][0]-out[32][0])/out[32][0],abs(out[40][1]-out[32][1])/out[32][1])
print(f"[H-6 gem8@33.03] a*={a:.5f} mu={c['mu']:.3f} RT={c['RT']:.5f} deep-fixed-a* F-CONV={conv:.2e} "
      f"(recorded drop 1.0e-5; chat S9-lite 3.54e-10) -> {'procedure-noise CONFIRMED (<<5e-6)' if conv<5e-6 else 'TRUNCATION'}")
json.dump(dict(g=g,astar=a,RT=c["RT"],conv_deep_fixed=float(conv)),open("cc_witness_h6.json","w"),indent=1)
