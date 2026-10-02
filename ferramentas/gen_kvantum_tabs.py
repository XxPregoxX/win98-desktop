#!/usr/bin/env python3
"""Gera as abas do Kvantum ([Tab], [TabFrame] em temas/kvantum/Win98/), no desenho do 98.css.

Antes as abas usavam o desenho do botão: pareciam botões soltos e não dava pra ver qual estava
selecionada. No 98 (98.css, menu[role=tablist]):
- aba: borda de 2px — cinza-claro #dfdfdf por fora e branco por dentro em cima/esquerda, preto
  #0a0a0a por fora e cinza #808080 por dentro à direita —, cantos de cima arredondados e sem
  borda embaixo; embaixo dela passa a borda de cima do painel (#dfdfdf, branco);
- no modo documento (Konsole), sem painel embaixo, as inativas não têm a linha dele (floating-tab-*);
- aba selecionada: 2px mais alta (as outras ficam 2px mais baixas: 2px transparentes em cima),
  na frente das vizinhas (active_tab_overlap) e sem a linha do painel embaixo, emendada nele.
O texto da aba selecionada fica em negrito (não é do 98: é pra achar a aba ativa de relance).
O painel das abas ([TabFrame]) ganha a borda de janela do 98.css (--border-window-outer/inner).
O X de fechar a aba (Konsole, Dolphin...) é o close.svg do 98.css (8x7); antes não aparecia porque
o Kvantum procurava um desenho que o tema não tinha.
Rodar de novo é seguro: substitui tudo o que for tab-* e tabframe-*.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "temas/kvantum/Win98/Win98.svg"
CFG = ROOT / "temas/kvantum/Win98/Win98.kvconfig"
COR = {"D": "#dfdfdf", "W": "#ffffff", "G": "#808080", "K": "#0a0a0a", "F": "#c0c0c0", "T": None}
M = 6  # miolo dos pedaços de exemplo

# pedaços da aba, em "pixels" (linhas de cima pra baixo). Bordas: cima 4 (2 transparentes nas
# inativas), embaixo 2, laterais 2.
SELECIONADA = {
    "-topleft": ["TT", "TD", "DW", "DW"],
    "-top": ["D", "W", "F", "F"],
    "-topright": ["TT", "KT", "GK", "GK"],
    "-left": ["DW"], "-right": ["GK"],
    "-bottomleft": ["DW", "DW"], "-bottom": ["F", "F"], "-bottomright": ["GK", "GK"],
}
INATIVA = {
    "-topleft": ["TT", "TT", "TT", "TD"],
    "-top": ["T", "T", "D", "W"],
    "-topright": ["TT", "TT", "TT", "KT"],
    "-left": ["DW"], "-right": ["GK"],
    # a borda de cima do painel passando embaixo da aba
    "-bottomleft": ["DD", "WW"], "-bottom": ["D", "W"], "-bottomright": ["DD", "WW"],
}
# modo documento (Konsole, abas sem painel embaixo): o Kvantum usa os "floating-tab-*". Sem painel,
# a linha dele embaixo das inativas ficava solta: elas terminam com as laterais descendo até o fim.
FLUTUANTE_INATIVA = dict(INATIVA, **{"-bottomleft": ["DW", "DW"], "-bottom": ["F", "F"],
                                      "-bottomright": ["GK", "GK"]})
# painel das abas: borda de janela do 98.css (fora: claro em cima/esq, preto embaixo/dir;
# dentro: branco em cima/esq, cinza embaixo/dir)
PAINEL = {
    "-topleft": ["DD", "DW"], "-top": ["D", "W"], "-topright": ["DK", "GK"],
    "-left": ["DW"], "-right": ["GK"],
    "-bottomleft": ["DG", "KK"], "-bottom": ["G", "K"], "-bottomright": ["GK", "KK"],
}
# X do 98.css (icon/close.svg, 8x7), num quadrado de 9x9
X = ["##....##", ".##..##.", "..####..", "...##...", "..####..", ".##..##.", "##....##"]


def rects(grade, x0, y0, largura=None, altura=None):
    """pedaço em pixels -> retângulos. Os que esticam (cima/baixo: 1 coluna; laterais: 1 linha)
    viram faixas inteiras do tamanho do exemplo: pixel solto deixa emenda quando o Kvantum estica."""
    out = []
    if largura is not None:      # cima/baixo: uma faixa horizontal por linha
        for y, linha in enumerate(grade):
            if COR[linha[0]]:
                out.append(f'<rect x="{x0}" y="{y0 + y}" width="{largura}" height="1" fill="{COR[linha[0]]}"/>')
        return out
    if altura is not None:       # laterais: uma faixa vertical por coluna
        for x, c in enumerate(grade[0]):
            if COR[c]:
                out.append(f'<rect x="{x0 + x}" y="{y0}" width="1" height="{altura}" fill="{COR[c]}"/>')
        return out
    for y, linha in enumerate(grade):
        for x, c in enumerate(linha):
            if COR[c]:
                out.append(f'<rect x="{x0 + x}" y="{y0 + y}" width="1" height="1" fill="{COR[c]}"/>')
    return out


def elemento(nome, pecas, interior, y):
    out, x = [], 0
    for part, grade in pecas.items():
        largura = M if part in ("-top", "-bottom") else None
        altura = M if part in ("-left", "-right") else None
        out.append(f'<g id="{nome}{part}">' + "".join(rects(grade, x, y, largura, altura)) + "</g>")
        x += 10
    corpo = f'<rect x="{x}" y="{y}" width="{M}" height="{M}" fill="{COR[interior]}"/>' if COR[interior] else ""
    out.append(f'<g id="{nome}">{corpo}</g>')
    return out


def xis(nome, cor, y):
    corpo = "".join(f'<rect x="{x}" y="{y + 1 + i}" width="1" height="1" fill="{cor}"/>'
                    for i, linha in enumerate(X) for x, c in enumerate(linha) if c == "#")
    # quadrado transparente de 9x9 marca o tamanho do desenho
    return f'<g id="{nome}"><rect x="0" y="{y}" width="9" height="9" fill="none"/>{corpo}</g>'


svg = SVG.read_text()
svg = re.sub(r'<g id="(?:floating-)?tab(?:frame)?-[A-Za-z-]+">.*?</g>\n?', "", svg)
m = re.search(r'<!-- tabs98-top=(\d+) -->', svg)
altura_svg = int(re.search(r'<svg [^>]*height="(\d+)"', svg).group(1))
top = int(m.group(1)) if m else altura_svg
out = [] if m else [f"<!-- tabs98-top={top} -->"]
y = top
for suf in ("", "-inactive"):
    for estado, pecas in (("normal", INATIVA), ("focused", INATIVA), ("toggled", SELECIONADA)):
        out += elemento(f"tab-{estado}{suf}", pecas, "F", y)
        y += 12
    for estado, pecas in (("normal", FLUTUANTE_INATIVA), ("focused", FLUTUANTE_INATIVA),
                          ("toggled", SELECIONADA)):
        out += elemento(f"floating-tab-{estado}{suf}", pecas, "F", y)
        y += 12
    for estado in ("normal", "focused", "pressed", "toggled", "toggledFocused", "toggledPressed"):
        out.append(xis(f"tab-close-{estado}{suf}", COR["K"], y))
        y += 12
    out.append(xis(f"tab-close-disabled{suf}", COR["G"], y))
    y += 12
    for estado in ("normal", "focused", "disabled"):
        out += elemento(f"tabframe-{estado}{suf}", PAINEL, "T", y)
        y += 12
svg = re.sub(r'(<svg [^>]*height=")\d+(")', rf"\g<1>{max(altura_svg, y)}\2", svg, count=1)
svg = svg.replace("</svg>", "\n".join(out) + "\n</svg>") if out else svg
SVG.write_text(svg)

cfg = CFG.read_text()
tab = ("[Tab]\ninherits=PanelButtonCommand\nframe.element=tab\ninterior.element=tab\nindicator.element=tab\n"
       "indicator.size=9\nframe.top=4\nframe.bottom=2\nframe.left=2\nframe.right=2\nframe.expansion=0\n"
       "text.margin.top=1\ntext.margin.bottom=1\ntext.margin.left=6\ntext.margin.right=6\n")
cfg = re.sub(r"\[Tab\]\n.*?(?=\n\[)", tab, cfg, count=1, flags=re.S)
cfg = re.sub(r"(\[TabFrame\]\n(?:.*\n)*?)frame\.element=\w+", r"\1frame.element=tabframe", cfg, count=1)
geral = {"attach_active_tab": "true", "joined_inactive_tabs": "false", "active_tab_overlap": "2",
         "mirror_doc_tabs": "true", "left_tabs": "true",
         # não é do 98, mas com só 2px de diferença não dava pra ver qual aba estava selecionada
         "bold_active_tab": "true"}
for chave, valor in geral.items():
    if re.search(rf"^{chave}=", cfg, re.M):
        cfg = re.sub(rf"^{chave}=.*$", f"{chave}={valor}", cfg, count=1, flags=re.M)
    else:
        cfg = re.sub(r"(\[%General\]\n)", rf"\1{chave}={valor}\n", cfg, count=1)
CFG.write_text(cfg)
print("abas do 98 geradas: tab-*, tab-close-*, tabframe-*; [Tab] e [TabFrame] atualizados")
