#!/usr/bin/env python3
"""G-TSH3 CC leg — PART 2: full-from-scratch solver (E4). Fresh code; TSH1/TSH2 solvers NOT
imported. Own Bessel-zero-subdivided Hankel tables (H-2-safe), own L-BFGS+Sobolev-preconditioned
descent (no Trotter — H-3-safe), own σ-parity classifier, own reducer. Implements AUTH-INST-1
exactly: Δq=0.02·(2π/a*), forced-origin ω-vs-q, j=2..6, W1=j2-4/W2=j4-6, Γ→K & Γ→M averaged,
F-LIN[0.95,1.05], F-ISO≤2%, F-CONV(n32→40)≤5e-6, F-CLS fT≥0.95. Substrate units ħ=m=ρ0=1.
No physical-c/observable/threshold here. Usage: python3 tsh3_cc_solver.py controls|anchor <k> <g>|point <k>
"""
import sys, os, json, numpy as np
from scipy.special import j0, j1, jv, jn_zeros
from scipy.optimize import minimize, minimize_scalar
from scipy.interpolate import CubicSpline
from scipy.linalg import eigh
OUT=os.path.dirname(os.path.abspath(__file__)); SQ3=np.sqrt(3.0)
def t1():
    pats=["299"+"792458","2.998"+"e8","GW"+"170817","gold"+"en","1.61"+"80","0.381"+"966","theta"+"_1"]
    s=open(os.path.abspath(__file__)).read().split("def t1")[1]
    assert not [p for p in pats if p in s], "T1 trip"
    print("[T1] clean")

# ---- own oscillation-safe Hankel table (Bessel-zero-subdivided 12-pt Gauss-Legendre) ----
_GX,_GW=np.polynomial.legendre.leggauss(12)
def hankel_table(U,rmax,ks):
    nz=int(np.ceil(ks.max()*rmax/np.pi))+4; z=np.concatenate([[0.0],jn_zeros(0,nz)])
    out=np.empty_like(ks)
    for i,k in enumerate(ks):
        edges=np.linspace(0,rmax,33) if k<1e-9 else np.append(z[z<k*rmax]/max(k,1e-300),rmax)
        a,b=edges[:-1],edges[1:]; mid=0.5*(a+b)[:,None]; half=0.5*(b-a)[:,None]
        r=mid+half*_GX[None,:]; w=half*_GW[None,:]
        out[i]=2*np.pi*float(np.sum(w*U(r)*j0(k*r)*r))
    return out

class Kernel:
    def __init__(s,name):
        s.name=name
        if name=="step": s.Uh=lambda k: np.where(np.asarray(k)<1e-9,np.pi,2*np.pi*j1(np.maximum(k,1e-9))/np.maximum(k,1e-9))
        elif name=="cap_p1": s.Uh=lambda k: np.where(np.asarray(k)<1e-6,np.pi/2,4*np.pi*jv(2,np.maximum(k,1e-6))/np.maximum(k,1e-6)**2)
        elif name=="cap_p2": s.Uh=lambda k: np.where(np.asarray(k)<1e-6,np.pi/3,16*np.pi*jv(3,np.maximum(k,1e-6))/np.maximum(k,1e-6)**3)
        else:
            tab=f"{OUT}/cc_uhat_{name}.npz"
            if os.path.exists(tab): z=np.load(tab); ks,uk=z["ks"],z["uk"]
            else:
                if name.startswith("gem"): p=float(name[3:]); U=lambda r: np.exp(-r**p); rmax={3.0:6.0,4.0:5.0,8.0:3.0}[p]
                elif name.startswith("gamma"): p=float(name[5:]); U=lambda r: 1.0/(1.0+r**p); rmax=14.0
                # validate builder vs analytic step before use
                kv=np.concatenate([np.linspace(0.01,30,40),np.linspace(30,419,60)])
                assert np.max(np.abs(hankel_table(lambda r:(r<1.0)*np.ones_like(r),1.0,kv)-2*np.pi*j1(kv)/kv))<1e-9
                ks=np.linspace(0.0,420.0,4200); uk=hankel_table(U,rmax,ks); np.savez(tab,ks=ks,uk=uk)
            sp=CubicSpline(ks,uk); s.Uh=lambda k,sp=sp: sp(np.clip(k,0.0,419.9))

