#!/usr/bin/env python3
# Tipos de arquivo sem icone 98:
#  1) buracos do Chicago95: tamanhos em que o desenho e uma folha em branco (ex.: text-plain em 22/24px,
#     o tamanho do Dolphin) -> usa o desenho do SE98 quando existir;
#  2) tipos que caem fora do estilo 98 (candy/breeze) -> apontam pra um icone 98 que combine.
import hashlib, os, shutil
ICONS = os.path.expanduser("~/.local/share/icons")
C95, SE98 = os.path.join(ICONS, "Chicago95/mimes"), os.path.join(ICONS, "SE98/mimes")
SIZES = ("16", "22", "24", "32", "48")
md5 = lambda p: hashlib.md5(open(os.path.realpath(p), "rb").read()).hexdigest()

def blank_art():
    out = set()
    for theme, names, sizes in ((C95, ["text-x-generic"], ("22", "24")),
                                (C95, ["application-x-generic"], SIZES), (SE98, ["application-x-generic"], SIZES)):
        for n in names:
            for s in sizes:
                p = os.path.join(theme, s, n + ".png")
                if os.path.exists(p): out.add(md5(p))
    return out
BLANK = blank_art()

def put(dst, src):
    if os.path.lexists(dst): os.remove(dst)       # quebra links pra arte generica
    shutil.copyfile(os.path.realpath(src), dst)

# 1) buracos do Chicago95
holes = []
for s in SIZES:
    cdir, sdir = os.path.join(C95, s), os.path.join(SE98, s)
    if not (os.path.isdir(cdir) and os.path.isdir(sdir)): continue
    for f in sorted(os.listdir(cdir)):
        c, se = os.path.join(cdir, f), os.path.join(sdir, f)
        if f.endswith(".png") and os.path.exists(c) and md5(c) in BLANK and os.path.exists(se) and md5(se) not in BLANK:
            put(c, se); holes.append(f"{s}/{f[:-4]}")

# 2) tipos orfaos -> icone 98 equivalente
ALIASES = {
    "text-csv": "x-office-spreadsheet",                       # Excel 97 abria CSV
    "application-yaml": "application-x-wine-extension-ini",   # configuracao = icone de .ini
    "application-x-yaml": "application-x-wine-extension-ini",
    "text-x-yaml": "application-x-wine-extension-ini",
    "text-x-kotlin": "text-x-script", "text-x-fortran": "text-x-script", "text-x-dsrc": "text-x-script",
    "text-x-matlab": "text-x-script", "text-x-gradle": "text-x-script",
    "text-x-scss": "text-css",
    "application-vnd.android.package-archive": "package-x-generic",
    "application-pkcs7-signature": "application-certificate",
    "application-pgp-signature": "application-certificate",
    "application-xsd": "application-xml",
    "video-x-theora+ogg": "video-x-generic",
    "application-x-generic": "application-octet-stream",      # folha com a bandeira do Windows (SE98, tem 22/24px)
    "application-x-godot-resource": "application-octet-stream",
    "application-vnd.dart": "text-x-script",                  # codigo-fonte (Flutter)
    "text-x-cmake": "text-x-script", "text-x-makefile": "text-x-script",
    "application-x-navi-animation": "image-x-win-bitmap",      # .ani = cursor animado do Windows, igual ao .cur
    "application-vnd.mlt+xml": "application-xml",
    "application-x-asar": "package-x-generic",
    "application-wasm": "application-x-executable",
}
def source(name, s):
    for base in (SE98, C95) if name == "application-octet-stream" else (C95, SE98):
        for ctx in (base, base.replace("/mimes", "/places"), base.replace("/mimes", "/apps")):
            p = os.path.join(ctx, s, name + ".png")
            if os.path.exists(p) and md5(p) not in BLANK: return p
    return None
FORCE = {"application-x-generic", "application-x-godot-resource", "text-x-cmake", "text-x-makefile"}
mapped = []
for alias, target in ALIASES.items():
    for s in SIZES:
        dst = os.path.join(C95, s, alias + ".png")
        if not os.path.isdir(os.path.dirname(dst)): continue
        # ja tem desenho proprio 98 (menos os que no Chicago95 sao so link pro texto generico)
        if alias not in FORCE and os.path.exists(dst) and md5(dst) not in BLANK: continue
        src = source(target, s)
        if src: put(dst, src); mapped.append(f"{s}/{alias}")
print(len(holes), "buracos consertados:", ", ".join(holes[:12]), "..." if len(holes) > 12 else "")
print(len(mapped), "tipos mapeados:", ", ".join(sorted({m.split('/')[1] for m in mapped})))
