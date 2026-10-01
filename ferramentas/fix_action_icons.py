#!/usr/bin/env python3
# Icones de acao que aparecem como folha em branco (ex.: "Abrir menu" do Konsole/Dolphin).
# Causa: o KDE trata nomes que comecam com tipo de arquivo ("application-", "audio-"...) como
# mimetype. Se o Chicago95 nao tem o icone, o KDE usa o generico do proprio Chicago95
# (application-x-generic) antes de procurar no SE98, que e o tema pai e tem o desenho certo.
# Conserto: copia o desenho do SE98 pra dentro do Chicago95.
#   ./fix_action_icons.py            aplica
#   ./fix_action_icons.py --auditar  lista quem cai no generico (precisa de PySide6)
import os, shutil, sys
ICONS = os.path.expanduser("~/.local/share/icons")
C95, SE98 = os.path.join(ICONS, "Chicago95/actions"), os.path.join(ICONS, "SE98/actions")
SIZES = ("16", "22", "24", "32", "48")
MIME_PREFIXES = ("application", "audio", "font", "image", "inode", "message", "model", "multipart", "text", "video")

def auditar():
    import glob
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("QT_QPA_PLATFORMTHEME", "kde")
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QIcon
    app = QApplication(sys.argv)
    names = set()
    for d in glob.glob("/usr/share/icons/breeze/actions/*/") + glob.glob(SE98 + "/*/"):
        names |= {f.rsplit(".", 1)[0] for f in os.listdir(d) if "-symbolic" not in f}
    for n in sorted(names):
        r = QIcon.fromTheme(n).name()
        if r != n and r.endswith("-generic") and n.split("-")[0] in MIME_PREFIXES:
            print(n, "->", r)

# Achados pelo --auditar (28/09/2026)
NAMES = ["application-menu", "audio-cd-duplicate", "audio-cd-new"]

if "--auditar" in sys.argv:
    auditar(); sys.exit()
done = []
for n in NAMES:
    for s in SIZES:
        src, dst = os.path.join(SE98, s, n + ".png"), os.path.join(C95, s, n + ".png")
        if not (os.path.exists(src) and os.path.isdir(os.path.dirname(dst))): continue
        if os.path.lexists(dst): os.remove(dst)
        shutil.copyfile(os.path.realpath(src), dst); done.append(f"{s}/{n}")
print(len(done), "icones copiados:", ", ".join(done))
