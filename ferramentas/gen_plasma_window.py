#!/usr/bin/env python3
"""Gera a "janelinha do 98" do tema do Plasma (temas/plasma/Win98/):

- dialogs/background.svg: fundo dos popups do Plasma (notificações, bandeja, calendário...):
  janela cinza com a borda do 98.css (--border-window-outer/inner), cantos retos, sem sombra.
- widgets/plasmoidheading.svg: cabeçalho dos popups (header) = faixa de título azul em degradê
  (#000080 → #1084d0, igual à barra de título das janelas), com a borda da janela em volta;
  rodapé (footer) = cinza com o sulco do 98 em cima.
O Plasma só mostra o cabeçalho do tema se o dialogs/background vier do mesmo tema.
Os dois arquivos também são ligados em opaque/, solid/ e translucent/.
"""
from pathlib import Path

THEME = Path(__file__).resolve().parent.parent / "temas/plasma/Win98"
FACE, LIGHT, WHITE, SHADOW, FRAME = "#c0c0c0", "#dfdfdf", "#ffffff", "#808080", "#0a0a0a"
NAVY, NAVY_LIGHT = "#000080", "#1084d0"
B = 3   # borda: 2px de relevo + 1px de cinza (padding da .window do 98.css)
M = 4   # margem do conteúdo dos popups (a mesma do Breeze)
C = 8   # tamanho do miolo nos pedaços de exemplo


def window_pixel(x, y, n):
    """Borda de janela do 98.css num quadrado n x n: -1 -1 moldura, 1 1 face clara,
    -2 -2 sombra, 2 2 branco (a primeira sombra da lista fica por cima)."""
    if x == n - 1 or y == n - 1:
        return FRAME
    if x == 0 or y == 0:
        return LIGHT
    if x == n - 2 or y == n - 2:
        return SHADOW
    if x == 1 or y == 1:
        return WHITE
    return None


def frame_pieces(prefix, center_fill, top=B, bottom=B, left=B, right=B, bevel_bottom=True):
    """Os 9 pedaços do FrameSvg (prefixo opcional), com a borda de janela e o miolo dado."""
    n = 2 * B + C
    def px(x, y):
        if not bevel_bottom and y >= n - B:   # sem borda embaixo: continua o que tem em cima
            y = n - B - 1
        return window_pixel(x, y, n) or FACE

    def area(x0, y0, w, h):
        pix = {(x, y): px(x0 + x, y0 + y) for x in range(w) for y in range(h)}
        # faixas inteiras no sentido em que o FrameSvg repete o pedaço (pixel solto deixa emenda)
        if all(len({pix[x, y] for y in range(h)}) == 1 for x in range(w)):
            return [(x, 0, 1, h, pix[x, 0]) for x in range(w)]
        if all(len({pix[x, y] for x in range(w)}) == 1 for y in range(h)):
            return [(0, y, w, 1, pix[0, y]) for y in range(h)]
        return [(x, y, 1, 1, c) for (x, y), c in sorted(pix.items())]

    e = n - B
    parts = {
        "top": area(B, 0, C, top), "bottom": area(B, n - bottom, C, bottom),
        "left": area(0, B, left, C), "right": area(n - right, B, right, C),
        "topleft": area(0, 0, left, top), "topright": area(n - right, 0, right, top),
        "bottomleft": area(0, n - bottom, left, bottom), "bottomright": area(n - right, n - bottom, right, bottom),
    }
    p = f"{prefix}-" if prefix else ""
    out = {p + k: v for k, v in parts.items() if v}
    out[p + "center"] = [(0, 0, C, C, center_fill)]
    return out


def to_svg(elements, extra=""):
    body, y = [], 0
    for name, rects in elements.items():
        w = max(rx + rw for rx, ry, rw, rh, c in rects)
        h = max(ry + rh for rx, ry, rw, rh, c in rects)
        rs = "".join(f'<rect x="{rx}" y="{y + ry}" width="{rw}" height="{rh}" fill="{c}"/>'
                     for rx, ry, rw, rh, c in rects)
        body.append(f'<g id="{name}">{rs}</g>')
        y += h + 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="40" height="{y + 40}" version="1.1">\n'
            + extra + "\n".join(body) + "\n" + f"%HINTS{y}%" + "</svg>\n")


