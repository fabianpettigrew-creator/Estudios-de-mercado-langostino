"""Construye fishstat.db (SQLite) desde los CSV bulk de FAO Global Production.
Hechos + dimensiones (especie ASFIS, país, fuente captura/acuicultura), indexado."""
import pandas as pd, sqlite3, os, sys, warnings
warnings.simplefilter('ignore')
try: sys.stdout.reconfigure(encoding='utf-8')
except: pass
HERE=os.path.dirname(os.path.abspath(__file__))
DB=os.path.join(os.path.dirname(HERE), "fishstat.db")   # datos/fishstat.db

con=sqlite3.connect(DB)

# --- Hechos ---
fact=pd.read_csv(os.path.join(HERE,"Global_production_quantity.csv"))
fact.columns=['country_un','sp_a3','area','source','measure','anio','valor','status']
fact.to_sql("produccion", con, if_exists="replace", index=False)

# --- Dimensión especie ---
sp=pd.read_csv(os.path.join(HERE,"CL_FI_SPECIES_GROUPS.csv"))
sp=sp[['3A_Code','Scientific_Name','Name_En','ISSCAAP_Group_En','Major_Group']].rename(
    columns={'3A_Code':'sp_a3','Scientific_Name':'cientifico','Name_En':'nombre',
             'ISSCAAP_Group_En':'isscaap','Major_Group':'grupo_mayor'})
sp.to_sql("especie", con, if_exists="replace", index=False)

# --- Dimensión país ---
pa=pd.read_csv(os.path.join(HERE,"CL_FI_COUNTRY_GROUPS.csv"))
pa=pa[['UN_Code','ISO3_Code','ISO2_Code','Name_En']].rename(
    columns={'UN_Code':'country_un','ISO3_Code':'iso3','ISO2_Code':'iso2','Name_En':'pais'})
pa.to_sql("pais", con, if_exists="replace", index=False)

# --- Dimensión fuente ---
fu=pd.read_csv(os.path.join(HERE,"CL_FI_PRODUCTION_SOURCE_DET.csv"))
fu=fu[['Code','Name_En']].rename(columns={'Code':'source','Name_En':'fuente'})
fu['tipo']=fu['source'].map(lambda s:'captura' if s=='CAPTURE' else 'acuicultura')
fu.to_sql("fuente", con, if_exists="replace", index=False)

# --- Índices ---
cur=con.cursor()
for ix in ["CREATE INDEX IF NOT EXISTS ix_sp ON produccion(sp_a3)",
           "CREATE INDEX IF NOT EXISTS ix_ctry ON produccion(country_un)",
           "CREATE INDEX IF NOT EXISTS ix_per ON produccion(anio)",
           "CREATE INDEX IF NOT EXISTS ix_spper ON produccion(sp_a3,anio)"]:
    cur.execute(ix)
con.commit()

# --- Resumen ---
n=cur.execute("SELECT COUNT(*) FROM produccion").fetchone()[0]
yr=cur.execute("SELECT MIN(anio),MAX(anio) FROM produccion").fetchone()
nsp=cur.execute("SELECT COUNT(DISTINCT sp_a3) FROM produccion").fetchone()[0]
print(f"fishstat.db creado: {DB}")
print(f"  produccion: {n:,} filas · años {yr[0]}-{yr[1]} · {nsp} especies")
print(f"  dims: especie({len(sp)}), pais({len(pa)}), fuente({len(fu)})")
con.close()
