# -*- coding: utf-8 -*-
"""Índice hedónico del entero L1 restringido a 2023-2026. Misma especificación que
hedonico.py: WLS de log(precio) sobre dummies de mes y destino, pesos = kilos, HC1."""
import numpy as np, pandas as pd, statsmodels.api as sm
FOB_MIN, FOB_MAX, KG_MIN = 3.0, 15.0, 500.0
DEST_MIN_SHARE, DEST_MIN_N = 0.005, 50

d = pd.read_pickle('/tmp/expo2326.pkl')
d = d[(d.pres=="entero") & (d.cal=="L1") & (d.anio>=2023)].copy()
n0, kg0 = len(d), d.kg.sum()
print(f"Entero L1 · 2023-2026: {n0:,} filas / {kg0/1e6:,.1f} kt iniciales")
d = d[(d.kg>0)&(d.fob>0)]
d = d[d.fob.between(FOB_MIN,FOB_MAX)]
d = d[d.kg>=KG_MIN]
print(f"  tras depurar (fob 3-15, embarque >= 500 kg): {len(d):,} filas / {d.kg.sum()/1e6:,.1f} kt "
      f"({d.kg.sum()/kg0*100:.2f}% del volumen)")
d["per"]=pd.PeriodIndex(d.anio.astype(str)+"-"+d.mes.astype(str).str.zfill(2),freq="M")
pd_=d.groupby("destino").agg(kg=("kg","sum"),n=("kg","size"))
grandes=pd_[(pd_.kg/pd_.kg.sum()>=DEST_MIN_SHARE)&(pd_.n>=DEST_MIN_N)].index
d["dest_g"]=d.destino.where(d.destino.isin(grandes),"Otros")
print(f"  destinos con efecto fijo propio ({len(grandes)}): {', '.join(sorted(grandes))}")
print(f"  a 'Otros': {d.destino.nunique()-len(grandes)} destinos, "
      f"{d[d.dest_g=='Otros'].kg.sum()/d.kg.sum()*100:.1f}% de los kilos · meses: {d.per.nunique()}\n")

y=np.log(d.fob.to_numpy()); w=d.kg.to_numpy()
meses=pd.PeriodIndex(sorted(d.per.unique()),freq="M"); base_mes=meses[0]
base_dest=d.groupby("dest_g").kg.sum().idxmax()
X=pd.get_dummies(d.per.astype(str),prefix="m",dtype=float).drop(columns=[f"m_{base_mes}"])
D=pd.get_dummies(d.dest_g,prefix="d",dtype=float).drop(columns=[f"d_{base_dest}"])
X=pd.concat([X.reset_index(drop=True),D.reset_index(drop=True)],axis=1)
X=sm.add_constant(X,has_constant="add")
res=sm.WLS(y,X.to_numpy(dtype=float),weights=w).fit(cov_type="HC1")
nom=list(X.columns)
print(f"WLS ponderado por kilos · N = {int(res.nobs):,} · R² = {res.rsquared:.3f} · "
      f"errores HC1 · base: mes {base_mes}, destino {base_dest}\n")

filas=[]
for c in [c for c in nom if c.startswith("d_")]:
    j=nom.index(c); dest=c[2:]
    prem=(np.exp(res.params[j])-1)*100
    se=res.bse[j]*100*np.exp(res.params[j])
    s=d[d.dest_g==dest]
    filas.append({"destino":dest,"premium_%":prem,"se_%":se,"t":res.params[j]/res.bse[j],
                  "fob_medio":(s.fob*s.kg).sum()/s.kg.sum(),"kt":s.kg.sum()/1e6,"filas":len(s)})
s=d[d.dest_g==base_dest]
filas.append({"destino":base_dest,"premium_%":0.0,"se_%":np.nan,"t":np.nan,
              "fob_medio":(s.fob*s.kg).sum()/s.kg.sum(),"kt":s.kg.sum()/1e6,"filas":len(s)})
T=pd.DataFrame(filas).sort_values("premium_%",ascending=False)
print("=== PREMIUM POR DESTINO · entero L1 · 2023-2026 (base España) ===")
print(T.round(2).to_string(index=False))
T.to_csv('/tmp/prem2326.csv',index=False)
