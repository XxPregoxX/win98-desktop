#!/usr/bin/env python3
"""Gera os botões [_][□][X] da barra de título (Aurorae: temas/aurorae/Win98/*.svg), pixel a pixel.

Antes eram desenhos de 16x16 mostrados em 22x20 (ButtonWidth/ButtonHeight do Win98rc): o KWin
ampliava, e o relevo e o X (feito com traço diagonal) saíam borrados. Agora cada botão tem
exatamente 22x20 e só retângulos de 1px: nada é ampliado nem suavizado, como no 98.
- relevo: o do botão do 98.css (fora: branco em cima/esquerda, preto embaixo/direita; dentro:
  #dfdfdf e cinza), invertido quando apertado;
- símbolos: os do 98.css (icon/minimize, maximize, restore, close), no tamanho original (1 pixel do
  desenho = 1 pixel da tela), na mesma posição relativa do 98.css;
- apertado: símbolo 1px pra direita e pra baixo; desativado: símbolo cinza com sombra branca.
Rodar de novo é seguro. Depois rodar gen_titlebar_icons.py (os ícones window-* copiam estes botões).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "temas/aurorae/Win98"
W, H = 22, 20  # ButtonWidth x ButtonHeight do Win98rc
WHITE, LIGHT, FACE, SHADOW, DARK = "#ffffff", "#dfdfdf", "#c0c0c0", "#808080", "#000000"

# símbolos do 98.css, em pixels
SIMBOLOS = {
    "close": ["##....##", ".##..##.", "..####..", "...##...", "..####..", ".##..##.", "##....##"],
    "minimize": ["######", "######"],
    "maximize": ["#########", "#########"] + ["#.......#"] * 6 + ["#########"],
    "restore": ["..######", "..######", "..#....#", "######.#", "######.#",
                "#....###", "#....#..", "#....#..", "#####..."],
}
# canto de cima/esquerda do símbolo no botão de 22x20 (centralizado; o [_] fica embaixo,
# com 1 linha de folga até o relevo, como no 98.css)
POSICAO = {"close": (7, 6), "minimize": (7, 15), "maximize": (6, 5), "restore": (7, 5)}


def relevo(afundado):
    fora_cl, dentro_cl, dentro_es, fora_es = (DARK, SHADOW, LIGHT, WHITE) if afundado \
        else (WHITE, LIGHT, SHADOW, DARK)
    r = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{FACE}"/>']
    # ordem do box-shadow do 98.css: o que vem por último fica por cima
    r += [f'<rect x="1" y="1" width="{W - 2}" height="1" fill="{dentro_cl}"/>',
          f'<rect x="1" y="1" width="1" height="{H - 2}" fill="{dentro_cl}"/>',
          f'<rect x="1" y="{H - 2}" width="{W - 2}" height="1" fill="{dentro_es}"/>',
          f'<rect x="{W - 2}" y="1" width="1" height="{H - 2}" fill="{dentro_es}"/>',
          f'<rect x="0" y="0" width="{W}" height="1" fill="{fora_cl}"/>',
          f'<rect x="0" y="0" width="1" height="{H}" fill="{fora_cl}"/>',
          f'<rect x="0" y="{H - 1}" width="{W}" height="1" fill="{fora_es}"/>',
          f'<rect x="{W - 1}" y="0" width="1" height="{H}" fill="{fora_es}"/>']
    return r


def simbolo(nome, x0, y0, cor):
    return [f'<rect x="{x0 + x}" y="{y0 + y}" width="1" height="1" fill="{cor}"/>'
            for y, linha in enumerate(SIMBOLOS[nome]) for x, c in enumerate(linha) if c == "#"]


def botao(nome):
    x, y = POSICAO[nome]
    estados = {
        "active": relevo(False) + simbolo(nome, x, y, DARK),
        "inactive": relevo(False) + simbolo(nome, x, y, DARK),
        "hover": relevo(False) + simbolo(nome, x, y, DARK),
        "pressed": relevo(True) + simbolo(nome, x + 1, y + 1, DARK),
        # desativado (ex.: maximizar numa janela de tamanho fixo): cinza com sombra branca
        "deactivated": relevo(False) + simbolo(nome, x + 1, y + 1, WHITE) + simbolo(nome, x, y, SHADOW),
    }
    partes = [f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
              f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" version="1.1">']
    for estado, rects in estados.items():
        partes.append(f'<g id="{estado}-center">' + "".join(rects) + "</g>")
    partes.append("</svg>")
    (DIR / f"{nome}.svg").write_text("\n".join(partes) + "\n")


for n in SIMBOLOS:
    botao(n)
print(f"botões da barra de título gerados ({W}x{H}, pixel a pixel): " + ", ".join(SIMBOLOS))
