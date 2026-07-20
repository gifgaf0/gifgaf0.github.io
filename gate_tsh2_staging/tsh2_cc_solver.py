#!/usr/bin/env python3
"""G-TSH2 CC leg — PART 2: full-from-scratch E5(a) solver. Fresh code, NO gz1/tsh1 lineage
imported. Own lattice class, own imaginary-time+polish schedule, own truncation n=34 (chat 32;
convergence 40), own σ-parity classifier, own zero-intercept reducer. Executes the LOCKED
instrument (md5 99eb26a5, verified byte-identical): kernels K3/K4/K5/K6, CERT/first-passing,
F9/F-LIN/F-ISO/F-CONV/F-CLS, W-μ, C-NEG/C-POS. Substrate units ħ=m=ρ0=1. No physical-c/KC anywhere.
Usage: python3 tsh2_cc_solver.py tables|controls|K3|K4|K5|K6
"""
import numpy as np, json, sys, os
from scipy.special import j0, j1, jv
from scipy.linalg import eigh, inv
from scipy.interpolate import CubicSpline

OUT=os.path.dirname(os.path.abspath(__file__)); NPRIM=34; NCONV=40
def t1_grep():   # locked §10 — assembled from fragments so the guard cannot self-trip
    pats=["299"+"792458","2.9"+"979","GW"+"170817","1.6"+"180","0.6"+"180","137"+".03"]
    s=open(os.path.abspath(__file__),errors='ignore').read()
    hit=[p for p in pats if p in s.replace('pats=[','')]
    assert not hit, f"T1 SELF-GREP TRIP: {hit}"
    print("T1 grep clean")

# ---------------- kernels (own Hankel tables for γ-family; analytic cap) ----------------
def uhat_step(k):
    k=np.asarray(k,float); s=np.where(k<1e-9,1.0,k); return np.where(k<1e-9,np.pi,2*np.pi*j1(s)/s)
def uhat_cap(k):
    k=np.asarray(k,float); s=np.where(k<1e-9,1.0,k); return np.where(k<1e-9,np.pi/2,4*np.pi*jv(2,s)/s**2)
_gt={}
def uhat_gamma(gam):
    if gam in _gt: return _gt[gam]
    d=np.load(f'{OUT}/cc_uhat_gam{gam}.npz'); cs=CubicSpline(d['k'],d['u']); kmax=float(d['k'][-1])
    def fn(k):
        k=np.asarray(k,float); o=np.zeros_like(k); m=k<=kmax; o[m]=cs(k[m]); return o
    _gt[gam]=fn; return fn
KDEF={'K3':dict(gam=4,grid=list(range(85,150,5)),apred=1.472,fam='gamma'),
      'K4':dict(gam=8,grid=list(range(25,90,5)),apred=1.490,fam='gamma'),
      'K5':dict(gam=12,grid=list(range(20,85,5)),apred=1.460,fam='gamma'),
      'K6':dict(gam=None,grid=list(range(110,175,5)),apred=1.137,fam='cap')}
def kernel_fn(K): return uhat_cap if KDEF[K]['fam']=='cap' else uhat_gamma(KDEF[K]['gam'])

def build_tables():   # own grid/rmax/dr (independent of chat's)
    for gam in (4,8,12):
        ks=np.arange(0.0,100.0001,0.02); out=np.empty_like(ks)
        def tr(kv,rmax,dr):
            r=np.arange(dr,rmax,dr); w=r/(1.0+r**gam)
            return np.array([2*np.pi*np.trapezoid(w*j0(k*r),r) for k in kv])
        lo=ks<=2.0
        out[lo]=tr(ks[lo],500.0 if gam==4 else 150.0,0.0015)   # my rmax/dr
        out[~lo]=tr(ks[~lo],90.0,0.0015)
        out[0]=2*np.pi*(np.pi/gam)/np.sin(2*np.pi/gam)
        np.savez(f'{OUT}/cc_uhat_gam{gam}.npz',k=ks,u=out)
        print(f"table gam={gam}: U0={out[0]:.6f} min={out.min():.6f}@k={ks[out.argmin()]:.2f}")

