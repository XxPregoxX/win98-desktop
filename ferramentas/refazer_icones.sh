#!/usr/bin/env bash
# Reaplica todos os ajustes de ícones no Chicago95 (terceiros/Chicago95), na ordem certa.
# Rodar depois de baixar o Chicago95/SE98 de novo (baixar_terceiros.sh). Precisa dos links
# instalados (./instalar.sh --so-links), porque alguns scripts perguntam ao KDE (kiconfinder6).
set -euo pipefail
F="$(cd "$(dirname "$0")" && pwd)"
for s in fix_special_folders.py fix_mime_icons.py fix_action_icons.py gen_titlebar_icons.py \
         fix_chrome_icon.py fix_app_icons.py gen_media_tray_icons.py gen_folder_colors.py \
         fix_chicago95_ajustes.py; do
    echo "== $s"; python3 "$F/$s"
done
gtk-update-icon-cache -f -q "$HOME/.local/share/icons/Chicago95/" || true
rm -f "$HOME/.cache/icon-cache.kcache"
echo "Pronto. Reinicie o plasmashell (kquitapp6 plasmashell; kstart plasmashell) e reabra os apps."
