"""Genera el logo de EcomBriefs (símbolo + wordmark) como SVG.

Uso: python3 gen_logo.py <font.ttf> <out_dir>
El wordmark se convierte a trazados con Manrope (OFL) a peso 700.
"""
import math, sys, os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont

FONT, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

GREEN = "#165F4C"
INK = "#172D27"
BG = "#F7F8F4"
GREEN_ON_DARK = "#8FD3B6"
DARK_BG = "#10241F"
WHITE = "#FFFFFF"

# ---------- Símbolo ----------
# Rejilla de 36 de alto: trazos de 8, aperturas de 6.
T, G = 8, 6
W_TOP, W_BOT = 34, 30
MID_X0, MID_X1 = T + G, 28
R_OUT, R_IN = 2.5, 1.25


def rounded_poly(pts, radii):
    """Polígono con esquinas redondeadas (arcos). pts en sentido horario (y hacia abajo)."""
    n = len(pts)
    d = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        r = radii[i]
        v1 = (p0[0] - p1[0], p0[1] - p1[1]); l1 = math.hypot(*v1)
        v2 = (p2[0] - p1[0], p2[1] - p1[1]); l2 = math.hypot(*v2)
        a = (p1[0] + v1[0] / l1 * r, p1[1] + v1[1] / l1 * r)
        b = (p1[0] + v2[0] / l2 * r, p1[1] + v2[1] / l2 * r)
        cross = v1[0] * v2[1] - v1[1] * v2[0]
        sweep = 1 if cross < 0 else 0
        d.append(("M" if i == 0 else "L") + f"{a[0]:g} {a[1]:g}")
        d.append(f"A{r:g} {r:g} 0 0 {sweep} {b[0]:g} {b[1]:g}")
    return "".join(d) + "Z"


def symbol_paths(ox=0.0, oy=0.0):
    yb = 2 * T + 2 * G  # arranque de la línea inferior
    pts = [(0, 0), (W_TOP, 0), (W_TOP, T), (T, T), (T, yb), (W_BOT, yb), (W_BOT, yb + T), (0, yb + T)]
    pts = [(x + ox, y + oy) for x, y in pts]
    radii = [R_OUT, R_OUT, R_OUT, R_IN, R_IN, R_OUT, R_OUT, R_OUT]
    outer = rounded_poly(pts, radii)
    my0 = T + G
    mid = [(MID_X0, my0), (MID_X1, my0), (MID_X1, my0 + T), (MID_X0, my0 + T)]
    mid = [(x + ox, y + oy) for x, y in mid]
    middle = rounded_poly(mid, [R_OUT] * 4)
    return outer, middle

SYM_W, SYM_H = W_TOP, 3 * T + 2 * G  # 36 x 40


# ---------- Favicon (rejilla de píxel 16 → dibujado a 32) ----------
def favicon_svg(bg=GREEN, fg=WHITE, radius=7):
    # Todos los valores son pares: a 16 px caen en píxel entero.
    stem_x, t, top, mid0, mid1, bot = 7, 4, 25, 15, 23, 23
    y = [6, 14, 22]
    outer = rounded_poly([(stem_x, y[0]), (top, y[0]), (top, y[0] + t), (stem_x + t, y[0] + t), (stem_x + t, y[2]), (bot, y[2]), (bot, y[2] + t), (stem_x, y[2] + t)],
                         [1, 1, 1, .5, .5, 1, 1, 1])
    middle = rounded_poly([(mid0, y[1]), (mid1, y[1]), (mid1, y[1] + t), (mid0, y[1] + t)], [1] * 4)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">'
            f'<title>EcomBriefs</title>'
            f'<rect width="32" height="32" rx="{radius}" fill="{bg}"/>'
            f'<path fill="{fg}" d="{outer}"/><path fill="{fg}" d="{middle}"/></svg>\n')


# ---------- Wordmark ----------
WGHT = 700
TRACK = -0.012  # em

vf = TTFont(FONT)
inst = instantiateVariableFont(vf, {"wght": WGHT})
glyphset = inst.getGlyphSet()
upem = inst["head"].unitsPerEm
cap = inst["OS/2"].sCapHeight

blob = hb.Blob.from_file_path(FONT)
face = hb.Face(blob)
hbfont = hb.Font(face)
hbfont.set_variations({"wght": WGHT})


def text_path(text, size, x0, baseline):
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": False})
    scale = size / upem
    x = 0.0
    pen = SVGPathPen(glyphset)
    order = inst.getGlyphOrder()
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gname = order[info.codepoint]
        tp = TransformPen(pen, (scale, 0, 0, -scale, x0 + (x + pos.x_offset) * scale, baseline))
        glyphset[gname].draw(tp)
        x += pos.x_advance + TRACK * upem
    width = (x - TRACK * upem) * scale
    return pen.getCommands(), width