# ---------------- lattice (own class) ----------------
class Lattice:
    def __init__(s,a,n,uf,g):
        s.a=a; s.n=n; s.g=g; s.uf=uf
        s.a1=np.array([a,0.0]); s.a2=np.array([a/2,np.sqrt(3)/2*a])
        s.A=abs(s.a1[0]*s.a2[1]-s.a1[1]*s.a2[0])
        B=2*np.pi*np.linalg.inv(np.array([s.a1,s.a2])).T; s.b1,s.b2=B[0],B[1]
        m=np.fft.fftfreq(n,1.0/n); s.M1,s.M2=np.meshgrid(m,m,indexing='ij')
        s.Gx=s.M1*s.b1[0]+s.M2*s.b2[0]; s.Gy=s.M1*s.b1[1]+s.M2*s.b2[1]; s.G2=s.Gx**2+s.Gy**2
        s.Ug=g*uf(np.sqrt(s.G2))
        u=np.arange(n)/n; S1,S2=np.meshgrid(u,u,indexing='ij')
        s.X=S1*s.a1[0]+S2*s.a2[0]; s.Y=S1*s.a1[1]+S2*s.a2[1]
    def phi(s,rho): return np.fft.ifft2(s.Ug*np.fft.fft2(rho)).real
    def Hpsi(s,psi): return np.fft.ifft2(0.5*s.G2*np.fft.fft2(psi))+s.phi(np.abs(psi)**2)*psi
    def Eden(s,psi):
        c=np.fft.fft2(psi)/s.n**2; ek=0.5*np.sum(s.G2*np.abs(c)**2)*s.A
        rho=np.abs(psi)**2; ei=0.5*np.mean(s.phi(rho)*rho)*s.A
        return float((ek+ei).real)/s.A

def seed(L,rng):
    n=L.n; w=0.30*np.linalg.norm(L.a1); d2=None
    for p in(-1,0,1):
        for q in(-1,0,1):
            dx=L.X-(p*L.a1[0]+q*L.a2[0]); dy=L.Y-(p*L.a1[1]+q*L.a2[1])
            dd=dx*dx+dy*dy; d2=dd if d2 is None else np.minimum(d2,dd)
    ps=np.exp(-d2/(2*w*w)).astype(complex)
    ps+=0.10*np.abs(ps).max()*(rng.standard_normal((n,n))+1j*rng.standard_normal((n,n)))
    return ps/np.sqrt(np.mean(np.abs(ps)**2))
def itime(L,psi,steps,dt=2e-3):
    kf=np.exp(-dt*0.5*L.G2)
    for _ in range(steps):
        psi=np.fft.ifft2(kf*np.fft.fft2(psi)); psi=psi*np.exp(-dt*L.phi(np.abs(psi)**2))
        psi/=np.sqrt(np.mean(np.abs(psi)**2))
    return psi
def recenter(L,psi):
    rho=np.abs(psi)**2; n=L.n; w=np.exp(-2j*np.pi*np.arange(n)/n)
    s1=(-np.angle(np.sum(rho*w[:,None])))/(2*np.pi); s2=(-np.angle(np.sum(rho*w[None,:])))/(2*np.pi)
    return np.fft.ifft2(np.exp(2j*np.pi*(L.M1*s1+L.M2*s2))*np.fft.fft2(psi))
