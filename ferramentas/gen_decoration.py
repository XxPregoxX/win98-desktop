#!/usr/bin/env python3
# Gera a decoracao Aurorae "Win98" com medidas batendo com o que o KWin reserva:
# laterais/base 5px, topo 26px (2 bevel + 2 face + barra de 22px; botões 22x20 do gen_aurorae_buttons.py).
import os, sys

S, B, T = 5, 5, 26          # lateral, base, topo
CAP_Y, CAP_H, CAP_X = 4, 22, 4   # barra: comeca na linha 4, 22px, recuada 4px das bordas
M, MID = 90, 60             # largura/altura das pecas esticaveis (tanto faz, sao esticadas)
LT_OUT, LT_IN, BR_OUT, BR_IN, FACE = "#dfdfdf", "#ffffff", "#000000", "#808080", "#c0c0c0"
CAPTIONS = {"": ("#000080", "#1084d0"), "-inactive": ("#808080", "#c0c0c0")}

out = []
def rect(x, y, w, h, fill):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>')

def group(elem_id, ox, oy, paint):
    out.append(f'<g id="{elem_id}">'); paint(ox, oy); out.append('</g>')

def frame(prefix, ox, oy, grad_id, cap_start, cap_end):
    # camadas pintadas de baixo pra cima: face, brilho interno, sombra interna, brilho externo, sombra externa
    def topleft(x, y):
        rect(x, y, S, T, FACE)
        rect(x + CAP_X, y + CAP_Y, S - CAP_X, CAP_H, cap_start)
        rect(x + 1, y + 1, S - 1, 1, LT_IN); rect(x + 1, y + 1, 1, T - 1, LT_IN)
        rect(x, y, S, 1, LT_OUT); rect(x, y, 1, T, LT_OUT)
    def top(x, y):
        rect(x, y, M, T, FACE)
        rect(x, y + CAP_Y, M, CAP_H, f"url(#{grad_id})")
        rect(x, y + 1, M, 1, LT_IN); rect(x, y, M, 1, LT_OUT)
    def topright(x, y):
        rect(x, y, S, T, FACE)
        rect(x, y + CAP_Y, S - CAP_X, CAP_H, cap_end)
        rect(x, y + 1, S, 1, LT_IN)
        rect(x + S - 2, y + 1, 1, T - 1, BR_IN)
        rect(x, y, S, 1, LT_OUT)
        rect(x + S - 1, y, 1, T, BR_OUT)
    def left(x, y):
        rect(x, y, S, MID, FACE); rect(x + 1, y, 1, MID, LT_IN); rect(x, y, 1, MID, LT_OUT)
    def right(x, y):
        rect(x, y, S, MID, FACE); rect(x + S - 2, y, 1, MID, BR_IN); rect(x + S - 1, y, 1, MID, BR_OUT)
    def center(x, y):
        rect(x, y, M, MID, FACE)  # opaco: nenhuma fresta transparente, mesmo com arredondamento
    def bottomleft(x, y):
        rect(x, y, S, B, FACE)
        rect(x + 1, y, 1, B, LT_IN); rect(x, y + B - 2, S, 1, BR_IN)
        rect(x, y, 1, B, LT_OUT); rect(x, y + B - 1, S, 1, BR_OUT)
    def bottom(x, y):
        rect(x, y, M, B, FACE); rect(x, y + B - 2, M, 1, BR_IN); rect(x, y + B - 1, M, 1, BR_OUT)
    def bottomright(x, y):
        rect(x, y, S, B, FACE)
        rect(x, y + B - 2, S, 1, BR_IN); rect(x + S - 2, y, 1, B, BR_IN)
        rect(x, y + B - 1, S, 1, BR_OUT); rect(x + S - 1, y, 1, B, BR_OUT)
    for name, dx, dy, fn in (("topleft", 0, 0, topleft), ("top", S, 0, top), ("topright", S + M, 0, topright),
                             ("left", 0, T, left), ("center", S, T, center), ("right", S + M, T, right),
                             ("bottomleft", 0, T + MID, bottomleft), ("bottom", S, T + MID, bottom),
                             ("bottomright", S + M, T + MID, bottomright)):
        group(f"{prefix}-{name}", ox + dx, oy + dy, lambda x, y, fn=fn: fn(x, y))

defs = []
for suffix, (a, b) in CAPTIONS.items():
    gid = "caption" + suffix
    defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
                f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')

H = T + MID + B
frame("decoration", 0, 0, "caption", *CAPTIONS[""])
frame("decoration-inactive", 0, H + 10, "caption-inactive", *CAPTIONS["-inactive"])
# maximizada: o Aurorae desenha so o "center" esticado na faixa da barra (sem moldura)
group("decoration-maximized-center", 110, 0, lambda x, y: rect(x, y, 60, CAP_H, "url(#caption)"))
group("decoration-maximized-inactive-center", 110, 30, lambda x, y: rect(x, y, 60, CAP_H, "url(#caption-inactive)"))
# dicas do FrameSvg: esticar bordas (senao o degrade e ladrilhado) + margens do conteudo
out.append('<rect id="hint-stretch-borders" x="110" y="60" width="1" height="1" fill="none"/>')
out.append(f'<rect id="hint-top-margin" x="180" y="0" width="1" height="{T}" fill="none"/>')
out.append(f'<rect id="hint-bottom-margin" x="182" y="0" width="1" height="{B}" fill="none"/>')
out.append(f'<rect id="hint-left-margin" x="184" y="0" width="{S}" height="1" fill="none"/>')
out.append(f'<rect id="hint-right-margin" x="184" y="4" width="{S}" height="1" fill="none"/>')

svg = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       f'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="{2 * H + 10}" shape-rendering="crispEdges">\n'
       '<defs>' + "".join(defs) + '</defs>\n' + "\n".join(out) + '\n</svg>\n')
dest = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.local/share/aurorae/themes/Win98/decoration.svg")
open(dest, "w").write(svg)
print("escrito:", dest, len(svg), "bytes")
