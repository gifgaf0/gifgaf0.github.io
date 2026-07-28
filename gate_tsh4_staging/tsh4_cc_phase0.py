#!/usr/bin/env python3
"""G-TSH4 Phase-0 CC recompute — INDEPENDENT from-scratch (chat core NOT imported).
Own 3D solver: preconditioned gradient descent to the TRUE discrete-GP minimum (res<=1e-8), NOT
the chat's split-step fixed point — so this independently (a) adjudicates the Q-A structure ordering
and (b) checks whether that ordering is robust to the split-step energy bias. Own kernel FTs, own
cell construction, own geometry optimization. Model e=<0.5|grad psi|^2>+(Lam/2)<n(U*n)>, <n>=1.
Usage: python3 tsh4_cc_phase0.py <step|gem8>
"""
import sys, os, json, numpy as np
os.environ.setdefault("OMP_NUM_THREADS","1")
from numpy.fft import fftn, ifftn, fftfreq
from scipy.special import gamma as Gamma
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar
OUT=os.path.dirname(os.path.abspath(__file__))

def utilde_step(k):
    k=np.asarray(k,float); o=np.empty_like(k); s=k<1e-3; ks=k[s]
    o[s]=4*np.pi*(1/3-ks**2/30+ks**4/840); kb=k[~s]
    o[~s]=4*np.pi*(np.sin(kb)-kb*np.cos(kb))/kb**3; return o
_GT=None
def utilde_gem8(k):
    global _GT
    if _GT is None:
        x,w=np.polynomial.legendre.leggauss(9000); r=0.5*3.2*(x+1); wr=0.5*3.2*w
        f=r*np.exp(-r**8)*wr; kk=np.linspace(0,520,26001); v=np.empty_like(kk)
        v[0]=4*np.pi*(1/8)*Gamma(3/8)
        for i in range(1,len(kk),256):
            j=min(i+256,len(kk)); kc=kk[i:j][:,None]
            v[i:j]=(4*np.pi/kk[i:j])*np.sum(f[None,:]*np.sin(kc*r[None,:]),axis=1)
        _GT=CubicSpline(kk,v)
    return _GT(np.clip(np.asarray(k,float),0,519.9))
KER={"step":utilde_step,"gem8":utilde_gem8}

def lambda_c(kern,kmax=60):
    f=KER[kern]; k=np.linspace(1e-6,kmax,400001); u=f(k); neg=u<0
    return float(np.min(-k[neg]**2/(4*u[neg])))

def sites(struct,a,c):
    if struct in("AA","AB","ABC"):
        Lx,Ly,Lz=a,a*np.sqrt(3),c; base=[(0,0),(a/2,a*np.sqrt(3)/2)]
        sh={"AA":[(0,0)],"AB":[(0,0),(a/2,a*np.sqrt(3)/6)],
            "ABC":[(0,0),(a/2,a*np.sqrt(3)/6),(a,a*np.sqrt(3)/3)]}[struct]
        S=[]
        for il,(sx,sy) in enumerate(sh):
            z=Lz*il/len(sh)
            for bx,by in base: S.append(((bx+sx)%Lx,(by+sy)%Ly,z))
        return (Lx,Ly,Lz),S
    if struct=="FCC": return (a,a,a),[(a*u,a*v,a*w) for u,v,w in [(0,0,0),(.5,.5,0),(.5,0,.5),(0,.5,.5)]]
    if struct=="BCC": return (a,a,a),[(a*u,a*v,a*w) for u,v,w in [(0,0,0),(.5,.5,.5)]]
def _fac(n):
    f=[];d=2
    while d*d<=n:
        while n%d==0: f.append(d);n//=d
        d+=1
    if n>1:f.append(n)
    return f or [1]
def grid(Ls,dx):
    N=[]
    for L in Ls:
        n=int(np.ceil(L/dx)); n+=n%2
        while max(_fac(n))>5: n+=2
        N.append(n)
    return tuple(N)
def ksq(Ls,Ns):
    K=np.meshgrid(*[2*np.pi*fftfreq(Ns[i],d=Ls[i]/Ns[i]) for i in range(3)],indexing="ij")
    return K[0]**2+K[1]**2+K[2]**2
def seed(Ls,Ns,S,wf=0.16,cst=6.0):
    xs=[np.linspace(0,Ls[i],Ns[i],endpoint=False) for i in range(3)]
    X,Y,Z=np.meshgrid(*xs,indexing="ij"); sig=wf*min(Ls); n=np.ones(Ns)
    for sx,sy,sz in S:
        dx=np.abs(X-sx);dx=np.minimum(dx,Ls[0]-dx);dy=np.abs(Y-sy);dy=np.minimum(dy,Ls[1]-dy)
        dz=np.abs(Z-sz);dz=np.minimum(dz,Ls[2]-dz); n+=cst*np.exp(-(dx**2+dy**2+dz**2)/(2*sig**2))
    n/=n.mean(); return np.sqrt(n)

