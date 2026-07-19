"""G-TSH1 CC leg — PART 2: independent from-scratch GP ground state + BdG shear spectrum.

Independent implementation (own grid Nc=120, own dt schedule, own reciprocal truncation,
own polarization classifier, own slope fitter, own Ward/C-NEG controls). Physics operator is
the supersolid Bogoliubov ω²-problem ω² f = L(L+2X) f (Hermitianized) — the correct operator,
coded independently. Targets: C1 (crystallizes, μ, gapless structure), C3 (Q1=T-LINEAR),
C4 (c_T,c_L1,R_T at g=22). Substrate units ħ=m=1; no physical-unit statement anywhere.
"""
import numpy as np
from numpy.fft import fft2, ifft2
from scipy.special import j1

def Uq_soft(q, g, R=1.0):                       # soft-core kernel, U(0)=π g
    x = np.asarray(q,float)*R; out=np.full_like(x,0.5); m=x>1e-9
    out[m]=j1(x[m])/x[m]; return 2*np.pi*g*R*R*out

def cellgeom(a, Nc):
    a1=np.array([a,0.0]); a2=np.array([0.5*a, np.sqrt(3)/2*a])
    b1=(2*np.pi/a)*np.array([1.0,-1/np.sqrt(3)]); b2=(2*np.pi/a)*np.array([0.0,2/np.sqrt(3)])
    m=np.fft.fftfreq(Nc)*Nc; MM,NN=np.meshgrid(m,m,indexing='ij')
    Gx=MM*b1[0]+NN*b2[0]; Gy=MM*b1[1]+NN*b2[1]
    s=(np.arange(Nc)+0.5)/Nc; S1,S2=np.meshgrid(s,s,indexing='ij')
    X=S1*a1[0]+S2*a2[0]; Y=S1*a1[1]+S2*a2[1]
    return dict(a=a,a1=a1,a2=a2,b1=b1,b2=b2,Gx=Gx,Gy=Gy,G2=Gx**2+Gy**2,
                area=a*a*np.sqrt(3)/2,X=X,Y=Y,Nc=Nc)

def relax(a, g, Nc=120, rho0=1.0, schedule=((0.001,9000),(3e-4,9000),(1e-4,12000))):
    ge=cellgeom(a,Nc); Uk=Uq_soft(np.sqrt(ge['G2']),g); Ntot=rho0*ge['area']
    rc=0.5*(ge['a1']+ge['a2']); d2=(ge['X']-rc[0])**2+(ge['Y']-rc[1])**2
    psi=(np.exp(-d2/(2*0.35**2))+0.05+0j)
    psi*=np.sqrt(Ntot/(np.sum(np.abs(psi)**2)*ge['area']/Nc**2))
    for dt,ns in schedule:
        Kin=np.exp(-0.5*dt*0.5*ge['G2'])
        for _ in range(ns):
            psi=ifft2(Kin*fft2(psi)); rho=np.abs(psi)**2
            Phi=ifft2(Uk*fft2(rho)).real
            psi=psi*np.exp(-dt*Phi); psi=ifft2(Kin*fft2(psi))
            psi*=np.sqrt(Ntot/(np.sum(np.abs(psi)**2)*ge['area']/Nc**2))
    psi=np.abs(psi); rho=psi**2; Phi=ifft2(Uk*fft2(rho)).real
    c=fft2(psi)/Nc**2; rk=fft2(rho)/Nc**2
    Ekin=np.sum(0.5*ge['G2']*np.abs(c)**2)*ge['area']; Eint=0.5*np.sum(Uk*np.abs(rk)**2)*ge['area']
    mu=(Ekin+2*Eint)/Ntot
    lap=ifft2(-ge['G2']*fft2(psi)).real
    res=float(np.sqrt(np.mean((-0.5*lap+Phi*psi-mu*psi)**2))/np.sqrt(np.mean(psi**2)))
    return dict(psi=psi,ge=ge,Uk=Uk,Phi=Phi,mu=mu,E_area=(Ekin+Eint)/ge['area'],res=res)

def astar(g, Nc=120, lo=1.35, hi=1.58, npts=13):
    al=np.linspace(lo,hi,npts); Es=[relax(a,g,Nc,schedule=((0.001,6000),(3e-4,6000)))['E_area'] for a in al]
    Es=np.array(Es); i=int(np.clip(np.argmin(Es),1,npts-2))
    p=np.polyfit(al[i-1:i+2],Es[i-1:i+2],2); return float(-p[1]/(2*p[0]))