# Composición horizontal: el símbolo mide 40; la altura de mayúscula del texto ≈ 26
# (0,65 del símbolo) y se centra ópticamente con el símbolo.
FONT_SIZE = 22.5 / (cap / upem)
GAP = 13  # distancia símbolo-nombre
PAD = 0
cap_px = cap / upem * FONT_SIZE
baseline = SYM_H / 2 + cap_px / 2
text_x = SYM_W + GAP
d_text, tw = text_path("EcomBriefs", FONT_SIZE, text_x, baseline)

# Límites verticales reales: descendentes no hay; la "f" y la "B" no pasan de la altura de ascendente.
LOGO_W = round(text_x + tw + 0.5, 2)
LOGO_H = SYM_H


def logo_svg(sym_color, text_color, bg=None, title="EcomBriefs", margin=0):
    outer, middle = symbol_paths(margin, margin)
    _, _ = outer, middle
    d_t, _ = text_path("EcomBriefs", FONT_SIZE, text_x + margin, baseline + margin)
    w, h = LOGO_W + 2 * margin, LOGO_H + 2 * margin
    bgr = f'<rect width="{w:g}" height="{h:g}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w*4:g}" height="{h*4:g}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{bgr}'
            f'<path fill="{sym_color}" d="{outer}"/><path fill="{sym_color}" d="{middle}"/>'
            f'<path fill="{text_color}" d="{d_t}"/></svg>\n')


def symbol_svg(color, bg=None, margin=0, size=None):
    outer, middle = symbol_paths(margin, margin)
    w, h = SYM_W + 2 * margin, SYM_H + 2 * margin
    bgr = f'<rect width="{w:g}" height="{h:g}" fill="{bg}"/>' if bg else ""
    sz = f' width="{size or w*4:g}" height="{(size or w*4)*h/w:g}"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}"{sz} role="img" aria-label="EcomBriefs">'
            f'<title>EcomBriefs</title>{bgr}<path fill="{color}" d="{outer}"/><path fill="{color}" d="{middle}"/></svg>\n')


def editable_svg():
    """Versión editable: símbolo con formas simples y nombre como texto vivo."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LOGO_W:g} {LOGO_H:g}" width="{LOGO_W*4:g}" height="{LOGO_H*4:g}">
  <!-- Versión EDITABLE del logo de EcomBriefs.
       Requiere la fuente Manrope (OFL) instalada, peso {WGHT}, espaciado {TRACK}em.
       Para compartir, usa los archivos con el texto convertido a trazados. -->
  <title>EcomBriefs (editable)</title>
  <g id="simbolo" fill="{GREEN}">
    <!-- Rejilla: trazos de {T}, aperturas de {G}. Eje vertical + tres líneas; la central queda separada del eje. -->
    <path d="{symbol_paths()[0]}"/>
    <rect x="{MID_X0}" y="{T+G}" width="{MID_X1-MID_X0}" height="{T}" rx="{R_OUT:g}"/>
  </g>
  <text id="nombre" x="{text_x:g}" y="{baseline:.3f}" font-family="Manrope" font-weight="{WGHT}" font-size="{FONT_SIZE:.3f}" letter-spacing="{TRACK*FONT_SIZE:.3f}" fill="{INK}">EcomBriefs</text>
</svg>
'''


files = {
    "ecombriefs-logo.svg": logo_svg(GREEN, INK),
    "ecombriefs-logo-fondo-oscuro.svg": logo_svg(GREEN_ON_DARK, WHITE),
    "ecombriefs-logo-mono-oscuro.svg": logo_svg(INK, INK),
    "ecombriefs-logo-mono-blanco.svg": logo_svg(WHITE, WHITE),
    "ecombriefs-logo-editable.svg": editable_svg(),
    "ecombriefs-simbolo.svg": symbol_svg(GREEN),
    "ecombriefs-simbolo-fondo-oscuro.svg": symbol_svg(GREEN_ON_DARK),
    "ecombriefs-simbolo-mono-oscuro.svg": symbol_svg(INK),
    "ecombriefs-simbolo-mono-blanco.svg": symbol_svg(WHITE),
    "favicon.svg": favicon_svg(),
}
for name, svg in files.items():
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(svg)

# Datos para incrustar el logo en HTML (cabecera, pie)
import json
outer, middle = symbol_paths()
json.dump({"viewBox": f"0 0 {LOGO_W:g} {LOGO_H:g}", "symbol": [outer, middle], "text": d_text,
           "sym_w": SYM_W, "sym_h": SYM_H, "logo_w": LOGO_W, "logo_h": LOGO_H},
          open(os.path.join(OUT, "_logo-data.json"), "w"))
print("logo", LOGO_W, LOGO_H, "font", FONT_SIZE, "text width", tw)