class Cell:
    def __init__(s,a,n,shear=0.0):
        s.a,s.n=a,n; a1=np.array([a,0.0]); a2=np.array([a/2+shear*a,a*SQ3/2])
        Am=np.stack([a1,a2],1); B=2*np.pi*np.linalg.inv(Am).T; s.b1,s.b2=B[:,0],B[:,1]
        m=np.fft.fftfreq(n,d=1.0/n); M1,M2=np.meshgrid(m,m,indexing="ij"); s.M1,s.M2=M1.astype(int),M2.astype(int)
        s.Gx=M1*s.b1[0]+M2*s.b2[0]; s.Gy=M1*s.b1[1]+M2*s.b2[1]; s.G2=s.Gx**2+s.Gy**2; s.area=abs(np.linalg.det(Am))
def meanfield(c,ker,g,rho): return np.real(np.fft.ifft2(ker.Uh(np.sqrt(c.G2))*(np.fft.fft2(rho)/c.n**2)*c.n**2))*g
def emr(c,ker,g,psi):
    n2=c.n**2; pG=np.fft.fft2(psi)/n2; kin=np.real(np.sum(c.G2*np.abs(pG)**2))/2.0
    rho=psi**2; rG=np.fft.fft2(rho)/n2; eint=0.5*g*np.real(np.sum(ker.Uh(np.sqrt(c.G2))*np.abs(rG)**2))
    Phi=meanfield(c,ker,g,rho); Hp=np.real(np.fft.ifft2(c.G2/2.0*pG*n2))+Phi*psi
    mu=float(np.mean(psi*Hp)); res=float(np.sqrt(np.mean((Hp-mu*psi)**2))/max(abs(mu),1e-12))
    return kin+eint,mu,res,Hp
def solve_state(c,ker,g,psi0=None,seed=None,deep=False):
    n=c.n
    if psi0 is None: rng=np.random.default_rng(seed if seed is not None else 0); psi0=1.0+3.0*rng.standard_normal((n,n))
    nrm=lambda p:p/np.sqrt(np.mean(p**2)); psi=nrm(psi0.copy())
    def fg(x):
        phi=x.reshape(n,n); sc=1.0/np.sqrt(np.mean(phi**2)); p=phi*sc
        e,mu,_,Hp=emr(c,ker,g,p); return e,(sc*(2.0/n**2)*(Hp-mu*p)).ravel()
    r=minimize(fg,psi.ravel(),jac=True,method="L-BFGS-B",options=dict(maxiter=4000,ftol=1e-16,gtol=1e-12))
    psi=nrm(r.x.reshape(n,n)); tgt=1e-12 if deep else 1e-6; iters=20000 if deep else 6000; dt=0.6
    for _ in range(iters):
        e,mu,res,Hp=emr(c,ker,g,psi)
        if res<=tgt: break
        pre=np.real(np.fft.ifft2(np.fft.fft2(Hp-mu*psi)/(c.G2/2.0+max(abs(mu),1.0)))); psi=nrm(psi-dt*pre)
    e,mu,res,_=emr(c,ker,g,psi); return psi,e,mu,res
def center(c,psi):
    i,j=np.unravel_index(np.argmax(psi**2),psi.shape); pG=np.fft.fft2(psi)/c.n**2
    ph=np.exp(2j*np.pi*(c.M1*(i/c.n)+c.M2*(j/c.n))); out=np.real(np.fft.ifft2(pG*ph*c.n**2))
    return -out if out.flat[0]<0 else out
MIR_K=lambda m1,m2:(m1,m1-m2); MIR_M=lambda m1,m2:(m1-m2,-m2)
def mperm(c,mir):
    n=c.n; iden=(np.mod(c.M1,n)*n+np.mod(c.M2,n)).ravel().astype(int); p1,p2=mir(c.M1,c.M2)
    return (np.mod(p1,n)*n+np.mod(p2,n)).ravel().astype(int),iden
