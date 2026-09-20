# -*- coding: utf-8 -*-
"""Exportación de camarón de Perú (Softrade, NANDINA 030617), 2019-2026.
Deduplica dentro de cada archivo Y descarta archivos de años repetidos
(hay dos descargas idénticas de 2023)."""
import pandas as pd, warnings, sys, re, glob, os; warnings.simplefilter('ignore')
sys.stdout.reconfigure(encoding='utf-8')
import sys as _sys, os as _os  # biblioteca BASES DE DATOS (mapa rutas_bases.py)
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from biblioteca import fuente
DIR=fuente("softrade_langostino", "EXPO PERU LANGOSTINO")
CLAVE=['DUA','Fecha','NANDINA','Exportador','País de Destino','Kgs. Netos','U$S FOB']

def anio_de(f):
    par=pd.read_excel(f,'Parámetros',header=None).iloc[:,0].dropna().astype(str)
    p=[x for x in par if 'Per' in x and '/' in x]
    return int(p[0][-4:]) if p else None

def cargar():
    vistos={}
    for f in sorted(glob.glob(os.path.join(DIR,"*.xlsx"))):
        if "~$" in f: continue
        a=anio_de(f)
        if a in vistos:            # año ya cargado: descarga repetida
            print(f"  · omitido {os.path.basename(f)[-14:]} (año {a} ya cargado)")
            continue
        d=pd.read_excel(f,'Detalle')
        ren={}
        for c in d.columns:
            s=str(c)
            if s.startswith('Vía Trans') or s=='Transporte': ren[c]='transporte'
            elif s.startswith('Nombre Trans') or s=='Transportista': ren[c]='transportista'
            elif s.startswith('Descripción'): ren[c]='descripcion'
            elif s.startswith('Cantidad'): ren[c]='cantidad'
            elif s in ('U$S Unitario','Unitario FOB'): ren[c]='unitario'
        d=d.rename(columns=ren)
        kk=[c for c in CLAVE if c in d.columns]
        n0=len(d); d=d[~d.duplicated(subset=kk,keep='first')]
        d['anio']=a
        d['kg']=pd.to_numeric(d['Kgs. Netos'],errors='coerce')
        d['fob']=pd.to_numeric(d['U$S FOB'],errors='coerce')
        d['dest']=d['País de Destino'].astype(str).str.strip()
        d['desc']=d.get('descripcion','').astype(str)
        vistos[a]=d[['anio','Fecha','dest','kg','fob','desc','Exportador']]
        print(f"  · {a}: {n0} filas → {len(d)} tras dedup ({n0-len(d)} dups)")
    return pd.concat(vistos.values(),ignore_index=True)

D=cargar()
D=D[(D['kg']>0)]
print(f"\nTOTAL limpio: {len(D):,} filas · {D.anio.min()}-{D.anio.max()}")
print("\n=== EXPORTACIÓN DE CAMARÓN DE PERÚ (NANDINA 030617) ===")
g=D.groupby('anio').apply(lambda s:pd.Series({'kt':s['kg'].sum()/1e6,'MUSD':s['fob'].sum()/1e6,
    'usd_kg':s['fob'].sum()/s['kg'].sum()}))
print(g.round(2).to_string())
D.to_pickle('_peru.pkl')
