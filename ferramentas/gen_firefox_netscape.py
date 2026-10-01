#!/usr/bin/env python3
"""Recorta os desenhos do FOXSCAPEuC (terceiros/) pro tema Netscape do Firefox.

Só corta e copia; não desenha nada. Sai em extras/firefox/chrome/netscape/:
  <botão>-{normal,hover,disabled,active}.png  24x24, da folha z-main/myToolbar.png
      (colunas de 24px na ordem abaixo; linhas: 0 normal, 24 hover, 48 desativado, 96 clicado)
  throbber.png / throbber-animado.gif          o "N" do Netscape 4 (32x32), parado e girando
  nova-aba-*.png, lista-abas-*.png              botões da barra de abas (img/newtab, img/alltabs)
Rodar de novo se trocar o FOXSCAPEuC.
"""
import shutil
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
FS = RAIZ / "terceiros/FOXSCAPEuC/foxscapeuc"
OUT = RAIZ / "extras/firefox/chrome/netscape"
OUT.mkdir(parents=True, exist_ok=True)

COLUNAS = ["back", "forward", "stop", "reload", "home", "downloads", "history", "bookmarks",
           "print", "new-tab", "new-window", "cut", "copy", "paste", "fullscreen",
           "zoom-out", "zoom-in"]
LINHAS = {"normal": 0, "hover": 24, "disabled": 48, "active": 96}

folha = Image.open(FS / "z-main/myToolbar.png").convert("RGBA")
for i, nome in enumerate(COLUNAS):
    for estado, y in LINHAS.items():
        folha.crop((i * 24, y, i * 24 + 24, y + 24)).save(OUT / f"{nome}-{estado}.png")

shutil.copy(FS / "thr/Throbber32S.png", OUT / "throbber.png")
shutil.copy(FS / "thr/Throbber32A.gif", OUT / "throbber-animado.gif")


def tiras(arquivo, prefixo, largura, estados):
    img = Image.open(FS / arquivo).convert("RGBA")
    for n, estado in enumerate(estados):
        img.crop((n * largura, 0, n * largura + largura, img.height)).save(OUT / f"{prefixo}-{estado}.png")


tiras("img/newtab.png", "nova-aba", 16, ["normal", "hover", "active"])
tiras("img/alltabs.png", "lista-abas", 14, ["normal", "hover", "active"])
print("desenhos do Netscape em", OUT)
