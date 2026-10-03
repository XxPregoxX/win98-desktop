#!/usr/bin/env python3
"""Gera os botões [_][□][X] da barra de título (Aurorae: temas/aurorae/Win98/*.svg), pixel a pixel.

Tamanho: 22x20 (ButtonWidth/ButtonHeight do Win98rc), ~1,4x o botão 16x14 do 98. No 98, num CRT
de 800x600/1024x768 (70-90 pixels por polegada), o botão tinha ~5-6 mm; numa tela de hoje
(~110 ppp) o 16x14 original fica miúdo e o dobro (32x28) fica grande demais. 1,4x não é inteiro,
então nada é esticado: como o Windows fazia quando a barra de título crescia, os símbolos são
REDESENHADOS no tamanho do botão (X de traço grosso em degraus, caixa de topo grosso, as duas
janelas do "restaurar", a barra do "minimizar"), sempre em pixel inteiro, sem suavização.
- relevo: o do botão do 98.css, 1px por cor (fora: branco em cima/esquerda, preto embaixo/direita;
  dentro: #dfdfdf e cinza), invertido quando apertado;
- apertado: símbolo 1px pra direita e pra baixo; desativado: símbolo cinza com sombra branca.
Antes: desenhos de 16x16 esticados pelo KWin pra 22x20 (borrados). Rodar de novo é seguro; depois
rodar gen_titlebar_icons.py (os ícones window-* de 22/24 copiam estes botões).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "temas/aurorae/Win98"
W, H = 22, 20
WHITE, LIGHT, FACE, SHADOW, FRAME, BLACK = "#ffffff", "#dfdfdf", "#c0c0c0", "#808080", "#0a0a0a", "#000000"


def caixa(w, h, topo):
    """janela de w x h com a borda de cima de 'topo' px (como o [□] do 98)"""
    return [["#" if (y < topo or y == h - 1 or x == 0 or x == w - 1) else "." for x in range(w)]
            for y in range(h)]


def restaurar(w, h, topo, d):
    """duas janelas: a de trás deslocada d px pra direita e pra cima, a da frente por cima dela"""
    g = [["."] * (w + d) for _ in range(h + d)]
    tras, frente = caixa(w, h, topo), caixa(w, h, topo)
    for y in range(h):
        for x in range(w):
            g[y][x + d] = tras[y][x]
    for y in range(h):              # a da frente cobre a de trás
        for x in range(w):
            g[y + d][x] = frente[y][x]
    return g


SIMBOLOS = {
    "close": [list(l) for l in ["##......##", "###....###", ".###..###.", "..######..", "...####...",
                                 "..######..", ".###..###.", "###....###", "##......##"]],
    "minimize": [list("########")] * 3,
    "maximize": caixa(12, 11, 3),
    "restore": restaurar(9, 8, 2, 3),
}
# canto de cima/esquerda do símbolo (centralizado; o [_] embaixo, 1 linha acima do relevo)
POSICAO = {n: ((W - len(g[0])) // 2, (H - len(g)) // 2) for n, g in SIMBOLOS.items()}
POSICAO["minimize"] = ((W - 8) // 2, H - 2 - 1 - 3)


def botao(nome, apertado=False, desativado=False):
    g = [[FACE] * W for _ in range(H)]
    fora_cl, dentro_cl, dentro_es, fora_es = (FRAME, SHADOW, LIGHT, WHITE) if apertado \
        else (WHITE, LIGHT, SHADOW, FRAME)
    for y in range(H):
        for x in range(W):
            if x == W - 1 or y == H - 1:
                g[y][x] = fora_es
            elif x == 0 or y == 0:
                g[y][x] = fora_cl
            elif x == W - 2 or y == H - 2:
                g[y][x] = dentro_es
            elif x == 1 or y == 1:
                g[y][x] = dentro_cl
    gx, gy = POSICAO[nome]

    def pinta(dx, dy, cor):
        for j, linha in enumerate(SIMBOLOS[nome]):
            for i, c in enumerate(linha):
                if c == "#":
                    g[gy + j + dy][gx + i + dx] = cor
    if desativado:
        pinta(1, 1, WHITE)
        pinta(0, 0, SHADOW)
    else:
        d = 1 if apertado else 0
        pinta(d, d, BLACK)
    return g


def rects(grade):
    """grade -> retângulos de 1px de altura, juntando pixels iguais em sequência"""
    out = []
    for y, linha in enumerate(grade):
        x = 0
        while x < len(linha):
            fim = x
            while fim + 1 < len(linha) and linha[fim + 1] == linha[x]:
                fim += 1
            out.append(f'<rect x="{x}" y="{y}" width="{fim - x + 1}" height="1" fill="{linha[x]}"/>')
            x = fim + 1
    return "".join(out)


for nome in SIMBOLOS:
    normal = rects(botao(nome))
    estados = {"active": normal, "inactive": normal, "hover": normal,
               "pressed": rects(botao(nome, apertado=True)),
               "deactivated": rects(botao(nome, desativado=True))}
    svg = [f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
           f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" version="1.1" shape-rendering="crispEdges">']
    svg += [f'<g id="{e}-center">{r}</g>' for e, r in estados.items()]
    svg.append("</svg>")
    (DIR / f"{nome}.svg").write_text("\n".join(svg) + "\n")
print(f"botões da barra de título: {W}x{H}, símbolos redesenhados em pixel inteiro")