def polish(L,psi,iters):   # own preconditioned steepest descent w/ backtracking
    psi=np.real(psi).copy(); psi/=np.sqrt(np.mean(psi**2)); E=L.Eden(psi); tau=0.5
    for _ in range(iters):
        Hp=np.real(L.Hpsi(psi)); mu=np.mean(psi*Hp)/np.mean(psi**2); r=Hp-mu*psi
        if np.sqrt(np.mean(r**2))<1e-10*max(abs(mu),1.0): break
        pre=1.0/(0.5*L.G2+1.0+0.02*abs(mu)); d=np.fft.ifft2(pre*np.fft.fft2(r)).real
        p2=psi-tau*d; p2/=np.sqrt(np.mean(p2**2)); E2=L.Eden(p2)
        if E2<=E+1e-14*abs(E): psi,E=p2,E2; tau=min(tau*1.15,1.0)
        else:
            tau*=0.5
            if tau<1e-4: break
    Hp=np.real(L.Hpsi(psi)); mu=float(np.mean(psi*Hp)/np.mean(psi**2))
    rn=float(np.sqrt(np.mean((Hp-mu*psi)**2))); return psi,mu,rn
def ground(L,steps,pol,rng):
    ps=itime(L,seed(L,rng),steps); ps=recenter(L,ps); ps,mu,rn=polish(L,ps,pol)
    ps=np.real(recenter(L,ps)); ps,mu,rn=polish(L,ps,80); return ps,mu,rn

# ---------------- a*-scan + CERT (locked §3/§4) ----------------
def vertex(p):
    (x1,y1),(x2,y2),(x3,y3)=p; d=(x1-x2)*(x1-x3)*(x2-x3)
    if abs(d)<1e-14: return None
    A=(x3*(y2-y1)+x2*(y1-y3)+x1*(y3-y2))/d; B=(x3*x3*(y1-y2)+x2*x2*(y3-y1)+x1*x1*(y2-y3))/d
    return None if A<=0 else -B/(2*A)
def scanE(uf,g,apred,n,tier):
    steps,pol=(4000,80) if tier==1 else (20000,400)
    sol={}
    for a in np.linspace(0.88,1.12,13)*apred:
        L=Lattice(a,n,uf,g); ps,mu,rn=ground(L,steps,pol,np.random.default_rng(7))
        sol[a]=(L.Eden(ps),ps,mu,rn)
    for _ in range(2):
        xs=sorted(sol); Es=[sol[a][0] for a in xs]; i=int(np.argmin(Es))
        if 0<i<len(xs)-1:
            av=vertex([(xs[i-1],Es[i-1]),(xs[i],Es[i]),(xs[i+1],Es[i+1])])
            if av and xs[0]<av<xs[-1] and min(abs(av-x) for x in xs)>1e-5:
                L=Lattice(av,n,uf,g); ps,mu,rn=ground(L,steps,pol,np.random.default_rng(7)); sol[av]=(L.Eden(ps),ps,mu,rn)
    xs=sorted(sol); Es=[sol[a][0] for a in xs]; i=int(np.argmin(Es))
    return dict(astar=xs[i],E=Es[i],psi=sol[xs[i]][1],mu=sol[xs[i]][2],rn=sol[xs[i]][3],interior=(0<i<len(xs)-1))
def cert(uf,g,apred,n,tier):
    r=scanE(uf,g,apred,n,tier); Eu=0.5*g*float(uf(np.array([0.0]))[0])
    rho=np.abs(r['psi'])**2; contrast=float((rho.max()-rho.min())/rho.mean())
    r.update(Eu=Eu,contrast=contrast,ok=bool((r['E']<=Eu-1e-5*abs(Eu)) and contrast>=0.5 and r['interior'])); return r

# ---------------- BdG (own dense build; locked pencil form) ----------------
def dense_ops(L,psi,mu,kv):
    n=L.n; N=n*n
    G2k=(L.Gx+kv[0])**2+(L.Gy+kv[1])**2; Ugk=L.g*L.uf(np.sqrt(G2k)); Phi=L.phi(psi**2)
    F=np.fft.ifft2(np.eye(N,dtype=complex).reshape(N,n,n),axes=(1,2))*N
    Vm=(np.fft.fft2(Phi[None]*F,axes=(1,2)).reshape(N,N)/N).T
    W=np.fft.ifft2(Ugk[None]*np.fft.fft2(psi[None]*F,axes=(1,2)),axes=(1,2))
    Xm=(np.fft.fft2(psi[None]*W,axes=(1,2)).reshape(N,N)/N).T
    Lm=np.diag(0.5*G2k.ravel()-mu)+Vm
    return 0.5*(Lm+Lm.conj().T),0.5*(Xm+Xm.conj().T)
