#!/usr/bin/env python3
"""Ícones window-close/-minimize/-maximize/-restore = botões da barra de título do 98.

Os packs só têm o símbolo preto, sem o botão (em fundo azul, como na notificação, some).
Aqui vira o botão cinza em relevo do 98.css (.title-bar-controls button, 16x14) com o
desenho dele (icon/close.svg, minimize.svg, maximize.svg, restore.svg) na posição do CSS.
Tamanhos: 16 = botão 16x14 do 98.css; 22/24 = o botão da barra de título (Aurorae, 22x20,
gen_aurorae_buttons.py), copiado pixel a pixel: é o tamanho que botão "chapado" do Plasma usa
(X da notificação), e fica igual à barra de título; 32/48 = o de 16 ampliado 2x/3x pixel a pixel.
Grava em terceiros/Chicago95/actions/<tam>/ (substitui links). Rodar de novo se reinstalar
o Chicago95.

Os nomes window-*-symbolic têm que continuar só o símbolo: quem pede eles (o Firefox, apps GTK)
desenha o botão por conta própria, e o GTK recolore o .symbolic.png canal por canal (o botão
cinza virava um quadrado verde). O Chicago95 tinha links window-*-symbolic.symbolic.png pro
window-*.png; aqui eles são apagados e o nome cai no SE98, que tem o símbolo do 98 em todos os
tamanhos.
"""
from pathlib import Path
from PIL import Image

C95 = Path(__file__).resolve().parent.parent / "terceiros/Chicago95/actions"
FACE, LIGHT, WHITE, SHADOW, FRAME = (192, 192, 192), (223, 223, 223), (255, 255, 255), (128, 128, 128), (10, 10, 10)
BLACK = (0, 0, 0)

# desenhos do 98.css como linhas de pixels, e a posição dentro do botão 16x14
GLYPHS = {
    "window-close": (["##....##",
                      ".##..##.",
                      "..####..",
                      "...##...",
                      "..####..",
                      ".##..##.",
                      "##....##"], 4, 3),
    "window-minimize": (["######",
                         "######"], 4, 14 - 3 - 2),
    "window-maximize": (["#########",
                         "#########",
                         "#.......#",
                         "#.......#",
                         "#.......#",
                         "#.......#",
                         "#.......#",
                         "#.......#",
                         "#########"], 3, 2),
    "window-restore": (["..######",
                        "..######",
                        "..#....#",
                        "######.#",
                        "######.#",
                        "#....###",
                        "#....#..",
                        "#....#..",
                        "######.."], 3, 2),
}


def button(glyph, gx, gy):
    """Botão 16x14 com o box-shadow do 98.css (--border-raised-outer/inner)."""
    im = Image.new("RGBA", (16, 14), FACE)
    px = im.load()
    for x in range(16):
        for y in range(14):
            if x == 15 or y == 13:
                c = FRAME          # -1 -1 moldura
            elif x == 0 or y == 0:
                c = WHITE          # 1 1 branco
            elif x == 14 or y == 12:
                c = SHADOW         # -2 -2 sombra
            elif x == 1 or y == 1:
                c = LIGHT          # 2 2 face clara
            else:
                continue
            px[x, y] = c
    for j, row in enumerate(glyph):
        for i, ch in enumerate(row):
            if ch == "#":
                px[gx + i, gy + j] = BLACK
    return im


AURORAE = C95.parent.parent.parent / "temas/aurorae/Win98"
AURORAE_FILE = {"window-close": "close", "window-minimize": "minimize",
                "window-maximize": "maximize", "window-restore": "restore"}


def aurorae_button(name, w=22, h=20):
    """botão da barra de título (já é 22x20 pixel a pixel: desenhado 1:1, sem ampliar)"""
    import os, sys
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtCore import QRectF
    from PySide6.QtGui import QGuiApplication, QImage, QPainter, QColor
    from PySide6.QtSvg import QSvgRenderer
    app = QGuiApplication.instance() or QGuiApplication(sys.argv)
    r = QSvgRenderer(str(AURORAE / f"{AURORAE_FILE[name]}.svg"))
    img = QImage(w, h, QImage.Format_ARGB32)
    img.fill(QColor(0, 0, 0, 0))
    p = QPainter(img)
    r.render(p, "active-center", QRectF(0, 0, w, h))
    p.end()
    return Image.frombuffer("RGBA", (w, h), img.bits().tobytes(), "raw", "BGRA", 0, 1).copy()


def main():
    for size in (16, 22, 24, 32, 48):
        d = C95 / str(size)
        if not d.is_dir():
            continue
        k = max(1, size // 16)
        for name, (glyph, gx, gy) in GLYPHS.items():
            if size in (22, 24):
                b = aurorae_button(name)
            else:
                b = button(glyph, gx, gy).resize((16 * k, 14 * k), Image.NEAREST)
            icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            icon.paste(b, ((size - b.width) // 2, (size - b.height) // 2))
            dst = d / f"{name}.png"
            if dst.is_symlink() or dst.exists():
                dst.unlink()           # quebra o link pro símbolo sem botão
            icon.save(dst)
        for name in GLYPHS:
            link = d / f"{name}-symbolic.symbolic.png"
            if link.is_symlink():
                link.unlink()          # apontava pro botão novo; o SE98 tem o símbolo
    print("botões da barra de título gerados em", C95)


if __name__ == "__main__":
    main()
