#!/usr/bin/env bash
# Baixa os pacotes de terceiros que o tema usa e que não vão no repositório (são grandes e têm
# os próprios autores e licenças, ver CREDITOS.md). Cada um vem da fonte original, numa versão
# fixa, a mesma com que o tema foi feito e testado.
#
#   ./ferramentas/baixar_terceiros.sh              ícones (Chicago95 + SE98) e cursor
#   ./ferramentas/baixar_terceiros.sh --foxscape   também o FOXSCAPEuC (só pra quem for refazer os
#                                                  desenhos do Netscape com gen_firefox_netscape.py)
#
# O que já existe em terceiros/ não é baixado de novo (apague a pasta pra baixar outra vez).
# Depois de baixar, os ajustes de ícones são aplicados por ferramentas/refazer_icones.sh
# (o instalar.sh faz tudo isso sozinho).
set -euo pipefail
P="$(cd "$(dirname "$0")/.." && pwd)"
T="$P/terceiros"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

# Chicago95, de grassmunk e colaboradores (GPL-3.0-or-later / MIT)
CHICAGO95_COMMIT=e89583c9a0fbc5022d099fbe6f12132a756027a8
# SE98, de nestoris (GPL-2.0)
SE98_COMMIT=e01de0a652679e288316ce9569c81b03042f0876
# FOXSCAPEuC v7, de Michael Walden (CC BY-NC-SA 3.0)
FOXSCAPE_URL="https://mw.rat.bz/foxscapeuc/FOXSCAPEuC%202021-03-06%20v7%20Fx85.0.zip"
FOXSCAPE_SHA256=036105e6a3d750cc9645edaf90ece9a44d8f81c88d27cca4d7dafeaf7f59ff22

baixar_github() {   # repo commit arquivo
    echo "  baixando $1 @ ${2:0:10}..."
    curl -fL --retry 3 -# -o "$TMP/$3" "https://codeload.github.com/$1/tar.gz/$2"
}

origem() {  # pasta linha...: anota de onde veio (ORIGEM.txt), já que não vai no repositório
    local d="$1"; shift; printf '%s\n' "$@" "Baixado por ferramentas/baixar_terceiros.sh. Não editar aqui." > "$d/ORIGEM.txt"
}

mkdir -p "$T"

if [ ! -d "$T/Chicago95" ] || [ ! -d "$T/Chicago95_Cursor_White" ]; then
    echo "== Chicago95 (ícones e cursor) — https://github.com/grassmunk/Chicago95"
    baixar_github grassmunk/Chicago95 "$CHICAGO95_COMMIT" c95.tgz
    mkdir -p "$TMP/c95"
    tar xzf "$TMP/c95.tgz" -C "$TMP/c95" --strip-components=1 \
        --wildcards '*/Icons/Chicago95/*' '*/Cursors/Chicago95_Cursor_White/*'
    for d in Icons/Chicago95 Cursors/Chicago95_Cursor_White; do
        n="$(basename "$d")"; [ -d "$T/$n" ] && continue
        mv "$TMP/c95/$d" "$T/"
        origem "$T/$n" "Chicago95, de grassmunk e colaboradores — https://github.com/grassmunk/Chicago95" \
            "commit $CHICAGO95_COMMIT, pasta $d" "Licença: GPL-3.0-or-later / MIT (README do Chicago95)"
    done
fi

if [ ! -d "$T/SE98" ]; then
    echo "== SE98 (ícones) — https://github.com/nestoris/Win98SE"
    baixar_github nestoris/Win98SE "$SE98_COMMIT" se98.tgz
    mkdir -p "$TMP/se98"
    tar xzf "$TMP/se98.tgz" -C "$TMP/se98" --strip-components=1 --wildcards '*/SE98/*'
    mv "$TMP/se98/SE98" "$T/"
    origem "$T/SE98" "SE98, de nestoris — https://github.com/nestoris/Win98SE" \
        "commit $SE98_COMMIT, pasta SE98" "Licença: GPL-2.0 (LICENSE do repositório)"
fi

if [ "${1:-}" = "--foxscape" ] && [ ! -d "$T/FOXSCAPEuC/foxscapeuc" ]; then
    echo "== FOXSCAPEuC (desenhos do Netscape) — https://mw.rat.bz/foxscapeuc/"
    curl -fL --retry 3 -# -o "$TMP/foxscape.zip" "$FOXSCAPE_URL"
    echo "$FOXSCAPE_SHA256  $TMP/foxscape.zip" | sha256sum -c --quiet
    mkdir -p "$T/FOXSCAPEuC" && unzip -q "$TMP/foxscape.zip" -d "$T/FOXSCAPEuC"
    origem "$T/FOXSCAPEuC" "FOXSCAPEuC v7 (2021-03-06), de Michael Walden — https://mw.rat.bz/foxscapeuc/" \
        "arquivo FOXSCAPEuC 2021-03-06 v7 Fx85.0.zip" "Licença: CC BY-NC-SA 3.0 (foxscapeuc/license.txt)"
fi

echo "Pronto: $T"