def bdg(L,psi,mu,kv,nm=6):
    Lm,Xm=dense_ops(L,psi,mu,kv); Li=inv(Lm); Li=0.5*(Li+Li.conj().T)
    w2,V=eigh(Lm+2*Xm,Li); return w2[:nm],V[:,:nm]
def parity_maps(n):
    i=np.arange(n); I,J=np.meshgrid(i,i,indexing='ij')
    return ((-I-J)%n,J),((-I)%n,(I+J)%n)     # σ_M (fixes ΓM=ŷ), σ_K
def fodd(fld,sm):
    return float(np.sum(np.abs(0.5*(fld-fld[sm]))**2)/np.sum(np.abs(fld)**2))
def classify(L,psi,w2,V,sm):
    oms=np.sqrt(np.clip(w2,0,None)); flds=[np.fft.ifft2(V[:,j].reshape(L.n,L.n))*L.n*L.n for j in range(V.shape[1])]
    fo=[fodd(f,sm) for f in flds]; ti=[j for j in range(len(oms)) if fo[j]>=0.95]; ei=[j for j in range(len(oms)) if fo[j]<=0.05]
    T=ti[0] if ti else None; E2=sorted(ei,key=lambda j:oms[j])[:2]; return oms,fo,T,E2
def speeds(L,psi,mu,kh,kmag,sm,tag):
    ks=[(j/40.0)*kmag for j in range(1,9)]; omT=[]; omL=[]; om2=[]; fT=[]; neg=False
    for kv in ks:
        w2,V=bdg(L,psi,mu,(kh[0]*kv,kh[1]*kv))
        if w2[0]<-1e-8*mu*mu: neg=True
        oms,fo,T,E2=classify(L,psi,w2,V,sm)
        if T is None or len(E2)<2: return None
        omT.append(oms[T]); fT.append(fo[T]); om2.append(oms[E2[0]]); omL.append(oms[E2[1]])
    ks=np.array(ks); omT=np.array(omT); omL=np.array(omL); om2=np.array(om2)
    zi=lambda o,sl: float(np.sum(o[sl]*ks[sl])/np.sum(ks[sl]**2))
    pe=lambda o,sl: float(np.polyfit(np.log(ks[sl]),np.log(o[sl]),1)[0])
    s26,W1,W2=slice(1,6),slice(1,5),slice(3,8)
    return dict(tag=tag,neg=neg,fT_min=float(min(fT)),cT=zi(omT,s26),cL1=zi(omL,s26),c2=zi(om2,s26),
                pT=(pe(omT,W1),pe(omT,W2)),pL1=(pe(omL,W1),pe(omL,W2)),
                omT=list(map(float,omT)),omL1=list(map(float,omL)),om2=list(map(float,om2)),ks=list(map(float,ks)))
def convproxy(L,psi,mu,kh,kmag,sm):
    kk=[]; oT=[]; oL=[]
    for j in(3,5):
        kv=(j/40.0)*kmag; w2,V=bdg(L,psi,mu,(kh[0]*kv,kh[1]*kv)); oms,fo,T,E2=classify(L,psi,w2,V,sm)
        if T is None or len(E2)<2: return None
        kk.append(kv); oT.append(oms[T]); oL.append(oms[E2[1]])
    kk=np.array(kk); oT=np.array(oT); oL=np.array(oL)
    return float(np.sum(oT*kk)/np.sum(kk**2)),float(np.sum(oL*kk)/np.sum(kk**2))
def ward(L,psi,mu):
    out=[]
    for Gc in(L.Gx,L.Gy):
        d=np.fft.ifft2(1j*Gc*np.fft.fft2(psi))
        r=(np.fft.ifft2(0.5*L.G2*np.fft.fft2(d))+L.phi(psi**2)*d-mu*d)+2*(psi*np.fft.ifft2(L.Ug*np.fft.fft2(psi*d)))
        out.append(float(np.sqrt(np.mean(np.abs(r)**2))/(np.sqrt(np.mean(np.abs(d)**2))*abs(mu))))
    return out

