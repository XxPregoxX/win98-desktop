#!/usr/bin/env python3
"""Apps que ainda saíam com ícone moderno (candy-icons, Breeze, hicolor) ganham um desenho do 98
que já existe no Chicago95/SE98, ou do pacote Win95 +PLUS+ (terceiros/Win95PLUS, CC BY 4.0).

Só os escolhidos pro tema: programas do Wine (são programas do Windows), utilitários
genéricos do KDE e o Discord. Apps de marca que se reconhecem pelo logo (OBS, Lutris, Heroic,
PCSX2, DOSBox, Shotcut, Pulsar, NeoChat...) ficam como estão.
Não mexe em nome que já resolve pra Chicago95/SE98. Copia o desenho em cada tamanho que a
fonte tem; nos outros o KDE usa o tamanho mais próximo. Rodar de novo se reinstalar o Chicago95.
Levantamento: ferramentas/app_icons_audit.txt.
"""
import os
import shutil
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
C95 = RAIZ / "terceiros/Chicago95"
SE98 = RAIZ / "terceiros/SE98"
W95PLUS = RAIZ / "terceiros/Win95PLUS/icons_32x32"
SIZES = ("16", "22", "24", "32", "48")
CATEGORIAS = ("apps", "categories", "actions", "places", "devices", "mimes", "mimetypes", "status")

# nome do ícone do app -> desenho 98 (nome no Chicago95/SE98, ou "w95plus:<arquivo>")
ALIASES = {
    # Wine
    "notepad": "accessories-text-editor",          # Bloco de Notas
    "wordpad": "libreoffice-writer",
    "winemine": "gnome-mines",                     # Campo Minado
    "winefile": "system-file-manager",
    "winecfg": "preferences-system",               # Painel de Controle
    "msiexec": "system-software-install",          # Adicionar/Remover Programas
    "winhelp": "help-browser",
    # utilitários do KDE e do sistema
    "kaddressbook": "addressbook",
    "kontact": "evolution",
    "kontact-import-wizard": "evolution",
    "ktnef": "internet-mail",
    "sieveeditor": "internet-mail",
    "kleopatra": "seahorse",                       # chaves e certificados
    "org.kde.kwatchgnupg": "seahorse",
    "kwalletmanager": "dialog-password",
    "firewall-config": "gufw",
    "tools-report-bug": "bug-buddy",
    "kmahjongg": "mahjongg",
    "krdc": "preferences-desktop-remote-desktop",
    "btop": "utilities-system-monitor",
    "nvtop": "utilities-system-monitor",
    "io.github.thetumultuousunicornofdarkness.cpu-x": "utilities-system-monitor",
    "org.fedoraproject.MediaWriter": "brasero",    # gravar mídia
    "kvantum": "preferences-desktop-theme",
    # pacote Win95 +PLUS+ (mesmo do ícone do Chrome)
    "discord": "w95plus:discord.png",
    "dev.vencord.Vesktop": "w95plus:discord.png",
}

# controle de mídia da bandeja: feito por gen_media_tray_icons.py (botão do CD Player do 98)
STATUS_ALIASES = {}

# força do sinal do Wi-Fi na lista de redes: o plasma-nm pede network-wireless-{0,20,40,60,80,100}
# (+ "-locked" com senha); o Chicago95 só tem as barras 0/25/50/75/100, e os níveis que faltam
# caíam no genérico network-wireless (um telefone de discada em 22px). Viram links pras barras
# mais próximas, nas mesmas pastas (status/48 e status/scalable), então saem idênticos.
WIFI = {}
for nivel, barra in ((0, 0), (20, 25), (40, 50), (60, 50), (80, 75), (100, 100)):
    WIFI[f"network-wireless-{nivel}"] = f"network-wireless-{barra}"
    WIFI[f"network-wireless-{nivel}-locked"] = f"network-wireless-{barra}"
    # ícone da dica de rede da bandeja (connectionicon.cpp): network-wireless-connected-{00,20..100}
    if nivel not in (0, 100):
        WIFI[f"network-wireless-connected-{nivel}"] = f"network-wireless-connected-{barra}"


def resolve(name):
    out = subprocess.run(["kiconfinder6", name], capture_output=True, text=True).stdout.strip()
    return os.path.realpath(out) if out else ""


def ja_e_98(name):
    p = resolve(name)
    return any(str(t) in p for t in (C95, SE98)) and "Win95PLUS" not in p


def fonte(src, size):
    for tema in (C95, SE98):
        for cat in CATEGORIAS:
            f = tema / cat / size / f"{src}.png"
            if f.exists():
                return f
    return None


def aplicar(alvo, src, pasta, forcar=False):
    if not forcar and ja_e_98(alvo):
        print(f"{alvo}: já é 98, não mexi")
        return
    feitos = []
    for size in SIZES:
        f = fonte(src, size)
        if not f:
            continue
        (C95 / pasta / size).mkdir(parents=True, exist_ok=True)
        destino = C95 / pasta / size / f"{alvo}.png"
        if destino.is_symlink() or destino.exists():
            destino.unlink()
        shutil.copyfile(os.path.realpath(f), destino)
        feitos.append(size)
    print(f"{alvo} <- {src}: {', '.join(feitos) or 'SEM DESENHO'}")


for alvo, src in WIFI.items():
    if alvo == src:
        continue
    feitos = []
    for pasta, ext in (("status/48", ".png"), ("status/scalable", ".svg")):
        fonte_ = C95 / pasta / f"{src}{ext}"
        if not (fonte_.exists() or fonte_.is_symlink()):
            continue
        destino = C95 / pasta / f"{alvo}{ext}"
        if destino.is_symlink() or destino.exists():
            destino.unlink()
        destino.symlink_to(f"{src}{ext}")
        feitos.append(pasta)
    print(f"{alvo} -> {src}: {', '.join(feitos) or 'SEM DESENHO'}")

for alvo, src in STATUS_ALIASES.items():
    aplicar(alvo, src, "status", forcar=True)

for alvo, src in ALIASES.items():
    if src.startswith("w95plus:"):
        destino = C95 / "apps/32" / f"{alvo}.png"
        if destino.is_symlink() or destino.exists():
            destino.unlink()
        shutil.copyfile(W95PLUS / src.split(":", 1)[1], destino)
        print(f"{alvo}: Win95 +PLUS+ (32)")
        continue
    aplicar(alvo, src, "apps")
