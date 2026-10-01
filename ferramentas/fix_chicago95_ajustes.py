#!/usr/bin/env python3
"""Últimos ajustes do Chicago95, os que foram feitos à mão e não seguem regra de outro script.

1) temas/icones/chicago95-ajustes/: desenhos finais das categorias do menu (cada uma com um ícone 98
   diferente, vários vindos do SE98), mais uns poucos ícones de app e de tipo de arquivo, e a lista
   `ajustes.txt` (`link <arquivo> <alvo>` e `apagar <arquivo>`, caminhos dentro do Chicago95).

2) Links "-symbolic": o menu e as Configurações do KDE pedem `applications-*-symbolic` e
   `preferences-*-symbolic`, que o Chicago95 não tem; sem eles caem no ícone moderno. Cria
   `<nome>-symbolic` -> `<nome>` pra todo applications-*/preferences-* de apps/, categories/ e panel/.

Rodar por último (refazer_icones.sh já chama). Mexe em terceiros/Chicago95.
"""
import os, re, shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
C95 = RAIZ / "terceiros/Chicago95"
AJ = RAIZ / "temas/icones/chicago95-ajustes"
NOME = re.compile(r"^((applications|preferences)-.+?)(\.png|\.svg)$")


def trocar(dst: Path):
    """apaga o que estiver no lugar (link, arquivo ou hardlink de outro ícone) antes de gravar"""
    if dst.is_symlink() or dst.exists():
        dst.unlink()
    dst.parent.mkdir(parents=True, exist_ok=True)


# 1) lista de links/apagados e desenhos finais
for linha in (AJ / "ajustes.txt").read_text().splitlines():
    linha = linha.strip()
    if not linha or linha.startswith("#"):
        continue
    acao, rel, *alvo = linha.split()
    dst = C95 / rel
    if acao == "apagar":
        if dst.is_symlink() or dst.exists():
            dst.unlink()
    elif acao == "link":
        trocar(dst)
        dst.symlink_to(alvo[0])

copiados = 0
base = AJ / "arquivos"
for src in sorted(base.rglob("*")):
    if src.is_file():
        dst = C95 / src.relative_to(base)
        trocar(dst)
        shutil.copy2(src, dst)
        copiados += 1

# 2) links -symbolic (depois da lista, pra valer também pros desenhos novos e não sobrar
#    link pra arquivo apagado)
links = 0
for ctx in ("apps", "categories", "panel"):
    for d in sorted((C95 / ctx).iterdir()):
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            m = NOME.match(f.name)
            if not m or m.group(1).endswith("-symbolic"):
                continue
            sym = d / f"{m.group(1)}-symbolic{m.group(3)}"
            if not sym.exists() and not sym.is_symlink():
                sym.symlink_to(f.name)
                links += 1

print(f"{links} links -symbolic, {copiados} desenhos copiados, ajustes.txt aplicado")
