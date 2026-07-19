"""G-TSH1 CC leg — PART 2d: mandatory C-NEG null control + independent axis-(ii) g6 point.
C-NEG: uniform superfluid (g=10, below crystallization) must yield ZERO transverse-classified
modes and exactly one gapless branch (pipeline does not hallucinate shear). g6: gamma-6 kernel
g=35, own tabulated Hankel transform, own BdG -> independent R_T for the axis-(ii) UNDERDETERMINED test.
"""
import numpy as np, time, json
from numpy.fft import fft2, ifft2
from scipy.special import j0, j1
from tsh1_cc_bdg import cellgeom, relax, bdg, branch, speed, astar, classify

# ---- independent gamma-6 kernel: U(q)=2π ∫ exp(-(r/R)^6) J0(qr) r dr, tabulated ----
_T={}
def Uq_g6(q,g,R=1.0):
    if R not in _T:
        r=np.linspace(0,4*R,4001); qs=np.linspace(0,80,8001); w=np.exp(-(r/R)**6)*r
        _T[R]=(qs,2*np.pi*np.array([np.trapezoid(w*j0(qq*r),r) for qq in qs]))
    qs,tab=_T[R]; return g*np.interp(np.abs(q),qs,tab)

def relax_uniform(a,g,Nc=120,rho0=1.0,schedule=((0.001,6000),(3e-4,6000))):
    ge=cellgeom(a,Nc); Uk=2*np.pi*g*0.5*np.ones_like(ge['G2'])  # soft-core; recompute properly below
    from scipy.special import j1 as _j1
    x=np.sqrt(ge['G2']); Uk=np.full_like(x,0.5); m=x>1e-9; Uk[m]=_j1(x[m])/x[m]; Uk=2*np.pi*g*Uk
    Ntot=rho0*ge['area']; psi=np.ones((Nc,Nc),complex); psi*=np.sqrt(Ntot/(np.sum(np.abs(psi)**2)*ge['area']/Nc**2))
    for dt,ns in schedule:
        Kin=np.exp(-0.5*dt*0.5*ge['G2'])
        for _ in range(ns):
            psi=ifft2(Kin*fft2(psi)); rho=np.abs(psi)**2; Phi=ifft2(Uk*fft2(rho)).real
            psi=psi*np.exp(-dt*Phi); psi=ifft2(Kin*fft2(psi))
            psi*=np.sqrt(Ntot/(np.sum(np.abs(psi)**2)*ge['area']/Nc**2))
    psi=np.abs(psi); rho=psi**2; Phi=ifft2(Uk*fft2(rho)).real
    c=fft2(psi)/Nc**2; rk=fft2(rho)/Nc**2
    Ekin=np.sum(0.5*ge['G2']*np.abs(c)**2)*ge['area']; Eint=0.5*np.sum(Uk*np.abs(rk)**2)*ge['area']
    return dict(psi=psi,ge=ge,Uk=Uk,Phi=Phi,mu=(Ekin+2*Eint)/Ntot,contrast=float(psi.max()/psi.min()))

t0=time.time(); res={}
# ===== C-NEG: uniform g=10 =====
stU=relax_uniform(1.4575,10.0)
unit=2*np.pi/1.4575
Tc=0; gl=[]
for kf in [0.05,0.10,0.15]:
    r=bdg(stU,10.0,kf*unit*np.array([1.0,0.0]),n=24)
    Tc+=sum(classify(m)=='T' for m in r['modes'])
g0=bdg(stU,10.0,0.002*unit*np.array([1.0,0.0]),n=24)['modes']
ngl=int(np.sum([m['om']<0.1*g0[5]['om'] for m in g0[:5]]))
cneg_pass=bool(Tc==0 and ngl==1 and stU['contrast']<1.02)
print(f"[C-NEG] contrast={stU['contrast']:.4f} T-classified={Tc} gapless={ngl} -> {'PASS' if cneg_pass else 'FAIL'}")
res['C_NEG']=dict(contrast=stU['contrast'],Tcount=Tc,n_gapless=ngl,PASS=cneg_pass)

# ===== axis-(ii): gamma-6 kernel g=35 =====
import tsh1_cc_bdg as B
_orig=B.Uq_soft
B.Uq_soft=lambda q,g,R=1.0: Uq_g6(q,g,R)     # swap kernel for the g6 run (own tabulated transform)
try:
    a6=astar(35.0,Nc=120,lo=1.38,hi=1.60,npts=9)
    st6=relax(a6,35.0,Nc=120,schedule=((0.001,8000),(3e-4,9000),(1e-4,15000),(3e-5,18000)))
    w6=bdg(st6,35.0,0.005*(2*np.pi/a6)*np.array([1.0,0.0]),n=28)
    f9=bool(st6['res']<=5e-3 and w6['w2min']>-0.05)
    br=branch(st6,35.0,[1.0,0.0],[0.05,0.075,0.10,0.125,0.15,0.175,0.20],n=28)
    cT,pT=speed(br['T']); cL,pL=speed(br['L']); RT=cT/cL
    print(f"[g6 g=35] a*={a6:.4f} mu={st6['mu']:.3f} F9={f9} c_T={cT:.4f} c_L1={cL:.4f} "
          f"R_T={RT:.5f} (chat 0.49885, {abs(RT-0.49885)/0.49885*100:.1f}%)")
    res['g6']=dict(a=a6,mu=st6['mu'],res=st6['res'],w2min=w6['w2min'],f9=f9,cT=cT,cL=cL,RT=RT,pT=pT,pL=pL)
finally:
    B.Uq_soft=_orig
# independent axis-(ii) pooled deviation (canonical + 3 soft + g6)
RTall=np.array([0.52317,0.52861,0.53477,0.54365,res['g6']['RT']])
Dii=float(np.max(np.abs(RTall-RTall.mean()))/RTall.mean())
print(f"[axis-ii] pooled R_T={[round(x,5) for x in RTall]}  D={Dii*100:.2f}% (chat 5.11%) -> "
      f"{'UNDERDETERMINED (3-10%)' if 0.03<Dii<0.10 else 'other'}")
res['axis_ii_D']=Dii
json.dump(res,open('/home/user/gifgaf0.github.io/gate_tsh1_staging/tsh1_cc_controls.json','w'),indent=1)
print(f"[controls] total {time.time()-t0:.0f}s")