def amir(v,perm,iden): o=np.empty_like(v); o[perm]=v[iden]; return o
def cert_state(c,ker,g,psi,e,e_unif):
    pc=center(c,psi); rho=pc**2; contrast=rho.max()/max(rho.min(),1e-14)
    pG=(np.fft.fft2(pc)/c.n**2).ravel(); mres=[]
    for mir in (MIR_K,MIR_M):
        perm,iden=mperm(c,mir); mres.append(float(np.max(np.abs(pG-amir(pG,perm,iden)))/np.max(np.abs(pG))))
    return dict(crystal=bool(e<e_unif-1e-9*abs(e_unif) and contrast>5.0),contrast=float(contrast),mirror_res=mres,psi=pc)
def astar_solve(ker,g,n,lo,hi,seed=0):
    memo={}
    def eoa(a):
        a=float(a)
        if a not in memo: cc=Cell(a,n); psi,e,mu,res=solve_state(cc,ker,g,seed=seed); memo[a]=(cc,e,mu,res,psi)
        return memo[a][1]
    r=minimize_scalar(eoa,bounds=(lo,hi),method="bounded",options=dict(xatol=2e-4))
    cc,e,mu,res,psi=memo[float(r.x)]; return float(r.x),cc,psi,e,mu,res

def _LX(c,ker,g,psi,mu,q):
    n=c.n; N=n*n; Gx=c.Gx.ravel()+q[0]; Gy=c.Gy.ravel()+q[1]; kin=(Gx**2+Gy**2)/2.0
    Vh=(np.fft.fft2(meanfield(c,ker,g,psi**2)-mu)/N).ravel(); ph=(np.fft.fft2(psi)/N).ravel()
    m1=np.mod(c.M1,n).ravel(); m2=np.mod(c.M2,n).ravel()
    W=(np.mod(m1[:,None]-m1[None,:],n)*n+np.mod(m2[:,None]-m2[None,:],n))
    L=np.diag(kin)+Vh[W]; Dk=ker.Uh(np.sqrt(Gx**2+Gy**2)); Am=ph[W]; X=g*(Am.conj().T@(Dk[:,None]*Am))
    return 0.5*(L+L.conj().T),0.5*(X+X.conj().T)
def bdg(c,ker,g,psi,mu,q,nev=6):
    L,X=_LX(c,ker,g,psi,mu,q); lam,Uu=eigh(L); assert lam.min()>-1e-7
    S=(Uu*np.sqrt(np.clip(lam,0,None)))@Uu.conj().T; Mm=0.5*((S@(L+2*X)@S)+(S@(L+2*X)@S).conj().T)
    w2,V=eigh(Mm,subset_by_index=[0,nev-1]); Si=(Uu*(1/np.sqrt(np.clip(lam,1e-12,None))))@Uu.conj().T
    return w2,Si@V
def speeds(c,ker,g,psi,mu,direction,dq,jmax=6):
    if direction=="K": u=np.array([1.0,0.0]); mir=MIR_K
    else: u=c.b1/np.linalg.norm(c.b1); mir=MIR_M
    perm,iden=mperm(c,mir); qs=[];wT=[];wL=[];fT=[]
    for j in range(1,jmax+1):
        w2,V=bdg(c,ker,g,psi,mu,u*(j*dq),nev=6); assert (w2>-0.05).all(), f"F-NEG {w2.min():.2g}"
        w=np.sqrt(np.clip(w2,0,None)); pars=np.array([float(np.real(np.vdot(V[:,k]/np.linalg.norm(V[:,k]),amir(V[:,k]/np.linalg.norm(V[:,k]),perm,iden)))) for k in range(V.shape[1])])
        idx=np.argsort(w)[:4]; odd=[i for i in idx if pars[i]<-0.5]; even=[i for i in idx if pars[i]>0.5]
        assert len(odd)>=1 and len(even)>=2, f"F-CLS parities {np.round(pars[idx],3)}"
        iT=odd[int(np.argmin(w[odd]))]; ev=sorted(even,key=lambda i:w[i])[:2]
        qs.append(j*dq); wT.append(w[iT]); wL.append(w[ev[1]]); fT.append(abs(pars[iT]))
    qs=np.array(qs); wT=np.array(wT); wL=np.array(wL)
    zi=lambda w: float(np.sum(qs[1:6]*w[1:6])/np.sum(qs[1:6]**2))
    ex=lambda w,i0,i1: float(np.polyfit(np.log(qs[i0:i1+1]),np.log(w[i0:i1+1]),1)[0])
    return dict(cT=zi(wT),cL1=zi(wL),fT=float(min(fT)),pT=[ex(wT,1,3),ex(wT,3,5)],pL1=[ex(wL,1,3),ex(wL,3,5)])