def hints(y, names, size):
    out = []
    for i, n in enumerate(names):
        w, h = (size, 1) if "left" in n or "right" in n else (1, size)
        out.append(f'<rect id="{n}" x="{i * 6}" y="{y + 4}" width="{w}" height="{h}" fill="none"/>')
    return "\n".join(out) + "\n"


# --- dialogs/background ---
bg = frame_pieces("", FACE)
svg = to_svg(bg)
y = int(svg.split("%HINTS")[1].split("%")[0])
svg = svg.replace(f"%HINTS{y}%", hints(y, ["hint-top-margin", "hint-bottom-margin",
                                            "hint-left-margin", "hint-right-margin"], M))

# --- widgets/plasmoidheading ---
grad = ('<defs><linearGradient id="caption" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY_LIGHT}"/>'
        '</linearGradient></defs>\n')
# embaixo, 4px cinza (continuando o relevo dos lados): a linha do tempo da notificação (2px, cor
# de seleção = o mesmo azul-marinho, grudada nos 2 últimos px do cabeçalho pelo código do KDE)
# fica embaixo da faixa azul com 2px de cinza no meio, pra não se misturar com ela
head = frame_pieces("header", "url(#caption)", bottom=4, bevel_bottom=False)
foot = {}
for k, v in frame_pieces("footer", FACE, top=2, bevel_bottom=True).items():
    foot[k] = v
# rodapé: em cima, o sulco do 98 (sombra + branco) no lugar do relevo da janela
for k in ("footer-top", "footer-topleft", "footer-topright"):
    w = max(rx + rw for rx, ry, rw, rh, c in foot[k])
    foot[k] = [(0, 0, w, 1, SHADOW), (0, 1, w, 1, WHITE)]
hsvg = to_svg({**head, **foot}, grad)
y = int(hsvg.split("%HINTS")[1].split("%")[0])
hsvg = hsvg.replace(f"%HINTS{y}%", hints(y, ["hint-top-margin", "hint-bottom-margin",
                                              "hint-left-margin", "hint-right-margin"], B))

files = {"dialogs/background.svg": svg, "widgets/plasmoidheading.svg": hsvg}
for rel, content in files.items():
    dst = THEME / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content)
    for variant in ("opaque", "solid", "translucent"):
        link = THEME / variant / rel
        link.parent.mkdir(parents=True, exist_ok=True)
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(Path("../" * (rel.count("/") + 1)) / rel)
print("gerados:", ", ".join(files), "(e links em opaque/solid/translucent)")

# --- cores do cabeçalho (só valem dentro do Plasma): texto branco sobre a faixa azul.
# A notificação nunca fica em foco, então o [Inactive] é igual ao ativo.
import configparser, io
colors = THEME / "colors"
cp = configparser.ConfigParser(interpolation=None, strict=False)
cp.optionxform = str
cp.read(colors)
for sec in ("Colors:Header", "Colors:Header][Inactive"):
    if not cp.has_section(sec):
        cp.add_section(sec)
    cp[sec].update({"BackgroundNormal": "0,0,128", "BackgroundAlternate": "16,132,208",
                    "ForegroundNormal": "255,255,255", "ForegroundActive": "255,255,255",
                    "ForegroundInactive": "192,192,192", "ForegroundLink": "255,255,255",
                    "ForegroundVisited": "224,224,224", "DecorationFocus": "255,255,255",
                    "DecorationHover": "255,255,255"})
header = "".join(l for l in colors.read_text().splitlines(True) if l.startswith("#"))
buf = io.StringIO()
cp.write(buf, space_around_delimiters=False)
colors.write_text(header + buf.getvalue())
print("colors: [Colors:Header] branco sobre azul")

