"""G-TSH1 CC leg — PART 2c: independent axis-(i) sweep. Compute R_T at soft-core g=28,34,44
from scratch (own a* scan + relax + polish + BdG) to test the Q2 axis-(i) PINNED claim:
the ratio holds ~2% while individual speeds change ~50%. Own D_axis_i computed at the end.
"""
import numpy as np, time, json
from tsh1_cc_bdg import relax, bdg, branch, speed, astar

SCHED=((0.001,8000),(3e-4,9000),(1e-4,15000),(3e-5,18000))
kfs=[0.05,0.075,0.10,0.125,0.15,0.175,0.20]
chat={28:0.52861,34:0.53476,44:0.54364}   # chat R_T (axis-i), for reference only
out={}
t0=time.time()
for g in [28.0,34.0,44.0]:
    a=astar(g,Nc=120,lo=1.35,hi=1.55,npts=9)
    st=relax(a,g,Nc=120,schedule=SCHED)
    unit=2*np.pi/a; w=bdg(st,g,0.005*unit*np.array([1.0,0.0]),n=28)
    f9=bool(st['res']<=5e-3 and w['w2min']>-0.05)
    br=branch(st,g,[1.0,0.0],kfs,n=28)
    cT,pT=speed(br['T']); cL,pL=speed(br['L']); RT=cT/cL
    out[int(g)]=dict(a=a,mu=st['mu'],res=st['res'],w2min=w['w2min'],f9=f9,cT=cT,cL=cL,RT=RT,pT=pT,pL=pL)
    print(f"[g={g:.0f}] a*={a:.4f} mu={st['mu']:.3f} F9={f9} c_T={cT:.4f} c_L1={cL:.4f} "
          f"R_T={RT:.5f} (chat {chat[int(g)]:.5f}, {abs(RT-chat[int(g)])/chat[int(g)]*100:.1f}%)  [{time.time()-t0:.0f}s]")
# independent axis-(i) pinning metric including canonical (polished) 0.52317
RTs=np.array([0.52317]+[out[g]['RT'] for g in [28,34,44]])
Di=float(np.max(np.abs(RTs-RTs.mean()))/RTs.mean())
print(f"\n[axis-i] R_T points (indep) = {[round(x,5) for x in RTs]}")
print(f"[axis-i] D = {Di*100:.2f}% (chat 2.10%)  -> {'PINNED (<3%)' if Di<0.03 else 'NOT PINNED'}")
print(f"[axis-i] individual c_T span {min(out[g]['cT'] for g in [28,34,44]):.2f}-{max(out[g]['cT'] for g in [28,34,44]):.2f} "
      f"vs canonical 5.78 (speeds change ~{(out[44]['cT']/5.78-1)*100:.0f}% while ratio holds {Di*100:.1f}%)")
out['axis_i_D']=Di
json.dump(out,open('/home/user/gifgaf0.github.io/gate_tsh1_staging/tsh1_cc_sweep.json','w'),indent=1)
print(f"[sweep] total {time.time()-t0:.0f}s")
