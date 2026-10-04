#!/usr/bin/env bash
# Troca o nome do programa no título do Konsole: "Prompt de Comando — Konsole" vira
# "Prompt de Comando — Konsole DOS".
# O " — Konsole" quem escreve é o KDE (KMainWindow), com o nome que o Konsole pega da tradução
# (i18nc("@title", "Konsole") no main.cpp). Aqui sai uma cópia da tradução oficial instalada, só com
# essa frase trocada, em ~/.local/share/locale/<idioma>/LC_MESSAGES/konsole.mo, que o KDE lê antes da
# do sistema. Rodar de novo depois de atualizar o Konsole (a cópia é refeita da tradução nova).
# Uso: ./ferramentas/gen_konsole_nome.sh [idioma] [nome]   (padrão: pt_BR, "Konsole DOS")
set -euo pipefail
IDIOMA="${1:-pt_BR}"; NOME="${2:-Konsole DOS}"
SISTEMA="/usr/share/locale/$IDIOMA/LC_MESSAGES/konsole.mo"
DEST="$HOME/.local/share/locale/$IDIOMA/LC_MESSAGES/konsole.mo"
command -v msgunfmt >/dev/null && command -v msgfmt >/dev/null || { echo "precisa do gettext (msgunfmt/msgfmt)"; exit 1; }
[ -f "$SISTEMA" ] || { echo "sem tradução do Konsole em $IDIOMA ($SISTEMA)"; exit 1; }
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
msgunfmt "$SISTEMA" -o "$TMP/konsole.po"
NOME="$NOME" python3 - "$TMP/konsole.po" <<'PY'
import os, re, sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
novo, n = re.subn(r'(msgctxt "@title"\nmsgid "Konsole"\nmsgstr )"[^"]*"', r'\1"' + os.environ["NOME"] + '"', s)
if n != 1:
    sys.exit(f"esperava 1 frase @title \"Konsole\", achei {n}")
open(p, "w", encoding="utf-8").write(novo)
PY
mkdir -p "$(dirname "$DEST")"
msgfmt "$TMP/konsole.po" -o "$DEST"
echo "nome do Konsole no título: \"$NOME\" ($DEST)"
