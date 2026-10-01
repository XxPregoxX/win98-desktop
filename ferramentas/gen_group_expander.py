#!/usr/bin/env python3
"""Gera os elementos group-expander-{bottom,top,left,right} em temas/plasma/Win98/widgets/tasks.svg.

É a setinha que a barra de tarefas mostra quando um app tem mais de uma janela (grupo).
Desenho: a seta preta do Win98 (7x4 px, a mesma dos combos e barras de rolagem), com contorno
cinza de 1px pra destacar sobre o ícone, apontando pro lado em que a lista de janelas abre.
A folga transparente afasta a seta da borda em relevo do botão.
Rodar de novo é seguro: substitui os elementos gerados antes.
"""
import re
from pathlib import Path

SVG = Path(__file__).resolve().parent.parent / "temas/plasma/Win98/widgets/tasks.svg"
FACE, INK = "#c0c0c0", "#000000"
GAP = 3  # folga até a borda do botão (relevo de 2px + 1px)
X0 = 30  # coluna livre do SVG onde os elementos ficam

# Seta ▲ num quadro 9x6: ponta em y=1, base (7px) em y=4.
glyph = {(4 - d + i, 1 + d) for d in range(4) for i in range(2 * d + 1)}
outline = {(x + dx, y + dy) for x, y in glyph for dx in (-1, 0, 1) for dy in (-1, 0, 1)} - glyph
W, H = 9, 6


def rotate(pts, edge):
    """Converte a seta ▲ (painel embaixo) pra orientação de cada borda, com a folga do lado da borda."""
    out = []
    for x, y in pts:
        if edge == "bottom":    # ▲, folga embaixo
            out.append((x, y))
        elif edge == "top":     # ▼, folga em cima
            out.append((x, H - 1 - y + GAP))
        elif edge == "left":    # ▶, folga à esquerda
            out.append((H - 1 - y + GAP, x))
        elif edge == "right":   # ◀, folga à direita
            out.append((y, x))
    return out


def element(edge, oy):
    w, h = (W, H + GAP) if edge in ("bottom", "top") else (H + GAP, W)
    rects = [f'<rect x="{X0}" y="{oy}" width="{w}" height="{h}" fill="none"/>']
    for color, pts in ((FACE, outline), (INK, glyph)):
        rects += [f'<rect x="{X0 + x}" y="{oy + y}" width="1" height="1" fill="{color}"/>'
                  for x, y in sorted(rotate(pts, edge))]
    return f'<g id="group-expander-{edge}">' + "".join(rects) + "</g>", h


svg = SVG.read_text()
svg = re.sub(r'<g id="group-expander-[a-z]+">.*?</g>\n?', "", svg)
parts, oy = [], 0
for edge in ("bottom", "top", "left", "right"):
    g, h = element(edge, oy)
    parts.append(g)
    oy += h + 2
svg = svg.replace("</svg>", "\n".join(parts) + "\n</svg>")
SVG.write_text(svg)
print(f"{SVG}: 4 elementos group-expander gerados")
