#!/usr/bin/env python3
# No Chicago95, varias pastas especiais (Documentos, Musica, Downloads...) em 22/24px sao so
# links pra pasta generica. Quando o SE98 tem desenho proprio pro mesmo nome/tamanho, copia ele.
import hashlib, os, shutil
ICONS = os.path.expanduser("~/.local/share/icons")
C95, SE98 = os.path.join(ICONS, "Chicago95/places"), os.path.join(ICONS, "SE98/places")
md5 = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
fixed = []
for size in ("16", "22", "24", "32", "48"):
    cdir, sdir = os.path.join(C95, size), os.path.join(SE98, size)
    if not (os.path.isdir(cdir) and os.path.isdir(sdir)):
        continue
    generic_c = md5(os.path.join(cdir, "folder.png"))
    generic_s = md5(os.path.join(sdir, "folder.png")) if os.path.exists(os.path.join(sdir, "folder.png")) else None
    for name in sorted(os.listdir(cdir)):
        if not name.startswith(("folder-", "user-")) or not name.endswith(".png"):
            continue
        cpath, spath = os.path.join(cdir, name), os.path.join(sdir, name)
        if not os.path.exists(spath) or md5(cpath) != generic_c:
            continue                      # Chicago95 ja tem desenho proprio aqui
        if md5(spath) in (generic_c, generic_s):
            continue                      # SE98 tambem e generico: nada a ganhar
        os.remove(cpath)                  # quebra o link pra pasta generica
        shutil.copyfile(os.path.realpath(spath), cpath)
        fixed.append(f"{size}/{name}")
print(len(fixed), "icones trocados:", ", ".join(fixed))
