#!/usr/bin/env python3
"""Gera os botões [_][□][X] da barra de título (Aurorae: temas/aurorae/Win98/*.svg).

O botão é o do 98.css (16x14, .title-bar-controls button) com os símbolos do 98.css, os mesmos
de gen_titlebar_icons.py, ampliado 2x pixel a pixel: cada pixel do 98 vira um quadrado de 2x2,
então fica nítido e do tamanho de uma tela de hoje (32x28; ButtonWidth/ButtonHeight do Win98rc).
Antes eram desenhos de 16x16 esticados pelo KWin pra 22x20, borrados; e no tamanho original (1x)
os símbolos ficavam miúdos.
Estados: normal (active/inactive/hover iguais, como no 98); apertado = relevo invertido e o
símbolo 1 pixel do 98 pra direita e pra baixo; desativado = símbolo cinza com sombra branca.
Rodar de novo é seguro. As medidas da barra de título que comportam estes botões estão em
gen_decoration.py e no Win98rc.
"""
from pathlib import Path

from gen_titlebar_icons import GLYPHS

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "temas/aurorae/Win98"
ESCALA = 2                     # 1 pixel do 98 = ESCALA x ESCALA pixels na tela
BW, BH = 16, 14                # botão do 98.css
WHITE, LIGHT, FACE, SHADOW, FRAME, BLACK = "#ffffff", "#dfdfdf", "#c0c0c0", "#808080", "#0a0a0a", "#000000"
ARQUIVO = {"window-close": "close", "window-minimize": "minimize",
           "window-maximize": "maximize", "window-restore": "restore"}


def botao16(glyph, gx, gy, apertado=False, desativado=False):
    """grade 16x14 de cores: relevo do 98.css (invertido se apertado) + símbolo"""
    g = [[FACE] * BW for _ in range(BH)]
    fora_cl, dentro_cl, dentro_es, fora_es = (FRAME, SHADOW, LIGHT, WHITE) if apertado \
        else (WHITE, LIGHT, SHADOW, FRAME)
    for y in range(BH):
        for x in range(BW):
            if x == BW - 1 or y == BH - 1:
                g[y][x] = fora_es
            elif x == 0 or y == 0:
                g[y][x] = fora_cl
            elif x == BW - 2 or y == BH - 2:
                g[y][x] = dentro_es
            elif x == 1 or y == 1:
                g[y][x] = dentro_cl
    d = 1 if apertado else 0

    def pinta(dx, dy, cor):
        for j, linha in enumerate(glyph):
            for i, c in enumerate(linha):
                if c == "#":
                    g[gy + j + dy][gx + i + dx] = cor
    if desativado:
        pinta(1, 1, WHITE)
        pinta(0, 0, SHADOW)
    else:
        pinta(d, d, BLACK)
    return g


def rects(grade):
    """grade -> retângulos ampliados ESCALA x, juntando pixels iguais em sequência na linha"""
    out = []
    for y, linha in enumerate(grade):
        x = 0
        while x < len(linha):
            fim = x
            while fim + 1 < len(linha) and linha[fim + 1] == linha[x]:
                fim += 1
            out.append(f'<rect x="{x * ESCALA}" y="{y * ESCALA}" width="{(fim - x + 1) * ESCALA}" '
                       f'height="{ESCALA}" fill="{linha[x]}"/>')
            x = fim + 1
    return "".join(out)


for nome, (glyph, gx, gy) in GLYPHS.items():
    normal = rects(botao16(glyph, gx, gy))
    estados = {"active": normal, "inactive": normal, "hover": normal,
               "pressed": rects(botao16(glyph, gx, gy, apertado=True)),
               "deactivated": rects(botao16(glyph, gx, gy, desativado=True))}
    w, h = BW * ESCALA, BH * ESCALA
    svg = [f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
           f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" version="1.1" shape-rendering="crispEdges">']
    svg += [f'<g id="{e}-center">{r}</g>' for e, r in estados.items()]
    svg.append("</svg>")
    (DIR / f"{ARQUIVO[nome]}.svg").write_text("\n".join(svg) + "\n")
print(f"botões da barra de título: {BW * ESCALA}x{BH * ESCALA} (98.css em {ESCALA}x)")
