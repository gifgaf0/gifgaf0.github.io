"""G-TSH1 CC leg — PART 2b: F9 discipline. Deep-polish the ground state at a*=1.4575 to
drive the GP residual < 5e-3 (raw w2min > -0.05), then re-extract c_T/c_L1 to show the shear
speed is ROBUST to the H3 tiny-q Trotter contamination (independent reproduction of H3+F9).
"""
import numpy as np, time, json
from tsh1_cc_bdg import relax, bdg, branch, speed

g=22.0; a=1.4575; t0=time.time()
# deep polish: append finer-dt stages (kills Trotter-bias residual, F9)
st=relax(a,g,Nc=120,schedule=((0.001,9000),(3e-4,9000),(1e-4,15000),(3e-5,25000),(1e-5,15000)))
unit=2*np.pi/a
w=bdg(st,g,0.005*unit*np.array([1.0,0.0]),n=28)
print(f"[polish] GP-res={st['res']:.2e} (<5e-3 req)  raw w2min(kf=.005)={w['w2min']:.4f} (>-0.05 req)")
f9=bool(st['res']<=5e-3 and w['w2min']>-0.05)
print(f"[F9] {'PASS' if f9 else 'FAIL'}   gapless oms={[round(m['om'],3) for m in w['modes'][:5]]}")
kfs=[0.05,0.075,0.10,0.125,0.15,0.175,0.20]
br=branch(st,g,[1.0,0.0],kfs,n=28)
cT,pT=speed(br['T']); cL,pL=speed(br['L']); RT=cT/cL
print(f"[polished] c_T={cT:.4f} ({abs(cT-5.7749)/5.7749*100:.1f}%) c_L1={cL:.4f} "
      f"({abs(cL-11.0453)/11.0453*100:.1f}%) R_T={RT:.5f} ({abs(RT-0.52284)/0.52284*100:.1f}%) "
      f"pT={pT:.3f} pL={pL:.3f}")
json.dump(dict(res=st['res'],w2min=w['w2min'],f9=f9,mu=st['mu'],cT=cT,cL=cL,RT=RT,pT=pT,pL=pL),
          open('/home/user/gifgaf0.github.io/gate_tsh1_staging/tsh1_cc_polish_g22.json','w'),indent=1)
print(f"[polish] total {time.time()-t0:.0f}s")
