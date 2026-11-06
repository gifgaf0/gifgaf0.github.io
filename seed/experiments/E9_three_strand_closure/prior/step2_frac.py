import numpy as np, sys, json
from scipy.optimize import minimize
N=161; e=1/(4*np.sqrt(3)); g=1/e**2; rho=np.ones(3)
X,Y=np.meshgrid(np.arange(N)-N//2, np.arange(N)-N//2, indexing='ij'); X=X.astype(float); Y=Y.astype(float)
def wrap(a): return (a+np.pi)%(2*np.pi)-np.pi
def run(d,eta):
    # vortex centres at plaquette centres
    c0=(0.5,0.5); c1=(0.5+d,0.5)
    pos=[c1,c0,c0]
    th=[np.arctan2(Y-p[1],X-p[0]) for p in pos]
    Sx=[wrap(t[1:,:]-t[:-1,:]) for t in th]; Sy=[wrap(t[:,1:]-t[:,:-1]) for t in th]
    nx=(N-1)*N; ny=N*(N-1); nphi=N*N
    def unpack(v):
        ph=[v[k*nphi:(k+1)*nphi].reshape(N,N) for k in range(3)]
        ax=v[3*nphi:3*nphi+nx].reshape(N-1,N); ay=v[3*nphi+nx:].reshape(N,N-1)
        return ph,ax,ay
    def f(v):
        ph,ax,ay=unpack(v); E=0.; gph=[np.zeros((N,N)) for _ in range(3)]
        gax=np.zeros_like(ax); gay=np.zeros_like(ay)
        for k in range(3):
            Dx=Sx[k]+ph[k][1:,:]-ph[k][:-1,:]-e*ax
            Dy=Sy[k]+ph[k][:,1:]-ph[k][:,:-1]-e*ay
            E+=0.5*rho[k]*((Dx**2).sum()+(Dy**2).sum())
            gph[k][1:,:]+=rho[k]*Dx; gph[k][:-1,:]-=rho[k]*Dx
            gph[k][:,1:]+=rho[k]*Dy; gph[k][:,:-1]-=rho[k]*Dy
            gax-=e*rho[k]*Dx; gay-=e*rho[k]*Dy
        F=ax[:,:-1]+ay[1:,:]-ax[:,1:]-ay[:-1,:]
        E+=0.5*(F**2).sum()
        gax[:,:-1]+=F; gax[:,1:]-=F; gay[1:,:]+=F; gay[:-1,:]-=F
        if eta:
            T=[th[k]+ph[k] for k in range(3)]
            for i in range(3):
                for j in range(i+1,3):
                    D=T[i]-T[j]; E-=eta*np.cos(D).sum(); s=eta*np.sin(D)
                    gph[i]+=s; gph[j]-=s
        return E, np.concatenate([x.ravel() for x in gph+[gax,gay]])
    v0=np.zeros(3*nphi+nx+ny)
    r=minimize(f,v0,jac=True,method='L-BFGS-B',options={'maxiter':20000,'maxfun':40000,'gtol':1e-7,'ftol':1e-14})
    ph,ax,ay=unpack(r.x); F=ax[:,:-1]+ay[1:,:]-ax[:,1:]-ay[:-1,:]
    # flux (in units of the quantum 2pi/e; lattice F = e*h^2*B so Phi/Phi0 = sum F/(2pi))
    PX,PY=np.meshgrid(np.arange(N-1)-N//2+0.5, np.arange(N-1)-N//2+0.5, indexing='ij')
    def flux(cx,R): return float(F[(PX-cx)**2+(PY-0.5)**2<R**2].sum()*e/(2*np.pi))
    out=dict(d=d,eta=eta,E=float(r.fun),success=bool(r.success),gnorm=float(np.abs(r.jac).max()),
             flux_total=float(F.sum()*e/(2*np.pi)))
    if d>=24: out.update(flux_near_moved=flux(0.5+d,10),flux_near_origin=flux(0.5,10))
    return out
if __name__=='__main__':
    eta=float(sys.argv[1]); res=[]
    for d in [0,2,4,6,8,12,16,20,24,28,32]:
        o=run(d,eta); res.append(o); print(json.dumps(o),flush=True)
    json.dump(res,open(f'results_eta{eta}.json','w'),indent=1)
