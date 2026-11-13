import json, math, numpy as np, cypari2
from sym2lib import window, alpha_cut, Xof
pari=cypari2.Pari()
out={}
for K in (300,1000,2500):
    ks,w=window(K,"C"); a=alpha_cut(ks,w,tau=1e-4)
    X=Xof(K); P=5*X
    ps=[int(q) for q in pari(f"primes([2,{int(P)}])")]
    r=math.ceil(len(ps)/6000) if len(ps)>6000 else 1
    sel=ps[::r]
    jobs=[[p,max(0,int(math.floor(2*p*math.cos(a)))-1)] for p in sel]
    nH=sum(2*p-tlo for p,tlo in jobs)
    maxN=max(4*p*p-tlo*tlo for p,tlo in jobs)
    out[K]=dict(alpha_cut=a,alphaK=a*K,nprimes=len(ps),r=r,nsel=len(sel),nH=nH,maxN=maxN)
    json.dump(sorted(jobs,key=lambda j:-(2*j[0]-j[1])),open(f"data/jobs_T{K}.json","w"))
    print(K,out[K])
json.dump(out,open("data/cuts.json","w"),indent=1)
