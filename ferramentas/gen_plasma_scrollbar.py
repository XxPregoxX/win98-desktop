#!/usr/bin/env python3
"""Gera temas/plasma/Win98/widgets/scrollbar.svg: a barra de rolagem do Plasma no jeito do 98.

- 16px de largura (hint-scrollbar-size), como no 98;
- marcador (slider / mouseover-slider) = botão em relevo (o mesmo de widgets/button);
- trilho (background-vertical / -horizontal) = o pontilhado cinza/branco do 98 (98.css
  ::-webkit-scrollbar-track), repetido (hint-tile-center, bordas de 2px pra o padrão não
  desencontrar).
Limites do Plasma 6 (ScrollBar.qml): não tem setinhas ("TODO: support arrows") e o trilho só
aparece com o mouse em cima (opacity fixa no código). Também ligado em opaque/, solid/, translucent/.
"""
from pathlib import Path

THEME = Path(__file__).resolve().parent.parent / "temas/plasma/Win98"
FACE, LIGHT, WHITE, SHADOW, FRAME = "#c0c0c0", "#dfdfdf", "#ffffff", "#808080", "#0a0a0a"
RAISED = [(WHITE, FRAME), (LIGHT, SHADOW)]   # anéis de fora pra dentro: (cima/esquerda, baixo/direita)
SIZE = 16
C = 8     # miolo dos pedaços de exemplo (par, pro pontilhado)
B = 2     # borda (par, pro pontilhado)


def ring_pixel(x, y, n, rings):
    k = min(x, y, n - 1 - x, n - 1 - y)
    if k >= len(rings):
        return None
    tl, br = rings[k]
    return br if (x == n - 1 - k or y == n - 1 - k) else tl


def dither(x, y):
    return FACE if (x + y) % 2 == 0 else WHITE


def pieces(prefix, pixel):
    n = 2 * B + C

    def area(x0, y0, w, h):
        return [(x, y, 1, 1, pixel(x0 + x, y0 + y, n)) for y in range(h) for x in range(w)]

    e = n - B
    return {
        f"{prefix}-topleft": area(0, 0, B, B), f"{prefix}-top": area(B, 0, C, B),
        f"{prefix}-topright": area(e, 0, B, B), f"{prefix}-left": area(0, B, B, C),
        f"{prefix}-center": area(B, B, C, C), f"{prefix}-right": area(e, B, B, C),
        f"{prefix}-bottomleft": area(0, e, B, B), f"{prefix}-bottom": area(B, e, C, B),
        f"{prefix}-bottomright": area(e, e, B, B),
    }


def slider_pixel(x, y, n):
    return ring_pixel(x, y, n, RAISED) or FACE


def track_pixel(x, y, n):
    return dither(x, y)


elements = {}
for p in ("slider", "mouseover-slider"):
    elements.update(pieces(p, slider_pixel))
for p in ("background-vertical", "background-horizontal"):
    elements.update(pieces(p, track_pixel))

body, y = [], 0
for name, rects in elements.items():
    h = max(ry + rh for rx, ry, rw, rh, c in rects)
    rs = "".join(f'<rect x="{rx}" y="{y + ry}" width="{rw}" height="{rh}" fill="{c}"/>'
                 for rx, ry, rw, rh, c in rects)
    body.append(f'<g id="{name}">{rs}</g>')
    y += h + 2
body.append(f'<rect id="hint-scrollbar-size" x="0" y="{y}" width="{SIZE}" height="{SIZE}" fill="none"/>')
y += SIZE + 2
for p in ("background-vertical", "background-horizontal"):
    body.append(f'<rect id="{p}-hint-tile-center" x="0" y="{y}" width="1" height="1" fill="none"/>')
    y += 3

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="40" height="{y + 4}" version="1.1" '
       'shape-rendering="crispEdges">\n' + "\n".join(body) + "\n</svg>\n")
rel = "widgets/scrollbar.svg"
(THEME / rel).write_text(svg)
for variant in ("opaque", "solid", "translucent"):
    link = THEME / variant / rel
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(Path("../../") / rel)
print("gerado:", THEME / rel, "(e links em opaque/solid/translucent)")
