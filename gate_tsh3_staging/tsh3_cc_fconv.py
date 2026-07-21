"""G-TSH3 F-CONV diagnostic: isolate the true n=32->40 TRUNCATION convergence for gem8/gem4
by deep-converging (res 1e-12) at a FIXED a* and FIXED dq (no a*-reoptimization jitter, no
solver-residual noise). The `point`-run F-CONV was dominated by non-deep (res 1e-6) speed noise
+ a*-jitter — both ~1e-5, the gate scale. This measures the physics convergence.
"""
import os, json, numpy as np
os.environ.setdefault("OMP_NUM_THREADS","1")
from tsh3_cc_solver import Kernel, Cell, solve_state, cert_state, speeds
def fconv_fixed(name):
    d=json.load(open(f"{os.path.dirname(os.path.abspath(__file__))}/cc_point_{name}.json"))
    g=d["gstar"]; a=d["astar"]; ker=Kernel(name); dq=0.02*2*np.pi/a; out={}
    for n in (32,40):
        c=Cell(a,n); e_unif=0.5*g*float(np.atleast_1d(ker.Uh(0.0))[0])
        psi,e,mu,res=solve_state(c,ker,g,seed=0,deep=True)      # DEEP res 1e-12
        cs=cert_state(c,ker,g,psi,e,e_unif); psi=cs["psi"]
        dK=speeds(c,ker,g,psi,mu,"K",dq); dM=speeds(c,ker,g,psi,mu,"M",dq)
        cT=0.5*(dK["cT"]+dM["cT"]); cL1=0.5*(dK["cL1"]+dM["cL1"])
        out[n]=dict(cT=cT,cL1=cL1,RT=cT/cL1,res=res)
    conv=max(abs(out[40]["cT"]-out[32]["cT"])/out[32]["cT"], abs(out[40]["cL1"]-out[32]["cL1"])/out[32]["cL1"])
    print(f"[{name}] fixed-a* deep F-CONV = {conv:.2e} (gate 5e-6)  "
          f"cT32={out[32]['cT']:.5f} cT40={out[40]['cT']:.5f}  RT32={out[32]['RT']:.5f} RT40={out[40]['RT']:.5f} "
          f"res=({out[32]['res']:.1e},{out[40]['res']:.1e}) -> {'PASS' if conv<=5e-6 else 'FAIL'}")
    return name,float(conv),out[32]["RT"]
if __name__=="__main__":
    import sys
    res={}
    for nm in sys.argv[1:]:
        k,cv,rt=fconv_fixed(nm); res[k]=dict(fconv=cv,RT=rt,certify=bool(cv<=5e-6))
    json.dump(res,open(f"{os.path.dirname(os.path.abspath(__file__))}/cc_fconv_fixed.json","w"),indent=1)
