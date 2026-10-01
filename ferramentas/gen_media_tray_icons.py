#!/usr/bin/env python3
"""Ícones do controle de mídia da bandeja (media-playback-{playing,paused,stopped}; o widget pede
com -symbolic): o jeito que o 98 mostrava play/pause, um botão cinza em relevo com o símbolo preto
dentro, como no CD Player e nos [_][□][X] das janelas.

Não existe play/pause "estilizado" do 98 pronto (procurado em 29/09/2026: ícones originais do
95-XP, win98theme, OpenGameArt...). Aqui só junta o que já existe: o relevo do botão do 98.css
(igual ao de gen_titlebar_icons.py) e os símbolos ▶ ❚❚ ■ do próprio Chicago95
(actions/<tam>/media-playback-{start,pause,stop}.png).
Grava em terceiros/Chicago95/status/<tam>/. Rodar de novo se reinstalar o Chicago95.
"""
from pathlib import Path
from PIL import Image

C95 = Path(__file__).resolve().parent.parent / "terceiros/Chicago95"
FACE, LIGHT, WHITE, SHADOW, FRAME = (192, 192, 192), (223, 223, 223), (255, 255, 255), (128, 128, 128), (10, 10, 10)
ESTADOS = {"playing": "media-playback-start", "paused": "media-playback-pause", "stopped": "media-playback-stop"}
# tamanho do ícone: (tamanho do símbolo do Chicago95 usado, ampliação pixel a pixel)
FONTES = {"16": ("16", 1), "22": ("22", 1), "24": ("24", 1), "32": ("32", 1), "48": ("16", 3)}


def botao(w, h):
    """Botão em relevo do 98.css (box-shadow do button): branco/moldura por fora, claro/sombra por dentro."""
    im = Image.new("RGBA", (w, h), FACE + (255,))
    px = im.load()
    for x in range(w):
        for y in range(h):
            if x == w - 1 or y == h - 1:
                c = FRAME
            elif x == 0 or y == 0:
                c = WHITE
            elif x == w - 2 or y == h - 2:
                c = SHADOW
            elif x == 1 or y == 1:
                c = LIGHT
            else:
                continue
            px[x, y] = c + (255,)
    return im


for size, (fonte, k) in FONTES.items():
    s = int(size)
    w, h = s, s - 2 * max(1, s // 16)          # 16x14, 22x20, 24x22, 32x28, 48x42 (como a barra de título)
    destino = C95 / "status" / size
    destino.mkdir(parents=True, exist_ok=True)
    for estado, nome in ESTADOS.items():
        glifo = Image.open(C95 / "actions" / fonte / f"{nome}.png").convert("RGBA")
        glifo = glifo.crop(glifo.getbbox())
        if k > 1:
            glifo = glifo.resize((glifo.width * k, glifo.height * k), Image.NEAREST)
        b = botao(w, h)
        b.alpha_composite(glifo, ((w - glifo.width) // 2, (h - glifo.height) // 2))
        icone = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        icone.paste(b, (0, (s - h) // 2))
        arq = destino / f"media-playback-{estado}.png"
        if arq.is_symlink() or arq.exists():
            arq.unlink()
        icone.save(arq)
print("botões de mídia gerados em", C95 / "status")
