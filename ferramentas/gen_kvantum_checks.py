#!/usr/bin/env python3
"""Gera as caixas de marcar e os botões de rádio do Kvantum (temas/kvantum/Win98/Win98.svg).

O desenho vem do 98.css (github.com/jdan/98.css, MIT), recriação pixel a pixel dos controles
do Win98, com o ✓ 7x7, a borda do rádio 12x12 e a bolinha 4x4 copiados dos SVGs dele (icon/*.svg).
- caixa: 13x13 branca com a borda de campo afundada (--border-field); ✓ em (3,3).
- clicando (:active) ou desativada: fundo cinza #c0c0c0; desativada: ✓ cinza.
- meio marcada (tristate): como no 98, ✓ cinza sobre fundo cinza.
Nomes que o Kvantum procura (interior.element=checkbox/radio):
  checkbox-{normal,focused,pressed,disabled}, checkbox-checked-*, checkbox-tristate-*,
  radio-*, radio-checked-*.  "focused" é o mouse em cima: no 98 não mudava nada.
Rodar de novo é seguro: substitui tudo o que for checkbox-* e radio-*.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "temas/kvantum/Win98/Win98.svg"
CFG = ROOT / "temas/kvantum/Win98/Win98.kvconfig"

WHITE, FACE, LIGHT, SHADOW, FRAME = "#ffffff", "#c0c0c0", "#dfdfdf", "#808080", "#0a0a0a"

# 98.css icon/checkmark.svg
CHECK = "M7 0H6V1H5V2H4V3H3V4H2V3H1V2H0V5H1V6H2V7H3V6H4V5H5V4H6V3H7V0Z"
# 98.css icon/radio-border.svg (a última camada é o miolo: branco, ou cinza no -disabled)
RADIO = [("M8 0H4V1H2V2H1V4H0V8H1V10H2V8H1V4H2V2H4V1H8V2H10V1H8V0Z", SHADOW),
         ("M8 1H4V2H2V3V4H1V8H2V9H3V8H2V4H3V3H4V2H8V3H10V2H8V1Z", "black"),
         ("M9 3H10V4H9V3ZM10 8V4H11V8H10ZM8 10V9H9V8H10V9V10H8ZM4 10V11H8V10H4ZM4 10V9H2V10H4Z", LIGHT),
         ("M11 2H10V4H11V8H10V10H8V11H4V10H2V11H4V12H8V11H10V10H11V8H12V4H11V2Z", "white")]
RADIO_CENTER = "M4 2H8V3H9V4H10V8H9V9H8V10H4V9H3V8H2V4H3V3H4V2Z"
# 98.css icon/radio-dot.svg
DOT = "M3 0H1V1H0V2V3H1V4H3V3H4V2V1H3V0Z"


def path(d, fill, x, y):
    return f'<path transform="translate({x} {y})" fill-rule="evenodd" d="{d}" fill="{fill}"/>'


def rect(x, y, w, h, fill):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'


def checkbox(x, y, bg, mark):
    # --border-field: inset -1 -1 branco, inset 1 1 sombra, inset -2 -2 face clara, inset 2 2 moldura
    # (no box-shadow a primeira sombra fica por cima, então desenha de trás pra frente)
    p = [rect(x, y, 13, 13, bg),
         rect(x, y, 13, 2, FRAME), rect(x, y, 2, 13, FRAME),
         rect(x, y + 11, 13, 2, LIGHT), rect(x + 11, y, 2, 13, LIGHT),
         rect(x, y, 13, 1, SHADOW), rect(x, y, 1, 13, SHADOW),
         rect(x, y + 12, 13, 1, WHITE), rect(x + 12, y, 1, 13, WHITE)]
    if mark:
        p.append(path(CHECK, mark, x + 3, y + 3))
    return p


def radio(x, y, center, dot):
    p = [rect(x, y, 13, 13, "none")]  # check_size é 13; o rádio do 98 tem 12
    p += [path(d, f, x, y) for d, f in RADIO] + [path(RADIO_CENTER, center, x, y)]
    if dot:
        p.append(path(DOT, dot, x + 4, y + 4))
    return p


STATES = {  # estado: (fundo, cor do ✓ marcado)
    "normal": (WHITE, "black"), "focused": (WHITE, "black"),
    "pressed": (FACE, "black"), "disabled": (FACE, SHADOW),
}
elements = []
for st, (bg, mark) in STATES.items():
    elements.append((f"checkbox-{st}", lambda x, y, bg=bg: checkbox(x, y, bg, None)))
    elements.append((f"checkbox-checked-{st}", lambda x, y, bg=bg, m=mark: checkbox(x, y, bg, m)))
    elements.append((f"checkbox-tristate-{st}", lambda x, y: checkbox(x, y, FACE, SHADOW)))
    elements.append((f"radio-{st}", lambda x, y, bg=bg: radio(x, y, bg, None)))
    elements.append((f"radio-checked-{st}", lambda x, y, bg=bg, m=mark: radio(x, y, bg, m)))

svg = SVG.read_text()
svg = re.sub(r'<g id="(?:checkbox|radio)-[a-z-]+">.*?</g>\n?', "", svg)
m = re.search(r'<svg [^>]*height="(\d+)"', svg)
top = int(m.group(1)) if "<!-- checks98 -->" not in svg else None
if top is None:  # rodada anterior: reaproveita a faixa já reservada
    top = int(re.search(r'<!-- checks98 y=(\d+) -->', svg).group(1))
    svg = re.sub(r'<!-- checks98 y=\d+ -->\n?', "", svg)
    svg = svg.replace("<!-- checks98 -->\n", "")
out = [f"<!-- checks98 y={top} -->"]
for i, (name, draw) in enumerate(elements):
    x, y = (i % 5) * 20, top + (i // 5) * 20
    out.append(f'<g id="{name}">' + "".join(draw(x, y)) + "</g>")
height = top + ((len(elements) + 4) // 5) * 20
svg = re.sub(r'(<svg [^>]*height=")\d+(")', rf"\g<1>{max(height, int(m.group(1)))}\2", svg, count=1)
svg = svg.replace("</svg>", "<!-- checks98 -->\n" + "\n".join(out) + "\n</svg>")
SVG.write_text(svg)

# Kvantum desenha caixa/rádio como "interior" (o indicator.element não vale pra eles)
cfg = CFG.read_text()
for sec, el in (("CheckBox", "checkbox"), ("RadioButton", "radio")):
    body = re.search(rf"\[{sec}\]\n(.*?)(?=\n\[|\Z)", cfg, re.S).group(1)
    new = "\n".join(l for l in body.splitlines()
                    if not l.startswith(("indicator.", "interior", "frame=", "frame."))).strip()
    new = f"frame=false\ninterior=true\ninterior.element={el}" + ("\n" + new if new else "")
    cfg = cfg.replace(f"[{sec}]\n{body}", f"[{sec}]\n{new}\n", 1)
CFG.write_text(cfg)
print(f"{len(elements)} elementos gerados em {SVG.name}; [CheckBox]/[RadioButton] ajustados")
