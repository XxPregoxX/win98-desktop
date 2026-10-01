#!/usr/bin/env python3
"""Gera temas/plasma/Win98/widgets/button.svg: os botões do Plasma com o relevo do 98.css.

Prefixos (os mesmos do Breeze, com as MESMAS margens, pra nenhum botão mudar de tamanho):
- normal: botão em relevo (button do 98.css). pressed: afundado (button:active), e a margem
  muda 1px pra direita/baixo, então o texto desce 1px ao clicar, como no 98.
- hover: vazio (no 98 botão não acendia). focus: borda preta de 1px em volta (botão em foco
  do 98). shadow: vazio.
- toolbutton-hover: vazio (os botões "chapados", tipo o X da notificação, não ganham mais o
  contorno azul do Breeze). toolbutton-pressed: afundado fino (barra de ferramentas do 98).
  toolbutton-focus: vazio.
Folga em cima (GAP): a moldura do botão em relevo (normal/pressed/focus) começa com 4px
transparentes, e a margem de cima cresce junto. O botão fica 4px mais alto, mas a parte visível é
a mesma. É o único jeito de dar espaço entre a imagem e os botões de ação da notificação: a grade
da notificação tem rowSpacing 0 e o bloco dos botões não tem margem (código do KDE).
Também ligado em opaque/, solid/ e translucent/.
"""
from pathlib import Path

THEME = Path(__file__).resolve().parent.parent / "temas/plasma/Win98"
FACE, LIGHT, WHITE, SHADOW, FRAME = "#c0c0c0", "#dfdfdf", "#ffffff", "#808080", "#0a0a0a"
C = 8   # miolo dos pedaços de exemplo
GAP = 4 # folga transparente em cima dos botões em relevo (ver acima)

RAISED = [(WHITE, FRAME), (LIGHT, SHADOW)]    # anéis de fora pra dentro: (cima/esquerda, baixo/direita)
SUNKEN = [(FRAME, WHITE), (SHADOW, LIGHT)]
THIN_SUNKEN = [(SHADOW, WHITE)]
BLACK_RING = [(FRAME, FRAME)]


def ring_pixel(x, y, n, rings):
    """Anel k = distância até a borda; no anel, baixo/direita cobre cima/esquerda (como a
    ordem das sombras do 98.css)."""
    k = min(x, y, n - 1 - x, n - 1 - y)
    if k >= len(rings):
        return None
    tl, br = rings[k]
    return br if (x == n - 1 - k or y == n - 1 - k) else tl


def frame(prefix, rings, center, gap=0):
    """Os 9 pedaços do FrameSvg; rings=[] ou center=None dão pedaços transparentes.
    gap: linhas transparentes em cima dos pedaços de cima (o desenho começa mais abaixo)."""
    b = max(len(rings), 1)
    n = 2 * b + C

    def area(x0, y0, w, h):
        pix = {(x, y): ring_pixel(x0 + x, y0 + y, n, rings) for x in range(w) for y in range(h)}
        if all(v is None for v in pix.values()):
            return [(0, 0, w, h, "none")]
        # faixas inteiras no sentido em que o FrameSvg repete o pedaço (pixel solto deixa emenda)
        if all(len({pix[x, y] for y in range(h)}) == 1 for x in range(w)):
            return [(x, 0, 1, h, pix[x, 0] or "none") for x in range(w)]
        if all(len({pix[x, y] for x in range(w)}) == 1 for y in range(h)):
            return [(0, y, w, 1, pix[0, y] or "none") for y in range(h)]
        return [(x, y, 1, 1, c or "none") for (x, y), c in sorted(pix.items())]

    e = n - b
    parts = {
        "topleft": area(0, 0, b, b), "top": area(b, 0, C, b), "topright": area(e, 0, b, b),
        "left": area(0, b, b, C), "right": area(e, b, b, C),
        "bottomleft": area(0, e, b, b), "bottom": area(b, e, C, b), "bottomright": area(e, e, b, b),
        "center": [(0, 0, C, C, center or "none")],
    }
    if gap:
        for k in ("topleft", "top", "topright"):
            w = max(rx + rw for rx, ry, rw, rh, c in parts[k])
            parts[k] = [(0, 0, w, gap, "none")] + [(rx, ry + gap, rw, rh, c) for rx, ry, rw, rh, c in parts[k]]
    return {f"{prefix}-{k}": v for k, v in parts.items()}


# prefixo: (anéis, miolo, margens esquerda/cima/direita/baixo)
PREFIXES = {
    "normal": (RAISED, FACE, (6, 6 + GAP, 6, 6)),
    "pressed": (SUNKEN, FACE, (7, 7 + GAP, 5, 5)),
    "hover": ([], None, (0, 0, 0, 0)),
    "focus": (BLACK_RING, None, (1, 1, 1, 1)),
    "shadow": ([], None, (0, 0, 0, 0)),
    "toolbutton-hover": ([], None, (4, 4, 4, 4)),
    "toolbutton-pressed": (THIN_SUNKEN, None, (4, 4, 4, 4)),
    "toolbutton-focus": ([], None, (2, 2, 2, 2)),
}

body, y = [], 0
COM_GAP = ("normal", "pressed", "focus")
for prefix, (rings, center, (ml, mt, mr, mb)) in PREFIXES.items():
    for name, rects in frame(prefix, rings, center, GAP if prefix in COM_GAP else 0).items():
        w = max(rx + rw for rx, ry, rw, rh, c in rects)
        h = max(ry + rh for rx, ry, rw, rh, c in rects)
        rs = "".join(f'<rect x="{rx}" y="{y + ry}" width="{rw}" height="{rh}" fill="{c}"/>'
                     for rx, ry, rw, rh, c in rects)
        body.append(f'<g id="{name}">{rs}</g>')
        y += h + 2
    # margens do conteúdo: largura (esquerda/direita) ou altura (cima/baixo) destes retângulos
    for side, size in (("left", ml), ("top", mt), ("right", mr), ("bottom", mb)):
        w, h = (size, 1) if side in ("left", "right") else (1, size)
        if size:
            body.append(f'<rect id="{prefix}-hint-{side}-margin" x="0" y="{y}" width="{w}" height="{h}" fill="none"/>')
            y += h + 2

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="40" height="{y + 10}" version="1.1">\n'
       + "\n".join(body) + "\n</svg>\n")

rel = "widgets/button.svg"
(THEME / rel).write_text(svg)
for variant in ("opaque", "solid", "translucent"):
    link = THEME / variant / rel
    link.parent.mkdir(parents=True, exist_ok=True)
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(Path("../../") / rel)
print("gerado:", THEME / rel, "(e links em opaque/solid/translucent)")
