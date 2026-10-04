#!/usr/bin/env bash
# Volta o KDE Plasma 6 pro visual padrão (Breeze) e tira o tema Windows 98: desfaz as
# configurações do instalar.sh, apaga os links que apontam pra esta pasta e tira o tema do Firefox.
# Não apaga esta pasta nem os backups. O fundo de tela e a altura do painel ficam como estão.
# Uso: ./desinstalar.sh            (desfaz)
#      ./desinstalar.sh --simular  (só mostra o que faria)
set -euo pipefail
P="$(cd "$(dirname "$0")" && pwd)"
SIM=0; [ "${1:-}" = "--simular" ] && SIM=1
x() { if [ $SIM = 1 ]; then echo "  [simular] $*"; else "$@"; fi; }
kw() { x kwriteconfig6 --file "$1" --group "$2" --key "$3" "$4"; }
kdel() { x kwriteconfig6 --file "$1" --group "$2" --key "$3" --delete; }

echo "== Menu Iniciar: volta pro Kickoff original (reinicia o plasmashell) =="
x kquitapp6 plasmashell >/dev/null 2>&1 || true; [ $SIM = 1 ] || sleep 1
SIM=$SIM python3 - <<'PY'
import configparser, os, subprocess
f = "plasma-org.kde.plasma.desktop-appletsrc"
c = configparser.ConfigParser(strict=False, interpolation=None); c.optionxform = str
c.read(os.path.expanduser("~/.config/" + f))
for s in c.sections():
    if c[s].get("plugin") == "org.kde.plasma.win98kickoff":
        groups = [g for part in s.strip("[]").split("][") for g in ("--group", part)]
        cmds = [["--key", "plugin", "org.kde.plasma.kickoff"],
                ["--group", "Configuration", "--group", "General", "--key", "icon", "--delete"]]
        for k in cmds:
            cmd = ["kwriteconfig6", "--file", f, *groups, *k]
            if os.environ.get("SIM") == "1": print("  [simular]", " ".join(cmd))
            else: subprocess.run(cmd, check=True)
        print("  applet", s)
PY

echo "== Cores, estilo, ícones, cursor, fontes =="
x plasma-apply-colorscheme BreezeLight || true
x plasma-apply-desktoptheme default || true
kw kdeglobals KDE widgetStyle Breeze
kw kdeglobals Icons Theme breeze
for k in font menuFont toolBarFont smallestReadableFont; do kdel kdeglobals General "$k"; done
kdel kdeglobals WM activeFont
kdel kdeglobals ToolbarIcons Size
kdel kdeglobals MainToolbarIcons Size
kw kcminputrc Mouse cursorTheme breeze_cursors
kdel kcminputrc Mouse cursorSize
x plasma-apply-cursortheme breeze_cursors --size 24 || true
x gsettings reset org.gnome.desktop.interface cursor-size || true
x gsettings reset org.gnome.desktop.sound theme-name || true
x rm -f "$HOME/.config/autostart/win98-startup.desktop"

echo "== Konsole =="
kdel konsolerc "Desktop Entry" DefaultProfile
kdel konsolerc MainWindow MenuBar
kdel konsolerc KonsoleWindow RememberWindowSize
x rm -f "$HOME/.local/share/locale/${LANG%%.*}/LC_MESSAGES/konsole.mo"
x rm -f "$HOME/.local/share/konsole/MS-DOS.profile" "$HOME/.local/share/kxmlgui5/konsole/konsoleui.rc" \
    "$HOME/.local/share/kxmlgui5/konsole/sessionui.rc"

echo "== Janelas e efeitos (KWin) =="
kw kwinrc org.kde.kdecoration2 library org.kde.breeze
kw kwinrc org.kde.kdecoration2 theme Breeze
for e in win98menuslide win98windows; do kw kwinrc Plugins "${e}Enabled" false; done
# os efeitos padrão voltam ao que o KDE decide (apaga a escolha do instalador)
for e in scale fade kwin4_effect_fade squash magiclamp fadingpopups slidingpopups; do kdel kwinrc Plugins "${e}Enabled"; done
x gdbus call --session --dest org.kde.KWin --object-path /KWin --method org.kde.KWin.reconfigure >/dev/null || true

echo "== Links que apontam pra esta pasta =="
for lst in "$P/.links" "$P/.links.local"; do
    [ -f "$lst" ] || continue
    while IFS='|' read -r rel live; do
        [ -n "$rel" ] || continue
        src="$HOME/$live"
        if [ -L "$src" ] && [ "$(readlink "$src")" = "$P/$rel" ]; then x rm "$src"; echo "  tirado: ~/$live"; fi
    done < "$lst"
done

echo "== Firefox =="
for base in "$HOME/.config/mozilla/firefox" "$HOME/.mozilla/firefox"; do
    for prof in "$base"/*/; do
        prof="${prof%/}"
        if [ -L "$prof/chrome" ] && [ "$(readlink "$prof/chrome")" = "$P/extras/firefox/chrome" ]; then
            x rm "$prof/chrome"; echo "  tema tirado: $prof"
        fi
        [ -f "$prof/user.js" ] || continue
        if [ $SIM = 1 ]; then echo "  [simular] tirar as linhas do tema de $prof/user.js"; continue; fi
        python3 - "$P/extras/firefox/user.js" "$prof/user.js" <<'PY'
import re, sys
nosso, dele = sys.argv[1], sys.argv[2]
INI, FIM = "// >>> tema win98-desktop", "// <<< tema win98-desktop"
chave = lambda l: (re.match(r'\s*user_pref\("([^"]+)"', l) or [None, None])[1]
nomes = {chave(l) for l in open(nosso).read().splitlines() if chave(l)}
fica, dentro = [], False
for l in open(dele).read().splitlines():
    if l.strip() == INI: dentro = True; continue
    if l.strip() == FIM: dentro = False; continue
    if not dentro and chave(l) not in nomes: fica.append(l)
open(dele, "w").write("\n".join(fica) + ("\n" if fica else ""))
PY
    done
done

echo "== Reiniciando o plasmashell =="
if [ $SIM = 1 ]; then echo "  [simular] kstart plasmashell"; else setsid kstart plasmashell >/dev/null 2>&1 & fi
cat <<'FIM'
Pronto. Saia e entre de novo na sessão pro cursor, as fontes e o estilo dos apps voltarem em tudo.
No Firefox (com ele fechado e aberto de novo), em about:config, as preferências do tema continuam
com o último valor: se quiser, volte browser.tabs.inTitlebar e
layout.css.prefers-color-scheme.content-override pro padrão.
FIM