# ---------------- per-kernel P1+P2 driver ----------------
def run_kernel(K):
    kd=KDEF[K]; uf=kernel_fn(K); grid=list(kd['grid']); dev=[]
    # P1: ascending scan + downward first-passing extension (locked §3)
    gstar=None
    for g in grid:
        r=cert(uf,g,kd['apred'],NPRIM,1); print(f"{K} t1 g={g}: a*={r['astar']:.4f} E/A={r['E']:.4f} Eu={r['Eu']:.4f} contr={r['contrast']:.3f} int={r['interior']} ok={r['ok']}",flush=True)
        if r['ok']: gstar=g; break
    if gstar is None:
        json.dump(dict(K=K,flag='FP-NONEXIST(p6m)'),open(f'{OUT}/cc_{K}.json','w'),indent=1); print(K,'FP-NONEXIST'); return
    while gstar==min(grid) and gstar-5>=5:
        gdn=gstar-5; r=cert(uf,gdn,kd['apred'],NPRIM,1); grid.insert(0,gdn); dev.append(f"grid extended down to {gdn}")
        print(f"{K} t1 g={gdn}: ok={r['ok']} (down-ext)",flush=True)
        if r['ok']: gstar=gdn
        else: break
    # tier-2 at g*, then g*-5 must fail deep
    r2=cert(uf,gstar,kd['apred'],NPRIM,2); print(f"{K} t2 g={gstar}: a*={r2['astar']:.5f} mu={r2['mu']:.4f} rn={r2['rn']:.2e} ok={r2['ok']}",flush=True)
    if not r2['ok']: dev.append(f"t2 fail g={gstar} advanced"); gstar+=5; r2=cert(uf,gstar,kd['apred'],NPRIM,2)
    for t in range(3):
        L=Lattice(r2['astar'],NPRIM,uf,gstar); ps,mu,rn=ground(L,20000,400,np.random.default_rng(1000+t))
        rel=abs(L.Eden(ps)-r2['E'])/abs(r2['E'])
        if rel>1e-5: dev.append(f"rerun{t} rel {rel:.1e}")
    if gstar-5>=5:
        r3=cert(uf,gstar-5,kd['apred'],NPRIM,2); print(f"{K} t2 g={gstar-5}: ok={r3['ok']} (must be False)",flush=True)
        if r3['ok']: dev.append(f"g*-5={gstar-5} certified deep")
    # P2: BdG on the certified g* state
    a=r2['astar']; L=Lattice(a,NPRIM,uf,gstar); psi,mu,rn=ground(L,20000,400,np.random.default_rng(7))
    psi=np.real(recenter(L,psi)); psi,mu,rn=polish(L,psi,300)
    sM,sK=parity_maps(NPRIM); wx,wy=ward(L,psi,mu)
    sres=float(np.sqrt(np.mean((psi-psi[sM])**2))/np.sqrt(np.mean(psi**2)))
    print(f"{K}: mu={mu:.4f} rn={rn:.2e} sres={sres:.2e} ward=({wx:.2e},{wy:.2e})",flush=True)
    flags=[]
    if max(wx,wy)>5e-3:
        flags.append('F9-FIRE'); json.dump(dict(K=K,flags=flags,excluded=True,deviations=dev),open(f'{OUT}/cc_{K}.json','w'),indent=1); print(K,'F9 FIRE'); return
    kGM=2*np.pi/(np.sqrt(3)*a); kGK=4*np.pi/(3*a)
    rM=speeds(L,psi,mu,(0.0,1.0),kGM,sM,'GM'); rK=speeds(L,psi,mu,(0.5,np.sqrt(3)/2),kGK,sK,'GK')
    if rM is None or rK is None:
        flags.append('F-CLS'); json.dump(dict(K=K,flags=flags,excluded=True,deviations=dev),open(f'{OUT}/cc_{K}.json','w'),indent=1); print(K,'F-CLS'); return
    if rM['neg'] or rK['neg']: flags.append('F-NEG')
    for r in (rM,rK):
        for p in list(r['pT'])+list(r['pL1']):
            if not(0.90<=p<=1.10): flags.append('F-LIN')
    isoT=abs(rM['cT']-rK['cT'])/(0.5*(rM['cT']+rK['cT']))*100; isoL=abs(rM['cL1']-rK['cL1'])/(0.5*(rM['cL1']+rK['cL1']))*100
    if isoT>2.0 or isoL>2.0: flags.append('F-ISO')
    # F-CONV n=40
    L40=Lattice(a,NCONV,uf,gstar); ps40,mu40,_=ground(L40,12000,400,np.random.default_rng(7)); ps40=np.real(recenter(L40,ps40)); ps40,mu40,_=polish(L40,ps40,200)
    sM40,sK40=parity_maps(NCONV)
    a32M=convproxy(L,psi,mu,(0.0,1.0),kGM,sM); a32K=convproxy(L,psi,mu,(0.5,np.sqrt(3)/2),kGK,sK)
    a40M=convproxy(L40,ps40,mu40,(0.0,1.0),2*np.pi/(np.sqrt(3)*a),sM40); a40K=convproxy(L40,ps40,mu40,(0.5,np.sqrt(3)/2),4*np.pi/(3*a),sK40)
    convT=max(abs(a32M[0]-a40M[0])/a32M[0],abs(a32K[0]-a40K[0])/a32K[0]); convL=max(abs(a32M[1]-a40M[1])/a32M[1],abs(a32K[1]-a40K[1])/a32K[1])
    if convT>1e-3 or convL>1e-3: flags.append('F-CONV')
    # W-μ static witness (§8)
    LE=Lattice(a,NPRIM,uf,gstar); psE,muE,_=ground(LE,20000,400,np.random.default_rng(7)); E0=LE.Eden(psE)*LE.A; mus=[]
    for eps in (0.005,0.01):
        Ep=[]
        for sgn in(+1,-1):
            a2s=(a/2+sgn*eps*np.sqrt(3)/2*a,np.sqrt(3)/2*a)
            Ls=Lattice.__new__(Lattice); Ls.__init__.__wrapped__ if False else None
            Ls=_sheared(a,a2s,NPRIM,uf,gstar); pss,mss,_=ground(Ls,20000,400,np.random.default_rng(7)); Ep.append(Ls.Eden(pss)*Ls.A)
        mus.append((Ep[0]+Ep[1]-2*E0)/(LE.A*eps*eps))
    mu_s=float(np.mean(mus)); cT=0.5*(rM['cT']+rK['cT']); cL1=0.5*(rM['cL1']+rK['cL1']); RT=cT/cL1
    wmu=float(mu_s/(1.0*cT*cT))
    out=dict(K=K,gstar=int(gstar),astar=float(a),mu=float(mu),gp_residual=float(rn),sres=sres,ward_x=wx,ward_y=wy,
             cT_GM=rM['cT'],cT_GK=rK['cT'],cL1_GM=rM['cL1'],cL1_GK=rK['cL1'],c2_GM=rM['c2'],c2_GK=rK['c2'],
             p_T=[*rM['pT'],*rK['pT']],p_L1=[*rM['pL1'],*rK['pL1']],f_T_min=min(rM['fT_min'],rK['fT_min']),
             iso_T_pct=isoT,iso_L1_pct=isoL,conv_dcT=float(convT),conv_dcL1=float(convL),
             cT=cT,cL1=cL1,c2=0.5*(rM['c2']+rK['c2']),R_T=float(RT),mu_static=mu_s,wmu_ratio=wmu,
             flags=flags,deviations=dev,excluded=bool(any(f in flags for f in('F-LIN','F-ISO','F9-FIRE','F-CLS','F-NEG'))))
    json.dump(out,open(f'{OUT}/cc_{K}.json','w'),indent=1)
    print(f"{K} P2: g*={gstar} a*={a:.5f} mu={mu:.4f} cT={cT:.4f} cL1={cL1:.4f} R_T={RT:.5f} isoT={isoT:.2f}% conv=({convT:.1e},{convL:.1e}) wmu={wmu:.3f} flags={flags}",flush=True)

