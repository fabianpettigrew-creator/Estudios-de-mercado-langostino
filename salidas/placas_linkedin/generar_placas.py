# -*- coding: utf-8 -*-
"""Genera las placas de LinkedIn (PNG 1080x1350 + PDF carrusel) desde contenido.py.

Uso:  python generar_placas.py
Salida: placas/placa_NN.png  y  Placas_langostino_carrusel.pdf
"""
import base64
import io
import os
import subprocess
import sys

import glob as _glob

AQUI = os.path.dirname(os.path.abspath(__file__))
# La carpeta de logos lleva tilde; se resuelve con glob para no depender del encoding.
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


LOGO_CLARO = b64(os.path.join(LOGOS, "logo-axia-horizontal-marino.png"))      # blanco sobre navy
LOGO_OSCURO = b64(os.path.join(LOGOS, "logo-axia-horizontal-transparente.png"))  # navy sobre claro

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#888; }
.slide {
  width:%(W)dpx; height:%(H)dpx; position:relative; overflow:hidden;
  font-family:"Segoe UI","Calibri",Arial,sans-serif;
  display:flex; flex-direction:column; padding:84px 86px 74px 86px;
  page-break-after:always; break-after:page;
}
.slide.claro { background:%(CREAM)s; color:%(TEXT)s; }
.slide.oscuro { background:%(NAVY)s; color:#fff; }

/* filete superior */
.slide::before { content:""; position:absolute; top:0; left:0; width:100%%; height:14px; background:%(GOLD)s; }

.kicker { font-size:25px; font-weight:700; letter-spacing:4.2px; color:%(GOLD)s;
          text-transform:uppercase; margin-bottom:30px; }

.headline { font-size:62px; font-weight:700; line-height:1.09; letter-spacing:-1.2px;
            max-width:16ch; margin-bottom:auto; }
.slide.oscuro .headline { color:#fff; }

/* bloque de dato */
.statblock { background:%(NAVY)s; padding:38px 46px 36px 46px; margin:32px 0 30px 0;
             border-left:11px solid %(GOLD)s; }
.stat { color:%(GOLD)s; font-weight:700; line-height:0.84; letter-spacing:-3px;
        white-space:nowrap; }
.stat .vs, .stat .arrow { color:#fff; font-weight:400; letter-spacing:0;
        font-size:0.44em; padding:0 0.26em; vertical-align:0.24em; }
.statlabel { color:#D9DDE4; font-size:28px; line-height:1.4; margin-top:22px; max-width:33ch; }

.body { font-size:30px; line-height:1.47; color:#3E4757; max-width:38ch; }
.slide.oscuro .body { color:#C8CDD6; }

.cita { border-left:6px solid %(GOLD)s; padding:4px 0 4px 26px; margin:0 0 34px 0;
        font-size:26px; line-height:1.42; color:#5A6272; font-style:italic; max-width:41ch; }

/* portada y cierre */
.titulo { font-size:112px; font-weight:700; line-height:1.02; letter-spacing:-3.5px; color:#fff; }
.subtitulo { font-size:38px; color:%(GOLD)s; margin-top:26px; font-weight:600; }
.lead { font-size:32px; line-height:1.5; color:#C8CDD6; margin-top:36px; max-width:34ch; }
.cta { font-size:27px; color:%(GOLD)s; font-weight:600; margin-top:40px; letter-spacing:0.4px; }
.rule { width:132px; height:7px; background:%(GOLD)s; margin:0 0 40px 0; }

/* pie */
.foot { display:flex; align-items:center; justify-content:space-between;
        margin-top:38px; padding-top:26px; border-top:1px solid rgba(0,0,0,0.13); }
.slide.oscuro .foot { border-top:1px solid rgba(255,255,255,0.20); }
.foot img { height:74px; display:block; }
.fuente { font-size:19px; color:%(MUTED)s; line-height:1.4; text-align:right; white-space:nowrap; }
.num { font-size:19px; color:%(MUTED)s; font-weight:600; letter-spacing:1.5px; margin-left:22px; }
.footright { display:flex; align-items:center; }
""" % dict(W=W, H=H, CREAM=CREAM, NAVY=NAVY, GOLD=GOLD, TEXT=TEXT, MUTED=MUTED)


def render_slide(s, idx, total, nro_hallazgo=None):
    num = "%02d / %02d" % (idx + 1, total)
    tipo = s["tipo"]
    oscuro = tipo in ("portada", "cierre")
    logo = LOGO_CLARO if oscuro else LOGO_OSCURO
    clase = "oscuro" if oscuro else "claro"

    if tipo == "portada":
        cuerpo = (
            '<div style="margin:auto 0 0 0"></div>'
            '<div class="rule"></div>'
            '<div class="titulo">%(titulo)s</div>'
            '<div class="subtitulo">%(subtitulo)s</div>'
            '<div class="lead">%(lead)s</div>'
            '<div style="margin:0 0 auto 0"></div>' % s
        )
    elif tipo == "cierre":
        cuerpo = (
            '<div style="margin:auto 0 0 0"></div>'
            '<div class="rule"></div>'
            '<div class="titulo">%(titulo)s</div>'
            '<div class="lead">%(lead)s</div>'
            '<div class="cta">%(cta)s</div>'
            '<div style="margin:0 0 auto 0"></div>' % s
        )
    else:
        cita = ('<div class="cita">&laquo;%s&raquo;</div>' % s["cita"]) if s.get("cita") else ""
        cuerpo = (
            '<h1 class="headline">%(headline)s</h1>'
            '<div class="statblock">'
            '  <div class="stat" style="font-size:%(stat_size)dpx">%(stat)s</div>'
            '  <div class="statlabel">%(stat_label)s</div>'
            '</div>' % s
        ) + cita + ('<p class="body">%(body)s</p>' % s)

    fuente = ("Fuente: " + s["fuente"]) if s.get("fuente") else ""
    pie = (
        '<div class="foot">'
        '  <img src="%s">'
        '  <div class="footright"><div class="fuente">%s</div><div class="num">%s</div></div>'
        '</div>'
    ) % (logo, fuente, num)

    if tipo in ("portada", "cierre"):
        pie = (
            '<div class="foot">'
            '  <img src="%s">'
            '  <div class="footright"><div class="num">%s</div></div>'
            '</div>'
        ) % (logo, num if tipo != "portada" else "")

    if s.get("tema"):
        kicker = "HALLAZGO %02d &middot; %s" % (nro_hallazgo, s["tema"])
    else:
        kicker = s.get("kicker", "")

    return '<div class="slide %s">%s%s%s</div>' % (
        clase,
        ('<div class="kicker">%s</div>' % kicker) if kicker else "",
        cuerpo,
        pie,
    )


def doc(bodies, para_pdf=False):
    extra = ""
    if para_pdf:
        extra = "@page { size:%dpx %dpx; margin:0; } body{background:#fff;}" % (W, H)
    else:
        extra = "body{background:#fff;} .slide{margin:0;}"
    return (
        '<!doctype html><html><head><meta charset="utf-8">'
        "<style>%s\n%s</style></head><body>%s</body></html>"
        % (CSS, extra, "".join(bodies))
    )


def main():
    sys.path.insert(0, AQUI)
    from contenido import SLIDES

    total = len(SLIDES)
    outdir = os.path.join(AQUI, "placas")
    tmp = os.path.join(AQUI, "_tmp")
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(tmp, exist_ok=True)
    # borrar PNG de corridas anteriores para que no queden placas huérfanas
    for viejo in _glob.glob(os.path.join(outdir, "placa_*.png")):
        os.remove(viejo)

    bodies = []
    nro = 0
    for i, s in enumerate(SLIDES):
        if s.get("tema"):
            nro += 1
        bodies.append(render_slide(s, i, total, nro))

    # --- PNG individuales ---
    for i, body in enumerate(bodies):
        html = os.path.join(tmp, "s%02d.html" % (i + 1))
        with io.open(html, "w", encoding="utf-8") as f:
            f.write(doc([body]))
        png = os.path.join(outdir, "placa_%02d.png" % (i + 1))
        subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--default-background-color=00000000",
            "--window-size=%d,%d" % (W, H),
            "--screenshot=" + png, "file:///" + html.replace("\\", "/"),
        ], check=True, capture_output=True)
        print("  PNG", os.path.basename(png))

    # --- PDF carrusel ---
    html = os.path.join(tmp, "carrusel.html")
    with io.open(html, "w", encoding="utf-8") as f:
        f.write(doc(bodies, para_pdf=True))
    pdf = os.path.join(AQUI, "Placas_langostino_carrusel.pdf")
    # Chrome devuelve 0 aunque no pueda escribir (p. ej. si el PDF está abierto),
    # así que se genera en temporal y se reemplaza, verificando el resultado.
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
        raise RuntimeError(
            "No se pudo escribir %s (%s). "
            "Cerrá el PDF si lo tenés abierto en un visor y volvé a correr." % (pdf, e))
    print("  PDF", os.path.basename(pdf))
    print("Listo: %d placas." % total)


if __name__ == "__main__":
    main()