def emr(psi,ks,Ut,Lam):
    npts=psi.size; n=psi*psi; nk=fftn(n); conv=np.real(ifftn(Ut*nk))
    kin=np.real(np.sum(0.5*ks*np.abs(fftn(psi))**2))/npts**2; inter=0.5*Lam*np.mean(n*conv)
    Hp=np.real(ifftn(0.5*ks*fftn(psi)))+Lam*conv*psi; mu=float(np.mean(psi*Hp))
    res=float(np.sqrt(np.mean((Hp-mu*psi)**2))/max(abs(mu),1e-12))
    return kin+inter,mu,res,Hp
def relax(psi,ks,Ut,Lam,iters=6000,tol=1e-8):
    nrm=lambda p:p/np.sqrt(np.mean(p*p)); psi=nrm(np.abs(psi)); e,mu,res,Hp=emr(psi,ks,Ut,Lam); dt=0.5
    for _ in range(iters):
        e,mu,res,Hp=emr(psi,ks,Ut,Lam)
        if res<=tol: break
        pre=np.real(ifftn(fftn(Hp-mu*psi)/(0.5*ks+max(abs(mu),1.0)))); p2=nrm(np.abs(psi-dt*pre))
        e2=emr(p2,ks,Ut,Lam)[0]
        if e2<=e+1e-15*abs(e): psi=p2
        else: dt*=0.5
        if dt<1e-4: break
    e,mu,res,_=emr(psi,ks,Ut,Lam); return psi,e,res
def struct_e(struct,a,c,kern,Lam,dx=0.05):
    Ls,S=sites(struct,a,c); Ns=grid(Ls,dx); ks=ksq(Ls,Ns); Ut=KER[kern](np.sqrt(ks))
    psi,e,res=relax(seed(Ls,Ns,S),ks,Ut,Lam); return e,res,Ls,psi
def optimize(struct,kern,Lam,a0,c0=None):
    if struct in("FCC","BCC"):
        r=minimize_scalar(lambda a:struct_e(struct,a,0,kern,Lam)[0],bounds=(a0*0.9,a0*1.1),method="bounded",options=dict(xatol=3e-4))
        e,res,Ls,_=struct_e(struct,r.x,0,kern,Lam); return e,res,float(r.x),None
    # hex: optimize a then c (few passes)
    a,c=a0,c0
    for _ in range(2):
        ra=minimize_scalar(lambda x:struct_e(struct,x,c,kern,Lam)[0],bounds=(a*0.93,a*1.07),method="bounded",options=dict(xatol=3e-4)); a=ra.x
        rc=minimize_scalar(lambda x:struct_e(struct,a,x,kern,Lam)[0],bounds=(c*0.93,c*1.07),method="bounded",options=dict(xatol=5e-4)); c=rc.x
    e,res,Ls,_=struct_e(struct,a,c,kern,Lam); return e,res,float(a),float(c)

# chat's reported optimal geometries (STARTING points only; CC re-optimizes independently)
G0={"step":{"AA":(1.2953,1.3609),"AB":(1.4001,2.2843),"ABC":(1.3998,3.4288),"FCC":(1.9796,None),"BCC":(1.5740,None)},
    "gem8":{"AA":(1.2830,1.3429),"AB":(1.3897,2.2680),"ABC":(1.3895,3.4036),"FCC":(1.9650,None),"BCC":(1.5570,None)}}

if __name__=="__main__":
    kern=sys.argv[1]; Lam=2.0*lambda_c(kern); out={"kernel":kern,"Lam":Lam,"structures":{}}
    print(f"[CC {kern}] Lam_c={Lam/2:.6f} Lam={Lam:.6f}",flush=True)
    for st in ("AA","AB","ABC","FCC","BCC"):
        a0,c0=G0[kern][st]; e,res,a,c=optimize(st,kern,Lam,a0,c0)
        out["structures"][st]=dict(e=e,res=res,a=a,c=c,coa=(c/a if c else None))
        print(f"  {st}: e={e:.9f} res={res:.1e} a={a:.5f}"+(f" c={c:.5f} c/a={c/a:.5f}" if c else ""),flush=True)
    es={k:v["e"] for k,v in out["structures"].items()}; mn=min(es,key=es.get)
    out["argmin"]=mn; e1=es[mn]; e2=min(v for k,v in es.items() if k!=mn)
    out["gap_to_2nd"]=(e2-e1)/abs(e1); out["ordering"]=sorted(es,key=es.get)
    # F-3: ABC free-c/a vs sqrt(6) fcc containment
    coa_abc=out["structures"]["ABC"]["coa"]; out["F3_ABC_coa_vs_sqrt6"]=(coa_abc,np.sqrt(6),abs(coa_abc-np.sqrt(6))/np.sqrt(6))
    out["F3_ABC_eq_FCC_rel"]=abs(out["structures"]["ABC"]["e"]-out["structures"]["FCC"]["e"])/abs(out["structures"]["FCC"]["e"])
    print(f"[CC {kern}] argmin={mn} gap_to_2nd={out['gap_to_2nd']:.4e} (delta_E=1e-4) ordering={out['ordering']}")
    print(f"[CC {kern}] F-3: ABC c/a={coa_abc:.5f} vs sqrt6={np.sqrt(6):.5f} ({out['F3_ABC_coa_vs_sqrt6'][2]:.1e}); ABC vs FCC e-rel={out['F3_ABC_eq_FCC_rel']:.1e}")
    json.dump(out,open(f"{OUT}/cc_phase0_{kern}.json","w"),indent=1)
