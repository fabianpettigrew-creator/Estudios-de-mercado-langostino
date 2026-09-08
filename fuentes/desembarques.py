# -*- coding: utf-8 -*-
"""Parser de desembarques oficiales (SSPyA): puerto × flota × especie × mes, 2013-2026."""
import pandas as pd, warnings, sys, re, glob, os, json; warnings.simplefilter('ignore')
sys.stdout.reconfigure(encoding='utf-8')
DIR=r"C:\Users\fmpet\OneDrive\IA agentes\Desembarques historicos argentina"
MES=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

def cargar_anio(path):
    anio=int(re.search(r'_(20\d\d)\.xlsx|(20\d\d)\.xlsx| (20\d\d)\.xlsx',path).group(1) or 0) if False else int(re.findall(r'(20\d\d)',os.path.basename(path))[-1])
    out=[]
    for sh in pd.ExcelFile(path).sheet_names:
        raw=pd.read_excel(path,sheet_name=sh,header=None)
        hi=None
        for i in range(min(8,len(raw))):
            if raw.iloc[i].astype(str).str.contains('Puerto',na=False).any(): hi=i;break
        if hi is None: continue
        d=pd.read_excel(path,sheet_name=sh,skiprows=hi)
        d.columns=[str(c).strip() for c in d.columns]
        ren={}
        for c in d.columns:
            cl=c.lower()
            if cl.startswith('puerto'): ren[c]='puerto'
            elif cl.startswith('flota'): ren[c]='flota'
            elif cl.startswith('especie'): ren[c]='especie'
        d=d.rename(columns=ren)
        if 'especie' not in d.columns: continue
        for c in ['puerto','flota']:
            if c in d.columns: d[c]=d[c].ffill()
            else: d[c]=None
        mcols=[c for c in d.columns if c in MES]
        if not mcols: continue
        m=d.melt(id_vars=['puerto','flota','especie'],value_vars=mcols,var_name='mes_nom',value_name='t')
        m['t']=pd.to_numeric(m['t'],errors='coerce').fillna(0)
        m['mes']=m['mes_nom'].map({n:i+1 for i,n in enumerate(MES)})
        m['anio']=anio; m['prov']=sh
        out.append(m[['anio','mes','prov','puerto','flota','especie','t']])
    return pd.concat(out,ignore_index=True) if out else None

files=sorted(glob.glob(os.path.join(DIR,"*.xlsx")))
D=pd.concat([cargar_anio(f) for f in files],ignore_index=True)
D['especie']=D['especie'].astype(str).str.strip()
D['flota']=D['flota'].astype(str).str.strip()
print(f"Cargado: {len(D):,} filas · años {D.anio.min()}-{D.anio.max()}")
lan=D[D['especie'].str.contains('angostino',case=False,na=False)]
print(f"Langostino: {len(lan):,} filas · especies: {sorted(lan.especie.unique())}")
print(f"\nFlotas que capturan langostino: ")
for fl,t in (lan.groupby('flota')['t'].sum()/1e3).sort_values(ascending=False).items():
    print(f"  {fl:34} {t:8.1f} kt (acum 2013-2026)")
lan.to_pickle('_lan.pkl')
