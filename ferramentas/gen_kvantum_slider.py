#!/usr/bin/env python3
"""Gera o trilho do controle deslizante do Kvantum ([Slider] em temas/kvantum/Win98/).

No 98 o trilho é um sulco fino afundado (a mesma borda do --border-field do 98.css: cinza e preto
em cima/esquerda, branco e cinza-claro embaixo/direita), igual dos dois lados do marcador. O
marcador continua sendo o botão em relevo ([SliderCursor]), em pé (11x22). Antes o [Slider] estava desligado e
só o marcador aparecia, solto.
Estados: normal, focused (mouse em cima), pressed, toggled (a parte já percorrida) e disabled,
cada um com a versão "-inactive" (janela sem foco); todos iguais, como no 98.
Rodar de novo é seguro: substitui tudo o que for slider-*.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "temas/kvantum/Win98/Win98.svg"
CFG = ROOT / "temas/kvantum/Win98/Win98.kvconfig"
WHITE, LIGHT, SHADOW, FRAME = "#ffffff", "#dfdfdf", "#808080", "#0a0a0a"
B, M = 2, 6  # espessura da borda; tamanho do miolo nos pedaços de exemplo


def field_pixel(x, y, n):
    """Cor do pixel (x, y) da borda afundada num quadrado n x n (ordem do box-shadow do 98.css)."""
    if x == n - 1 or y == n - 1:
        return WHITE
    if x == 0 or y == 0:
        return SHADOW
    if x == n - 2 or y == n - 2:
        return LIGHT
    if x == 1 or y == 1:
        return FRAME
    return None


def pieces(fill):
    """Os 9 pedaços que o Kvantum espera, como listas de (x, y, w, h, cor) relativas."""
    n = 2 * B + M
    def area(x0, y0, w, h):
        px = {(x, y): field_pixel(x0 + x, y0 + y, n) or fill for x in range(w) for y in range(h)}
        # faixas inteiras no sentido em que o Kvantum estica (pixel solto deixa emenda)
        if all(len({px[x, y] for y in range(h)}) == 1 for x in range(w)):
            return [(x, 0, 1, h, px[x, 0]) for x in range(w)]
        if all(len({px[x, y] for x in range(w)}) == 1 for y in range(h)):
            return [(0, y, w, 1, px[0, y]) for y in range(h)]
        return [(x, y, 1, 1, c) for (x, y), c in sorted(px.items())]
    e = n - B
    return {"": [(0, 0, M, M, fill)],
            "-top": area(B, 0, M, B), "-bottom": area(B, e, M, B),
            "-left": area(0, B, B, M), "-right": area(e, B, B, M),
            "-topleft": area(0, 0, B, B), "-topright": area(e, 0, B, B),
            "-bottomleft": area(0, e, B, B), "-bottomright": area(e, e, B, B)}


STATES = ("normal", "focused", "pressed", "toggled", "disabled")

svg = SVG.read_text()
svg = re.sub(r'<g id="slider-[a-z-]+">.*?</g>\n?', "", svg)
m = re.search(r'<!-- slider98-top=(\d+) -->', svg)
height = int(re.search(r'<svg [^>]*height="(\d+)"', svg).group(1))
top = int(m.group(1)) if m else height
out = [] if m else [f"<!-- slider98-top={top} -->"]
y = top
for st in STATES:
    for suffix in ("", "-inactive"):
        x = 0
        for part, rects in pieces(FRAME).items():
            name = f"slider-{st}{suffix}{part}"
            body = "".join(f'<rect x="{x + rx}" y="{y + ry}" width="{w}" height="{h}" fill="{c}"/>'
                           for rx, ry, w, h, c in rects)
            out.append(f'<g id="{name}">{body}</g>')
            x += 10
        y += 10
svg = re.sub(r'(<svg [^>]*height=")\d+(")', rf"\g<1>{max(height, y)}\2", svg, count=1)
svg = svg.replace("</svg>", "\n".join(out) + "\n</svg>") if out else svg
SVG.write_text(svg)

cfg = CFG.read_text()
novo = ("[Slider]\nframe=true\nframe.element=slider\nframe.top=2\nframe.bottom=2\nframe.left=2\n"
        "frame.right=2\ninterior=true\ninterior.element=slider\n")
cfg = re.sub(r"\[Slider\]\n.*?(?=\n\[)", novo, cfg, count=1, flags=re.S)
# marcador do 98: em pé, 11 de largo por 22 de alto (no Kvantum "width" é a altura no deslizante
# horizontal e "length" é a largura)
cfg = re.sub(r"^slider_handle_width=.*$", "slider_handle_width=22", cfg, count=1, flags=re.M)
cfg = re.sub(r"^slider_handle_length=.*$", "slider_handle_length=11", cfg, count=1, flags=re.M)
CFG.write_text(cfg)
print(f"trilho do deslizante gerado ({len(STATES) * 2} estados); [Slider] usa slider")