def ward(c,ker,g,psi,mu):
    L,X=_LX(c,ker,g,psi,mu,np.zeros(2)); ph=(np.fft.fft2(psi)/c.n**2).ravel(); o=[]
    for Gc in (c.Gx.ravel(),c.Gy.ravel()):
        v=1j*Gc*ph
        if np.linalg.norm(v)<1e-14: continue
        o.append(float(np.linalg.norm((L+2*X)@v)/(np.linalg.norm(v)*max(abs(mu),1e-12))))
    return max(o)
def certify(name,g,n=32,seed=0,a_hint=None):
    ker=Kernel(name); e_unif=0.5*g*float(np.atleast_1d(ker.Uh(0.0))[0])
    lo,hi=(a_hint*0.75,a_hint*1.35) if a_hint else (0.8,2.3)
    astar,c,psi,e,mu,res=astar_solve(ker,g,n,lo,hi,seed=seed); cs=cert_state(c,ker,g,psi,e,e_unif)
    if not cs["crystal"]: return dict(kernel=name,g=g,crystal=False,e=e,e_unif=e_unif,contrast=cs["contrast"])
    psi=cs["psi"]; wd=ward(c,ker,g,psi,mu); dq=0.02*2*np.pi/astar
    dK=speeds(c,ker,g,psi,mu,"K",dq); dM=speeds(c,ker,g,psi,mu,"M",dq)
    cT=0.5*(dK["cT"]+dM["cT"]); cL1=0.5*(dK["cL1"]+dM["cL1"])
    return dict(kernel=name,g=g,crystal=True,astar=astar,mu=mu,e=e,res=res,contrast=cs["contrast"],ward=wd,
                cT=cT,cL1=cL1,RT=cT/cL1,fT=min(dK["fT"],dM["fT"]),iso_T=abs(dK["cT"]-dM["cT"])/cT,iso_L=abs(dK["cL1"]-dM["cL1"])/cL1,
                pT=dK["pT"]+dM["pT"],pL1=dK["pL1"]+dM["pL1"])
def gates(c):
    ok=True; notes=[]
    if c["ward"]>5e-3: ok=False; notes.append(f"F9 {c['ward']:.1e}")
    if not all(0.95<=p<=1.05 for p in c["pT"]): ok=False; notes.append(f"F-LIN T {np.round(c['pT'],3)}")
    if not all(0.95<=p<=1.05 for p in c["pL1"]): ok=False; notes.append(f"F-LIN L1 {np.round(c['pL1'],3)}")
    if c["iso_T"]>0.02 or c["iso_L"]>0.02: ok=False; notes.append(f"F-ISO {c['iso_T']:.2%}/{c['iso_L']:.2%}")
    if c["fT"]<0.95: ok=False; notes.append(f"F-CLS {c['fT']:.3f}")
    return ok,notes

GC=dict(gem3=71.87,gem4=39.19,gem8=22.02,cap_p2=451.24,gamma8=22.75,step=14.74)
AH=dict(gem3=1.46,gem4=1.42,gem8=1.38,cap_p2=0.96,gamma8=1.55,step=1.45)
def first_passing(name):
    g=5.0*np.ceil(GC[name]/5.0); hist={}
    run=lambda gv: hist.setdefault(gv,certify(name,float(gv),a_hint=AH[name]))
    c=run(g)
    while not c.get("crystal"): g+=5.0; c=run(g)
    while g-5.0>0:
        c2=run(g-5.0)
        if c2.get("crystal"): g-=5.0; c=c2
        else: break
    assert not run(g-5.0).get("crystal"), f"deep-fail bracket violated {g-5}"
    return float(g),c

