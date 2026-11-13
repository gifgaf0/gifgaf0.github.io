import json, glob, numpy as np
from sym2lib import window, per_prime, Xof
K=300; ks,w=window(K,"C"); X=Xof(K)
tlo=dict((p,t) for p,t in json.load(open("data/jobs_T300.json")))
diffs=[];full=[]
for f in sorted(glob.glob("data/HE_w*.npz")):
    z=dict(np.load(f))
    for i,p in enumerate(z["ps"]):
        p=int(p); a,b=z["offs"][i],z["offs"][i+1]; v=z["vals"][a:b]
        if p>5*X: continue
        rF=per_prime(p,np.arange(0,2*p),v,ks,w)
        lo=tlo[p]; rT=per_prime(p,np.arange(lo,2*p),v[lo:],ks,w)
        D=rF["D_c0"]+rF["D_c2"]
        sF=(rF["ell_c0"]+rF["ell_c2"])/D*np.sqrt(X); sT=(rT["ell_c0"]+rT["ell_c2"])/D*np.sqrt(X)
        diffs.append(sT-sF); full.append(sF)
d=np.array(diffs); print(f"K=300 tau=1e-4 truncation, sqrt(X)*E_S1, {len(d)} primes: max|diff|={np.abs(d).max():.2e} rms={np.sqrt((d**2).mean()):.2e}; rms of statistic={np.sqrt((np.array(full)**2).mean()):.3f}")