def bdg(st, g, qvec, n=28, nmodes=6):
    ge=st['ge']; Nc=ge['Nc']; psi0=st['psi']; mu=st['mu']
    ph=fft2(psi0)/Nc**2; Phih=fft2(st['Phi'])/Nc**2
    ml=np.arange(n)-n//2; Mi,Ni=np.meshgrid(ml,ml,indexing='ij'); mi=Mi.ravel(); ni=Ni.ravel(); P=n*n
    Gx=mi*ge['b1'][0]+ni*ge['b2'][0]; Gy=mi*ge['b1'][1]+ni*ge['b2'][1]
    dm=(mi[:,None]-mi[None,:])%Nc; dn=(ni[:,None]-ni[None,:])%Nc
    Mpsi=ph[dm,dn]; MPhi=Phih[dm,dn]
    kq2=(Gx+qvec[0])**2+(Gy+qvec[1])**2
    L=0.5*np.diag(kq2)+MPhi-mu*np.eye(P); L=0.5*(L+L.conj().T)
    ev,V=np.linalg.eigh(L); negf=-ev.min()/max(ev.max(),1e-12); ev=np.clip(ev,0,None)
    Lh=(V*np.sqrt(ev))@V.conj().T
    Ukq=Uq_soft(np.sqrt(kq2),g); Xq=Mpsi@(Ukq[:,None]*Mpsi)
    M=Lh@(L+2*Xq)@Lh; M=0.5*(M+M.conj().T)
    w2,W=np.linalg.eigh(M); om=np.sqrt(np.clip(w2,0,None))
    # polarization classifier (independent): project δρ onto rigid-translation gradients
    rho0=psi0**2; rG=fft2(rho0)/Nc**2
    dxr=ifft2(1j*ge['Gx']*rG).real*Nc**2; dyr=ifft2(1j*ge['Gy']*rG).real*Nc**2
    A=np.stack([dxr.ravel(),dyr.ravel()],1); AtA=A.T@A
    okA=np.linalg.norm(A)>1e-8                 # null for a uniform state (no crystal)
    qn=np.hypot(*qvec); qh=np.array(qvec)/qn; qp=np.array([-qh[1],qh[0]])
    modes=[]
    for j in range(nmodes):
        f=Lh@W[:,j]; grid=np.zeros((Nc,Nc),complex); grid[mi%Nc,ni%Nc]=f
        fr=ifft2(grid)*Nc**2; drho=psi0*fr; b=drho.ravel(); nb=np.vdot(b,b).real
        if okA and nb>1e-20:
            s=np.linalg.solve(AtA,A.T@b); pd=float(np.vdot(A@s,A@s).real/nb)
            pl=abs(s@qh)**2; pt=abs(s@qp)**2; fT=float(pt/(pl+pt)) if pl+pt>0 else 0.0
        else: pd,fT=0.0,0.0
        modes.append(dict(om=float(om[j]),P=pd,fT=fT))
    return dict(modes=modes,w2min=float(w2[0]),Lneg=float(negf))

def classify(m):
    if m['P']<0.5: return 'phase'
    if m['fT']>=0.8: return 'T'
    if m['fT']<=0.2: return 'L'
    return 'MIX'

def branch(st, g, qhat, kfs, n=28):
    a=st['ge']['a']; unit=2*np.pi/a; out={'T':[], 'L':[]}
    for kf in kfs:
        r=bdg(st,g,kf*unit*np.array(qhat),n=n)
        cls=[classify(m) for m in r['modes']]
        Ls=[(m,c) for m,c in zip(r['modes'],cls) if c=='L']
        Ts=[(m,c) for m,c in zip(r['modes'],cls) if c=='T']
        if Ts: out['T'].append((kf*unit, max(Ts,key=lambda t:t[0]['fT'])[0]['om']))
        if Ls: out['L'].append((kf*unit, max(Ls,key=lambda t:t[0]['P'])[0]['om']))  # upper L = first sound
    return out

def speed(pairs):
    k=np.array([p[0] for p in pairs]); o=np.array([p[1] for p in pairs])
    c=float(np.sum(k*o)/np.sum(k*k)); p=float(np.polyfit(np.log(k),np.log(o),1)[0]); return c,p

if __name__=='__main__':
    import sys, time, json
    g=22.0; t0=time.time()
    a_s=astar(g); print(f"[CC-BdG] a*={a_s:.4f} (chat 1.4575)  [{time.time()-t0:.0f}s]")
    st=relax(a_s,g); print(f"[CC-BdG] mu={st['mu']:.4f} (chat 55.85)  GP-res={st['res']:.2e}")
    # F9 Ward control: raw w2min at tiny q must be > -0.05
    unit=2*np.pi/a_s; w=bdg(st,g,0.005*unit*np.array([1.0,0.0]),n=28)
    print(f"[F9 Ward] w2min(kf=0.005)={w['w2min']:.4f} (>-0.05 req)  gapless oms={[round(m['om'],3) for m in w['modes'][:5]]}")
    kfs=[0.05,0.075,0.10,0.125,0.15,0.175,0.20]
    br=branch(st,g,[1.0,0.0],kfs,n=28)
    cT,pT=speed(br['T']); cL,pL=speed(br['L']); RT=cT/cL
    print(f"[CC-BdG] c_T={cT:.4f} (chat 5.7749, p={pT:.3f}) | c_L1={cL:.4f} (chat 11.0453, p={pL:.3f})")
    print(f"[CC-BdG] R_T={RT:.5f} (chat 0.52284)")
    print(f"  rel err: c_T {abs(cT-5.7749)/5.7749*100:.1f}%  c_L1 {abs(cL-11.0453)/11.0453*100:.1f}%  R_T {abs(RT-0.52284)/0.52284*100:.1f}%")
    json.dump(dict(a=a_s,mu=st['mu'],res=st['res'],w2min=w['w2min'],
                   cT=cT,cL=cL,RT=RT,pT=pT,pL=pL,
                   Tband=br['T'],Lband=br['L']),
              open('/home/user/gifgaf0.github.io/gate_tsh1_staging/tsh1_cc_bdg_g22.json','w'),indent=1)
    print(f"[CC-BdG] total {time.time()-t0:.0f}s")
