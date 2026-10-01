#!/usr/bin/env python3
"""Gera o desenho dos itens de lista do Kvantum ([ItemView] em temas/kvantum/Win98/).

O Kvantum não desenha nada no item em estado normal (é regra dele). Nos outros estados:
- focused (mouse em cima): campo afundado branco, o "afundar" escolhido pro tema;
- pressed/toggled (selecionado, com ou sem foco): azul-marinho chapado, como a seleção do 98,
  pra o texto branco da seleção aparecer (antes era branco no branco).
Cada estado também tem a versão "-inactive" (janela sem foco), igual à ativa.
A borda afundada segue o --border-field do 98.css (a mesma das caixas de marcar).
Rodar de novo é seguro: substitui tudo o que for itemview-*.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "temas/kvantum/Win98/Win98.svg"
CFG = ROOT / "temas/kvantum/Win98/Win98.kvconfig"
WHITE, LIGHT, SHADOW, FRAME, NAVY = "#ffffff", "#dfdfdf", "#808080", "#0a0a0a", "#000080"
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


def pieces(sunken, fill):
    """Os 9 pedaços que o Kvantum espera, como listas de (x, y, w, h, cor) relativas."""
    n = 2 * B + M
    def area(x0, y0, w, h):
        px = {(x, y): (field_pixel(x0 + x, y0 + y, n) if sunken else fill) or fill
              for x in range(w) for y in range(h)}
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


STATES = {"focused": (True, WHITE), "pressed": (False, NAVY), "toggled": (False, NAVY)}

svg = SVG.read_text()
svg = re.sub(r'<(?:g|rect) id="itemview-[a-z-]+"[^>]*?(?:/>|>.*?</g>)\n?', "", svg)
svg = re.sub(r'<!-- itemview98 y=\d+ -->\n?', "", svg)
m = re.search(r'<!-- itemview98-top=(\d+) -->', svg)
height = int(re.search(r'<svg [^>]*height="(\d+)"', svg).group(1))
top = int(m.group(1)) if m else height
out = [] if m else [f"<!-- itemview98-top={top} -->"]
y = top
for st, (sunken, fill) in STATES.items():
    for suffix in ("", "-inactive"):
        x = 0
        for part, rects in pieces(sunken, fill).items():
            name = f"itemview-{st}{suffix}" if not part else f"itemview-{st}{suffix}{part}"
            body = "".join(f'<rect x="{x + rx}" y="{y + ry}" width="{w}" height="{h}" fill="{c}"/>'
                           for rx, ry, w, h, c in rects)
            out.append(f'<g id="{name}">{body}</g>')
            x += 10
        y += 10
svg = re.sub(r'(<svg [^>]*height=")\d+(")', rf"\g<1>{max(height, y)}\2", svg, count=1)
svg = svg.replace("</svg>", "\n".join(out) + "\n</svg>") if out else svg
SVG.write_text(svg)

cfg = CFG.read_text()
body = re.search(r"\[ItemView\]\n(.*?)(?=\n\[|\Z)", cfg, re.S).group(1)
new = re.sub(r"^(frame|interior)\.element=.*$", r"\1.element=itemview", body, flags=re.M)
cfg = cfg.replace(f"[ItemView]\n{body}", f"[ItemView]\n{new}", 1)
CFG.write_text(cfg)
print(f"itemview gerado ({len(STATES) * 2} estados); [ItemView] usa itemview")
