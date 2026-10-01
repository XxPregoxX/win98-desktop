#!/usr/bin/env python3
"""Gera temas/plasma/Win98/widgets/switch.svg: a chave liga/desliga do Plasma desenhada como a
caixa de marcar do 98 (no 98 não existia chave).

O SwitchIndicator do Plasma (org.kde.plasma.components) monta a chave com: trilho ("inactive",
tamanho em hint-bar-size, encolhido 1px de cada lado), parte preenchida ("active", do começo do
trilho até a bolinha, só com a chave ligada) e bolinha ("handle*"). Aqui:
- trilho = caixa branca afundada 13x13 (--border-field do 98.css) → desligada;
- parte preenchida = a mesma caixa com o ✓ do 98.css → ligada (cobre o trilho inteiro);
- bolinha e sombra/foco dela = transparentes, do tamanho da caixa (fica parada).
Também ligado em opaque/, solid/ e translucent/.
"""
from pathlib import Path

THEME = Path(__file__).resolve().parent.parent / "temas/plasma/Win98"
WHITE, LIGHT, SHADOW, FRAME = "#ffffff", "#dfdfdf", "#808080", "#0a0a0a"
FIELD = [(SHADOW, WHITE), (FRAME, LIGHT)]   # anéis de fora pra dentro: (cima/esquerda, baixo/direita)
BOX = 13        # caixa de marcar do 98
B = 2           # borda afundada
C = BOX - 2 * B # miolo (9)
CHECK = "M7 0H6v1H5v1H4v1H3v1H2V3H1V2H0v3h1v1h1v1h1V6h1V5h1V4h1V3h1V0z"   # ✓ 7x7 do 98.css


def ring_pixel(x, y, n, rings):
    k = min(x, y, n - 1 - x, n - 1 - y)
    if k >= len(rings):
        return None
    tl, br = rings[k]
    return br if (x == n - 1 - k or y == n - 1 - k) else tl


def frame(prefix, checked, y0):
    n = BOX
    out, y = [], y0

    def area(name, x0, yy, w, h):
        rs = "".join(f'<rect x="{x}" y="{y + dy}" width="1" height="1" fill="{ring_pixel(x0 + x, yy + dy, n, FIELD)}"/>'
                     for dy in range(h) for x in range(w))
        return f'<g id="{prefix}-{name}">{rs}</g>'

    e = n - B
    for name, (x0, yy, w, h) in {
        "topleft": (0, 0, B, B), "top": (B, 0, C, B), "topright": (e, 0, B, B),
        "left": (0, B, B, C), "right": (e, B, B, C),
        "bottomleft": (0, e, B, B), "bottom": (B, e, C, B), "bottomright": (e, e, B, B),
    }.items():
        out.append(area(name, x0, yy, w, h))
        y += max(h, 1) + 2
    centro = f'<rect x="0" y="{y}" width="{C}" height="{C}" fill="{WHITE}"/>'
    if checked:
        centro += f'<path d="{CHECK}" fill="{FRAME}" transform="translate(1,{y + 1})"/>'
    out.append(f'<g id="{prefix}-center">{centro}</g>')
    y += C + 2
    return out, y


body, y = [], 0
for prefix, checked in (("inactive", False), ("active", True)):
    part, y = frame(prefix, checked, y)
    body += part
for name in ("handle", "handle-hover", "handle-pressed", "handle-active", "handle-shadow", "handle-focus"):
    body.append(f'<rect id="{name}" x="0" y="{y}" width="{BOX}" height="{BOX}" fill="none"/>')
    y += BOX + 2
# o trilho encolhe 1px de cada lado: 15 de largura dá a caixa de 13
body.append(f'<rect id="hint-bar-size" x="0" y="{y}" width="{BOX + 2}" height="{BOX}" fill="none"/>')
y += BOX + 2

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="40" height="{y + 4}" version="1.1" '
       'shape-rendering="crispEdges">\n' + "\n".join(body) + "\n</svg>\n")
rel = "widgets/switch.svg"
(THEME / rel).write_text(svg)
for variant in ("opaque", "solid", "translucent"):
    link = THEME / variant / rel
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(Path("../../") / rel)
print("gerado:", THEME / rel, "(e links em opaque/solid/translucent)")
