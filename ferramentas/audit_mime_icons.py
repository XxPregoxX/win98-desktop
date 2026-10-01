#!/usr/bin/env python3
# Levanta os tipos de arquivo que existem na home e mostra que icone cada um recebe
# na cadeia de temas (mesma ordem de busca do KDE: nome especifico, depois o generico).
import os, collections, sys
HOME = os.path.expanduser("~"); ICONS = os.path.join(HOME, ".local/share/icons")
CHAIN = ["Chicago95", "SE98", "candy-icons", "breeze", "hicolor"]
RETRO = {"Chicago95", "SE98"}
BLANK = {"text-x-generic", "unknown", "application-octet-stream"}

globs = {}
for line in open("/usr/share/mime/globs2"):
    if line.startswith("#"): continue
    w, mime, pat = line.strip().split(":")[:3]
    if pat.startswith("*.") and "*" not in pat[2:] and "[" not in pat:
        ext = pat[2:].lower()
        if int(w) >= globs.get(ext, (0, ""))[0]: globs[ext] = (int(w), mime)
generic = dict(l.strip().split(":", 1) for l in open("/usr/share/mime/generic-icons") if ":" in l)

import hashlib
def find(name):
    """(tema, caminho) do icone, preferindo o tamanho 32 dos temas retro."""
    for t in CHAIN:
        for base in (os.path.join(ICONS, t), os.path.join("/usr/share/icons", t)):
            if t in RETRO:
                for ctx in ("mimes", "places", "apps", "devices", "categories", "status"):
                    p = os.path.join(base, ctx, "32", name + ".png")
                    if os.path.exists(p): return (t, p)
            for root, dirs, files in os.walk(base):
                for ext in (".png", ".svg"):
                    if name + ext in files: return (t, os.path.join(root, name + ext))
                dirs[:] = [d for d in dirs if not d.startswith(".")]
    return None
md5 = lambda p: hashlib.md5(open(os.path.realpath(p), "rb").read()).hexdigest()
BLANK_MD5 = set()
for t in RETRO:
    for n in BLANK | {"application-x-generic"}:
        for ctx in ("mimes", "places"):
            for size in ("16", "22", "32"):
                p = os.path.join(ICONS, t, ctx, size, n + ".png")
                if os.path.exists(p): BLANK_MD5.add(md5(p))

counts = collections.Counter()
skip = {".cache", ".local", ".config", ".mozilla", ".var", "node_modules", ".git", "venv", ".venv", "__pycache__"}
for root, dirs, files in os.walk(HOME):
    dirs[:] = [d for d in dirs if d not in skip and not d.startswith(".")]
    for f in files:
        if "." in f: counts[f.rsplit(".", 1)[1].lower()] += 1

cache = {}
rows = []
for ext, n in counts.most_common():
    if ext not in globs or n < 2: continue
    mime = globs[ext][1]; specific = mime.replace("/", "-")
    gen = generic.get(mime, mime.split("/")[0] + "-x-generic")
    for name in (specific, gen, "text-x-generic"):
        if name not in cache: cache[name] = find(name)
        if cache[name]: got = (name,) + cache[name]; break
    real = os.path.basename(os.path.realpath(got[2]))[:-4] if got[1] in RETRO else got[0]
    if got[1] not in RETRO:
        status = "FALTA"
    elif got[0] in BLANK or real in BLANK | {"application-x-generic", "application-octet-stream"}:
        status = "gener"
    else:
        status = "ok"
    ok = status
    rows.append((ok, ext, n, mime, got[0], got[1]))
order = {"FALTA": 0, "gener": 1, "ok": 2}
for st, ext, n, mime, name, theme in sorted(rows, key=lambda r: (order[r[0]], -r[2])):
    print(f"{st:<5} .{ext:<8} {n:>5} arq  {mime:<45} -> {name} ({theme})")
