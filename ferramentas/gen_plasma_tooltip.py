#!/usr/bin/env python3
"""Gera temas/plasma/Win98/widgets/tooltip.svg: a dica do 98 (amarelo #ffffe1, borda preta de
1px, cantos retos, sem sombra) pra todas as dicas do Plasma, inclusive a das miniaturas da
barra de tarefas. Margem do conteúdo = a do Breeze (4px), pra nada mudar de tamanho.
Também ligado em opaque/, solid/ e translucent/.
"""
from pathlib import Path

THEME = Path(__file__).resolve().parent.parent / "temas/plasma/Win98"
FILL, BORDER = "#ffffe1", "#000000"
C = 8   # miolo dos pedaços de exemplo
M = 4   # margem do conteúdo

pieces = {
    "topleft": (1, 1, BORDER), "top": (C, 1, BORDER), "topright": (1, 1, BORDER),
    "left": (1, C, BORDER), "center": (C, C, FILL), "right": (1, C, BORDER),
    "bottomleft": (1, 1, BORDER), "bottom": (C, 1, BORDER), "bottomright": (1, 1, BORDER),
}
body, y = [], 0
for name, (w, h, color) in pieces.items():
    body.append(f'<rect id="{name}" x="0" y="{y}" width="{w}" height="{h}" fill="{color}"/>')
    y += h + 2
for side in ("left", "top", "right", "bottom"):
    w, h = (M, 1) if side in ("left", "right") else (1, M)
    body.append(f'<rect id="hint-{side}-margin" x="0" y="{y}" width="{w}" height="{h}" fill="none"/>')
    y += h + 2

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="20" height="{y + 4}" version="1.1">\n'
       + "\n".join(body) + "\n</svg>\n")
rel = "widgets/tooltip.svg"
(THEME / rel).write_text(svg)
for variant in ("opaque", "solid", "translucent"):
    link = THEME / variant / rel
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(Path("../../") / rel)
print("gerado:", THEME / rel, "(e links em opaque/solid/translucent)")
