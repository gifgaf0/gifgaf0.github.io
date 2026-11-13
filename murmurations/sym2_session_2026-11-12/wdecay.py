import numpy as np
def bump(v):
    out=np.zeros_like(v); m=np.abs(v)<1; out[m]=np.exp(-1/(1-v[m]**2)); return out
for K in [150,1000,3000]:
    k=np.arange(4,8*K,2).astype(float)
    X=((K-1)/(2*np.pi))**2; Xk=((k-1)/(2*np.pi))**2
    w=bump(np.log2(Xk/X)); k=k[w>0]; w=w[w>0]
    al=np.linspace(0,np.pi/2,200001)[1:]
    # W(alpha)=sum w sin((k-1)alpha), chunked
    W=np.zeros_like(al)
    for i in range(0,len(al),5000):
        W[i:i+5000]=np.sin(np.outer(al[i:i+5000],k-1))@w
    Wm=np.abs(W).max()
    for tau in [1e-4,1e-5,1e-6,1e-7]:
        idx=np.where(np.abs(W)>tau*Wm)[0].max()
        a=al[idx]; mrel=a*a  # m/p ~ alpha^2 (small alpha)
        X5=5*X
        print(f"K={K} tau={tau:.0e}: alpha_cut*K={a*K:8.1f}  m_cut at p=5X: {X5*(1-np.cos(a))*2:9.0f}  (2p={2*X5:.0f})")