def _sheared(a,a2s,n,uf,g):
    L=Lattice(a,n,uf,g)   # rebuild with sheared a2
    L.a2=np.array(a2s,float); L.A=abs(L.a1[0]*L.a2[1]-L.a1[1]*L.a2[0])
    B=2*np.pi*np.linalg.inv(np.array([L.a1,L.a2])).T; L.b1,L.b2=B[0],B[1]
    L.Gx=L.M1*L.b1[0]+L.M2*L.b2[0]; L.Gy=L.M1*L.b1[1]+L.M2*L.b2[1]; L.G2=L.Gx**2+L.Gy**2; L.Ug=g*uf(np.sqrt(L.G2))
    u=np.arange(n)/n; S1,S2=np.meshgrid(u,u,indexing='ij'); L.X=S1*L.a1[0]+S2*L.a2[0]; L.Y=S1*L.a1[1]+S2*L.a2[1]
    return L

# ---------------- controls (locked §10) ----------------
def controls():
    uf=uhat_step; L=Lattice(1.4575,NPRIM,uf,8.0); psi=np.ones((NPRIM,NPRIM)); mu=8.0*float(uf(np.array([0.0]))[0])
    kGM=2*np.pi/(np.sqrt(3)*1.4575); sM,_=parity_maps(NPRIM); okan=True; gtot=None; godd=0
    for j in(1,2,3,4):
        kv=(j/40.0)*kGM; w2,V=bdg(L,psi,mu,(0.0,kv)); oms=np.sqrt(np.clip(w2,0,None))
        an=np.sqrt(0.5*kv*kv*(0.5*kv*kv+2*8.0*float(uf(np.array([kv]))[0]))); okan&= abs(oms[0]-an)/an<1e-6
        flds=[np.fft.ifft2(V[:,m].reshape(NPRIM,NPRIM))*NPRIM*NPRIM for m in range(6)]; gl=[m for m in range(6) if oms[m]<3.0*an]
        gtot=len(gl); godd+=sum(1 for m in gl if fodd(flds[m],sM)>0.5)
    cneg=bool(okan and gtot==1 and godd==0); print(f"C-NEG: analytic<1e-6={okan} gapless={gtot} odd={godd} -> {'PASS' if cneg else 'FAIL'}")
    dels=[np.array([np.cos(t),np.sin(t)]) for t in np.arange(6)*np.pi/3]
    Dk=lambda k: sum(2*np.sin(0.5*np.dot(k,d))**2*np.outer(d,d) for d in dels)
    res=[]
    for kh in(np.array([0.0,1.0]),np.array([0.5,np.sqrt(3)/2])):
        for km in(1e-3,5e-4):
            ev,evec=np.linalg.eigh(Dk(kh*km)); cs=np.sqrt(ev)/km; res.append((cs[1]/cs[0],abs(np.dot(evec[:,0],kh))))
    cpos=bool(max(abs(r/np.sqrt(3)-1) for r,_ in res)<1e-6 and max(p for _,p in res)<=0.05)
    print(f"C-POS: max|cL/cT/√3-1|={max(abs(r/np.sqrt(3)-1) for r,_ in res):.2e} -> {'PASS' if cpos else 'FAIL'}")
    json.dump(dict(cneg=cneg,cpos=cpos),open(f'{OUT}/cc_p0.json','w'),indent=1)

if __name__=='__main__':
    t1_grep(); ph=sys.argv[1]
    if ph=='tables': build_tables()
    elif ph=='controls': controls()
    else: run_kernel(ph)