def controls():
    ker=Kernel("step"); g=8.0; a=1.45; n=32; c=Cell(a,n); psi=np.ones((n,n)); mu=g*float(np.atleast_1d(ker.Uh(0.0))[0])
    errs=[]; odd_gl=0
    for dirn,mir in (("K",MIR_K),("M",MIR_M)):
        u=np.array([1.0,0.0]) if dirn=="K" else c.b1/np.linalg.norm(c.b1); perm,iden=mperm(c,mir)
        for j in (1,3,5):
            q=u*(j*0.05*2*np.pi/a); w2,V=bdg(c,ker,g,psi,mu,q,nev=4); kq=float(np.linalg.norm(q)); ek=kq*kq/2
            ana=np.sqrt(max(ek*(ek+2*g*float(np.atleast_1d(ker.Uh(kq))[0])),0.0)); errs.append(abs(np.sqrt(max(w2[0],0))-ana)/max(ana,1e-12))
            for k in range(4):
                s=V[:,k]/np.linalg.norm(V[:,k]); par=float(np.real(np.vdot(s,amir(s,perm,iden))))
                if par<-0.5 and w2[k]<0.05*ek: odd_gl+=1
    cneg=bool(max(errs)<1e-6 and odd_gl==0)
    nb=[np.array([np.cos(t),np.sin(t)]) for t in np.arange(6)*np.pi/3]; ratios=[]
    for th in (0.0,np.pi/6):
        u=np.array([np.cos(th),np.sin(th)]); Ac=np.zeros((2,2))
        for dv in nb: Ac+=0.5*np.dot(u,dv)**2*np.outer(dv,dv)
        c2s,Vv=np.linalg.eigh(Ac); pol=[abs(np.dot(Vv[:,i],u)) for i in range(2)]; iL=int(np.argmax(pol))
        ratios.append(float(np.sqrt(c2s[iL]/c2s[1-iL])))
    cpos=bool(all(abs(r-SQ3)<1e-9 for r in ratios))
    print(f"[controls] C-NEG maxerr={max(errs):.1e} odd_gapless={odd_gl} -> {'PASS' if cneg else 'FAIL'}; C-POS cL/cT={ratios} -> {'PASS' if cpos else 'FAIL'}")
    json.dump(dict(cneg=cneg,cpos=cpos,cneg_maxerr=float(max(errs)),cpos_ratios=ratios),open(f"{OUT}/cc_p0.json","w"))

if __name__=="__main__":
    t1(); ph=sys.argv[1]
    if ph=="controls": controls()
    elif ph=="anchor":
        name,g=sys.argv[2],float(sys.argv[3]); c=certify(name,g,a_hint=AH.get(name,1.46))
        print(f"[anchor {name}@{g:.0f}] a*={c['astar']:.5f} mu={c['mu']:.4f} cT={c['cT']:.4f} cL1={c['cL1']:.4f} RT={c['RT']:.5f} fT={c['fT']:.3f} ward={c['ward']:.1e}")
        json.dump({k:(float(v) if isinstance(v,(int,float,np.floating)) else v) for k,v in c.items()},open(f"{OUT}/cc_anchor_{name}_{int(g)}.json","w"),indent=1)
    elif ph=="point":
        name=sys.argv[2]; gstar,c=first_passing(name)
        c40=certify(name,gstar,n=40,a_hint=c["astar"]); conv=max(abs(c40["cT"]-c["cT"])/c["cT"],abs(c40["cL1"]-c["cL1"])/c["cL1"])
        ok,notes=gates(c);
        if conv>5e-6: ok=False; notes.append(f"F-CONV {conv:.1e}")
        status="CERTIFIED" if ok else "EXCLUDED"
        out=dict(kernel=name,gstar=gstar,status=status,notes=notes,astar=c["astar"],mu=c["mu"],cT=c["cT"],cL1=c["cL1"],RT=c["RT"],
                 fT=c["fT"],ward=c["ward"],res=c["res"],iso_T=c["iso_T"],iso_L=c["iso_L"],pT=c["pT"],pL1=c["pL1"],conv=float(conv),RT40=c40["RT"])
        json.dump({k:(float(v) if isinstance(v,np.floating) else v) for k,v in out.items()},open(f"{OUT}/cc_point_{name}.json","w"),indent=1)
        print(f"[point {name}] g*={gstar:.0f} {status} a*={c['astar']:.5f} mu={c['mu']:.3f} RT={c['RT']:.5f} cT={c['cT']:.4f} cL1={c['cL1']:.4f} conv={conv:.1e} notes={notes}")
