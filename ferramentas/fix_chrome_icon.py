#!/usr/bin/env python3
"""Ícone do Google Chrome = chrome.png do pacote Windows 95 +PLUS+ (terceiros/Win95PLUS, CC BY 4.0).

No Chicago95, google-chrome era link pro desenho do Internet Explorer (chromium-browser) em
16/22/24/32/48 e no SVG escalável. Aqui:
- 32: o chrome.png original (o pacote só foi desenhado em 32x32);
- 16/22/24/48 e scalable: as entradas do IE saem, e o KDE usa o de 32 redimensionado (não
  inventa desenho em tamanho que o autor não fez; se o SVG do IE ficasse, ele ganharia em 48).
O chromium-browser (o IE) continua lá pro Chromium. Rodar de novo se reinstalar o Chicago95.
"""
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
APPS = RAIZ / "terceiros/Chicago95/apps"
CHROME = RAIZ / "terceiros/Win95PLUS/icons_32x32/chrome.png"
NOMES = ["google-chrome", "google-chrome-stable", "google-chrome-unstable", "google-chrome-beta"]

for size in ("16", "22", "24", "32", "48", "scalable"):
    for nome in NOMES:
        for ext in (".png", ".svg"):
            f = APPS / size / f"{nome}{ext}"
            if f.is_symlink() or f.exists():
                f.unlink()
                print("removido:", f.relative_to(RAIZ))
dst = APPS / "32" / "google-chrome.png"
shutil.copy(CHROME, dst)
print("instalado:", dst.relative_to(RAIZ))
