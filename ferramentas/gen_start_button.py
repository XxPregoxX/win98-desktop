#!/usr/bin/env python3
# Gera o botao Iniciar do 98 em tamanho 1:1 (115x35, o tamanho que o painel de 40px mostra):
# win98-start-button.png (em relevo) e win98-start-pressed.png (afundado, conteudo +1px).
import os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont

W, H = 115, 35
ICONS = os.path.expanduser("~/.local/share/icons")
FLAG_SVG = os.path.join(ICONS, "Chicago95/places/scalable/start-here.svg")
FONT = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf"
WHITE, LIGHT, FACE, SHADOW, DARK = "#ffffff", "#dfdfdf", "#c0c0c0", "#808080", "#000000"
FLAG = 24

flag_png = os.path.join(tempfile.gettempdir(), "win98_flag24.png")
subprocess.run(["magick", "-background", "none", "-density", "384", FLAG_SVG, "-resize", f"{FLAG}x{FLAG}", flag_png], check=True)
flag = Image.open(flag_png).convert("RGBA")
font = ImageFont.truetype(FONT, 21)

def button(pressed):
    im = Image.new("RGBA", (W, H), FACE); d = ImageDraw.Draw(im)
    # bevel do botao do 98 (98.css): em relevo = claro em cima/esq; afundado = invertido
    tl_out, tl_in, br_in, br_out = (DARK, SHADOW, LIGHT, WHITE) if pressed else (WHITE, LIGHT, SHADOW, DARK)
    d.line([(1, 1), (W - 2, 1)], tl_in); d.line([(1, 1), (1, H - 2)], tl_in)
    d.line([(1, H - 2), (W - 2, H - 2)], br_in); d.line([(W - 2, 1), (W - 2, H - 2)], br_in)
    d.line([(0, 0), (W - 1, 0)], tl_out); d.line([(0, 0), (0, H - 1)], tl_out)
    d.line([(0, H - 1), (W - 1, H - 1)], br_out); d.line([(W - 1, 0), (W - 1, H - 1)], br_out)
    off = 1 if pressed else 0
    im.alpha_composite(flag, (7 + off, (H - FLAG) // 2 + off))
    d.text((36 + off, H // 2 + off), "Iniciar", font=font, fill=DARK, anchor="lm")
    return im

button(False).save(os.path.join(ICONS, "win98-start-button.png"))
button(True).save(os.path.join(ICONS, "win98-start-pressed.png"))
print("gerados em", ICONS)
