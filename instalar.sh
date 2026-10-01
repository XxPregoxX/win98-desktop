#!/usr/bin/env bash
# Instala o tema Windows 98 no KDE Plasma 6: liga os arquivos do projeto nos lugares
# que o KDE procura (links simbolicos) e aplica todas as configuracoes.
# Uso: ./instalar.sh            (tudo)
#      ./instalar.sh --so-links (so recria os links, sem mexer em configuracao)
# O que estiver no lugar de um link, e as configuracoes do Plasma que o instalador muda, vao antes
# pra backups/antes-da-instalacao-<data>/. Pra voltar ao visual padrao: ./desinstalar.sh
set -euo pipefail
P="$(cd "$(dirname "$0")" && pwd)"
BK="$P/backups/antes-da-instalacao-$(date +%Y%m%d-%H%M%S)"

# ---------- o que precisa estar instalado ----------
falta=()
for c in kwriteconfig6 plasma-apply-colorscheme plasma-apply-desktoptheme plasma-apply-cursortheme \
         gdbus kquitapp6 kstart kiconfinder6 python3 curl tar gtk-update-icon-cache; do
    command -v "$c" >/dev/null || falta+=("$c")
done
python3 -c 'import PIL, PySide6' 2>/dev/null || falta+=("python3: Pillow e PySide6")
ls /usr/lib*/qt6/plugins/styles/libkvantum.so >/dev/null 2>&1 || falta+=("Kvantum (plugin do Qt 6)")
if [ ${#falta[@]} -gt 0 ]; then
    echo "Falta instalar: ${falta[*]}"
    echo "No Fedora: sudo dnf install kvantum python3-pillow python3-pyside6 kf6-kiconthemes gtk-update-icon-cache"
    exit 1
fi

# ---------- pacotes de terceiros (icones e cursor), baixados das fontes originais ----------
novos=0
for d in Chicago95 SE98 Chicago95_Cursor_White; do [ -d "$P/terceiros/$d" ] || novos=1; done
[ $novos = 1 ] && bash "$P/ferramentas/baixar_terceiros.sh"

echo "== Links =="
ligar() {
    while IFS='|' read -r rel live; do
        [ -n "$rel" ] || continue
        src="$HOME/$live"; dst="$P/$rel"
        [ -e "$dst" ] || { echo "  (sem $rel, pulei)"; continue; }
        if [ -L "$src" ] && [ "$(readlink "$src")" = "$dst" ]; then continue; fi
        if [ -e "$src" ] || [ -L "$src" ]; then mkdir -p "$BK"; mv "$src" "$BK/"; echo "  guardado em backups: $live"; fi
        mkdir -p "$(dirname "$src")"; ln -s "$dst" "$src"; echo "  ligado: ~/$live"
    done < "$1"
}
ligar "$P/.links"
# links só desta máquina (fora do repositório), no mesmo formato
[ -f "$P/.links.local" ] && ligar "$P/.links.local"

# icones recem-baixados: aplica os ajustes (precisa dos links acima)
[ $novos = 1 ] && bash "$P/ferramentas/refazer_icones.sh"
[ "${1:-}" = "--so-links" ] && exit 0

# guarda as configuracoes do Plasma que vao mudar
mkdir -p "$BK"
for f in kdeglobals kwinrc kcminputrc plasma-org.kde.plasma.desktop-appletsrc Kvantum/kvantum.kvconfig; do
    [ -f "$HOME/.config/$f" ] && cp "$HOME/.config/$f" "$BK/$(echo "$f" | tr / _)"
done

kw() { kwriteconfig6 --file "$1" --group "$2" --key "$3" "$4"; }

echo "== Cores, estilo, icones, cursor, fontes =="
plasma-apply-colorscheme Win98
plasma-apply-desktoptheme Win98
mkdir -p ~/.config/Kvantum && cp "$P/extras/kvantum/kvantum.kvconfig" ~/.config/Kvantum/
kw kdeglobals KDE widgetStyle kvantum
kw kdeglobals Icons Theme Chicago95
F="Liberation Sans,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
for k in font menuFont toolBarFont; do kw kdeglobals General "$k" "$F"; done
kw kdeglobals General smallestReadableFont "Liberation Sans,9,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
kw kdeglobals WM activeFont "Liberation Sans,10,-1,5,700,0,0,0,0,0,0,0,0,0,0,1"
kw kdeglobals ToolbarIcons Size 22
kw kdeglobals MainToolbarIcons Size 22
kw kdeglobals KDE AnimationDurationFactor 1
kw kcminputrc Mouse cursorTheme Chicago95_Cursor_White
kw kcminputrc Mouse cursorSize 32
plasma-apply-cursortheme breeze_cursors >/dev/null 2>&1 || true   # troca e volta: faz o tamanho pegar no Wayland
plasma-apply-cursortheme Chicago95_Cursor_White --size 32 || true
gsettings set org.gnome.desktop.interface cursor-size 32 || true
gsettings set org.gnome.desktop.sound theme-name Win98 || true
gsettings set org.gnome.desktop.sound event-sounds true || true
# som de entrada na sessao (o .desktop precisa do caminho completo)
mkdir -p ~/.config/autostart
[ -L ~/.config/autostart/win98-startup.desktop ] && rm ~/.config/autostart/win98-startup.desktop
sed "s|@SONS@|$HOME/.local/share/sounds/Win98|" "$P/extras/win98-startup.desktop" > ~/.config/autostart/win98-startup.desktop

echo "== Janelas e efeitos (KWin) =="
kw kwinrc org.kde.kdecoration2 library org.kde.kwin.aurorae
kw kwinrc org.kde.kdecoration2 theme __aurorae__svg__Win98
for e in win98menuslide win98windows; do kw kwinrc Plugins "${e}Enabled" true; done
# substituidos pelo win98windows (abrir/fechar = desenrolar, minimizar = zoom ate o botao)
for e in scale fade kwin4_effect_fade squash magiclamp; do kw kwinrc Plugins "${e}Enabled" false; done
kw kwinrc Plugins fadingpopupsEnabled false      # substituidos pelo win98menuslide
kw kwinrc Plugins slidingpopupsEnabled false
kw kwinrc KDE AnimationDurationFactor 1
gdbus call --session --dest org.kde.KWin --object-path /KWin --method org.kde.KWin.reconfigure >/dev/null

echo "== Estilo QML (linha entre itens de lista) =="
# o extras/env/win98-qml.sh (ligado pelos links) vale a partir do proximo login;
# os Flatpaks nao enxergam ~/.local/share/win98-qml, entao nao recebem a variavel
flatpak override --user --unset-env=QT_QUICK_CONTROLS_STYLE 2>/dev/null || true

echo "== Firefox (tema Netscape, sites no modo escuro) =="
# imagens dos botões [_][□][X] que o KDE gera da decoração (usadas se as abas forem pra barra de título)
ln -sfn "$HOME/.config/gtk-3.0/assets" "$P/extras/firefox/chrome/win98-gtk-assets"
# perfis padrao do Firefox (os do profiles.ini; vale pra pasta nova e pra antiga)
perfis="$(python3 - <<'PY'
import configparser, os
for base in ("~/.config/mozilla/firefox", "~/.mozilla/firefox"):
    base = os.path.expanduser(base); ini = os.path.join(base, "profiles.ini")
    if not os.path.isfile(ini): continue
    c = configparser.ConfigParser(interpolation=None); c.read(ini)
    achados = set()
    for s in c.sections():
        if s.startswith("Install") and c[s].get("Default"):
            achados.add(c[s]["Default"])
        if s.startswith("Profile") and c[s].get("Default") == "1":
            achados.add(c[s]["Path"])
    for a in achados:
        p = a if os.path.isabs(a) else os.path.join(base, a)
        if os.path.isdir(p): print(p)
PY
)"
while IFS= read -r prof; do
    [ -n "$prof" ] && [ -d "$prof" ] || continue
    # junta as preferencias do tema ao user.js do perfil, sem apagar as que ja estavam la
    [ -f "$prof/user.js" ] && cp "$prof/user.js" "$BK/firefox-user.js-$(basename "$prof")"
    python3 - "$P/extras/firefox/user.js" "$prof/user.js" <<'PY'
import re, sys, os
nosso, dele = sys.argv[1], sys.argv[2]
INI, FIM = "// >>> tema win98-desktop", "// <<< tema win98-desktop"
chave = lambda l: (re.match(r'\s*user_pref\("([^"]+)"', l) or [None, None])[1]
novas = open(nosso).read().splitlines()
nomes = {chave(l) for l in novas if chave(l)}
velhas, dentro = [], False
for l in (open(dele).read().splitlines() if os.path.exists(dele) else []):
    if l.strip() == INI: dentro = True; continue
    if l.strip() == FIM: dentro = False; continue
    if not dentro and chave(l) not in nomes: velhas.append(l)
open(dele, "w").write("\n".join(velhas + [INI] + novas + [FIM]) + "\n")
PY
    if [ -d "$prof/chrome" ] && [ ! -L "$prof/chrome" ]; then
        mkdir -p "$BK" && mv "$prof/chrome" "$BK/firefox-chrome-$(basename "$prof")"
    fi
    ln -sfn "$P/extras/firefox/chrome" "$prof/chrome"
    echo "  $prof"
done <<< "$perfis"

echo "== Painel: fundo teal, altura, bandeja, relogio =="
gdbus call --session --dest org.kde.plasmashell --object-path /PlasmaShell --method org.kde.PlasmaShell.evaluateScript '
var ds = desktops();
for (var i = 0; i < ds.length; i++) {
    ds[i].wallpaperPlugin = "org.kde.color";
    ds[i].currentConfigGroup = ["Wallpaper", "org.kde.color", "General"];
    ds[i].writeConfig("Color", "0,128,128");
}
var ps = panels();
for (var i = 0; i < ps.length; i++) {
    ps[i].height = 40;
    ps[i].floating = false;          // no 98 a barra era grudada na borda
    var ws = ps[i].widgets();
    for (var j = 0; j < ws.length; j++) {
        var w = ws[j];
        if (w.type == "org.kde.plasma.systemtray") { w.currentConfigGroup = ["General"]; w.writeConfig("showAllItems", true); }
        if (w.type == "org.kde.plasma.digitalclock") { w.currentConfigGroup = ["Appearance"]; w.writeConfig("showDate", true); w.writeConfig("dateFormat", "shortDate"); }
    }
}' >/dev/null

echo "== Botao Iniciar: troca o Kickoff pelo fork win98kickoff (reinicia o plasmashell) =="
kquitapp6 plasmashell >/dev/null 2>&1 || true; sleep 1
python3 - <<'PY'
import configparser, os, subprocess
f = "plasma-org.kde.plasma.desktop-appletsrc"
c = configparser.ConfigParser(strict=False, interpolation=None); c.optionxform = str
c.read(os.path.expanduser("~/.config/" + f))
for s in c.sections():
    if c[s].get("plugin") in ("org.kde.plasma.kickoff", "org.kde.plasma.win98kickoff"):
        groups = [g for part in s.strip("[]").split("][") for g in ("--group", part)]
        w = lambda *k: subprocess.run(["kwriteconfig6", "--file", f, *groups, *k], check=True)
        w("--key", "plugin", "org.kde.plasma.win98kickoff")
        gen = [*groups, "--group", "Configuration", "--group", "General"]
        for key, val in (("icon", os.path.expanduser("~/.local/share/icons/win98-start-button.png")), ("appNameFormat", "0")):
            subprocess.run(["kwriteconfig6", "--file", f, *gen, "--key", key, val], check=True)
        print("  applet", s)
PY
setsid kstart plasmashell >/dev/null 2>&1 &
echo "Pronto. Pode ser preciso sair e entrar de novo na sessao pro cursor e as fontes pegarem em tudo."
