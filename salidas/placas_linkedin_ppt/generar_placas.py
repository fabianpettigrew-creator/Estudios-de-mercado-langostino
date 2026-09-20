# -*- coding: utf-8 -*-
"""Genera las placas del resumen ejecutivo (PNG 1080x1350 + PDF carrusel).

Uso:  python generar_placas.py
Salida: placas/placa_NN.png  y  Placas_resumen_langostino.pdf
"""
import base64
import glob as _glob
import io
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
# Raiz del OneDrive: cuatro niveles arriba de esta carpeta
# (<esta>/salidas/Estudios de mercado langostino/IA agentes/<OneDrive>).
_ONEDRIVE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
LOGOS = _glob.glob(os.path.join(_ONEDRIVE, "Logos", "Fabian Pettigrew",
                                "Logo para consultora econ*mica"))[0]
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

W, H = 1080, 1350

NAVY = "#151D2B"
GOLD = "#C99A5F"
CREAM = "#F7F5F1"
TEXT = "#2B3242"
MUTED = "#858C9A"


def b64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


LOGO_CLARO = b64(os.path.join(LOGOS, "logo-axia-horizontal-marino.png"))
LOGO_OSCURO = b64(os.path.join(LOGOS, "logo-axia-horizontal-transparente.png"))

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
.slide {
  width:%(W)dpx; height:%(H)dpx; position:relative; overflow:hidden;
  font-family:"Segoe UI","Calibri",Arial,sans-serif;
  display:flex; flex-direction:column; padding:78px 82px 68px 82px;
  page-break-after:always; break-after:page;
}
.slide.claro  { background:%(CREAM)s; color:%(TEXT)s; }
.slide.oscuro { background:%(NAVY)s;  color:#fff; }
.slide::before { content:""; position:absolute; top:0; left:0; width:100%%; height:13px; background:%(GOLD)s; }

.kicker { font-size:23px; font-weight:700; letter-spacing:3.8px; color:%(GOLD)s;
          text-transform:uppercase; margin-bottom:22px; }
.headline { font-size:54px; font-weight:700; line-height:1.1; letter-spacing:-1.1px; max-width:19ch; }
.slide.oscuro .headline { color:#fff; }
.intro { font-size:26px; line-height:1.42; color:#59606F; margin-top:18px; max-width:44ch; }
.slide.oscuro .intro { color:#B6BCC7; }

.cuerpo { margin-top:32px; margin-bottom:auto; }

/* --- remate --- */
.remate { font-size:23px; line-height:1.44; color:#4A5263; background:rgba(21,29,43,0.045);
          border-left:6px solid %(GOLD)s; padding:20px 24px; margin-top:26px; }
.slide.oscuro .remate { color:#C8CDD6; background:rgba(255,255,255,0.06); }

/* --- lista (cinco números) --- */
.fila { display:flex; align-items:baseline; gap:24px; padding:19px 0;
        border-bottom:1px solid rgba(21,29,43,0.11); }
.fila:last-child { border-bottom:none; }
.fila .val { font-size:52px; font-weight:700; color:%(GOLD)s; line-height:1;
             min-width:230px; letter-spacing:-1.5px; }
.fila .txt .lab { font-size:26px; font-weight:600; color:%(NAVY)s; line-height:1.25; }
.fila .txt .not { font-size:21px; color:#7A8291; line-height:1.34; margin-top:5px; }

/* --- puntos numerados --- */
.punto { display:flex; gap:24px; padding:17px 0; }
.punto .n { font-size:44px; font-weight:700; color:%(GOLD)s; line-height:0.95;
            min-width:56px; letter-spacing:-1px; }
.punto .tit { font-size:28px; font-weight:700; line-height:1.22; margin-bottom:7px; }
.punto .des { font-size:23px; line-height:1.42; color:#4A5263; }
.slide.oscuro .punto .des { color:#B6BCC7; }

/* --- tarjetas apiladas --- */
.tarjeta { background:#fff; border-left:8px solid %(GOLD)s; padding:22px 26px; margin-bottom:16px;
           box-shadow:0 1px 0 rgba(21,29,43,0.08); }
.tarjeta:last-child { margin-bottom:0; }
.tarjeta .eyebrow { font-size:17px; font-weight:700; letter-spacing:2.4px; color:%(GOLD)s;
                    text-transform:uppercase; margin-bottom:7px; }
.tarjeta .tit { font-size:31px; font-weight:700; color:%(NAVY)s; line-height:1.15; margin-bottom:9px; }
.tarjeta .des { font-size:22px; line-height:1.42; color:#4A5263; }

/* --- dos stats --- */
.statblock { background:%(NAVY)s; border-left:10px solid %(GOLD)s; padding:26px 32px 24px 32px;
             margin-bottom:18px; }
.statblock:last-child { margin-bottom:0; }
.statblock .n { color:%(GOLD)s; font-weight:700; line-height:0.9; letter-spacing:-2.5px; white-space:nowrap; }
.statblock .lab { color:#fff; font-size:27px; font-weight:600; margin-top:12px; line-height:1.25; }
.statblock .not { color:#AEB6C2; font-size:21px; margin-top:8px; line-height:1.38; max-width:54ch; }

/* --- barras --- */
.stat_previo { background:%(NAVY)s; border-left:10px solid %(GOLD)s; padding:24px 30px; margin-bottom:24px; }
.stat_previo .n { color:%(GOLD)s; font-size:76px; font-weight:700; line-height:0.95; letter-spacing:-2px; }
.stat_previo .d { color:#C8CDD6; font-size:22px; line-height:1.38; margin-top:10px; max-width:42ch; }

.barra { display:flex; align-items:center; gap:16px; margin-bottom:15px; }
.barra .nom { font-size:24px; font-weight:600; width:158px; text-align:right; color:%(NAVY)s; }
.barra .pista { flex:1; height:42px; position:relative; }
.barra .rel { height:42px; background:#C3C9D2; }
.barra.destacada .rel { background:%(GOLD)s; }
.barra .v1 { font-size:23px; font-weight:700; color:%(NAVY)s; width:118px; }
.barra .v2 { font-size:22px; color:#6E7686; width:92px; }
.pie_grafico { font-size:19px; color:#858C9A; margin-top:6px; padding-left:174px; }

/* --- aranceles --- */
.bloque_t { font-size:25px; font-weight:700; color:%(NAVY)s; margin:0 0 12px 0; }
.bloque_t.seg { margin-top:24px; }
.ab { display:flex; align-items:center; gap:12px; margin-bottom:8px; }
.ab .nom { font-size:21px; width:146px; text-align:right; color:%(NAVY)s; font-weight:600; }
.ab.destacada .nom { color:%(GOLD)s; }
.ab .pista { flex:1; height:26px; display:flex; }
.ab .s301 { height:26px; background:%(NAVY)s; }
.ab .adcvd { height:26px; background:#B9C0CB; }
.ab.destacada .s301 { background:%(GOLD)s; }
.ab .tot { font-size:21px; font-weight:700; width:78px; color:%(NAVY)s; }
.ab.destacada .tot { color:%(GOLD)s; }
.leyenda { font-size:18px; color:#858C9A; padding-left:130px; margin-top:2px; }

/* --- portada y cierre --- */
.titulo { font-size:94px; font-weight:700; line-height:1.03; letter-spacing:-3px; color:#fff; }
.subtitulo { font-size:33px; color:%(GOLD)s; margin-top:22px; font-weight:600; letter-spacing:0.5px; }
.lead { font-size:28px; line-height:1.48; color:#C8CDD6; margin-top:28px; max-width:40ch; }
.cta { font-size:24px; color:%(GOLD)s; font-weight:600; margin-top:24px; letter-spacing:0.4px; }
.rule { width:120px; height:7px; background:%(GOLD)s; margin:0 0 34px 0; }

/* --- pie --- */
.foot { display:flex; align-items:center; justify-content:space-between;
        margin-top:30px; padding-top:22px; border-top:1px solid rgba(21,29,43,0.14); }
.slide.oscuro .foot { border-top:1px solid rgba(255,255,255,0.20); }
.foot img { height:68px; display:block; }
.fuente { font-size:18px; color:%(MUTED)s; text-align:right; line-height:1.35; white-space:nowrap; }
.num { font-size:18px; color:%(MUTED)s; font-weight:600; letter-spacing:1.4px; margin-left:20px; white-space:nowrap; }
.footright { display:flex; align-items:center; }
""" % dict(W=W, H=H, CREAM=CREAM, NAVY=NAVY, GOLD=GOLD, TEXT=TEXT, MUTED=MUTED)


def _barras(barras, escala=None):
    mx = escala or max(b[1] for b in barras)
    out = []
    for nom, v, v1, v2, dest in barras:
        out.append(
            '<div class="barra%s"><div class="nom">%s</div>'
            '<div class="pista"><div class="rel" style="width:%.1f%%"></div></div>'
            '<div class="v1">%s</div><div class="v2">%s</div></div>'
            % (" destacada" if dest else "", nom, 100.0 * v / mx, v1, v2)
        )
    return "".join(out)


def _aranceles(s):
    mx = max(a[1] + a[2] for a in s["us"])
    us = []
    for nom, s301, adcvd, tot, dest in s["us"]:
        us.append(
            '<div class="ab%s"><div class="nom">%s</div><div class="pista">'
            '<div class="s301" style="width:%.1f%%"></div>'
            '<div class="adcvd" style="width:%.1f%%"></div></div>'
            '<div class="tot">%s</div></div>'
            % (" destacada" if dest else "", nom, 100.0 * s301 / mx, 100.0 * adcvd / mx, tot)
        )
    ue = []
    mxu = max(u[1] for u in s["ue"]) or 1
    for nom, v, lab in s["ue"]:
        dest = (v == 0.0)
        ue.append(
            '<div class="ab%s"><div class="nom">%s</div><div class="pista">'
            '<div class="s301" style="width:%.1f%%"></div></div>'
            '<div class="tot">%s</div></div>'
            % (" destacada" if dest else "", nom, 100.0 * v / mxu, lab)
        )
    return (
        '<div class="bloque_t">%s</div>%s<div class="leyenda">%s</div>'
        '<div class="bloque_t seg">%s</div>%s<div class="leyenda">%s</div>'
        % (s["titulo_us"], "".join(us), s["leyenda_us"],
           s["titulo_ue"], "".join(ue), s["leyenda_ue"])
    )


def render_slide(s, idx, total):
    tipo = s["tipo"]
    oscuro = tipo == "portada" or s.get("oscuro")
    clase = "oscuro" if oscuro else "claro"
    logo = LOGO_CLARO if oscuro else LOGO_OSCURO
    num = "%02d / %02d" % (idx + 1, total)

    if tipo == "portada":
        cuerpo = (
            '<div style="margin:auto 0 0 0"></div><div class="rule"></div>'
            '<div class="titulo">%(titulo)s</div>'
            '<div class="subtitulo">%(subtitulo)s</div>'
            '<div class="lead">%(lead)s</div>'
            '<div style="margin:0 0 auto 0"></div>' % s
        )
        cab = '<div class="kicker">%s</div>' % s["kicker"]
        return _envolver(clase, cab + cuerpo, logo, "", "", num if False else "")

    cab = '<div class="kicker">%s</div><h1 class="headline">%s</h1>' % (s["kicker"], s["headline"])
    if s.get("intro"):
        cab += '<div class="intro">%s</div>' % s["intro"]

    if tipo == "lista":
        filas = "".join(
            '<div class="fila"><div class="val">%s</div>'
            '<div class="txt"><div class="lab">%s</div><div class="not">%s</div></div></div>'
            % it for it in s["items"])
        cuerpo = '<div class="cuerpo">%s</div>' % filas

    elif tipo == "puntos":
        ps = "".join(
            '<div class="punto"><div class="n">%d</div>'
            '<div><div class="tit">%s</div><div class="des">%s</div></div></div>'
            % (i + 1, t, d) for i, (t, d) in enumerate(s["puntos"]))
        cuerpo = '<div class="cuerpo">%s</div>' % ps

    elif tipo == "tarjetas":
        ts = "".join(
            '<div class="tarjeta"><div class="eyebrow">%s</div>'
            '<div class="tit">%s</div><div class="des">%s</div></div>' % t
            for t in s["tarjetas"])
        cuerpo = '<div class="cuerpo">%s</div>' % ts

    elif tipo == "dos_stats":
        bs = "".join(
            '<div class="statblock"><div class="n" style="font-size:%dpx">%s</div>'
            '<div class="lab">%s</div><div class="not">%s</div></div>'
            % (size, n, lab, not_) for n, size, lab, not_ in s["stats"])
        cuerpo = '<div class="cuerpo">%s</div>' % bs

    elif tipo == "barras":
        prev = ""
        if s.get("stat_previo"):
            prev = ('<div class="stat_previo"><div class="n">%s</div><div class="d">%s</div></div>'
                    % s["stat_previo"])
        cuerpo = ('<div class="cuerpo">%s%s<div class="pie_grafico">%s</div></div>'
                  % (prev, _barras(s["barras"]), s["pie_grafico"]))

    elif tipo == "aranceles":
        cuerpo = '<div class="cuerpo">%s</div>' % _aranceles(s)

    else:
        raise ValueError("tipo desconocido: " + tipo)

    if s.get("remate"):
        cuerpo += '<div class="remate">%s</div>' % s["remate"]
    if s.get("cta"):
        cuerpo += '<div class="cta">%s</div>' % s["cta"]

    return _envolver(clase, cab + cuerpo, logo, s.get("fuente", ""), "", num)


def _envolver(clase, contenido, logo, fuente, _x, num):
    f = ('<div class="fuente">%s</div>' % ("Fuente: " + fuente)) if fuente else '<div class="fuente"></div>'
    pie = ('<div class="foot"><img src="%s">'
           '<div class="footright">%s<div class="num">%s</div></div></div>' % (logo, f, num))
    return '<div class="slide %s">%s%s</div>' % (clase, contenido, pie)


def doc(bodies, para_pdf=False):
    extra = ("@page { size:%dpx %dpx; margin:0; } body{background:#fff;margin:0;}" % (W, H)
             if para_pdf else "body{background:#fff;margin:0;}")
    return ('<!doctype html><html><head><meta charset="utf-8">'
            "<style>%s\n%s</style></head><body>%s</body></html>"
            % (CSS, extra, "".join(bodies)))


def main():
    sys.path.insert(0, AQUI)
    from contenido import SLIDES

    total = len(SLIDES)
    outdir = os.path.join(AQUI, "placas")
    tmp = os.path.join(AQUI, "_tmp")
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(tmp, exist_ok=True)
    for viejo in _glob.glob(os.path.join(outdir, "placa_*.png")):
        os.remove(viejo)

    bodies = [render_slide(s, i, total) for i, s in enumerate(SLIDES)]

    for i, body in enumerate(bodies):
        html = os.path.join(tmp, "s%02d.html" % (i + 1))
        with io.open(html, "w", encoding="utf-8") as f:
            f.write(doc([body]))
        png = os.path.join(outdir, "placa_%02d.png" % (i + 1))
        subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--window-size=%d,%d" % (W, H),
            "--screenshot=" + png, "file:///" + html.replace("\\", "/"),
        ], check=True, capture_output=True)
        print("  PNG", os.path.basename(png))

    html = os.path.join(tmp, "carrusel.html")
    with io.open(html, "w", encoding="utf-8") as f:
        f.write(doc(bodies, para_pdf=True))
    pdf = os.path.join(AQUI, "Placas_resumen_langostino.pdf")
    pdf_tmp = os.path.join(tmp, "carrusel.pdf")
    if os.path.exists(pdf_tmp):
        os.remove(pdf_tmp)
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        "--print-to-pdf-no-header", "--print-to-pdf=" + pdf_tmp,
        "file:///" + html.replace("\\", "/"),
    ], check=True, capture_output=True)
    if not os.path.exists(pdf_tmp):
        raise RuntimeError("Chrome no generó el PDF; revisar el HTML en " + tmp)
    try:
        os.replace(pdf_tmp, pdf)
    except OSError as e:
        raise RuntimeError("No se pudo escribir %s (%s). "
                           "Cerrá el PDF si lo tenés abierto y volvé a correr." % (pdf, e))
    print("  PDF", os.path.basename(pdf))
    print("Listo: %d placas." % total)


if __name__ == "__main__":
    main()
